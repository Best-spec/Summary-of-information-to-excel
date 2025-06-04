import pandas as pd
import os
import glob
from collections import defaultdict
import tkinter as tk # สมมติว่าคุณใช้ Tkinter สำหรับ UI
from tkinter import messagebox
import matplotlib.pyplot as plt # Import for plotting

# --- จำเป็นต้องมีตัวแปร categories นี้อยู่จริงในโค้ดของคุณ ---
# หากคุณประกาศไว้ที่อื่นแล้ว ไม่ต้องประกาศซ้ำที่นี่
# แต่ถ้ายังไม่มี ต้องมั่นใจว่า categories มีข้อมูลตามโครงสร้างนี้
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

# Helper mapping for full language names to their codes
lang_name_to_code = {
    "English": "en", "Thai": "th", "Russia": "ru",
    "German": "de", "Arabic": "ar", "Chinese": "zh"
}
# Helper mapping for language codes to full names (for display)
lang_code_to_name = {
    "en": "English", "th": "Thai", "ru": "Russia",
    "de": "German", "ar": "Arabic", "zh": "Chinese"
}


class Overall:
    def __init__(self, folder_path_var):
        """
        Constructor สำหรับ InquiryApp.
        Args:
            folder_path_var (tk.StringVar): ตัวแปร Tkinter StringVar ที่เก็บ path ของโฟลเดอร์.
            result_text_widget (tk.Text): Tkinter Text widget สำหรับแสดงผลลัพธ์.
        """
        self.folder_path = folder_path_var



    def find_inquiry(self):
        """
        ค้นหาและสรุปข้อมูล Inquiry จากไฟล์ CSV ในโฟลเดอร์ที่กำหนด.
        จะอ่านไฟล์ CSV, จัดหมวดหมู่ตามภาษา, นับจำนวน Inquiry ในแต่ละหมวดหมู่,
        และคำนวณผลรวม Inquiry ทั้งหมดในแต่ละภาษา.
        Returns:
            dict: ผลรวม Inquiry แยกตามภาษา (e.g., {'English': 100, 'Thai': 50}).
        """
        folder = self.folder_path
        if not folder or not os.path.isdir(folder):
            # ไม่แสดง messagebox ที่นี่ เพราะ find_all_summaries จะจัดการ
            return {}

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

            lang = None
            if "-en" in file: lang = "English"
            elif "-th" in file: lang = "Thai"
            elif "-ru" in file: lang = "Russia"
            elif "-de" in file: lang = "German"
            elif "-ar" in file: lang = "Arabic"
            elif "-zh" in file: lang = "Chinese"
            else: continue

            if col_name in df.columns and not df[col_name].empty:
                for cat in categories.get(lang, []):
                    count = df[col_name].astype(str).str.strip().eq(cat).sum()
                    summary[lang][cat] += count
        
        total_inquiry_by_lang = {
            lang: sum(cats.values()) 
            for lang, cats in summary.items()
        }

        def format_lang_counts(lang_counts: dict) -> str:
            lines = []
            for lang, count in lang_counts.items():
                lines.append(f"{lang}: {int(count)}")
            return "\n".join(lines)

        text_output = format_lang_counts(total_inquiry_by_lang)
        return text_output, total_inquiry_by_lang

    def find_FeedAndPack(self):
        """
        ค้นหาและสรุปข้อมูล Feedback & Suggestion และ Package Inquiry จากไฟล์ CSV ในโฟลเดอร์ที่กำหนด.
        Returns:
            tuple: (dict of feedback counts by language, dict of package counts by language).
        """
        folder_path = self.folder_path
        if not folder_path or not os.path.isdir(folder_path):
            return {}, {}
        
        feed_counts_by_lang = defaultdict(int)
        pack_counts_by_lang = defaultdict(int)

        all_csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

        for file in all_csv_files:
            lang = None
            if "-en" in file: lang = "English"
            elif "-th" in file: lang = "Thai"
            elif "-ru" in file: lang = "Russia"
            elif "-de" in file: lang = "German"
            elif "-ar" in file: lang = "Arabic"
            elif "-zh" in file: lang = "Chinese"
            else: continue

            try:
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip().str.replace('\ufeff', '')
                col_name = df.columns[0] # Assuming first column for counting rows
                count = len(df[col_name])
            except Exception as e:
                print(f"Failed to process {file}: {e}")
                continue

            if "feedback-suggestion" in file and lang:
                feed_counts_by_lang[lang] += count
            elif "packages" in file and lang:
                pack_counts_by_lang[lang] += count

        return dict(feed_counts_by_lang), dict(pack_counts_by_lang)

    def find_appointment(self):
        """
        ค้นหาและสรุปข้อมูล Appointment และ Appointment Recommended จากไฟล์ CSV ในโฟลเดอร์ที่กำหนด.
        Returns:
            dict: ผลรวม Appointment และ Appointment Recommended แยกตามรหัสภาษา
                  (e.g., {'en': {'appointment count': 902, 'appointment recommended count': 617}}).
        """
        folder = self.folder_path
        if not folder or not os.path.isdir(folder):
            return {}

        langs_codes = ["ar", "de", "en", "ru", "th", "zh"]
        lang_summary = {lang_code: {"appointment count": 0, "appointment recommended count": 0} for lang_code in langs_codes}
        
        recommended_files = glob.glob(os.path.join(folder, "*appointment-recommended*.csv"))
        normal_files = [f for f in glob.glob(os.path.join(folder, "*appointment*.csv"))
                        if "appointment-recommended" not in os.path.basename(f)]

        def get_lang_from_filename(filename):
            for code in langs_codes:
                if f"-{code}" in filename:
                    return code
            return None

        for file in recommended_files:
            lang_code = get_lang_from_filename(file)
            if not lang_code: continue
            try:
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip().str.replace('\ufeff', '')
                col_name = df.columns[1] # Assuming second column for counting rows
                count = len(df[col_name])
                lang_summary[lang_code]["appointment recommended count"] += count
            except Exception as e:
                print(f"Failed to process {file}: {e}")
                continue

        for file in normal_files:
            lang_code = get_lang_from_filename(file)
            if not lang_code: continue
            try:
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip().str.replace('\ufeff', '')
                col_name = df.columns[1] # Assuming second column for counting rows
                count = len(df[col_name])
                lang_summary[lang_code]["appointment count"] += count
            except Exception as e:
                print(f"Failed to process {file}: {e}")
                continue

        return lang_summary
    
    def find_all_summaries(self):
        """
        เรียกใช้เมธอด find_inquiry, find_FeedAndPack, และ find_appointment
        เพื่อรวบรวมและแสดงผลรวมทั้งหมดของ Inquiry, Package, Feedback, Appointment
        และ Appointment Recommended แยกตามแต่ละภาษา.
        """
        folder = self.folder_path # Corrected from self.folder_path
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder")
            return

        # Get individual summaries
        data, inquiry_totals = self.find_inquiry()
        feed_counts, pack_counts = self.find_FeedAndPack()
        appointment_summary = self.find_appointment()

        # Initialize combined totals for all known languages
        # Use lang_code_to_name.values() to get full names from codes
        all_languages_names = sorted(list(set(categories.keys()) | set(feed_counts.keys()) | set(pack_counts.keys()) | set(lang_code_to_name.values())))
        
        combined_totals = defaultdict(lambda: {
            "Inquiry": 0,
            "Package": 0,
            "Feedback": 0,
            "Appointment": 0,
            "Appointment Recommended": 0,
            "Total for Language": 0 # This will be the sum of all categories for this language
        })

        for lang_name in all_languages_names:
            lang_code = lang_name_to_code.get(lang_name) # Get code if available

            # Add Inquiry totals
            combined_totals[lang_name]["Inquiry"] = inquiry_totals.get(lang_name, 0)

            # Add Package and Feedback totals
            combined_totals[lang_name]["Package"] = pack_counts.get(lang_name, 0)
            combined_totals[lang_name]["Feedback"] = feed_counts.get(lang_name, 0)

            # Add Appointment totals (using language code)
            if lang_code and lang_code in appointment_summary:
                combined_totals[lang_name]["Appointment"] = appointment_summary[lang_code].get("appointment count", 0)
                combined_totals[lang_name]["Appointment Recommended"] = appointment_summary[lang_code].get("appointment recommended count", 0)

            # Calculate total for this specific language
            combined_totals[lang_name]["Total for Language"] = (
                combined_totals[lang_name]["Inquiry"] +
                combined_totals[lang_name]["Package"] +
                combined_totals[lang_name]["Feedback"] +
                combined_totals[lang_name]["Appointment"] +
                combined_totals[lang_name]["Appointment Recommended"]
            )

        # Format output for display (text summary)
        output_lines = []
        output_lines.append("--- Combined Totals by Language ---")
        output_lines.append("")

        grand_total_all_categories = 0

        if not combined_totals:
            output_lines.append("No data found across all categories.")
        else:
            # Prepare data for plotting and text display, sorted by Total for Language (descending)
            sorted_combined_totals = sorted(combined_totals.items(), key=lambda item: item[1]["Total for Language"], reverse=True)
            
            plot_data = [] # Data for the plot: [(language_name, total_count), ...]

            for lang_name, lang_data in sorted_combined_totals:
                output_lines.append(f"Language: {lang_name}")
                output_lines.append(f"  Inquiry: {lang_data['Inquiry']}")
                output_lines.append(f"  Package: {lang_data['Package']}")
                output_lines.append(f"  Feedback: {lang_data['Feedback']}")
                output_lines.append(f"  Appointment: {lang_data['Appointment']}")
                output_lines.append(f"  Appointment Recommended: {lang_data['Appointment Recommended']}")
                output_lines.append(f"  --- Total for {lang_name}: {lang_data['Total for Language']}")
                output_lines.append("")
                grand_total_all_categories += lang_data['Total for Language']
                
                # Add to plot data
                plot_data.append((lang_name, lang_data['Total for Language']))

        output_lines.append("--- Grand Total Across All Languages and Categories ---")
        output_lines.append(f"Grand Total: {grand_total_all_categories}")
        output_lines.append("---")

        readable_text = "\n".join(output_lines)

        # Display text summary in Text widget
        # self.result_text.delete(1.0, tk.END)
        text_to_insert = str(readable_text)
        return text_to_insert, plot_data
    
    def _create_and_show_plot(self, plot_data):
        """
        สร้างและแสดงกราฟแท่งของยอดรวมแต่ละภาษาในหน้าต่างแยกต่างหาก.
        Args:
            plot_data (list of tuples): ข้อมูลสำหรับพล็อตในรูปแบบ [(language_name, total_count), ...].
        """
        if not plot_data:
            messagebox.showinfo("No Data", "No data available to plot.")
            return

        languages = [item[0] for item in plot_data]
        totals = [item[1] for item in plot_data]

        # Create a figure and a set of subplots
        fig, ax = plt.subplots(figsize=(10, 6)) 
        
        # Create the bar chart
        bars = ax.bar(languages, totals, color='skyblue')
        
        # Add labels and title
        ax.set_xlabel("Language")
        ax.set_ylabel("Total Count")
        ax.set_title("Combined Total Inquiries by Language (Sorted Descending)")
        
        # Rotate x-axis labels if too many languages
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on top of bars
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 5, round(yval), ha='center', va='bottom')

        plt.tight_layout() # Adjust layout to prevent labels from overlapping
        
        # Show the plot in a separate window
        plt.show()
