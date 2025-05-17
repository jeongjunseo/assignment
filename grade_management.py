##################
# 프로그램명: 성적관리 프로그램(grade_management)
# 작성자: 소프트웨어학부/정준서
# 작성일: 2025-04-13
# github : https://github.com/jeongjunseo/-
# 프로그램 설명: 5명의 학생의 성적을 관리(학번, 이름, 영어점수, C-언어 점수, 파이썬 점수를 입력받아 총점, 평균, 학점, 등수  계산)
#DB활용
##################

import sqlite3

class StudentManager:
    def __init__(self):
        self.conn = sqlite3.connect("students.db")
        self.create_table()

    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT,
                english INTEGER,
                c_language INTEGER,
                python INTEGER
            )
        ''')
        self.conn.commit()

    def calculate_total_avg_grade(self, student):
        total = student[2] + student[3] + student[4]
        average = total / 3
        if average >= 90:
            grade = 'A'
        elif average >= 80:
            grade = 'B'
        elif average >= 70:
            grade = 'C'
        elif average >= 60:
            grade = 'D'
        else:
            grade = 'F'
        return total, average, grade

    def input_students(self):
        for _ in range(5):
            student_id = input("학번: ")
            name = input("이름: ")
            english = int(input("영어 점수: "))
            c_lang = int(input("C언어 점수: "))
            python = int(input("파이썬 점수: "))
            self.conn.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?)", 
                              (student_id, name, english, c_lang, python))
        self.conn.commit()

    def fetch_all_students(self):
        return self.conn.execute("SELECT * FROM students").fetchall()

    def display_students(self):
        print("\n[전체 학생 정보 출력]")
        students = self.fetch_all_students()
        ranked_students = sorted(students, key=lambda x: sum(x[2:]), reverse=True)
        for rank, s in enumerate(ranked_students, start=1):
            total, avg, grade = self.calculate_total_avg_grade(s)
            print(f"{s[0]} {s[1]} 총점:{total} 평균:{avg:.2f} 학점:{grade} 등수:{rank}")

    def insert_student(self):
        student_id = input("학번: ")
        name = input("이름: ")
        english = int(input("영어 점수: "))
        c_lang = int(input("C언어 점수: "))
        python = int(input("파이썬 점수: "))
        self.conn.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?)", 
                          (student_id, name, english, c_lang, python))
        self.conn.commit()

    def delete_student(self, student_id):
        self.conn.execute("DELETE FROM students WHERE student_id=?", (student_id,))
        self.conn.commit()

    def search_student(self, keyword):
        print(f"\n[검색결과: '{keyword}']")
        students = self.conn.execute(
            "SELECT * FROM students WHERE student_id=? OR name=?", 
            (keyword, keyword)).fetchall()
        ranked_students = sorted(self.fetch_all_students(), key=lambda x: sum(x[2:]), reverse=True)
        for s in students:
            total, avg, grade = self.calculate_total_avg_grade(s)
            rank = next((i+1 for i, st in enumerate(ranked_students) if st[0] == s[0]), None)
            print(f"{s[0]} {s[1]} 총점:{total} 평균:{avg:.2f} 학점:{grade} 등수:{rank}")

    def sort_by_total(self):
        print("\n[총점으로 정렬됨]")
        self.display_students()

    def count_above_80(self):
        students = self.fetch_all_students()
        count = sum(1 for s in students if (s[2] + s[3] + s[4]) / 3 >= 80)
        print(f"\n평균 80점 이상 학생 수: {count}")

    def close(self):
        self.conn.close()

def main():
    manager = StudentManager()
    manager.input_students()

    while True:
        print("\n--- 메뉴 ---")
        print("1. 전체 출력\n2. 학생 추가\n3. 학생 삭제\n4. 학생 검색\n5. 총점 정렬\n6. 80점 이상 학생 수\n0. 종료")
        choice = input("선택: ")

        if choice == '1':
            manager.display_students()
        elif choice == '2':
            manager.insert_student()
        elif choice == '3':
            sid = input("삭제할 학번: ")
            manager.delete_student(sid)
        elif choice == '4':
            keyword = input("학번 또는 이름: ")
            manager.search_student(keyword)
        elif choice == '5':
            manager.sort_by_total()
        elif choice == '6':
            manager.count_above_80()
        elif choice == '0':
            manager.close()
            break
        else:
            print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()