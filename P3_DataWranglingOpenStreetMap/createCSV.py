#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import csv
import cerberus
import codecs
import tool
"""
When create the csv file ,use this file.
The path is at result directory.
"""

file_name = "data/shanghai_china.osm"

NODES_PATH = "result/nodes.csv"
NODE_TAGS_PATH = "result/nodes_tags.csv"
WAYS_PATH = "result/ways.csv"
WAY_NODES_PATH = "result/ways_nodes.csv"
WAY_TAGS_PATH = "result/ways_tags.csv"
NODE_FIELDS = ['id', 'lat', 'lon', 'user',
               'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


class UnicodeDictWriter(csv.DictWriter, object):
    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, str) else v) for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def get_element(file_name, tags=('node', 'way', 'relation')):

    context = ET.iterparse(file_name, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with codecs.open(NODES_PATH, 'w') as nodes_file, \
        codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
        codecs.open(WAYS_PATH, 'w') as ways_file, \
        codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
        codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

    nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
    node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
    ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
    way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
    way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

    nodes_writer.writeheader()
    node_tags_writer.writeheader()
    ways_writer.writeheader()
    way_nodes_writer.writeheader()
    way_tags_writer.writeheader()

    validator = cerberus.Validator()

    for element in get_element(file_name, tags=("node", "way")):
        el = tool.inital_csvs(element)
        print(el)
        if el:
            tool.validate_element(el, validator)
        if element.tag == "node":
            nodes_writer.writerow(el['node'])
            node_tags_writer.writerows(el['node_tags'])
        elif element.tag == 'way':
            ways_writer.writerow(el['way'])
            way_nodes_writer.writerows(el['way_nodes'])
            way_tags_writer.writerows(el['way_tags'])
