from django.db.models import Q

from api.models import Repair
from api.utils import UTF8JsonResponse, return_response
import json


def get_library(request):
    if request.method == 'GET':
        search = request.GET.get('search', '')
        repairs = Repair.objects.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(plan__icontains=search)
        )

        library_detail = []
        for repair in repairs:
            data = {}
            data['title'] = repair.title
            data['content'] = repair.description
            data['solve'] = repair.plan
            data['type'] = repair.type
            data['worker'] = repair.solver.realname
            data['contact'] = repair.staffContact
            library_detail.append(data)

        return return_response(1001, '查询知识库成功', library_detail)\
