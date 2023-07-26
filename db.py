import os, psycopg2, string, random, hashlib

#postgresへの接続
def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

#ソルトの生成
def get_salt():
    charset = string.ascii_letters + string.digits

    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return hashed_password

#アカウント登録
def insert_user(name, email, password):
    sql = "INSERT INTO users VALUES(default, %s, %s, %s, %s, current_timestamp)"
    
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (name, email, hashed_password, salt))
        count = cursor.rowcount
        connection.commit()
        
    except psycopg2.DatabaseError:
        count = 0
        
    finally:
        cursor.close()
        connection.close()
        
    return count

#ユーザーログイン
def userslogin(email, password):
    sql = "SELECT password, salt FROM users WHERE email = %s"
    flg = False
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (email,))
        users = cursor.fetchone()
        
        if users != None:
            salt = users[1]
            
            haehed_password = get_hash(password, salt)
            
            if haehed_password == users[0]:
                flg = True
                
    except psycopg2.DatabaseError:
        flg = False
    
    finally:
        cursor.close()
        connection.close()
        
    return flg

#管理者ログイン
def adminlogin(email, password):
    sql = "SELECT password, salt FROM admin WHERE email = %s"
    flg = False
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (email,))
        users = cursor.fetchone()
        
        if users != None:
            salt = users[1]
            
            haehed_password = get_hash(password, salt)
            
            if haehed_password == users[0]:
                flg = True
                
    except psycopg2.DatabaseError:
        flg = False
    
    finally:
        cursor.close()
        connection.close()
        
    return flg

#図書登録
def insert_book(book_name, author, publisher):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        sql = "INSERT INTO book_all VALUES (default, %s, %s, %s, '貸出可能', current_timestamp)"
    
        cursor.execute(sql, (book_name, author, publisher))
        count = cursor.rowcount
        connection.commit()
    
    except psycopg2.DatabaseError:
        count = 0
        
    finally:
        cursor.close()
        connection.close()
    
    return count

#図書削除
def delete_book(book_id):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        sql = "DELETE FROM book_all WHERE book_id = %s"
    
        cursor.execute(sql, (book_id, ))
        count = cursor.rowcount
        connection.commit()
    
    except psycopg2.DatabaseError:
        count = 0
    
    finally:
        cursor.close()
        connection.close()
    
    return count

#図書編集
def update_book(book_name, author, publisher, book_id):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "UPDATE book_all SET book_name = %s, author = %s, publisher = %s WHERE book_id = %s"
    
    cursor.execute(sql, (book_name, author, publisher, book_id))
    connection.commit()
    
    cursor.close()
    connection.close()

#図書一覧
def book_all():
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT book_id, book_name, author, publisher, situ FROM book_all ORDER BY book_id ASC"
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

#貸出リスト
def lend_list():
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT No, user_id, book_id, lendday, returnday FROM lend ORDER BY No ASC"
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

#貸出
def book_lend(user_id, book_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "INSERT INTO lend VALUES(default, %s, %s, NOW(), NOW()+CAST('7 days' as INTERVAL))"
    
    cursor.execute(sql, (user_id, book_id))
    connection.commit()
    
    cursor.close()
    connection.close()

def bookupdate_lend(book_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "UPDATE book_all SET situ = '貸出中' WHERE book_id = %s"
    
    cursor.execute(sql, (book_id,))
    connection.commit()
    
    cursor.close()
    connection.close()

#返却
def book_return(book_id, user_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM lend WHERE book_id = %s AND user_id = %s"
    
    cursor.execute(sql, (book_id, user_id))
    connection.commit()
    
    cursor.close()
    connection.close()

def bookupdate_return(book_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "UPDATE book_all SET situ = '貸出可能' WHERE book_id = %s"
    
    cursor.execute(sql, (book_id, ))
    connection.commit()
    
    cursor.close()
    connection.close()

#ユーザー情報
def user_parson(name):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT id, name, email FROM users WHERE name LIKE %s"
    
    searchname = "%" + name + "%"
    cursor.execute(sql, (searchname,))
    results = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return results

#ユーザー編集
def update_user(name, email, id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "UPDATE users SET name = %s, email = %s WHERE id = %s"
    
    cursor.execute(sql, (name, email, id))
    connection.commit()
    
    cursor.close()
    connection.close()

#ユーザー削除
def user_delete(id):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        sql = "DELETE FROM users WHERE id = %s"
    
        cursor.execute(sql, (id, ))
        count = cursor.rowcount
        connection.commit()
    
    except psycopg2.DatabaseError:
        count = 0
    
    finally:
        cursor.close()
        connection.close()
    
    return count