"""
Make an example database.  
"""
import sqlite3
conn = sqlite3.connect('example.sqlite')

conn.execute("""\
CREATE TABLE IF NOT EXISTS bus (
BusID INTEGER PRIMARY KEY,
BusNum INTEGER,
BusName VARCHAR(255)
);
""")

conn.execute("""\
CREATE TABLE IF NOT EXISTS branch (
BranchID INTEGER PRIMARY KEY,
LineID INTEGER,
FromBusID INTEGER,
ToBusID INTEGER,
ckt VARCHAR(2),
BranchName VARCHAR(255),
FOREIGN KEY (FromBusID) REFERENCES bus(BusID),
FOREIGN KEY (ToBusID) REFERENCES bus(BusID),
FOREIGN KEY (LineID) REFERENCES line(LineID)
);
""")

conn.execute("""\
CREATE TABLE IF NOT EXISTS line (
LineID INTEGER PRIMARY KEY,
LineName VARCHAR(255)
);
""")

sql = """
INSERT INTO bus(BusID, BusNum, BusName)
VALUES (1, 101, 'Bubba');
INSERT INTO bus(BusID, BusNum, BusName)
VALUES (2, 102, 'Gump');
INSERT INTO bus(BusID, BusNum, BusName)
VALUES (3, 103, 'Shrimp');
INSERT INTO bus(BusID, BusNum, BusName)
VALUES (4, 104, 'Grits');

INSERT INTO line (LineID, LineName)
VALUES (1, 'Bubba - Shrimp');
INSERT INTO line (LineID, LineName)
VALUES (2, 'Shrimp - Grits');

INSERT INTO branch (BranchID, LineID, FromBusID, ToBusID, ckt, BranchName)
VALUES (1, 1, 1, 2, '1',  'Bubba - Gump');
INSERT INTO branch (BranchID, LineID, FromBusID, ToBusID, ckt, BranchName)
VALUES (2, 1, 2, 3, '1',  'Gump - Shrimp');
INSERT INTO branch (BranchID, LineID, FromBusID, ToBusID, ckt, BranchName)
VALUES (3, 2, 3, 4, '1',  'Shrimp - Grits');
"""

for s in sql.split(';'):
    with conn:
        conn.execute(s)
