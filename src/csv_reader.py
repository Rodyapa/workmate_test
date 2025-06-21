import csv
import os
import re

from tabulate import tabulate


# Класс для чтения CSV файлов
class CSVReader:
    """
    Класс для чтения CSV файлов.
    Атрибуты:
    - path: str - путь к csv файлу
    - args: argparse.Namespace - аргументы командной строки
    - headers: list[str] - заголовки столбцов
    - data: list[list[str]] - данные из csv файла

    Методы:
    - __init__(self, path, args) - инициализация класса
    - read(self) - чтение csv файла и печать в табличном виде
    - _get_path(self) - получение пути к csv файлу
    - _filter(self, expression) - фильтрация данных
    - _aggregate(self, expression) - агрегация данных

    Чтобы расширить функционал, нужно добавить новые внутренние методы.
    Затем добавить их в метод read.
    """
    def __init__(self, path, args):
        self.path = path
        self.args = args

    def read(self) -> None:
        """
        Чтение csv файла и печать в табличном виде
        """
        path = self._get_path()
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            self.headers = next(reader)
            data = [row for row in reader]
            if self.args.where:
                data = self._filter(self.args.where, data)
            if self.args.aggregate:
                data = self._aggregate(self.args.aggregate, data)
        print(tabulate(data, headers=self.headers, tablefmt="grid"))

    def _get_path(self) -> str:
        """
        Получение пути к csv файлу
        """
        if not os.path.exists(self.path):
            print(f"Файл {self.path} не найден")
            exit(1)
        return self.path

    def _filter(self, expression, data) -> list[list[str]]:
        """
        Фильтрация данных
        """
        # Проверяем выражение
        valid_exp_pattern = (r"^(?P<column>[a-zA-Z0-9_ ]+)"
                             r"(?P<operator>[<>=])"
                             r"(?P<value>[a-zA-Z0-9\._ ]+)$")
        if (not isinstance(expression, str)
                or not re.match(valid_exp_pattern, expression)):
            print('Укажите значение для аргумента --where в формате: "column+value". '
                  'Можно использовать операторы <, >, =')
            exit(1)

        # Получаем столбец, оператор и значение
        column, operator, value = (
            re.match(valid_exp_pattern, expression).groups())

        # Проверяем столбец и оператор
        if column not in self.headers:
            print(f"Колонка {column} не найдена")
            exit(1)
        if operator not in ["<", ">", "="]:
            print(f"Оператор {operator} не поддерживается")
            exit(1)
        
        # Фильтруем данные
        if operator == "<":
            try:
                return [row for row in data if float(row[self.headers.index(column)]) < float(value)]
            except ValueError:
                return [row for row in data if row[self.headers.index(column)] < value]
        elif operator == ">":
            try:
                return [row for row in data if float(row[self.headers.index(column)]) > float(value)]
            except ValueError:
                return [row for row in data if row[self.headers.index(column)] > value]
        elif operator == "=":
            return [row for row in data if row[self.headers.index(column)] == value]

        return data

    def _aggregate(self, expression, data) -> list[list[str]]:
        """
        Агрегация данных
        """
        # Проверяем выражение
        valid_exp_pattern = r"^(?P<column>[a-zA-Z0-9_ ]+)=(?P<value>min|avg|max)$"
        if not isinstance(expression, str) or not re.match(valid_exp_pattern, expression):
            print('Укажите значение для аргумента --aggregate в формате: "column=value". '
                  'value может быть min, avg, max')
            exit(1)

        # Получаем столбец и значение
        column, value = re.match(valid_exp_pattern, expression).groups()

        # Проверяем столбец и оператор
        if column not in self.headers:
            print(f"Колонка {column} не найдена")
            exit(1)
        if value not in ["min", "avg", "max"]:
            print(f"Значение {value} не поддерживается")
            exit(1)

        # Получаем все значения в столбце
        col_idx = self.headers.index(column)
        col_values = [row[col_idx] for row in data]

        # Проверяем, что все значения числа
        try:
            col_values = [float(v) for v in col_values]
        except ValueError:
            print("Агрегация поддерживается только для чисел")
            exit(1)

        # Агрегируем данные
        if not col_values:
            return [["Нет данных"]]
        
        if value == "min":
            return [[str(min(col_values))]]
        elif value == "avg":
            return [[str(round(sum(col_values) / len(col_values), 2))]]
        elif value == "max":
            return [[str(max(col_values))]]

        return data
