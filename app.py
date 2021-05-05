from flask import Flask, render_template
from data import SourceData

app = Flask(__name__)


# Flask将index.html设置为起始路径
@app.route('/')
def render_index_page():
    data = SourceData()
    return render_template('index.html', form=data, title=data.title)


if __name__ == '__main__':
    app.run()
