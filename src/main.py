import argparse

from csv_reader import CSVReader

# Парсим аргументы
parser = argparse.ArgumentParser(description="Считыватель CSV файлов", add_help=False)
parser.add_argument("-h", "--help", action="help", help="Показать справку")
parser.add_argument("-f", "--file", type=str, help="Путь к csv файлу", required=True)
parser.add_argument("-a", "--aggregate",  help="Агрегировать данные", required=False)
parser.add_argument("-w", "--where", help="Фильтровать данные", required=False)

args = parser.parse_args()

# Создаем экземпляр класса CSVReader и читаем данные
csv_reader = CSVReader(args.file, args)
csv_reader.read()
