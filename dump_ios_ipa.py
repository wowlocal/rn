#!/usr/bin/env python3
"""Install an authorized IPA on a jailbroken iPhone and dump a decrypted IPA.

The script is intentionally conservative: a dumped IPA is accepted as decrypted
evidence only when the dumped bundle metadata matches the source IPA and the
main executable reports cryptid 0.
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import os
import plistlib
import platform
import re
import shutil
import shlex
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_IDUMP = REPO_ROOT / "tmp" / "idump" / "idump"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "tmp" / "ios-dumps"
DEFAULT_IDUMP_VERSION = "v1.1.1"
DEFAULT_IDUMP_FRIDA = "17.9.11"
DEFAULT_EXTRACTOR_SCRIPT = REPO_ROOT / "tmp" / "tools" / "frida-ipa-extract" / "extract.py"
DEFAULT_EXTRACTOR_PYTHON = REPO_ROOT / "tmp" / "frida-venv" / "bin" / "python"
REMOTE_PATH = "/var/jb/usr/local/bin:/var/jb/usr/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"


class CommandError(RuntimeError):
    def __init__(self, message: str, result: subprocess.CompletedProcess[str] | None = None):
        super().__init__(message)
        self.result = result


def run(
    argv: list[str],
    *,
    env: dict[str, str] | None = None,
    check: bool = True,
    quiet: bool = False,
) -> subprocess.CompletedProcess[str]:
    if not quiet:
        print("$ " + " ".join(shlex.quote(part) for part in argv), flush=True)
    result = subprocess.run(argv, text=True, capture_output=True, env=env)
    if check and result.returncode != 0:
        if result.stdout:
            print(result.stdout, end="", file=sys.stderr)
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        raise CommandError(f"command failed with exit {result.returncode}: {argv[0]}", result)
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_part(value: str) -> str:
    value = value.strip() or "unknown"
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._-") or "unknown"


def first_payload_app_info(zipf: zipfile.ZipFile) -> tuple[str, dict[str, Any]]:
    candidates = [
        name
        for name in zipf.namelist()
        if name.startswith("Payload/")
        and name.count("/") == 2
        and name.endswith(".app/Info.plist")
    ]
    if not candidates:
        raise ValueError("IPA does not contain Payload/*.app/Info.plist")
    info_name = sorted(candidates)[0]
    with zipf.open(info_name) as handle:
        info = plistlib.loads(handle.read())
    app_dir = info_name.rsplit("/", 1)[0]
    return app_dir, info


def ipa_metadata(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as zipf:
        app_dir, info = first_payload_app_info(zipf)
    return {
        "path": str(path),
        "payload_app_dir": app_dir,
        "bundle_id": info.get("CFBundleIdentifier"),
        "version": info.get("CFBundleShortVersionString"),
        "build": info.get("CFBundleVersion"),
        "display_name": info.get("CFBundleDisplayName") or info.get("CFBundleName"),
        "executable": info.get("CFBundleExecutable"),
        "minimum_os": info.get("MinimumOSVersion"),
    }


def ssh_env(password: str | None) -> dict[str, str]:
    env = os.environ.copy()
    if password:
        env["SSHPASS"] = password
        # Avoid "Too many authentication failures" from agent-provided keys.
        env.pop("SSH_AUTH_SOCK", None)
    return env


def ssh_prefix(args: argparse.Namespace, password: str | None) -> list[str]:
    command: list[str] = []
    if password:
        command.extend(["sshpass", "-e"])
    command.extend(
        [
            "ssh",
            "-p",
            str(args.port),
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile=/dev/null",
        ]
    )
    if password:
        command.extend(
            [
                "-o",
                "PubkeyAuthentication=no",
                "-o",
                "PreferredAuthentications=password,keyboard-interactive",
                "-o",
                "NumberOfPasswordPrompts=1",
            ]
        )
    command.append(f"{args.user}@{args.host}")
    return command


def scp_prefix(args: argparse.Namespace, password: str | None) -> list[str]:
    command: list[str] = []
    if password:
        command.extend(["sshpass", "-e"])
    command.extend(
        [
            "scp",
            "-P",
            str(args.port),
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile=/dev/null",
        ]
    )
    if password:
        command.extend(
            [
                "-o",
                "PubkeyAuthentication=no",
                "-o",
                "PreferredAuthentications=password,keyboard-interactive",
                "-o",
                "NumberOfPasswordPrompts=1",
            ]
        )
    return command


def ssh(args: argparse.Namespace, password: str | None, remote_command: str, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(ssh_prefix(args, password) + [remote_command], env=ssh_env(password), check=check)


def scp_to_device(args: argparse.Namespace, password: str | None, local_path: Path, remote_path: str) -> None:
    target = f"{args.user}@{args.host}:{remote_path}"
    run(scp_prefix(args, password) + [str(local_path), target], env=ssh_env(password))


def resolve_install_method(args: argparse.Namespace, password: str | None) -> str:
    if args.skip_install:
        return "none"
    if args.install_method != "auto":
        return args.install_method
    if shutil.which("ideviceinstaller"):
        return "ideviceinstaller"
    return "appinst"


def ensure_tools(args: argparse.Namespace, password: str | None, install_method: str) -> None:
    if password and not shutil.which("sshpass"):
        raise RuntimeError("sshpass is required when using password authentication")
    if install_method == "appinst":
        for tool in ("ssh", "scp"):
            if not shutil.which(tool):
                raise RuntimeError(f"missing host tool: {tool}")
        ssh(
            args,
            password,
            f"export PATH={REMOTE_PATH}; command -v appinst >/dev/null || "
            "(echo 'missing device tool: appinst' >&2; exit 127)",
        )
    elif install_method == "ideviceinstaller" and not shutil.which("ideviceinstaller"):
        raise RuntimeError("missing host tool: ideviceinstaller")


def idump_path(args: argparse.Namespace) -> Path:
    if args.idump:
        return Path(args.idump)
    if DEFAULT_IDUMP.exists():
        return DEFAULT_IDUMP
    found = shutil.which("idump")
    if found:
        return Path(found)
    return DEFAULT_IDUMP


def frida_ipa_extract_python(args: argparse.Namespace) -> Path:
    if args.extractor_python:
        return Path(args.extractor_python)
    if DEFAULT_EXTRACTOR_PYTHON.exists():
        return DEFAULT_EXTRACTOR_PYTHON
    return Path(sys.executable)


def frida_ipa_extract_command(args: argparse.Namespace) -> list[str]:
    if args.extractor:
        extractor = Path(args.extractor)
        if extractor.name.endswith(".py"):
            return [str(frida_ipa_extract_python(args)), str(extractor)]
        return [str(extractor)]
    found = shutil.which("frida-ipa-extract")
    if found:
        return [found]
    if DEFAULT_EXTRACTOR_SCRIPT.exists():
        return [str(frida_ipa_extract_python(args)), str(DEFAULT_EXTRACTOR_SCRIPT)]
    raise RuntimeError(
        "frida-ipa-extract not found. Install it or pass --extractor /path/to/extract.py."
    )


def resolve_dump_method(args: argparse.Namespace) -> str:
    if args.method != "auto":
        return args.method
    has_frida_ipa_extract = (
        args.extractor
        or DEFAULT_EXTRACTOR_SCRIPT.exists()
        or shutil.which("frida-ipa-extract")
    )
    return "frida-ipa-extract" if has_frida_ipa_extract else "idump"


def download_idump(destination: Path) -> None:
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system != "darwin":
        raise RuntimeError("--download-idump currently knows only iDump's darwin release names")
    arch = "arm64" if machine in {"arm64", "aarch64"} else "amd64"
    name = f"idump-darwin-{arch}-frida-{DEFAULT_IDUMP_FRIDA}"
    url = f"https://github.com/Fi5t/iDump/releases/download/{DEFAULT_IDUMP_VERSION}/{name}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {url}", flush=True)
    with urllib.request.urlopen(url) as response, destination.open("wb") as handle:
        shutil.copyfileobj(response, handle)
    destination.chmod(0o755)


def install_ipa(
    args: argparse.Namespace,
    password: str | None,
    ipa: Path,
    install_method: str,
) -> str | None:
    if args.skip_install:
        return None
    if install_method == "ideviceinstaller":
        run(["ideviceinstaller", "install", str(ipa)])
        return None
    remote_dir = ssh(args, password, "mktemp -d /tmp/iosdump.XXXXXX").stdout.strip().splitlines()[-1]
    remote_ipa = f"{remote_dir}/input.ipa"
    scp_to_device(args, password, ipa, remote_ipa)
    quoted_ipa = shlex.quote(remote_ipa)
    ssh(args, password, f"export PATH={REMOTE_PATH}; appinst {quoted_ipa}")
    return remote_dir


def maybe_prepare_app(args: argparse.Namespace, password: str | None, metadata: dict[str, Any]) -> None:
    executable = metadata.get("executable")
    bundle_id = args.bundle_id or metadata.get("bundle_id")
    if args.kill_before_dump and executable:
        ssh(
            args,
            password,
            f"export PATH={REMOTE_PATH}; killall {shlex.quote(str(executable))} >/dev/null 2>&1 || true",
            check=False,
        )
    if args.prelaunch and bundle_id:
        ssh(args, password, f"export PATH={REMOTE_PATH}; uiopen {shlex.quote(str(bundle_id))}; sleep {args.launch_wait}", check=False)


def dump_with_idump(args: argparse.Namespace, metadata: dict[str, Any], idump: Path, output_ipa: Path) -> subprocess.CompletedProcess[str]:
    command = idump_dump_command(args, metadata, idump, output_ipa)
    output_ipa.parent.mkdir(parents=True, exist_ok=True)
    return run(command)


def idump_dump_command(args: argparse.Namespace, metadata: dict[str, Any], idump: Path, output_ipa: Path) -> list[str]:
    bundle_id = args.bundle_id or metadata.get("bundle_id")
    if not bundle_id:
        raise RuntimeError("cannot determine bundle id; pass --bundle-id")
    command = [str(idump), "-o", str(output_ipa)]
    if args.dodge != "none":
        command.append(f"--dodge={args.dodge}")
    for extra in args.idump_arg:
        command.append(extra)
    command.append(str(bundle_id))
    return command


def dump_with_frida_ipa_extract(
    args: argparse.Namespace,
    metadata: dict[str, Any],
    output_ipa: Path,
) -> subprocess.CompletedProcess[str]:
    command = frida_ipa_extract_dump_command(args, metadata, output_ipa)
    output_ipa.parent.mkdir(parents=True, exist_ok=True)
    return run(command)


def frida_ipa_extract_dump_command(args: argparse.Namespace, metadata: dict[str, Any], output_ipa: Path) -> list[str]:
    bundle_id = args.bundle_id or metadata.get("bundle_id")
    if not bundle_id:
        raise RuntimeError("cannot determine bundle id; pass --bundle-id")
    command = frida_ipa_extract_command(args)
    command.append("-U")
    if args.attach_pid is not None:
        command.extend(["--pid", str(args.attach_pid)])
    elif not args.attach_running:
        command.extend(["-f", str(bundle_id)])
    command.extend(["-o", str(output_ipa)])
    if args.no_resume and not args.attach_running and args.attach_pid is None:
        command.append("--no-resume")
    if args.all_binaries:
        command.append("--all-binaries")
    for extra in args.extractor_arg:
        command.append(extra)
    if args.attach_running and args.attach_pid is None:
        command.append(str(bundle_id))
    return command


def main_executable_cryptid(ipa: Path, metadata: dict[str, Any]) -> dict[str, Any]:
    otool = shutil.which("otool")
    executable = metadata.get("executable")
    app_dir = metadata.get("payload_app_dir")
    result: dict[str, Any] = {
        "checked": False,
        "tool": "otool",
        "executable": executable,
        "cryptid": None,
        "error": None,
    }
    if not otool:
        result["error"] = "otool not found"
        return result
    if not executable or not app_dir:
        result["error"] = "missing executable metadata"
        return result
    zip_member = f"{app_dir}/{executable}"
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        try:
            with zipfile.ZipFile(ipa) as zipf:
                zipf.extract(zip_member, temp_path)
        except KeyError:
            result["error"] = f"{zip_member} not found in dumped IPA"
            return result
        executable_path = temp_path / zip_member
        completed = run([otool, "-l", str(executable_path)], check=False, quiet=True)
    result["checked"] = True
    if completed.returncode != 0:
        result["error"] = completed.stderr.strip() or f"otool exited {completed.returncode}"
        return result
    match = re.search(r"\bcryptid\s+(\d+)", completed.stdout)
    if not match:
        result["error"] = "LC_ENCRYPTION_INFO cryptid not found"
        return result
    result["cryptid"] = int(match.group(1))
    return result


MACHO_MAGICS = {
    b"\xca\xfe\xba\xbe",  # fat, big-endian
    b"\xca\xfe\xba\xbf",  # fat64, big-endian
    b"\xbe\xba\xfe\xca",  # fat, little-endian
    b"\xbf\xba\xfe\xca",  # fat64, little-endian
    b"\xfe\xed\xfa\xce",  # 32-bit, big-endian
    b"\xce\xfa\xed\xfe",  # 32-bit, little-endian
    b"\xfe\xed\xfa\xcf",  # 64-bit, big-endian
    b"\xcf\xfa\xed\xfe",  # 64-bit, little-endian
}


def is_macho_member(zipf: zipfile.ZipFile, member: str) -> bool:
    try:
        with zipf.open(member) as handle:
            return handle.read(4) in MACHO_MAGICS
    except (KeyError, OSError, zipfile.BadZipFile):
        return False


def macho_category(member: str, metadata: dict[str, Any]) -> str:
    app_dir = str(metadata.get("payload_app_dir") or "")
    executable = str(metadata.get("executable") or "")
    if app_dir and executable and member == f"{app_dir}/{executable}":
        return "main_executable"
    if ".appex/" in member:
        return "app_extension"
    if "/Frameworks/" in member:
        return "framework_or_dylib"
    if member.endswith(".dylib"):
        return "framework_or_dylib"
    return "other_macho"


def macho_encryption_info(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "checked": False,
        "tool": "otool",
        "cryptids": [],
        "error": None,
    }
    otool = shutil.which("otool")
    if not otool:
        result["error"] = "otool not found"
        return result
    completed = run([otool, "-l", str(path)], check=False, quiet=True)
    result["checked"] = True
    if completed.returncode != 0:
        result["error"] = completed.stderr.strip() or f"otool exited {completed.returncode}"
        return result
    result["cryptids"] = [int(value) for value in re.findall(r"\bcryptid\s+(\d+)", completed.stdout)]
    if not result["cryptids"]:
        result["error"] = "LC_ENCRYPTION_INFO cryptid not found"
    return result


def macho_cryptid_inventory(ipa: Path, metadata: dict[str, Any]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        with zipfile.ZipFile(ipa) as zipf:
            for index, member in enumerate(sorted(zipf.namelist())):
                info = zipf.getinfo(member)
                if info.is_dir() or not is_macho_member(zipf, member):
                    continue
                extracted = temp_path / f"macho-{index}"
                with zipf.open(member) as src, extracted.open("wb") as dst:
                    shutil.copyfileobj(src, dst)
                encryption = macho_encryption_info(extracted)
                cryptids = encryption.get("cryptids") or []
                entries.append(
                    {
                        "member": member,
                        "category": macho_category(member, metadata),
                        "size": info.file_size,
                        "checked": encryption["checked"],
                        "cryptids": cryptids,
                        "cryptid": max(cryptids) if cryptids else None,
                        "encrypted": any(value != 0 for value in cryptids) if cryptids else None,
                        "error": encryption["error"],
                    }
                )

    encrypted = [entry for entry in entries if entry.get("encrypted") is True]
    unknown = [entry for entry in entries if not entry.get("cryptids")]
    by_category: dict[str, int] = {}
    for entry in entries:
        category = str(entry["category"])
        by_category[category] = by_category.get(category, 0) + 1
    return {
        "tool": "otool",
        "mach_o_count": len(entries),
        "encrypted_count": len(encrypted),
        "unknown_cryptid_count": len(unknown),
        "counts_by_category": by_category,
        "entries": entries,
    }


def classify_decrypted_coverage(
    accepted: bool,
    inventory: dict[str, Any],
) -> dict[str, Any]:
    entries = inventory.get("entries") or []
    encrypted = [entry for entry in entries if entry.get("encrypted") is True]
    unknown = [entry for entry in entries if not entry.get("cryptids")]
    encrypted_non_extension = [
        entry for entry in encrypted if entry.get("category") != "app_extension"
    ]
    unknown_non_extension = [
        entry for entry in unknown if entry.get("category") != "app_extension"
    ]
    encrypted_extensions = [
        entry for entry in encrypted if entry.get("category") == "app_extension"
    ]
    unknown_extensions = [
        entry for entry in unknown if entry.get("category") == "app_extension"
    ]

    if not accepted:
        coverage_class = "rejected"
    elif not encrypted and not unknown:
        coverage_class = "full_bundle_decrypted"
    elif not encrypted_non_extension and not unknown_non_extension and (
        encrypted_extensions or unknown_extensions
    ):
        coverage_class = "loaded_app_decrypted"
    else:
        coverage_class = "main_only_decrypted"

    return {
        "coverage_class": coverage_class,
        "encrypted_members": [entry["member"] for entry in encrypted],
        "unknown_cryptid_members": [entry["member"] for entry in unknown],
        "remaining_encrypted_appex_members": [
            entry["member"] for entry in encrypted_extensions
        ],
        "remaining_encrypted_non_extension_members": [
            entry["member"] for entry in encrypted_non_extension
        ],
    }


def device_context(args: argparse.Namespace, password: str | None) -> dict[str, str]:
    if shutil.which("ideviceinfo"):
        key_map = {
            "product_version": "ProductVersion",
            "product_build": "BuildVersion",
            "hardware_model": "HardwareModel",
            "device_name": "DeviceName",
        }
        context: dict[str, str] = {}
        for output_key, info_key in key_map.items():
            result = run(["ideviceinfo", "-k", info_key], check=False, quiet=True)
            if result.returncode == 0:
                context[output_key] = result.stdout.strip()
            else:
                context[f"{output_key}_error"] = result.stderr.strip() or f"exit {result.returncode}"
        return context

    commands = {
        "product_version": "/usr/bin/plutil -extract ProductVersion raw /System/Library/CoreServices/SystemVersion.plist",
        "product_build": "/usr/bin/plutil -extract ProductBuildVersion raw /System/Library/CoreServices/SystemVersion.plist",
        "hardware_model": "sysctl -n hw.model",
        "kernel": "uname -a",
    }
    context: dict[str, str] = {}
    for key, command in commands.items():
        result = ssh(args, password, f"export PATH={REMOTE_PATH}; {command}", check=False)
        if result.returncode == 0:
            context[key] = result.stdout.strip()
        else:
            context[f"{key}_error"] = result.stderr.strip() or f"exit {result.returncode}"
    return context


def metadata_matches(source: dict[str, Any], dumped: dict[str, Any]) -> dict[str, bool]:
    keys = ("bundle_id", "version", "build")
    return {key: bool(source.get(key) and source.get(key) == dumped.get(key)) for key in keys}


def default_output_path(args: argparse.Namespace, metadata: dict[str, Any], method: str) -> Path:
    if args.output:
        return Path(args.output)
    name = "_".join(
        safe_part(str(metadata.get(key) or "unknown"))
        for key in ("bundle_id", "version", "build")
    )
    return Path(args.output_dir) / f"{name}_{safe_part(method)}.ipa"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install an IPA on a jailbroken iPhone and dump a decrypted IPA.",
    )
    parser.add_argument("ipa", type=Path, help="Authorized source IPA to install and dump")
    parser.add_argument(
        "--method",
        choices=("auto", "frida-ipa-extract", "idump"),
        default="auto",
        help="Dump implementation to use",
    )
    parser.add_argument("--host", default="127.0.0.1", help="SSH host for the phone")
    parser.add_argument("--port", type=int, default=2222, help="SSH port for the phone")
    parser.add_argument("--user", default="mobile", help="SSH user")
    parser.add_argument("--password-env", default="IOS_SSH_PASSWORD", help="Environment variable containing SSH password")
    parser.add_argument("--ask-pass", action="store_true", help="Prompt for SSH password")
    parser.add_argument("--idump", help="Path to idump binary; defaults to tmp/idump/idump or PATH")
    parser.add_argument(
        "--download-idump",
        action="store_true",
        help="Download iDump into tmp/idump/idump if using iDump and missing",
    )
    parser.add_argument("--extractor", help="Path to frida-ipa-extract command or extract.py")
    parser.add_argument("--extractor-python", help="Python interpreter for --extractor extract.py")
    parser.add_argument(
        "--extractor-arg",
        action="append",
        default=[],
        help="Extra argument passed to frida-ipa-extract; repeatable",
    )
    parser.add_argument(
        "--resume-after-spawn",
        dest="no_resume",
        action="store_false",
        help="Do not pass --no-resume to frida-ipa-extract",
    )
    parser.set_defaults(no_resume=True)
    parser.add_argument(
        "--attach-running",
        action="store_true",
        help="Attach frida-ipa-extract to a running app by bundle id instead of spawning it",
    )
    parser.add_argument("--attach-pid", type=int, help="Attach frida-ipa-extract to a specific running process id")
    parser.add_argument(
        "--all-binaries",
        action="store_true",
        help="Pass --all-binaries to a patched frida-ipa-extract dumper",
    )
    parser.add_argument("--bundle-id", help="Override bundle identifier")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for dumped IPA")
    parser.add_argument("--output", type=Path, help="Exact dumped IPA output path")
    parser.add_argument("--report", type=Path, help="JSON verification report path; defaults next to output IPA")
    parser.add_argument("--skip-install", action="store_true", help="Dump currently installed app without installing IPA")
    parser.add_argument(
        "--install-method",
        choices=("auto", "appinst", "ideviceinstaller"),
        default="auto",
        help="IPA install backend; auto prefers ideviceinstaller when available",
    )
    parser.add_argument(
        "--no-kill-before-dump",
        dest="kill_before_dump",
        action="store_false",
        help="Do not kill the app before dumping",
    )
    parser.set_defaults(kill_before_dump=True)
    parser.add_argument("--prelaunch", action="store_true", help="Launch app with uiopen before iDump")
    parser.add_argument("--launch-wait", type=int, default=3, help="Seconds to wait after --prelaunch")
    parser.add_argument(
        "--dodge",
        choices=("none", "basic", "advanced"),
        default="none",
        help="Pass iDump anti-Frida bypass mode; iDump only",
    )
    parser.add_argument("--idump-arg", action="append", default=[], help="Extra argument passed to iDump; repeatable")
    parser.add_argument("--keep-remote-temp", action="store_true", help="Do not delete remote temp dir after install")
    parser.add_argument("--allow-encrypted-output", action="store_true", help="Exit 0 even if cryptid is not 0")
    parser.add_argument("--dry-run", action="store_true", help="Print metadata and planned output without installing or dumping")
    args = parser.parse_args()
    if args.attach_running and args.attach_pid is not None:
        parser.error("--attach-running and --attach-pid are mutually exclusive")
    return args


def main() -> int:
    args = parse_args()
    ipa = args.ipa.expanduser().resolve()
    if not ipa.exists():
        print(f"IPA not found: {ipa}", file=sys.stderr)
        return 2

    password = os.environ.get(args.password_env)
    if args.ask_pass and not password:
        password = getpass.getpass(f"SSH password for {args.user}@{args.host}:{args.port}: ")

    source_metadata = ipa_metadata(ipa)
    if args.bundle_id:
        source_metadata["bundle_id"] = args.bundle_id
    method = resolve_dump_method(args)
    install_method = resolve_install_method(args, password)
    source = {
        **source_metadata,
        "path": str(ipa),
        "size": ipa.stat().st_size,
        "sha256": sha256(ipa),
    }
    output_ipa = default_output_path(args, source_metadata, method).resolve()
    report_path = (args.report or output_ipa.with_suffix(output_ipa.suffix + ".json")).resolve()
    idump = idump_path(args).resolve() if method == "idump" else None

    print(
        json.dumps(
            {
                "source": source,
                "method": method,
                "install_method": install_method,
                "output_ipa": str(output_ipa),
                "report": str(report_path),
            },
            indent=2,
        ),
        flush=True,
    )
    if args.dry_run:
        return 0

    remote_dir: str | None = None
    dump_result: subprocess.CompletedProcess[str] | None = None
    report: dict[str, Any] = {
        "source": source,
        "device": {"host": args.host, "port": args.port, "user": args.user},
        "installer": {"method": install_method},
        "dumper": {"method": method, "all_binaries": bool(args.all_binaries)},
        "output": {"path": str(output_ipa)},
        "verification": {},
    }
    try:
        try:
            ensure_tools(args, password, install_method)
            report["device"]["context"] = device_context(args, password)
            remote_dir = install_ipa(args, password, ipa, install_method)
            maybe_prepare_app(args, password, source_metadata)
            if method == "frida-ipa-extract":
                report["dumper"]["command"] = frida_ipa_extract_dump_command(args, source_metadata, output_ipa)
                dump_result = dump_with_frida_ipa_extract(args, source_metadata, output_ipa)
            else:
                if idump is None:
                    raise RuntimeError("internal error: iDump path was not initialized")
                if args.download_idump and not idump.exists():
                    download_idump(idump)
                if not idump.exists():
                    raise RuntimeError(f"iDump not found: {idump}. Pass --idump or use --download-idump.")
                if not os.access(idump, os.X_OK):
                    idump.chmod(idump.stat().st_mode | 0o111)
                report["dumper"]["path"] = str(idump)
                report["dumper"]["command"] = idump_dump_command(args, source_metadata, idump, output_ipa)
                dump_result = dump_with_idump(args, source_metadata, idump, output_ipa)
        except CommandError as exc:
            if exc.result:
                report["dumper"]["stdout"] = exc.result.stdout
                report["dumper"]["stderr"] = exc.result.stderr
                report["dumper"]["returncode"] = exc.result.returncode
            report["verification"]["accepted_decrypted_evidence"] = False
            report["verification"]["error"] = str(exc)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(json.dumps(report, indent=2) + "\n")
            print(f"Report: {report_path}", file=sys.stderr)
            return 1
    finally:
        if remote_dir and not args.keep_remote_temp:
            ssh(args, password, f"rm -rf {shlex.quote(remote_dir)}", check=False)

    if dump_result:
        report["dumper"]["stdout"] = dump_result.stdout
        report["dumper"]["stderr"] = dump_result.stderr
        report["dumper"]["returncode"] = dump_result.returncode

    if not output_ipa.exists():
        report["verification"]["accepted_decrypted_evidence"] = False
        report["verification"]["error"] = "dumper did not create output IPA"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + "\n")
        print(f"Report: {report_path}", file=sys.stderr)
        return 1

    dumped_metadata = ipa_metadata(output_ipa)
    matches = metadata_matches(source_metadata, dumped_metadata)
    crypt = main_executable_cryptid(output_ipa, dumped_metadata)
    accepted = all(matches.values()) and crypt.get("cryptid") == 0
    inventory = macho_cryptid_inventory(output_ipa, dumped_metadata)
    coverage = classify_decrypted_coverage(accepted, inventory)
    report["output"].update(
        {
            "size": output_ipa.stat().st_size,
            "sha256": sha256(output_ipa),
            "metadata": dumped_metadata,
        }
    )
    report["verification"].update(
        {
            "metadata_matches": matches,
            "main_executable_encryption": crypt,
            "mach_o_cryptid_inventory": inventory,
            "decrypted_coverage": coverage,
            "accepted_decrypted_evidence": accepted,
        }
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n")

    print(f"Dumped IPA: {output_ipa}")
    print(f"Report: {report_path}")
    print(f"Metadata matches: {matches}")
    print(f"Main executable cryptid: {crypt.get('cryptid')}")
    print(f"Decrypted coverage: {coverage['coverage_class']}")
    if not accepted:
        print("Rejected as decrypted evidence: metadata mismatch or cryptid is not 0.", file=sys.stderr)
        return 0 if args.allow_encrypted_output else 1
    print("Accepted as decrypted evidence.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CommandError, RuntimeError, ValueError, zipfile.BadZipFile) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
