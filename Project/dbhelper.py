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
        '''
            Creates a user account in the database

            Args:
                username (String): account username
                password (String): account password
        '''
        try:
            query = "INSERT INTO UserAccount (Username, Password) VALUES (%s, %s)"
            self.cursor.execute(query, [username, password])
            self.connection.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert user account: {error}")

    def create_user_profile(self, id, first_name, last_name, email):
        '''
            Creates a user profile in the database

            Args:
                id (Integer): user id which the profile belongs to
                first_name (String): User's first name
                last_name (String): User's last name
                email (String): User's email
        '''
        try:
            query = "INSERT INTO UserProfile (Id, FirstName, LastName, Email) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, [id, first_name, last_name, email])
            self.connection.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert user profile: {error}")

    def create_chat_history(self, user_id):
        try:
            query = "INSERT INTO ChatHistory (UserId) VALUES (%s)"
            self.cursor.execute(query, [user_id])
            self.connection.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert chat history: {error}")

    def create_chat_messages(self, chat_history_id, messages):
        '''
            messages is a list of tuples in the form (sender_id, message_text)
        '''

        for message in messages:
            try:
                query = "INSERT INTO ChatHistoryMessage (ChatHistoryId, SenderId, Message) VALUES (%s, %s, %s)"
                self.cursor.execute(query, [chat_history_id, message[0], message[1]])
                self.connection.commit()
            except mysql.connector.Error as error:
                print(f"Failed to insert chat history message: {error}")
        
    
    ### GET ###
    def get_user_profile(self, id):
        query = "SELECT * FROM UserProfile WHERE Id = %s"

        self.cursor.execute(query, [id])
        user_profile = self.cursor.fetchone()
        
        return user_profile
    
    def get_chat_history(self, id):
        query = "SELECT * FROM ChatHistory WHERE Id = %s"

        self.cursor.execute(query, [id])
        chat_history = self.cursor.fetchone()
        
        return chat_history
    
    def get_chat_history_messages(self, chat_history_id):
        chat_history_messages = []

        query = "SELECT SenderId, Message FROM ChatHistoryMessage WHERE ChatHistoryId = %s"

        self.cursor.execute(query, [chat_history_id])
        for message in self.cursor:
             chat_history_messages.append((message[0], message[1]))

        return chat_history_messages


    ### UPDATE ###
    def update_user_account(self, user_account):
        query = "UPDATE UserAccount SET Username = %s, Password = %s WHERE Id = %s"

        self.cursor.execute(query, [user_account[1], user_account[2], user_account[0]])
        self.connection.commit()

    def update_user_account(self, user_profile):
        query = "UPDATE UserProfile SET FirstName = %s, LastName = %s, Email = %s WHERE Id = %s"

        self.cursor.execute(query, [user_profile[1], user_profile[2], user_profile[3], user_profile[0]])
        self.connection.commit()


    ### DELETE ####
    def delete_user_account(self, user_id):
        query = "DELETE FROM UserAccount WHERE Id = %s"

        self.cursor.execute(query, [user_id])
        self.connection.commit()