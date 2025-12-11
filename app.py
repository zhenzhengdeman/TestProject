from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
# 1. 初始化 Flask 网站
app = Flask(__name__)

# 2. 配置数据库地址
# sqlite:///books.db 意思是：在当前文件夹下创建一个叫 books.db 的文件作为数据库
# SQLite 是最轻量级的数据库，不需要安装软件，就是一个文件，非常适合学习
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
# 关闭一个不必要的追踪功能，省点内存
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. 初始化数据库插件
db = SQLAlchemy(app)


# 4. 定义 "书" 的模型 (这就是 ORM 的核心！)
# 我们定义一个 Python 类，数据库会自动把它变成一张表
class Book(db.Model):
    # id 是主键 (Primary Key)，就像书的身份证号，自动生成 (1, 2, 3...)
    id = db.Column(db.Integer, primary_key=True)
    # title 是书名，String(80) 表示最多80个字，nullable=False 表示不能为空
    title = db.Column(db.String(80), nullable=False)
    # price 是价格，Float 表示小数
    price = db.Column(db.Float, nullable=False)
    # author是作者
    author = db.Column(db.String(50), nullable=False)

    # 这是一个可选的方法，为了让打印出来的书更好看
    def __repr__(self):
        return f'<书名: {self.title}, 价格: {self.price}>'

# 这是新加的路由
@app.route('/', methods=['GET', 'POST'])
def index():
    # 如果是 POST 请求，说明用户点击了“添加”按钮
    if request.method == 'POST':
        # 1. 从表单里拿数据 (根据 HTML 里的 name="...")
        book_title = request.form.get('title')
        book_price = request.form.get('price')
        book_author = request.form.get('author')

        # 2. 创建新书对象
        new_book = Book(title=book_title, price=float(book_price), author=book_author)

        # 3. 存入数据库
        db.session.add(new_book)
        db.session.commit()

        # 4. 事情办完了，刷新一下页面 (重定向回首页)
        # 这样用户就能立刻看到新加的书了
        return redirect('/')

    # 如果是 GET 请求 (平时访问)，就正常显示书单
    books = Book.query.all()
    return render_template('index.html', books=books)


# 这里的 <int:id> 是一个占位符
# 比如你访问 /delete/5，这里的 id 就会变成 5
@app.route('/delete/<int:id>')
def delete_book(id):
    # 1. 根据 ID 去数据库里找这本书
    book_to_delete = Book.query.get_or_404(id)

    # 2. 从数据库删除
    db.session.delete(book_to_delete)

    # 3. 提交更改 (别忘了！)
    db.session.commit()

    # 4. 删完后，回到首页看看结果
    return redirect('/')

# 5. 让 Flask 跑起来，并创建数据库
if __name__ == '__main__':
    # 这一步非常重要：它会检测有没有 books.db，如果没有，就根据上面的 Class 自动创建！
    with app.app_context():
        db.create_all()
        print("✅ 数据库 books.db 和数据表已成功创建！")
    # 启动网站模式
    app.run(host="0.0.0.0",port=5000, debug=True)