from utilities import connect_to_mongodb, get_data_from_mongodb

data_list_old = [
    {"color": "01", "radius": ['59%', '70%']},
    {"color": "02", "radius": ['49%', '60%']},
    {"color": "03", "radius": ['39%', '50%']},
    {"color": "04", "radius": ['29%', '40%']},
    {"color": "05", "radius": ['20%', '30%']},
]
data_list_new = list()
data_list = list()
conn = connect_to_mongodb()
collection = conn['data_51job']
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
print(data_list)
