import argparse
import json
import os.path
from datetime import date


def add_worker(staff, name, post, year):
    """
    Добавить данные о работнике.
    """
    staff.append({"name": name, "post": post, "year": year})
    return staff


def display_workers(staff):
    """
    Отобразить список работников.
    """
    if staff:
        line = "+-{}-+-{}-+-{}-+-{}-+".format("-" * 4, "-" * 30, "-" * 20, "-" * 8)

        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} | {:^8} |".format(
                "№", "Ф.И.О.", "Должность", "Год"
            )
        )
        print(line)
        for idx, worker in enumerate(staff, 1):
            print(
                "| {:>4} | {:<30} | {:<20} | {:>8} |".format(
                    idx,
                    worker.get("name", ""),
                    worker.get("post", ""),
                    worker.get("year", 0),
                )
            )
            print(line)
    else:
        print("Список работников пуст.")


def select_workers(staff, period):
    """
    Выбрать работников с заданным стажем.
    """
    today = date.today()
    result = []
    for employee in staff:
        if today.year - employee.get("year", today.year) >= period:
            result.append(employee)

    return result


def save_workers(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_workers(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main():
    """
    Главная функция программы.
    """
    parser = argparse.ArgumentParser("workers")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser("add", help="Add a new worker")
    add.add_argument(
        "-f", "--filename", action="store", required=True, help="The data file name"
    )
    add.add_argument(
        "-n", "--name", action="store", required=True, help="The worker's name"
    )
    add.add_argument("-p", "--post", action="store", help="The worker's post")
    add.add_argument(
        "-y",
        "--year",
        action="store",
        type=int,
        required=True,
        help="The year of hiring",
    )

    display = subparsers.add_parser("display", help="Display all workers")
    display.add_argument(
        "-f", "--filename", action="store", required=True, help="The data file name"
    )

    select = subparsers.add_parser("select", help="Select the workers")
    select.add_argument(
        "-f", "--filename", action="store", required=True, help="The data file name"
    )
    select.add_argument(
        "-P",
        "--period",
        action="store",
        type=int,
        required=True,
        help="The required period",
    )
    args = parser.parse_args()

    is_dirty = False
    if os.path.exists(args.filename):
        workers = load_workers(args.filename)
    else:
        workers = []

    if args.command == "add":
        workers = add_worker(workers, args.name, args.post, args.year)
        is_dirty = True
    elif args.command == "display":
        display_workers(workers)
    elif args.command == "select":
        selected = select_workers(workers, args.period)
        display_workers(selected)
    if is_dirty:
        save_workers(args.filename, workers)


if __name__ == "__main__":
    main()
