from pymongo import MongoClient

# 获取mongodb实例
def connect_to_mongodb():
    MONGO_URI = 'mongodb+srv://admin:uniHVb5ghi6hFmb@cluster0.faj5b.mongodb.net'
    MONGO_DB = 'graduation_project'
    client = MongoClient(MONGO_URI)
    conn = client[MONGO_DB]
    return conn


# 从mongodb中获取数据
def get_data_from_mongodb(title, collection):
    data_list = list()
    title = str(title)
    if title.__contains__('岗位分布'):
        position_category = ['前端', '后端', '产品', '算法', '数据', '运营', '测试']
        for i in position_category:
            res = collection.count_documents({'job_name': {'$regex': i}})
            # 返回一个包含name和value两个键值对的字典
            data_dict = {'name': i, 'value': int(res)}
            data_list.append(data_dict)
    elif title.__contains__('平均薪资'):
        position_category = ['前端', '后端', '产品', '算法', '数据', '运营', '测试']
        for i in position_category:
            pipeline = [{'$match': {'job_name': {'$regex': i}}},
                        {'$group': {'_id': i, 'value': {'$avg': '$providesalary_text'}}}]
            res = collection.aggregate(pipeline)
            for data in res:
                # 保留小数点后第一位
                data_dict = {'name': i, 'value': int(data.get('value') * 10)}
                data_list.append(data_dict)
    elif title.__contains__('企业类型'):
        pipeline = [{'$group': {'_id': '$companytype_text', 'value': {'$sum': 1}}}]
        res = collection.aggregate(pipeline)
        for data in res:
            if data.get('_id') == '':
                pass
            else:
                data_dict = {'name': data.get('_id'), 'value': data.get('value')}
                data_list.append(data_dict)
    elif title.__contains__('企业规模'):
        company_size = ['少于50人', '50-150人', '150-500人', '500-1000人', '1000-5000人', '5000-10000人', '10000人以上']
        for size in company_size:
            if size.__contains__('少于50人'):
                gt = 0
                lt = 49
            elif size.__contains__('以上'):
                gt = 10000
                lt = 100000
            elif size.__contains__('-'):
                text = size.replace('人', '').split('-')
                gt = int(text[0])
                lt = int(text[1])
            else:
                continue
            # Count the documents where greater than or equal to gt and less than lt
            count = collection.count_documents({'companysize_text': {'$gte': gt, '$lt': lt}})
            data_dict = {'name': str(size), 'value': count}
            data_list.append(data_dict)
    elif title.__contains__('所属行业'):
        pipeline = [{'$group': {'_id': '$companyind_text', 'value': {'$sum': 1}}}]
        res = collection.aggregate(pipeline)
        for data in res:
            data_dict = {'name': data['_id'], 'value': data['value']}
            data_list.append(data_dict)
    elif title.__contains__('薪资和工作年限'):
        position_category = ['前端', '后端', '产品', '算法', '数据', '运营', '测试']
        for i in position_category:
            # 先选工作分类再按照{名称:薪资list}的字典结构做成数组, 年份在data.py的xAsis定义
            pipeline = [{'$match': {'job_name': {'$regex': i}}},
                        {'$group': {'_id': '$workyear', 'value': {'$avg': '$providesalary_text'}}},
                        {'$sort': {'_id': 1}}]
            res = list(collection.aggregate(pipeline))
            salary_list = list()
            for index in range(0, len(res)):
                salary = int(res[index].get('value') * 10)
                salary_list.append(salary)
            data_dict = {'name': i, 'value': salary_list}
            data_list.append(data_dict)
    elif title.__contains__('不同类型企业薪资待遇情况'):
        pipeline = [{'$group': {'_id': '$companytype_text', 'value': {'$avg': '$providesalary_text'}}}]
        res = collection.aggregate(pipeline)
        for data in res:
            if data.get('_id') == '':
                pass
            else:
                data_dict = {'name': data.get('_id'), 'value': data.get('value') * 10}
                data_list.append(data_dict)
    elif title.__contains__('一线城市岗位数量'):
        data_list_old = [
            {"color": "01", "radius": ['59%', '70%']},
            {"color": "02", "radius": ['49%', '60%']},
            {"color": "03", "radius": ['39%', '50%']},
            {"color": "04", "radius": ['29%', '40%']},
            {"color": "05", "radius": ['20%', '30%']},
        ]
        data_list_new = list()
        city = ['北京', '上海', '广州', '深圳', '杭州']
        total_num = collection.count_documents({})
        # 计算各省市的岗位与总数的比值并封装成字典,用列表存储
        for i in city:
            res = collection.count_documents({'workarea_text': i})
            proportion = int(res / total_num * 100)
            data_dict = {'name': i, 'value': proportion, 'value2': 100 - proportion}
            data_list_new.append(data_dict)
        # 将两个列表里的字典合并
        for j in range(0, len(city)):
            data_dict_complete = {**data_list_new[j], **data_list_old[j]}
            data_list.append(data_dict_complete)
    else:
        pass
    return data_list