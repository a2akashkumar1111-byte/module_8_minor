import json
import os
from models import Book, Magazine, ReferenceBook, StudentMember, FacultyMember, ResearchStudent, NotifiedMember

def save_data(manager):
    data = {
        "items": {},
        "members": {},
        "loans": manager.loans
    }

    for iid, item in manager.items.items():
        t = "Book"
        if isinstance(item, Magazine):
            t = "Magazine"
        if isinstance(item, ReferenceBook):
            t = "ReferenceBook"
        data["items"][iid] = {
            "type": t,
            "title": item.title,
            "is_available": item.is_available
        }

    for mid, mem in manager.members.items():
        t = "StudentMember"
        if isinstance(mem, FacultyMember):
            t = "FacultyMember"
        if isinstance(mem, ResearchStudent):
            t = "ResearchStudent"
        if isinstance(mem, NotifiedMember):
            t = "NotifiedMember"
        data["members"][mid] = {
            "type": t,
            "name": mem.name,
            "borrowing_limit": mem.borrowing_limit,
            "active_loans": mem._active_loans
        }

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

def load_data(manager):
    if not os.path.exists("data.json"):
        return

    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except:
        print("Invalid data.json")
        return

    for iid, info in data.get("items", {}).items():
        if info["type"] == "Book":
            obj = Book(iid, info["title"])
        elif info["type"] == "Magazine":
            obj = Magazine(iid, info["title"])
        else:
            obj = ReferenceBook(iid, info["title"])
        obj.is_available = info["is_available"]
        manager.items[iid] = obj

    for mid, info in data.get("members", {}).items():
        if info["type"] == "StudentMember":
            obj = StudentMember(mid, info["name"])
        elif info["type"] == "FacultyMember":
            obj = FacultyMember(mid, info["name"])
        elif info["type"] == "ResearchStudent":
            obj = ResearchStudent(mid, info["name"])
        else:
            obj = NotifiedMember(mid, info["name"])
        obj.borrowing_limit = info["borrowing_limit"]
        obj._active_loans = info["active_loans"]
        manager.members[mid] = obj

    manager.loans = data.get("loans", {})