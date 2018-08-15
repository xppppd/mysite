'''
http://news.maxjia.com/maxnews/app/list/?limit=10
max+最新的10条新闻

小黑盒新闻 抓不到头条
https://api.xiaoheihe.cn/maxnews/app/list
抓头条必须携带设备信息
https://api.xiaoheihe.cn/maxnews/app/list?lang=zh-cn&os_type=iOS&os_version=11.3.1&_time=1533116345&version=1.1.35&device_id=8DEDA24A-B0CF-4FA3-A600-2859073BB90D&heybox_id=304443&limit=20&offset=0&rec_mark=timeline&tag=-1
limit参数限制条数
offset 参数限制起始位置
'''

import requests
import pymysql


db_info = ("localhost", "xiongpan", "123456", "mysite_test")


def get_maxplus_news():
    url = 'http://news.maxjia.com/maxnews/app/list?limit=30'
    headers = {'Host': 'news.maxjia.com:443',
               'Accept': '*/*',
               'Connection': 'keep - alive',
               'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/41.0.2272.118 Safari/537.36 ApiMaxJia/1.0',
               'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
               'Cookie': 'phone_num=0009010503070900050704;pkey=MTQ0ODcwMjgwNy4yNTE4MDQyNjgxNDY1XzFiYWF3aGFocmxlc29kbmZ2'
               }
    r = requests.get(url, headers=headers)
    content = r.json()
    return content['result']


def get_heybox_news():
    url = 'https://api.xiaoheihe.cn/maxnews/app/list?lang=zh-cn&os_type=iOS&os_version=11.3.1&_time=1533116345&version=1.1.35&device_id=8DEDA24A-B0CF-4FA3-A600-2859073BB90D&heybox_id=304443&limit=20&offset=0&rec_mark=timeline&tag=-1'
    headers = {'Host': 'api.xiaoheihe.cn:443',
               'Accept': '*/*',
               'Connection': 'keep - alive',
               'User-Agent': 'xiaoheihe/1.1.35 (iPhone; iOS 11.3.1; Scale/3.00)',
               'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
               'Cookie': 'pkey=MTUwMjAyMzE4NC43Nl8zMDQ0NDNrb2p0ZWdpZ2VvZGF3dHhw;hkey=6e0ea564a7fe9a271183e039b5481422'
               }
    r = requests.get(url, headers=headers)
    content = r.json()
    return content['result']

def get_ids(cur,table_name):
    sql = "select id from {}".format(table_name)
    id_list = []
    try:
        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        for row in results:
            id_list.append(row[0])
        print(id_list)
    except Exception as e:
        raise e
    return id_list


def save_to_db(data_list):
    print(data_list[0])
    db = pymysql.connect(*db_info)
    cursor = db.cursor()
    id_list = get_ids(cursor,'news_info')
    for data in data_list:
        try:
            id = data['newsid']
        except:
            # print(data)
            continue
        if int(id) not in id_list:
            click = data['click']
            date = data['date']
            imgs = data['imgs'][0]
            newsUrl = data['newUrl']
            tag = data['tag']
            title = data['title']
            sql = 'INSERT INTO news_info (id,click,date,imgs,newsUrl,tag,title)' \
                  ' VALUES ("{}","{}","{}","{}","{}","{}","{}")'.format(id, click, date, imgs, newsUrl, tag, title)
            # 存入数据库
            print(sql)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except Exception as e:
                # 如果发生错误则回滚
                print(e)
                db.rollback()
    # 关闭数据库连接
    db.close()


def save_d2_to_db(data_list):
    db = pymysql.connect(*db_info)
    cursor = db.cursor()
    id_list = get_ids(cursor,'d2_news_info')
    for data in data_list:
        try:
            id = data['newsid']
        except:
            print(data)
            continue
        if int(id) not in id_list:
            click = data['click']
            date = data['date']
            imgs = data['imgs'][0]
            newsUrl = data['newUrl']
            tag = 'DOTA2'
            title = data['title']
            topic_type = data['news_topic_type'][0] if data['news_topic_type'] else None
            matchList = data['match_list'] if 'match_list' in data else ''
            sql = 'INSERT INTO d2_news_info (id,click,date,imgs,newsUrl,tag,title,matchList,topic_type) VALUES ' \
                  '("{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(id, click, date, imgs, newsUrl, tag, title,
                                                                          str(matchList), topic_type)
            # 存入数据库
            print(sql)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except Exception as e:
                # 如果发生错误则回滚
                print(e)
                db.rollback()
    # 关闭数据库连接
    db.close()


def update_to_db(data_list, table):
    db = pymysql.connect(*db_info)
    cursor = db.cursor()
    for data in data_list:
        try:
            id = data['newsid']
            click = data['click']
        except:
            print(data)
            continue
        top = 0
        if 'top' in data and data['top']:
            top = 1
        sql = 'UPDATE {} SET click = {} where id = {}'.format(table, click, id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print('{} click update failed'.format(id))
            db.rollback()
        sql = 'UPDATE {} SET top = {} where id = {}'.format(table, top, id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print('{} top update failed!!'.format(id))
            db.rollback()
    db.close()


if __name__ == '__main__':
    data_list = get_maxplus_news()
    save_d2_to_db(data_list)
    update_to_db(data_list, 'd2_news_info')

    data_list2 = get_heybox_news()
    save_to_db(data_list2)
    update_to_db(data_list2, 'news_info')
