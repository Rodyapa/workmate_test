# workmate_test
## Установка зависимостей
```bash
pip install -r requirements.txt
```

## Запуск скрипта c тестовыми данными из тз.
```bash
cd src
python3 main.py --file ../tests/test_data/test.csv
python3 main.py --file ../tests/test_data/test.csv --where "rating>4.7"
python3 main.py --file ../tests/test_data/test.csv --aggregate "rating=avg"
python3 main.py --f ../tests/test_data/test.csv --where "brand=xiaomi" --aggregate "rating=min"
```

## Запуск скрипта с большим тестовым файлом csv
```bash
cd src
python3 main.py --f ../tests/test_data/large_test.csv --where "brand=Apple"
```

## Запуск всех тестов
```bash
# Из корня проекта
python3 run_tests.py
```