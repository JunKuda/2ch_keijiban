from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
app = Flask(__name__)

# データベースの立ち上げ
db_uri = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

# 書き込み内容のDB
class Article(db.Model):
    # 内容はプライマイキー、投稿日、名前、本文
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.Text())
    msg = db.Column(db.Text())

@app.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        date = datetime.now()
        name = request.form['name']
        msg = request.form['msg']
        post = Article(pub_date=date, name=name, msg=msg)
        db.session.add(post)
        db.session.commit()
        contents = Article.query.all()
        return render_template('index.html', contents = contents)

    contents = Article.query.all()
    return render_template('index.html', contents=contents)
    

if __name__ == '__main__':
    app.run()