BruhMoment = False
while BruhMoment == False:
    print("\nWhat do you want to update?")
    print("[1] Name")
    print("[2] Arcane")
    print("[3] Nationality")
    print("[4] Physical Desc.")
    choice = input("Enter Choice: ")
    if choice not in ["1", "2", "3", "4", "Name", "Arcane", "Nationality", "Physical Desc."]:
        print("Please Input a Valid Choice")
        continue
    else:
        BruhMoment = True