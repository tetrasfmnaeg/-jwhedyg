from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # セッションのための秘密鍵

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)

@app.route('/')
def index():
    messages = Message.query.all()  # メッセージを全て取得
    return render_template('index.html', messages=messages)

@app.route('/post_message', methods=['POST'])
def post_message():
    name = request.form['name']
    content = request.form['content']
    
    # セッションに名前を保存
    session['username'] = name

    new_message = Message(name=name, content=content)
    db.session.add(new_message)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete_message/<int:id>', methods=['POST'])
def delete_message(id):
    message_to_delete = Message.query.get_or_404(id)
    delete_name = request.form['delete_name']
    
    # セッションに保存された名前とメッセージの投稿者名が一致する場合に削除
    if message_to_delete.name == delete_name:
        db.session.delete(message_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        error = "名前が一致しません"
        messages = Message.query.all()
        return render_template('index.html', messages=messages, error=error)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # 初回実行時にテーブルを作成
    app.run(debug=True)

