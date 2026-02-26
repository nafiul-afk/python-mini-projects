# Advanced Text Editor

A professional, feature-rich text editor built with Python and Tkinter for Linux systems.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.6+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## Features

### File Management
- New, Open, Save, Save As
- Recent files menu (last 10 files)
- Multiple file format support (.txt, .py, .js, .html, .css, etc.)
- Unsaved changes warning
- Auto-save functionality

### Editing
- Unlimited Undo/Redo
- Cut, Copy, Paste
- Select All
- Find and Replace with navigation
- Go to Line

### View & Display
- Line numbers (toggle)
- Word wrap (toggle)
- Zoom In/Out/Reset
- Dark/Light theme toggle
- Status bar with live stats

### Formatting
- Font chooser
- Text color picker
- Background color picker
- Text case conversion (Upper/Lower/Title)

### Tools
- Word count
- Character count
- Insert date/time
- Auto-save (5-minute interval)

### Keyboard Shortcuts
- `Ctrl+N` - New File
- `Ctrl+O` - Open File
- `Ctrl+S` - Save
- `Ctrl+Shift+S` - Save As
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Ctrl+F` - Find
- `Ctrl+H` - Replace
- `Ctrl+G` - Go to Line
- `Ctrl+D` - Toggle Dark Mode
- `Ctrl++` / `Ctrl+-` - Zoom In/Out
- `F5` - Insert Date/Time
- And many more!

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python)
- Linux operating system (tested on Ubuntu, Mint, Fedora)

## Installation

### Method 1: Quick Install (Recommended)

```bash
# Clone or download the repository
cd Text-Editor
# Make the install script executable
chmod +x install.sh

# Install for current user
./install.sh

# OR install system-wide (requires sudo)
sudo ./install.sh
```

After installation, you can:
- Launch from your application menu
- Run `text-editor` from terminal
- Right-click text files → Open With → Advanced Text Editor

### Method 2: Run Directly

```bash
# Make the script executable
chmod +x app.py

# Run the application
./app.py
```

### Method 3: Python Package Install

```bash
# Install using pip
pip install -e .

# Run from anywhere
text-editor
```

## Usage

### Launching the Editor

**From Application Menu:**
- Search for "Advanced Text Editor" in your application launcher

**From Terminal:**
```bash
text-editor
```

**From File Manager:**
- Right-click any text file
- Select "Open With" → "Advanced Text Editor"

### Quick Start Guide

1. **Create a new file**: Click "📄 New" or press `Ctrl+N`
2. **Open existing file**: Click "📂 Open" or press `Ctrl+O`
3. **Save your work**: Click "💾 Save" or press `Ctrl+S`
4. **Toggle dark mode**: Press `Ctrl+D` for comfortable night editing
5. **Find text**: Press `Ctrl+F` to search in your document
6. **Check word count**: Go to Tools → Word Count

## Customization

### Changing Themes
- Press `Ctrl+D` to toggle between light and dark themes
- Use Format → Text Color to customize text color
- Use Format → Background Color to customize background

### Changing Fonts
- Go to Format → Font
- Select from available system fonts
- Use `Ctrl++` and `Ctrl+-` to adjust size

### Auto-Save
- Enable via Tools → Auto-Save
- Automatically saves every 5 minutes
- Only works when file has a saved location

## Uninstallation

```bash
# Make uninstall script executable
chmod +x uninstall.sh

# Uninstall (use sudo if installed system-wide)
./uninstall.sh
```

## Project Structure

```
n/
├── app.py                  # Main application
├── setup.py               # Python package setup
├── install.sh             # Installation script
├── uninstall.sh           # Uninstallation script
├── text-editor.desktop    # Desktop entry file
├── icon.png              # Application icon (generated)
└── README.md             # This file
```

## Troubleshooting

### Application doesn't appear in menu
```bash
# Update desktop database
update-desktop-database ~/.local/share/applications
```

### Icon not showing
```bash
# Update icon cache
gtk-update-icon-cache ~/.local/share/icons/hicolor
```

### Command not found: text-editor
Make sure `~/.local/bin` is in your PATH:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests


## Acknowledgments

- Built with Python and Tkinter
- Inspired by modern text editors like Notepad++, Sublime Text, and VS Code

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Enjoy your new text editor!** 


