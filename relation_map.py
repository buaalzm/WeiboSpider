import pymongo
import json
import os
from pyecharts import options as opts
from pyecharts.charts import Graph, Page
from pyecharts.faker import Collector

C = Collector()


@C.funcs
def graph_weibo() -> Graph:
    with open(os.path.join("fixtures", "weibo.json"), "r", encoding="utf-8") as f:
        j = json.load(f)
        nodes, links, categories, cont, mid, userl = j
    c = (
        Graph()
        .add(
            "",
            nodes,
            links,
            categories,
            repulsion=50,
            linestyle_opts=opts.LineStyleOpts(curve=0.2),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title="Graph-微博转发关系图"),
        )
    )
    return c

if __name__ == '__main__':
    init_id = '6505979820'
    dbclient = pymongo.MongoClient(host='localhost', port=27017)
    db = dbclient['Sina']
    info_collection = db['Information']
    relation_collection = db['Relationships']
    label_collection = db['Label']

    id_set = [item['_id'] for item in label_collection.find()]  # 所有账号的集合

    disp_id = [init_id]
    fan0_id = [r['_id'] for r in label_collection.find({'label':'fan0'})]
    follow0_id = [r['_id'] for r in label_collection.find({'label':'follow0'})]
    fans_follows0 = list(set(fan0_id) | set(follow0_id))  # 取关注和粉丝的并集
    condition_fan1 = {'followed_id': {'$in': fans_follows0}}  # 一级好友的粉丝
    condition_follow1 = {'fan_id': {'$in': fans_follows0}}  # 一级好友的关注

    fan1_id = [r['fan_id'] for r in relation_collection.find(condition_fan1)]
    follow1_id = [r['followed_id'] for r in relation_collection.find(condition_follow1)]

    disp_id = list(set(disp_id)|set(fans_follows0)|(set(fan1_id)&set(follow1_id)))
    node_condition = {'_id':{'$in':disp_id}}


    nodes = []
    for item in label_collection.find(node_condition):
        circle_size = item['friend_cnt'] if item['friend_cnt']<100 else 100
        nodes.append({'name': item['name'],
         "symbolSize": circle_size,
         "draggable": "False",
         "value": 10 if item['label'] == 'famous' else item['friend_cnt'],
         "category": item['label'],
         "label": {
             "normal": {
                 "show": "True"
             }
         }
         })

    links = []
    for link in relation_collection.find():
        if link['fan_id'] in disp_id and link['followed_id'] in disp_id:
            links.append({'source': link['fan_name'],
             'target': link['followed_name']
             })

    categories = [
        {'name': item} for item in label_collection.distinct('label')
    ]

    graph = Graph(init_opts=opts.InitOpts(width="1920px", height="1080px"))

    graph.add(
        "",
        nodes,
        links,
        categories,
        repulsion=50,
        linestyle_opts=opts.LineStyleOpts(curve=0.2),
        label_opts=opts.LabelOpts(is_show=False),
    ).set_global_opts(
        legend_opts=opts.LegendOpts(is_show=False),
        title_opts=opts.TitleOpts(title="Graph-微博好友关系图"),
    ).render()

