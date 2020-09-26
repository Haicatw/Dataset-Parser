# Dataset Parser

## Introduction
---------------
This script takes care of parsing the dataset following standard decribed in dataset specification section. It will parse and cast data into desired types and preserve given metadata.

## Requirements
---------------
No third party module is reqired.

## Dataset Specification
------------------------
The dataset should be in csv format and separated into four files, including original data of vertex and edge as well as metadata of vertex and edge.

### Example:
- Original Data Format
  ```
  column_name1, column_name2, column_name3, ...
  data1, data2, data3, ...
  ...
  ```

- Metadata Data Format
  ```
  column_name1, column_name2, column_name3, ...
  type_name_1, type_name_2, type_name_3, ...
  name_alias1, name_alias2, name_alias3, ...
  ```

### Type Specification and Corresponding Types
| Dataset Type   | Python Type | Graph-Tool Type | Numpy Type | SQL Type |
| -------------- | ----------- | --------------- | ---------- | -------- |
| bool           | bool        | bool            | bool       | BOOLEAN  |
| int            | int         | int             | int64      | INT      |
| float          | float       | float           | float64    | DOUBLE   |
| string         | string      | string          | object     | TEXT     |
| list of bool   | python list | vector\<bool>   | object     | JSON     |
| list of int    | python list | vector\<int>    | object     | JSON     |
| list of float  | python list | vector\<float>  | object     | JSON     |
| list of string | python list | vector\<string> | object     | JSON     |
| custom         | object      | object          | object     | JSON     |

- Users should use dataset type names as the indicator for types.
- **custom** type should be strictly in JSON object format, and it should be used as few as possible.
- The parser only converts dataset data to python types. Other casting needs implementation.
- For **list** types, the raw data in dataset should be wrapped in [ ] or ( )

## Interface
------------
A parser class is provided.
### Constructor
```
myParser = Parser(vertexFilePath, vertexMetaPath, edgeFilePath, edgeMetaPath)
```
### Parsed Data
Direct access to the internal data structure is exposed to users.
```
myParser.vertexNameList,
myParser.rawVertexDf,
myParser.vertexAlies,
myParser.vertexTypes,
myParser.edgeNameList,
myParser.rawEdgeDf,
myParser.edgeAlies,
myParser.edgeTypes
```