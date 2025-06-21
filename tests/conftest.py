import sys
from pathlib import Path

import pytest

# Добавляем путь к корневой директории проекта
code_path = Path(__file__).parent.parent
sys.path.insert(0, str(code_path))


# Настройка pytest
def pytest_configure(config):
    """Конфигурация pytest"""
    # Маркеры для категоризации тестов
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "edge_case: mark test as edge case test"
    )


@pytest.fixture(scope="session")
def test_data_dir():
    """Возвращает путь к директории с тестовыми данными"""
    return Path(__file__).parent / "test_data"


@pytest.fixture(scope="session")
def code_dir():
    """Возвращает путь к корневой директории проекта"""
    return Path(__file__).parent.parent
