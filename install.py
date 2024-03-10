import subprocess

# Список фреймворков для установки
frameworks = ['aiogram', 'pandas', 'matplotlib','icecream','sqlite3 ','python-dotenv',]  # Пример фреймворков

# Установка фреймворков с помощью pip
for framework in frameworks:
    subprocess.run(['pip', 'install', framework])