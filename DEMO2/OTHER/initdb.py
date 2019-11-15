import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "pythonsqlite.db"

    table1 = """ CREATE TABLE IF NOT EXISTS User(
	id			integer 	    AUTO_INCREMENT PRIMARY KEY,
	name		text 			NOT NULL,
	password	text			NOT NULL,
	userType	text 			CHECK(userType = "Admin" OR userType = "Faculty" OR userType = "Customer")
);
 """

    table2 = """CREATE TABLE IF NOT EXISTS Admin(
	id			integer		    PRIMARY KEY,
	name		text			NOT NULL,
	password	text			NOT NULL,
	userType	text			NOT NULL,
	FOREIGN KEY (id) REFERENCES User (id)
);
"""
    table3 = """CREATE TABLE IF NOT EXISTS Faculty(
	id			integer		    PRIMARY KEY,
	name		text			NOT NULL,
	password	text			NOT NULL,
	userType	text			NOT NULL,
	FOREIGN KEY (id) REFERENCES User (id)
);
    """

    table4 = """CREATE TABLE IF NOT EXISTS Reservations(
	id			integer		    PRIMARY KEY,
    customerId  integer         not NULL,
	startDate	text			CHECK(startDate IS strftime('%Y-%m-%d', startDate)),
	endDate		text			CHECK(endDate IS strftime('%Y-%m-%d', endDate)),
	roomType	text			NOT NULL,
	FOREIGN KEY (customerId) REFERENCES User (id),
	FOREIGN KEY	(roomType) REFERENCES roomType(type)
);
        """

    table5 = """CREATE TABLE IF NOT EXISTS roomType(
	type			text		PRIMARY KEY
        CHECK(type = "double-full" OR type = "double-queen" OR type = "queen" OR type = "king" OR type = "suite"),
	price			real		NOT NULL,
	quantity	integer	NOT NULL
);
"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, table1)
        #create_table(conn, table2)
        #create_table(conn, table3)
        create_table(conn, table4)
        create_table(conn, table5)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
