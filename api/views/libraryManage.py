from django.db.models import Q

from api.models import Library
from api.utils import UTF8JsonResponse, return_response
import json
from django.forms.models import model_to_dict

def get_library(request):
    if request.method == 'GET':
        search = request.GET.get('search', '')

        filter = Q()
        if search:
            filter &= Q(title__icontains=search) | Q(description__icontains=search) | Q(solution__icontains=search)

        libraries = Library.objects.filter(filter)

        library_detail = []
        for library in libraries:
            data=model_to_dict(library)
            library_detail.append(data)

        return return_response(1001, '查询知识库成功', library_detail)
