#pragma once

// Embedded rclone configuration support.
//
// The arrays below hold an obfuscated rclone configuration file and an
// optional rclone config password. The contents are XOR-obfuscated with
// `kEmbeddedConfigKey` and stored as raw bytes so the plain text never
// appears in the binary.
//
// At application startup, utils.cpp::LoadEmbeddedConfig() decrypts the
// blob into a temporary file with restricted permissions, points the
// rclone wrapper at that file and (if present) sets RCLONE_CONFIG_PASS
// from the obfuscated password before any rclone process is launched.
// CleanupEmbeddedConfig() removes the temp file at shutdown.
//
// IMPORTANT
// =========
// This is *obfuscation*, not real encryption: anyone with the binary and
// enough patience can recover the key and decode the blob. It is meant
// to keep the config out of the hands of casual users of the application.
//
// To embed a real configuration, run:
//
//     python3 scripts/embed_config.py path/to/rclone.conf [password]
//
// from the repository root. That script will overwrite this file with the
// XOR-obfuscated bytes.
//
// When kEmbeddedConfigSize is 0 the application falls back to the user's
// configured rclone.conf path from preferences (legacy behaviour).

namespace embedded_config {

// XOR key bytes used to obfuscate the config and password. Replace with
// fresh random bytes whenever you regenerate the embedded config.
static const unsigned char kEmbeddedConfigKey[] = {
    0x52, 0x43, 0x4c, 0x4f, 0x4e, 0x45, 0x42, 0x52, 0x4f, 0x57, 0x53, 0x45,
    0x52, 0x4f, 0x42, 0x46, 0x55, 0x53, 0x43, 0x41, 0x54, 0x49, 0x4f, 0x4e,
    0x4b, 0x45, 0x59, 0x21, 0x21, 0x21, 0x21, 0x21};
static const unsigned int kEmbeddedConfigKeySize =
    sizeof(kEmbeddedConfigKey) / sizeof(kEmbeddedConfigKey[0]);

// Obfuscated rclone.conf bytes. Empty by default; replaced by
// scripts/embed_config.py with the user's actual config.
static const unsigned char kEmbeddedConfig[] = {0x00};
static const unsigned int kEmbeddedConfigSize = 0;

// Obfuscated rclone config password (used only when the embedded config
// itself is rclone-encrypted with `rclone config password`). Empty by
// default.
static const unsigned char kEmbeddedConfigPassword[] = {0x00};
static const unsigned int kEmbeddedConfigPasswordSize = 0;

} // namespace embedded_config
