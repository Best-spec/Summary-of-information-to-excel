import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import glob
import os
import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import tempfile
import numpy as np
from total_all import TotalMonth
from overall import Overall
from config_graph import ColorConfig



# หมวดหมู่ภาษา (ตัวอย่าง)
# รายการประเภท inquiry แต่ละภาษา
categories = {
    'English' : [
        "General Inquiry",
        "Estimated Cost",
        "Contact My Doctor at Bangkok Hospital Pattaya",
        "Other"
    ],

    'Thai' : [
        "สอบถามทั่วไป",
        "ค่าใช้จ่าย",
        "ติดต่อกับหมอประจำตัวที่โรงพยาบาลกรุงเทพพัทยา",
        "อื่นๆ"
    ],

    'Russia' : [
        "Общий запрос",
        "Узнать про цену",
        "Написать врачу",
        "Другое"
    ],
    'Arabic' : [
        "General Inquiry",
        "Estimated Cost",
        "Contact My Doctor at Bangkok Hospital Pattaya",
        "Other"
    ],

    'Chinese' : [
        "普通咨询",
        "预估价格咨询",
        "联系芭提雅曼谷医院医生",
        "其他"
    ],

    'German' : [
        "Allgemeine Anfrage",
        "Vorraussichtliche Kosten",
        "Arzt im Bangkok Hospital Pattaya kontaktieren",
        "Andere"
    ]
}

class InquiryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inquiry Summary UI")
        self.folder_path = tk.StringVar()

        self.setup_ui()
        self.state = True

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Row 0: Folder selection
        ttk.Label(frame, text="CSV Folder:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.folder_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Browse", command=self.browse_folder).grid(row=0, column=2)

        # Row 1: Button row
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="w")

        ttk.Button(button_frame, text="Inquiry", command=self.find_inquiry).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Appointment", command=self.show_find_appointment).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Feedback-package", command=self.find_FeedAndPack).pack(side="left", padx=10)
        ttk.Button(button_frame, text="PlotAll", command=self.plot_graph_Type_of_Email_by_month).pack(side="left", padx=10)
        ttk.Button(button_frame, text="TopCenter", command=self.top_20).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Total_month", command=self.total_month).pack(side="left", padx=10)

        # Row 2: Text widget with scrollbars
        text_frame = ttk.Frame(frame)
        text_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")

        self.result_text = tk.Text(text_frame, wrap="none", font=("Courier New", 10))
        self.result_text.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        scroll_y = ttk.Scrollbar(text_frame, orient="vertical", command=self.result_text.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")

        scroll_x = ttk.Scrollbar(text_frame, orient="horizontal", command=self.result_text.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")

        self.result_text.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # ให้ text widget ขยายได้
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path.set(path)
    
    def find_inquiry(self):
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder")
            return

        summary = defaultdict(lambda: defaultdict(int))
        csv_files = glob.glob(os.path.join(folder, "*.csv"))

        for file in csv_files:
            try:
                df = pd.read_csv(file)
                df.columns = df.columns.str.replace('\ufeff', '').str.strip('"')
                col_name = df.columns[0]
            except Exception as e:
                print(f"Failed to process {file}: {e}")
                continue

            if "-en" in file:
                lang = "English"
            elif "-th" in file:
                lang = "Thai"
            elif "-ru" in file:
                lang = "Russia"
            elif "-de" in file:
                lang = "German"
            elif "-ar" in file:
                lang = "Arabic"
            elif "-zh" in file:
                lang = "Chinese"
            else:
                continue

            for cat in categories.get(lang, []):
                count = df[col_name].astype(str).str.strip().eq(cat).sum()
                summary[lang][cat] += count
        
        summary_dict = {
            lang: {cat: int(count) for cat, count in summary[lang].items()}
            for lang in summary
        }

        # แปลง summary_dict เป็นข้อความอ่านง่าย
        # def format_summary_dict(summary_dict):
        #     lines = []
        #     for lang, cats in summary_dict.items():
        #         lines.append(f"Language: {lang}")
        #         for cat, count in cats.items():
        #             lines.append(f"  - {cat}: {count}")
        #         lines.append("")  # เว้นบรรทัดระหว่างภาษา
        #     return "\n".join(lines)

        def show_inquiry(summary_dict):
            # summary_dict = {'Arabic': {'General Inquiry': 0, 'Estimated Cost': 0, 'Contact My Doctor at Bangkok Hospital Pattaya': 0, 'Other': 0}, 'German': {'Allgemeine Anfrage': 3, 'Vorraussichtliche Kosten': 3, 'Arzt im Bangkok Hospital Pattaya kontaktieren': 2, 'Andere': 4}, 'English': {'General Inquiry': 81, 'Estimated Cost': 76, 'Contact My Doctor at Bangkok Hospital Pattaya': 19, 'Other': 39}, 'Russia': {'Общий запрос': 3, 'Узнать про цену': 3, 'Написать врачу': 0, 'Другое': 6}, 'Thai': {'สอบถามทั่วไป': 5, 'ค่าใช้จ่าย': 8, 'ติดต่อกับหมอประจำตัวที่โรงพยาบาลกรุงเทพพัทยา': 2, 'อื่นๆ': 0}, 'Chinese': {'普通咨询': 1, '预估价格咨询': 0, '联系芭提雅曼谷医院医生': 0, '其他': 0}}

            # สร้าง mapping ของคำถามแต่ละประเภทในแต่ละภาษา
            category_mapping = {
                'General Inquiry': ['General Inquiry', 'Allgemeine Anfrage', 'Общий запрос', 'สอบถามทั่วไป', '普通咨询'],
                'Estimated Cost': ['Estimated Cost', 'Vorraussichtliche Kosten', 'Узнать про цену', 'ค่าใช้จ่าย', '预估价格咨询'],
                'Contact Doctor': ['Contact My Doctor at Bangkok Hospital Pattaya', 'Arzt im Bangkok Hospital Pattaya kontaktieren', 'Написать врачу', 'ติดต่อกับหมอประจำตัวที่โรงพยาบาลกรุงเทพพัทยา', '联系芭提雅曼谷医院医生'],
                'Other': ['Other', 'Andere', 'Другое', 'อื่นๆ', '其他']
            }

            # สร้าง reverse mapping เพื่อหาประเภทจากชื่อคำถาม
            reverse_mapping = {}
            for category, questions in category_mapping.items():
                for question in questions:
                    reverse_mapping[question] = category

            # สร้างตารางใหม่โดยจำแนกตามประเภทคำถาม
            category_summary = {}
            all_languages = list(summary_dict.keys())

            # เตรียมข้อมูลสำหรับแต่ละประเภทคำถาม
            for category in category_mapping.keys():
                category_summary[category] = {}
                for lang in all_languages:
                    category_summary[category][lang] = 0

            # รวบรวมข้อมูลจากแต่ละภาษา
            for lang, questions in summary_dict.items():
                for question, count in questions.items():
                    category = reverse_mapping.get(question, 'Other')
                    category_summary[category][lang] += count

            # เตรียม header (สลับแกน: ภาษาเป็นแถว, ประเภทคำถามเป็นคอลัมน์)
            all_categories = list(category_mapping.keys())
            headers = ["Language"] + all_categories + ["Total Language"]
            table = []

            # เติมข้อมูลแต่ละภาษา (แถว)
            for lang in all_languages:
                row = [lang]
                total = 0
                for category in all_categories:
                    count = category_summary[category][lang]
                    row.append(count)
                    total += count
                row.append(total)
                table.append(row)

            # คำนวณผลรวมแต่ละประเภทคำถาม (column total)
            total_row = ["Total inquiry"]
            for col in range(1, len(all_categories) + 2):  # บวกอีก 1 สำหรับ Total column
                col_sum = sum(row[col] for row in table)
                total_row.append(col_sum)
            table.append(total_row)

            # จัดรูปแบบข้อความแบบ fixed-width columns
            col_widths = [max(len(str(row[i])) for row in [headers] + table) for i in range(len(headers))]
            lines = []

            def format_row(row):
                return " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))

            lines.append(format_row(headers))
            lines.append("-+-".join("-" * w for w in col_widths))
            for row in table:
                lines.append(format_row(row))

            result_table = "\n".join(lines)
            # print(result_table)
            return result_table
        
        readable_text = show_inquiry(summary_dict)
        self.result_text.delete(1.0, tk.END)

        if summary_dict:
            self.result_text.insert(tk.END, readable_text)
        else:
            self.result_text.insert(tk.END, "No inquiry data found.")

        root = self.root
        show_graph = TotalMonth(folder)
        show_graph.graph_inquiry(summary ,root)

    def find_appointment(self):
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder")
            return

        summary = defaultdict(lambda: defaultdict(int))

        langs = ["ar", "de", "en", "ru", "th", "zh"]
        lang_summary = {lang: {"appointment count": 0, "appointment recommended count": 0} for lang in langs}
        total_all_col_rec, total_all_col = 0, 0

        recommended_files = glob.glob(os.path.join(folder, "*appointment-recommended*.csv"))
        normal_files = [f for f in glob.glob(os.path.join(folder, "*appointment*.csv"))
                        if "appointment-recommended" not in os.path.basename(f)]

        # อ่านไฟล์ recommended
        for file in recommended_files:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip().str.replace('\ufeff', '')
            col_name = df.columns[1]
            count = len(df[col_name])
            total_all_col_rec += count

            for lang in langs:
                if f"-{lang}" in file:
                    lang_summary[lang]["appointment recommended count"] += count
                    break

        # อ่านไฟล์ปกติ
        for file in normal_files:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip().str.replace('\ufeff', '')
            col_name = df.columns[1]
            count = len(df[col_name])
            total_all_col += count

            for lang in langs:
                if f"-{lang}" in file:
                    lang_summary[lang]["appointment count"] += count
                    break

        # เติมข้อมูลใน DataFrame สำหรับ plot
        data_frame_for_plot = {
            "lang": [],
            "appointment count": [],
            "appointment recommended count": []
        }

        for lang in langs:
            data_frame_for_plot["lang"].append(lang)
            data_frame_for_plot["appointment count"].append(lang_summary[lang]["appointment count"])
            data_frame_for_plot["appointment recommended count"].append(lang_summary[lang]["appointment recommended count"])

        # เพิ่ม total
        data_frame_for_plot["lang"].append("total")
        data_frame_for_plot["appointment count"].append(total_all_col)
        data_frame_for_plot["appointment recommended count"].append(total_all_col_rec)

        return total_all_col, total_all_col_rec

    # def find_FeedAndPack(self):
    #     folder_path = self.folder_path.get()
    #     if not folder_path or not os.path.isdir(folder_path):
    #         messagebox.showerror("Error", "Please select a valid folder")
    #         return
        
    #     total_all_col_feed, total_all_col_pack = 0, 0 
    #     feedback = glob.glob(os.path.join(folder_path, "*feedback*.csv"))
    #     packages = glob.glob(os.path.join(folder_path, "*packages*.csv"))


    #     # อ่านไฟล์ feedback
    #     for file in feedback:
    #         df = pd.read_csv(file)
    #         df.columns = df.columns.str.strip().str.replace('\ufeff', '')
    #         col_name = df.columns[0]
    #         count = len(df[col_name])
    #         total_all_col_feed += count

    #     # อ่านไฟล์ packages
    #     for file in packages:
    #         df = pd.read_csv(file)
    #         df.columns = df.columns.str.strip().str.replace('\ufeff', '')
    #         col_name = df.columns[0]
    #         count = len(df[col_name])
    #         total_all_col_pack += count

    #     # แสดงผลใน Text widget
    #     self.result_text.delete(1.0, tk.END)  # เคลียร์ข้อความเก่า
    #     self.result_text.insert(tk.END, f"📦 Package Inquiry count: {total_all_col_pack}\n")
    #     self.result_text.insert(tk.END, f"💬 Feedback & Suggestion count: {total_all_col_feed}\n")

    #     return total_all_col_feed, total_all_col_pack

    def find_FeedAndPack(self):
        folder_path = self.folder_path.get()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Please select a valid folder")
            return
        
        # Dictionary to store counts by language
        lang_stats = {}
        
        # Find files
        feedback = glob.glob(os.path.join(folder_path, "*feedback*.csv"))
        packages = glob.glob(os.path.join(folder_path, "*packages*.csv"))
        
        # Function to extract language from filename
        def extract_language(filename):
            # Extract just the filename without path
            basename = os.path.basename(filename)
            # Common language patterns in filenames
            if '_th' in basename.lower() or 'thai' in basename.lower():
                return 'th'
            elif '_en' in basename.lower() or 'english' in basename.lower():
                return 'en'
            elif '_zh' in basename.lower() or 'chinese' in basename.lower():
                return 'zh'
            elif '_ja' in basename.lower() or 'japanese' in basename.lower():
                return 'ja'
            else:
                # Try to detect from filename pattern (e.g., feedback_th.csv, packages_en.csv)
                parts = basename.lower().replace('.csv', '').split('_')
                for part in parts:
                    if part in ['th', 'en', 'zh', 'ar', 'thai', 'english', 'chinese', 'japanese']:
                        return part if len(part) == 2 else {'thai': 'th', 'english': 'en', 'chinese': 'zh', 'japanese': 'ja'}.get(part, part)
                return 'unknown'  # Default if language cannot be determined

        # Process feedback files
        for file in feedback:
            lang = extract_language(file)
            if lang not in lang_stats:
                lang_stats[lang] = {'feedback': 0, 'packages': 0}
            
            try:
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip().str.replace('\ufeff', '')
                if len(df.columns) > 0:
                    col_name = df.columns[0]
                    count = len(df[col_name].dropna())  # Count non-null values
                    lang_stats[lang]['feedback'] += count
            except Exception as e:
                print(f"Error reading {file}: {e}")
        
        # Process packages files
        for file in packages:
            lang = extract_language(file)
            if lang not in lang_stats:
                lang_stats[lang] = {'feedback': 0, 'packages': 0}
            
            try:
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip().str.replace('\ufeff', '')
                if len(df.columns) > 0:
                    col_name = df.columns[0]
                    count = len(df[col_name].dropna())  # Count non-null values
                    lang_stats[lang]['packages'] += count
            except Exception as e:
                print(f"Error reading {file}: {e}")
        
        # Display results in table format
        self.display_language_statistics(lang_stats)

    def display_language_statistics(self, lang_stats):
        """Display language statistics in a formatted table"""
        if not lang_stats:
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, "No files found or no data to display\n")
            return
        
        # Calculate totals
        total_feedback = sum(stats['feedback'] for stats in lang_stats.values())
        total_packages = sum(stats['packages'] for stats in lang_stats.values())
        grand_total = total_feedback + total_packages
        
        # Format table content
        table_content = []
        
        # Header
        header_line = f"{'Lang':<8} | {'Feedback':<8} | {'Packages':<8} | {'Total':<8}"
        separator_line = "-" * len(header_line)
        table_content.append("Language Statistics:")
        table_content.append("=" * 50)
        table_content.append(header_line)
        table_content.append(separator_line)
        
        # Data rows
        for lang in sorted(lang_stats.keys()):
            stats = lang_stats[lang]
            lang_total = stats['feedback'] + stats['packages']
            row = f"{lang:<8} | {stats['feedback']:<8} | {stats['packages']:<8} | {lang_total:<8}"
            table_content.append(row)
        
        # Total row
        table_content.append(separator_line)
        total_row = f"{'Total':<8} | {total_feedback:<8} | {total_packages:<8} | {grand_total:<8}"
        table_content.append(total_row)
        table_content.append("=" * 50)
        table_content.append("")  # Empty line at the end
        
        # Clear previous results and insert new content
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, '\n'.join(table_content))
        
        # Optional: Also print to console for debugging
        print("\nLanguage Statistics:")
        print('\n'.join(table_content))

    def plot_graph_Type_of_Email_by_month(self):
        def custom_input_popup():
            popup = tk.Toplevel(self.root)
            popup.title("Web Commerce")
            popup.geometry("300x130")
            popup.grab_set()  # บังคับให้กรอกก่อนทำอย่างอื่น

            ttk.Label(popup, text="กรอกเลข Web Commerce:").pack(pady=5)

            entry = ttk.Entry(popup)
            entry.pack(pady=5)
            entry.focus()

            result = {'value': None}
            def submit():
                value = entry.get()
                if value.isdigit():
                    result["value"] = int(value)
                    popup.destroy()
                else:
                    messagebox.showerror("Error", "ให้กรอกตัวเลข")

            ttk.Button(popup, text="ตกลง", command=submit).pack(pady=5)

            result = result

            popup.wait_window()  # รอจน popup ถูกปิด
            return result["value"]

        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder")
            return
        
                # ถามเลขเดือนจาก user
        month = custom_input_popup()
        if month is None:
            return  # ผู้ใช้ยกเลิก
        
        
        inq = TotalMonth(folder)
        self.summary = inq.inquiry()
        self.summaryAppointment = self.find_appointment()
        self.summaryFeed = self.find_FeedAndPack()

        # plot graph Type of Email by month

        # translations สำหรับแปลงชื่อ category เป็นภาษาอังกฤษ
        translations = {
            # Russian
            "Общий запрос": "General Inquiry",
            "Узнать про цену": "Estimated Cost",
            "Написать врачу": "Contact My Doctor at Bangkok Hospital Pattaya",
            "Другое": "Other",
            # German
            "Allgemeine Anfrage": "General Inquiry",
            "Vorraussichtliche Kosten": "Estimated Cost",
            "Arzt im Bangkok Hospital Pattaya kontaktieren": "Contact My Doctor at Bangkok Hospital Pattaya",
            "Andere": "Other",
            # Thai
            "สอบถามทั่วไป": "General Inquiry",
            "ค่าใช้จ่าย": "Estimated Cost",
            "ติดต่อกับหมอประจำตัวที่โรงพยาบาลกรุงเทพพัทยา": "Contact My Doctor at Bangkok Hospital Pattaya",
            "อื่นๆ": "Other",
            # Arabic
            "General Inquiry": "General Inquiry",
            "Estimated Cost": "Estimated Cost",
            "Contact My Doctor at Bangkok Hospital Pattaya": "Contact My Doctor at Bangkok Hospital Pattaya",
            "Other": "Other",
            # Chinese
            "普通咨询": "General Inquiry",
            "预估价格咨询": "Estimated Cost",
            "联系芭提雅曼谷医院医生": "Contact My Doctor at Bangkok Hospital Pattaya",
            "其他": "Other",
            # English already in English
            "General Inquiry": "General Inquiry",
            "Estimated Cost": "Estimated Cost",
            "Contact My Doctor at Bangkok Hospital Pattaya": "Contact My Doctor at Bangkok Hospital Pattaya",
            "Other": "Other",
        }

        # รวม count โดยใช้ชื่อหมวดหมู่ภาษาอังกฤษ
        global_summary = defaultdict(int)

        for lang in self.summary:
            for cat, count in self.summary[lang].items():
                eng_cat = translations.get(cat, cat)  # แปลงเป็นอังกฤษ ถ้าไม่มีให้ใช้ชื่อเดิม
                global_summary[eng_cat] += count
            
        global_summary.pop("", None)  # ถ้าไม่มี key จะไม่เกิด error

        # เรียงมากไปน้อย
        sorted_items = sorted(global_summary.items(), key=lambda x: x[1], reverse=True)
        categories_list = [item[0] for item in sorted_items]
        categories_list.append('Package Inquiry')
        categories_list.append('Feedback & Suggestion')
        categories_list.append('Appointment')
        categories_list.append('Appointment Recommended')
        categories_list.append('Web Commerce')
        counts = [item[1] for item in sorted_items]
        counts.append(self.summaryFeed[0])
        counts.append(self.summaryFeed[1])
        counts.append(self.summaryAppointment[0])
        counts.append(self.summaryAppointment[1])
        counts.append(month)

        # ✅ แสดงข้อมูลใน self.result_text
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Summary: Type of Email by Month\n\n")
        for category, count in zip(categories_list, counts):
            self.result_text.insert(tk.END, f"{category:<35}: {count}\n")

        popup = ColorConfig(self.root, 9)
        color_dict = popup.get_result()
        # ถ้าเอาไปใช้กับกราฟ:
        colorX = popup.get_graph_colors(custom_colors=color_dict)

        # วาดกราฟ
        plt.figure(figsize=(10, 5))
        bars = plt.bar(categories_list, counts, color=colorX['bar_colors'][:len(categories_list)])

        # ใส่ตัวเลขบนกราฟ พร้อมเปลี่ยนสีฟอนต์เป็นแดง (เปลี่ยนได้ตามใจ)
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, height + 1, str(height),
                    ha='center', va='bottom', fontsize=10, color=colorX['bar_text_color'])  # <-- เพิ่ม color ตัวเลขบนกราฟ

        plt.ylim(0, max(counts) * 1.2)
        plt.title("Type of Email by month", fontsize=14, color=colorX['title_color'])      # เปลี่ยนสี title
        # plt.xlabel("Category (English)", fontsize=12, color='green')            # เปลี่ยนสี xlabel
        plt.ylabel("Total Count", fontsize=12, color=colorX['ylabel_color'])                   # เปลี่ยนสี ylabel
        plt.xticks(rotation=45, ha='right', color=colorX['xtick_color'])
        plt.yticks(color=colorX['ytick_color'])  # ใส่ตรงนี้
        plt.tight_layout()

        # ✅ เซฟก่อนแสดง
        # temp_path = os.path.join(tempfile.gettempdir(), "plotAll.png")
        # plt.savefig(temp_path)
        # plt.savefig("output_graph.png", dpi=300, transparent=True, bbox_inches='tight')
        
        def get_base_path():
            if getattr(sys, 'frozen', False):
                # 👉 ตอนถูกแปลงเป็น .exe ด้วย pyinstaller
                return sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
            else:
                # 👉 ตอนรันแบบ .py ปกติ
                return os.path.dirname(os.path.abspath(__file__))

        # ใช้ path นี้ในการเซฟ
        save_path = os.path.join(get_base_path(), "plotAll.png")

        # วาดกราฟและเซฟ
        plt.savefig(save_path, dpi=300, transparent=True, bbox_inches='tight')

        plt.show()

    
    def show_find_appointment(self):
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder")
            return

        summary = defaultdict(lambda: defaultdict(int))

        langs = ["ar", "de", "en", "ru", "th", "zh"]
        lang_summary = {lang: {"appointment count": 0, "appointment recommended count": 0} for lang in langs}
        total_all_col_rec, total_all_col = 0, 0

        recommended_files = glob.glob(os.path.join(folder, "*appointment-recommended*.csv"))
        normal_files = [f for f in glob.glob(os.path.join(folder, "*appointment*.csv"))
                        if "appointment-recommended" not in os.path.basename(f)]

        # อ่านไฟล์ recommended
        for file in recommended_files:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip().str.replace('\ufeff', '')
            col_name = df.columns[1]
            count = len(df[col_name])
            total_all_col_rec += count

            for lang in langs:
                if f"-{lang}" in file:
                    lang_summary[lang]["appointment recommended count"] += count
                    break

        # อ่านไฟล์ปกติ
        for file in normal_files:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip().str.replace('\ufeff', '')
            col_name = df.columns[1]
            count = len(df[col_name])
            total_all_col += count

            for lang in langs:
                if f"-{lang}" in file:
                    lang_summary[lang]["appointment count"] += count
                    break

        # เติมข้อมูลใน DataFrame สำหรับ plot
        data_frame_for_plot = {
            "lang": [],
            "appointment count": [],
            "appointment recommended count": []
        }

        for lang in langs:
            data_frame_for_plot["lang"].append(lang)
            data_frame_for_plot["appointment count"].append(lang_summary[lang]["appointment count"])
            data_frame_for_plot["appointment recommended count"].append(lang_summary[lang]["appointment recommended count"])

        # เพิ่ม total
        data_frame_for_plot["lang"].append("total")
        data_frame_for_plot["appointment count"].append(total_all_col)
        data_frame_for_plot["appointment recommended count"].append(total_all_col_rec)


        # ✅ สร้าง DataFrame ก่อนนำไป plot
        df_plot = pd.DataFrame(data_frame_for_plot)
        # self.plot_and_open_with_default_viewer(df_plot)
        # แยก total ออกก่อน (ถ้ามี)
        df_total = df_plot[df_plot['lang'] == 'total']
        df_plot = df_plot[df_plot['lang'] != 'total']


        # สร้างคอลัมน์รวม
        df_plot['total'] = df_plot['appointment count'] + df_plot['appointment recommended count']

        # เรียงลำดับตามค่ารวม
        df_plot = df_plot.sort_values(by='total', ascending=False).reset_index(drop=True)

        # ลบคอลัมน์ total ที่ใช้ช่วยเรียง
        df_plot = df_plot.drop(columns=['total'])

        # ต่อแถว total กลับ
        df_plot = pd.concat([df_plot, df_total], ignore_index=True)

        # print(df_plot)
        self.result_text.delete(1.0, tk.END)

        if True:
            self.result_text.insert(tk.END, df_plot.to_string(index=False))
        else:
            self.result_text.insert(tk.END, "No inquiry data found.")

        # --- Plot ---
        x = df_plot['lang']
        width = 0.35
        x_pos = range(len(x))

        #สีกราฟ
        popup = ColorConfig(self.root, 2)
        color_dict = popup.get_result()
        # ถ้าเอาไปใช้กับกราฟ:
        colorX = popup.get_graph_colors(custom_colors=color_dict)

        
        plt.figure(figsize=(10,6))
        bars1 = plt.bar(x_pos, df_plot['appointment count'], width=width, label='Appointment', color=colorX['bar_colors'][0])
        bars2 = plt.bar([p + width for p in x_pos], df_plot['appointment recommended count'], width=width, label='Recommended', color=colorX['bar_colors'][1])

        # เพิ่มตัวเลขบนแท่งกราฟ
        for bar in bars1:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.5, str(int(height)), ha='center', va='bottom', color=colorX['bar_text_color'])

        for bar in bars2:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.5, str(int(height)), ha='center', va='bottom', color=colorX['bar_text_color'])

        plt.xticks([p + width / 2 for p in x_pos], x, color=colorX['xtick_color'])
        plt.yticks(color=colorX['ytick_color'])  # ใส่ตรงนี้
        plt.xlabel("Language", color=colorX['xlabel_color'])
        plt.ylabel("Count", color=colorX['ylabel_color'])
        plt.title("Appointment vs Recommended by Language", color=colorX['title_color'])
        plt.legend(labelcolor=colorX['title_color'])
        plt.tight_layout()

        def get_base_path():
            if getattr(sys, 'frozen', False):
                # 👉 ตอนถูกแปลงเป็น .exe ด้วย pyinstaller
                return sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
            else:
                # 👉 ตอนรันแบบ .py ปกติ
                return os.path.dirname(os.path.abspath(__file__))

        # ใช้ path นี้ในการเซฟ
        save_path = os.path.join(get_base_path(), "appointment.png")

        # วาดกราฟและเซฟ
        plt.savefig(save_path, dpi=300, transparent=True, bbox_inches='tight')
        # ✅ เซฟก่อนแสดง
        plt.show()

        # ✅ ปิดหลังแสดงผล
        plt.close()

    def top_20(self):
        folder_path = self.folder_path.get()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Please select a valid folder")
            return
        output_path = "./GraphImages"
        langs = ["ar", "de", "en", "ru", "th", "zh-hans"]

        os.makedirs(output_path, exist_ok=True)

        # ชื่อคลินิกใน centers_and_clinics
        centers_and_clinics = {
            "Ambulance Service": 0,
            "Prestige Wellness Center": 0,
            "Dermatology and Plastic Surgery Center": 0,
            "Breast Center": 0,
            "Breast Feeding Clinic": 0,
            "Cardiac Care Unit": 0,
            "Cardiac Cath Lab": 0,
            "Cardiac Rehabilitations": 0,
            "Dental Cosmetic and Implant Center": 0,
            "Diabetes Mellitus (DM) & Endocrinology Center": 0,
            "Diagnostic Imaging Dept (JTH)": 0,
            "Ear Nose Throat Center": 0,
            "Emergency Medical Service Center": 0,
            "Emergency & Accident Dept(JTH)": 0,
            "Eye Center": 0,
            "Fertility Center": 0,
            "Gastrointestinal & Liver Center": 0,
            "Gastrointestinal": 0,
            "Health Promotion Center": 0,
            "Hearing Speech Balance Tinnitus Center": 0,
            "Heart Center": 0,
            "Hemodialysis Center": 0,
            "Hyperbaric Oxygen Therapy": 0,
            "Diagnostic Imaging and Interventional Radiology Center": 0,
            "ICU - Trauma and Surgery": 0,
            "Intermediate Intensive Care": 0,
            "Laboratory": 0,
            "Labour Room": 0,
            "Lasik and SuperSight Surgery Center": 0,
            "Internal Medicine Center": 0,
            "Mental Health Center": 0,
            "Neonatal Intensive Care Unit (NICU)": 0,
            "Neuroscience Center": 0,
            "Nursery": 0,
            "Women's Health Center": 0,
            "Oncology Center": 0,
            "Operating Room": 0,
            "Orthopedic Center": 0,
            "Pediatric Intensive Care Unit or PICU": 0,
            "Child Health Center": 0,
            "Rehabilitation Center": 0,
            "Surgery Center": 0,
            "Urology Center": 0,
            "Wound Care Unit": 0,
            "Hospital Director Office": 0,
            "Medical Staff Organization": 0,
            "Anesthetic": 0,
            "BPH Clinic : Bangsare": 0,
            "BPH Clinic : Bo Win": 0,
            "BPH Clinic : Kreua Sahaphat": 0,
            "ICU Medicine": 0,
            "ICU Neurosciences": 0, 
            "KOH LARN Clinic": 0,
            "Nutrition Therapeutic": 0,
            "U-Tapao Clinic": 0,
            "Jomtien Hospital": 0,
        }

        name_map = {
            "แผนกเคลื่อนย้ายผู้ป่วยทางการแพทย์": "Ambulance Service",
            "ศูนย์ส่งเสริมสุขภาพ": "Prestige Wellness Center",
            "ศูนย์ผิวพรรณและศัลยกรรมความงาม": "Dermatology and Plastic Surgery Center",
            "ศูนย์เต้านม": "Breast Center",
            "ศูนย์สุขภาพสตรี": "Breast Feeding Clinic",
            "ศูนย์หัวใจ": "Cardiac Care Unit",
            "ศูนย์ทันตกรรมความงามและรากเทียม": "Dental Cosmetic and Implant Center",
            "ศูนย์เบาหวานและต่อมไร้ท่อ": "Diabetes Mellitus (DM) & Endocrinology Center",
            "ศูนย์วินิจฉัยและรังสีร่วมรักษา": "Diagnostic Imaging Dept (JTH)",
            "ศูนย์หู คอ จมูก": "Ear Nose Throat Center",
            "แผนกฉุกเฉิน": "Emergency Medical Service Center",
            "ศูนย์ตา": "Eye Center",
            "ศูนย์มีบุตรยาก": "Fertility Center",
            "ศูนย์ระบบทางเดินอาหารและตับ": "Gastrointestinal & Liver Center",
            "ศูนย์เวชศาสตร์ฟื้นฟู": "Rehabilitation Center",
            "ศูนย์สมองและระบบประสาท": "Neuroscience Center",
            "ศูนย์สุขภาพจิต": "Mental Health Center",
            "ศูนย์อายุรกรรมทั่วไป": "Internal Medicine Center",
            "ศูนย์ศัลยกรรมทั่วไป": "Surgery Center",
            "ศูนย์ศัลยกรรมกระดูกและข้อ": "Orthopedic Center",
            "ศูนย์กุมารเวช": "Child Health Center",
            "ศูนย์ศัลยกรรมระบบทางเดินปัสสาวะ": "Urology Center",
            "ศูนย์โรคมะเร็ง": "Oncology Center",
            "ศูนย์แก้ไขสายตาด้วยเลสิคและซุปเปอร์ไซต์": "Lasik and SuperSight Surgery Center",
            "ศูนย์ดูแลแผล": "Wound Care Unit",
            "ศูนย์โภชนบำบัด": "Nutrition Therapeutic",
        }



        total_normal_counts = defaultdict(int)
        total_recommended_counts = defaultdict(int)

        def count_from_files(file_pattern, target_counts):
            files = glob.glob(file_pattern)
            for file in files:
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip().str.replace('\ufeff', '')
                if len(df.columns) < 2:
                    continue
                col_name = df.columns[1]
                for dept in df[col_name].astype(str).str.strip():
                    if dept in centers_and_clinics:
                        target_counts[dept] += 1
                    else:
                        key = name_map.get(dept)
                        if key != None:
                            target_counts[key] += 1
                        else:
                            print(key)
                            

        # รวมข้อมูลจากทุกภาษา
        for lang in langs:
            count_from_files(os.path.join(folder_path, f"appointment-{lang}-*.csv"), total_normal_counts)
            count_from_files(os.path.join(folder_path, f"appointment-recommended-{lang}-*.csv"), total_recommended_counts)

        df_total = pd.DataFrame([
            {
                "clinic": k,
                "appointment count": total_normal_counts[k],
                "recommended count": total_recommended_counts[k],
                "total": total_normal_counts[k] + total_recommended_counts[k]
            }
            for k in centers_and_clinics
        ])

        df_show = df_total
        df_show = df_show.sort_values(by="total", ascending=False)

        self.result_text.configure(font=("Courier New", 10))  # Set font ก่อน
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "📋 Appointment Summary\n\n")
        self.result_text.insert(tk.END, df_show.to_string(index=False))


        print(df_show.to_string(index=False))

        df_total = df_total[df_total["total"] > 0].sort_values(by="total", ascending=False).head(20)
        df_total.to_csv(os.path.join(output_path, "top_20_clinic_summary_all_languages.csv"), index=False, encoding='utf-8-sig')

        # --- สร้างกราฟรวม ---
        x = np.arange(len(df_total))
        width = 0.25
        plt.figure(figsize=(max(12, len(df_total) * 0.7), 6))

        popup = ColorConfig(root, 3)
        color_dict = popup.get_result()
        colorX = popup.get_graph_colors(custom_colors=color_dict)

        bars1 = plt.bar(x - width, df_total["appointment count"], width=width, label='Appointment', color=colorX['bar_colors'][0])
        bars2 = plt.bar(x, df_total["recommended count"], width=width, label='Recommended', color=colorX['bar_colors'][1])
        bars3 = plt.bar(x + width, df_total["total"], width=width, label='Total', color=colorX['bar_colors'][2])

        plt.xticks(x, df_total["clinic"], rotation=45, ha='right', color=colorX['xtick_color'])
        plt.yticks(color=colorX['ytick_color'])  # ใส่ตรงนี้
        plt.xlabel("Clinic / Center", color=colorX['xlabel_color'])
        plt.ylabel("Count", color=colorX['ylabel_color'])
        plt.title("Top 20 Clinics - All Languages Combined", color=colorX['title_color'])
        plt.legend(labelcolor=colorX['title_color'])
        plt.tight_layout()
        # plt.grid(axis='y', linestyle='--', alpha=0.7)

        max_height = df_total[["appointment count", "recommended count", "total"]].values.max()
        plt.ylim(0, max_height * 1.2 if max_height > 0 else 1)

        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    plt.text(bar.get_x() + bar.get_width() / 2., height + 0.1, str(int(height)), 
                            ha='center', va='bottom', fontsize=8, color=colorX['bar_text_color'])

        def get_base_path():
            if getattr(sys, 'frozen', False):
                # 👉 ตอนถูกแปลงเป็น .exe ด้วย pyinstaller
                return sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
            else:
                # 👉 ตอนรันแบบ .py ปกติ
                return os.path.dirname(os.path.abspath(__file__))

        # ใช้ path นี้ในการเซฟ
        save_path = os.path.join(get_base_path(), "top20.png")

        # วาดกราฟและเซฟ
        plt.savefig(save_path, dpi=300, transparent=True, bbox_inches='tight')
        plt.show()


    def total_month(self):
        """
        ค้นหาและสรุปข้อมูล Inquiry (รวมถึง Sales, Support, General), Estimated Cost,
        Contact My Doctor at BPH, และ Other จากไฟล์ CSV ในโฟลเดอร์ที่กำหนด.
        จะอ่านไฟล์ CSV, จัดหมวดหมู่ตามภาษา, นับจำนวนแต่ละหมวดหมู่,
        และคำนวณผลรวมรวมทั้งหมดสำหรับแต่ละภาษาและผลรวมรวมทั้งหมด.
        """
        folder = self.folder_path.get()

        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder")
            return
        
        self.result_text.delete(1.0, tk.END)
        over = Overall(folder)
        inq, raw = over.find_inquiry()
        self.result_text.insert(tk.END, inq)

        each_lang_FeedAndPack = TotalMonth(folder)
        each = each_lang_FeedAndPack.each_FeedAndPack()
        self.result_text.insert(tk.END, each)

        each_lang_appointment_sum = TotalMonth(folder)
        self.result_text.insert(tk.END, each_lang_appointment_sum.each_appointment())


        data, graph = over.find_all_summaries()
        self.result_text.insert(tk.END, data)
        
        over._create_and_show_plot(graph, root)
        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = InquiryApp(root)
    root.mainloop()