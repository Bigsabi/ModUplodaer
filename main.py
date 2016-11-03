#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
import json
import urllib
import urllib2
class Updater(object):
    def __init__(self,Url,Name,Port):
        self.Url=Url
        self.Name=Name
        self.Port=Port
    def FullAddress(self):
        return self.Url+":"+bytes(self.Port)+"/Mods.json"
#,Path,MD5,Href,Ignore,Delete
global UpdaterConfig
def ConvertUpdaterHook(parsed_dict):
    if parsed_dict.has_key("Url"):
        return Updater(parsed_dict['Url'],parsed_dict['Name'],parsed_dict['Port'])
    else:
        return Updater("www.bigcraft.cn",parsed_dict['Name'],parsed_dict['Port'])
class Mod(object):
    def __init__(self,Path,MD5,Href,Ignore,Delete):
        self.Path = Path
        self.MD5 = MD5
        self.Href = Href
        self.Ignore = Ignore
        self.Delete = Delete
def ConvertModHook(parsed_dict):
    return Mod(
        Path=parsed_dict['Path'],
        MD5=parsed_dict['MD5'],
        Href=parsed_dict['Href'],
        Ignore=parsed_dict['Ignore'],
        Delete=parsed_dict['Delete']
    )
configFile = open('./Config.json','r')
#读取Config文件
UpdaterConfig = json.load(configFile,object_hook=ConvertUpdaterHook)

# if a.has_key('Url') is False:
#     UploaderConfig = Uploader("www.bigcraft.cn",a['Name'],a['Port'])
# else:
#     UploaderConfig = Uploader(a['Url'],a['Name'],a['Port'])
req = urllib2.Request("http://www.bigcraft.cn:2333/Mods.json")
res_data = urllib2.urlopen(req)
res = res_data.read()
#html = urllib.urlopen("http://www.bigcraft.cn:2298/Mods.json")
#.replace("\r","").replace("\n","")
for jsonobject in json.loads(res,object_hook=ConvertModHook):
    print jsonobject
# b = json.JSONDecoder(object_hook=Uploader)

fin.close()
print a