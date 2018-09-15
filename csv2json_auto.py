#!/usr/bin/python
#coding:utf-8
import csv,glob,os,json,shutil
cnf={}

def fmtCnf ():
    global cnf
    _input = raw_input(u"输入要转换的文件(不输入为全部文件):".encode("gbk"))
    if len(_input)==0:
        _input = "*"
    jsonfile = glob.glob('csv/%s.cnf' % _input)
    for f in jsonfile:
        print 'fmtCnf read=',f
        basename = os.path.basename(f).replace('.cnf','')
        cnf[basename]={}

        v = open(f,'rb').read()
        vline = v.split("\r\n")
        for line in vline:
            if len(line)==0:continue
            lineArr = line.split('=',1)
            cnf[basename][lineArr[0]] = lineArr[1]
        #print 'fmtCnf conf=',cnf[basename]
        print '=============='
        


deled={}

def fmtJSON (f):
    global cnf
    global deled

    keyDict = {}
    keyIndex2Dict={"0":""}
    jsonFile = f
    csvFile = f
    
    folder = "./samejson"
    
    if csvFile.find('~')!=-1:
        csvArr = csvFile.split('~')
        jsonFile = csvArr[0] 
        csvFile = csvArr[0]
        folder = './'+csvArr[1]
    
    allAdd = os.getcwd()+folder

    if not os.path.exists(allAdd):
        os.makedirs(allAdd)

    if csvFile.find('@')!=-1:
        csvArr = csvFile.split('@')
        jsonFile = csvArr[0]
        csvFile = csvArr[1]
       
    reader = csv.reader(open('csv/'+ csvFile +'.csv','rb'))
    res = None
    #print 'fmtJSON=',f
    for idx,item in enumerate(reader):
        if idx==0:
            for i,k in enumerate(item):
                keyDict[k] = i
                keyIndex2Dict[str(i+1)] = k

        else:

            s = cnf[f]['line']
            _tmpArr = keyDict.keys()
            _tmpArr.sort(cmp=lambda x,y:cmp(len(y),len(x)))

            for dk in _tmpArr:
                v = (item[keyDict[dk]])
                
                #打乱内容，防止被重复替换
                newv=""
                for letter in v:
                    newv += letter +chr(1)

                s = s.replace(dk, newv )
            
            try:
                #去掉打乱码
                s = s.replace(chr(1),'')
                s = s.decode('gbk')
                _js = json.loads(s)
            except Exception as e:
                print e
                print ''
                print 'file =',f
                print 'line =',idx
                print 'data =',item
                print s

            if 'group' in cnf[f]:
                __gk = (item[keyDict[ cnf[f]['group'] ]]).decode('gbk')
                
                if res==None:res={}

                if 'key' in cnf[f]:
                    if not __gk in res :
                        res[__gk] = {}

                    __k = (item[keyDict[ cnf[f]['key'] ]]).decode('gbk')
                    res[__gk][__k] = _js
                else:
                    if not __gk in res :
                        res[__gk] = []
                    res[__gk].append(_js)

            else:
                
                if 'key' in cnf[f]:
                    if res==None:res={}
                    __k = (item[keyDict[ cnf[f]['key'] ]]).decode('gbk')
                    res[ __k ] = _js
                else:
                    if res==None:res=[]
                    res.append(_js)
    
    if jsonFile == "jiban":
        for k,v in res.items():
            while '' in v['hidlist']:
                v['hidlist'].remove('')

    if jsonFile == "guanka":
        f = open("./samejson/fights.json",'r')
        fightJson = json.loads(f.read())

        f2 = open("./samejson/npc.json",'r')
        npcJson = json.loads(f2.read())

        for k,v in res.items():
            _fightid = v['fights'][-1]
            _fcon = fightJson[str(_fightid)]
            _npcid = ''
            for ele in _fcon:
                if 'master' in ele and ele['master'] ==1:
                    _npcid = ele['npcid']

            if _npcid == '':
                print "no master in fights id:",_fightid
                continue

            _npcCon = npcJson[str(_npcid)]
            v['npcimg'] = _npcCon['yhead']
            v['npcname'] = _npcCon['name']
    
    res = (json.dumps(res,ensure_ascii=False,indent=2)).encode('utf8')
    fjson = folder+"/"+ jsonFile +".json"
    _fName = f
    f = open(fjson, 'w')
    f.truncate()
    f.write(res)
    f.close()
    print 'fmtJSON write=',fjson
    print '=============='

def start ():
    global cnf
    fmtCnf()
    for f in cnf:
        fmtJSON(f)
    
    _mearge = [
        ["item","mergeitem","samejson/item.json","item"],
        ["armyattr~clientjson","mergearmyattr","clientjson/armyattr.json","armyattr"]
    ]        
    for f in cnf:
        for ele in _mearge:
            if str(f)==ele[0]:
                #os.system(ele[1])
                __import__(ele[1])
                shutil.move(ele[3] + ".json",  ele[2])
                print "move ===== " + ele[2]
       

start()
