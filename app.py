from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure secret key
DATABASE = 'quotes.db'

# Database Initialization

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 email TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS quotes (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 quote TEXT NOT NULL,
                 author TEXT NOT NULL,
                 explanation TEXT NOT NULL,
                 section TEXT NOT NULL,
                 timestamp DATETIME,
                 completed INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def ensure_completed_column():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("PRAGMA table_info(quotes)")
    columns = [row[1] for row in c.fetchall()]
    if 'completed' not in columns:
        c.execute("ALTER TABLE quotes ADD COLUMN completed INTEGER DEFAULT 0")
        conn.commit()
    conn.close()


init_db()
ensure_completed_column()

# Authentication & User Management

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        c = conn.cursor()
        try:
            hashed_password = generate_password_hash(password)
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                     (username, email, hashed_password))
            conn.commit()
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email or username already exists.', 'error')
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Quotes Management

@app.route('/home')
@login_required
def home():
    return render_template('home.html', username=session.get('username'))

@app.route('/section/<section_name>')
def section_home(section_name):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', (section_name,))
    quotes = c.fetchall()
    conn.close()
    return render_template('home.html', quotes=quotes, section=section_name)


@app.route('/create_draft/<section_name>')
def create_draft(section_name):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section) VALUES (?, ?, ?, ?)', ("", "", "", section_name))
    conn.commit()
    draft_id = c.lastrowid
    conn.close()
    return redirect(url_for('new_quote', section_name=section_name, draft_id=draft_id))

@app.route('/new/<section_name>')
def new_quote(section_name):
    draft_id = request.args.get('draft_id')
    return render_template('index.html', section=section_name, draft_id=draft_id)

@app.route('/submitloveq_form', methods=['POST'])
def submitloveq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'loveq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('loveq'))

@app.route('/submitlovep_form', methods=['POST'])
def submitlovep_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lovep', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lovep'))

@app.route('/submitlifep_form', methods=['POST'])
def submitlifep_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lifep', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lifep'))

@app.route('/submitlifeq_form', methods=['POST'])
def submitlifeq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lifeq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lifeq'))

@app.route('/submitwisdomq_form', methods=['POST'])
def submitwisdomq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'wisdomq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('wisdomq'))

@app.route('/submitsadq_form', methods=['POST'])
def submitsadq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'sadq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('sadq'))

@app.route('/submitmotivationq_form', methods=['POST'])
def submitmotivationq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'motivationq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('motivationq'))

@app.route('/submitsuccessq_form', methods=['POST'])
def submitsuccessq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'successq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('successq'))

@app.route('/submitwisdomp_form', methods=['POST'])
def submitwisdomp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'wisdomp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('wisdomp'))

@app.route('/submitsadp_form', methods=['POST'])
def submitsadp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'sadp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('sadp'))

@app.route('/submitmotivationp_form', methods=['POST'])
def submitmotivationp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'motivationp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('motivationp'))

@app.route('/submitsuccessp_form', methods=['POST'])
def submitsuccessp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'successp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('successp'))

#french
@app.route('/submitlovefq_form', methods=['POST'])
def submitlovefq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lovefq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lovefq'))

@app.route('/submitlovefp_form', methods=['POST'])
def submitlovefp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lovefp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lovefp'))

@app.route('/submitlifefp_form', methods=['POST'])
def submitlifefp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lifefp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lifefp'))

@app.route('/submitlifefq_form', methods=['POST'])
def submitlifefq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lifefq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lifefq'))

@app.route('/submitwisdomfq_form', methods=['POST'])
def submitwisdomfq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'wisdomfq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('wisdomfq'))

@app.route('/submitsadfq_form', methods=['POST'])
def submitsadfq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'sadfq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('sadfq'))

@app.route('/submitmotivationfq_form', methods=['POST'])
def submitmotivationfq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'motivationfq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('motivationfq'))

@app.route('/submitsuccessfq_form', methods=['POST'])
def submitsuccessfq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'successfq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('successfq'))

@app.route('/submitwisdomfp_form', methods=['POST'])
def submitwisdomfp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'wisdomfp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('wisdomfp'))

