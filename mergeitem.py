#!/usr/bin/python
#coding:utf-8

import json,glob,os

'''
合并所有item为一个json
'''

'''
详细注释:
    "comment":{
        "k":"道具id(itemid)",
        "isMutil":"是否可叠加",
        "name":"道具名",
        "type":"道具类型(大类型,主要用于分类,1.军械,2.宝物,3.将魂,4.消耗品)",
        "stype":"子类型,道具实际类型(5.经验卡,6.属性卡,7.不可使用类型,8.随机道具,9.特殊道具)",
        "stype-5":"经验卡道具,addexp 为该卡增加的经验 useobj 为使用对象(hero武将,me主公)",
        "stype-6":"属性卡,增加人物属性的道具",
        "stype-7":"不可使用类型,无法再背包中使用,只可以存在背包中",
        "stype-8":"获得随机道具,randarr 为随机道具组,num 为随机获得几个道具",
        "color":"物品品质(颜色)",
        "以上为必选key,所有道具都会有的东西":"可选key的注释请写在下面"
    },

'''
_commoent = {
    "comment":{
        "iid": u"道具ID",
        u"以上为必选key,所有道具都会有的东西": u"可选key的注释请写在下面",
        "color": u"品质0-白，1-绿，2-蓝，3-紫，4-橙",
        "lv": u"等级",
		"icon": u"图标",
        "name": u"道具名",
        "type": u"1-材料，2-消耗品，3-装备，4-配件，6-限时宠物，7-采集道具，8-宝箱",
        "stype": u"材料:无stype; 消耗品：2-伤害类道具，3-持续恢复类道具，4-瞬间恢复道具，5-体力道具，6-汽油道具； 装备:1-武器，2-头盔，3-衣服，4-裤子，5-手套，6-鞋子；配件：1-枪头，2-子弹袋，3-握把，4-瞄准，5-托腮，6-弹夹;限时宠物：宠物id；采集道具：1-斧头类，2-矿镐类",
		"wtype": u"0-其他；1-手枪，2-霰弹枪，3-冲锋枪，4-步枪，5-狙击枪",
        "value": u"消耗品有用：体力道具-恢复数值；探险消耗品：道具的参数和类型",
        "cap": u"单个道具占用的容量",
		"ismutil": u"叠加数量上限，-1为无限叠加，int为单个格子叠加数量上限",
		"ttime": u"限时宠物过期时间，单位：秒",
        u"以上为必选key,所有道具都会有的东西":u"可选key的注释请写在下面"
    },
}
def start():
    print "start merge all item"
    files = glob.glob('samejson/item*.json')
    _globalMap = {'data':{}}
    for ele in files:
        print "process json:%s" % ele
        _raw = open(ele,"rb").read()
        _rr = json.loads(_raw,encoding='utf-8')
        _globalMap['data'].update(_rr)
    
    #_globalMap.update(_commoent)
    _output = json.dumps(_globalMap,indent=4,ensure_ascii=False).encode('utf-8')
    _comments = json.dumps(_commoent,indent=4,ensure_ascii=False).encode('utf-8')
    _file = open("item.json","w")
    _file.truncate()
    _file.write(_comments[0:len(_comments)-2] + ",")
    _file.write(_output[1:])
    _file.close()
    print "process success..."
    
start()


