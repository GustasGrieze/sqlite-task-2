# Tasks:
# Update current code base with these 4 new methods. 
# Test it.
# First, lower the number of the possible entry to 100 the db -> table. (possible increase by 1000's)
# Update current task that instead of creating 1 table,  it would create 2 : 
# New table name = 'personalInfo' consist (name, surname, dob ('YYYY-MM-DD' format, year should be calculated from the age value, and other two values auto generates) (date of birth), email: (name.surname@gmail.com), phone(+3706******* , * - random numbers), sex (male, female, unicorn))
# During the creation of the second table , it should use the same class object.
# !! Important - names and surnames should be the same in both database tables by the same order. 

import sqlite3
import names
from random import randint, randrange, choice
import time
from calendar import isleap


class SqlDatabase:
    def __init__(self, db_name: str) -> None:
        self._conn = sqlite3.connect(db_name+".db")
        self._cursor = self._conn.cursor()

    def create_table(self, table_name: str, columns: str) -> None:
        try:
            with self._conn:
                self._cursor.execute(f"""CREATE TABLE IF NOT EXISTS
                {table_name} (
                {columns}
                )""")
        except Exception as e:
            print(f"Unable to create table!. Error msg: {e}")

    def write(self, table_name: str, entry_values: str) -> None:
        with self._conn:
            self._cursor.execute(f"INSERT INTO {table_name} VALUES ({entry_values})")

            
def generate_first_name() -> str:
    return names.get_first_name()

def generate_last_name() -> str:
    return names.get_last_name()

def get_random_age() -> int:
    return randint(18, 99)

def get_random_salary() -> int:
    return randrange(50000, 250000, 25000)

def get_date_of_birth(generated_age: int) -> str:
    year_of_birth = 2022 - generated_age
    my_dictio = {"01":31, "02":28, "03":31, "04":29, "05":31, "06":30, "07":31, "08":31, "09":30, "10":31, "11":30, "12":31}
    month, day = choice(list(my_dictio.items()))
    random_day = randint(1, 31)
    if random_day > day:
        random_day -= 1
    if month == "02":
        if isleap(year_of_birth):
            random_day -= 3
        else:
            random_day -= 2
    if random_day <= 9:
        random_day = "0" + str(random_day)
    return f"{year_of_birth}-{month}-{random_day}"

def get_email(name: str, surname: str) -> str:
    return f"{name}.{surname}@gmail.com"

def get_phone_number() -> int:
    return 86000000 + randint(100000, 999999)

def get_gender() -> str:
    return choice(['Male', 'Female'])


