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
BranchID INTEGER PRIMARY KEY AUTOINCREMENT,
LineID INTEGER NOT NULL,
FromBusID INTEGER NOT NULL,
ToBusID INTEGER NOT NULL,
ckt VARCHAR(2),
BranchName VARCHAR(255),
FOREIGN KEY(LineID) REFERENCES line(LineID),
FOREIGN KEY(FromBusID) REFERENCES bus(BusID),
FOREIGN KEY(ToBusID) REFERENCES bus(BusID)
);

CREATE TABLE IF NOT EXISTS equipment (
EquipmentID INTEGER PRIMARY KEY,
BranchID INTEGER NOT NULL,
BusID INTEGER NOT NULL,
EquipmentName VARCHAR(255),
IsNew INTEGER,
FOREIGN KEY(BranchID) REFERENCES branch(BranchID),
FOREIGN KEY(BusID) REFERENCES bus(BusID)
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
INSERT INTO line (LineID, LineName)
VALUES (13, 'Grits - LtDan');
INSERT INTO line (LineID, LineName)
VALUES (14, 'LtDan - Forest');
INSERT INTO line (LineID, LineName)
VALUES (15, 'Forest - Tom');
INSERT INTO line (LineID, LineName)
VALUES (16, 'Tom - Hanks');

INSERT INTO branch (BranchID, LineID, FromBusID, ToBusID, ckt, BranchName)
VALUES (11, 11, 11, 12, '1',  'Bubba - Gump');
INSERT INTO branch (BranchID, LineID, FromBusID, ToBusID, ckt, BranchName)
VALUES (12, 11, 12, 13, '1',  'Gump - Shrimp');
INSERT INTO branch (BranchID, LineID, FromBusID, ToBusID, ckt, BranchName)
VALUES (13, 12, 13, 14, '1',  'Shrimp - Grits');

INSERT into equipment (EquipmentID, BranchID, BusID, EquipmentName, IsNew)
VALUES (1, 11, 11, 'Switch', 0);
INSERT into equipment (EquipmentID, BranchID, BusID, EquipmentName, IsNew)
VALUES (2, 11, 11, 'Breaker', 0);
INSERT into equipment (EquipmentID, BranchID, BusID, EquipmentName, IsNew)
VALUES (3, 11, 11, 'CT', 0);
INSERT into equipment (EquipmentID, BranchID, BusID, EquipmentName, IsNew)
VALUES (4, 11, 11, 'Wavetrap', 0);

INSERT into equipment (EquipmentID, BranchID, BusID, EquipmentName, IsNew)
VALUES (5, 11, 12, 'Switch', 0);
INSERT into equipment (EquipmentID, BranchID, BusID, EquipmentName, IsNew)
VALUES (6, 11, 12, 'Breaker', 0);
INSERT into equipment (EquipmentID, BranchID, BusID, EquipmentName, IsNew)
VALUES (7, 11, 12, 'CT', 0);
INSERT into equipment (EquipmentID, BranchID, BusID, EquipmentName, IsNew)
VALUES (8, 11, 12, 'Wavetrap', 0);
"""

for s in sql.split(';'):
    with conn:
        conn.execute(s)
