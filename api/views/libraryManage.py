from django.db.models import Q

from api.models import Repair
from api.utils import UTF8JsonResponse


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
            data['title'] = '标题'  #
            data['content'] = repair.description
            data['solve'] = repair.plan
            data['type'] = '1'  #
            data['worker'] = repair.solver
            data['contact'] = repair.staffContact
            library_detail.append(data)

        return UTF8JsonResponse({'errno': 1001, 'msg': '查询知识库成功', 'data': library_detail})
