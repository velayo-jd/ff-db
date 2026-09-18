from db_connect import connect
db = connect()
cursor = db.cursor()

def add_character():
    sql = "INSERT INTO characters (name, arcane, nationality, physical_description) VALUES (%s, %s, %s, %s)"

    print("\nAdding a Character...")
    name = input("Their Name?: ")
    arcane = input(f"{name}'s Arcane: ")
    nationality = input(f"{name}'s Nationality Desciption: ")
    print(f"\nREMINDER to describe them well: Gender, age, eye color, hair color, height, among other misc details.")
    physical_description = input(f"{name}'s Physical Desciption: ")

    cursor.execute(sql, (name, arcane, nationality, physical_description))
    db.commit()
    print(f"'{name}' has been added!")
    db.close

db.close()