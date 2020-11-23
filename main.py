# -*- coding: utf-8 -*-
"""
Программа, сортирующая файлы по заданным настройкам.

Модуль может из входной директории рассортировать файлы с нужными названиями и
расширениями в выходную директорию, создав там отдельные директории под каждое
название и поддиректории, если включена ассоциативная сортировка

===============================================================================

TODO: разработать GUI
"""

import os
import shutil
import configparser
import logging

# ================================Блок настроек================================

# Инициализация парсера файла настроек
config = configparser.ConfigParser()
config.read('setting.ini', encoding='UTF-8')

# Определение рабочих директорий и проверка их существования
MOVE_FROM = config['MainSetting']['move_from']
MOVE_TO = config['MainSetting']['move_to']

# Признаки файлов, с которыми нужно работать
NAME_FRAGMENTS = \
    config['MainSetting']['name_fragment'].replace(' ', '').split(',')
FILE_EXTENSIONS = \
    config['MainSetting']['extensions'].replace(' ', '').split(',')

# Ассоциативная сортировка
IS_ASSOCIATION = bool(int(config['Customize']['associative']))

# Логирование
IS_LOGGING = bool(int(config['Customize']['logging']))

# Настройка логирование, если оно включено
if IS_LOGGING:
    logging.basicConfig(
        filename='FileManager.log',
        filemode='w',
        format='[%(asctime)s - {%(levelname)s}] - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
        level=logging.DEBUG)

# ================================Блок проверок================================


def check_path(directory: str, error: str) -> None:
    """
    Функция проверки директории на корректность.

    Если указанная директория не существует, то при включенном логгировании
    записывается ошибка в лог-файл и вызывается искюлчение.

    :param directory: (str) директория для проверки
    :param error: (str) - текст для ошибки
    :return: None
    """
    if not os.path.exists(directory) and IS_LOGGING:
        logging.error('Несуществующая {0} директория: {1}'.format(
            error,
            directory
        ))
        # Хороший тон - формирование своих исключений
        raise Exception('Несуществующая {0} директория: {1}'.format(
            error,
            directory
        ))


# Проверка каждой директории:
check_path(MOVE_FROM, 'входная')
check_path(MOVE_TO, 'выходная')

# =============Блок объявления рабочих констант, переменных и т.п.=============

# TODO: добавить кастомизацию ассоциаций
# Названия папок
IMAGE = 'Image'
AUDIO = 'Audio'
VIDEO = 'Video'
TEXT = 'Text'
DOC = 'Documentation'
OTHER = 'Other'

# Список папок
FOLDERS = [IMAGE, AUDIO, VIDEO, TEXT, DOC]

# Списки расширений, взято остюда:
# https://developer.mozilla.org/ru/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
image_ext = ['.bmp', '.gif', '.jpeg', '.jpg', '.png', '.svg', '.tif', '.tiff',
             '.webp', '.emf']
audio_ext = ['.aac', '.mp3', '.oga', '.wav', '.weba']
video_ext = ['.avi', '.mpeg', '.mp4', '.ogv', '.webm', '.3gp', '.3g2']
text_ext = ['.txt']
doc_ext = ['.doc', '.docx', '.pdf', '.djvu']

# Список типов расширений:
EXTENSIONS: list = [image_ext, audio_ext, video_ext, text_ext, doc_ext]

# Словарь ассоциаций
association: dict = dict()

# Создание словаря ассоциаций
for index in range(len(FOLDERS)):
    association.update(dict.fromkeys(EXTENSIONS[index], FOLDERS[index]))

# ============================Основной рабочий блок============================

# Создание папок в указаной директории
for name_fragment in NAME_FRAGMENTS:
    dir_name = MOVE_TO + '\\' + name_fragment
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        if IS_LOGGING:
            logging.info('Создана директория {0}'.format(dir_name))
    else:
        if IS_LOGGING:
            logging.info('Директория {0} уже существует!'.format(dir_name))

    # Для каждой ассоциации нужно создать свою папка
    for folder_name in FOLDERS:
        folder = dir_name + "\\" + folder_name
        if not os.path.exists(folder):
            os.mkdir(folder)
            if IS_LOGGING:
                logging.info('Создана директория {0}'.format(folder))
        else:
            if IS_LOGGING:
                logging.info('Директория {0} уже существует!'.format(folder))

    # TODO: нужно подумать над созданием данной папки
    # Отдельно создание папки Other
    folder = dir_name + "\\" + OTHER
    if not os.path.exists(folder):
        os.mkdir(folder)
        logging.info('Создана директория {0}'.format(folder))
    else:
        logging.info('Директория {0} уже существует!'.format(folder))

# Поиск и перемещение подходящих файлов
for item in os.listdir(MOVE_FROM):
    if os.path.isfile(os.path.join(MOVE_FROM, item)):
        filename, file_extension = os.path.splitext(item)

        # Поиск первого подходящего файла по фрагменту имени
        for name_fragment in NAME_FRAGMENTS:
            if filename.find(name_fragment) != -1:
                shutil.move(
                    MOVE_FROM + '\\' + item,
                    MOVE_TO + '\\' + name_fragment + '\\' +
                    association.get(file_extension, OTHER)
                )
                if IS_LOGGING:
                    logging.info('Перемещение файла {0}'.format(item))
