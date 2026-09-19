from tabulate import tabulate
from db_connect import connect
db = connect()
cursor = db.cursor()

def add_terminology():
    sql = "INSERT INTO terminologies (term, term_type, term_definition) VALUES (%s, %s, %s)"

    print("\nAdding a Terminology...")
    term = input("\nThe term?: ")
    term_type = input(f"What type of term is '{term}'?: ")
    print(f"\nREMINDER to define it well; like 5Ws 1H.")
    term_definition = input(f"{term}'s Definition: ")

    cursor.execute(sql, (term, term_type, term_definition))
    db.commit()
    print(f"'{term}' has been added!")


def view_terminologies():
    print("\nCurrent Terminologies...")

    cursor.execute("SELECT term, term_type, term_definition FROM terminologies")
    rows = cursor.fetchall()

    if not rows:
        print("No terminology found.")
        return False
    else:
        headers = ["ID", "Term", "Term Type", "Term Definition"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        return True


def update_terminology():
    if not view_terminologies():
        print("\nNo characters to update.")
        return
    
    print("\nUpdating Terminology...")
    char_id = input("\nEnter terminology ID to update: ")

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

    field_map = {
        "1": "term", "Term": "term",
        "2": "term type", "Term Type": "term type",
        "3": "term definition", "Term Definition": "term definition",
    }

    field = field_map[choice]
    updoot_val = input(f"Enter new {field}: ")

    sql = f"UPDATE terminologies SET {field} = %s WHERE id = %s"
    cursor.execute(sql, (updoot_val, char_id))
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