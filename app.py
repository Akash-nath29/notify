import os
from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from sqlalchemy.sql import func
# from datetime import date

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'

pagedown = PageDown(app)

db = SQLAlchemy(app)


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    noticename = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def __init__(self, noticename, body):
        self.noticename = noticename
        self.body = body


@app.route('/')
def index():
    notices = Notice.query.order_by(Notice.created_at.desc()).all()
    return render_template('index.html', notices=notices)

@app.route('/add_record')
def add_record():
    return render_template('addRecord.html')

@app.route('/add_notice', methods=['GET', 'POST'])
def addNotice():
    if request.method == 'POST':
        name = request.form.get("noticename")
        body = request.form.get("noticebody")
        newNotice = Notice(name, body)
        db.session.add(newNotice)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='80')