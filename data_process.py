import pymongo


if __name__ == '__main__':
    init_id = '6505979820'
    dbclient = pymongo.MongoClient(host='localhost', port=27017)
    db = dbclient['Sina']
    info_collection = db['Information']
    relation_collection = db['Relationships']
    label_collection = db['Label']

    id_set = [item['_id'] for item in label_collection.find()]

    # 在label中添加name字段
    # id_name_set = []
    # for id in id_set:
    #     item = relation_collection.find_one({'fan_id': id})
    #     if item:
    #         id_name_set.append({'id':id, 'name':item['fan_name']})
    #         label_collection.update_one({'_id':id}, {'$set': {'name':item['fan_name']}})
    #         continue
    #     else:
    #         item = relation_collection.find_one({'followed_id': id})
    #         id_name_set.append({'id':id, 'name':item['followed_name']})
    #         label_collection.update_one({'_id': id}, {'$set': {'name': item['followed_name']}})

    # count link
    # cnt_set = [{'_id':id,'cnt':int(0)} for id in id_set]
    # for item in relation_collection.find():
    #     for cnt_item in cnt_set:
    #         if item['fan_id']== cnt_item['_id']:
    #             cnt_item['cnt'] += 1
    #             continue
    #
    # for item in relation_collection.find():
    #     for cnt_item in cnt_set:
    #         if item['followed_id']== cnt_item['_id']:
    #             cnt_item['cnt'] += 1
    #             continue
    #
    # for id in id_set:
    #     for cnt_item in cnt_set:
    #         if id == cnt_item['_id']:
    #             label_collection.update_one({'_id':id},{'$set':{'friend_cnt':cnt_item['cnt']}})
    #             continue

    # 标记大V
    # condition_famous = {'fans_num': {'$gt': 500}}  # 选取粉丝大于500的账号
    # famous_id0 = [r['_id'] for r in info_collection.find(condition_famous)]
    #
    # for id in famous_id0:
    #     label_collection.update_one({'_id':id},{'$set':{'label':'famous'}})

    # 把自己label变成center
    #label_collection.update_one({'_id': init_id}, {'$set': {'label': 'center'}})
