import csv
import sqlite3

INPUT_STRING='''
ENTER THE OPTION:
1. Create TABLE
2. DUMP USER from csv to the USER TABLE 
3. ADD USER into TABLE 
4. QUERY all USER from the TABLE 
5. QUERY all USER by ID and TABLE
6. QUERY specified no. of USERs from TABLE
7. DELETE all USERS
8. DELETE all USERS by id
9. UPDATE all USER
10. Press any key to exit

'''

def create_connection():
    try:
        con=sqlite3.connect('users.sqlite3') #creating new database named (users)
        return con
    except Exception as e:
        print(e)



def create_table(con):
    CREATE_USERS_TABLE_QUERY="""
    CREATE TABLE IF NOT EXISTS users(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name CHAR(255) NOT NULL,
    last_name CHAR(255) NOT NULL,
    company_name CHAR(255) NOT NULL,
    address CHAR(255) NOT NULL,
    city CHAR(255) NOT NULL,
    county CHAR(255) NOT NULL,
    state CHAR(255) NOT NULL,
    zip REAL NOT NULL,
    phone1 CHAR(255) NOT NULL,
    phone2 CHAR(255),
    email CHAR(255) NOT NULL,
    web text
    );
"""


    cur =con.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    print('Users table was created sucessfully.')


def read_csv():
    users=[]
    with open('sample_users.csv','r') as f:
        data=csv.reader(f)
        for user in data:
            users.append(tuple(user))

    return users[1:]

def insert_users(con,users):
    user_add_query='''
    INSERT INTO users
    (
    first_name,
    last_name,
    company_name,
    address,
    city,
    county,
    state,
    zip,
    phone1,
    phone2,
    email,
    web
    )
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
    '''
    cur=con.cursor()
    cur.executemany(user_add_query,users)
    con.commit()
    print(f'{len(users)} users were imported sucessfully')

def select_users(con,no_of_users=None):
    cur=con.cursor()
    if no_of_users:
        users=cur.execute(f'SELECT * FROM users LIMIT {no_of_users} ')
    else:
        users=cur.execute("SELECT * FROM users")
    for user in users:
        print(user)

def select_user_by_id(con,user_id):
    cur=con.cursor()
    users=cur.execute('SELECT * FROM users where id=?;',(user_id,))
    for user in users:
        print(user)

def delete_users(con):
    cur=con.cursor()
    cur.execute('DELETE * FROM users;')
    con.commit()
    print('All users are deleted sucessfully')

def delete_user_by_id(con,user_id):
    cur=con.cursor()
    cur.execute('DELETE FROM users where id=?',(user_id,))
    con.commit()
    print(f'User with id [{user_id}] was deleted sucessfully.')

COLUMNS=(
    'first_name',
    'last_name', 
    'company_name', 
    'address', 
    'city', 
    'county', 
    'state', 
    'zip', 
    'phone1', 
    'phone2', 
    'email', 
    'web'
)

def update_user_by_id(con,user_id,column_name,column_value):
    update_query=f'UPDATE users set {column_name}=? where id = ?;'
    cur=con.cursor()
    cur.execute(update_query,(column_value,user_id))
    con.commit()
    print(
        f'[{column_name}] was updated with value [{column_name}] of user with id [{user_id}]'
    )

def main():
    con=create_connection()
    if con:
        user_input=input(INPUT_STRING)
        if user_input=='1':
            create_table(con)

        elif user_input=='2':
            users = read_csv()
            insert_users(con,users)

        elif user_input=='3':
            user_data=[]
            for column in COLUMNS:
                column_value=input(f'Enter the value of {column}:')
                user_data.append(column_value)
            insert_users(con,[tuple(user_data)])

        elif user_input=='4':
            select_users(con)

        elif user_input=='5':
            user_id=input('enter the user id')
            if user_id.isnumeric():
                select_user_by_id(con,user_id)
            else:
                print('Invalid user id. exiting the Program')

        elif user_input=='6':
            no_of_users=input('enter the number of users')
            if no_of_users.isnumeric():
                select_users(con,no_of_users)
        
        elif user_input=='7':
            confirm=input('are you sure to delete all the users? (y/n):')
            if confirm.lower() in['y','yes']:
                delete_users(con)
            else:
                print('Data still available')

        elif user_input=='8':
            user_id=input('enter the user id ')
            if user_id.isnumeric():
                delete_user_by_id(con,user_id)

        elif user_input=='9':
            user_id=input('Enter the id of user: ')
            if user_id.isnumeric():
                column_name=input(
                    f'Enter the column you want to update. please make sure your column is within {COLUMNS}:'
                )
                if column_name in COLUMNS:
                    column_value=input("enter the value of {column_name}:")
                    update_user_by_id(con,user_id, column_name,column_value)
        else:
            exit()
            
main()