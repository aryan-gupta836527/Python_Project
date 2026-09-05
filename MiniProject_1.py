#Mini-project
class Book:
    def __init__(self, title, author, book_id):#Available should be True by default
        self.title = title
        self.author = author
        self.book_id = book_id
        self.__available = True # We didn't use default argument as it can be changed when giving fnc call
    def borrow(self):
        if self.__available:
            print("Book borrowed successfully")
            print()
            self.__available = False
            return True
        else:
            print("Book is not available")
            print()
            return False
    def return_book(self):
        if not self.__available:
            print("Book returned successfully")
            print()
            self.__available = True #The book is now available
            return True
        else:
            print("Book is not available")
            print()
            return False
    def display(self):
        print(f"ID: {self.book_id}\nTitle: {self.title}\nAuthor: {self.author}\nAvailable: {self.__available}")
        print()
    @property
    def available(self):
        return self.__available

class Member:
    def __init__(self, name, member_id): # borrowed_books should be an empty list by default
        self.name = name
        self.member_id = member_id
        self.borrowed_books = [] # Same as l:07
    def borrow_book(self,book):# we will give one parameter in parentheses which will be an object of class Book
        i=book.borrow()# now book(Book object) calls borrow of Book class as the obj before dot belongs to Book class
        if i:
            self.borrowed_books.append(book)#self is used we need to use borrowed_books belongs to the class we are working on.
                                            # But notice that we are appending book(object of Book class)
    def return_book(self, book):
        if book in self.borrowed_books:# here book becomes an object of Books class as it is iterating over a list which contains objects of Book class
            book.return_book()# This calls return_book of Book class
            self.borrowed_books.remove(book)
        else:
            print("Book not borrowed by member")
    def display(self):
        for i in self.borrowed_books:# Same as l:43
            i.display()#Calls display of Book class

class Library:
    def __init__(self):
        self.books = []#Same as l:07
        self.members = []#Same as l:07
    def add_book(self, book):#Here we give book which is an object of Book class
        self.books.append(book)
    def add_member(self, member):#Here we give member which is an object of Member class
        self.members.append(member)
    def display_books(self):
        for i in self.books:
            i.display()#Calls display of Book class
    def display_members(self):
        for i in self.members:
            print(i.name, i.member_id)#It accesses attributes of the Member object.
    def borrow_book(self,member_id,book_id):
        member = self.search_member(member_id)
        book = self.search_book(book_id)
        if member is None:
            print("Member not found")
            return
        if book is None:
            print("Book not found")
            return
        member.borrow_book(book)

    def return_book(self, member_id, book_id):
        member=self.search_member(member_id)#self means object of the same class where the method is defined
        book=self.search_book(book_id)
        if member is None:
            print("Member not found")
            return
        if book is None:
            print("Book not found")
            return
        member.return_book(book)
    def search_book(self, book_id):
        for b in self.books:
            if b.book_id == book_id:#b is a Book object → access its book_id attribute and book_id is provided by user in parentheses
                return b #Returns an object of Book class
            #return None => Not used here as it wil terminate the loop after first check
        return None
    def search_member(self, member_id):
        for m in self.members:
            if m.member_id == member_id:#Same as l:89 but for Member class
                return m
            #same as l:105
        return None
    def remove_member(self, member_id):
        member = self.search_member(member_id)
        if member is None:
            print("Member not found")
            return
        if member.borrowed_books:
            print("member must return all books before removal")
            return
        self.members.remove(member)#Removes an object of Member class from the list of objects of Members belonging to the Library class
        print("Member removed")
    def remove_book(self, book_id):
        book = self.search_book(book_id)
        if book is None:
            print("Book not found")
            return
        if not book.available:
            print("Book is currently borrowed")
            return
        self.books.remove(book)
        print("Book removed")