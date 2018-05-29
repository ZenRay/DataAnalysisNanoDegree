#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
from sqlschema import schema
import pprint
import csv

limitation_tag = ["bounds", "osm"]  # exclude the meta tag
way_expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
                "Trail", "Parkway", "Commons"]

NODE_FIELDS = ["id", "lat", "lon", "user",
               "uid", "version", "changeset", "timestamp"]
NODE_TAGS_FIELDS = ["id", "key", "value", "type"]
WAY_FIELDS = ["id", "user", "uid", "version", "changeset", "timestamp"]
WAY_TAGS_FIELDS = ["id", "key", "value", "type"]
WAY_NODES_FIELDS = ["id", "node_id", "position"]
RELATION_FIELDS = ["id", "user", "uid", "version", "changeset", "timestamp"]
RELATION_TAGS_FIELDS = ["id", "key", "value", "type"]
RELATION_NODES_FIELDS = ["id", "node_id", "position"]
LOWER_COLON = re.compile(r'^([a-z]+):{1}([a-z]+:{0,1}[a-z]*)+')
# re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# parent_attr = {'relation': {'timestamp', 'uid', 'changeset', 'version', 'id', 'user'},
#                'node': {'lat', 'timestamp', 'lon', 'uid', 'changeset', 'version', 'id', 'user'},
#                'way': {'timestamp', 'uid', 'changeset', 'version', 'id', 'user'}}

mapping = {"Rd.": "Road", "Hwy.": "Highway", "Lu": "Road", "Rd. (S)": "Road South",
           "Lib.": "Library", "Rd": "Road", "lu": "Road", "Rd. (N)": "Road North",
           "Rd. (W)": "Road West", "Rd. (E)": "Road East", "rd": "Road"}


def get_tags(file_name, limitation_tag=limitation_tag):
    """
    Get the information about the elememantary tag behind the root!

    There are limitation tags that I want exclude the tags. Because
    the tags just are meta tags to describe the file.

    The result is a dict. The key is the tag, and the value is a
    number of the tag.
    """
    with open(file_name, "r") as file:
        tags_dict = defaultdict(int)  # the information of elementary tag

        trees = ET.parse(file)
        root = trees.getroot()

        for element in root:
            if element.tag in limitation_tag:
                continue
            tags_dict[element.tag] += 1
    return tags_dict


def get_all_tags(file_name):
    """
    Get the information about the all tags!

    I parse the file use the function iterparse, which iter the element.
    And I want to print the meta information, in this function.

    The result is a dict. The key is the tag, and the value is a
    number of the tag.
    """
    with open(file_name, "r") as file:
        all_tags_dict = defaultdict(int)  # all tags and count number

        tree = ET.iterparse(file, events=("start", "end"))
        for event, element in tree:
            if element.tag in all_tags_dict:
                all_tags_dict[element.tag] += 1
            else:
                all_tags_dict[element.tag] = 1
            if False:  # Don`t print the meta information
                print("the meta infomation of the bounds tag and the osm tag")
                if event == "start":
                    if element.tag == "bounds":
                        print("\nThe boundary about %s zone:" % "ShangHai")
                        print("The min latitue is {0}; the min longitude is {1}; \
                            the max latitue is {2}; the max longitude is {3}".format(
                            element.attrib["minlat"], element.attrib["minlon"],
                            element.attrib["maxlat"], element.attrib["maxlon"]))

                    if element.tag == "osm":
                        print("\nThe meta information about the file:")
                        print("The OSM version is %s, and the timestamp is %s" %
                              (element.attrib["version"], element.attrib["timestamp"]))
    return all_tags_dict


def get_attr_set(element):
    """
    Get the keys about the element!

    This function is called, which can get the set about the attribute
    of the element.

    The result is a set. The value is the attribute of the tag, in the set.
    """

    attr_set = set()
    for key in element.attrib.keys():
        attr_set.add(key)
    return attr_set


def get_attr_dict(elements, tags: dict = dict()) -> dict:
    """
    Get the attributes about all the element contain the tags' attribute!
    This function is called,which can get the sets about the fixed
    tag. So, I can specify the special tags. I will use the parameter
    tags which can be specitied the fixed tag.
    The result is a dict. The key is the special tag and the value is
    a set about the tags' keys.
    """

    # initial the result variable, and push the specify the key of
    # the specified tags'attribute into the variable
    attr_dict = dict()

    for key in tags.keys():
        attr_dict[key] = set()

    for event, element in elements:
        if event == "start":
            if element.tag in attr_dict:
                attr_dict[element.tag] = get_attr_set(
                    element).union(attr_dict[element.tag])

    return attr_dict


