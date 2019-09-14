from django.http import HttpResponse,JsonResponse
import json
import time
from house.models import LianJiaTenementHouse
# Create your views here.
def house_views(request):
    """
    处理前端请求 返回符合条件数据
    :param request:
    :return:
    """
    if request.method == "POST":
        print('POST')
        user_message = json.loads(request.body)
        # 前端传过来的数据 {'W_L': [116.42543, 39.903909], 'DS': 8.333333333333332, 'price': '1000'}
        # W_L: 工作地点经纬度， DS:距离 单位km  prices：接受价格1000  条件就是0<=1000
        print(user_message)
        #select * from LianJia_table where (lon< 116.406878 and  lon>116.406876) and (lat < 39.721465 and lat >39.721463);
        house_list = LianJiaTenementHouse.objects.all()
        toget_array = []
        for i in house_list:
            dict = {}
            dict['locat']=[float(i.lon), float(i.lat)]
            dict['house_name']=i.house_name
            dict['address']=i.house_name
            dict['url']=i.url
            dict['message']=i.house_name
            toget_array.append(dict)
            print(dict)
    time.sleep(1)
    return JsonResponse({'code':200,'data':toget_array})