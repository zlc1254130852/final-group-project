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

    def create_test(self, test_type, test_name):
        try:
            query = "INSERT INTO Test (Type, Name) VALUES (%s, %s)"
            self.cursor.execute(query, [test_type, test_name])
            self.connection.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert test: {error}")

    def create_user_answers(self, test_id, user_id, answers):
        '''
            answers is a list of tuples in the form (question_id, answer)
        '''
        for answer in answers:
            try:
                query = "INSERT INTO TestUserAnswer (TestId, UserId, QuestionId, Answer) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(query, [test_id, user_id, answer[0], answer[1]])
                self.connection.commit()
            except mysql.connector.Error as error:
                print(f"Failed to insert user test answers: {error}")

    def create_correct_answers(self, test_id, answers):
        '''
            answers is a list of tuples in the form (question_id, answer)
        '''
        for answer in answers:
            try:
                query = "INSERT INTO TestCorrectAnswer (TestId, QuestionId, Answer) VALUES (%s, %s, %s)"
                self.cursor.execute(query, [test_id, answer[0], answer[1]])
                self.connection.commit()
            except mysql.connector.Error as error:
                print(f"Failed to insert correct test answers: {error}") 

    def create_user_test_results(self, test_id, user_id, user_score, total_score):
        '''
            answers is a list of tuples in the form (question_id, answer)
        '''
        
        try:
            query = "INSERT INTO UserTestResult (TestId, QuestionId, Answer) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, [test_id, user_id, user_score, total_score])
            self.connection.commit()
        except mysql.connector.Error as error:
            print(f"Failed to insert correct test answers: {error}")              
    
    
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
    
    def get_test_correct_answers(self, test_id):
        answers = []

        query = "SELECT QuestionId, Answer FROM TestCorrectAnswer WHERE TestId = %s"

        self.cursor.execute(query, [test_id])
        for answer in self.cursor:
             answers.append((answer[0], answers[1]))

        return answers
    
    def get_test_user_answers(self, test_id, user_id):
        answers = []

        query = "SELECT QuestionId, Answer FROM TestUserAnswer WHERE TestId = %s AND UserId = %s"

        self.cursor.execute(query, [test_id, user_id])
        for answer in self.cursor:
             answers.append((answer[0], answers[1]))

        return answers
    
    def get_user_test_resutls(self, test_id, user_id):
        results = []

        query = "SELECT UserScore, TotalScore FROM UserTestResult WHERE TestId = %s AND UserId = %s"

        self.cursor.execute(query, [test_id, user_id])
        for result in self.cursor:
             results.append((result[0], result[1]))

        return results


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