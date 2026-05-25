#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from check_rn_versions import DISCORD_APP_ID, DISCORD_BUNDLE_ID, main


if __name__ == "__main__":
    raise SystemExit(
        main(
            default_app_id=DISCORD_APP_ID,
            default_bundle_id=DISCORD_BUNDLE_ID,
            default_app_slug="discord",
            default_app_name="Discord",
            default_download_dir=Path("discord-ipas"),
            default_report=Path("discord-rn-versions"),
            default_version_list_out=Path("discord-ipas/discord-version-list.json"),
            default_fallback_ipas=[Path("Discord.ipa")],
            description=(
                "Download Discord iOS app versions with ipatool and infer "
                "React Native versions from the IPAs."
            ),
        )
    )
