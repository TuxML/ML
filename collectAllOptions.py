#!/usr/bin/python3

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

def getPropertiesNames(allyesconfig):
    # Extract all property names
    properties = []
    allyes = open(allyesconfig, "r")
    for line in allyes:
        name, value = getNameAndValue(line)
        if name=="": continue
        properties.append(name)

    return properties

def collectAllConfigOptions():
    config_folder = "configs/"
    config_files = os.listdir(config_folder)
    file_count = len(config_files)

    configs = []
    for file_number, config_file in enumerate(config_files):
        config_properties = []
        config_content = open(config_folder + config_file, "r")
        # Config properties
        for line in config_content:
            name, value = getNameAndValue(line)
            if name=="": continue
            config_properties.append(name)
        configs.append(config_properties) 
    return configs


if __name__ == "__main__":
    properties = getPropertiesNames("allyes.config")
    print("properties" , properties)
    print("properties" , len(properties))
    allConfigOptions = collectAllConfigOptions()
    print(len(allConfigOptions))
    missingOptions = []
    i = 0
    for config in allConfigOptions:
        i = i + 1
        print("config... ", i)
        for option in config:
            if option not in properties:
                missingOptions.append(option)
    print ("options missing in allyes ",  len(missingOptions))
    print ("options missing in allyes ",  missingOptions)
    
