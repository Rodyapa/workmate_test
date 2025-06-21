import pytest
import tempfile
import csv
import os
import sys
from pathlib import Path

# Добавляем путь к папке src
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.csv_reader import CSVReader
from unittest.mock import MagicMock

class TestEdgeCases:
    """Тесты граничных случаев и обработки ошибок"""

    @pytest.fixture
    def empty_csv_file(self):
        """Создает пустой CSV файл"""
        with tempfile.NamedTemporaryFile(
                mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'price', 'rating'])  # только заголовки
            temp_file = f.name

        yield temp_file
        os.unlink(temp_file)

    @pytest.fixture
    def single_row_csv_file(self):
        """Создает CSV файл с одной строкой данных"""
        with tempfile.NamedTemporaryFile(
                mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'price', 'rating'])
            writer.writerow(['test phone', '100', '4.5'])
            temp_file = f.name

        yield temp_file
        os.unlink(temp_file)

    @pytest.fixture
    def mixed_data_csv_file(self):
        """Создает CSV файл со смешанными типами данных"""
        with tempfile.NamedTemporaryFile(
                mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'price', 'rating', 'available'])
            writer.writerow(['phone1', '100', '4.5', 'true'])
            writer.writerow(['phone2', '200', '4.0', 'false'])
            writer.writerow(['phone3', '150', '4.2', 'true'])
            temp_file = f.name

        yield temp_file
        os.unlink(temp_file)

    @pytest.fixture
    def mock_args(self):
        """Создает mock аргументов"""
        args = MagicMock()
        args.where = None
        args.aggregate = None
        return args

    def test_empty_csv_file(self, empty_csv_file, mock_args, capsys):
        """Тест обработки пустого CSV файла (только заголовки)"""
        reader = CSVReader(empty_csv_file, mock_args)
        reader.read()

        captured = capsys.readouterr()
        assert "name" in captured.out
        assert "price" in captured.out
        assert "rating" in captured.out
        # Не должно быть данных
        assert "test" not in captured.out

    def test_single_row_csv_file(self, single_row_csv_file, mock_args, capsys):
        """Тест CSV файла с одной строкой данных"""
        reader = CSVReader(single_row_csv_file, mock_args)
        reader.read()

        captured = capsys.readouterr()
        assert "test phone" in captured.out
        assert "100" in captured.out
        assert "4.5" in captured.out

    def test_filter_empty_result(self, single_row_csv_file, mock_args):
        """Тест фильтрации с пустым результатом"""
        reader = CSVReader(single_row_csv_file, mock_args)
        reader._get_path()
        with open(single_row_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            reader.data = [row for row in reader_csv]

        result = reader._filter("price>1000", reader.data)
        assert len(result) == 0

    def test_filter_all_results(self, single_row_csv_file, mock_args):
        """Тест фильтрации, возвращающей все результаты"""
        reader = CSVReader(single_row_csv_file, mock_args)
        reader._get_path()
        with open(single_row_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            reader.data = [row for row in reader_csv]

        result = reader._filter("price>0", reader.data)
        assert len(result) == 1
        assert result[0][1] == "100"

    def test_aggregate_single_value(self, single_row_csv_file, mock_args):
        """Тест агрегации одного значения"""
        reader = CSVReader(single_row_csv_file, mock_args)
        reader._get_path()
        with open(single_row_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            reader.data = [row for row in reader_csv]

        result = reader._aggregate("price=min", reader.data)
        assert result == [['100.0']]

        result = reader._aggregate("price=max", reader.data)
        assert result == [['100.0']]

        result = reader._aggregate("price=avg", reader.data)
        assert result == [['100.0']]

    def test_filter_with_spaces_in_column_name(
            self, mixed_data_csv_file, mock_args):
        """Тест фильтрации с пробелами в названии колонки"""
        reader = CSVReader(mixed_data_csv_file, mock_args)
        reader._get_path()
        with open(mixed_data_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            reader.data = [row for row in reader_csv]

        result = reader._filter("name=phone1", reader.data)
        assert len(result) == 1
        assert result[0][0] == "phone1"

    def test_filter_boolean_values(self, mixed_data_csv_file, mock_args):
        """Тест фильтрации булевых значений"""
        reader = CSVReader(mixed_data_csv_file, mock_args)
        reader._get_path()
        with open(mixed_data_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            reader.data = [row for row in reader_csv]

        result = reader._filter("available=true", reader.data)
        assert len(result) == 2  # phone1 и phone3

    def test_filter_float_comparison(self, mixed_data_csv_file, mock_args):
        """Тест фильтрации с плавающей точкой"""
        reader = CSVReader(mixed_data_csv_file, mock_args)
        reader._get_path()
        with open(mixed_data_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            reader.data = [row for row in reader_csv]

        result = reader._filter("rating>4.1", reader.data)
        assert len(result) == 2  # phone1 и phone3

    def test_aggregate_float_values(self, mixed_data_csv_file, mock_args):
        """Тест агрегации значений с плавающей точкой"""
        reader = CSVReader(mixed_data_csv_file, mock_args)
        reader._get_path()
        with open(mixed_data_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            reader.data = [row for row in reader_csv]

        result = reader._aggregate("rating=avg", reader.data)
        expected_avg = round((4.5 + 4.0 + 4.2) / 3, 2)
        assert result == [[str(expected_avg)]]

    def test_filter_case_sensitive(self, mixed_data_csv_file, mock_args):
        """Тест чувствительности к регистру при фильтрации"""
        reader = CSVReader(mixed_data_csv_file, mock_args)
        reader._get_path()
        with open(mixed_data_csv_file, "r", encoding="utf-8") as file:
            reader_csv = csv.reader(file)
            reader.headers = next(reader_csv)
            reader.data = [row for row in reader_csv]

        result = reader._filter("name=PHONE1", reader.data)
        assert len(result) == 0  # должно быть 0, так как регистр не совпадает

    def test_filter_with_underscore_in_column_name(
            self, mixed_data_csv_file, mock_args):
        """Тест фильтрации с подчеркиванием в названии колонки"""
        # Создаем временный файл с колонкой, содержащей подчеркивание
        with tempfile.NamedTemporaryFile(
                mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['product_name', 'price', 'rating'])
            writer.writerow(['phone1', '100', '4.5'])
            writer.writerow(['phone2', '200', '4.0'])
            temp_file = f.name

        try:
            reader = CSVReader(temp_file, mock_args)
            reader._get_path()
            with open(temp_file, "r", encoding="utf-8") as file:
                reader_csv = csv.reader(file)
                reader.headers = next(reader_csv)
                reader.data = [row for row in reader_csv]

            result = reader._filter("product_name=phone1", reader.data)
            assert len(result) == 1
            assert result[0][0] == "phone1"
        finally:
            os.unlink(temp_file)

    def test_filter_with_numbers_in_column_name(
            self, mixed_data_csv_file, mock_args):
        """Тест фильтрации с цифрами в названии колонки"""
        # Создаем временный файл с колонкой, содержащей цифры
        with tempfile.NamedTemporaryFile(
                mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['product_1', 'price', 'rating'])
            writer.writerow(['phone1', '100', '4.5'])
            writer.writerow(['phone2', '200', '4.0'])
            temp_file = f.name

        try:
            reader = CSVReader(temp_file, mock_args)
            reader._get_path()
            with open(temp_file, "r", encoding="utf-8") as file:
                reader_csv = csv.reader(file)
                reader.headers = next(reader_csv)
                reader.data = [row for row in reader_csv]

            result = reader._filter("product_1=phone1", reader.data)
            assert len(result) == 1
            assert result[0][0] == "phone1"
        finally:
            os.unlink(temp_file)
