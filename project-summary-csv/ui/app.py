import tkinter as tk
from tkinter import ttk
from ui.components.select_folder import FolderSelector
from ui.components.analysis_button import AnalysisButton

class MainApp:
    """
    Manages the main application UI and coordinates user interactions.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Inquiry Summary UI")
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # SRP - ใช้ FolderSelector แยกความรับผิดชอบเรื่อง path ไปต่างหาก
        self.folder_selector = FolderSelector(self.main_frame)
        self.folder_selector.render()

        # SRP - ใช้ AnalysisButton แยกความรับผิดชอบเรื่องการวิเคราะห์ CSV ไปต่างหาก
        self.butttons_analysis = AnalysisButton(
            self.main_frame
        )
        self.butttons_analysis.render()


        # # Row 1: Button row in sub-frame
        # button_frame = ttk.Frame(frame)
        # button_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="w")

        # ttk.Button(button_frame, text="Inquiry", command=self.find_inquiry).pack(side="left",padx=10)
        # ttk.Button(button_frame, text="Appointment", command=self.show_find_appointment).pack(side="left",padx=10)
        # ttk.Button(button_frame, text="Feedback-package", command=self.find_FeedAndPack).pack(side="left",padx=10)
        # ttk.Button(button_frame, text="PlotAll", command=self.plot_graph_Type_of_Email_by_month).pack(side="left",padx=10)
        # ttk.Button(button_frame, text="TopCenter", command=self.top_20).pack(side="left",padx=10)

        # self.result_text = tk.Text(frame, height=20, wrap=tk.WORD)
        # self.result_text.grid(row=3, column=0, columnspan=3, pady=10)