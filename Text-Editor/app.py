import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font, colorchooser
from tkinter.scrolledtext import ScrolledText
import os
import re
from datetime import datetime
import json

class AdvancedTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Text Editor")
        self.root.geometry("1200x800")
        
        # File management
        self.current_file = None
        self.is_modified = False
        self.recent_files = self.load_recent_files()
        
        # Theme settings
        self.dark_mode = False
        self.current_font_family = "Consolas"
        self.current_font_size = 12
        
        # Find/Replace state
        self.find_window = None
        self.last_search = ""
        self.search_index = "1.0"
        
        # Undo/Redo stacks
        self.undo_stack = []
        self.redo_stack = []
        self.max_undo = 100
        
        # Auto-save
        self.auto_save_enabled = False
        self.auto_save_interval = 300000  # 5 minutes
        self.auto_save_job = None
        
        # Line numbers
        self.show_line_numbers = True
        
        # Setup UI
        self.setup_menu()
        self.setup_toolbar()
        self.setup_editor()
        self.setup_status_bar()
        self.setup_shortcuts()
        
        # Protocol for window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start auto-save if enabled
        if self.auto_save_enabled:
            self.schedule_auto_save()
    
    def setup_menu(self):
        """Create menu bar with all options"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        
        # Recent Files submenu
        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Recent Files", menu=self.recent_menu)
        self.update_recent_menu()
        
        file_menu.add_separator()
        file_menu.add_command(label="Print", command=self.print_file, accelerator="Ctrl+P")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Ctrl+Q")
        
        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.show_find_dialog, accelerator="Ctrl+F")
        edit_menu.add_command(label="Replace", command=self.show_replace_dialog, accelerator="Ctrl+H")
        edit_menu.add_command(label="Go to Line", command=self.go_to_line, accelerator="Ctrl+G")
        
        # View Menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self.zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", command=self.zoom_out, accelerator="Ctrl+-")
        view_menu.add_command(label="Reset Zoom", command=self.reset_zoom, accelerator="Ctrl+0")
        view_menu.add_separator()
        view_menu.add_checkbutton(label="Line Numbers", command=self.toggle_line_numbers, 
                                   variable=tk.BooleanVar(value=self.show_line_numbers))
        view_menu.add_checkbutton(label="Word Wrap", command=self.toggle_word_wrap)
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_theme, accelerator="Ctrl+D")
        
        # Format Menu
        format_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Format", menu=format_menu)
        format_menu.add_command(label="Font...", command=self.choose_font)
        format_menu.add_command(label="Text Color...", command=self.choose_text_color)
        format_menu.add_command(label="Background Color...", command=self.choose_bg_color)
        format_menu.add_separator()
        format_menu.add_command(label="Uppercase", command=self.to_uppercase)
        format_menu.add_command(label="Lowercase", command=self.to_lowercase)
        format_menu.add_command(label="Title Case", command=self.to_titlecase)
        
        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Word Count", command=self.show_word_count)
        tools_menu.add_command(label="Character Count", command=self.show_char_count)
        tools_menu.add_separator()
        tools_menu.add_checkbutton(label="Auto-Save", command=self.toggle_auto_save,
                                    variable=tk.BooleanVar(value=self.auto_save_enabled))
        tools_menu.add_command(label="Insert Date/Time", command=self.insert_datetime, accelerator="F5")
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_command(label="About", command=self.show_about)
    
    def setup_toolbar(self):
        """Create toolbar with quick access buttons"""
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # New button
        btn_new = tk.Button(toolbar, text="📄 New", command=self.new_file, relief=tk.FLAT)
        btn_new.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Open button
        btn_open = tk.Button(toolbar, text="📂 Open", command=self.open_file, relief=tk.FLAT)
        btn_open.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Save button
        btn_save = tk.Button(toolbar, text="💾 Save", command=self.save_file, relief=tk.FLAT)
        btn_save.pack(side=tk.LEFT, padx=2, pady=2)
        
        tk.Frame(toolbar, width=2, bd=1, relief=tk.SUNKEN).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Cut, Copy, Paste
        btn_cut = tk.Button(toolbar, text="✂️ Cut", command=self.cut, relief=tk.FLAT)
        btn_cut.pack(side=tk.LEFT, padx=2, pady=2)
        
        btn_copy = tk.Button(toolbar, text="📋 Copy", command=self.copy, relief=tk.FLAT)
        btn_copy.pack(side=tk.LEFT, padx=2, pady=2)
        
        btn_paste = tk.Button(toolbar, text="📌 Paste", command=self.paste, relief=tk.FLAT)
        btn_paste.pack(side=tk.LEFT, padx=2, pady=2)
        
        tk.Frame(toolbar, width=2, bd=1, relief=tk.SUNKEN).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Undo, Redo
        btn_undo = tk.Button(toolbar, text="↶ Undo", command=self.undo, relief=tk.FLAT)
        btn_undo.pack(side=tk.LEFT, padx=2, pady=2)
        
        btn_redo = tk.Button(toolbar, text="↷ Redo", command=self.redo, relief=tk.FLAT)
        btn_redo.pack(side=tk.LEFT, padx=2, pady=2)
        
        tk.Frame(toolbar, width=2, bd=1, relief=tk.SUNKEN).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Find
        btn_find = tk.Button(toolbar, text="🔍 Find", command=self.show_find_dialog, relief=tk.FLAT)
        btn_find.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Theme toggle
        btn_theme = tk.Button(toolbar, text="🌓 Theme", command=self.toggle_theme, relief=tk.FLAT)
        btn_theme.pack(side=tk.LEFT, padx=2, pady=2)
    
    def setup_editor(self):
        """Create main text editor area with line numbers"""
        # Container frame
        editor_frame = tk.Frame(self.root)
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # Line numbers
        self.line_numbers = tk.Text(editor_frame, width=5, padx=5, takefocus=0, border=0,
                                     background='lightgray', state='disabled', wrap='none')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Main text widget
        self.text_edit = ScrolledText(editor_frame, wrap=tk.WORD, undo=True, maxundo=-1,
                                       font=(self.current_font_family, self.current_font_size))
        self.text_edit.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind events
        self.text_edit.bind('<<Modified>>', self.on_text_change)
        self.text_edit.bind('<KeyRelease>', self.update_line_numbers)
        self.text_edit.bind('<MouseWheel>', self.update_line_numbers)
        self.text_edit.bind('<Button-1>', self.update_status_bar)
        self.text_edit.bind('<KeyRelease>', self.update_status_bar, add='+')
        
        # Initial line numbers
        self.update_line_numbers()
    
    def setup_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = tk.Frame(self.root, bd=1, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Position label
        self.position_label = tk.Label(self.status_bar, text="Line: 1 | Col: 1", anchor=tk.W)
        self.position_label.pack(side=tk.LEFT, padx=5)
        
        # File info label
        self.file_label = tk.Label(self.status_bar, text="Untitled", anchor=tk.W)
        self.file_label.pack(side=tk.LEFT, padx=20)
        
        # Modified indicator
        self.modified_label = tk.Label(self.status_bar, text="", anchor=tk.W)
        self.modified_label.pack(side=tk.LEFT, padx=5)
        
        # Word count
        self.word_count_label = tk.Label(self.status_bar, text="Words: 0", anchor=tk.E)
        self.word_count_label.pack(side=tk.RIGHT, padx=5)
        
        # Encoding
        self.encoding_label = tk.Label(self.status_bar, text="UTF-8", anchor=tk.E)
        self.encoding_label.pack(side=tk.RIGHT, padx=5)
    
    def setup_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_as_file())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        self.root.bind('<Control-p>', lambda e: self.print_file())
        
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        
        self.root.bind('<Control-f>', lambda e: self.show_find_dialog())
        self.root.bind('<Control-h>', lambda e: self.show_replace_dialog())
        self.root.bind('<Control-g>', lambda e: self.go_to_line())
        
        self.root.bind('<Control-plus>', lambda e: self.zoom_in())
        self.root.bind('<Control-minus>', lambda e: self.zoom_out())
        self.root.bind('<Control-0>', lambda e: self.reset_zoom())
        self.root.bind('<Control-d>', lambda e: self.toggle_theme())
        
        self.root.bind('<F5>', lambda e: self.insert_datetime())
    
    # ==================== FILE OPERATIONS ====================
    
    def new_file(self):
        """Create a new file"""
        if self.check_unsaved_changes():
            self.text_edit.delete(1.0, tk.END)
            self.current_file = None
            self.is_modified = False
            self.update_title()
            self.update_status_bar()
    
    def open_file(self):
        """Open an existing file"""
        if not self.check_unsaved_changes():
            return
        
        filepath = filedialog.askopenfilename(
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("JavaScript Files", "*.js"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("All Files", "*.*")
            ]
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            self.text_edit.delete(1.0, tk.END)
            self.text_edit.insert(1.0, content)
            self.current_file = filepath
            self.is_modified = False
            self.add_to_recent(filepath)
            self.update_title()
            self.update_status_bar()
            self.update_line_numbers()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")
    
    def save_file(self):
        """Save current file"""
        if self.current_file:
            try:
                content = self.text_edit.get(1.0, tk.END)
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.is_modified = False
                self.update_title()
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{e}")
                return False
        else:
            return self.save_as_file()
    
    def save_as_file(self):
        """Save file with new name"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("JavaScript Files", "*.js"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("All Files", "*.*")
            ]
        )
        
        if not filepath:
            return False
        
        try:
            content = self.text_edit.get(1.0, tk.END)
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            self.current_file = filepath
            self.is_modified = False
            self.add_to_recent(filepath)
            self.update_title()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")
            return False
    
    def print_file(self):
        """Print current document"""
        messagebox.showinfo("Print", "Print functionality would open system print dialog.\n"
                                     "This requires platform-specific implementation.")
    
    # ==================== EDIT OPERATIONS ====================
    
    def undo(self):
        """Undo last action"""
        try:
            self.text_edit.edit_undo()
        except tk.TclError:
            pass
    
    def redo(self):
        """Redo last undone action"""
        try:
            self.text_edit.edit_redo()
        except tk.TclError:
            pass
    
    def cut(self):
        """Cut selected text"""
        try:
            self.text_edit.event_generate("<<Cut>>")
        except:
            pass
    
    def copy(self):
        """Copy selected text"""
        try:
            self.text_edit.event_generate("<<Copy>>")
        except:
            pass
    
    def paste(self):
        """Paste from clipboard"""
        try:
            self.text_edit.event_generate("<<Paste>>")
        except:
            pass
    
    def select_all(self):
        """Select all text"""
        self.text_edit.tag_add(tk.SEL, "1.0", tk.END)
        self.text_edit.mark_set(tk.INSERT, "1.0")
        self.text_edit.see(tk.INSERT)
        return 'break'
    
    # ==================== FIND/REPLACE ====================
    
    def show_find_dialog(self):
        """Show find dialog"""
        self.find_window = tk.Toplevel(self.root)
        self.find_window.title("Find")
        self.find_window.geometry("400x100")
        self.find_window.resizable(False, False)
        
        tk.Label(self.find_window, text="Find:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.find_entry = tk.Entry(self.find_window, width=30)
        self.find_entry.grid(row=0, column=1, padx=5, pady=5)
        self.find_entry.insert(0, self.last_search)
        self.find_entry.focus()
        
        btn_frame = tk.Frame(self.find_window)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        tk.Button(btn_frame, text="Find Next", command=self.find_next).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Find Previous", command=self.find_previous).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Close", command=self.find_window.destroy).pack(side=tk.LEFT, padx=5)
        
        self.find_entry.bind('<Return>', lambda e: self.find_next())
        self.find_entry.bind('<Escape>', lambda e: self.find_window.destroy())
    
    def show_replace_dialog(self):
        """Show find and replace dialog"""
        replace_window = tk.Toplevel(self.root)
        replace_window.title("Find and Replace")
        replace_window.geometry("400x150")
        replace_window.resizable(False, False)
        
        tk.Label(replace_window, text="Find:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        find_entry = tk.Entry(replace_window, width=30)
        find_entry.grid(row=0, column=1, padx=5, pady=5)
        find_entry.insert(0, self.last_search)
        
        tk.Label(replace_window, text="Replace:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        replace_entry = tk.Entry(replace_window, width=30)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def replace_one():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            if find_text:
                try:
                    start = self.text_edit.search(find_text, tk.INSERT, tk.END)
                    if start:
                        end = f"{start}+{len(find_text)}c"
                        self.text_edit.delete(start, end)
                        self.text_edit.insert(start, replace_text)
                        self.text_edit.tag_remove(tk.SEL, "1.0", tk.END)
                        self.text_edit.tag_add(tk.SEL, start, f"{start}+{len(replace_text)}c")
                except:
                    pass
        
        def replace_all():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            if find_text:
                content = self.text_edit.get(1.0, tk.END)
                new_content = content.replace(find_text, replace_text)
                self.text_edit.delete(1.0, tk.END)
                self.text_edit.insert(1.0, new_content)
        
        btn_frame = tk.Frame(replace_window)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Replace", command=replace_one).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Replace All", command=replace_all).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Close", command=replace_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def find_next(self):
        """Find next occurrence"""
        search_term = self.find_entry.get()
        if not search_term:
            return
        
        self.last_search = search_term
        self.text_edit.tag_remove(tk.SEL, "1.0", tk.END)
        
        start = self.text_edit.search(search_term, self.search_index, tk.END)
        if start:
            end = f"{start}+{len(search_term)}c"
            self.text_edit.tag_add(tk.SEL, start, end)
            self.text_edit.mark_set(tk.INSERT, end)
            self.text_edit.see(start)
            self.search_index = end
        else:
            self.search_index = "1.0"
            messagebox.showinfo("Find", "No more occurrences found.")
    
    def find_previous(self):
        """Find previous occurrence"""
        search_term = self.find_entry.get()
        if not search_term:
            return
        
        self.last_search = search_term
        self.text_edit.tag_remove(tk.SEL, "1.0", tk.END)
        
        start = self.text_edit.search(search_term, tk.INSERT, "1.0", backwards=True)
        if start:
            end = f"{start}+{len(search_term)}c"
            self.text_edit.tag_add(tk.SEL, start, end)
            self.text_edit.mark_set(tk.INSERT, start)
            self.text_edit.see(start)
        else:
            messagebox.showinfo("Find", "No more occurrences found.")
    
    def go_to_line(self):
        """Go to specific line number"""
        line = tk.simpledialog.askinteger("Go to Line", "Enter line number:", 
                                          parent=self.root, minvalue=1)
        if line:
            self.text_edit.mark_set(tk.INSERT, f"{line}.0")
            self.text_edit.see(tk.INSERT)
            self.update_status_bar()
    
    # ==================== VIEW OPERATIONS ====================
    
    def zoom_in(self):
        """Increase font size"""
        self.current_font_size += 2
        self.update_font()
    
    def zoom_out(self):
        """Decrease font size"""
        if self.current_font_size > 6:
            self.current_font_size -= 2
            self.update_font()
    
    def reset_zoom(self):
        """Reset font size to default"""
        self.current_font_size = 12
        self.update_font()
    
    def update_font(self):
        """Update text widget font"""
        self.text_edit.config(font=(self.current_font_family, self.current_font_size))
    
    def toggle_line_numbers(self):
        """Toggle line numbers visibility"""
        self.show_line_numbers = not self.show_line_numbers
        if self.show_line_numbers:
            self.line_numbers.pack(side=tk.LEFT, fill=tk.Y, before=self.text_edit)
        else:
            self.line_numbers.pack_forget()
    
    def toggle_word_wrap(self):
        """Toggle word wrap"""
        current_wrap = self.text_edit.cget('wrap')
        new_wrap = tk.NONE if current_wrap == tk.WORD else tk.WORD
        self.text_edit.config(wrap=new_wrap)
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            # Dark theme
            bg_color = "#1e1e1e"
            fg_color = "#d4d4d4"
            select_bg = "#264f78"
            line_bg = "#252526"
        else:
            # Light theme
            bg_color = "white"
            fg_color = "black"
            select_bg = "#b3d7ff"
            line_bg = "lightgray"
        
        self.text_edit.config(bg=bg_color, fg=fg_color, selectbackground=select_bg,
                              insertbackground=fg_color)
        self.line_numbers.config(bg=line_bg, fg=fg_color)
    
    # ==================== FORMAT OPERATIONS ====================
    
    def choose_font(self):
        """Open font chooser dialog"""
        font_window = tk.Toplevel(self.root)
        font_window.title("Choose Font")
        font_window.geometry("300x200")
        
        tk.Label(font_window, text="Font Family:").pack(pady=5)
        
        font_families = list(font.families())
        font_var = tk.StringVar(value=self.current_font_family)
        
        font_listbox = tk.Listbox(font_window, height=8)
        for family in sorted(font_families)[:50]:  # Show first 50 fonts
            font_listbox.insert(tk.END, family)
        font_listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        def apply_font():
            selection = font_listbox.curselection()
            if selection:
                self.current_font_family = font_listbox.get(selection[0])
                self.update_font()
                font_window.destroy()
        
        tk.Button(font_window, text="Apply", command=apply_font).pack(pady=5)
    
    def choose_text_color(self):
        """Choose text color"""
        color = colorchooser.askcolor(title="Choose Text Color")
        if color[1]:
            self.text_edit.config(fg=color[1])
    
    def choose_bg_color(self):
        """Choose background color"""
        color = colorchooser.askcolor(title="Choose Background Color")
        if color[1]:
            self.text_edit.config(bg=color[1])
    
    def to_uppercase(self):
        """Convert selected text to uppercase"""
        try:
            selected = self.text_edit.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_edit.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_edit.insert(tk.INSERT, selected.upper())
        except:
            pass
    
    def to_lowercase(self):
        """Convert selected text to lowercase"""
        try:
            selected = self.text_edit.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_edit.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_edit.insert(tk.INSERT, selected.lower())
        except:
            pass
    
    def to_titlecase(self):
        """Convert selected text to title case"""
        try:
            selected = self.text_edit.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_edit.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_edit.insert(tk.INSERT, selected.title())
        except:
            pass
    
    # ==================== TOOLS ====================
    
    def show_word_count(self):
        """Show word count"""
        content = self.text_edit.get(1.0, tk.END)
        words = len(content.split())
        messagebox.showinfo("Word Count", f"Total words: {words}")
    
    def show_char_count(self):
        """Show character count"""
        content = self.text_edit.get(1.0, tk.END)
        chars = len(content) - 1  # Subtract trailing newline
        chars_no_space = len(content.replace(" ", "").replace("\n", ""))
        messagebox.showinfo("Character Count", 
                           f"Total characters: {chars}\n"
                           f"Characters (no spaces): {chars_no_space}")
    
    def toggle_auto_save(self):
        """Toggle auto-save feature"""
        self.auto_save_enabled = not self.auto_save_enabled
        if self.auto_save_enabled:
            self.schedule_auto_save()
        else:
            if self.auto_save_job:
                self.root.after_cancel(self.auto_save_job)
    
    def schedule_auto_save(self):
        """Schedule auto-save"""
        if self.auto_save_enabled and self.current_file and self.is_modified:
            self.save_file()
        if self.auto_save_enabled:
            self.auto_save_job = self.root.after(self.auto_save_interval, self.schedule_auto_save)
    
    def insert_datetime(self):
        """Insert current date and time"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text_edit.insert(tk.INSERT, now)
    
    # ==================== RECENT FILES ====================
    
    def load_recent_files(self):
        """Load recent files from config"""
        config_file = os.path.expanduser("~/.text_editor_recent.json")
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_recent_files(self):
        """Save recent files to config"""
        config_file = os.path.expanduser("~/.text_editor_recent.json")
        try:
            with open(config_file, 'w') as f:
                json.dump(self.recent_files[:10], f)  # Keep only 10 recent files
        except:
            pass
    
    def add_to_recent(self, filepath):
        """Add file to recent files list"""
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        self.recent_files.insert(0, filepath)
        self.save_recent_files()
        self.update_recent_menu()
    
    def update_recent_menu(self):
        """Update recent files menu"""
        self.recent_menu.delete(0, tk.END)
        if not self.recent_files:
            self.recent_menu.add_command(label="(No recent files)", state=tk.DISABLED)
        else:
            for filepath in self.recent_files[:10]:
                self.recent_menu.add_command(
                    label=os.path.basename(filepath),
                    command=lambda f=filepath: self.open_recent_file(f)
                )
    
    def open_recent_file(self, filepath):
        """Open a recent file"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.text_edit.delete(1.0, tk.END)
                self.text_edit.insert(1.0, content)
                self.current_file = filepath
                self.is_modified = False
                self.update_title()
                self.update_status_bar()
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{e}")
        else:
            messagebox.showerror("Error", "File no longer exists!")
            self.recent_files.remove(filepath)
            self.save_recent_files()
            self.update_recent_menu()
    
    # ==================== HELP ====================
    
    def show_shortcuts(self):
        """Show keyboard shortcuts"""
        shortcuts = """
Keyboard Shortcuts:

File Operations:
  Ctrl+N - New File
  Ctrl+O - Open File
  Ctrl+S - Save File
  Ctrl+Shift+S - Save As
  Ctrl+P - Print
  Ctrl+Q - Exit

Edit Operations:
  Ctrl+Z - Undo
  Ctrl+Y - Redo
  Ctrl+X - Cut
  Ctrl+C - Copy
  Ctrl+V - Paste
  Ctrl+A - Select All

Find/Replace:
  Ctrl+F - Find
  Ctrl+H - Replace
  Ctrl+G - Go to Line

View:
  Ctrl++ - Zoom In
  Ctrl+- - Zoom Out
  Ctrl+0 - Reset Zoom
  Ctrl+D - Toggle Dark Mode

Tools:
  F5 - Insert Date/Time
        """
        messagebox.showinfo("Keyboard Shortcuts", shortcuts)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
Advanced Text Editor
Version 1.0

A feature-rich text editor built with Python and Tkinter.

Features:
• Multiple file format support
• Find and Replace
• Syntax highlighting ready
• Auto-save
• Recent files
• Dark/Light themes
• And much more!

Created with ❤️ using Python
        """
        messagebox.showinfo("About", about_text)
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def on_text_change(self, event=None):
        """Handle text change event"""
        if self.text_edit.edit_modified():
            self.is_modified = True
            self.update_title()
            self.text_edit.edit_modified(False)
            self.update_status_bar()
    
    def update_line_numbers(self, event=None):
        """Update line numbers"""
        if not self.show_line_numbers:
            return
        
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        
        line_count = self.text_edit.get(1.0, tk.END).count('\n')
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert(1.0, line_numbers_string)
        self.line_numbers.config(state='disabled')
    
    def update_status_bar(self, event=None):
        """Update status bar information"""
        # Cursor position
        cursor_pos = self.text_edit.index(tk.INSERT)
        line, col = cursor_pos.split('.')
        self.position_label.config(text=f"Line: {line} | Col: {int(col) + 1}")
        
        # File name
        if self.current_file:
            filename = os.path.basename(self.current_file)
            self.file_label.config(text=filename)
        else:
            self.file_label.config(text="Untitled")
        
        # Modified indicator
        if self.is_modified:
            self.modified_label.config(text="●", fg="red")
        else:
            self.modified_label.config(text="")
        
        # Word count
        content = self.text_edit.get(1.0, tk.END)
        words = len(content.split())
        self.word_count_label.config(text=f"Words: {words}")
    
    def update_title(self):
        """Update window title"""
        title = "Advanced Text Editor"
        if self.current_file:
            title += f" - {os.path.basename(self.current_file)}"
        else:
            title += " - Untitled"
        if self.is_modified:
            title += " *"
        self.root.title(title)
    
    def check_unsaved_changes(self):
        """Check for unsaved changes before closing/opening"""
        if self.is_modified:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save them?"
            )
            if response:  # Yes
                return self.save_file()
            elif response is None:  # Cancel
                return False
            # No - continue without saving
        return True
    
    def on_closing(self):
        """Handle window closing"""
        if self.check_unsaved_changes():
            self.root.destroy()


def main():
    root = tk.Tk()
    app = AdvancedTextEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
