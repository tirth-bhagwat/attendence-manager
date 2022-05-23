import sqlite3
import re


class DB:
    def __init__(self, path, filename=''):
        self.path = f"{path}{'' if filename == '' else '/'}{filename}.db"

        print(self.path)
        with sqlite3.connect(self.path) as connection:
            pass

    def createTable(self, tableName):
        # possible errors:
        # table {} already exists
        # unrecognized token: "21C22001"
        # unable to open database file
        try:
            with sqlite3.connect(self.path) as connection:
                connection.execute(f'''
                    CREATE TABLE {tableName}(
                        id INTEGER PRIMARY KEY AUTOINCREMENT
                    );
                ''')
            return 0
        except sqlite3.Error as err:
            return err

    def deleteTable(self, tableName):
        try:
            with sqlite3.connect(self.path) as connection:
                connection.execute(f'''
                    DROP TABLE {tableName}
                ''')
            return 0
        except sqlite3.Error as err:
            return err

    def addCol(
        self,
        tableName: str,
        colName: str,
        dType: str = "TEXT"
    ):
        # possible errors:
        # no such table: {}
        try:
            with sqlite3.connect(self.path) as connection:
                connection.execute(f'''
                    ALTER TABLE {tableName}
                    ADD COLUMN {colName} {dType};
                ''')
            return 0
        except sqlite3.Error as err:
            return err

    def addRow(
        self,
        tableName: str,
        rowNames: tuple,
        values: tuple
    ):
        try:
            with sqlite3.connect(self.path) as connection:
                connection.execute(f'''
                    INSERT INTO {tableName} {rowNames}
                    VALUES {values};
                ''')
            return 0
        except sqlite3.Error as err:
            return err

# db3=DB('./data/db3.db')
# print(db3.deleteTable(t1))
# print(db3.createTable(t1))
# print(db3.addCol(t1,'c1',0))
# print(db3.delCol(t1,'c2'))
