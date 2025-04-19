import sqlite3
import os

DB_DIR = "test_databases"
os.makedirs(DB_DIR, exist_ok=True)

async def create_test_databases():
    # 1. Simple Library Database
    db_path = os.path.join(DB_DIR, "library.sqlite")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE books
                 (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER)''')
    
    books = [
        (1, "The Hobbit", "J.R.R. Tolkien", 1937),
        (2, "1984", "George Orwell", 1949),
        (3, "Pride and Prejudice", "Jane Austen", 1813),
        (4, "Harry Potter", "J.K. Rowling", 1997),
        (5, "The Great Gatsby", "F. Scott Fitzgerald", 1925)
    ]
    c.executemany('INSERT INTO books VALUES (?,?,?,?)', books)
    conn.commit()
    conn.close()
    
    # 2. Student Grades Database
    db_path = os.path.join(DB_DIR, "school.sqlite")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE students
                 (id INTEGER PRIMARY KEY, name TEXT, grade INTEGER)''')
    
    students = [
        (1, "John Smith", 85),
        (2, "Emma Johnson", 92),
        (3, "Michael Brown", 78),
        (4, "Sarah Davis", 95),
        (5, "James Wilson", 88)
    ]
    c.executemany('INSERT INTO students VALUES (?,?,?)', students)
    conn.commit()
    conn.close()

    # 3. Pet Shop Database
    db_path = os.path.join(DB_DIR, "petshop.sqlite")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE pets
                 (id INTEGER PRIMARY KEY, name TEXT, species TEXT, age INTEGER, price REAL)''')
    
    pets = [
        (1, "Max", "Dog", 2, 500.00),
        (2, "Luna", "Cat", 1, 300.00),
        (3, "Rocky", "Dog", 3, 450.00),
        (4, "Charlie", "Bird", 1, 50.00),
        (5, "Bella", "Cat", 2, 350.00)
    ]
    c.executemany('INSERT INTO pets VALUES (?,?,?,?,?)', pets)
    conn.commit()
    conn.close()


    # 4. Movie Ratings Database
    db_path = os.path.join(DB_DIR, "movies.sqlite")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE movies
                 (id INTEGER PRIMARY KEY, title TEXT, genre TEXT, rating FLOAT)''')
    
    movies = [
        (1, "The Matrix", "Sci-Fi", 8.7),
        (2, "Frozen", "Animation", 7.4),
        (3, "The Dark Knight", "Action", 9.0),
        (4, "Inception", "Sci-Fi", 8.8),
        (5, "Toy Story", "Animation", 8.3)
    ]
    c.executemany('INSERT INTO movies VALUES (?,?,?,?)', movies)
    conn.commit()
    conn.close()

       # 5. Restaurant Menu Database
    db_path = os.path.join(DB_DIR, "restaurant.sqlite")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE menu
                 (id INTEGER PRIMARY KEY, item TEXT, category TEXT, price REAL)''')
    
    items = [
        (1, "Burger", "Main", 9.99),
        (2, "Caesar Salad", "Starter", 6.99),
        (3, "Ice Cream", "Dessert", 4.99),
        (4, "Pizza", "Main", 12.99),
        (5, "Coffee", "Drinks", 2.99)
    ]
    c.executemany('INSERT INTO menu VALUES (?,?,?,?)', items)
    conn.commit()
    conn.close()
    # 6. Employee Database
    db_path = os.path.join(DB_DIR, "employees.sqlite")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE employees
                 (id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary INTEGER)''')
    
    employees = [
        (1, "Alice Johnson", "IT", 75000),
        (2, "Bob Smith", "Sales", 65000),
        (3, "Carol White", "IT", 78000),
        (4, "David Brown", "HR", 60000),
        (5, "Eve Wilson", "Sales", 68000)
    ]
    c.executemany('INSERT INTO employees VALUES (?,?,?,?)', employees)
    conn.commit()
    conn.close()
    # 7. Product Inventory Database
    db_path = os.path.join(DB_DIR, "inventory.sqlite")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE products
                 (id INTEGER PRIMARY KEY, name TEXT, category TEXT, quantity INTEGER, price REAL)''')
    
    products = [
        (1, "Laptop", "Electronics", 15, 999.99),
        (2, "T-Shirt", "Clothing", 100, 19.99),
        (3, "Book", "Books", 50, 14.99),
        (4, "Smartphone", "Electronics", 25, 599.99),
        (5, "Jeans", "Clothing", 75, 49.99)
    ]
    c.executemany('INSERT INTO products VALUES (?,?,?,?,?)', products)
    conn.commit()
    conn.close()
    # 8. Car Dealership Database
    db_path = os.path.join(DB_DIR, "cars.sqlite")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE cars
                 (id INTEGER PRIMARY KEY, brand TEXT, model TEXT, year INTEGER, price REAL)''')
    
    cars = [
        (1, "Toyota", "Camry", 2022, 25000),
        (2, "Honda", "Civic", 2021, 22000),
        (3, "Ford", "Mustang", 2023, 35000),
        (4, "Tesla", "Model 3", 2022, 45000),
        (5, "BMW", "X3", 2021, 42000)
    ]
    c.executemany('INSERT INTO cars VALUES (?,?,?,?,?)', cars)
    conn.commit()
    conn.close()



    # 9. Music Collection Database
    db_path = os.path.join(DB_DIR, "music.sqlite")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE songs
                 (id INTEGER PRIMARY KEY, title TEXT, artist TEXT, genre TEXT, duration INTEGER)''')
    
    songs = [
        (1, "Happy", "Pharrell Williams", "Pop", 238),
        (2, "Bohemian Rhapsody", "Queen", "Rock", 354),
        (3, "Shape of You", "Ed Sheeran", "Pop", 233),
        (4, "Sweet Child O' Mine", "Guns N' Roses", "Rock", 356),
        (5, "Bad Guy", "Billie Eilish", "Pop", 194)
    ]
    c.executemany('INSERT INTO songs VALUES (?,?,?,?,?)', songs)
    conn.commit()
    conn.close()
    # 10. Sports League Database
    db_path = os.path.join(DB_DIR, "sports.sqlite")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE teams
                 (id INTEGER PRIMARY KEY, name TEXT, city TEXT, wins INTEGER, losses INTEGER)''')
    
    teams = [
        (1, "Eagles", "Philadelphia", 12, 4),
        (2, "Lakers", "Los Angeles", 15, 5),
        (3, "Bulls", "Chicago", 8, 10),
        (4, "Warriors", "Golden State", 14, 6),
        (5, "Celtics", "Boston", 13, 7)
    ]
    c.executemany('INSERT INTO teams VALUES (?,?,?,?,?)', teams)
    conn.commit()
    conn.close()
