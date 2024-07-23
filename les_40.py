import pandas as pd

# Создание словаря
data = {
    'name': 'Иван',
    'id': '001',
    'param': 'значение'
}

# Запись словаря в файл в формате JSON
with open('data.json', 'w') as file:
    file.write(pd.Series(data).to_json())

# Загрузка данных из файла и отображение в консоли с использованием dump(2)
with open('data.json', 'r') as file:
    loaded_data = pd.read_json(file.read(), typ='series')
    print(loaded_data.to_json(orient='index', indent=2))
