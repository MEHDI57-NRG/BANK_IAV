import csv
import os

class CSVManager:
    def __init__(self, filename):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as file:
                pass

    def read_data(self):
        with open(self.filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)

    def write_data(self, data):
        with open(self.filename, 'w', newline='') as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    

    def get_num_rows(self):
        with open(self.filename, 'r', newline='') as file:
            reader = csv.reader(file)
            num_rows = sum(1 for row in reader)
        return num_rows - 1 if num_rows != 0 else num_rows
