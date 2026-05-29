# Password Manager
import json
import random
import string

FILE_NAME = "passwords.json"


def load_passwords():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except:
        return {}


def save_passwords(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def generate_password(length=10):
    chars = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(random.choice(chars) for _ in range(length))


passwords = load_passwords()

while True:
    print("\n===== PASSWORD MANAGER =====")
    print("1. Add Password")
    print("2. View Password")
    print("3. Generate Password")
    print("4. Exit")

    choice = input("Choose: ")

    if choice == "1":
        website = input("Website: ")
        username = input("Username: ")
        password = input("Password: ")

        passwords[website] = {
            "username": username,
            "password": password
        }

        save_passwords(passwords)

        print("Password Saved!")

    elif choice == "2":
        website = input("Enter website: ")

        if website in passwords:
            print(passwords[website])
        else:
            print("No data found.")

    elif choice == "3":
        print("Generated Password:", generate_password())

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")