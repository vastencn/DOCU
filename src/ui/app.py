import os
import customtkinter as ctk
from tkinter import filedialog
from typing import Dict, List, Any
from src.utils.file_scanner import scan_directory, read_file_preview

class FileBrowserApp(ctk.CTk):
    def __init__(self, initial_dir: str = r"E:\DOCU"):
        super().__init__()

        # Window configuration
        self.title("DOCU - Modern Documentation File Browser")
        self.geometry("1100;700".replace(";", "x"))
        self.minsize(850, 500)

        # Set default appearance
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.current_dir = initial_dir if os.path.exists(initial_dir) else os.getcwd()
        self.scanned_files: List[Dict[str, Any]] = []
        self.checkbox_vars: Dict[str, ctk.BooleanVar] = {}
        self.selected_file_path: str = ""

        # Build UI
        self._create_header_panel()
        self._create_main_content()
        self._create_status_bar()

        # Initial Scan
        self.scan_files()

    def _create_header_panel(self):
        """Top controls for directory selection, search, and filters."""
        header_frame = ctk.CTkFrame(self, corner_radius=8)
        header_frame.pack(fill="x", padx=12, pady=(12, 6))

        # Top row: Path & Browse
        row1 = ctk.CTkFrame(header_frame, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=(8, 4))

        lbl_dir = ctk.CTkLabel(row1, text="Target Folder:", font=ctk.CTkFont(size=13, weight="bold"))
        lbl_dir.pack(side="left", padx=(0, 8))

        self.entry_path = ctk.CTkEntry(row1, placeholder_text="Enter or browse folder path...", height=34)
        self.entry_path.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entry_path.insert(0, self.current_dir)
        self.entry_path.bind("<Return>", lambda event: self.scan_files())

        btn_browse = ctk.CTkButton(
            row1, 
            text="📁 Browse...", 
            width=110, 
            height=34, 
            command=self.browse_directory,
            fg_color="#1f6aa5",
            hover_color="#144870"
        )
        btn_browse.pack(side="left", padx=(0, 6))

        btn_refresh = ctk.CTkButton(
            row1, 
            text="🔄 Refresh", 
            width=90, 
            height=34, 
            command=self.scan_files
        )
        btn_refresh.pack(side="left")

        # Second row: Filters & Options
        row2 = ctk.CTkFrame(header_frame, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=(4, 8))

        lbl_filter = ctk.CTkLabel(row2, text="Filter:")
        lbl_filter.pack(side="left", padx=(0, 6))

        self.combo_ext = ctk.CTkComboBox(
            row2,
            values=[
                "All Files (*.*)",
                "Markdown (*.md)",
                "Python (*.py)",
                "JSON (*.json)",
                "Text (*.txt)",
                "JavaScript (*.js)"
            ],
            width=160,
            command=lambda choice: self.scan_files()
        )
        self.combo_ext.set("All Files (*.*)")
        self.combo_ext.pack(side="left", padx=(0, 12))

        lbl_search = ctk.CTkLabel(row2, text="Search:")
        lbl_search.pack(side="left", padx=(0, 6))

        self.entry_search = ctk.CTkEntry(row2, placeholder_text="Filter by filename...", width=200)
        self.entry_search.pack(side="left", padx=(0, 12))
        self.entry_search.bind("<KeyRelease>", lambda event: self.scan_files())

        self.var_subfolders = ctk.BooleanVar(value=True)
        self.chk_subfolders = ctk.CTkCheckBox(
            row2, 
            text="Include Subfolders", 
            variable=self.var_subfolders,
            command=self.scan_files
        )
        self.chk_subfolders.pack(side="left", padx=(0, 12))

        # Theme toggle on right
        self.btn_theme = ctk.CTkButton(
            row2, 
            text="Toggle Theme", 
            width=100, 
            command=self.toggle_theme,
            fg_color="gray30",
            hover_color="gray40"
        )
        self.btn_theme.pack(side="right")

    def _create_main_content(self):
        """Split view: Left = CTkScrollableFrame with checkboxes, Right = File Preview."""
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=12, pady=6)

        # Left Column: File Checklist
        left_box = ctk.CTkFrame(content_frame, width=460, corner_radius=8)
        left_box.pack(side="left", fill="both", expand=False, padx=(0, 6))
        left_box.pack_propagate(False)

        # Left Top Action Bar
        action_bar = ctk.CTkFrame(left_box, fg_color="transparent")
        action_bar.pack(fill="x", padx=8, pady=(8, 4))

        lbl_list_title = ctk.CTkLabel(action_bar, text="Scanned Files", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_list_title.pack(side="left")

        btn_invert = ctk.CTkButton(action_bar, text="Invert", width=60, height=26, font=ctk.CTkFont(size=11), command=self.invert_selection)
        btn_invert.pack(side="right", padx=(4, 0))

        btn_none = ctk.CTkButton(action_bar, text="None", width=55, height=26, font=ctk.CTkFont(size=11), command=self.deselect_all)
        btn_none.pack(side="right", padx=(4, 0))

        btn_all = ctk.CTkButton(action_bar, text="All", width=50, height=26, font=ctk.CTkFont(size=11), command=self.select_all)
        btn_all.pack(side="right")

        # Scrollable Frame for Checkboxes
        self.file_scroll_frame = ctk.CTkScrollableFrame(left_box, label_text="Folder Checklist", corner_radius=6)
        self.file_scroll_frame.pack(fill="both", expand=True, padx=8, pady=(4, 8))

        # Right Column: File Preview Panel
        right_box = ctk.CTkFrame(content_frame, corner_radius=8)
        right_box.pack(side="right", fill="both", expand=True, padx=(6, 0))

        preview_header = ctk.CTkFrame(right_box, fg_color="transparent")
        preview_header.pack(fill="x", padx=10, pady=(8, 4))

        self.lbl_preview_title = ctk.CTkLabel(
            preview_header, 
            text="File Preview & Inspector", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.lbl_preview_title.pack(side="left")

        self.lbl_file_meta = ctk.CTkLabel(
            preview_header, 
            text="Select a file to preview", 
            text_color="gray60",
            font=ctk.CTkFont(size=12)
        )
        self.lbl_file_meta.pack(side="right")

        # Textbox for preview
        self.txt_preview = ctk.CTkTextbox(right_box, font=ctk.CTkFont(family="Consolas", size=12), wrap="none")
        self.txt_preview.pack(fill="both", expand=True, padx=10, pady=(4, 10))
        self.txt_preview.insert("1.0", "Select any file on the left to preview its content.")
        self.txt_preview.configure(state="disabled")

    def _create_status_bar(self):
        """Bottom status bar."""
        self.status_frame = ctk.CTkFrame(self, height=30, corner_radius=4)
        self.status_frame.pack(fill="x", padx=12, pady=(0, 8))

        self.lbl_status = ctk.CTkLabel(
            self.status_frame, 
            text="Initializing...", 
            font=ctk.CTkFont(size=11)
        )
        self.lbl_status.pack(side="left", padx=10)

        self.lbl_counts = ctk.CTkLabel(
            self.status_frame, 
            text="0 files selected", 
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.lbl_counts.pack(side="right", padx=10)

    def browse_directory(self):
        """Opens native directory dialog."""
        folder = filedialog.askdirectory(initialdir=self.current_dir, title="Select Directory")
        if folder:
            self.current_dir = os.path.normpath(folder)
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, self.current_dir)
            self.scan_files()

    def scan_files(self):
        """Scans the configured directory and updates checklist widgets."""
        path_input = self.entry_path.get().strip()
        if not path_input:
            path_input = self.current_dir

        if not os.path.isdir(path_input):
            self.lbl_status.configure(text=f"Directory does not exist: {path_input}")
            return

        self.current_dir = os.path.normpath(path_input)
        ext_filter = self.combo_ext.get()
        search_query = self.entry_search.get()
        inc_sub = self.var_subfolders.get()

        self.scanned_files = scan_directory(
            target_dir=self.current_dir,
            include_subfolders=inc_sub,
            search_query=search_query,
            extension_filter=ext_filter
        )

        # Clear existing checkboxes
        for widget in self.file_scroll_frame.winfo_children():
            widget.destroy()
        self.checkbox_vars.clear()

        if not self.scanned_files:
            lbl_empty = ctk.CTkLabel(self.file_scroll_frame, text="No matching files found.", text_color="gray50")
            lbl_empty.pack(pady=20)
            self.update_status(0, 0)
            return

        # Pack CTkCheckBox for each file
        for item in self.scanned_files:
            file_path = item["full_path"]
            var = ctk.BooleanVar(value=False)
            self.checkbox_vars[file_path] = var

            item_frame = ctk.CTkFrame(self.file_scroll_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=2, padx=4)

            chk = ctk.CTkCheckBox(
                item_frame,
                text=item["rel_path"],
                variable=var,
                command=self._on_checkbox_toggle,
                font=ctk.CTkFont(size=12)
            )
            chk.pack(side="left", fill="x", expand=True)

            btn_view = ctk.CTkButton(
                item_frame,
                text=item["size_str"],
                width=65,
                height=22,
                font=ctk.CTkFont(size=10),
                fg_color="gray25",
                hover_color="gray35",
                command=lambda p=file_path, it=item: self.preview_file(p, it)
            )
            btn_view.pack(side="right", padx=(4, 0))

        self.update_status(0, len(self.scanned_files))
        self.lbl_status.configure(text=f"Scanned {len(self.scanned_files)} files in {self.current_dir}")

    def _on_checkbox_toggle(self):
        """Update selected count when checkboxes change."""
        selected = sum(1 for v in self.checkbox_vars.values() if v.get())
        self.update_status(selected, len(self.scanned_files))

    def preview_file(self, file_path: str, file_info: Dict[str, Any]):
        """Renders file content into the preview text area."""
        self.selected_file_path = file_path
        self.lbl_preview_title.configure(text=f"Preview: {file_info['name']}")
        self.lbl_file_meta.configure(text=f"Size: {file_info['size_str']} | Type: {file_info['ext'] or 'None'}")

        content = read_file_preview(file_path, max_lines=250)

        self.txt_preview.configure(state="normal")
        self.txt_preview.delete("1.0", "end")
        self.txt_preview.insert("1.0", content)
        self.txt_preview.configure(state="disabled")

    def select_all(self):
        for var in self.checkbox_vars.values():
            var.set(True)
        self._on_checkbox_toggle()

    def deselect_all(self):
        for var in self.checkbox_vars.values():
            var.set(False)
        self._on_checkbox_toggle()

    def invert_selection(self):
        for var in self.checkbox_vars.values():
            var.set(not var.get())
        self._on_checkbox_toggle()

    def update_status(self, selected_count: int, total_count: int):
        self.lbl_counts.configure(text=f"{selected_count} / {total_count} files selected")

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        new_mode = "Light" if current == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
