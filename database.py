import sqlite3

connection =sqlite3.connect('market.db')
sql =connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS user(tg_id INTEGER, name TEXT,number TEXT,address TEXT,red_date DATETIME);')
sql.execute('CREATE TABLE IF NOT EXISTS sklad(pr_id INTEGER PRIMARY KEY AUTOINCREMENT, pr_name TEXT,pr_price REAL, pr_quantity INTEGER,'
            'pr_desc DATETIME,pr_photo TEXT,pr_reg_date DATETIME);')
sql.execute('CREATE TABLE IF NOT EXISTS cart(tg_id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,user_product,quantity INTEGER,'
            'total_for_product REAL);')

def registration(tg_id,name,number,address):
    connection = sqlite3.connect('market.db')
    sql = connection.cursor()
    sql.execute(' INSERT INTO user(tg_id,name,number,address) VALUES(?, ?, ?, ?);', (tg_id,name,number,address))

    connection.commit()

def check_user(user_id):
    connection = sqlite3.connect('market.db')
    sql = connection.cursor()
    cheker = sql.execute('SELECT tg_id FROM user WHERE tg_id=?;', (user_id, ))
    if cheker.fetchone():
        return True
    else:
        return False

def add_to_cart(pr_name,pr_price,pr_quantity,pr_desc,pr_photo):
    connection = sqlite3.connect('market.db')
    sql = connection.cursor()
    sql.execute('INSERT INTO sklad'
                '(pr_name,pr_price,pr_quantity,pr_desc,pr_photo) VALUES'
                '(?, ?, ?, ?, ?)', (pr_name,pr_price,pr_quantity,pr_desc,pr_photo))
    connection.commit()

def delete_from_skald():
    connection = sqlite3.connect('market.db')
    sql = connection.cursor()
    sql.execute('DELETE FROM sklad;')

def delete_execute_from_sklad(pr_id):
    connection = sqlite3.connect('market.db')
    sql = connection.cursor()
    sql.execute('DELETE FROM sklad WHERE pr_id=?;', (pr_id, ))

def get_product_name():
    connection = sqlite3.connect('market.db')
    sql = connection.cursor()
    products = sql.execute('SELECT pr_name, pr_id, pr_quantity FROM sklad;').fetchall()
    sorted_product = [(i[0],i[1]) for i in products if i[2] > 0]
    return sorted_product

def get_product_id():
    connection = sqlite3.connect('market.db')
    sql = connection.cursor()
    products = sql.execute('SELECT pr_name, pr_id, pr_quantity FROM sklad;').fetchall()
    sorted_product = [i[1] for i in products if i[2] > 0]
    return sorted_product

def exact_product(pr_id):
    connection = sqlite3.connect('market.db')
    sql = connection.cursor()
    exact_product = sql.execute('SELECT pr_photo, pr_desc, pr_price FROM sklad WHERE pr_id=?;', (pr_id, )).fetchone()
    return exact_product

def add_product_to_cart(user_id, user_product, quantity):
    connection = sqlite3.connect('market.db')
    sql = connection.cursor()
    product_price = exact_product(user_product)[2]
    sql.execute('INSERT INTO cart'
                '(user_id,user_product,quantity,total_for_product) VALUES'
                '(?,?,?,?);', (user_id,user_product,quantity,quantity * product_price))
    connection.commit()

def delete_exect_kor(pr_id, user_id):
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()
    sql.execute('DELETE FROM korzina WHERE user_product = ? AND user_id=?;', (pr_id,user_id))
    connection.commit()

def get_exect_product_from_cart(user_id):
    connection = sqlite3.connect('market.db')
    sql = connection.cursor()
    cart =sql.execute('SELECT sklad.pr_name, cart.quantity,cart.total_for_product FROM cart INNER JOIN sklad ON pr_id=cart.user_product WHERE user_id=?;', (user_id, )).fetchall()
    return cart

def delete_cart(user_id):
    connection = sqlite3.connect('market.db')
    sql = connection.cursor()
    sql.execute('DELETE FROM cart WHERE user_id=?;', (user_id, ))
    connection.commit()

def get_user_number_name(user_id):
    connection = sqlite3.connect('market.db')
    sql = connection.cursor()
    exect_user =sql.execute('SELECT name, number FROM user WHERE tg_id=?;', (user_id, ))
    return exect_user.fetchone()