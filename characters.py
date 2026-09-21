from tabulate import tabulate
from db_connect import connect
db = connect()
cursor = db.cursor()

def add_character():
    query = "INSERT INTO characters (name, arcane, nationality, physical_description) VALUES (%s, %s, %s, %s)"

    print("\nAdding a Character...")
    name = input("Their Name?: ")
    arcane = input(f"{name}'s Arcane: ")
    nationality = input(f"{name}'s Nationality: ")
    print(f"\nREMINDER to describe them well: Gender, age, eye color, hair color, height, among other misc details.")
    physical_description = input(f"{name}'s Physical Description: ")

    cursor.execute(query, (name, arcane, nationality, physical_description))
    db.commit()
    print(f"'{name}' has been added!")


def view_characters():
    print("\nCurrent Characters...")

    cursor.execute("SELECT * FROM characters")
    myresult = cursor.fetchall()

    if not myresult:
        print("No characters found.")
        return False
    else:
        headers = ["ID", "Name", "Arcane", "Nationality", "Physical Description"]
        print(tabulate(myresult, headers=headers, tablefmt="grid", maxcolwidths=[5, 15, 15, 20, 40]))
        return True

#def search_characters():
 #   print("\nViewing  Character...")
  #  char_id = input("Enter character ID to searh: ")
   # ok problem

    
def update_character():

    if not view_characters():
        print("\nNo characters to update.")
        return
    
    print("\nUpdating Character...")
    char_id = input("Enter character ID to update: ")

    sooo_valid = ["1", "2", "3", "4", "5", "Name", "Arcane", "Nationality", "Physical Desc.", "Exit"]
    BruhMoment = False
    while BruhMoment == False:
        print("\nWhat do you want to update?")
        print("[1] Name")
        print("[2] Arcane")
        print("[3] Nationality")
        print("[4] Physical Desc.")
        print("[5] Back")
        choice = input("Enter Choice: ")
        if choice == "-67":
            print("HA. HAHA. HAHAHA. IM LOSING MY MIND BRUH.")
            continue
        if choice not in sooo_valid:
            print("Please Input a Valid Choice")
            continue
        if choice in ["5", "Exit"]:
            print("Update cancelled.")
            return
        BruhMoment = True

    what_this = {
        "1": "name", "Name": "name",
        "2": "arcane", "Arcane": "arcane",
        "3": "nationality", "Nationality": "nationality",
        "4": "physical_description", "Physical Desc.": "physical_description"
    }

    field = what_this[choice]
    updoot_val = input(f"Enter new {field}: ")

    query = f"UPDATE characters SET {field} = %s WHERE id = %s"
    cursor.execute(query, (updoot_val, char_id))
    db.commit()

    if cursor.rowcount == 0:
        print("No character found |*_*|")
    else:
        print("Character succefully updated |^ - ^|")

def delete_character():
    if not view_characters():
        print("\nNo characters to delete.")
        return

    print("\nDeleting Character...")
    char_id = input("\nEnter character ID to delete: ")
    checker = input(f"You SURE you want to delete ch.{char_id}? (y/n):")

    if checker.lower() == "n":
        print("Deletetion Canceled.")
        return
    if checker.lower() != "y":
        print("Enter 'y' or 'n' bro it's not that hard istg")
        return

    delete_query = "DELETE FROM characters where id = %s"
    cursor.execute(delete_query, (char_id,))
    db.commit()

    if cursor.rowcount == 0:
        print("There's no character with that ID")
    else:
        print("TO MAKE NOVELS, ONE MUST LEARN TO MURDER THEIR BELOVED")