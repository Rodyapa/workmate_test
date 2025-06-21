import pytest
import subprocess
import tempfile
import csv
import os
import sys
from pathlib import Path

# Добавляем путь к папке src
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestMainIntegration:
    """Интеграционные тесты для главного скрипта"""
    
    @pytest.fixture
    def sample_csv_file(self):
        """Возвращает путь к существующему CSV файлу с тестовыми данными"""
        return str(Path(__file__).parent / "test_data" / "test.csv")
    
    def test_main_basic_reading(self, sample_csv_file):
        """Тест базового чтения CSV файла через main.py"""
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "src" / "main.py"),
            "-f", sample_csv_file
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert "name" in result.stdout
        assert "price" in result.stdout
        assert "iphone 15 pro" in result.stdout
        assert "galaxy s23 ultra" in result.stdout
    
    def test_main_with_filter(self, sample_csv_file):
        """Тест фильтрации через main.py"""
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "src" / "main.py"),
            "-f", sample_csv_file,
            "-w", "brand=apple"
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert "iphone 15 pro" in result.stdout
        assert "apple" in result.stdout
        # Проверяем, что другие бренды не попали в результат
        assert "samsung" not in result.stdout
        assert "xiaomi" not in result.stdout
    
    def test_main_with_aggregate(self, sample_csv_file):
        """Тест агрегации через main.py"""
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "src" / "main.py"),
            "-f", sample_csv_file,
            "-a", "price=min"
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert "149" in result.stdout  # минимальная цена
    
    def test_main_with_filter_and_aggregate(self, sample_csv_file):
        """Тест комбинации фильтрации и агрегации"""
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "src" / "main.py"),
            "-f", sample_csv_file,
            "-w", "price>500",
            "-a", "price=avg"
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        # Должна быть средняя цена только для дорогих телефонов (>500)
        expected_avg = "919"
        assert expected_avg in result.stdout
    
    def test_main_file_not_found(self):
        """Тест обработки несуществующего файла"""
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "src" / "main.py"),
            "-f", "nonexistent_file.csv"
        ], capture_output=True, text=True)
        
        assert result.returncode == 1
        assert "не найден" in result.stderr or "не найден" in result.stdout
    
    def test_main_missing_required_argument(self):
        """Тест отсутствия обязательного аргумента"""
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "src" / "main.py")
        ], capture_output=True, text=True)
        
        assert result.returncode != 0
        assert "error" in result.stderr.lower()
    
    def test_main_help(self):
        """Тест справки"""
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "src" / "main.py"),
            "--help"
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert "Считыватель CSV файлов" in result.stdout
        assert "-f" in result.stdout
        assert "--file" in result.stdout
        assert "--where" in result.stdout
        assert "--aggregate" in result.stdout
    
    def test_main_invalid_filter_expression(self, sample_csv_file):
        """Тест невалидного выражения фильтрации"""
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "src" / "main.py"),
            "-f", sample_csv_file,
            "-w", "invalid_expression"
        ], capture_output=True, text=True)
        
        assert result.returncode == 1
        assert "формате" in result.stderr or "формате" in result.stdout
    
    def test_main_invalid_aggregate_expression(self, sample_csv_file):
        """Тест невалидного выражения агрегации"""
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "src" / "main.py"),
            "-f", sample_csv_file,
            "-a", "invalid_expression"
        ], capture_output=True, text=True)
        
        assert result.returncode == 1
        assert "формате" in result.stderr or "формате" in result.stdout
    
    def test_main_column_not_found_in_filter(self, sample_csv_file):
        """Тест несуществующей колонки в фильтрации"""
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "src" / "main.py"),
            "-f", sample_csv_file,
            "-w", "nonexistent_column>100"
        ], capture_output=True, text=True)
        
        assert result.returncode == 1
        assert "не найдена" in result.stderr or "не найдена" in result.stdout
    
    def test_main_column_not_found_in_aggregate(self, sample_csv_file):
        """Тест несуществующей колонки в агрегации"""
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "src" / "main.py"),     
            "-f", sample_csv_file,
            "-a", "nonexistent_column=min"
        ], capture_output=True, text=True)
        
        assert result.returncode == 1
        assert "не найдена" in result.stderr or "не найдена" in result.stdout
    
    def test_main_string_aggregation_error(self, sample_csv_file):
        """Тест ошибки при агрегации строковой колонки"""
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent / "src" / "main.py"),
            "-f", sample_csv_file,
            "-a", "name=min"
        ], capture_output=True, text=True)
        
        assert result.returncode == 1
        assert "только для чисел" in result.stderr or "только для чисел" in result.stdout
