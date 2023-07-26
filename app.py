from flask import Flask, render_template, request, redirect,url_for,session
import db,string,random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

#ログイン画面
@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    
    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg=msg)

#ユーザーログイン
@app.route('/', methods=['POST'])
def userlogin():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if db.userslogin(email, password):
        session['user'] = True
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=10)
        return redirect(url_for('userhome'))
    else:
        error = 'メールアドレスまたはパスワードが違います'
        
        input_data = {'email':email, 'password':password}
        return render_template('index.html', error=error, data=input_data)

#管理者ログイン
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/adminlogin', methods=['POST'])
def adminlogin():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if db.adminlogin(email, password):
        session['admin'] = True
        from datetime import timedelta
        return redirect(url_for('adminhome'))
    else:
        error = 'メールアドレスまたはパスワードが違います'
        
        input_data = {'email':email, 'password':password}
        return render_template('admin.html', error=error, data=input_data)

#ログアウト
@app.route('/userlogout')
def userlogout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/adminlogout')
def adminlogout():
    session.pop('admin', None)
    return redirect(url_for('index'))

#アカウント登録
@app.route('/accountregister')
def accountregister():
    return render_template('accountregister.html')

@app.route('/accountregistercompletion', methods=['POST'])
def accountregi_completion():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if name == '':
        error = 'ユーザー名が入力されていません'
        return render_template('accountregister.html', error=error, name=name, email=email, password=password)
    if email == '':
        error = 'メールアドレスが入力されていません'
        return render_template('accountregister.html', error=error, name=name, email=email, password=password)
    if password == '':
        error = 'パスワードが入力されていません'
        return render_template('accountregister.html', error=error, name=name, email=email)
    
    count = db.insert_user(name, email, password)
    
    if count == 1:
        msg = '登録が完了しました'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('accountregister.html', error=error)

#ユーザー画面
@app.route('/userhome', methods=['GET'])
def userhome():
    return render_template('userhome.html')

#管理者画面
@app.route('/adminhome', methods=['GET'])
def adminhome():
    return render_template('adminhome.html')

#貸出一覧
@app.route('/lendlist')
def lendlist():
    lend_book = db.lend_list()
    return render_template('lendall.html', book=lend_book)

#図書一覧
@app.route('/bookalluser')
def bookallU():
    allbooku = db.book_all()
    return render_template('bookallU.html', book=allbooku)

@app.route('/bookalladmin')
def bookallA():
    allbooka = db.book_all()
    return render_template('bookallA.html', book=allbooka)

#図書登録
@app.route('/bookregister')
def bookregister():
    return render_template('bookregi.html')

@app.route('/bookregistercompletion', methods=['POST'])
def bookregi_completion():
    book_name = request.form.get('book_name')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    
    if book_name == '':
        error = '図書名が入力されていません'
        return render_template('bookregi.html', error=error, book_name=book_name, author=author, publisher=publisher)
    if author == '':
        error = '著者が入力されていません'
        return render_template('bookregi.html', error=error, book_name=book_name, author=author, publisher=publisher)
    if publisher == '':
        error = '出版社が入力されていません'
        return render_template('bookregi.html', error=error, book_name=book_name, author=author, publisher=publisher)
    
    count = db.insert_book(book_name, author, publisher)
    
    if count == 1:
        return render_template('bookregicomp.html')
    else:
        error = '登録できませんでした'
        return render_template('bookregi.html', error=error)

#図書削除
@app.route('/bookdelete')
def bookdelete():
    return render_template('bookdele.html')

@app.route('/bookdeletecompletion', methods=['POST'])
def bookdele_completion():
    book_id = request.form.get('book_id')
    
    if book_id == '':
        error = '図書IDが入力されていません'
        return render_template('bookdele.html', error=error, book_id=book_id)
    
    count = db.delete_book(book_id)
    
    if count == 1:
        return render_template('bookdelecomp.html')
    else:
        error = '削除できませんでした'
        return render_template('bookdele.html', error=error)

