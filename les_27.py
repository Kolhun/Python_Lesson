import os
import time

directory = "D:\PythonProject\Python_Lesson"

for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)
        file_size = os.path.getsize(file_path)
        file_last_modified = os.path.getmtime(file_path)
        file_last_modified_formatted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_last_modified))
        parent_directory = os.path.dirname(file_path)

        print(f"Файл: {file_path}")
        print(f"Размер файла: {file_size} байт")
        print(f"Время последнего изменения файла: {file_last_modified_formatted}")
        print(f"Родительская директория файла: {parent_directory}")
        print()
