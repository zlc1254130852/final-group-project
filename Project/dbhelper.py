import mysql.connector

class DatabaseHelper:

    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Connected to MySQL database.")
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL database: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection to MySQL database closed.")
    
    ### LOGIN ###
    def verify_credentials(self, username, password):
        res = False

        query = "SELECT * FROM UserAccount WHERE Username = %s"

        self.cursor.execute(query, [username])
        user_account = self.cursor.fetchone()


        # NEED TO ADD HASHING
        if password == user_account[2]:
            res = True

        return res
    
    ### CREATE ### 
    def create_user_account(self, username, password):
        try:
            query = "INSERT INTO UserAccount (Username, Password) VALUES (%s, %s)"
            self.cursor.execute(query, [username, password])
            self.connection.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert user: {error}")

    def create_user_profile(self, id, first_name, last_name, email):
        try:
            query = "INSERT INTO UserProfile (UserId, FirstName, LastName, Email) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, [id, first_name, last_name, email])
            self.connection.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert user: {error}")
    
    ### RETRIEVE ###
    def get_user_profile(self, id):
        query = "SELECT * FROM UserProfile WHERE UserID = %s"

        self.cursor.execute(query, [id])
        user_profile = self.cursor.fetchone()
        
        return user_profile
    
    ### UPDATE ###

    ### DELETE ####

db = DatabaseHelper('localhost', 'mysql', 'abcd1234', 'main')
db.connect()
print(db.get_user_profile(3))
db.close()