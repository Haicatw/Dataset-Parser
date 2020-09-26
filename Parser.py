from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import csv
import re

vectorPattern = re.compile(r"(\[|\()(.*)(\]|\))")


class Parser:
    def __init__(
        self, vertexFilePath, vertexMetaPath, edgeFilePath, edgeMetaPath
    ):
        # columnNames, rawData, alies, typeInfo
        (
            self.vertexNameList,
            self.rawVertexDf,
            self.vertexAlies,
            self.vertexTypes,
        ) = get_data(vertexFilePath, vertexMetaPath)
        (
            self.edgeNameList,
            self.rawEdgeDf,
            self.edgeAlies,
            self.edgeTypes,
        ) = get_data(edgeFilePath, edgeMetaPath)
        print(self.rawVertexDf)

    def getTypes(self, indicator):
        if indicator == 0:
            return self.vertexTypes
        return self.edgeTypes

    def getMeta(self, indicator):
        if indicator == 0:
            return [
                self.vertexNameList,
                self.vertexAlies,
                self.vertexTypes,
            ]
        return [
            self.edgeNameList,
            self.edgeAlies,
            self.edgeTypes,
        ]


def get_data(filePath, metaFilePath, unknownValue=""):
    rawData = {}
    columnNames, processedGraphData, alies, typeInfo = parse_file(
        filePath, metaFilePath, unknownValue
    )
    for field in columnNames:
        rawData[field] = []

    for row in processedGraphData:
        for field in row:
            rawData[field].append(row[field])

    return [columnNames, rawData, alies, typeInfo]


def parse_file(filePath, metaFilePath, unknownValue=""):
    reader = csv.DictReader(open(filePath))
    fields = reader.fieldnames
    reader = csv.DictReader(open(filePath), fieldnames=fields)
    next(reader)
    columnNames, alies, typeInfo = parse_meta(metaFilePath)
    processedGraphData = []
    for row in reader:
        tempDict = {}
        for field in row:
            if row[field] == unknownValue:
                tempDict[field] = None
            else:
                tempDict[field] = caster(row[field], typeInfo[field])
        processedGraphData.append(tempDict)
    return [columnNames, processedGraphData, alies, typeInfo]


def parse_meta(metaFilePath):
    reader = csv.DictReader(open(metaFilePath))
    fields = reader.fieldnames
    reader = csv.DictReader(open(metaFilePath), fieldnames=fields)
    typeInfo = None
    alies = None
    columnNames = None
    for row in reader:
        if columnNames == None:
            columnNames = row
        elif typeInfo == None:
            typeInfo = row
        elif alies == None:
            alies = row
    return [columnNames, alies, typeInfo]


def vector_parser(rawStr):
    tempMatch = vectorPattern.findall(rawStr)
    try:
        return tempMatch[0][1].split(",")
    except IndexError:
        return [rawStr]


def caster(rawVal, userType):
    print(rawVal, userType)
    if rawVal == "":
        return rawVal
    if userType == "bool":
        try:
            rawVal = int(rawVal)
            if rawVal == 0:
                return False
            else:
                return True
        except ValueError:
            try:
                return bool(rawVal)
            except NameError:
                if rawVal == "true":
                    return True
                else:
                    return False
    elif userType == "int":
        try:
            return int(rawVal)
        except:
            return int(float(rawVal))
    elif userType == "float":
        return float(rawVal)
    elif userType == "string":
        return rawVal.strip("'\" ")
    elif userType == "list of bool":
        rawList = vector_parser(rawVal)
        processedList = []
        for val in rawList:
            processedList.append(caster(val.strip("'\" "), "bool"))
        return processedList
    elif userType == "list of int":
        rawList = vector_parser(rawVal)
        processedList = []
        for val in rawList:
            processedList.append(caster(val.strip("'\" "), "int"))
        return processedList
    elif userType == "list of float":
        rawList = vector_parser(rawVal)
        processedList = []
        for val in rawList:
            processedList.append(caster(val.strip("'\" "), "float"))
        return processedList
    elif userType == "list of string":
        rawList = vector_parser(rawVal)
        processedList = []
        if isinstance(rawList, str):
            processedList.append(rawList)
        else:
            for val in rawList:
                processedList.append(caster(val.strip("'\" "), "string"))
        return processedList
    elif userType == "custom":
        try:
            return eval(rawVal)
        except:
            return rawVal
