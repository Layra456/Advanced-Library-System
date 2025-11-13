import json
import time
import pwinput

# ================== Load & Save Functions ==================


def load_function():
    try:
        with open("library_user.JSON", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []
    try:
        with open("library_books.JSON", "r") as f:
            books = json.load(f)
    except FileNotFoundError:
        books = []
    return users, books


def save_function(users, books):
    with open("library_user.JSON", "w") as f:
        json.dump(users, f, indent=4)
    with open("library_books.JSON", "w") as f:
        json.dump(books, f, indent=4)

# ================== Find User ==================


def find_user(users, pin, card_number, username):
    for user in users:
        if pin == user["pin"] and card_number == user["card_number"] and username == user["username"]:
            return user
    return None

# ================== Show Books ==================


def show_books(books):
    if not books:
        print("📚 There are no books available yet.")
        return
    print("📚 Available Books:")
    for idx, book in enumerate(books, start=1):
        status = "✅ Available" if book["available"] else "❌ Borrowed"
        print(
            f"{idx}. {book['title']} - {book['author']} - {book['time']} | {status}")

# ================== Borrow Book ==================


def borrow_book(user, books):
    show_books(books)
    choice = input(
        "📖 Enter the number of the book you want to borrow: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(books):
        print("❌ Invalid choice!")
        return

    book = books[int(choice)-1]
    if not book["available"]:
        print(f"❌ The book '{book['title']}' is already borrowed.")
        return

    book["available"] = False
    user["transactions"].append({
        "type": "Borrowed",
        "book": book["title"],
        "time": time.ctime()
    })
    print(f"✅ You successfully borrowed '{book['title']}' from the library!")

# ================== Return Book ==================


def return_book(user, books):
    borrowed_books = [t for t in user["transactions"]
                      if t["type"] == "Borrowed"]

    if not borrowed_books:
        print("📖 You have no borrowed books to return.")
        return

    print("📖 Books you have borrowed:")
    for idx, t in enumerate(borrowed_books, start=1):
        print(f"{idx}. {t['book']} | Borrowed on {t['time']}")

    choice = input(
        "📌 Enter the number of the book you want to return: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(borrowed_books):
        print("❌ Invalid choice!")
        return

    book_name = borrowed_books[int(choice)-1]['book']

    for book in books:
        if book_name == book['title']:
            book["available"] = True

    user["transactions"].append({
        "type": "Returned",
        "book": book_name,
        "time": time.ctime()
    })
    print(f"✅ You successfully returned '{book_name}' to the library!")

# ================== Change PIN ==================


def change_pin(user):
    old_pin = pwinput.pwinput("🔒 Enter your current PIN: ", mask="*").strip()
    if old_pin != user["pin"]:
        print("❌ PIN does not match!")
        return

    new_pin = pwinput.pwinput(
        "🔑 Enter your new 4-digit PIN: ", mask="*").strip()
    if len(new_pin) == 4 and new_pin.isdigit():
        user["pin"] = new_pin
        print("✅ Your PIN has been successfully changed!")
    else:
        print("❌ Invalid PIN format! Must be exactly 4 digits.")

# ================== View Transactions ==================


def view_transactions(user, books):
    if not user["transactions"]:
        print("📜 You have no transactions yet.")
        return

    print("📜 Transaction History:")
    for t in user["transactions"]:
        # Find the current book to check its availability
        book_obj = next((b for b in books if b["title"] == t["book"]), None)
        if book_obj:
            status = "✅ Available" if book_obj["available"] else "❌ Borrowed"
        else:
            status = "❓ Unknown"
        print(
            f"➡️ {t['type']} | 📖 {t['book']} | 🕒 {t['time']} | Status: {status}")

# ================== Library System ==================


def library_system():
    while True:
        users, books = load_function()
        print("\n===== 📚 Welcome to Python Library System 📚 =====")
        print("1. Login")
        print("2. Create Account")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            username = input("👤 Enter your username: ").strip().lower()
            pin = pwinput.pwinput("🔒 Enter your PIN: ", mask="*").strip()
            card_number = input("💳 Enter your card number: ").strip()

            user = find_user(users, pin, card_number, username)
            if not user:
                print("❌ Invalid login credentials!")
                continue

            print(f"👋 Welcome back, {user['username'].title()}!")

        elif choice == "2":
            username = input("👤 Choose a username: ").strip()
            if any(u["username"] == username for u in users):
                print("❌ Username already exists!")
                continue
            pin = pwinput.pwinput("🔑 Choose a 4-digit PIN: ", mask="*").strip()
            if len(pin) != 4 or not pin.isdigit():
                print("❌ Invalid PIN format! Must be 4 digits.")
                continue
            card_number = input("💳 Enter your card number: ").strip()
            new_user = {
                "username": username,
                "pin": pin,
                "card_number": card_number,
                "transactions": []
            }
            users.append(new_user)
            save_function(users, books)
            print("✅ Account created successfully! Please login next time.")
            continue

        elif choice == "3":
            print("👋 Exiting Library System. Goodbye!")
            break
        else:
            print("❌ Invalid choice!")
            continue

        # ===== Logged-in Menu =====
        while True:
            print("\n===== 🏛️ Library Menu =====")
            print("1. Show Books")
            print("2. Borrow Book")
            print("3. Return Book")
            print("4. View Transactions")
            print("5. Change PIN")
            print("6. Logout")
            option = input("Select an option (1-6): ").strip()

            if option == "1":
                show_books(books)
            elif option == "2":
                borrow_book(user, books)
            elif option == "3":
                return_book(user, books)
            elif option == "4":
                view_transactions(user, books)
            elif option == "5":
                change_pin(user)
            elif option == "6":
                print(f"🔒 Logging out {user['username']}...")
                save_function(users, books)
                break
            else:
                print("❌ Invalid option!")

            save_function(users, books)


if __name__ == "__main__":
    library_system()
