# workmate_test
## Установка зависимостей
```bash
pip install requirements.txt
```

## Запуск скрипта c тестовыми данными из тз.
```bash
python3 main.py --f tests/test_data/test.csv --where "brand=xiaomi" --agregate "rating=min"
```

## Запуск всех тестов
```bash
python run_tests.py
```