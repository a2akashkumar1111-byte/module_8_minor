import datetime

class LibraryManager:
    def __init__(self):
        self.items = {}
        self.members = {}
        self.loans = {}

    def register_item(self, item):
        if item.item_id in self.items:
            print("Item ID already exists")
            return False
        self.items[item.item_id] = item
        return True

    def register_member(self, member):
        if member.member_id in self.members:
            print("Member ID already exists")
            return False
        self.members[member.member_id] = member
        return True

    def borrow_item(self, member_id, item_id):
        if member_id not in self.members:
            print("Member not found")
            return False
        if item_id not in self.items:
            print("Item not found")
            return False

        item = self.items[item_id]
        member = self.members[member_id]

        if not item.is_available:
            print("Item not available")
            return False

        if item.loan_period_days() == 0:
            print("Reference book cannot be borrowed")
            return False

        if not member.can_borrow():
            print("Member limit exceeded")
            return False

        issue_date = datetime.date.today()
        due_date = issue_date + datetime.timedelta(days=item.loan_period_days())

        item.is_available = False
        member._active_loans.append(item_id)
        self.loans[item_id] = {
            "member_id": member_id,
            "issue_date": str(issue_date),
            "due_date": str(due_date)
        }

        if hasattr(member, 'send_notice'):
            member.send_notice(f"{item_id} issued, due {due_date}")

        print(f"Borrow successful: {item_id} issued to {member_id}")
        print(f"Due date: {due_date}")
        return True

    def return_item(self, item_id):
        if item_id not in self.loans:
            print("Item not in active loans")
            return False

        loan = self.loans[item_id]
        member_id = loan["member_id"]

        due_date = datetime.date.fromisoformat(loan["due_date"])
        today = datetime.date.today()
        overdue = (today - due_date).days
        if overdue < 0:
            overdue = 0

        fine = self.calculate_fine(overdue)

        self.items[item_id].is_available = True
        self.members[member_id]._active_loans.remove(item_id)
        del self.loans[item_id]

        print(f"Return successful: {item_id}")
        print(f"Overdue days: {overdue}, Fine: {fine}")
        return True

    @staticmethod
    def calculate_fine(overdue_days):
        return overdue_days * 10