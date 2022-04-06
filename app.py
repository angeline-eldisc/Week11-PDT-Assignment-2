from unicodedata import category
from flask import (
    Flask, request, render_template, session, flash, redirect, url_for, jsonify
)

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, EmailField
from wtforms.validators import InputRequired, EqualTo, Email, Length, ValidationError

from db import db_connection

app = Flask(__name__)
app.secret_key = '*&YUHJBHGT^&*DDGFS^$GDF^&G$DFD^GF$HH#GB$D%V'
    
class loginForm(FlaskForm):
    username = StringField('Username or E-mail', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class registerForm(FlaskForm):
    name = StringField('Full Name', validators=[InputRequired(), Length(min=5, message='Full name must be minimum 5 characters')])
    email = EmailField('E-mail', validators=[InputRequired(), Email(message='E-mail must be in email format')])
    username = StringField('Username', validators=[InputRequired(), Length(min=5, message='Username must be minimum 5 characters')])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, message='Password must be minimum 5 characters'), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Confirm Password', validators=[InputRequired()])
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['username']
        password = request.form['password']

        conn = db_connection()
        cur = conn.cursor()
        sql = "SELECT id, username, name FROM users WHERE username = '%s' OR email = '%s' AND password = '%s'" % (
            username, email, password)
        cur.execute(sql)
        user = cur.fetchone()

        error = ''
        category = ''
        if user is None:
            error = 'Wrong credentials. No user found'
            category = 'danger'
        else:
            session.clear()
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['name'] = user[2]
            return redirect(url_for('index'))

        flash(error, category)
        cur.close()
        conn.close()

    formLogin = loginForm()
    return render_template('login.html', form = formLogin)

@app.route('/register', methods=['GET', 'POST'])
def register():
    formRegister = registerForm()
    if request.method == 'POST':
        formRegister.validate_on_submit()
        try:
            username = request.form['username']
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            
            username.strip()
            name.strip()
            email.strip()
            password.strip()
            
            conn = db_connection()
            cur = conn.cursor()
            
            sql = "SELECT * FROM users WHERE username = '%s'" % (username)
            cur.execute(sql)
            countUsername = cur.fetchall()
            
            sql = "SELECT * FROM users WHERE email = '%s'" % (email)
            cur.execute(sql)
            countEmail = cur.fetchall()
            
            sql = "INSERT INTO users (username, name, email, password) VALUES ('%s', '%s', '%s', '%s')" % (username, name, email, password)
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            
            flash("Registration Success! Your account has been created.", "success")
            return redirect(url_for('login'))
        except (Exception):
            # flash('Username or E-mail must be unique!', 'warning')
            
            if countEmail:
                formRegister.email.errors.append('E-mail must be unique')
            if countUsername:
                formRegister.username.errors.append('Username must be unique')
            return render_template('register.html', form = formRegister)
        
    return render_template('register.html', form = formRegister)

@app.route('/')
def index():
    conn = db_connection()
    cur = conn.cursor()
    sql = "SELECT COUNT(title) FROM articles"
    cur.execute(sql)
    count_articles = cur.fetchone()
    
    if session and session.get('user_id'):
        sql = "SELECT COUNT(title) FROM articles WHERE user_id = '%s'" % (session.get('user_id'))
        cur.execute(sql)
        count_your_articles = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if session and session.get('user_id'):
        return render_template('home.html', count_articles = count_articles, count_your_articles = count_your_articles)
    return render_template('home.html', count_articles = count_articles)

@app.route('/articles')
def articles():
    conn = db_connection()
    cur = conn.cursor()
    sql = "SELECT id, title, body, user_id FROM articles ORDER BY title"
    cur.execute(sql)
    articles = cur.fetchall()
    code = "articles"
    cur.close()
    conn.close()

    return render_template('articles.html', articles = articles, code = code)

@app.route('/your_articles')
def your_articles():
    conn = db_connection()
    cur = conn.cursor()
    if session and session.get('user_id'):
        sql = "SELECT id, title, body, user_id FROM articles WHERE user_id = '%s' ORDER BY title" % (session.get('user_id'))
        cur.execute(sql)
        articles = cur.fetchall()
    else:
        articles = None
    code = "your_articles"
    cur.close()
    conn.close()

    return render_template('articles.html', articles = articles, code = code)

@app.route('/article/create', methods=['GET', 'POST'])
def create():
    # check if user is logged in
    if not session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.get_json() or {}

        if data.get('title') and data.get('body'):
            title = data.get('title', '')
            body = data.get('body', '')
            user_id = session.get('user_id')
            
            title = title.strip()
            body = body.strip()
            
            conn = db_connection()
            cur = conn.cursor()
            sql = "INSERT INTO articles (title, body, user_id) VALUES ('%s', '%s', '%d')" % (title, body, user_id)
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            
            flash("Success! Article successfully added.", "success")
            return jsonify({'Status': 200, 'message': 'Success', 'redirect': '/articles'})
        
        return jsonify({'Status': 500, 'message': 'No data submitted'})
            
    return render_template('create.html')


@app.route('/article/<int:article_id>', methods=['GET'])
def detail(article_id):
    conn = db_connection()
    cur = conn.cursor()
    sql = "SELECT articles.title, articles.body, users.name FROM articles JOIN users ON users.id = articles.user_id WHERE articles.user_id = %s" % (article_id)
    cur.execute(sql)
    article = cur.fetchone()
    cur.close()
    conn.close()
    
    return render_template('detail.html', article=article)

@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit(article_id):
    # check if user is logged in
    if not session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        conn = db_connection()
        cur = conn.cursor()
        title = request.form['title']
        body = request.form['body']
        title = title.strip()
        body = body.strip()
        
        sql_params = (title, body, article_id)
        
        sql = "UPDATE articles SET title = '%s', body = '%s' WHERE id = %d" % sql_params
        
        print(sql)
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()
        
        flash("Success! Article successfully edited.", "success")
        return redirect(url_for('articles'))

    conn = db_connection()
    cur = conn.cursor()
    sql = 'SELECT id, title, body FROM articles WHERE id = %s' % article_id
    cur.execute(sql)
    article = cur.fetchone()
    cur.close()
    conn.close()
    
    return render_template('edit.html', article = article)

@app.route('/article/<int:article_id>/delete', methods=['GET', 'POST'])
def delete(article_id):
    # check if user is logged in
    if not session:
        return redirect(url_for('login'))

    conn = db_connection()
    cur = conn.cursor()
    sql = 'DELETE FROM articles WHERE id = %s' % article_id
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
    
    flash("Success! Article successfully deleted.", "success")
    return jsonify({'status': 200, 'redirect': '/articles'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
