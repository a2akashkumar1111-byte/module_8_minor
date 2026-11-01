from abc import ABC, abstractmethod
import datetime

class LibraryItem(ABC):
    library_name = "E-Library"

    def __init__(self, item_id, title):
        self.item_id = item_id
        self.title = title
        self.is_available = True

    @abstractmethod
    def loan_period_days(self):
        pass

    @classmethod
    def set_library_name(cls, name):
        cls.library_name = name

class Book(LibraryItem):
    def __init__(self, item_id, title):
        super().__init__(item_id, title)

    def loan_period_days(self):
        return 14

class Magazine(LibraryItem):
    def __init__(self, item_id, title):
        super().__init__(item_id, title)

    def loan_period_days(self):
        return 7

class ReferenceBook(LibraryItem):
    def __init__(self, item_id, title):
        super().__init__(item_id, title)

    def loan_period_days(self):
        return 0

class Member:
    max_active_loans_default = 3

    def __init__(self, member_id, name, borrowing_limit=None):
        self.member_id = member_id
        self.name = name
        self._active_loans = []
        if borrowing_limit is None:
            self.borrowing_limit = Member.max_active_loans_default
        else:
            self.borrowing_limit = borrowing_limit

    @property
    def active_loans(self):
        return self._active_loans

    def can_borrow(self):
        return len(self._active_loans) < self.borrowing_limit

    @classmethod
    def set_default_limit(cls, limit):
        cls.max_active_loans_default = limit

class StudentMember(Member):
    def __init__(self, member_id, name):
        super().__init__(member_id, name, borrowing_limit=3)

class FacultyMember(Member):
    def __init__(self, member_id, name):
        super().__init__(member_id, name, borrowing_limit=5)

class ResearchStudent(StudentMember):
    def __init__(self, member_id, name):
        super().__init__(member_id, name)
        self.borrowing_limit = 4

class NotificationMixin:
    def send_notice(self, message):
        print(f"Notice to {self.name}: {message}")

class NotifiedMember(Member, NotificationMixin):
    def __init__(self, member_id, name):
        super().__init__(member_id, name, borrowing_limit=3)