#!/bin/bash

# Uninstallation script for Advanced Text Editor

set -e

echo "========================================="
echo "Advanced Text Editor - Uninstallation"
echo "========================================="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    INSTALL_TYPE="system"
    INSTALL_DIR="/usr/local/bin"
    DESKTOP_DIR="/usr/share/applications"
    ICON_DIR="/usr/share/icons/hicolor/256x256/apps"
    echo "Uninstalling system-wide installation..."
else
    INSTALL_TYPE="user"
    INSTALL_DIR="$HOME/.local/bin"
    DESKTOP_DIR="$HOME/.local/share/applications"
    ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
    echo "Uninstalling user installation..."
fi

echo ""

# Remove files
FILES_REMOVED=0

if [ -f "$INSTALL_DIR/text-editor" ]; then
    echo "→ Removing application..."
    rm -f "$INSTALL_DIR/text-editor"
    FILES_REMOVED=$((FILES_REMOVED + 1))
fi

if [ -f "$DESKTOP_DIR/text-editor.desktop" ]; then
    echo "→ Removing desktop entry..."
    rm -f "$DESKTOP_DIR/text-editor.desktop"
    FILES_REMOVED=$((FILES_REMOVED + 1))
fi

if [ -f "$ICON_DIR/text-editor.png" ]; then
    echo "→ Removing icon..."
    rm -f "$ICON_DIR/text-editor.png"
    FILES_REMOVED=$((FILES_REMOVED + 1))
fi

# Remove config file (optional - ask user)
CONFIG_FILE="$HOME/.text_editor_recent.json"
if [ -f "$CONFIG_FILE" ]; then
    read -p "Remove configuration file (recent files)? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f "$CONFIG_FILE"
        echo "→ Configuration file removed"
        FILES_REMOVED=$((FILES_REMOVED + 1))
    fi
fi

# Update caches
if command -v update-desktop-database &> /dev/null; then
    echo "→ Updating desktop database..."
    if [ "$INSTALL_TYPE" = "system" ]; then
        update-desktop-database /usr/share/applications 2>/dev/null || true
    else
        update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
    fi
fi

if command -v gtk-update-icon-cache &> /dev/null; then
    echo "→ Updating icon cache..."
    if [ "$INSTALL_TYPE" = "system" ]; then
        gtk-update-icon-cache /usr/share/icons/hicolor 2>/dev/null || true
    else
        gtk-update-icon-cache "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
    fi
fi

echo ""
if [ $FILES_REMOVED -gt 0 ]; then
    echo "========================================="
    echo "✓ Uninstallation Complete!"
    echo "========================================="
    echo ""
    echo "Advanced Text Editor has been removed."
else
    echo "========================================="
    echo "No installation found"
    echo "========================================="
fi