#図書編集
@app.route('/bookupdate')
def bookupdate():
    return render_template('bookup.html')

@app.route('/bookupdatecompletion', methods=['POST'])
def bookup_completion():
    book_name = request.form.get('book_name')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    book_id = request.form.get('book_id')
    
    if book_name == '':
        error = '図書名が入力されていません'
        return render_template('bookup.html', error=error, book_name=book_name, author=author, publisher=publisher, book_id=book_id)
    if author == '':
        error = '著者が入力されていません'
        return render_template('bookup.html', error=error, book_name=book_name, author=author, publisher=publisher, book_id=book_id)
    if publisher == '':
        error = '出版社が入力されていません'
        return render_template('bookup.html', error=error, book_name=book_name, author=author, publisher=publisher, book_id=book_id)
    if book_id == '':
        error = '図書IDが入力されていません'
        return render_template('bookup.html', error=error, book_name=book_name, author=author, publisher=publisher, book_id=book_id)
    
    db.update_book(book_name, author, publisher, book_id)
    
    return render_template('bookupcomp.html')

#貸出
@app.route('/lend')
def lend():
    return render_template('lend.html')

@app.route('/lend_completion', methods=['POST'])
def lend_completion():
    user_id = request.form.get('user_id')
    book_id = request.form.get('book_id')
    
    if user_id == '':
        error = 'ユーザーIDが入力されていません'
        return render_template('lend.html', error=error, user_id=user_id, book_id=book_id)
    if book_id == '':
        error = '図書IDが入力されていません'
        return render_template('lend.html', error=error, user_id=user_id, book_id=book_id)
    
    db.book_lend(user_id,book_id)
    db.bookupdate_lend(book_id)
    return render_template('lendcomp.html')

#返却
@app.route('/return')
def returnbook():
    return render_template('return.html')

@app.route('/return_completion', methods=['POST'])
def return_completion():
    book_id = request.form.get('book_id')
    user_id = request.form.get('user_id')
    
    if user_id == '':
        error = 'ユーザーIDが入力されていません'
        return render_template('lend.html', error=error, user_id=user_id, book_id=book_id)
    if book_id == '':
        error = '図書IDが入力されていません'
        return render_template('lend.html', error=error, user_id=user_id, book_id=book_id)
    
    db.book_return(book_id,user_id)
    db.bookupdate_return(book_id)
    return render_template('returncomp.html')

#ユーザー情報
@app.route('/user_search')
def user_search():
    return render_template('usersearch.html')

@app.route('/user_infomation', methods=['POST'])
def user_infomation():
    name = request.form.get('name')
    
    if name == '':
        error = 'ユーザー名が入力されていません'
        return render_template('usersearch.html', error=error, name=name)
    
    user = db.user_parson(name)
    return render_template('userinfo.html', users=user)

#ユーザー編集
@app.route('/user_update')
def user_update():
    return render_template('userup.html')

@app.route('/userup_completion', methods=['POST'])
def userup_completion():
    name = request.form.get('name')
    email = request.form.get('email')
    id = request.form.get('id')
    
    if name == '':
        error = 'ユーザー名が入力されていません'
        return render_template('userup.html', error=error, name=name, email=email, id=id)
    if email == '':
        error = 'メールアドレスが入力されていません'
        return render_template('userup.html', error=error, name=name, email=email, id=id)
    if id == '':
        error = 'ユーザーIDが入力されていません'
        return render_template('userup.html', error=error, name=name, email=email, id=id)
    
    db.update_user(name, email, id)
    
    return redirect(url_for('userhome'))

#アカウント削除
@app.route('/userdelete')
def user_delete():
    return render_template('userdele.html')

@app.route('/userdeletecompletion', methods=['POST'])
def userdele_completion():
    id = request.form.get('id')
    
    if id == '':
        error = 'ユーザーIDが入力されていません'
        return render_template('userdele.html', error=error, id=id)
    
    count = db.user_delete(id)
    
    if count == 1:
        return redirect(url_for('index'))
    else:
        error = '削除できませんでした'
        return render_template('userdele.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)