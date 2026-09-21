from tabulate import tabulate
from db_connect import connect
db = connect()
cursor = db.cursor()

# id name type region stat details

def add_location():
    query = "INSERT INTO locations (name, type, region, stat, details) VALUES (%s, %s, %s, %s, %s)"

    print("\nAdding a Location...")
    name = input("Location Name?: ")
    type = input(f"{name}'s Type: ")
    region = input(f"{name}'s Region: ")
    status = input(f"{name}'s Status: ")
    print(f"\nREMINDER to describe well, especially the story relevant details.")
    details = input(f"{name}'s Physical Details: ")

    cursor.execute(query, (name, type, region, status, details))
    db.commit()
    print(f"'{name}' has been added!")

# id name type region stat details

def view_locations():
    print("\nCurrent locations...")

    cursor.execute("SELECT * FROM locations")
    myresult = cursor.fetchall()

    if not myresult:
        print("No locations found.")
        return False
    else:
        headers = ["ID", "Name", "Type", "Region", "Status", "Details"]
        print(tabulate(myresult, headers=headers, tablefmt="grid", maxcolwidths=[5, 15, 15, 20, 20, 40]))
        return True

# id name type region stat details

def search_location(): #c+v on update_character dawgs
    if not view_locations():
        print("\nNo locations to search.")
        return
    
    print("\nSearching Locations...")
    sooo_valid = ["1", "2", "3", "4", "5", "6", "ID", "Name", "Type", "Region", "Status", "Exit"]
    BruhMoment = False
    while BruhMoment == False:
        print("\nWhat do you want to search up?")
        print("[1] ID")
        print("[2] Name")
        print("[3] Type")
        print("[4] Region")
        print("[5] Status")
        print("[6] Back")
        choice = input("Enter Choice: ")
        if choice == "-21":
            print("What's 9+10?")
            continue
        if choice not in sooo_valid:
            print("Please Input a Valid Choice")
            continue
        if choice in ["6", "Back"]:
            print("Update cancelled.")
            return
        BruhMoment = True

    terms = {
        "1": "id", "ID": "id",
        "2": "name", "Name": "name",
        "3": "type", "Type": "type",
        "4": "region", "Region": "region",
        "5": "stat", "Status": "stat",
    }

    field = terms[choice]
    updoot_val = input(f"Term on '{field}' to search: ")

    #cursor.execute("SELECT * FROM locations")
    #myresult = cursor.fetchall()
    #%{keyword}%

    query = f"SELECT * FROM locations WHERE {field} LIKE %s"
    cursor.execute(query, (f"%{updoot_val}%",))
    myresult = cursor.fetchall()

    if cursor.rowcount == 0:
        print("No matches found |*_*|")
    else:
        headers = ["ID", "Name", "Type", "Region", "Status", "Details"]
        print(tabulate(myresult, headers=headers, tablefmt="grid", maxcolwidths=[5, 15, 15, 20, 20, 40]))

# id name type region stat details

def update_locations():
    if not view_locations():
        print("\nNo locations to update.")
        return
    
    print("\nUpdating Locations...")
    char_id = input("Enter location ID to update: ")

    sooo_valid = ["1", "2", "3", "4", "5", "6", "7" "ID", "Name", "Type", "Region", "Status", "Details", "Exit"]
    BruhMoment = False
    while BruhMoment == False:
        print("\nWhat do you want to update?")
        print("[1] ID")
        print("[2] Name")
        print("[3] Type")
        print("[4] Region")
        print("[5] Status")
        print("[6] Details")
        print("[7] Back")
        choice = input("Enter Choice: ")
        if choice == "-21":
            print("What's 9+10?")
            continue
        if choice not in sooo_valid:
            print("Please Input a Valid Choice")
            continue
        if choice in ["7", "Back"]:
            print("Update cancelled.")
            return
        BruhMoment = True

    terms = {
            "1": "id", "ID": "id",
            "2": "name", "Name": "name",
            "3": "type", "Type": "type",
            "4": "region", "Region": "region",
            "5": "stat", "Status": "stat",
            "6": "details", "Details": "details",
        }

    field = terms[choice]
    updoot_val = input(f"Enter new {field}: ")

    #UPDATE * SET *{} = %s WHERE id = %s
    query = f"UPDATE locations SET {field} = %s WHERE id = %s"
    cursor.execute(query, (updoot_val, char_id))
    db.commit()

    if cursor.rowcount == 0:
        print("No locations found |*_*|")
    else:
        print("Location succefully updated |^ - ^|")

def delete_location():
    if not view_locations():
        print("\nNo locations to delete.")
        return

    print("\nDeleting Location...")
    char_id = input("\nEnter location ID to delete: ")
    checker = input(f"You SURE you want to location ch.{char_id}? (y/n):")

    if checker.lower() == "n":
        print("Deletetion Canceled.")
        return
    if checker.lower() != "y":
        print("Enter 'y' or 'n' bro it's not that hard istg")
        return

    delete_query = "DELETE FROM locations where id = %s"
    cursor.execute(delete_query, (char_id,))
    db.commit()

    if cursor.rowcount == 0:
        print("There's no location with that ID")
    else:
        print("TO MAKE NOVELS, ONE MUST LEARN TO MURDER THEIR BELOVED")