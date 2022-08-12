import mysql.connector
from random import choice


class ConnectDB:
    def __init__(self, dbhost, dbuser, dbpassword, dbname):
        self.__dbhost = dbhost
        self.__dbuser = dbuser
        self.__dbpassword = dbpassword
        self.__dbname = dbname

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dbhost}, {self.__dbuser}, {self.__dbpassword}, {self.__dbname})'

    @property
    def host(self):
        return self.__dbhost

    @property
    def user(self):
        return self.__dbuser

    @property
    def name(self):
        return self.__dbname

    def connect(self):
        """Tries to connect to the database"""
        try:
            db = mysql.connector.connect(
                host=self.__dbhost,
                user=self.__dbuser,
                password=self.__dbpassword,
                database=self.__dbname
            )
            return db
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'

    def return_infos(self, table):
        """Return all the occurrences of the specified table"""
        db = ConnectDB(self.__dbhost, self.__dbuser, self.__dbpassword, self.__dbname)
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM {table}"
        cursor.execute(sql)
        result = cursor.fetchall()  # Fetch all rows from database table
        print(f'{len(result)} result(s) found in {table}!')
        return result

    def check_user(self, user):
        """Check if the user is already taken and return True"""
        db = ConnectDB(self.__dbhost, self.__dbuser, self.__dbpassword, self.__dbname)
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM accounts WHERE user='{user}'"
        cursor.execute(sql)
        rows = cursor.fetchall()  # Fetch all rows from database table

        # Check if one or more users were find in the database with the same user passed as argument
        if len(rows) > 0:
            return True  # User already taken
        return False

    def check_email(self, email):
        """Check if the email is already taken and return True"""
        db = ConnectDB(self.__dbhost, self.__dbuser, self.__dbpassword, self.__dbname)
        conn = db.connect()
        cursor = conn.cursor()

        sql = f"SELECT * FROM accounts WHERE email='{email}'"
        cursor.execute(sql)
        rows = cursor.fetchall()  # Fetch all rows from database table

        # Check if one or more emails were find in the database with the same email passed as argument
        if len(rows) > 0:
            return True  # Email already taken
        return False

    def send_account(self, *args):
        """Send account details to the database"""

        account = tuple(args)

        try:
            db = ConnectDB(self.__dbhost, self.__dbuser, self.__dbpassword, self.__dbname)
            conn = db.connect()
            cursor = conn.cursor()

            sql = f"INSERT INTO accounts (user, email, password) " \
                  f"VALUES ('{account[0]}', '{account[1]}', '{account[2]}')"
            cursor.execute(sql)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'

    def send_token(self, token):
        """Send token to the database and set it as inactive by default"""
        try:
            db = ConnectDB(self.__dbhost, self.__dbuser, self.__dbpassword, self.__dbname)
            conn = db.connect()
            cursor = conn.cursor()

            sql = f"INSERT INTO tokens (token, active) VALUES ('{token}', '0')"
            cursor.execute(sql)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'


class Token:
    def __init__(self):
        pass

    def __repr__(self):
        return f'{self.__class__.__name__} Class'

    @staticmethod
    def generate_token():
        """Creates a token with 759.375 different combinations and return it"""
        chars = ['a', 'b', 'c', 'd', 'e', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        token = ''

        for i in range(5):
            token += str(choice(chars))
        return token

    @staticmethod
    def activate_token(token):
        """Set token column in the database as 1 (active) and return True"""
        try:
            db = ConnectDB('localhost', 'root', '', 'login_python')
            conn = db.connect()
            cursor = conn.cursor()

            sql = f"UPDATE tokens SET active='1' WHERE token='{token}'"
            cursor.execute(sql)
            conn.commit()
            return True
        except mysql.connector.Error as errorMsg:
            return f'Error: {errorMsg}'
