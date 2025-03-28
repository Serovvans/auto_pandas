# auto-pandas
Этот проект включает скрипт auto-data-frame.py, который представляет собой надстройку над pandas и предоставляет дополнительные возможности для анализа данных с использованием моделей машинного обучения.

## Установка
Для установки необходимых зависимостей выполните следующие шаги:

1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/Serovvans/auto_pandas
    ```

2. Настройте конфигурацию установки для llama-cpp
    Для MacOS на M1
    ```bash
    CMAKE_ARGS="-DCMAKE_OSX_ARCHITECTURES=arm64 -DCMAKE_APPLE_SILICON_PROCESSOR=arm64 -DLLAMA_METAL=on" pip install --upgrade --verbose --force-reinstall --no-cache-dir llama-cpp-python
    ```
    Для Linux и MacOS(Intel)
    ```bash
    CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS"
    ```
    Для Windows
    ```bash
    CMAKE_GENERATOR = "MinGW Makefiles"
    CMAKE_ARGS = "-DLLAMA_OPENBLAS=on -DCMAKE_C_COMPILER=C:/w64devkit/bin/gcc.exe -DCMAKE_CXX_COMPILER=C:/w64devkit/bin/g++.exe"
    ```

3. Установите зависимости из requirements.txt:

    ```bash
    pip install -r auto_pandas/requirements.txt
    ```

## Использование
auto_data_frame.py
Этот скрипт предоставляет класс AutoDataFrame, который расширяет возможности pandas.DataFrame и включает методы для автоматической генерации кода на основе описания задачи и данных.

Пример использования
```python
import auto_pandas.auto_data_frame as adf

# Чтение CSV файла и создание экземпляра AutoDataFrame
df = adf.read_csv('path/to/your/data.csv')

# Генерация функции для получения статистики
statistic_code = df.get_statistic("Calculate the average value for the column 'age'.")

print(statistic_code)

# Генерация функции для изменения таблицы
change_code = df.change_table("Add a new column 'age_group' based on the column 'age'.")

print(change_code)

# Генерация функции для построения графика
plot_code = df.plot_by_promt("Create a histogram for the column 'age'.")

print(plot_code)
```
