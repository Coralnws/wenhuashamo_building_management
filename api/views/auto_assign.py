import jieba

def auto_assign(text):
    stop_words = ['的', '了', '是', '在', '和','我','你','他','它','着','住']
    tokens = jieba.cut(text)  # 使用jieba分词器对文本进行分词
    filtered_tokens = [token for token in tokens if token not in stop_words]


    print(filtered_tokens )

auto_assign("我的厕所水管爆裂了")

    
