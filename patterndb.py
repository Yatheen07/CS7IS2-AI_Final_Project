import sqlite3
import util


def main():
    con = sqlite3.connect('cornerpattern.db')
    print("Creating corner pattern database");
    cusrsor = con.execute('CREATE TABLE CORNER_PATTERN(CORNERS VARCHAR2(100),VALUE INT)')
    print('Corner pattern Table created sucessfully')
    con = sqlite3.connect('edgepattern.db')
    print("Creating edge pattern database");
    cusrsor = con.execute('CREATE TABLE EDGE_PATTERN(EDGES VARCHAR2(100),VALUE INT)')
    print('Edge pattern Table created sucessfully')

if __name__ == '__main__':
    main()