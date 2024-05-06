import argparse
import json
from datetime import date


def add_student(students, full_name, group_number, grades):
    """
    Добавить данные о студенте.
    """
    grades = [float(grade) for grade in grades.split()]
    student = {
        'full_name': full_name,
        'group_number': group_number,
        'grades': grades,
    }
    students.append(student)
    students.sort(key=lambda item: item.get('group_number', ''))


def list_students(students):
    """
    Вывести список студентов.
    """
    line = '+-{}-+-{}-+-{}-+'.format('-' * 30, '-' * 15, '-' * 20)
    print(line)
    print('| {:^30} | {:^15} | {:^20} |'.format("Ф.И.О.", "Номер группы", "Успеваемость"))
    print(line)
    for student in students:
        average_grade = sum(student.get('grades', 0)) / len(student.get('grades', 1))
        if average_grade > 4.0:
            print('| {:<30} | {:<15} | {:<20} |'.format(student.get('full_name', ''), student.get('group_number', ''),
                                                        ', '.join(map(str, student.get('grades', [])))))
    print(line)


def save_to_json(filepath, data):
    """
    Сохранить всех студентов в файл JSON.
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_from_json(filepath):
    """
    Загрузить всех студентов из файла JSON.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)


def validate_data(data):
    """
    Проверить валидность данных JSON.
    """
    # Ваш код валидации данных с использованием JSON Schema


def main():
    parser = argparse.ArgumentParser("students")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser("add", help="Add a new student")
    add.add_argument("-f", "--filename", action="store", required=True, help="The data file name")
    add.add_argument("-n", "--name", action="store", required=True, help="The student's full name")
    add.add_argument("-g", "--group", action="store", required=True, help="The student's group number")
    add.add_argument("-r", "--grades", action="store", required=True, help="The student's grades")

    display = subparsers.add_parser("display", help="Display all students")
    display.add_argument("-f", "--filename", action="store", required=True, help="The data file name")

    args = parser.parse_args()

    if args.command == "add":
        students = load_from_json(args.filename)
        add_student(students, args.name, args.group, args.grades)
        save_to_json(args.filename, students)
    elif args.command == "display":
        students = load_from_json(args.filename)
        list_students(students)


if __name__ == "__main__":
    main()
