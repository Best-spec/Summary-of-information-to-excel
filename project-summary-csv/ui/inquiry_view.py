import tkinter as tk
from services.data_service import DataService
from utils.localization import translate

class InquiryView:
    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.label = tk.Label(self.frame, text=translate("inquiry_title"))
        self.label.pack()

        # Data loading demo
        data = DataService.load_inquiries()
        print(data)