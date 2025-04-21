import sqlite3                                   #import the library of sqlite

# Connect to SQLite database
conn = sqlite3.connect("Expense_Tracker_System.db")                                                                         
c = conn.cursor()

# Create User table
c.execute(""" create table User(                                                                                             
          id integer  primary key autoincrement,                                                                             
          username TEXT unique,                                                                                            
          password text                                                                                                      
          )""")                                                                                                              
                                                                                                                            

# Create Expenses table

c.execute(""" create table Expenses(  
          id integer  primary key autoincrement,
          user_id integer references User(id),
          category Text,
          date text,
          amount real,
          description text
          )""")

# Create Income table

c.execute(""" create table Income(  
          id integer  primary key autoincrement,
          user_id integer references User(id),
          amount real,
          date text,
          source text
          )""")




# Commit changes and close connection
conn.commit()
conn.close()

print("Database and tables created successfully!")


# Datatypes
# NULL
# INTEGER
# REAL
# TEXT
 # BLOB 