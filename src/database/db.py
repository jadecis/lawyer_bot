import sqlite3

class Database():
    def __init__(self, db_file):
        self.connection= sqlite3.connect(db_file)
        self.cursor= self.connection.cursor()
    
    def get_user(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM users WHERE user_id= ?", (user_id, )).fetchone()
    
    def info_payment_user(self, user_id): 
        with self.connection:
            return self.cursor.execute("SELECT * FROM payment WHERE user_id= ?", (user_id, )).fetchone()
        
    def add_payment_user(self, user_id, end_date, payment): 
        with self.connection:
            return self.cursor.execute("INSERT INTO payment (user_id, end_date, payment ) VALUES (?, ?, ?)", (user_id, end_date, payment, ))
        
     
    def add_user(self, user_id, user_name, status): 
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id, user_name, status ) VALUES (?, ?, ?)",
                                (user_id, user_name, status, ))
          
    def update_user(self, user_id, user_name, status):
        with self.connection:
            self.cursor.execute("UPDATE users SET user_name= ?, status= ? WHERE user_id=?",
                                ( user_name, status, user_id,))
            
    def add_specialist(self, user):
        with self.connection:
            self.cursor.execute("""
            INSERT INTO specialist
            (
                user_id,
                user_name,
                first_name,
                last_name,
                country,
                region,
                special,
                contact,
                payment
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (user["user_id"],
             user["user_name"],
             user["first_name"],
             user["last_name"],
             user["country"],
             user["region"],
             user["special"],
             user["contact"],
             True,))
            
    def add_emigrant(self, user):
        with self.connection:
            self.cursor.execute("""
            INSERT INTO emigrant
            (
                user_id,
                user_name,
                first_name,
                last_name,
                country,
                region,
                special,
                problem
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (user["user_id"],
                user["user_name"],
                user["first_name"],
                user["last_name"],
                user["country"],
                user["region"],
                user["special"],
                user["problem"], ))
            
    def update_emigrant(self, user):
        with self.connection:
            self.cursor.execute("""
            UPDATE emigrant 
            SET user_id= ?,
                user_name= ?,
                first_name= ?,
                last_name= ?,
                country= ?,
                region= ?,
                special= ?,
                problem= ?
            WHERE user_id= ?
            """,
            (   user["user_id"],
                user["user_name"],
                user["first_name"],
                user["last_name"],
                user["country"],
                user["region"],
                user["special"],
                user["problem"],
                user["user_id"],))
            
    def update_specialist(self, user):
        with self.connection:
            self.cursor.execute("""
            UPDATE specialist
            SET user_id= ?,
                user_name= ?,
                first_name= ?,
                last_name= ?,
                country= ?,
                region= ?,
                special= ?,
                contact= ?
            WHERE user_id= ?""",
            (user["user_id"],
             user["user_name"],
             user["first_name"],
             user["last_name"],
             user["country"],
             user["region"],
             user["special"],
             user["contact"],
             user["user_id"],))
            
    def get_specialist(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM specialist WHERE user_id= ?", (user_id,)).fetchone()
        
    def get_emigrants_by(self, filtres):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM emigrant WHERE special = ? and country in ({filtres['counrty']})",
                                       (filtres['special'],
                                        )).fetchall()
            
    def get_specialists_by(self, special):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM specialist WHERE special = ?", (special,)).fetchall()
        