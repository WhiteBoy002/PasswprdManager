import mysql.connector
import customtkinter
from hashlib import sha256
from tkinter import Text

# Connect to MySQL (assuming default setup)
connection = mysql.connector.connect(
    host="localhost",
    user="root",
)

# Check if the connection is successful
if connection.is_connected():
    cursor = connection.cursor()
    cursor.execute("USE managerbase")
    connection.commit()

current_user_id = None  # Initialize the variable to hold the ID of the logged-in user

# Function to set the current user ID after login
def set_current_user_id(user_id):
    global current_user_id
    current_user_id = user_id

# Example usage after the user logs in and you obtain the user ID
set_current_user_id(1)  # Example user ID, replace it with the actual ID obtained after login

def switch_frame(current_frame, next_frame):
    current_frame.place_forget()
    next_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

def switch_to_login():
    switch_frame(signup_frame, login_frame)

def switch_to_signup():
    switch_frame(login_frame, signup_frame)
    
def switch_to_show_add1():
    switch_frame(login_frame, add_frame)

def switch_to_add():
    switch_frame(add_show_frame, add_frame)

def switch_to_show_add():
    switch_frame(add_frame, add_show_frame)

def establish_connection():
    try:
        # Connect to MySQL (assuming default setup)
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            database="managerbase"  # Specify the database name
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error occurred while connecting to the database: {err}")
        return None

def login():
    global current_user_id
    username = login_entry1.get()
    password = login_entry2.get()

    if not username and not password:
        login_status_label.configure(text="Username and password cannot be empty.", text_color='red')
        return
    elif not username:
        login_status_label.configure(text="Username cannot be empty.", text_color='red')
        return
    elif not password:
        login_status_label.configure(text="Password cannot be empty.", text_color='red')
        return

    hashed_password = sha256(password.encode()).hexdigest()

    cursor.execute('''
        SELECT * FROM users
        WHERE username = %s AND password = %s
    ''', (username, hashed_password))

    account = cursor.fetchone()
    if account:
        current_user_id = account[0]  # Assuming the ID is the first column in the users table
        login_status_label.configure(text="Login successful!", text_color='green')
        switch_to_show_add1()
    else:
        login_status_label.configure(text="Account not found or incorrect password.", text_color='red')

