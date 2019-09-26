from django.http import HttpResponse,JsonResponse
import json
import time
from house.models import LianJiaTenementHouse
import pymysql
# Create your views here.
def house_views(request):
    """
    处理前端请求 返回符合条件数据
    :param request:
    :return:
    """
    db = pymysql.connect('localhost', 'root', '123456', 'House_db', charset='utf8')
    cursor = db.cursor()
    if request.method == "POST":
        print('POST')
        user_message = json.loads(request.body)
        # 前端传过来的数据 {'W_L': [116.42543, 39.903909], 'DS': 8.333333333333332, 'price': '1000'}
        # W_L: 工作地点经纬度， DS:距离 单位km  prices：接受价格1000  条件就是0<=1000
        # 距离计算公式
        #select * from location where sqrt((((113.914619-longitude)*PI()*12656*cos(((22.50128+latitude)/2)*PI()/180)/180) * ((113.914619-longitude)*PI()*12656*cos (((22.50128+latitude)/2)*PI()/180)/180) ) + ( ((22.50128-latitude)*PI()*12656/180) * ((22.50128-latitude)*PI()*12656/180) ) )<2
        #而这条sql执行的速度却非常缓慢,用了近1秒的时间才返回结果,导致整体的运算速度下降.
        # 而在实际的使用中,不太可能会发生需要计算该用户与所有其他用户的距离,然后再排序的情况,当用户数量达到一个级别时,就可以在一个较小的范围里进行搜索,而非在所有用户中进行搜索.
        # 所以对于这个例子,我增加了4个where条件,只对于经度和纬度大于或小于该用户1度(111公里)范围内的用户进行距离计算,同时对数据表中的经度和纬度两个列增加了索引来优化where语句执行时的速度.
        # 最终的sql语句如下

        print(user_message)
        user_lat = str(user_message['W_L'][1])
        user_lon = str(user_message['W_L'][0])
        user_price = float(user_message['price'])
        print(user_lat,user_lon)
        # sql = """
        #     select * from LianJia_table where sqrt((((116.365543-lon)*PI()*12656*cos(((39.963164+lat)/2)*PI()/180)/180) * ((39.963164-lon)*PI()*12656*cos (((39.963164+lat)/2)*PI()/180)/180) ) + ( ((39.963164-lat)*PI()*12656/180) * ((39.963164-lat)*PI()*12656/180)))<7
        # """
        sql = 'select * from LianJia_table where ' \
        'sqrt(((('+user_lon+'-lon)*PI()*12656*cos((('+user_lat +'+lat)/2)*PI()/180)/180) * (('+user_lon+'-lon)*PI()*12656*cos ((('+user_lat+'+lat)/2)*PI()/180)/180) ) + ( (('+user_lat+'-lat)*PI()*12656/180) * (('+user_lat+'-lat)*PI()*12656/180)) )<'+str(user_message['DS'])+\
        'and price>='+str(user_price-(5000 if user_price>=5000 else 1000))+\
        'and price<='+str(user_price)
        a = cursor.execute(sql)
        print('查询到',a)
        if a:
            house_list = cursor.fetchall()
            print(house_list)

            toget_array = []
            for i in house_list:
                dict = {}
                dict['locat']=[float(i[5]), float(i[6])]
                dict['house_name']=i[1]
                dict['platform']=i[2]
                dict['url']=i[7]
                dict['price']=float(i[4])
                dict['img'] = i[8]
                toget_array.append(dict)
                print(dict)
            return JsonResponse({'code':200,'data':toget_array})
        else:
            return JsonResponse({'code':404,'error':'没有找到符合条件的房子'})