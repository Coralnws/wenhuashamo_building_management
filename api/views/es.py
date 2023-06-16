from django.http import JsonResponse
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.connections import connections
import jieba.analyse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json

from ..utils import *

# 创建elasticsearch全局客户端
client = connections.create_connection(hosts=['http://120.46.205.87:9200'],
                                       http_auth=('elastic'), timeout=40)
paper_index = "title1"
author_index = "author"


# client = connections.create_connection(hosts=['http://127.0.0.1:9200'],
#                                        http_auth=('elastic','MgMCEKrwxeDHYvDVQREh'), timeout=20)


# 不同的查询项有不同的策略，如下是主题查询，则策略为关键词匹配title
def Qby_item(item: str, text: str):
    # 主题检索，按照篇名摘要权重查询
    if item == "idea":
        # 关键词提取
        keywords1 = jieba.analyse.extract_tags(text)
        Q_text = " ".join([keyword + "*" for keyword in keywords1])

        # 标题高权重，摘要低权重
        q = Q({"multi_match": {"query": Q_text, "fields": ["title^2", "abstract"]}})
        return q
    # 标题查询：切词，精确匹配
    elif item == "title":
        q = Q("match", title="*" + text + "*")
        return q
    # 作者名检索：不切词，精确匹配
    elif item == "author":
        q = Q({"match_phrase": {"authors.name": "*" + text + "*"}})
        return q
    # 作者单位：模糊查询
    elif item == "org":
        print("*" + text + "*")
        q = Q({"wildcard": {"authors.org": "*" + text + "*"}})
        return q
    # 会议期刊：同上
    elif item == "venue" or item == "issn":
        q = Q({"multi_match": {"query": "*" + text + "*", "fields": ["venue.raw", "issn"]}})
        return q

@csrf_exempt
def QPaper(request):
    info = json.loads(request.body)
    print(info)
    d = info.get('search')
    if d is None:
        return UTF8JsonResponse({'errno': 100002, 'msg': 'search请求为空'})
    # d = {"text": "Center for Astrophysics", "by": "idea", "from": 0, "size": 1,
    #      "filter": [{"item": "title", "text": "Center for Astrophysics"}], "year_filter": [1995, 1997], "sort": "year"}

    # 构建查询
    s = Search(using=client, index=paper_index).extra(from_=d["from"], size=d["size"])

    # 按字段匹配
    q = Qby_item(d["by"], d["text"]).to_dict()

    if d["filter"] is [] and d["year_filter"] is []:
        # 聚合查询，全部
        s.aggs.bucket("title_agg_info", "terms", field="title")  # 关键词。这里相当于是对标题进行切词并词频统计。
        s.aggs.bucket("year_agg_info", "terms", field="year")  # 年份
        s.aggs.bucket("authors_agg_info", "terms", field="authors.name.keyword")  # 作者名，取text下的keyword用于聚合
        s.aggs.bucket("venue_agg_info", "terms", field="venue.raw.keyword")  # 会议
        s.aggs.bucket("issn_agg_info", "terms", field="issn")  # 期刊
        s.aggs.bucket("org_agg_info", "terms", field="authors.org")  # 机构，太长需要切词
    else:
        # 侧边栏筛选
        # 构建筛选器
        my_filter = {"bool": {"must":
                                  [Qby_item(**f).to_dict() for f in d["filter"]] + [
                                      {"terms": {"year": d["year_filter"]}}]
                              }}

        q = {"bool": {
                "must": q,
                "filter": my_filter
            }}

        print([Qby_item(**f).to_dict() for f in d["filter"]])
        s = s.query(q)

    # 排序：相关度（默认），发表时间，被引，综合
    if d.get("sort"):
        s = s.sort(d["sort"])

    response = s.execute()
    ret = {"paper": [hit.to_dict() for hit in response], "aggs": response.aggs.to_dict()}
    print(ret)
    return UTF8JsonResponse({'errno': 100000, 'msg': '查询成功', 'post': ret})


# QPaper()

@csrf_exempt
def QAuthor(request):
    info = json.loads(request.body)
    d = info.get('search')
    if d is None:
        return UTF8JsonResponse({'errno': 100002, 'msg': 'search请求为空'},charset='utf-8')
    #d = {"name": "Ren Bao-Cang", "relative_paper_num": 20 ,"sort":"-n_citation"}
    # 返回作者

    author = Search(using=client, index=author_index)

    q = Q("match_phrase", name="*" + d["name"] + "*")
    author = author.query(q)

            # 排序：相关度（默认），发表时间，被引，综合
    author = author.sort(d["sort"])
        
    res_a = author.execute()

    # 返回相关文献
    paper = Search(using=client, index=paper_index).extra(from_=0, size=d["relative_paper_num"])

    q = Q({"match_phrase": {"authors.name": "*" + d["name"] + "*"}})
    paper = paper.query(q)
    paper = paper.sort(d["sort"])
    res_p = paper.execute()



    ret = {"author": [hit.to_dict() for hit in res_a], "paper": [hit.to_dict() for hit in res_p]}
    # print(ret)
    return UTF8JsonResponse({'errno': 100000, 'msg': '查询成功', 'post': ret})


# QAuthor()