@app.route('/submitsadfp_form', methods=['POST'])
def submitsadfp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'sadfp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('sadfp'))

@app.route('/submitmotivationfp_form', methods=['POST'])
def submitmotivationfp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'motivationfp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('motivationfp'))

@app.route('/submitsuccessfp_form', methods=['POST'])
def submitsuccessfp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'successfp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('successfp'))
#french
#chinese
@app.route('/submitlovecq_form', methods=['POST'])
def submitlovecq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lovecq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lovecq'))

@app.route('/submitlovecp_form', methods=['POST'])
def submitlovecp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lovecp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lovecp'))

@app.route('/submitlifecp_form', methods=['POST'])
def submitlifecp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lifecp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lifecp'))

@app.route('/submitlifecq_form', methods=['POST'])
def submitlifecq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lifecq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lifecq'))

@app.route('/submitwisdomcq_form', methods=['POST'])
def submitwisdomcq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'wisdomcq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('wisdomcq'))

@app.route('/submitsadcq_form', methods=['POST'])
def submitsadcq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'sadcq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('sadcq'))

@app.route('/submitmotivationcq_form', methods=['POST'])
def submitmotivationcq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'motivationcq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('motivationcq'))

@app.route('/submitsuccesscq_form', methods=['POST'])
def submitsuccesscq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'successcq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('successcq'))

@app.route('/submitwisdomcp_form', methods=['POST'])
def submitwisdomcp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'wisdomcp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('wisdomcp'))

@app.route('/submitsadcp_form', methods=['POST'])
def submitsadcp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'sadcp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('sadcp'))

@app.route('/submitmotivationcp_form', methods=['POST'])
def submitmotivationcp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'motivationcp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('motivationcp'))

@app.route('/submitsuccesscp_form', methods=['POST'])
def submitsuccesscp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'successcp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('successcp'))

#chinese
#German
@app.route('/submitlovegq_form', methods=['POST'])
def submitlovegq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lovegq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lovegq'))

@app.route('/submitlovegp_form', methods=['POST'])
def submitlovegp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lovegp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lovegp'))

@app.route('/submitlifegp_form', methods=['POST'])
def submitlifegp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lifegp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lifegp'))

@app.route('/submitlifegq_form', methods=['POST'])
def submitlifegq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lifegq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lifegq'))

@app.route('/submitwisdomgq_form', methods=['POST'])
def submitwisdomgq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'wisdomgq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('wisdomgq'))

@app.route('/submitsadgq_form', methods=['POST'])
def submitsadgq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'sadgq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('sadgq'))

@app.route('/submitmotivationgq_form', methods=['POST'])
def submitmotivationgq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'motivationgq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('motivationgq'))

@app.route('/submitsuccessgq_form', methods=['POST'])
def submitsuccessgq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'successgq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('successgq'))

@app.route('/submitwisdomgp_form', methods=['POST'])
def submitwisdomgp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'wisdomgp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('wisdomgp'))

@app.route('/submitsadgp_form', methods=['POST'])
def submitsadgp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'sadgp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('sadgp'))

@app.route('/submitmotivationgp_form', methods=['POST'])
def submitmotivationgp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'motivationgp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('motivationgp'))

@app.route('/submitsuccessgp_form', methods=['POST'])
def submitsuccessgp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'successgp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('successgp'))
#German
#Spanish
@app.route('/submitlovesq_form', methods=['POST'])
def submitlovesq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lovesq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lovesq'))

@app.route('/submitlovesp_form', methods=['POST'])
def submitlovesp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lovesp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lovesp'))

@app.route('/submitlifesp_form', methods=['POST'])
def submitlifesp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lifesp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lifesp'))

@app.route('/submitlifesq_form', methods=['POST'])
def submitlifesq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lifesq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lifesq'))

@app.route('/submitwisdomsq_form', methods=['POST'])
def submitwisdomsq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'wisdomsq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('wisdomsq'))

@app.route('/submitsadsq_form', methods=['POST'])
def submitsadsq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'sadsq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('sadsq'))

@app.route('/submitmotivationsq_form', methods=['POST'])
def submitmotivationsq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'motivationsq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('motivationsq'))

