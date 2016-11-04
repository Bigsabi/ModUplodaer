#coding:utf-8
import os
import hashlib
import Mod
def Schedule(a,b,c):
    # a:已经下载的数据块
    # b:数据块的大小
    # c:远程文件的大小
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print '%.2f%%' % per
def appendModInfo(LocalMods):
    appendModInfoByPath("./.minecraft/mods/",LocalMods)
    #appendModInfoByPath("./.minecraft/mods/")
#获取指定路径下所有文件MD5
def appendModInfoByPath(filepath,LocalMods):
    for filePath in os.listdir(filepath):
        if os.path.isdir(filepath+filePath) is False:
            f = open(filepath+filePath,'rb')
            md5obj = hashlib.md5()
            md5obj.update(f.read())
            hash = md5obj.hexdigest()
            f.close()
            LocalMods.append(Mod.Mod(filepath+filePath,str(hash).upper(),"",False,False))
        else:
            appendModInfoByPath(filepath+filePath+"/",LocalMods)