def create_account():
    username = signup_entry1.get()
    password = signup_entry2.get()

    if not username and not password:
        signup_status_label.configure(text="Username and password cannot be empty.", text_color='red')
        return
    elif not username:
        signup_status_label.configure(text="Username cannot be empty.", text_color='red')
        return
    elif not password:
        signup_status_label.configure(text="Password cannot be empty.", text_color='red')
        return

    hashed_password = sha256(password.encode()).hexdigest()

    try:
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        ''', (username, hashed_password))
        connection.commit()
        signup_status_label.configure(text="Account created successfully!", text_color='green')
    except mysql.connector.IntegrityError:
        signup_status_label.configure(text="Username already exists. Please choose another username.", text_color='red')

def create_table(connection):
    try:
        cursor = connection.cursor()
        # SQL query to create the table if it doesn't exist
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS addedpass (
            id INT AUTO_INCREMENT PRIMARY KEY,
            userid INT,
            website VARCHAR(255),
            username VARCHAR(255),
            password VARCHAR(255)
        )
        '''
        # Execute the query
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'addedpass' created successfully.")
    except mysql.connector.Error as err:
        print(f"Error occurred while creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, website, username, password):
    try:
        cursor = connection.cursor()
        # SQL query to insert data into the table
        insert_query = '''
        INSERT INTO addedpass (userid, website, username, password) 
        VALUES (%s, %s, %s, %s)
        '''
        # Execute the query with the data
        cursor.execute(insert_query, (current_user_id, website, username, password))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error occurred while inserting data: {err}")
    finally:
        cursor.close()

def add_password(status_label):
    website = web_entry.get()
    username = user_entry.get()
    password = pass_entry.get()

    # Insert data into the table
    try:
        # Insert data into the table with the obtained user_id
        insert_data(connection, website, username, password)
        status_label.configure(text="Data inserted successfully.", text_color='green')  # Update status label
    except mysql.connector.Error as err:
        print(f"Error occurred while inserting data: {err}")



def fetch_passwords(connection, user_id):
    try:
        cursor = connection.cursor()  
        # SQL query to fetch passwords for a specific user
        select_query = '''
        SELECT website, username, password
        FROM addedpass
        WHERE userid = %s
        '''
        # Execute the query
        cursor.execute(select_query, (user_id,))
        # Fetch all rows
        passwords = cursor.fetchall()
        return passwords
    except mysql.connector.Error as err:
        print(f"Error occurred while fetching passwords: {err}")
        return None
    finally:
        cursor.close()

def fetch_user_info(connection, user_id):
    try:
        cursor = connection.cursor()  
        # SQL query to fetch user information based on user ID
        select_query = '''
        SELECT id, username
        FROM users
        WHERE id = %s
        '''
        # Execute the query
        cursor.execute(select_query, (user_id,))
        # Fetch user info
        user_info = cursor.fetchone()
        return user_info
    except mysql.connector.Error as err:
        print(f"Error occurred while fetching user info: {err}")
        return None
    finally:
        cursor.close()

def switch_to_show_add2():
    # Establish connection to the database
    connection = establish_connection()
    if connection:
        user_info = fetch_user_info(connection, current_user_id)
        if user_info:
            username = user_info[1]  # Assuming username is the second column in the users table
            passwords = fetch_passwords(connection, current_user_id)  
            if passwords:
                show_frame = customtkinter.CTkFrame(master=root)
                show_frame.pack(pady=20, padx=60, fill="both", expand=True)

                label = customtkinter.CTkLabel(master=show_frame, text=f"ALL THE PASSWORDS FOR USER: {username}", font=("Helvetica", 30))
                label.place(relx=0.5, rely=0.1, anchor="center")
                
                button1 = customtkinter.CTkButton(master=add_frame, text="BACK",  width=80, height=30, font=("Helvetica", 16), command=switch_to_show_add)
                button1.place(relx=0.5, rely=0.90, anchor="center")

                text_box = Text(master=show_frame, font=("Helvetica", 16), wrap="word")
                text_box.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.9, relheight=1.1)  # Adjust relheight here

                # Display passwords
                text = ""
                for password in passwords:
                    text += f"Website: {password[0]}\n"
                    text += f"Username: {password[1]}\n"
                    text += f"Password: {password[2]}\n\n"

                text_box.insert("1.0", text)

                text_box.config(state="disabled")  # Set the text widget to read-only

                show_frame.mainloop()
            else:
                print("No passwords found for the user.")
        else:
            print("User information not found.")
    else:
        print("Connection to the database failed.")

# Root window
root = customtkinter.CTk()
root.geometry("800x600")
root.minsize(800, 600)
      
# Add frame
add_frame = customtkinter.CTkFrame(master=root)
add_frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=add_frame, text="ADD Password", font=("Helvetica", 40))
label.place(relx=0.5, rely=0.1, anchor="center")

web_entry = customtkinter.CTkEntry(master=add_frame, placeholder_text="Website", width=320, height=60, font=("Helvetica", 16))
web_entry.place(relx=0.5, rely=0.245, anchor="center")

user_entry = customtkinter.CTkEntry(master=add_frame, placeholder_text="Username", width=320, height=60, font=("Helvetica", 16))
user_entry.place(relx=0.5, rely=0.395, anchor="center")

pass_entry = customtkinter.CTkEntry(master=add_frame, placeholder_text="Password", show="*", width=320, height=60, font=("Helvetica", 16))
pass_entry.place(relx=0.5, rely=0.55, anchor="center")
status_label = customtkinter.CTkLabel(master=add_frame, text="", font=("Helvetica", 16))
status_label.place(relx=0.5, rely=0.8, anchor="center")

button = customtkinter.CTkButton(master=add_frame, text="ADD PASSWORD", width=320, height=60, font=("Helvetica", 16), command=lambda: add_password(status_label))
button.place(relx=0.5, rely=0.74, anchor="center")

label = customtkinter.CTkLabel(master=add_frame, text="--------------------OR--------------------", font=("Helvetica", 20))
label.place(relx=0.5, rely=0.87, anchor="center")

