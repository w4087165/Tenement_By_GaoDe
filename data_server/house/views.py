from django.http import HttpResponse,JsonResponse
import json
# Create your views here.
def house_views(request):
    """
    处理前端请求 返回符合条件数据
    :param request:
    :return:
    """
    # if request.method == "GET":
    #     print('get')
    #     user_message = json.loads(request.body)
    #     print(user_message)

    return JsonResponse({'code':200})