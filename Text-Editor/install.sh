#!/bin/bash

# Installation script for Advanced Text Editor
# This script installs the text editor system-wide on Linux

set -e  # Exit on error

echo "========================================="
echo "Advanced Text Editor - Installation"
echo "========================================="
echo ""

# Check if running as root for system-wide installation
if [ "$EUID" -eq 0 ]; then 
    INSTALL_TYPE="system"
    INSTALL_DIR="/usr/local/bin"
    DESKTOP_DIR="/usr/share/applications"
    ICON_DIR="/usr/share/icons/hicolor/256x256/apps"
    echo "Installing system-wide (requires root)..."
else
    INSTALL_TYPE="user"
    INSTALL_DIR="$HOME/.local/bin"
    DESKTOP_DIR="$HOME/.local/share/applications"
    ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
    echo "Installing for current user only..."
fi

echo ""

# Create directories if they don't exist
mkdir -p "$INSTALL_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Copy the main application
echo "→ Installing application..."
cp "$SCRIPT_DIR/app.py" "$INSTALL_DIR/text-editor"
chmod +x "$INSTALL_DIR/text-editor"

# Generate icon if it doesn't exist
if [ ! -f "$SCRIPT_DIR/icon.png" ]; then
    echo "→ Generating application icon..."
    # Create a simple icon using ImageMagick if available
    if command -v convert &> /dev/null; then
        convert -size 256x256 xc:white \
                -font DejaVu-Sans -pointsize 72 -fill black \
                -gravity center -annotate +0+0 "T" \
                "$SCRIPT_DIR/icon.png" 2>/dev/null || echo "  (Icon generation skipped)"
    fi
fi

# Copy icon if it exists
if [ -f "$SCRIPT_DIR/icon.png" ]; then
    echo "→ Installing icon..."
    cp "$SCRIPT_DIR/icon.png" "$ICON_DIR/text-editor.png"
fi

# Create desktop entry
echo "→ Creating desktop entry..."
cat > "$DESKTOP_DIR/text-editor.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Advanced Text Editor
Comment=A feature-rich text editor with modern features
Exec=$INSTALL_DIR/text-editor %F
Icon=text-editor
Terminal=false
Categories=Utility;TextEditor;Development;
Keywords=text;editor;notepad;
StartupNotify=true
MimeType=text/plain;text/x-python;text/x-javascript;text/html;text/css;application/x-shellscript;
EOF

chmod +x "$DESKTOP_DIR/text-editor.desktop"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    echo "→ Updating desktop database..."
    if [ "$INSTALL_TYPE" = "system" ]; then
        update-desktop-database /usr/share/applications 2>/dev/null || true
    else
        update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
    fi
fi

# Update icon cache
if command -v gtk-update-icon-cache &> /dev/null; then
    echo "→ Updating icon cache..."
    if [ "$INSTALL_TYPE" = "system" ]; then
        gtk-update-icon-cache /usr/share/icons/hicolor 2>/dev/null || true
    else
        gtk-update-icon-cache "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
    fi
fi

echo ""
echo "========================================="
echo "✓ Installation Complete!"
echo "========================================="
echo ""
echo "You can now:"
echo "  1. Launch from application menu: 'Advanced Text Editor'"
echo "  2. Run from terminal: 'text-editor'"
echo "  3. Right-click text files → Open With → Advanced Text Editor"
echo ""

if [ "$INSTALL_TYPE" = "user" ]; then
    echo "Note: Make sure $INSTALL_DIR is in your PATH"
    if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        echo ""
        echo "To add it, run:"
        echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
        echo "  source ~/.bashrc"
        echo ""
    fi
fi

echo "Enjoy your new text editor! 🎉"