button1 = customtkinter.CTkButton(master=add_frame, text="BACK",  width=80, height=30, font=("Helvetica", 16), command=switch_to_show_add)
button1.place(relx=0.5, rely=0.95, anchor="center")

# Create add or show frame
add_show_frame = customtkinter.CTkFrame(master=root)
add_show_frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=add_show_frame, text="ADD or SHOW", font=("Helvetica", 40))
label.place(relx=0.5, rely=0.2, anchor="center")

button = customtkinter.CTkButton(master=add_show_frame, text="ADD",  width=320, height=60, font=("Helvetica", 16), command=switch_to_add)
button.place(relx=0.5, rely=0.45, anchor="center")

button = customtkinter.CTkButton(master=add_show_frame, text="SHOW",  width=320, height=60, font=("Helvetica", 16), command=switch_to_show_add2)
button.place(relx=0.5, rely=0.65, anchor="center")

# Create login frame
login_frame = customtkinter.CTkFrame(master=root)
login_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

login_label = customtkinter.CTkLabel(master=login_frame, text="Login System", font=("Helvetica", 40))
login_label.place(relx=0.5, rely=0.2, anchor="center")

login_entry1 = customtkinter.CTkEntry(master=login_frame, placeholder_text="Username", width=320, height=60, font=("Helvetica", 16))
login_entry1.place(relx=0.5, rely=0.35, anchor="center")

login_entry2 = customtkinter.CTkEntry(master=login_frame, placeholder_text="Password", show="*", width=320, height=60, font=("Helvetica", 16))
login_entry2.place(relx=0.5, rely=0.5, anchor="center")

login_button = customtkinter.CTkButton(master=login_frame, text="Login", width=320, height=60, font=("Helvetica", 16), command=login)
login_button.place(relx=0.5, rely=0.65, anchor="center")

login_status_label = customtkinter.CTkLabel(master=login_frame, text="", font=("Helvetica", 16))
login_status_label.place(relx=0.5, rely=0.75, anchor="center")

login_or_label = customtkinter.CTkLabel(master=login_frame, text="--------------------OR--------------------", font=("Helvetica", 20))
login_or_label.place(relx=0.5, rely=0.8, anchor="center")

signup_button = customtkinter.CTkButton(master=login_frame, text="SignUp", width=80, height=30, font=("Helvetica", 16), command=switch_to_signup)
signup_button.place(relx=0.5, rely=0.88, anchor="center")

# Create signup frame
signup_frame = customtkinter.CTkFrame(master=root)
signup_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

signup_label = customtkinter.CTkLabel(master=signup_frame, text="SignUp System", font=("Helvetica", 40))
signup_label.place(relx=0.5, rely=0.2, anchor="center")

signup_entry1 = customtkinter.CTkEntry(master=signup_frame, placeholder_text="Username", width=320, height=60, font=("Helvetica", 16))
signup_entry1.place(relx=0.5, rely=0.35, anchor="center")

signup_entry2 = customtkinter.CTkEntry(master=signup_frame, placeholder_text="Password", show="*", width=320, height=60, font=("Helvetica", 16))
signup_entry2.place(relx=0.5, rely=0.5, anchor="center")

signup_button = customtkinter.CTkButton(master=signup_frame, text="SignUp", width=320, height=60, font=("Helvetica", 16), command=create_account)
signup_button.place(relx=0.5, rely=0.65, anchor="center")

signup_status_label = customtkinter.CTkLabel(master=signup_frame, text="", font=("Helvetica", 16))
signup_status_label.place(relx=0.5, rely=0.75, anchor="center")

signup_or_label = customtkinter.CTkLabel(master=signup_frame, text="--------------------OR--------------------", font=("Helvetica", 20))
signup_or_label.place(relx=0.5, rely=0.8, anchor="center")

login_button = customtkinter.CTkButton(master=signup_frame, text="Login", width=80, height=30, font=("Helvetica", 16), command=switch_to_login)
login_button.place(relx=0.5, rely=0.88, anchor="center")

switch_frame(add_frame, add_show_frame)
switch_frame(signup_frame, login_frame)
switch_to_login()

root.mainloop()

# Close the connection
connection.close()
