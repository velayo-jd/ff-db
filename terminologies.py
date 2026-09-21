from tabulate import tabulate
from db_connect import connect
db = connect()
cursor = db.cursor()

def add_terminology():
    query = "INSERT INTO terminologies (term, term_type, term_definition) VALUES (%s, %s, %s)"

    print("\nAdding a Terminology...")
    term = input("The term?: ")
    term_type = input(f"What type of term is '{term}'?: ")
    print(f"\nREMINDER to define it well; like 5Ws 1H.")
    term_definition = input(f"{term}'s Definition: ")

    cursor.execute(query, (term, term_type, term_definition))
    db.commit()
    print(f"'{term}' has been added!")


def view_terminologies():
    print("\nCurrent Terminologies...")

    cursor.execute("SELECT * FROM terminologies")
    myresult = cursor.fetchall()

    if not myresult:
        print("No terminology found.")
        return False
    else:
        headers = ["ID", "Term", "Term Type", "Term Definition"]
        print(tabulate(myresult, headers=headers, tablefmt="grid", maxcolwidths=[5, 15, 15, 20, 40]))
        return True

def search_terminology(): #c+v on update_character dawgs
    if not view_terminologies():
        print("\nNo terminologies to search.")
        return
    
    print("\nSearching Terminology...")
    sooo_valid = ["1", "2", "3", "4", "5", "ID", "Term", "Term Type", "Exit"]
    BruhMoment = False
    while BruhMoment == False:
        print("\nWhat do you want to search up?")
        print("[1] ID")
        print("[2] Term")
        print("[3] Term Type")
        print("[4] Back")
        choice = input("Enter Choice: ")
        if choice == "-67":
            print("HA. HAHA. HAHAHA. IM LOSING MY MIND BRUH.")
            continue
        if choice not in sooo_valid:
            print("Please Input a Valid Choice")
            continue
        if choice in ["4", "Back"]:
            print("Update cancelled.")
            return
        BruhMoment = True

    terms = {
        "1": "id", "ID": "id", "Id": "id", "id": "id",
        "2": "term", "Term": "term",
        "3": "term_type", "Term Type": "term_type",
    }

    field = terms[choice]
    updoot_val = input(f"Term on '{field}' to search: ")

    #cursor.execute("SELECT * FROM characters")
    #myresult = cursor.fetchall()
    #%{keyword}%

    query = f"SELECT * FROM terminologies WHERE {field} LIKE %s"
    cursor.execute(query, (f"%{updoot_val}%",))
    myresult = cursor.fetchall()

    if cursor.rowcount == 0:
        print("No matches found |*_*|")
    else:
        headers = ["ID", "Term", "Term Type", "Term Definiton"]
        print(tabulate(myresult, headers=headers, tablefmt="grid", maxcolwidths=[5, 15, 15, 20, 40]))

def update_terminology():
    if not view_terminologies():
        print("\nNo characters to update.")
        return
    
    print("\nUpdating Terminology...")
    char_id = input("Enter terminology ID to update: ")

    sooo_valid = ["1", "2", "3", "4", "Term", "Term Type", "Term Definition", "Exit"]
    BruhMoment = False
    while BruhMoment == False:
        print("\nWhat do you want to update?")
        print("[1] Term")
        print("[2] Term Type")
        print("[3] Term Definition")
        print("[4] Exit")
        choice = input("Enter Choice: ")
        if choice == "-69":
            print("I was legally advised to not make any further joke on this easter egg.")
            continue
        if choice not in sooo_valid:
            print("Please Input a Valid Choice")
            continue
        if choice in ["5", "Exit"]:
            print("Update cancelled.")
            return
        BruhMoment = True

    what_this = {
        "1": "term", "Term": "term",
        "2": "term_type", "Term Type": "term_type",
        "3": "term_definition", "Term Definition": "term_definition",
    }

    field = what_this[choice]
    updoot_val = input(f"Enter new {field}: ")
    #UPDATE * SET *{} = %s WHERE id = %s
    query = f"UPDATE terminologies SET {field} = %s WHERE id = %s"
    cursor.execute(query, (updoot_val, char_id))
    db.commit()

    if cursor.rowcount == 0:
        print("No terminology found |*_*|")
    else:
        print("Terminoly succefully updated |^ - ^|")

def delete_terminology():
    if not view_terminologies():
        print("\nNo terminology to delete.")
        return

    print("\nDeleting Terminology...")
    char_id = input("\nEnter terminology ID to delete: ")
    checker = input(f"You SURE you want to delete term {char_id}? (y/n):")

    if checker.lower() == "n":
        print("Deletetion Canceled.")
        return
    if checker.lower() != "y":
        print("Enter 'y' or 'n' bro it's not that hard istg")
        return

    delete_query = "DELETE FROM terminologies where id = %s"
    cursor.execute(delete_query, (char_id,))
    db.commit()

    if cursor.rowcount == 0:
        print("There's no terminology with that ID")
    else:
        print("TO MAKE NOVELS, ONE MUST LEARN TO MURDER THEIR BELOVED")