import json
users= {}
rooms = {}
def save_user(users):
    """Saves the user database to a separate JSON file."""
    with open ('users.json', 'w') as file:
        json.dump(users, file)
    print("User database updated. ")
def load_user():
    """Loads users from users.json on startup."""
    global users
    try:
        with open ('users.json') as file:
            users = json.load(file)
    except FileNotFoundError:
        users= {}
def register_user():
    username= input("Enter your username: ")
    password= input("Enter your password: ")
    confirm_password= input("Confirm your password: ")
    role= input("Enter role (admin/staff): " ).lower()
    if username in users:
        print("Username already exists")
        return False
    else:
        users[username]= {"password":password, "role":role}
        save_user(users)
        print(f"User {username} has been registered")

def login_user():
    global current_role
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in users and users[username]["password"] == password:
        current_role= users[username]["role"]
        print(f"logged in as a {current_role}")
        return True
    else:
        print("Invalid credentials")
        return False
def change_password():
    username=input("Enter your username: ")
    if username not in users:
        print("Username does not exist")
        return False
    new_password= input("Enter your new password: ")
    confirm_password= input("Confirm your new password: ")
    if new_password != confirm_password:
        print("Passwords do not match")
        return False
    else:
        users[username]["password"]= new_password
        save_user(users)
        print(f"Password has been changed")
        return True
class Room:
    def __init__(self, room_number):
        self.number = room_number
        self.is_clean= False
        self.supply_used= []
    def add_supply(self, item):
        self.supply_used.append(item)
        print(f"Added {item} to room {self.number}")
    def room_report(self):
        status= "Clean" if self.is_clean else "Dirty"
        print(f"Room: {self.number} | status: {status}")
        print(f"Supply used: {self.supply_used}")
    def finish_cleaning(self):
        print(f"\n------Finalizing Room {self.number}------")
        for item in self.supply_used:
            use_supply(item)
        self.is_clean= True
        log_entry = f"Room {self.number} was cleaned. Supply used: {self.supply_used}"
        log_action(log_entry)
        print(f"Room {self.number} status update to: Clean")
    def to_dict(self):
        return{
            "number": self.number,
            "is_clean": self.is_clean,
            "supply_used": self.supply_used
        }
storage={
    "soap": 10,
    "body wash": 5,
    "tea": 50,
    "coffee": 0
}
def search_item(item):
    if item in storage:
        print(f"{item}: {storage[item]}")
    else:
        print(f"{item}: Not Found")
def check_low_stock(treshold=5):
    low_item= [item for item, qty in storage.items() if qty <= treshold]
    if low_item:
        for item in low_item:
            print(f"{item}: {storage[item]}")
def save_all_data():
    """
    Converts Rooms object to dictionary and saves the entire system state (Invrntory + Rooms) to database.json
    """
    serialized_rooms = {num: r.to_dict() for num, r in rooms.items()}
    data= {
        "inventory": storage,
        "rooms": serialized_rooms
    }
    with open('database.json', 'w') as file:
        json.dump(data, file)
    print(f"--- All data (Inventory & Rooms) saved! ---")
def load_all_data():
    global storage, rooms
    try:
        with open('database.json', 'r') as file:
            data = json.load(file)
            storage = data["inventory"]
            for num, room_data in data["rooms"].items():
                new_room= Room(num)
                new_room.is_clean= room_data["is_clean"]
                new_room.supply_used= room_data["supply_used"]
                rooms[num] = new_room
        print(f"--- Database loaded Sucessfully  ---")
    except FileNotFoundError:
        print(f"--- Database Not Found  ---")



def use_supply(item):
    if item in storage:
        if storage[item]>0:
            storage[item] -= 1
            print(f"We now have, {storage[item]}")
            return storage[item]
        else:
            print(f"Warning out of order {item}")
            return 0
    else:
        print(f"Error {item} does not exist in invemtory. ")
        return None

def add_new_item(item, quantity):
    if item in storage:
        storage[item] += quantity
        print(f"We now have added {item}, {storage[item]}")
    else:
        storage[item] = quantity
        print(f"We now have added {item}, {storage[item]} in storage")
    return storage[item]
def view_inventory():
    print("-------------Inventory-------------")
    for item in storage:
        print(f"{item}: {storage[item]}")
    print("------------------------------------")
def delete_item(item):
    if item not in storage:
        print(f"We don't have {item}")
    else:
        print(f"We have removed {item}")
        del storage[item]
def log_action(message):
    with open("activity_log.txt", "a") as file:
        file.write(f"{message}\n")
        print(f"Activity loged to history")
def main():
    while True:
        print("------Welcome to Storage-------------")
        print("1. View Inventory")
        print("2. Use Item")
        print("3. Add/Restore Item")
        print("4. Delete Item")
        print("5. Search Item")
        print("6. Check Low Stock")
        print("7. Save all Data")
        print("8. Load Inventory")
        print("9. Room Management")
        print("10. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_inventory()
        elif choice == "2":
            name= input("What Item you used")
            use_supply(name)
        elif choice == "3":
            name= input("Item name: ")
            try:
                qua=int(input("Quantity: "))
                if qua>0:
                    add_new_item(name, qua)
                else:
                    print("Quentity must be in positive integer")
            except ValueError:
                print("Please enter an integer")
        elif choice == "4":
            if current_role == "admin":
                name = input("Item name to delete:")
                delete_item(name)
            else:
                print("ACCESS DENIED: Only Admins can delete items.")
        elif choice == "5":
            name= input("Item name: ")
            search_item(name)
        elif choice == "6":
            check_low_stock()
        elif choice == "7":
            save_all_data()
        elif choice == "8":
            load_all_data()
        elif choice == "9":
            manage_room()
        elif choice == "10":
            print("Thank you!")
            break
        else:
            print("Invalid choice")
def manage_room():
    global rooms
    while True:
        print("------Room Management------------")
        print("1. Create Room")
        print("2. Add supply to the room")
        print("3. View Room")
        print("4. Finish Cleaning room")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            num_input = input("Room number: ")
            if num_input not in rooms:
                rooms[num_input]= Room(num_input)
                print(f"Room {num_input} added in system")
            else:
                print(f"Room {num_input} already added in system")
        elif choice == "2":
            num_input = input("Room name: ")
            if num_input in rooms:
                item= input("Item name: ")
                rooms[num_input].add_supply(item)
            else:
                print(f"Room not found. Please create a new room.")
        elif choice == "3":
            num_input = input("Room name: ")
            if num_input in rooms:
                rooms[num_input].room_report()
            else:
                print("Room not found.")
        elif choice == "4":
            num_input= input("Room name: ")
            if num_input in rooms:
                rooms[num_input].finish_cleaning()
            else:
                print("Room not found.")
        elif choice == "5":
            print("Exiting Room Managment")
            break
        else:
            print("Invalid choice")
if __name__ == "__main__":
    load_all_data()
    load_user()
    while True:
        print("HOUSEKEEPING SECURE LOGIN")
        print("1. Login")
        print("2. Register")
        print("3. Change Password")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            if login_user():
                main()
        elif choice == "2":
            register_user(users)
            save_user()
        elif choice == "3":
            change_password()
            save_user()
        elif choice == "4":
            print("Exiting")
            break
        else:
            print("Invalid choice")


