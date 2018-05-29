#!/usr/bin/python
# -*- coding utf-8 -*-

import sqlite3
import csv


dbfile = "result/shanghai.db"  # create database variable
files = ["nodes.csv", "nodes_tags.csv",
         "ways.csv", "ways_nodes.csv", "ways_tags.csv"]  # create a list for files


# initialdb.close()
connetcion = sqlite3.connect(dbfile)
connetcion.text_factory = str
cursor = connetcion.cursor()

tables = ["nodes", "nodestags", "ways", "waysnodes", "waystags"]
for table in tables:
    cursor.execute("DROP TABLE IF EXISTS %s" % table)

# create the table schema
node_schema = """
CREATE TABLE nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT
);
"""

nodetags_schema = """
CREATE TABLE nodestags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
);
"""

way_schema = """
CREATE TABLE ways(
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
);
"""

waytags_schema = """
CREATE TABLE waystags(
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
);
"""

waynodes_schema = """
CREATE TABLE waysnodes(
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);
"""
schemas = [node_schema, nodetags_schema,
           way_schema, waynodes_schema, waytags_schema]

files = ["nodes.csv", "nodes_tags.csv",
         "ways.csv", "ways_nodes.csv", "ways_tags.csv"]
for schema, file in zip(schemas, files):
    cursor.execute(schema)
    if file == "nodes.csv":
        with open("result/" + file, "r", encoding="utf-8") as data:
            csvdata = csv.DictReader(data)
            for row in csvdata:
                # print(row.keys())
                id_value = int(row["id"])
                lat_value = float(row["lat"])
                lon_value = float(row["lon"])
                user_value = str(row["user"])
                uid_value = int(row["uid"])
                version_value = str(row["version"])
                changeset_value = int(row["changeset"])
                timestamp_value = str(row["timestamp"])

                cursor.execute('INSERT INTO nodes VALUES (?,?,?,?,?,?,?,?)',
                               (id_value, lat_value, lon_value, user_value,
                                uid_value, version_value, changeset_value, timestamp_value))
        print("The file {} is written in the database {}".format(file, dbfile))

    if file == "nodes_tags.csv":
        with open("result/" + file, "r", encoding="utf-8") as data:
            csvdata = csv.DictReader(data)
            for row in csvdata:
                # print(row["id"])
                id_value = int(row["id"])
                key_value = str(row["key"])
                value_value = str(row["value"])
                type_value = str(row["type"])

                cursor.execute('INSERT INTO nodestags VALUES (?,?,?,?)',
                               (id_value, key_value, value_value, type_value))
        print("The file {} is written in the database {}".format(file, dbfile))

    if file == "ways.csv":
        with open("result/" + file, "r", encoding="utf-8") as data:
            csvdata = csv.DictReader(data)
            for row in csvdata:
                id_value = int(row["id"])
                user_value = str(row["user"])
                uid_value = int(row["uid"])
                version_value = str(row["version"])
                changeset_value = int(row["changeset"])
                timestamp_value = str(row["timestamp"])

                cursor.execute('INSERT INTO ways VALUES (?,?,?,?,?,?)',
                               (id_value, user_value, uid_value, version_value,
                                changeset_value, timestamp_value))
        print("The file {} is written in the database {}".format(file, dbfile))

    if file == "ways_nodes.csv":
        with open("result/" + file, "r", encoding="utf-8") as data:
            csvdata = csv.DictReader(data)
            for row in csvdata:
                id_value = int(row["id"])
                node_id_value = str(row["node_id"])
                position_value = str(row["position"])

                cursor.execute('INSERT INTO waysnodes VALUES (?,?,?)',
                               (id_value, node_id_value, position_value))
        print("The file {} is written in the database {}".format(file, dbfile))

    if file == "ways_tags.csv":
        with open("result/" + file, "r", encoding="utf-8") as data:
            csvdata = csv.DictReader(data)
            for row in csvdata:
                id_value = int(row["id"])
                key_value = str(row["key"])
                value_value = str(row["value"])
                type_value = str(row["type"])

                cursor.execute('INSERT INTO waystags VALUES (?,?,?,?)',
                               (id_value, key_value, value_value, type_value))

        print("The file {} is written in the database {}".format(file, dbfile))
connetcion.commit()
