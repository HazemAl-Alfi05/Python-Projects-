# Smart GPA Calculator

def grade_to_gpa(grade):
    if grade >= 90:
        return 4.0
    elif grade >= 80:
        return 3.0
    elif grade >= 70:
        return 2.0
    elif grade >= 60:
        return 1.0
    else:
        return 0.0


subjects = int(input("How many subjects? "))

total_gpa = 0

for i in range(subjects):
    print(f"\nSubject {i+1}")

    name = input("Enter subject name: ")
    grade = float(input("Enter grade: "))

    gpa = grade_to_gpa(grade)

    print(f"{name} GPA: {gpa}")

    total_gpa += gpa

final_gpa = total_gpa / subjects

print("\n========== RESULT ==========")
print(f"Final GPA: {round(final_gpa, 2)}")

if final_gpa >= 2:
    print("Status: PASS")
else:
    print("Status: FAIL")