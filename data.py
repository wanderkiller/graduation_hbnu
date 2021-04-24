#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/26 14:48
# @Author : way
# @Site : 
# @Describe:
from utilities import connect_to_mongodb
from utilities import get_data_from_mongodb


class SourceDataDemo:
    def __init__(self):
        conn = connect_to_mongodb()
        collection = conn['data_51job']

        # 默认的标题
        self.title = '大数据可视化展板通用模板'
        # 两个小的form看板
        self.counter = {'name': '服务器信息', 'value': 'AZURE Hong Kong (eastasia)'}
        self.counter2 = {'name': 'MongoDB数据总量', 'value': collection.count_documents({})}
        # 总共是6个图表，数据格式用json字符串，其中第3个图表是有3个小的图表组成的
        self.echart1_data = {
            'title': '岗位分布',
            'data': get_data_from_mongodb('岗位分布', collection)
        }
        self.echart2_data = {
            'title': '平均薪资 (k/月)',
            'data': get_data_from_mongodb('平均薪资', collection)
        }
        self.echarts3_1_data = {
            'title': '企业类型',
            'data': get_data_from_mongodb('企业类型', collection)
        }
        self.echarts3_2_data = {
            'title': '企业规模',
            'data': get_data_from_mongodb('企业规模', collection)
        }
        self.echarts3_3_data = {
            'title': '所属行业',
            'data': get_data_from_mongodb('所属行业', collection)
        }
        self.echart4_data = {
            'title': '薪资和工作年限 (k/月)',
            'data': get_data_from_mongodb('薪资和工作年限', collection),
            'xAxis': ['01', '03', '04', '05', '06', '07', '08']
        }
        self.echart5_data = {
            'title': '不同类型企业薪资待遇情况 (k/月)',
            'data': get_data_from_mongodb('不同类型企业薪资待遇情况', collection)
        }
        # 这是一个环状图，有颜色的加上没颜色的正好等于100，半径是外圈直径和内圈直径，左闭右开
        # 用各城市的数目/总岗位数*100
        self.echart6_data = {
            'title': '一线城市岗位数量',
            'data': get_data_from_mongodb('一线城市岗位数量', collection)
        }

        self.map_1_data = {
            'symbolSize': 1000,
            'data': [
                {'name': '北京', 'value': 500},
                {'name': '上海', 'value': 700},
                {'name': '广州', 'value': 900},
                {'name': '杭州', 'value': 600},
                {'name': '深圳', 'value': 1000}
            ]
        }

    @property
    def echart1(self):
        data = self.echart1_data
        echart = {
            'title': data.get('title'),
            # 第一次get获取到的是许多键值对，所以需要对每个键值对再次get
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')]
        }
        # 返回的是标题和对应的数据，并没有说用什么方式展现！
        return echart

    @property
    def echart2(self):
        data = self.echart2_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')]
        }
        return echart

    @property
    def echarts3_1(self):
        data = self.echarts3_1_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echarts3_2(self):
        data = self.echarts3_2_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echarts3_3(self):
        data = self.echarts3_3_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echart4(self):
        data = self.echart4_data
        echart = {
            'title': data.get('title'),
            'names': [i.get("name") for i in data.get('data')],
            'xAxis': data.get('xAxis'),
            'data': data.get('data'),
        }
        return echart

    @property
    def echart5(self):
        data = self.echart5_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echart6(self):
        data = self.echart6_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def map_1(self):
        data = self.map_1_data
        echart = {
            'symbolSize': data.get('symbolSize'),
            'data': data.get('data'),
        }
        return echart


class SourceData(SourceDataDemo):

    def __init__(self):
        """
        按照 SourceDataDemo 的格式覆盖数据即可
        """
        super().__init__()
        self.title = '51Job可视化大屏'
