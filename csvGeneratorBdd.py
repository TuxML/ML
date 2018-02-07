#!/usr/bin/python3

import irmaDBCredentials
import MySQLdb
import os
import re

def getNameAndValue(line):
    i = 0
    if len(line) == 0 or line[i] == '#':return ("","")
    # get property name
    name = ""
    while i < len(line):
        if line[i] == '=': break
        name += line[i]
        i+=1
    if len(name) == 0 or name == '\n': return ("","")
    # get value name
    value = ""
    i+=1
    while i < len(line): 
        value += line[i]
        i+=1
    return (name, value)

def getPropertiesNames(allyesconfig, numProperties):
    properties = {"KERNEL_SIZE":["-1"]*numProperties, "COMPILE_TIME":["-1"]*numProperties}

    # Extract all property names
    allyes = open(allyesconfig, "r")
    for line in allyes:
        name, value = getNameAndValue(line)
        if name=="": continue
        properties[name] = ['n']*numProperties

    return properties

def fillProperties(properties, numProperties, results):
    for number, (config_file, core_size, compilation_time) in enumerate(results):
        properties["KERNEL_SIZE"][number] = str(core_size)
        properties["COMPILE_TIME"][number] = str(compilation_time)

        for line in config_file.splitlines():
            name, value = getNameAndValue(line)
            if name=="": continue
            if name not in properties:
                properties[name] = ['n']*numProperties

            properties[name][number] = value

    return properties


def getFromDB():
    try:
        conn = MySQLdb.connect(**irmaDBCredentials.info)
        cursor = conn.cursor()

        # Get all .configs that successfully compiled
        query = ("SELECT config_file, core_size, compilation_time FROM TuxML WHERE compilation_time > -1")

        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

    except MySQLdb.Error as err:
        print("Error : Can't read from db : {}".format(err.args[1]))
        exit(-1)
    finally:
        conn.close()

    return results

def printCSV(numProperties, properties):
    keys_line = ""
    value_lines = [""]*numProperties
    for (k,v) in properties.items():
        keys_line += k + ","
        for i in range(numProperties):
            value_lines[i] += v[i] + ","

    print(keys_line)
    for line in value_lines:
        print(line)


if __name__ == "__main__":
    results = getFromDB()
    numProperties = len(results)
    properties = getPropertiesNames("allyes.config", numProperties)
    properties = fillProperties(properties, numProperties, results)
    printCSV(numProperties, properties)