@app.route('/submitsuccesssq_form', methods=['POST'])
def submitsuccesssq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'successsq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('successsq'))

@app.route('/submitwisdomsp_form', methods=['POST'])
def submitwisdomsp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'wisdomsp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('wisdomsp'))

@app.route('/submitsadsp_form', methods=['POST'])
def submitsadsp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'sadsp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('sadsp'))

@app.route('/submitmotivationsp_form', methods=['POST'])
def submitmotivationsp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'motivationsp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('motivationsp'))

@app.route('/submitsuccesssp_form', methods=['POST'])
def submitsuccesssp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'successsp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('successsp'))
#Spanish
#Hindi
@app.route('/submitlovehq_form', methods=['POST'])
def submitlovehq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lovehq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lovehq'))

@app.route('/submitlovehp_form', methods=['POST'])
def submitlovehp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lovehp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lovehp'))

@app.route('/submitlifehp_form', methods=['POST'])
def submitlifehp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lifehp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lifehp'))

@app.route('/submitlifehq_form', methods=['POST'])
def submitlifehq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'lifehq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('lifehq'))

@app.route('/submitwisdomhq_form', methods=['POST'])
def submitwisdomhq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'wisdomhq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('wisdomhq'))

@app.route('/submitsadhq_form', methods=['POST'])
def submitsadhq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'sadhq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('sadhq'))

@app.route('/submitmotivationhq_form', methods=['POST'])
def submitmotivationhq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'motivationhq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('motivationhq'))

@app.route('/submitsuccesshq_form', methods=['POST'])
def submitsuccesshq_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'successhq', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('successhq'))

@app.route('/submitwisdomhp_form', methods=['POST'])
def submitwisdomhp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'wisdomhp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('wisdomhp'))

@app.route('/submitsadhp_form', methods=['POST'])
def submitsadhp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'sadhp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('sadhp'))

@app.route('/submitmotivationhp_form', methods=['POST'])
def submitmotivationhp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'motivationhp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('motivationhp'))

