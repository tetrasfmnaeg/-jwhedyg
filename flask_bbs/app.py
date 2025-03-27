from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# アプリケーションとデータベースの設定
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'  # SQLiteを使用
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 不要な警告を無効化

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# メッセージのデータベースモデル
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<Message {self.id}>'


# メインページの表示（メッセージの表示）
@app.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)


# メッセージの追加
@app.route('/add', methods=['POST'])
def add_message():
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        new_message = Message(name=name, content=content)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('index'))


# メッセージの削除
@app.route('/delete/<int:id>', methods=['POST'])
def delete_message(id):
    message_to_delete = Message.query.get_or_404(id)
    db.session.delete(message_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


# アプリケーションの起動
if __name__ == '__main__':
    app.run(debug=True)

