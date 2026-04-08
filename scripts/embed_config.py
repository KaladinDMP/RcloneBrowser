#!/usr/bin/env python3
"""Embed an rclone configuration (and optional password) into the build.

Usage:

    python3 scripts/embed_config.py path/to/rclone.conf [config_password]

The script reads the supplied rclone.conf, generates a fresh random XOR
key, obfuscates the bytes (and optionally the rclone config password),
and rewrites src/embedded_config.h so the next build will bake the
configuration into the binary.

This is *obfuscation*, not real encryption: anyone with the binary and
enough patience can recover the key and decode the blob. It is meant to
keep the config out of the hands of casual end-users of the application.
"""
from __future__ import annotations

import os
import secrets
import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HEADER_PATH = REPO_ROOT / "src" / "embedded_config.h"
KEY_LENGTH = 32


def format_byte_array(data: bytes, indent: str = "    ") -> str:
    """Format raw bytes as a C-style array literal, 12 bytes per line."""
    if not data:
        return "0x00"
    lines = []
    chunk_size = 12
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        lines.append(", ".join(f"0x{b:02x}" for b in chunk))
    return (",\n" + indent).join(lines)


def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def main() -> int:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(__doc__)
        return 2

    config_path = Path(sys.argv[1])
    password = sys.argv[2] if len(sys.argv) == 3 else ""

    if not config_path.is_file():
        print(f"error: {config_path} does not exist or is not a file",
              file=sys.stderr)
        return 1

    config_bytes = config_path.read_bytes()
    key = secrets.token_bytes(KEY_LENGTH)
    obf_config = xor_bytes(config_bytes, key)
    pwd_bytes = password.encode("utf-8") if password else b""
    obf_pwd = xor_bytes(pwd_bytes, key)

    key_array = format_byte_array(key)
    config_array = format_byte_array(obf_config)
    pwd_array = format_byte_array(obf_pwd) if obf_pwd else "0x00"

    header = textwrap.dedent(
        f"""\
        #pragma once

        // GENERATED FILE - do not edit by hand. Regenerate with:
        //
        //     python3 scripts/embed_config.py path/to/rclone.conf [password]
        //
        // The contents below are an XOR-obfuscated copy of the embedded
        // rclone configuration. See utils.cpp::LoadEmbeddedConfig() for the
        // runtime decoding logic and embedded_config.h's history for the
        // intent.

        namespace embedded_config {{

        static const unsigned char kEmbeddedConfigKey[] = {{
            {key_array}}};
        static const unsigned int kEmbeddedConfigKeySize =
            sizeof(kEmbeddedConfigKey) / sizeof(kEmbeddedConfigKey[0]);

        static const unsigned char kEmbeddedConfig[] = {{
            {config_array}}};
        static const unsigned int kEmbeddedConfigSize =
            sizeof(kEmbeddedConfig) / sizeof(kEmbeddedConfig[0]);

        static const unsigned char kEmbeddedConfigPassword[] = {{
            {pwd_array}}};
        static const unsigned int kEmbeddedConfigPasswordSize = {len(pwd_bytes)};

        }} // namespace embedded_config
        """
    )

    HEADER_PATH.write_text(header)
    print(
        f"Wrote {HEADER_PATH.relative_to(REPO_ROOT)} "
        f"({len(config_bytes)} byte config, "
        f"{len(pwd_bytes)} byte password)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
