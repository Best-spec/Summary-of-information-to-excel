from tkinter import filedialog
import tkinter as tk
from tkinter import ttk

class FolderSelector:
    """
    Responsible for rendering folder selection UI and managing folder path state.
    """

    def __init__(self, parent, label_text="CSV Folder:"):
        self._parent = parent
        self._label_text = label_text
        self._folder_path = tk.StringVar()

    def render(self):
        """
        Renders the folder selection widgets (Label, Entry, Browse Button)
        """
        folder_frame = ttk.Frame(self._parent)
        folder_frame.grid(row=0, column=0, columnspan=3, sticky="w")  # ติดแนบซ้าย

        ttk.Label(folder_frame, text=self._label_text).grid(row=0, column=0, padx=2)
        ttk.Entry(folder_frame, textvariable=self._folder_path, width=50).grid(row=0, column=1, padx=2)
        ttk.Button(folder_frame, text="Browse", command=self._browse_folder).grid(row=0, column=2, padx=2)

    def _browse_folder(self):
        """
        Opens a folder dialog and sets the selected path
        """
        selected_path = filedialog.askdirectory()
        if selected_path:
            self._folder_path.set(selected_path)

    def get_path(self) -> str:
        """
        Returns the currently selected folder path
        """
        return self._folder_path.get()

    def set_path(self, path: str):
        """
        Allows setting the path manually
        """
        self._folder_path.set(path)
