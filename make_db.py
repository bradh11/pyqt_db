"""
Make an example database.  

Remember the FOREIGN KEY constraints are only enforced if the 'PRAGMA foreign_keys;' is run on every
connection.
"""
import sqlite3
import os
import os.path as osp

db = 'example.sqlite'
if osp.exists(db):
    os.remove(db)
conn = sqlite3.connect(db)

sql = """\
CREATE TABLE IF NOT EXISTS bus (
BusID INTEGER PRIMARY KEY,
BusNum INTEGER,
BusName VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS line (
LineID INTEGER PRIMARY KEY,
LineName VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS branch (
BranchID INTEGER PRIMARY KEY,
LineID INTEGER NOT NULL,
FromBusID INTEGER NOT NULL,
ToBusID INTEGER NOT NULL,
ckt VARCHAR(2),
BranchName VARCHAR(255),
FOREIGN KEY(LineID) REFERENCES line(LineID),
FOREIGN KEY(FromBusID) REFERENCES bus(BusID),
FOREIGN KEY(ToBusID) REFERENCES bus(BusID)
);

PRAGMA foreign_keys = ON;

INSERT INTO bus(BusID, BusNum, BusName)
VALUES (11, 1001, 'Bubba');
INSERT INTO bus(BusID, BusNum, BusName)
VALUES (12, 1002, 'Gump');
INSERT INTO bus(BusID, BusNum, BusName)
VALUES (13, 1003, 'Shrimp');
INSERT INTO bus(BusID, BusNum, BusName)
VALUES (14, 1004, 'Grits');

INSERT INTO line (LineID, LineName)
VALUES (11, 'Bubba - Shrimp');
INSERT INTO line (LineID, LineName)
VALUES (12, 'Shrimp - Grits');

INSERT INTO branch (BranchID, LineID, FromBusID, ToBusID, ckt, BranchName)
VALUES (11, 11, 11, 12, '1',  'Bubba - Gump');
INSERT INTO branch (BranchID, LineID, FromBusID, ToBusID, ckt, BranchName)
VALUES (12, 11, 12, 13, '1',  'Gump - Shrimp');
INSERT INTO branch (BranchID, LineID, FromBusID, ToBusID, ckt, BranchName)
VALUES (13, 12, 13, 14, '1',  'Shrimp - Grits');
"""

for s in sql.split(';'):
    with conn:
        conn.execute(s)
