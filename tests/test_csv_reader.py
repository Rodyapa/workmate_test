import pytest
import os
import tempfile
import csv
from unittest.mock import MagicMock
import sys
from pathlib import Path

# Добавляем путь к папке src
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from csv_reader import CSVReader

class TestCSVReader:
    """Тесты для класса CSVReader"""

    @pytest.fixture
    def sample_csv_file(self):
        """Возвращает путь к существующему CSV файлу с тестовыми данными"""
        return str(Path(__file__).parent / "test_data" / "test.csv")

    @pytest.fixture
    def mock_args(self):
        """Создает mock аргументов"""
        args = MagicMock()
        args.where = None
        args.aggregate = None
        return args

    def test_init(self, sample_csv_file, mock_args):
        """Тест инициализации класса"""
        reader = CSVReader(sample_csv_file, mock_args)
        assert reader.path == sample_csv_file
        assert reader.args == mock_args

    def test_get_path_valid(self, sample_csv_file, mock_args):
        """Тест получения валидного пути"""
        reader = CSVReader(sample_csv_file, mock_args)
        result = reader._get_path()
        assert result == sample_csv_file

    def test_get_path_invalid(self, mock_args, capsys):
        """Тест получения невалидного пути"""
        reader = CSVReader("nonexistent_file.csv", mock_args)
        with pytest.raises(SystemExit) as exc_info:
            reader._get_path()
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Файл nonexistent_file.csv не найден" in captured.out

    def test_read_basic(self, sample_csv_file, mock_args, capsys):
        """Тест базового чтения CSV файла"""
        reader = CSVReader(sample_csv_file, mock_args)
        reader.read()

        captured = capsys.readouterr()
        assert "name" in captured.out
        assert "price" in captured.out
        assert "iphone 15 pro" in captured.out
        assert "galaxy s23 ultra" in captured.out

    def test_filter_equals_string(self, sample_csv_file, mock_args):
        """Тест фильтрации с оператором = для строк"""
        reader = CSVReader(sample_csv_file, mock_args)
        reader._get_path()
        with open(sample_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            data = [row for row in reader_csv]

        result = reader._filter("brand=apple", data)
        assert len(result) == 4
        assert result[0][1] == "apple"  # brand column (индекс 1)

    def test_filter_greater_than_numeric(self, sample_csv_file, mock_args):
        """Тест фильтрации с оператором > для чисел"""
        reader = CSVReader(sample_csv_file, mock_args)
        reader._get_path()
        with open(sample_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            data = [row for row in reader_csv]

        result = reader._filter("price>500", data)
        assert len(result) == 5  # iphone и galaxy
        assert all(float(row[2]) > 500 for row in result)

    def test_filter_less_than_numeric(self, sample_csv_file, mock_args):
        """Тест фильтрации с оператором < для чисел"""
        reader = CSVReader(sample_csv_file, mock_args)
        reader._get_path()
        with open(sample_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            data = [row for row in reader_csv]

        result = reader._filter("price<300", data)
        assert len(result) == 3  # redmi и poco
        assert all(float(row[2]) < 300 for row in result)

    def test_filter_invalid_expression(
            self, sample_csv_file, mock_args, capsys):
        """Тест фильтрации с невалидным выражением"""
        reader = CSVReader(sample_csv_file, mock_args)
        reader._get_path()
        with open(sample_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            data = [row for row in reader_csv]

        with pytest.raises(SystemExit) as exc_info:
            reader._filter("invalid_expression", data)
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert ("Укажите значение для аргумента "
                "--where в формате" in captured.out)

    def test_filter_column_not_found(self, sample_csv_file, mock_args, capsys):
        """Тест фильтрации с несуществующей колонкой"""
        reader = CSVReader(sample_csv_file, mock_args)
        reader._get_path()
        with open(sample_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            data = [row for row in reader_csv]

        with pytest.raises(SystemExit) as exc_info:
            reader._filter("nonexistent_column>100", data)
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Колонка nonexistent_column не найдена" in captured.out

    def test_aggregate_min(self, sample_csv_file, mock_args):
        """Тест агрегации с min"""
        reader = CSVReader(sample_csv_file, mock_args)
        reader._get_path()
        with open(sample_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            data = [row for row in reader_csv]

        result = reader._aggregate("price=min", data)
        assert result == [['149.0']]  # минимальная цена

    def test_aggregate_max(self, sample_csv_file, mock_args):
        """Тест агрегации с max"""
        reader = CSVReader(sample_csv_file, mock_args)
        reader._get_path()
        with open(sample_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            data = [row for row in reader_csv]

        result = reader._aggregate("price=max", data)
        assert result == [['1199.0']]  # максимальная цена

    def test_aggregate_avg(self, sample_csv_file, mock_args):
        """Тест агрегации с avg"""
        reader = CSVReader(sample_csv_file, mock_args)
        reader._get_path()
        with open(sample_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            data = [row for row in reader_csv]

        result = reader._aggregate("price=avg", data)
        expected_avg = 602.0
        assert result == [[str(expected_avg)]]

    def test_aggregate_invalid_expression(
            self, sample_csv_file, mock_args, capsys):
        """Тест агрегации с невалидным выражением"""
        reader = CSVReader(sample_csv_file, mock_args)
        reader._get_path()
        with open(sample_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            data = [row for row in reader_csv]

        with pytest.raises(SystemExit) as exc_info:
            reader._aggregate("invalid_expression", data)
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert ("Укажите значение для аргумента "
                "--aggregate в формате" in captured.out)

    def test_aggregate_column_not_found(
            self, sample_csv_file, mock_args, capsys):
        """Тест агрегации с несуществующей колонкой"""
        reader = CSVReader(sample_csv_file, mock_args)
        reader._get_path()
        with open(sample_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            data = [row for row in reader_csv]

        with pytest.raises(SystemExit) as exc_info:
            reader._aggregate("nonexistent_column=min", data)
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Колонка nonexistent_column не найдена" in captured.out

    def test_aggregate_invalid_operation(
            self, sample_csv_file, mock_args, capsys):
        """Тест агрегации с невалидной операцией"""
        reader = CSVReader(sample_csv_file, mock_args)
        reader._get_path()
        with open(sample_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            data = [row for row in reader_csv]

        with pytest.raises(SystemExit) as exc_info:
            reader._aggregate("price=invalid", data)
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert ("Укажите значение для аргумента "
                "--aggregate в формате: "
                '"column=value". value может быть min, avg, max'
                in captured.out)

    def test_aggregate_string_column(self, sample_csv_file, mock_args, capsys):
        """Тест агрегации строковой колонки (должна вызывать ошибку)"""
        reader = CSVReader(sample_csv_file, mock_args)
        reader._get_path()
        with open(sample_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            data = [row for row in reader_csv]

        with pytest.raises(SystemExit) as exc_info:
            reader._aggregate("name=min", data)
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Агрегация поддерживается только для чисел" in captured.out
