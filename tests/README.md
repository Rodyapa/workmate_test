# Тестирование CSV Reader
## Структура тестов
```
tests/
├── conftest.py                 # Конфигурация pytest
├── test_csv_reader.py         # Unit тесты для класса CSVReader
├── test_main_integration.py   # Интеграционные тесты для main.py
├── test_edge_cases.py         # Тесты граничных случаев
├── requirements-test.txt      # Зависимости для тестирования
└── README.md                  # Этот файл
```

## Запуск тестов

### Установка зависимостей
```bash
pip install -r tests/requirements-test.txt
```

### Запуск всех тестов
```bash
python run_tests.py
```