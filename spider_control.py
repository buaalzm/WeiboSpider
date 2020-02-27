import os
import json
import pymongo


class SpiderControl:
    def __init__(self, init_uid):
        self.init_uid = init_uid
        self.set_uid([self.init_uid])
        self.dbclient = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.dbclient['Sina']
        self.info_collection = self.db['Information']
        self.relation_collection = self.db['Relationships']
        self.label_collection = self.db['Label']

    def set_uid(self, uid_list):
        uid_data = {'start_uids': uid_list}
        with open('start_uids.json','w') as f:
            json.dump(uid_data, f)

def add_filter(list1,list2):
    return list(set(list1+list2))

if __name__ == '__main__':
    init_id = '6505979820'
    sc = SpiderControl(init_id)

    try:
        sc.label_collection.insert({'_id':init_id,'label':'center'})
    except:
        print('已有该数据')

    # 这里第一次运行weibo_spider，第一次爬取粉丝和关注

    info_filter = [init_id]  # 标记已经爬过的id
    relation_filter = [init_id]  # 标记已经爬过的id

    condition_fan0 = {'followed_id':init_id} # 主人公的粉丝
    condition_follow0 = {'fan_id':init_id} # 主人公的关注

    fan0_id = [r['fan_id'] for r in sc.relation_collection.find(condition_fan0)]
    follow0_id = [r['followed_id'] for r in sc.relation_collection.find(condition_follow0)]

    # 打标签
    for id in follow0_id:
        try:
            sc.label_collection.insert_one({'_id':id,'label':'follow0'})  # 没有就添加
        except:
            sc.label_collection.update_one({'_id':id},{'$set':{'label':'follow0'}})  # 有就更新
    for id in fan0_id:
        try:
            sc.label_collection.insert_one({'_id':id,'label':'fan0'})
        except:
            sc.label_collection.update_one({'_id':id},{'$set':{'label':'fan0'}})


    fans_follows0 = list(set(fan0_id) | set(follow0_id)) # 取关注和粉丝的并集

    # 运行爬虫weibo_userinfo获得粉丝和关注用户的信息

    info_filter = add_filter(info_filter, fans_follows0)

    condition_famous = {'fans_num':{'$gt':500}}  # 选取粉丝大于500的账号
    famous_id0 = [r['_id'] for r in sc.info_collection.find(condition_famous)]

    relation_filter = add_filter(relation_filter, famous_id0)

    uid_set = list(set(fans_follows0) - set(relation_filter))
    print('id数量{}'.format(len(uid_set)))

    sc.set_uid(uid_set)

    # 运行爬虫weibo_spider获得这些人的粉丝关注网络

    condition_fan1 = {'followed_id': {'$in':fans_follows0}}  # 一级好友的粉丝
    condition_follow1 = {'fan_id': {'$in':fans_follows0}}  # 一级好友的关注

    fan1_id = [r['fan_id'] for r in sc.relation_collection.find(condition_fan1)]
    follow1_id = [r['followed_id'] for r in sc.relation_collection.find(condition_follow1)]

    fan1_id = list(set(fan1_id)-set(fans_follows0))  # 去除0级好友
    follow1_id = list(set(follow1_id) - set(fans_follows0))  # 去除0级好友

    # 打标签
    for id in follow1_id:
        try:
            sc.label_collection.insert_one({'_id': id, 'label': 'follow1'})  # 没有就添加
        except:
            sc.label_collection.update_one({'_id': id}, {'$set': {'label': 'follow1'}})  # 有就更新
    for id in fan1_id:
        try:
            sc.label_collection.insert_one({'_id': id, 'label': 'fan1'})
        except:
            sc.label_collection.update_one({'_id': id}, {'$set': {'label': 'fan1'}})

    fans_follows1 = list(set(fan1_id) & set(follow1_id)) # 取关注和粉丝的交集

    uid_set = list(set(fans_follows1) - set(info_filter))
    print('id数量{}'.format(len(uid_set)))

    sc.set_uid(uid_set)

    # 运行spider_userinfo

    info_filter = add_filter(info_filter, fans_follows1)












