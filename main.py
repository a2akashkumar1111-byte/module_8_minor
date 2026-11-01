from models import Book, Magazine, ReferenceBook, StudentMember, FacultyMember, ResearchStudent, NotifiedMember
from library_service import LibraryManager
from storage import save_data, load_data

manager = LibraryManager()
load_data(manager)

while True:
    print("\n1. Register book 2. Register member")
    print("3. Borrow item 4. Return item")
    print("5. View reports 6. Exit")
    ch = input("Choice: ")

    if ch == "1":
        iid = input("Item ID: ")
        title = input("Title: ")
        print("1.Book 2.Magazine 3.ReferenceBook")
        t = input("Type: ")
        if t == "1":
            item = Book(iid, title)
        elif t == "2":
            item = Magazine(iid, title)
        else:
            item = ReferenceBook(iid, title)
        manager.register_item(item)
        save_data(manager)

    elif ch == "2":
        mid = input("Member ID: ")
        name = input("Name: ")
        print("1.Student 2.Faculty 3.ResearchStudent 4.NotifiedMember")
        t = input("Type: ")
        if t == "1":
            mem = StudentMember(mid, name)
        elif t == "2":
            mem = FacultyMember(mid, name)
        elif t == "3":
            mem = ResearchStudent(mid, name)
        else:
            mem = NotifiedMember(mid, name)
        manager.register_member(mem)
        save_data(manager)

    elif ch == "3":
        mid = input("Member ID: ")
        iid = input("Item ID: ")
        manager.borrow_item(mid, iid)
        save_data(manager)

    elif ch == "4":
        iid = input("Item ID: ")
        manager.return_item(iid)
        save_data(manager)

    elif ch == "5":
        print("\nAll items:")
        for iid, item in manager.items.items():
            print(iid, item.title, "Available:" , item.is_available, "Loan days:", item.loan_period_days())

        print("\nAvailable items:")
        for iid, item in manager.items.items():
            if item.is_available:
                print(iid, item.title)

        print("\nActive loans:")
        for iid, loan in manager.loans.items():
            print(iid, "|", loan["member_id"], "| Due:", loan["due_date"])

        print("\nMembers:")
        for mid, mem in manager.members.items():
            print(mid, mem.name, "Borrowed:", len(mem.active_loans), "/", mem.borrowing_limit)

    elif ch == "6":
        save_data(manager)
        break