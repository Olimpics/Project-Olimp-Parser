import pandas as pd
import os

input_dir = r"C:\Users\brawl\projects\microservice\fastapi-project\input_files"

os.makedirs(input_dir, exist_ok=True)

data = {
    "ПІБ": ["Іванов Іван Іванович", "Петров Петро Петрович"],
    "Статус": [1, 1],
    "Дата початку навчання": ["2021-09-01", "2021-09-01"],
    "Дата закінчення навчання": ["2025-06-30", "2025-06-30"],
    "Курс": [2, 2],
    "Факультет ID": [1, 1],
    "Освітній ступінь ID": [1, 1],
    "Форма навчання ID": [1, 1],
    "Скорочений": [0, 0],
    "Освітня програма ID": [1, 2],
    "Кафедра ID": [1, 1],
    "Група ID": [1, 2]
}

df = pd.DataFrame(data)

file_path = os.path.join(input_dir, "student.xlsx")
df.to_excel(file_path, index=False)

print(f"Sample file created at {file_path}")