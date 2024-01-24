import sqlite3
from tabulate import tabulate


# Function to create a database and adding of initial data.
def create_database():
    connection = sqlite3.connect("ebookstore.db")
    cursor = connection.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS book_list (
                        ID INTEGER PRIMARY KEY,
                        Title TEXT,
                        Author TEXT,
                        Quantity INTEGER
                    )''')
    
    # Check if the table is empty
    cursor.execute("SELECT COUNT(*) FROM book_list")
    count = cursor.fetchone()[0]
    
    if count == 0:
        initial_data = [
            ("A Tale of Two Cities", "Charles Dickens", 30),
            ("Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
            ("The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
            ("The Lord of the Rings", "J.R.R Tolkien", 37),
            ("Alice in Wonderland", "Lewis Carroll", 12)
        ]
        
        cursor.executemany("INSERT INTO book_list (Title, Author, Quantity) VALUES (?, ?, ?)", initial_data)
        connection.commit()
    else:
        pass  # Table already contains data, no action required
    
    connection.close()


# Function to enable the user to add a book to the database.
def add_book(title, author, quantity):
    connection = sqlite3.connect("ebookstore.db")
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO book_list (Title, Author, Quantity) VALUES (?, ?, ?)", (title, author, quantity))
    
    connection.commit()
    connection.close()


# Function to enable the user to update a book on the database.
def update_book(book_id):
    connection = sqlite3.connect("ebookstore.db")
    cursor = connection.cursor()

    # Check if the book with the given ID exists
    cursor.execute("SELECT * FROM book_list WHERE ID=?", (book_id,))
    book = cursor.fetchone()

    if book is not None:
        print("Please enter the updated information:")
        title = input("Please enter the updated title: ")
        author = input("Please enter the updated author: ")
        quantity = int(input("Please enter the updated quantity: "))
        
        cursor.execute("UPDATE book_list SET Title=?, Author=?, Quantity=? WHERE ID=?", (title, author, quantity, book_id))
        print("Book has been updated successfully!")
    else:
        print("Book with the given ID was not found.")

    connection.commit()
    connection.close()


# Function to enable the user to delete a book from the database.
def delete_book(book_id):
    connection = sqlite3.connect("ebookstore.db")
    cursor = connection.cursor()
    
    # Check if the book with the given ID exists
    cursor.execute("SELECT * FROM book_list WHERE ID=?", (book_id,))
    book = cursor.fetchone()
    
    if book is not None:
        cursor.execute("DELETE FROM book_list WHERE ID = ?", (book_id,))
        print("Book has been deleted successfully!")
    else:
        print("Book with the given ID was not found.")
    
    connection.commit()
    connection.close()


# Function to enable the user to search for a book on the database.
def search_book(book_id):
    connection = sqlite3.connect("ebookstore.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM book_list WHERE ID = ?", (book_id,))
    result = cursor.fetchall()
    
    connection.close()
    
    return result


# Function to enable the user to view the books on the database.
def view_books():
    connection = sqlite3.connect("ebookstore.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM book_list")
    books = cursor.fetchall()
    
    connection.close()
    
    if books:
        headers = ["ID", "Title", "Author", "Quantity"]
        table_data = [list(book) for book in books]
        print("\nList of Books:")
        print(tabulate(table_data, headers, tablefmt="grid"))
    else:
        print("No books were found in the database.")


# Function to display the menu of options and to action the desired user option.
def main():
    create_database()
    
    while True:
        print("""
Menu:
1. Add a book
2. Update a book
3. Delete a book
4. Search for a books
5. View all books
0. Exit""")
        
        choice = input("Please select an option by entering the option number: ")
        
        if choice == "1": # 1. Add a book
            title = input("Please enter the book title: ")
            author = input("Please enter the author of the book: ")
            quantity = int(input("Please enter the quantity of the book: "))
            add_book(title, author, quantity)
            print("Book has been added successfully!")

        elif choice == "2": # 2. Update a book
            book_id = int(input("Please enter the book ID you would like to update: "))
            update_book(book_id)

        elif choice == "3": # 3. Delete a book
            book_id = int(input("Please enter the ID of the book you would like to delete: "))
            delete_book(book_id)

        elif choice == "4": # 4. Search for a books
            book_id = input("Please enter the book ID you would like to look up: ")
            result = search_book(book_id)
            if result:
                print("Search results:")
                for book in result:
                    print(f"""
ID:        {book[0]} 
Title:     {book[1]} 
Author:    {book[2]}
Quantity:  {book[3]}
""")

            else:
                print("Book was not found.")

        elif choice == "5": # 5. View all books
            view_books()

        elif choice == "0": # 0. Exit
            break

        else:
            print("Invalid choice. Please make sure to use the number correlating to the option.")

if __name__ == "__main__":
    main()
