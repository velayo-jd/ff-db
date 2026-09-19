import db_connect
from characters import add_character, view_characters, update_character, delete_character
from terminologies import add_terminology, view_terminologies, update_terminology, delete_terminology
#condensada sakto packs my goat

def characters_menu():
    while True:
        print("\nCHARACTERS...")
        print("[1] Add Character")
        print("[2] View All")
        print("[3] Update Character")
        print("[4] Delete Character")
        print("[5] Back")

        choice = input("Enter choice: ")

        if choice == "1":
            add_character()
        elif choice == "2":
            view_characters()
        elif choice == "3":
            update_character()
        elif choice == "4":
            delete_character()
        elif choice == "5":
            break
        else:
            print("Invalid choice knucklechucks.")


def terminologies_menu():
    while True:
        print("\nTERMINOLOGIES...")
        print("[1] Add Terminology")
        print("[2] View All")
        print("[3] Update Terminology")
        print("[4] Delete Terminology")
        print("[5] Back")

        choice = input("Enter choice: ")

        if choice == "1":
            add_terminology()
        elif choice == "2":
            view_terminologies()
        elif choice == "3":
            update_terminology()
        elif choice == "4":
            delete_terminology()
        elif choice == "5":
            break
        else:
            print("Invalid choice knucklechucks.")


def menu():
    while True:
        print("\n==================")
        print("Final Fall DB Bible")
        print("-------------------")
        print("[1] Characters")
        print("[2] Terminologies")
        print("[3] Exit")
        print("===================")

        choice = input("Enter Choice: ")

        if choice == "1":
            characters_menu()
        elif choice == "2":
            terminologies_menu()
        elif choice == "3":
            print("Exiting... goodbye.")
            break
        else:
            print("Invalid choice knucklechucks.")

    db_connect.db.close()

menu() 