def get_attr_value(element):
    """
    Get the value about the tag's attribute!

    This function is called, which can parse the element like
    key=value in the fixed tag.

    The result is a dict.The value is a dict about the tag's
    keys and its value; and the result's key is the tag.
    """
    keys_value = dict()  # element's key : key's value
    for key in element.attrib.keys():
        keys_value[key] = set()
        keys_value[key].add(element.attrib[key])
    return keys_value


def get_attr_allvalues(element, tag: "elementary tag"):
    """
    Get the alue about the element's attribute and the childs' attribute!

    This function is called, which can parse the fixed element's attribute,
    next step I parset the fixed element's child elements' attribute.The
    parameter of parent tag is fixed elementary tag.

    The result is a dict. The keys are the parents' tag and the childs' tag,
    and the value is a set contain the attibutes' value of the tags.
    """
    if element.tag == tag:
        # the parent attribute value can parse directly
        parent_attr_value = get_attr_value(element)

        # the childrens' atrribute must iter in the children, so create a
        # nested dict
        child_attr_value = dict()
        for child in element.getchildren():
            child_key = element.tag + "_child_" + child.tag
            child_attr_value[child_key] = dict()

            # parse the child's attribute
            child_value = get_attr_value(child)

            # union the child's attribute value, and need to
            # create set for every child attribute
            for key in child_value.keys():
                if key not in child_attr_value[child_key]:
                    child_attr_value[child_key][key] = set()

                child_attr_value[child_key][key] = child_attr_value[child_key][key].union(
                    child_value[key])
        return parent_attr_value, child_attr_value


def count_attr_type(element, attribute, check_out: "out function dict"):
    """
    count the different type of attribute.

    There are three type of regular pattern.The attribute is k or v.

    return the dict
    """
    # setup the regular pattern
    lower = re.compile(r'^([a-z]|_)*$')
    lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
    problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

    if element.tag == "tag":
        tag = 0
    if lower.search(element.attrib[attribute]):
        check_out["lower"] += 1
        tag = 1
    elif lower_colon.search(element.attrib[attribute]):
        check_out["lower_colon"] += 1
        tag = 1
    elif problemchars.search(element.attrib[attribute]):
        check_out["problemchars"] += 1
        tag = 1

    if tag == 0:
        check_out["other"] += 1
    return check_out


def audit_attribute(element, attribute):
    """
    Check the value the attribute in the element!

    The attribute value can choose k or v

    The result is boolen value
    """
    return attribute == element.attrib["k"]


def update_vaue(name, pattern, mapping=mapping):
    """
    Update the invalidate value!

    Return the validate value
    """
    pattern_value = pattern.search(name).group()
    name = name.replace(pattern_value, mapping[pattern_value])
    return name