@app.route('/submitsuccesshp_form', methods=['POST'])
def submitsuccesshp_form():
    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']

    # Save to DB with section='loveq'
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO quotes (quote, author, explanation, section, completed, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (quote, author, explanation, 'successhp', 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return redirect(url_for('successhp'))
#Hindi

@app.route('/submit', methods=['POST'])
def submit():
    draft_id = request.form.get('draft_id')
    quote = request.form.get('quote')
    author = request.form.get('author')
    explanation = request.form.get('explanation')
    section = request.form.get('section')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE quotes SET quote = ?, author = ?, explanation = ?, timestamp = ?, completed = 1 WHERE id = ?', (quote, author, explanation, timestamp, draft_id))
    conn.commit()
    conn.close()
    return redirect(url_for('section_home', section_name=section))

@app.route('/submit/<section>', methods=['POST'])
def submit_form(section):

    quote = request.form['quote']
    author = request.form['author']
    explanation = request.form['explanation']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    new_entry = {
        'quote': quote,
        'author': author,
        'explanation': explanation,
        'timestamp': timestamp
    }

    quotes_data[section].append(new_entry)
    return redirect(url_for(section))  # Redirect back to the right page


@app.route('/cancel/<int:draft_id>/<section_name>')
def cancel(draft_id, section_name):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM quotes WHERE id = ?', (draft_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('section_home', section_name=section_name))

@app.route('/top')
def top_quotes():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE completed = 1 ORDER BY timestamp DESC LIMIT 5')
    quotes = c.fetchall()
    conn.close()
    return render_template('top.html', quotes=quotes)

@app.route('/quotes')
def quotes():
    return render_template('quotes.html')

@app.route('/proverbs')
def proverbs():
    return render_template('proverbs.html')

@app.route('/spanish')
def spanish():
    return render_template('spanish.html')

@app.route('/hindi')
def hindi():
    return render_template('hindi.html')

@app.route('/german')
def german():
    return render_template('german.html')

@app.route('/chinese')
def chinese():
    return render_template('chinese.html')

#chinese
@app.route('/lovecp')
def lovecp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lovecp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lovecp.html', quotes=quotes)


@app.route('/successcp')
def successcp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('successcp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('successcp.html', quotes=quotes)

@app.route('/motivationcp')
def motivationcp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('motivationcp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('motivationcp.html', quotes=quotes)

@app.route('/wisdomcp')
def wisdomcp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('wisdomcp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('wisdomcp.html', quotes=quotes)

@app.route('/sadcp')
def sadcp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('sadcp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('sadcp.html', quotes=quotes)

@app.route('/lifecp')
def lifecp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lifecp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lifecp.html', quotes=quotes)


@app.route('/lovecq')
def lovecq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lovecq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lovecq.html', quotes=quotes)



@app.route('/successcq')
def successcq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('successcq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('successcq.html', quotes=quotes)

@app.route('/motivationcq')
def motivationcq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('motivationcq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('motivationcq.html', quotes=quotes)

@app.route('/wisdomcq')
def wisdomcq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('wisdomcq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('wisdomcq.html', quotes=quotes)

@app.route('/sadcq')
def sadcq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('sadcq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('sadcq.html', quotes=quotes)

@app.route('/lifecq')
def lifecq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lifecq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lifecq.html', quotes=quotes)
#chinese
#french
@app.route('/lovefp')
def lovefp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lovefp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lovefp.html', quotes=quotes)


@app.route('/successfp')
def successfp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('successfp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('successfp.html', quotes=quotes)

@app.route('/motivationfp')
def motivationfp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('motivationfp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('motivationfp.html', quotes=quotes)

@app.route('/wisdomfp')
def wisdomfp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('wisdomfp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('wisdomfp.html', quotes=quotes)

@app.route('/sadfp')
def sadfp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('sadfp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('sadfp.html', quotes=quotes)

@app.route('/lifefp')
def lifefp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lifefp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lifefp.html', quotes=quotes)


@app.route('/lovefq')
def lovefq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lovefq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lovefq.html', quotes=quotes)



@app.route('/successfq')
def successfq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('successfq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('successfq.html', quotes=quotes)

@app.route('/motivationfq')
def motivationfq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('motivationfq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('motivationfq.html', quotes=quotes)

@app.route('/wisdomfq')
def wisdomfq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('wisdomfq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('wisdomfq.html', quotes=quotes)

@app.route('/sadfq')
def sadfq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('sadfq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('sadfq.html', quotes=quotes)

@app.route('/lifefq')
def lifefq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lifefq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lifefq.html', quotes=quotes)

#french
#Hindi
@app.route('/lovehp')
def lovehp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lovehp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lovehp.html', quotes=quotes)


@app.route('/successhp')
def successhp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('successhp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('successhp.html', quotes=quotes)

@app.route('/motivationhp')
def motivationhp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('motivationhp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('motivationhp.html', quotes=quotes)

@app.route('/wisdomhp')
def wisdomhp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('wisdomhp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('wisdomhp.html', quotes=quotes)

@app.route('/sadhp')
def sadhp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('sadhp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('sadhp.html', quotes=quotes)

@app.route('/lifehp')
def lifehp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lifehp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lifehp.html', quotes=quotes)


@app.route('/lovehq')
def lovehq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lovehq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lovehq.html', quotes=quotes)



@app.route('/successhq')
def successhq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('successhq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('successhq.html', quotes=quotes)

@app.route('/motivationhq')
def motivationhq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('motivationhq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('motivationhq.html', quotes=quotes)

@app.route('/wisdomhq')
def wisdomhq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('wisdomhq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('wisdomhq.html', quotes=quotes)

@app.route('/sadhq')
def sadhq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('sadhq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('sadhq.html', quotes=quotes)

@app.route('/lifehq')
def lifehq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lifehq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lifehq.html', quotes=quotes)
#Hindi

@app.route('/french')
def french():
    return render_template('french.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/habout')
def habout():
    return render_template('habout.html')

@app.route('/sabout')
def sabout():
    return render_template('sabout.html')

@app.route('/gabout')
def gabout():
    return render_template('gabout.html')

@app.route('/cabout')
def cabout():
    return render_template('cabout.html')

@app.route('/fabout')
def fabout():
    return render_template('fabout.html')
#German
@app.route('/lovegp')
def lovegp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lovegp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lovegp.html', quotes=quotes)


@app.route('/successgp')
def successgp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('successgp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('successgp.html', quotes=quotes)

@app.route('/motivationgp')
def motivationgp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('motivationgp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('motivationgp.html', quotes=quotes)

@app.route('/wisdomgp')
def wisdomgp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('wisdomgp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('wisdomgp.html', quotes=quotes)

@app.route('/sadgp')
def sadgp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('sadgp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('sadgp.html', quotes=quotes)

@app.route('/lifegp')
def lifegp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lifegp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lifegp.html', quotes=quotes)


@app.route('/lovegq')
def lovegq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lovegq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lovegq.html', quotes=quotes)



@app.route('/successgq')
def successgq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('successgq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('successgq.html', quotes=quotes)

@app.route('/motivationgq')
def motivationgq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('motivationgq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('motivationgq.html', quotes=quotes)

@app.route('/wisdomgq')
def wisdomgq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('wisdomgq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('wisdomgq.html', quotes=quotes)

@app.route('/sadgq')
def sadgq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('sadgq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('sadgq.html', quotes=quotes)

@app.route('/lifegq')
def lifegq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lifegq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lifegq.html', quotes=quotes)
#German
#Spanish
@app.route('/lovesp')
def lovesp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lovesp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lovesp.html', quotes=quotes)


@app.route('/successsp')
def successsp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('successsp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('successsp.html', quotes=quotes)

@app.route('/motivationsp')
def motivationsp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('motivationsp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('motivationsp.html', quotes=quotes)

@app.route('/wisdomsp')
def wisdomsp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('wisdomsp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('wisdomsp.html', quotes=quotes)

@app.route('/sadsp')
def sadsp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('sadsp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('sadsp.html', quotes=quotes)

@app.route('/lifesp')
def lifesp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lifesp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lifesp.html', quotes=quotes)


@app.route('/lovesq')
def lovesq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lovesq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lovesq.html', quotes=quotes)



@app.route('/successsq')
def successsq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('successsq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('successsq.html', quotes=quotes)

@app.route('/motivationsq')
def motivationsq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('motivationsq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('motivationsq.html', quotes=quotes)

@app.route('/wisdomsq')
def wisdomsq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('wisdomsq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('wisdomsq.html', quotes=quotes)

@app.route('/sadsq')
def sadsq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('sadsq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('sadsq.html', quotes=quotes)

@app.route('/lifesq')
def lifesq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lifesq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lifesq.html', quotes=quotes)
#Spanish
@app.route('/lovep')
def lovep():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lovep',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lovep.html', quotes=quotes)


@app.route('/successp')
def successp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('successp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('successp.html', quotes=quotes)

@app.route('/motivationp')
def motivationp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('motivationp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('motivationp.html', quotes=quotes)

@app.route('/wisdomp')
def wisdomp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('wisdomp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('wisdomp.html', quotes=quotes)

@app.route('/sadp')
def sadp():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('sadp',))
    quotes = c.fetchall()
    conn.close()
    return render_template('sadp.html', quotes=quotes)

@app.route('/lifep')
def lifep():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lifep',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lifep.html', quotes=quotes)


@app.route('/loveq')
def loveq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('loveq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('loveq.html', quotes=quotes)



@app.route('/successq')
def successq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('successq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('successq.html', quotes=quotes)

@app.route('/motivationq')
def motivationq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('motivationq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('motivationq.html', quotes=quotes)

@app.route('/wisdomq')
def wisdomq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('wisdomq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('wisdomq.html', quotes=quotes)

@app.route('/sadq')
def sadq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('sadq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('sadq.html', quotes=quotes)

@app.route('/lifeq')
def lifeq():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT quote, author, explanation, timestamp FROM quotes WHERE section = ? AND completed = 1 ORDER BY id DESC', ('lifeq',))
    quotes = c.fetchall()
    conn.close()
    return render_template('lifeq.html', quotes=quotes)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
