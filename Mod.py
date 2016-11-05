# -*- coding: utf-8 -*-
#coding:utf-8
import json
#Mod信息
class Mod(object):
    def __init__(self,Path,MD5,Href,Ignore,Delete):
        self.Path = Path
        self.MD5 = MD5
        self.Href = Href
        self.Ignore = Ignore
        self.Delete = Delete
#Mod信息Hook
def ConvertModHook(parsed_dict):
    return Mod(
        Path=parsed_dict['Path'],
        MD5=parsed_dict['MD5'],
        Href=parsed_dict['Href'],
        Ignore=parsed_dict['Ignore'],
        Delete=parsed_dict['Delete']
    )
# class PythonObjectEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
#             return JSONEncoder.default(self, obj)
#         return json.dumps(vars(obj),sort_keys=True, indent=4)

# def as_python_object(dct):
#     if '_python_object' in dct:
#         return pickle.loads(str(dct['_python_object']))
#     return dct