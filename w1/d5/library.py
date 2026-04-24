import json
import asyncio
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
from datetime import datetime
from enum import Enum


class BookStatus(Enum):
    AVAILABLE = "可借"
    BORROWED = "已借出"
    RESERVED = "已预约"


@dataclass
class Book:
    isbn: str
    title: str
    author: str
    category: str
    status: BookStatus = BookStatus.AVAILABLE
    borrower: Optional[str] = None
    borrow_date: Optional[str] = None

    def borrow(self, borrower: str) -> bool:
        if self.status == BookStatus.AVAILABLE:
            self.status = BookStatus.BORROWED
            self.borrower = borrower
            self.borrow_date = datetime.now().strftime("%Y-%m-%d")
            return True
        return False

    def return_book(self) -> bool:
        if self.status == BookStatus.BORROWED:
            self.status = BookStatus.AVAILABLE
            self.borrower = None
            self.borrow_date = None
            return True
        return False

    def to_dict(self) -> dict:
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "status": self.status.value,
            "borrower": self.borrower,
            "borrow_date": self.borrow_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        status = BookStatus(data.get("status", "可借"))
        return cls(
            isbn=data["isbn"],
            title=data["title"],
            author=data["author"],
            category=data.get("category", "未分类"),
            status=status,
            borrower=data.get("borrower"),
            borrow_date=data.get("borrow_date")
        )

    def __str__(self) -> str:
        return f"《{self.title}》 - {self.author} [{self.status.value}]"


@dataclass
class Member:
    member_id: str
    name: str
    borrowed_books: Set[str] = field(default_factory=set)

    def can_borrow(self) -> bool:
        return len(self.borrowed_books) < 5

    def to_dict(self) -> dict:
        return {
            "member_id": self.member_id,
            "name": self.name,
            "borrowed_books": list(self.borrowed_books)
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Member':
        return cls(
            member_id=data["member_id"],
            name=data["name"],
            borrowed_books=set(data.get("borrowed_books", []))
        )


class Library:
    def __init__(self, name: str):
        self.name = name
        self.books: Dict[str, Book] = {}  # ISBN -> Book
        self.members: Dict[str, Member] = {}  # member_id -> Member

    def add_book(self, book: Book) -> None:
        if book.isbn in self.books:
            raise ValueError(f"ISBN {book.isbn} 已存在")
        self.books[book.isbn] = book
        print(f"添加图书: {book.title}")

    def remove_book(self, isbn: str) -> Optional[Book]:
        if isbn not in self.books:
            raise ValueError(f"ISBN {isbn} 不存在")

        book = self.books[isbn]
        if book.status == BookStatus.BORROWED:
            raise ValueError("已借出的图书不能删除")

        del self.books[isbn]
        print(f"删除图书: {book.title}")
        return book

    def add_member(self, member: Member) -> None:
        if member.member_id in self.members:
            raise ValueError(f"会员ID {member.member_id} 已存在")
        self.members[member.member_id] = member
        print(f"添加会员: {member.name}")

    def borrow_book(self, isbn: str, member_id: str) -> bool:
        if isbn not in self.books:
            raise ValueError("图书不存在")
        if member_id not in self.members:
            raise ValueError("会员不存在")

        book = self.books[isbn]
        member = self.members[member_id]

        if not member.can_borrow():
            raise ValueError("已达到借阅上限")

        if book.borrow(member.name):
            member.borrowed_books.add(isbn)
            print(f"{member.name} 借阅了 《{book.title}》")
            return True
        else:
            raise ValueError("图书不可借")

    def return_book(self, isbn: str, member_id: str) -> bool:
        if isbn not in self.books:
            raise ValueError("图书不存在")
        if member_id not in self.members:
            raise ValueError("会员不存在")

        book = self.books[isbn]
        member = self.members[member_id]

        if book.return_book():
            member.borrowed_books.discard(isbn)
            print(f"{member.name} 归还了 《{book.title}》")
            return True
        return False

    def search_books(self, keyword: str) -> List[Book]:
        keyword = keyword.lower()
        return [
            book for book in self.books.values()
            if keyword in book.title.lower() or
               keyword in book.author.lower() or
               keyword in book.category.lower()
        ]

    def get_available_books(self) -> List[Book]:
        return [book for book in self.books.values()
                if book.status == BookStatus.AVAILABLE]

    def get_statistics(self) -> Dict:
        total = len(self.books)
        available = sum(1 for b in self.books.values()
                        if b.status == BookStatus.AVAILABLE)
        borrowed = sum(1 for b in self.books.values()
                       if b.status == BookStatus.BORROWED)

        # 按类别统计
        categories = {}
        for book in self.books.values():
            categories[book.category] = categories.get(book.category, 0) + 1

        return {
            "total_books": total,
            "available": available,
            "borrowed": borrowed,
            "total_members": len(self.members),
            "categories": categories
        }

    def save_to_file(self, filepath: str) -> None:
        data = {
            "name": self.name,
            "books": [b.to_dict() for b in self.books.values()],
            "members": [m.to_dict() for m in self.members.values()]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"图书馆数据保存到: {filepath}")

    def load_from_file(self, filepath: str) -> None:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.name = data.get("name", self.name)

        self.books.clear()
        for book_data in data.get("books", []):
            book = Book.from_dict(book_data)
            self.books[book.isbn] = book

        self.members.clear()
        for member_data in data.get("members", []):
            member = Member.from_dict(member_data)
            self.members[member.member_id] = member

        print(f"从 {filepath} 加载了 {len(self.books)} 本书, {len(self.members)} 个会员")
