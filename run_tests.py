"""
Скрипт для запуска тестов проекта
"""

import os
import subprocess
import sys
from pathlib import Path


def run_tests():
    """Запускает все тесты с подробным отчетом"""
    
    # Переходим в корневую директорию проекта
    project_root = Path(__file__).parent
    os.chdir(project_root)

    print("Запуск тестов с покрытием кода")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",  # подробный вывод
            "--cov=csv_reader",  # покрытие кода
            "--cov-report=term-missing",  # показывать непокрытые строки
            "--cov-report=html:tests/coverage_html",  # HTML отчет
            "--tb=short"  # короткий traceback
        ], check=False)
        
        if result.returncode == 0:
            print("Все тесты прошли успешно!")
        else:
            print(f"Некоторые тесты не прошли (код выхода: {result.returncode})")
        
        return result.returncode
        
    except Exception as e:
        print(f"Ошибка запуска тестов: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code) 
