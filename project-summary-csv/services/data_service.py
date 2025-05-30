import csv

class DataService:
    @staticmethod
    def load_inquiries():
        try:
            with open("data/inquiries.csv", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            return []
