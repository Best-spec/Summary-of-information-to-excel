import tkinter as tk
from tkinter import ttk

class AnalysisButton:
    """
    Represents a button that triggers analysis of CSV files in the selected folder.
    """
    
    def __init__(self, parent, text="Analyze CSV"):
        self._parent = parent
        # self._command = command
        self._text = text

    def render(self):
        """
        Renders the analysis button in the specified grid position.
        """
        button_frame = ttk.Frame(self._parent)
        button_frame.grid(row=1, column=0, columnspan=3, sticky="w")  # ติดแนบซ้าย

        ttk.Button(button_frame, text="Inquiry").grid(row=1, column=0, padx=2)
        ttk.Button(button_frame, text="Appointment").grid(row=1, column=1, padx=2)
        ttk.Button(button_frame, text="Feedback").grid(row=1, column=2, padx=2)

    def show(self):
        """
        Displays the button in the UI.
        """
        print("Button rendered with text:", self._text)

        