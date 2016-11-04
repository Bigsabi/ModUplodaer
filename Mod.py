#coding:utf-8
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