class MainDatabase(SqlDatabase):
    def __init__(self) -> None:
        self.user_database_name = input("Enter your desired database name: ")
        super().__init__(self.user_database_name)
        self.user_table_name = input("Please enter your desired table name: ")
        self.user_column_names = input("Please enter your column names: ")
        self.info_user_table_name = input("Please enter your second desired table name: ")
        self.info_user_column_names = input("Please enter your second table column names: ")
        self.db = SqlDatabase(self.user_database_name)
        self.create_database_table(self.user_table_name, self.user_column_names)
        self.create_database_table(self.info_user_table_name, self.info_user_column_names)
        self.populate_database()
        self.interface()

    def create_database_table(self, table_name, column_names) -> None:
        self.db.create_table(table_name, column_names)

    def populate_database(self) -> None:
        for i in range(100):
            given_name = generate_first_name()
            given_surname = generate_last_name()
            given_age = get_random_age()
            self.db.write(table_name=self.user_table_name, entry_values=f"'{given_name}', '{given_surname}', '{given_age}', '{get_random_salary()}'")
            self.db.write(table_name=self.info_user_table_name, entry_values=f"'{given_name}', '{given_surname}', '{get_date_of_birth(given_age)}', '{get_email(given_name, given_surname)}', '{get_phone_number()}', '{get_gender()}'")
            print(f"{i}%", end="\rCompleted:", flush=True)

    def print_users_with_a_bigger_than_selected_salary(self) -> list:
        value = input("Please enter the amount of money you want: ")
        with self._conn:
            self._cursor.execute(f"SELECT Name From {self.user_table_name} WHERE Salary >= {value}")
            return (self._cursor.fetchall())

    def print_every_user(self) -> list:
        with self._conn:
            self._cursor.execute(f"SELECT Name, Surname FROM {self.user_table_name}")
            return (self._cursor.fetchall())

    def delete_selected_user(self) -> str:
        selected_user_surname = input("Enter the surname of the user you would like to delete: ")
        with self._conn:
            self._cursor.execute(f"DELETE from {self.user_table_name} WHERE surname={selected_user_surname}")
            return f"Deleted user {selected_user_surname}"

    def select_specified_people_1(self) -> list:
        with self._conn:
            self._cursor.execute(f"SELECT Name, Surname FROM {self.user_table_name} WHERE Name LIKE'a%' AND Surname LIKE'%w%'")
            return (self._cursor.fetchall())

    def select_specified_people_2(self) -> list:
        with self._conn:
            self._cursor.execute(f"SELECT Name, Surname FROM {self.user_table_name} WHERE Salary < 150000 OR Age > 50")
            return (self._cursor.fetchall())

    def select_specified_people_3(self) -> list:
        with self._conn:
            self._cursor.execute(f"SELECT Name, Surname, Salary FROM {self.user_table_name} WHERE Age BETWEEN 38 AND 72")
            return (self._cursor.fetchall())

    def select_specified_people_4(self) -> list:
        with self._conn:
            self._cursor.execute(f"SELECT COUNT(Name), AVG(Salary) FROM {self.user_table_name} WHERE Age BETWEEN 19 AND 43")
            return (self._cursor.fetchall())

    def add_column(self) -> None:
        with self._conn:
            selected_table = input("Please enter the table name you would like to alter: ")
            selected_column = input("Please enter the column name you would like to add: ")
            data_type = input("Enter your desired data type: ")
            self._cursor.execute(f"ALTER TABLE {selected_table} ADD COLUMN {selected_column} {data_type}")

    def rename_column(self) -> None:
        with self._conn:
            selected_table = input("Please enter the table name you would like to alter: ")
            selected_column = input("Please enter the column name you would like to alter: ")
            new_column_name = input("Please enter the new column name: ")
            self._cursor.execute(f"ALTER TABLE {selected_table} RENAME COLUMN {selected_column} TO {new_column_name}")
    
    def rename_table(self) -> None:
        with self._conn:
            selected_table = input("Please enter the table name you would like to alter: ")
            alter_table_to = input("Please enter the name you would like to rename the table to: ")
            self._cursor.execute(f"ALTER TABLE {selected_table} RENAME TO {alter_table_to}")
    
    def drop_column(self) -> None:
        with self._conn:
            selected_table = input("Please enter the table name you would like to alter: ")
            selected_column = input("Please enter the column name: ")
            self._cursor.execute(f"ALTER TABLE {selected_table} DROP COLUMN {selected_column}")

    def interface(self) -> None:
        while True:
            time.sleep(3)
            first_input = input('''\n
            Welcome to our HR system
            Select one of the options bellow to choose which operation you would like to execute:
            1 - Print every user in the database
            2 - Delete a user from the database
            3 - Print users with a bigger than selected salary
            4 - Specialized command
            5 - Specialized command
            6 - Specialized command
            7 - Specialized command
            8 - Add a new column
            9 - Rename a colmun
            10 - Rename a table
            11 - Drop a column

            To exit the program, type EXIT.
            
            Your choice: \n''').lower()
                
            if first_input == '1':
                print(self.print_every_user())

            elif first_input == '2':
                print(self.delete_selected_user())

            elif first_input == '3':
                print(self.print_users_with_a_bigger_than_selected_salary())

            elif first_input == '4':
                print(self.select_specified_people_1())

            elif first_input == '5':
                print(self.select_specified_people_2())

            elif first_input == '6':
                print(self.select_specified_people_3())

            elif first_input == '7':
                print(self.select_specified_people_4())

            elif first_input == '8':
                self.add_column()

            elif first_input == '9':
                self.rename_column()

            elif first_input == '10':
                self.rename_table()

            elif first_input == '11':
                self.drop_column()

            elif first_input == 'exit':
                print("The program has ended")
                break

            else:
                print("Choose one of the listed options")


if __name__ == "__main__":
    MainDatabase()

