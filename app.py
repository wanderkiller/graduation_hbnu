from flask import Flask, render_template
from data import SourceData

app = Flask(__name__)


# Flask将index.html设置为起始路径
@app.route('/')
def render_index_page():
    data = SourceData()
    return render_template('index.html', form=data, title=data.title)


# @app.route('/chart')
# def render_chart_page():
#     pipeline = [{'$match': {'workarea_text': '深圳'}},
#                 {'$group': {'_id': '$workyear', 'avg': {'$avg': '$providesalary_text'}}},
#                 {'$sort': {'_id': 1}}]
#     x = generate_list_for_matplotlib(get_data_from_mongodb(pipeline), '_id')
#     y = generate_list_for_matplotlib(get_data_from_mongodb(pipeline), 'avg')
#     imd = draw_chart('plot', x_asis=x, y_asis=y, x_label='Work years', y_label='Average salary')
#     return render_template('register.html', img=imd)
#

if __name__ == '__main__':
    app.run()
