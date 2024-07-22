import pandas as pd

# Создать DataFrame (для удобной работы с табличными данными)
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']}
df = pd.DataFrame(data)

# Вывод DataFrame
print(df)
