from lib2to3.pgen2.token import NUMBER
import sqlite3

con = sqlite3.connect('cornerpattern.db')
print("Creating pattern database");

cusrsor = con.execute('CREATE TABLE CORNER_PATTERN(CORNERS VARCHAR2(100),VALUE INT)')
print('Table created sucessfully')