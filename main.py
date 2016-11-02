import json
import urllib
import urllib2
class Uploader(object):
    def __init__(self,Url,Name,Port):
        self.Url="http://www.bigcraft.cn"
        self.Name=Name
        self.Port=Port
        self.FullAddress=self.Url+":"+bytes(self.Port)+"/Mods.json"
#,Path,MD5,Href,Ignore,Delete        
class Mod(object):
    Path=""
    MD5=""
    Href=""
    Ignore=""
    Delete=""
    # def __init__(self):
    #     self.Path = Path
    #     self.MD5 = MD5
    #     self.Href = Href
    #     self.Ignore = Ignore
    #     self.Delete = Delete
global UploaderConfig
fin = open('./Config.json')
#读取Config文件
a = json.load(fin)
if a.has_key('Url') is False:
    UploaderConfig = Uploader("www.bigcraft.cn",a['Name'],a['Port'])
else:
    UploaderConfig = Uploader(a['Url'],a['Name'],a['Port'])
req = urllib2.Request("http://www.bigcraft.cn:2333/Mods.json")
res_data = urllib2.urlopen(req)
res = res_data.read()
#html = urllib.urlopen("http://www.bigcraft.cn:2298/Mods.json")
#.replace("\r","").replace("\n","")
datastr = json.loads(res.replace("\r","").replace("\n",""),Mod)
# b = json.JSONDecoder(object_hook=Uploader)

fin.close()
print a