class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecture(self, lecturer, course, grade):
        if (
                isinstance(lecturer, Lecturer) and
                course in self.courses_in_progress and
                course in lecturer.courses_attached and
                1 <= grade <= 10
        ):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def average_grade(self):
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0.0

    def __str__(self):
        avg = self.average_grade()
        courses_in_progress = ', '.join(self.courses_in_progress) or "Нет"
        finished_courses = ', '.join(self.finished_courses) or "Нет"
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {avg}\n"
            f"Курсы в процессе изучения: {courses_in_progress}\n"
            f"Завершенные курсы: {finished_courses}"
        )

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() < other.average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() == other.average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_grade(self):
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0.0

    def __str__(self):
        avg = self.average_grade()
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {avg}"
        )

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() < other.average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() == other.average_grade()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if (
                isinstance(student, Student) and
                course in self.courses_attached and
                course in student.courses_in_progress and
                1 <= grade <= 10
        ):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"



student_1 = Student('Ruoy', 'Eman', 'male')
student_1.courses_in_progress = ['Python', 'Git']
student_1.finished_courses = ['Введение в программирование']

student_2 = Student('Jane', 'Doe', 'female')
student_2.courses_in_progress = ['Python', 'Java']
student_2.finished_courses = ['Основы SQL']

lecturer_1 = Lecturer('Some', 'Buddy')
lecturer_1.courses_attached = ['Python', 'Git']

lecturer_2 = Lecturer('Alice', 'Smith')
lecturer_2.courses_attached = ['Python', 'Java']

reviewer_1 = Reviewer('Ivan', 'Ivanov')
reviewer_1.courses_attached = ['Python', 'Git']

reviewer_2 = Reviewer('Petr', 'Petrov')
reviewer_2.courses_attached = ['Python', 'Java']

reviewer_1.rate_hw(student_1, 'Python', 10)
reviewer_1.rate_hw(student_1, 'Python', 9)
reviewer_1.rate_hw(student_1, 'Git', 8)

reviewer_2.rate_hw(student_2, 'Python', 7)
reviewer_2.rate_hw(student_2, 'Java', 9)

student_1.rate_lecture(lecturer_1, 'Python', 10)
student_1.rate_lecture(lecturer_1, 'Git', 9)

student_2.rate_lecture(lecturer_2, 'Python', 8)
student_2.rate_lecture(lecturer_2, 'Java', 10)

print("\n Проверка ошибок:")
print("  - Студент пытается оценить лектора по курсу, который не учит:",
      student_1.rate_lecture(lecturer_1, 'Java', 5))
print("  - Ревьюер пытается оценить студента по курсу, который не ведёт:",
      reviewer_1.rate_hw(student_1, 'Java', 5))


print("\n Реализуем функции для расчёта средней оценки по курсу.")

def average_grade_for_students(students_list, course_name):
    total_grades = []
    for student in students_list:
        if course_name in student.grades:
            total_grades.extend(student.grades[course_name])
    return round(sum(total_grades) / len(total_grades), 1) if total_grades else 0.0


def average_grade_for_lecturers(lecturers_list, course_name):
    total_grades = []
    for lecturer in lecturers_list:
        if course_name in lecturer.grades:
            total_grades.extend(lecturer.grades[course_name])
    return round(sum(total_grades) / len(total_grades), 1) if total_grades else 0.0


print("\n Результаты расчётов:")

print(f"  - Средняя оценка студентов по 'Python': {average_grade_for_students([student_1, student_2], 'Python')}")
print(f"  - Средняя оценка студентов по 'Java': {average_grade_for_students([student_1, student_2], 'Java')}")
print(f"  - Средняя оценка лекторов по 'Python': {average_grade_for_lecturers([lecturer_1, lecturer_2], 'Python')}")
print(f"  - Средняя оценка лекторов по 'Git': {average_grade_for_lecturers([lecturer_1, lecturer_2], 'Git')}")


print("\n--- __str__ для всех типов объектов ---")
print("Студент 1:")
print(student_1)
print("\nЛектор 1:")
print(lecturer_1)
print("\nРевьюер 1:")
print(reviewer_1)

print("\n--- Сравнение объектов ---")
print(f"student_1 < student_2? → {student_1 < student_2}")
print(f"lecturer_1 > lecturer_2? → {lecturer_1 > lecturer_2}")

student_1.add_courses('Специалист по искусственному интеллекту')
student_2.add_courses('Основы С++')

print("\n Вывод после добавления курсов:")
print("\n Студент 1:")
print(student_1)
print("\n Студент 2:")
print(student_2)
