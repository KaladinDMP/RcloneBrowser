#pragma once

#include "pch.h"

std::unique_ptr<QSettings> GetSettings();

void ReadSettings(QSettings *settings, QObject *widget);
void WriteSettings(QSettings *settings, QObject *widget);

bool IsPortableMode();

QString GetRclone();
void SetRclone(const QString &rclone);

QStringList GetRcloneConf();
void SetRcloneConf(const QString &rcloneConf);

void UseRclonePassword(QProcess *process);
void SetRclonePassword(const QString &rclonePassword);

QStringList GetDefaultOptionsList(const QString &settingsOptions);
QStringList GetRemoteModeRcloneOptions();
QStringList GetShowHidden();
QStringList GetRcloneCmd(const QStringList &args);

QDir GetConfigDir(void);

// Decrypts the obfuscated rclone configuration embedded in
// embedded_config.h, writes it to a temporary file with restricted
// permissions, and points the rclone wrapper at that file. If an
// embedded config password is present it is also decoded and supplied
// via RCLONE_CONFIG_PASS for every rclone process.
// Returns true if an embedded config was loaded successfully.
bool LoadEmbeddedConfig();

// Removes the temporary file written by LoadEmbeddedConfig(). Safe to
// call even when no embedded config was loaded.
void CleanupEmbeddedConfig();

// True when LoadEmbeddedConfig() successfully loaded an embedded config
// (used to lock down the preferences UI so users cannot override it).
bool HasEmbeddedConfig();

unsigned int compareVersion(std::string, std::string);
