#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from summarize_rn_timeline import main


if __name__ == "__main__":
    raise SystemExit(
        main(
            default_report=Path("discord-rn-versions.csv"),
            default_out_prefix=Path("discord-rn-timeline"),
            description="Summarize Discord IPA React Native version ranges.",
        )
    )