def inital_csvs(element, node_attr_fileds=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                problem_chars=PROBLEMCHARS, default_tag_type="regular"):
    """
    Deal with the different tag by using different way!

    Fisrt part, it deals with the node tag. The rest deals with the
    way tag or the relation tag.

    The result is a dict.
    """

    # node_attribs = {}
    # if element.tag == "node":
    #     tags = []
    #     for nodekey in NODE_FIELDS:
    #         if nodekey in element.attrib:
    #             node_attribs[nodekey] = element.attrib[nodekey]
    #         node_attribs["id"] = node_attribs["id"]
    #     for child in element.findall("tag"):
    #         tags_dict = {}  # create the dict about the tag attribtue

    #         if PROBLEMCHARS.search(child.attrib["k"]):
    #             continue
    #         elif LOWER_COLON.search(child.attrib["k"]):
    #             tags_dict["type"] = LOWER_COLON.search(
    #                 child.attrib["k"].group(1))
    #             tags_dict["key"] = LOWER_COLON.search(
    #                 child.attrib["k"].group(1))
    #             tags_dict["value"] = child.attrib["v"]
    #             tags_dict["id"] = node_attribs["id"]
    #         else:
    #             tags_dict["type"] = default_tag_type
    #             tags_dict["key"] = child.attrib["k"]
    #             tags_dict["value"] = child.attrib["v"]
    #             tags_dict["id"] = node_attribs["id"]
    #         tags.append(tags_dict)

    #     return {"node": node_attribs, "node_tag": tags}
    # elif element.tag in ["way", "relaiton"]:
    #     return initial_csv(element)

    node_attribs = {}
    way_attribs = {}

    # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    if element.tag == 'node':
        tags = []
        for nodekey in NODE_FIELDS:
            if nodekey in element.attrib:
                node_attribs[nodekey] = element.attrib[nodekey]
        for child in element.findall("tag"):
            tagdict = {}
            if PROBLEMCHARS.search(child.attrib["k"]):
                continue
            elif LOWER_COLON.search(child.attrib["k"]):
                # print child.attrib["k"]
                tagdict["type"] = LOWER_COLON.search(
                    child.attrib["k"]).group(1)
                tagdict["key"] = LOWER_COLON.search(child.attrib["k"]).group(2)
                tagdict["value"] = child.attrib["v"]
                tagdict["id"] = node_attribs["id"]
            else:
                tagdict["type"] = default_tag_type
                tagdict["key"] = child.attrib["k"]
                tagdict["value"] = child.attrib["v"]
                tagdict["id"] = node_attribs["id"]
            tags.append(tagdict)
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        tags = []
        way_nodes = []
        for waykey in WAY_FIELDS:
            if waykey in element.attrib:
                way_attribs[waykey] = element.attrib[waykey]
        for child in element.iterfind("tag"):
            tagdict = {}
            if PROBLEMCHARS.search(child.attrib["k"]):
                continue
            elif LOWER_COLON.search(child.attrib["k"]):
                # tagdict = {}
                tagdict["type"] = LOWER_COLON.search(
                    child.attrib["k"]).group(1)
                tagdict["key"] = LOWER_COLON.search(child.attrib["k"]).group(2)
                tagdict["value"] = child.attrib["v"]
                tagdict["id"] = way_attribs["id"]
                # tags.append(tagdict)
            else:
                # tagdict = {}
                tagdict["type"] = default_tag_type
                tagdict["key"] = child.attrib["k"]
                tagdict["value"] = child.attrib["v"]
                tagdict["id"] = way_attribs["id"]
                # tags.append(tagdict)
            tags.append(tagdict)

        childlocationindex = 0
        for child in element.findall("nd"):
            waydict = {}
            waydict["id"] = way_attribs["id"]
            waydict["node_id"] = child.attrib["ref"]
            waydict["position"] = childlocationindex
            childlocationindex += 1
            way_nodes.append(waydict)
        # print tags
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


def initial_csv(element, tags=["way", "relaiton"], attr_fields=WAY_FIELDS,
                problem_chars=PROBLEMCHARS, default_tag_type="regular"):
    """
    Just deal with the wey tag and the relation tag"
    """
    tag_attribs = {}
    if element.tag in tags:
        tags = []
        tag_nodes = []
        for parent_key in WAY_FIELDS:
            if parent_key in element.attrib:
                tag_attribs[parent_key] = element.attrib[parent_key]
            tag_attribs["id"] = int(tag_attribs["id"])
            ag_attribs["uid"] = int(tag_attribs["uid"])
            ag_attribs["changeset"] = int(tag_attribs["changeset"])

        for child in element.iterfind("tag"):
            tagdict = {}
            if PROBLEMCHARS.search(child.attrib["k"]):
                continue
            elif LOWER_COLON.search(child.attrib["k"]):
                tagdict["type"] = LOWER_COLON.search(
                    child.attrib["k"]).group(1)
                tagdict["key"] = LOWER_COLON.search(child.attrib["k"]).group(2)
                tagdict["value"] = child.attrib["v"]
                tagdict["id"] = tag_attribs["id"]
            else:
                tagdict["type"] = default_tag_type
                tagdict["key"] = child.attrib["k"]
                tagdict["value"] = child.attrib["v"]
                tagdict["id"] = tag_attribs["id"]
            tags.append(tagdict)

        childlocationindex = 0
        for child in element.findall("nd"):
            waydict = {}
            waydict["id"] = tag_attribs["id"]
            waydict["node_id"] = int(child.attrib["ref"])
            waydict["position"] = childlocationindex
            childlocationindex += 1
            tag_nodes.append(waydict)

        return {(element.tag): tag_attribs,
                (element.tag + '_nodes'): tag_nodes,
                (element.tag + '_tags'): tags}


def validate_element(element, validator, schema=schema):
    """
    check the element whether match schema!

    raise the invalidate element
    """
    if validator.validate(element, schema) is not True:
        for filed, errors in validator.errors.items():
            message = "\nElement of type '{0}' has the following errors: \n{1}"
            error_string = pprint.pformat(errors)
            raise Exception(message.format(filed, error_string))

# create the csv file and write the data into the file. The code is used in the
# udacity class


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
