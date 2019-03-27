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
    # 書き込み時
    if request.method == 'POST':
        date = datetime.now()
        name = request.form['name']
        msg = request.form['msg']
        post = Article(pub_date=date, name=name, msg=msg)
        db.session.add(post)
        db.session.commit()
        # 書き込み後はlatestと同じ処理
        # 2回同じ処理を書くのはダサいな
        sql = "SELECT * FROM (SELECT * FROM article ORDER BY pub_date DESC LIMIT 10) ORDER BY pub_date;"
        connection = db.session.connection()
        contents = connection.execute(sql)
        return render_template('index.html', contents = contents)
    
    if request.method == 'GET':
        # 初期値はlatest
        page = request.args.get('page', 'latest')
        # 全取得
        if  page == 'all':
            contents = Article.query.all()
            return render_template('index.html', contents = contents)

        # 頭から10件は簡単       
        if page == 'first':
            contents = Article.query.limit(10)
            return render_template('index.html', contents = contents)

        # 最新10件を取得するのに大苦戦
        if page == 'latest':
            # これはダメ
            # contents = Article.query.limit(-10)

            # sql文を直書き
            # 2回ORDER BY させる
            sql = "SELECT * FROM (SELECT * FROM article ORDER BY pub_date DESC LIMIT 10) ORDER BY pub_date;"
            connection = db.session.connection()
            contents = connection.execute(sql)
            return render_template('index.html', contents = contents)
    
    # GETでもPOSTでもないとき
    else:
        contents = Article.query.all()
        return render_template('index.html', contens = contents)
    

if __name__ == '__main__':
    app.run()