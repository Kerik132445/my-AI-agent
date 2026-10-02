import os
import shutil

WORKING_DIRECTORY = r"C:\AI Gven"


home = os.path.expanduser("~")

SPECIAL_DIRECTORIES = {
    "рабочий стол": os.path.join(home, "Desktop"),
    "desktop": os.path.join(home, "Desktop"),

    "загрузки": os.path.join(home, "Downloads"),
    "downloads": os.path.join(home, "Downloads"),

    "документы": os.path.join(home, "Documents"),
    "documents": os.path.join(home, "Documents"),
}


def resolve_path(path):
    if os.path.isabs(path):
        return path

    for name, directory in SPECIAL_DIRECTORIES.items():
        path_lower = path.lower()
        if path_lower.startswith(name):
            lstrip = os.path.join(directory, path[len(name):].lstrip("/\\"))
            return lstrip

    return os.path.join(WORKING_DIRECTORY, path)


def list_files(name_dir):
    name_dir = resolve_path(name_dir)

    files = os.listdir(name_dir)
    return f"Список файлов: {files}"


def read_file(path):
    path = resolve_path(path)

    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def open_file(path):
    path = resolve_path(path)
    os.startfile(path)
    return f"{path} был успешно открыт"


def create_file(path, content):
    path = resolve_path(path)

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
    return f"Файл {path} с содержимым: {content} был успешно создан"


def copy_file(source, destination):
    source = resolve_path(source)
    destination = resolve_path(destination)

    shutil.copy(source, destination, follow_symlinks=True)
    return f"файл {source} был успешно скопирован в {destination}"


def move_file(source, destination):
    source = resolve_path(source)
    destination = resolve_path(destination)

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
        directory = resolve_path(directory)
        for dirpath, dirnames, filenames in os.walk(directory, topdown=True):
            for filename in filenames:
                if filename == name:
                    full_path = os.path.join(dirpath, filename)
                    results.append(full_path)
    return results


def delete_file(path):
    path = resolve_path(path)

    os.remove(path)
    return f"Файл {path} был успешно удален"


def create_folder(path, exist_ok=True):
    path = resolve_path(path)

    os.makedirs(path, exist_ok=exist_ok)
    return f"Папка {path} была создана"


def delete_folder(path):
    path = resolve_path(path)

    shutil.rmtree(path)
    return f"Папка {path} успешно удалена"
