#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict
import xml.etree.cElementTree as ET
import re
import tool


"""
 The tool module that there are some functions being used in the fileis
 created by myself!

 Firstly, parsing the xml, so that we can know the tags and the subtags
 with some infomation basically
"""

# choose the file to analysis
file_name_choose = input(
    "Please choose the file: \n 1: sample file 2: full file:\t")
if file_name_choose == "1":
    file_name = "data/shanghai_china.osm"
elif file_name_choose == "2":
    file_name = "originaldata/shanghai_china.osm"

# create a dict about the information of the all tags
all_tags_dict = tool.get_all_tags(file_name)
print("In the file all tags and the quantity are:")
print(all_tags_dict)

# create a dict about the information of the elementary tag after the root
tags_dict = tool.get_tags(file_name)
print("\nThe information about the elementary tags after the root:")
print(tags_dict)

sub_tags_dict = defaultdict(int)
for i in all_tags_dict.keys():
    if i in ["osm", "bounds"] or i in tags_dict.keys():
        continue
    else:
        sub_tags_dict[i] = all_tags_dict[i]
print("\nThe information about the sub tags behind the elementary tags:")
print(sub_tags_dict)

"""
 Now, I will get the information of the tags' attributes.Next, I want to analysis the
 keys about the tags, which I use two different tags.They are elementary tags,
 and the other one is secondary tags.
"""

with open(file_name, "r") as file:
    elements = ET.iterparse(file, events=("start", "end"))
    parent_attribute = tool.get_attr_dict(elements, tags=tags_dict)

with open(file_name, "r") as file:
    elements = ET.iterparse(file, events=("start", "end"))
    all_subattr_dict = tool.get_attr_dict(elements, tags=sub_tags_dict)

print("\nThe structure of the parent attribute is:")
print(parent_attribute)
print("\nThe structure of all children attribute is:")
print(all_subattr_dict)


"""
 Now, I know the parent tags and their attribute.So I want to get its children's
 tags and their attribute.The parent tags' structure is
 parent_attr = {'relation': {'timestamp', 'uid', 'changeset', 'version', 'id', 'user'},
        'node': {'lat', 'timestamp', 'lon', 'uid', 'changeset', 'version', 'id', 'user'},
        'way': {'timestamp', 'uid', 'changeset', 'version', 'id', 'user'}}
"""

with open(file_name, "r") as file:
    trees = ET.parse(file)
    root = trees.getroot()

    child_attr = dict()

    for element in root:
        if element.tag in parent_attribute:
            for child in element.getchildren():
                child_key = element.tag + "_child_" + child.tag

                for key in child.attrib.keys():
                    if child_key not in child_attr:
                        child_attr[child_key] = set()

                    child_attr[child_key].add(key)

    # push the parent attr to the all structure, then adding the children's attribute
    all_attr_struc = parent_attribute
    for child_key in child_attr:
        all_attr_struc[child_key] = child_attr[child_key]

print("\nThe attribute of the all element and their children is:")
print(all_attr_struc)

# it takes long time to run the code, so pause to run
if False:
    """
     I will parse the elements attribute and the unique value. So, this progress is audit
     the value.
    """

    # inital the variable contain the all tags, that is a dict

    all_value = dict()
    for key in all_attr_struc.keys():
        all_value[key] = dict()

        for attr_key in all_attr_struc[key]:
            all_value[key][attr_key] = set()

    with open(file_name, "r") as file:
        trees = ET.parse(file)
        root = trees.getroot()

        for element in root:
            if element.tag in parent_attribute.keys():
                parent_attr_value, child_attr_value = tool.get_attr_allvalues(
                    element, element.tag)

            # union the parent attribute and its value into  the variable all_value
                for key in parent_attr_value.keys():
                    all_value[element.tag][key] = all_value[element.tag][key].\
                        union(parent_attr_value[key])

            # union the child attribute and its value into the variable all_value
                for child_tag in child_attr_value:
                    for child_attr, attr_value in child_attr_value[child_tag].items():
                        all_value[child_tag][child_attr] = all_value[child_tag][child_attr].union(
                            attr_value)

"""
 Next, I pick up some tag to audit the value whether it's vilidate
"""
# create a set to store the value, which keeps unique
with open(file_name, "r") as file:
    street_name = defaultdict(set)
    postal_code = defaultdict(set)
    wikipedia = defaultdict(set)
    name_en = defaultdict(set)
    for _, element in ET.iterparse(file, events=("start",)):
        if element.tag == "tag":
            if tool.audit_attribute(element, "addr:street"):
                street_name["addr:street"].add(element.attrib["v"])
            if tool.audit_attribute(element, "addr:postcode"):
                postal_code["addr:postcode"].add(element.attrib["v"])
            if tool.audit_attribute(element, "wikipedia"):
                wikipedia["wikipedia"].add(element.attrib["v"])
        if element.tag in ["way", "node"]:
            for child in element.iter("tag"):
                if tool.audit_attribute(child, "name:en"):
                    name_en["name:en"].add(child.attrib["v"])

print("The head 20 street name is:\n")
pprint.pprint(list(street_name["addr:street"])[0:20])

print("The postal code is:\n")
pprint.pprint(postal_code)

print("The wikipedia is:\n")
pprint.pprint(wikipedia)

print("The head 20 english name is:\n")
pprint.pprint(list(name_en["name:en"])[0:20])


# just check the attribute k
check_out = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
with open(file_name, "r") as file:
    for _, element in ET.iterparse(file):
        if element.tag == "tag":
            tool.count_attr_type(element, "k", check_out)

print("The total of the attribute k in different type:\n")
pprint.pprint(check_out)


pattern = re.compile(
    r"(\S*\s+\([N|S|E|W]\)|Lib.|Rd|Lu|Rd.|Hwy.)$", re.IGNORECASE)
#     r"(Lib.|Rd|Lu|Rd.|\S[A-Z][a-z]*)$", re.IGNORECASE)
problem_name = []
done_name = []
for name in name_en["name:en"]:
    m = pattern.search(name)
    if m:
        problem_name.append(m.group())
        done_name.append(tool.update_vaue(name, pattern))

print("Before fixing the name:\n")
pprint.pprint(problem_name)

print("After fixing the name:\n")
pprint.pprint(done_name)


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
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, str) else v) for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def get_element(file_name, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

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
#     writeheader()
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