@csrf_exempt
def AdvancedQ(request):
    info = json.loads(request.body)
    d = info.get('search')

    # d中各键内容可为空，但必须存在
    # d = {
    #     "must": [{"item": "title", "text": "Center for Astrophysics"}],  # 精确 是
    #     "must_not": [{"item": "title", "text": "ASTROPHYSICS"}],  # 精确 否
    #     "should": [{"item": "title", "text": "ASTROPHYSICS"}],  # 模糊 是（只能影响评分排序）
    #     "should_not": [{"item": "title", "text": "ASTROPHYSICS"}],  # 模糊 否（只能影响评分排序）
    #     "other": 0, "issn": 0, "venue": 0,
    #     "year": {"gte": 1990, "lt": 2005}
    # }

    # 文献来源,可多选:会议、文献、其它（两个都不是）
    source = []
    if d["issn"]:
        source.append({"exists": {"field": "issn"}})
    if d["venue"]:
        source.append({"exists": {"field": "venue"}})
    if d["other"]:
        source.append({"bool": {"must_not": [
            {"exists": {"field": "issn"}},
            {"exists": {"field": "venue"}}
        ]}})

    # 对结果进行精确过滤，不影响评分排序
    my_filter = {
        "bool": {"must": [
            {"range": {"year": d["year"]}},
            {"bool": {"should": source}},
        ]},
    }

    q = {
        "bool": {
            "must": [Qby_item(**must).to_dict() for must in d["must"]],
            "must_not": [Qby_item(**must_not).to_dict() for must_not in d["must_not"]],
            "should": [Qby_item(**should).to_dict() for should in d["should"]] +
                      [{"bool": {"must_not": Qby_item(**should_not).to_dict()}} for should_not in d["should_not"]],
            "filter": my_filter,
        }
    }

    paper = Search(using=client, index=paper_index).extra(from_=0, size=500)
    paper = paper.query(q)
    res = paper.execute()
    print(paper.count())
    # print([hit.to_dict() for hit in res][0])
    return UTF8JsonResponse({'errno': 100000, 'msg': '查询成功', 'post': [hit.to_dict() for hit in res]})

# AdvancedQ()


def searchAuthor(d):
    author = Search(using=client, index=author_index)

    q = Q({"match": {"id" : d }})
    author = author.query(q)
    res_a = author.execute()
    print(res_a)

    ret = {"data": [hit.to_dict() for hit in res_a]}
    return ret

# @csrf_exempt
# def getAuthorById(request):
#     d = request.GET.get('scholarId','')
#     if d is None:
#         return UTF8JsonResponse({'errno': 100002, 'msg': 'search请求为空'},charset='utf-8')
    
#     ret = searchAuthor(d)
#     print(ret['data'])


#     return UTF8JsonResponse({'errno': 100000, 'msg': '查询成功', 'data': ret})

def searchPaper(d):
    paper = Search(using=client, index=paper_index)
    q = Q({"match": {"id" : d }})
    paper = paper.query(q)
    res_p = paper.execute()

    ret = {"data": [hit.to_dict() for hit in res_p]}
    return ret

@csrf_exempt
def getPaperById(request):
    #info = json.loads(request.body)
    d = request.GET.get('paperId','')

    if d is None:
        return UTF8JsonResponse({'errno': 100002, 'msg': 'search请求为空'},charset='utf-8')
    ret = searchPaper(d)
    
    return UTF8JsonResponse({'errno': 100000, 'msg': '查询成功', 'post': ret})

@csrf_exempt
def getAuthorById(request):
    d = request.GET.get('scholarId','')
    if d is None:
        return UTF8JsonResponse({'errno': 100002, 'msg': 'search请求为空'},charset='utf-8')
    ret = searchAuthor(d)
    cooperatorList=[]
    scholarList=[]
    for tmp in ret['data'][0]['pubs']:
        paperId=tmp['i']
        authorRank=tmp['r']
        data = searchPaper(paperId)
        data = data['data']
        
        if len(data) > 0:
            data=data[0]

            if 'title' in data : tmp['title'] = data['title'] 
            if 'year' in data : tmp['year'] = data['year']
            if 'n_citation' in data : tmp['n_citation'] = data['n_citation']
            if 'authors' in data : 
                tmp['authors']=[]
                authorList = data['authors']
                exist=0
                for tmp2 in authorList:
                    str=tmp2['name']
                    #print(str)
                    for name in scholarList:
                        if str.lower() == name.lower():
                            exist=1
                            break
                    if exist == 0:        
                        scholarList.append(tmp2['name'])
                        cooperatorList.append(tmp2)        
                    #print(cooperatorList)
                    exist=0
                tmp['authors'] = authorList

    # #print(cooperatorList)
    # for scholar in cooperatorList:
    #     if 'id' in scholar:
    #         scholarData=searchAuthor(scholar['id'])['data']
    #         # del scholar['id']
    #         # del scholar['name']
    #         scholar['data']=scholarData
       
    ret['cooperator'] = cooperatorList
    
    return UTF8JsonResponse({'errno': 100000, 'msg': '查询成功', 'post': ret})

@csrf_exempt
def AuthorRank(request):
    d=request.GET.get('sort','')
    if d is None:
        return UTF8JsonResponse({'errno': 100002, 'msg': 'search请求为空'},charset='utf-8')
    # d = {"name": "Ren Bao-Cang", "relative_paper_num": 20}
    # 返回作者
    author = Search(using=client, index=author_index)

    q = Q("match", name="*")
    author = author.query(q)
    author = author.sort(d)
    res_a = author.execute()

    ret = {"author": [hit.to_dict() for hit in res_a]}
    # print(ret)
    return UTF8JsonResponse({'errno': 100000, 'msg': '查询成功', 'post': ret})