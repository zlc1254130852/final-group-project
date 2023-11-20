CREATE TABLE UserAccount (
	Id int AUTO_INCREMENT,
	Username VARCHAR(30) NOT NULL,
	Password VARCHAR(30) NOT NULL,
	PRIMARY KEY (Id),
	UNIQUE(Username)
);

CREATE TABLE UserProfile (
	Id int,
	FirstName VARCHAR(30) NOT NULL,
	LastName VARCHAR(30) NOT NULL,
	Email VARCHAR(255),
	DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (Id),
	FOREIGN KEY (Id) REFERENCES UserAccount(Id) ON DELETE CASCADE,
	UNIQUE(Email)
);

CREATE TABLE ChatHistory (
	Id int AUTO_INCREMENT,
    UserId int NOT NULL,
    ChatDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (Id),
    FOREIGN KEY (UserId) REFERENCES UserAccount(Id) ON DELETE CASCADE
);

CREATE TABLE ChatHistoryMessage (
	Id int AUTO_INCREMENT,
    ChatHistoryId int,
    SenderId int,
    Message TEXT,
    PRIMARY KEY (Id),
    FOREIGN KEY (ChatHistoryId) REFERENCES ChatHistory(Id) ON DELETE CASCADE
);

CREATE TABLE Test (    
    Id INT NOT NULL AUTO_INCREMENT,          
    Type VARCHAR(100) NOT NULL,         
    Name VARCHAR(100) NOT NULL,     
    PRIMARY KEY (Id)
);

CREATE TABLE TestCorrectAnswer (    TestId INT NOT NULL,  QuestionId INT NOT NULL,     Answer VARCHAR(100) NOT NULL,     FOREIGN KEY (TestId) REFERENCES Test(Id) );

CREATE TABLE TestUserAnswer (    
    TestId INT NOT NULL,  
    UserId INT NO NULL,
    QuestionId INT NOT NULL,     
    Answer VARCHAR(100) NOT NULL,     
    FOREIGN KEY (TestId) REFERENCES Test(Id), 
    FOREIGN KEY (UserId) REFERENCES UserAccount(Id)
);

CREATE TABLE UserTestResult (  
    ResultId INT NOT NULL AUTO_INCREMENT,  
    TestId INT NOT NULL,     
    UserId INT NOT NULL,  
    UserScore INT NOT NULL,     
    TotalScore INT NOT NULL,     
    PRIMARY KEY (ResultId),     
    FOREIGN KEY (TestId) REFERENCES Test(Id),     
    FOREIGN KEY (UserId) REFERENCES UserAccount(Id)
);