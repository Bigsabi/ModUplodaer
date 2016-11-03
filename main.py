#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
import os
import json
import urllib
import urllib2

#更新器基础信息
class Updater(object):
    def __init__(self,Url,Name,Port):
        self.Url=Url
        self.Name=Name
        self.Port=Port
    def FullAddress(self):
        return self.Url+":"+bytes(self.Port)+"/Mods.json"
#更新器基础信息Hook
def ConvertUpdaterHook(parsed_dict):
    if parsed_dict.has_key("Url"):
        return Updater(parsed_dict['Url'],parsed_dict['Name'],parsed_dict['Port'])
    else:
        return Updater("http://www.bigcraft.cn",parsed_dict['Name'],parsed_dict['Port'])
def getFileMD5(filepath):
        if os.isdir(filepath):
            f = open(filepath,'rb')
            md5obj = hashlib.md5()
            md5obj.update(f.read())
            hash = md5obj.hexdigest()
            f.close()
            return str(hash).upper()
        return None
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
#基础信息
global UpdaterConfig
#Mod列表
global ServerMods
configFile = open('./Config.json','r')
#读取Config文件
UpdaterConfig = json.load(configFile,object_hook=ConvertUpdaterHook)
configFile.close()

#req = urllib2.Request("http://www.bigcraft.cn:2333/Mods.json")
req = urllib2.Request(UpdaterConfig.FullAddress())
res_data = urllib2.urlopen(req)
res = res_data.read()

#for C in json.loads(res,object_hook=ConvertModHook):
#    print C
#Mods = arr[0,100]
ServerMods = []
for jsonobject in json.loads(res,object_hook=ConvertModHook):
    ServerMods.append(jsonobject)

for fileInfo in os.listdir("./.minecraft/mods/"):
    print getFileMD5(".minecraft/mods/"+bytes(fileInfo))

print a