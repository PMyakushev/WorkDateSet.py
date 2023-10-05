
import pandas as pd

import json
import os

# Библиотека для работы с СУБД
# from sqlalchemy import engine as sql

# Модуль для работы с отображением вывода Jupyter
from IPython import display

# Создаем списки для столбцов таблицы vacancies
IDs = []  # Список идентификаторов вакансий
names = []  # Список наименований вакансий
descriptions = []  # Список описаний вакансий

# Создаем списки для столбцов таблицы skills
skills_vac = []  # Список идентификаторов вакансий
skills_name = []  # Список названий навыков

# В выводе будем отображать прогресс
# Для этого узнаем общее количество файлов, которые надо обработать
# Счетчик обработанных файлов установим в ноль
cnt_docs = len(os.listdir('C:/Users/ALTAIR/Desktop/ParsingDodo/HH.ru/Ссылки'))
i = 0

# Проходимся по всем файлам в папке vacancies
for fl in os.listdir('C:/Users/ALTAIR/Desktop/ParsingDodo/HH.ru/Обработанные'):

    # Открываем, читаем и закрываем файл
    f = open('C:/Users/ALTAIR/Desktop/ParsingDodo/HH.ru/Обработанные/{}'.format(fl), encoding='utf8')
    jsonText = f.read()
    f.close()
    name = []
    # Текст файла переводим в справочник
    jsonObj = json.loads(jsonText)

    # Заполняем списки для таблиц
    try:
        IDs.append(jsonObj['id'])
    except:
        IDs.append(None)  # Заменяем отсутствующий id на None
    try:
        names.append(jsonObj['name'])
    except KeyError:  # Если ключ 'name' отсутствует, добавляем None
        names.append(None)
    try:
        descriptions.append(jsonObj['description'])
    except KeyError:  # Если ключ 'description' отсутствует, добавляем None
        descriptions.append(None)

    # Т.к. навыки хранятся в виде массива, то проходимся по нему циклом
    for skl in jsonObj.get('key_skills', []):
        skills_vac.append(jsonObj['id'])
        skills_name.append(skl['name'])

    # Увеличиваем счетчик обработанных файлов на 1, очищаем вывод ячейки и выводим прогресс
    i += 1
    display.clear_output(wait=True)
    display.display('Готово {} из {}'.format(i, cnt_docs))

# Создадим соединение с БД
# eng = sql.create_engine('postgresql://{Пользователь}:{Пароль}@{Сервер}:{Port}/{База данных}')
# conn = eng.connect()

# Создаем пандосовский датафрейм, который затем сохраняем в БД в таблицу vacancies
df = pd.DataFrame({'id': IDs, 'name': names, 'description': descriptions})
# df.to_sql('vacancies', conn, schema='public', if_exists='append', index=False)

# Тоже самое, но для таблицы skills
df = pd.DataFrame({'vacancy': skills_vac, 'skill': skills_name})
# df.to_sql('skills', conn, schema='public', if_exists='append', index=False)

# Закрываем соединение с БД
# conn.close()

# Выводим сообщение об окончании программы
display.clear_output(wait=True)
display.display('Вакансии загружены в БД')

df_vacancies = pd.DataFrame({'id': IDs, 'name': names, 'description': descriptions})
df_vacancies.to_csv('vacancies.csv', index=False)

df_skills = pd.DataFrame({'vacancy': skills_vac, 'skill': skills_name})
df_skills.to_csv('skills.csv', index=False)