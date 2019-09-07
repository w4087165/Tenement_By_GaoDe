from django.http import HttpResponse,JsonResponse
import json
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

        toget_array=[
            {'locat':[116.4254309,39.903901],
             'house_name':'月季园',
             'url':'www.baidu.com',
             'message':'啥啥啥',
            }
        ]

    return JsonResponse({'code':200,'data':toget_array})