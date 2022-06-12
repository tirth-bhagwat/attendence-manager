import functools
import os
import re
import sqlite3


def tupleToSQL(tup):
    tup = ('',)+tup
    return str(
        functools.reduce(
            lambda i, j: f'''{i},"{j}"''',
            tup
        )
    )[1:]


class DB:
    def __init__(
        self,
        path: str,
        filename: str = ''
    ):
        self.path = f"{path}{'' if filename == '' else '/'}{filename}{'.db' if filename != '' else ''}"

        with sqlite3.connect(self.path) as connection:
            pass

    def rows(self, tableName: str):
        try:
            with sqlite3.connect(self.path) as connection:
                cur = connection.cursor()
                cur.execute(f'''
                    SELECT COUNT(*) FROM {tableName}
                ''')
                rows = cur.fetchall()[0][0]
            return rows
        except sqlite3.Error as err:
            return err

    def isNotEmpty(self):
        '''Moves the database file from EMPTY_DATA_DIR to DATA_DIR'''
        if "/empty/" in self.path:
            emptyInd = re.match(".*/empty/", self.path)
            newPath = self.path[0:emptyInd.end()-6]+self.path[emptyInd.end():]
            os.rename(self.path, newPath)
            self.path = newPath

    def createTable(self, tableName: str):
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

    def deleteTable(self, tableName: str):
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

    def readRows(
        self,
        tableName: str,
        columns: tuple,
        where: str = ''
    ):
        try:
            cursor = None
            with sqlite3.connect(self.path) as connection:
                columns = tupleToSQL(columns)
                cursor = connection.cursor()
                cursor.execute(f'''
                    SELECT {columns}
                    FROM {tableName} {'' if where == '' else f'WHERE {where}'}
                ''')
            return cursor.fetchall()
        except sqlite3.Error as err:
            return err


# db3 = DB('./data', 'cse2')
# print("output : ", db3.readRows('student_details', ("enroll_num", "f_name","l_name")))
# print(db3.deleteTable(t1))
# print(db3.createTable(t1))
# print(db3.addCol(t1,'c1',0))
# print(db3.delCol(t1,'c2'))
