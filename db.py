import sqlite3
def connect():
    try:
        conn= sqlite3.connect("promeal.db")
        conn.row_factory=sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Eroare {e}")
        return None


def create_database():
    with connect() as conn:
        cursor = conn.cursor()
        
        conn.execute("PRAGMA foreign_keys = ON")

        # 2. Tabelul MESE (Meals)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT DEFAULT NULL,
                name TEXT UNIQUE NOT NULL, -- UNIQUE previne duplicarea meselor
                img_url TEXT DEFAULT NULL
            )
        """)

        # 3. Tabelul INGREDIENTE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL, -- UNIQUE previne duplicarea ingredientelor
                protein_per_100g REAL NOT NULL,
                calories_per_100g REAL NOT NULL,
                carbo_per_100g REAL NOT NULL
            )
        """)
        
        # 4. Tabelul de legătură MESE-INGREDIENTE 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meal_ingredients (
                meal_id INTEGER,
                ingredient_id INTEGER,
                quantity REAL NOT NULL,
                PRIMARY KEY (meal_id, ingredient_id),
                FOREIGN KEY(meal_id) REFERENCES meals(id) ON DELETE CASCADE,
                FOREIGN KEY(ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE
            )
        """)

        # 5. Tabelul UTILIZATORI
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT, -- Am pus 'id' cu litere mici pentru consistență
                f_name TEXT,
                l_name TEXT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                age INTEGER, -- TINYINT e suportat, dar INTEGER e standard în SQLite
                weight INTEGER,
                height INTEGER,
                target TEXT DEFAULT NULL,
                gender TEXT
            )
        """)

        # 6. Tabelul de LOGURI (Istoric mese consumate)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meal_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                meal_id INTEGER,
                meal_type TEXT,
                date DATE DEFAULT (DATE('now','localtime')),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (meal_id) REFERENCES meals(id) ON DELETE CASCADE
            )
        """)
        #7. Tabelul Favorite Meals
        cursor.execute("""CREATE TABLE IF NOT EXISTS favorite_meals (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTERGER,
                       meal_id INTEGER,
                       FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
                       FOREIGN KEY (meal_id) REFERENCES meals(id) ON DELETE CASCADE)""")
        conn.commit()
        print("Baza de date a fost configurată cu succes!")
