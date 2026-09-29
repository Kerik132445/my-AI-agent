import os

import shutil


def list_files(name_dir):
    files = os.listdir(name_dir)
    return f"Список файлов: {files}"


def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def open_file(path):
    os.startfile(path)
    return f"{path} был успешно открыт"


def create_file(path, content):
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
    return f"Файл {path} с содержимым: {content} был успешно создан"


def copy_file(source, destination):
    shutil.copy(source, destination, follow_symlinks=True)
    return f"файл {source} был успешно скопирован в {destination}"


def move_file(source, destination):
    shutil.move(source, destination)
    return f"файл {source} был успешно перемещен в {destination}"


def find_files(name, directory=None):
    results = []
    if not directory:
        for dirpath, dirnames, filenames in os.walk('C:/', topdown=True):
            for filename in filenames:
                if filename == name:
                    full_path = os.path.join(dirpath, filename)
                    results.append(full_path)
    else:
        for dirpath, dirnames, filenames in os.walk(directory, topdown=True):
            for filename in filenames:
                if filename == name:
                    full_path = os.path.join(dirpath, filename)
                    results.append(full_path)
    return results


def delete_file(path):
    os.remove(path)
    return f"Файл {path} был успешно удален"
