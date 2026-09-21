import db_connect
from characters import add_character, view_characters, update_character, delete_character, search_character
from terminologies import add_terminology, view_terminologies, update_terminology, delete_terminology, search_terminology
#condensada sakto packs my goat
from locations import add_location, view_locations, update_locations, delete_location, search_location

def locations_menu():
    while True:
        print("\nLOCATIONS...")
        print("[1] Add Location")
        print("[2] View All")
        print("[3] Search Location")
        print("[4] Update Location")
        print("[5] Delete Location")
        print("[6] Back")

        choice = input("Enter choice: ")

        if choice == "1":
            add_location()
        elif choice == "2":
            view_locations()
        elif choice == "3":
            search_location()
        elif choice == "4":
            update_locations()
        elif choice == "5":
            delete_location()
        elif choice == "6":
            break
        else:
            print("Invalid choice knucklechucks.")


def characters_menu():
    while True:
        print("\nCHARACTERS...")
        print("[1] Add Character")
        print("[2] View All")
        print("[3] Search Character")
        print("[4] Update Character")
        print("[5] Delete Character")
        print("[6] Back")

        choice = input("Enter choice: ")

        if choice == "1":
            add_character()
        elif choice == "2":
            view_characters()
        elif choice == "3":
            search_character()
        elif choice == "4":
            update_character()
        elif choice == "5":
            delete_character()
        elif choice == "6":
            break
        else:
            print("Invalid choice knucklechucks.")


def terminologies_menu():
    while True:
        print("\nTERMINOLOGIES...")
        print("[1] Add Terminology")
        print("[2] View All")
        print("[3] Search Terminology")
        print("[4] Update Terminology")
        print("[5] Delete Terminology")
        print("[6] Back")

        choice = input("Enter choice: ")

        if choice == "1":
            add_terminology()
        elif choice == "2":
            view_terminologies()
        elif choice == "3":
            search_terminology()
        elif choice == "4":
            update_terminology()
        elif choice == "5":
            delete_terminology()
        elif choice == "6":
            break
        else:
            print("Invalid choice knucklechucks.")


def menu():
    while True:
        print("\n====================")
        print("Final Fall DB Bible")
        print("--------------------")
        print("[1] Characters")
        print("[2] Terminologies")
        print("[3] Locations")
        print("[4] Exit")
        print("====================")

        choice = input("Enter Choice: ")

        if choice == "1":
            characters_menu()
        elif choice == "2":
            terminologies_menu()
        elif choice == "3":
            locations_menu()
        elif choice == "4":
            print("Exiting... goodbye.")
            break
        else:
            print("Invalid choice knucklechucks.")

    db_connect.db.close()

menu() 