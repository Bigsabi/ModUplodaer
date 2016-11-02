import json
class Uploader(object):
    def __init__(self,Url,Name,Port):
        self.Url="www.bigcraft.cn"
        self.Name=Name
        self.Port=Port
    def A(self):
        return self.Url+self.Port
class Mods(object):
    def __init__(self,Path,MD5,Href,Ignore,Delete):
        self.Path = Path
        self.MD5 = MD5
        self.Href = Href
        self.Ignore = Ignore
        self.Delete = Delete
global UploaderConfig
fin = open('./Config.json')
a = json.load(fin)
if a.has_key('Url') is False:
    UploaderConfig = Uploader("www.bigcraft.cn",a['Name'],a['Port'])
else:
    UploaderConfig = Uploader(a['Url'],a['Name'],a['Port'])
fin.close()
print a