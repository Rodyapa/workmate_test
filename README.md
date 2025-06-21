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

## Пример запуска скрипта
```
(venv) motu@motu-HP:~/dev_projects/workmate_test/src$ python3 main.py --file ../tests/test_data/test.csv
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
+==================+=========+=========+==========+
| iphone 15 pro    | apple   |     999 |      4.9 |
+------------------+---------+---------+----------+
| galaxy s23 ultra | samsung |    1199 |      4.8 |
+------------------+---------+---------+----------+
| redmi note 12    | xiaomi  |     199 |      4.6 |
+------------------+---------+---------+----------+
| iphone 14        | apple   |     799 |      4.7 |
+------------------+---------+---------+----------+
| galaxy a54       | samsung |     349 |      4.2 |
+------------------+---------+---------+----------+
| poco x5 pro      | xiaomi  |     299 |      4.4 |
+------------------+---------+---------+----------+
| iphone se        | apple   |     429 |      4.1 |
+------------------+---------+---------+----------+
| galaxy z flip 5  | samsung |     999 |      4.6 |
+------------------+---------+---------+----------+
| redmi 10c        | xiaomi  |     149 |      4.1 |
+------------------+---------+---------+----------+
| iphone 13 mini   | apple   |     599 |      4.5 |
+------------------+---------+---------+----------+
(venv) motu@motu-HP:~/dev_projects/workmate_test/src$ python3 main.py --file ../tests/test_data/test.csv --where "rating>4.7"
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
+==================+=========+=========+==========+
| iphone 15 pro    | apple   |     999 |      4.9 |
+------------------+---------+---------+----------+
| galaxy s23 ultra | samsung |    1199 |      4.8 |
+------------------+---------+---------+----------+
(venv) motu@motu-HP:~/dev_projects/workmate_test/src$ python3 main.py --file ../tests/test_data/test.csv --aggregate "rating=avg"
+--------+
|   name |
+========+
|   4.49 |
+--------+
(venv) motu@motu-HP:~/dev_projects/workmate_test/src$ python3 main.py --f ../tests/test_data/test.csv --where "brand=xiaomi" --aggregate "rating=min"
+--------+
|   name |
+========+
|    4.1 |
+--------+
(venv) motu@motu-HP:~/dev_projects/workmate_test/src$ python3 main.py --f ../tests/test_data/large_test.csv --where "brand=Apple"
+---------------+---------+---------+----------+-----------+-------------+----------------+----------------+
| name          | brand   |   price |   rating |   storage | color       |   release_year | is_available   |
+===============+=========+=========+==========+===========+=============+================+================+
| iPhone 15 Pro | Apple   |     999 |      4.9 |       256 | Space Black |           2023 | true           |
+---------------+---------+---------+----------+-----------+-------------+----------------+----------------+
| iPhone 15     | Apple   |     799 |      4.8 |       128 | Blue        |           2023 | true           |
+---------------+---------+---------+----------+-----------+-------------+----------------+----------------+
| iPhone 14 Pro | Apple   |     899 |      4.7 |       256 | Deep Purple |           2022 | true           |
+---------------+---------+---------+----------+-----------+-------------+----------------+----------------+
| iPhone 14     | Apple   |     699 |      4.6 |       128 | Midnight    |           2022 | true           |
+---------------+---------+---------+----------+-----------+-------------+----------------+----------------+
| iPhone 13 Pro | Apple   |     799 |      4.5 |       256 | Sierra Blue |           2021 | false          |
+---------------+---------+---------+----------+-----------+-------------+----------------+----------------+
| iPhone 13     | Apple   |     599 |      4.4 |       128 | Pink        |           2021 | true           |
+---------------+---------+---------+----------+-----------+-------------+----------------+----------------+
```