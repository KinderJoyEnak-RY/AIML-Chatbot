import re
import aiml
from helper.update_aiml import connect, update_aiml_file, custom_make_translation
from flask import Flask, render_template, url_for, redirect, request, session, flash
from helper.spell_checker import correction
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import string
import random

app = Flask(__name__)
app.secret_key = 'bptTaw74SPxYjzd'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

kernel = aiml.Kernel()
kernel.bootstrap(learnFiles="./data/std-startup.xml", commands="load aiml")
#membuat the kernel and memuat AIML files dari file xml, pada direktory data

conn = connect

@app.route("/chat")
def chat():
    #update aiml file
    update_aiml_file()
    return render_template("content/chat.html")
    #fungsi ini untuk meminta nama file template dan daftar variabel untuk diisi ke dalam placeholder yang ada di dalam folder template tersebut  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggegin' in session:
        return redirect(url_for('home'))
    # Check jika "username" dan "password" POST requests add (user submit form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables untuk request username dan password
        username = request.form['username']
        password = request.form['password']
        # Check akun ada di database
        mycursor = conn.cursor()
        mycursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
        # Fetch 1 data record and return result
        user = mycursor.fetchone()
        # If user ada di tabel
        if user:
            # Create session data
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            # Redirect to home
            return redirect(url_for('home'))
        else:
            # jiak user tidak ada atau username/password salah
             flash('Invalid username/password','danger')
    # tampilakan the login form dengan flash pesan (if any)
    return render_template('auth/login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'loggegin' in session:
        return redirect(url_for('home'))
    # Check jika "username", "password" dan "email" POST request ada  (user submitted form)
    if request.method == 'POST' and 'fullname' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
       # Create variables untuk request username dan password
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mycursor = conn.cursor()
        mycursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = mycursor.fetchone()
        # if akun ada makan tampilkan error and validation checks
        if account:
            flash('Account already exists!','warning')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!','warning')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!','warning')
        elif not username or not password or not email:
            flash('Please fill out the form!','warning')
        else:
            # Jika tidak ada akun maka insert new akun ke user table
            mycursor.execute('INSERT INTO user (fullname, username, password, email, created_at, updated_at) VALUES (%s, %s, %s, %s, now(), now())', ( fullname, username, password, email,))
            conn.commit()
            flash('You have successfully registered!', 'success')
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # jika form kosong (no POST data)
        flash('Please fill out the form!','warning')
    # tampilakan the login form dengan flash pesan (if any)
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    #hapus session login
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

 #halaman utama

@app.route("/")
def home():
    #jika user berhasil login
    if 'loggedin' in session:
        mycursor = conn.cursor()
        mycursor.execute('''SELECT a.tag, GROUP_CONCAT(DISTINCT b.pattern SEPARATOR '; ') as pattern, GROUP_CONCAT(DISTINCT c.response SEPARATOR '; ') as response
                            FROM tag a
                            LEFT JOIN pattern b ON a.id = b.tag_id
                            LEFT JOIN response c ON a.id = c.tag_id
                            GROUP BY a.tag
                            ORDER BY a.id''')
        data = mycursor.fetchall()
        mycursor.close()
        getUsername = session['username']
        id = session['id']
        flash('Login successful','success')
        return render_template('content/home.html', data=data, id=id, getUsername=getUsername)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
 
 #halaman profile
@app.route("/profile/<int:id>", methods=['GET'])
def profile(id):
      #jika user berhasil login
    if 'loggedin' in session:
        mycursor = conn.cursor()
        mycursor.execute('select * from user where id=%s', ( id,))
        data = mycursor.fetchall()
        mycursor.close()
        getUsername = session['username']
        id = session['id']
        return render_template('content/profile.html', data=data, getUsername=getUsername, id=id)
    # User is not loggedin redirect to profile page
    return redirect(url_for('profile', id=id))

 #halaman edit profile
@app.route('/profile/edit/<int:id>', methods=['GET', 'POST'])
def edit_profile(id):
    if request.method == 'GET':
       return redirect(url_for('profile', id=id))
    else:
        #Create variables untuk request username dan password
        fullname = request.form['fullname']
        email = request.form['email']
        username = request.form['username']
        mycursor = conn.cursor()
        #update user biodata berdasarkan request
        mycursor.execute(''' UPDATE `user` SET fullname = %s, email = %s, username = %s, updated_at = now() WHERE id = %s ''',(fullname, email, username, id, ))
        conn.commit()        
        mycursor.close()
        flash('Data user successfully edited', 'success')
        return redirect(url_for('profile', id=id))

    return render_template('content/profile.html')

 #halaman edit profile password
@app.route('/profile/editpass/<int:id>', methods=['GET', 'POST'])
def editpass_profile(id):
    if request.method == 'GET':
       return redirect(url_for('profile', id=id))
    else:
        #Create variables untuk request username dan password
        password = request.form['password']
        mycursor = conn.cursor()
        #update user password berdasarkan request
        mycursor.execute(''' UPDATE `user` SET password = %s, updated_at = now() WHERE id = %s ''',(password, id, ))
        conn.commit()        
        mycursor.close()
        flash('Data user password successfully edited', 'success')
        return redirect(url_for('profile', id=id))

    return render_template('content/profile.html')

 #halaman tag
@app.route("/tag")
def tag():
     #jika user berhasil login
    if 'loggedin' in session:
        mycursor = conn.cursor()
        #select data id, tag dari table tag untuk
        mycursor.execute(''' SELECT id, tag FROM tag''')
        #tampung hasil query di variabel data
        data = mycursor.fetchall()
        mycursor.close()
        getUsername = session['username']
        id = session['id']
        return render_template('content/tag.html', data=data, id=id, getUsername = session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

 #fungsi untuk menambah data tag
@app.route("/tag/add", methods=['GET', 'POST'])
def add_tag():
    if request.method == 'GET':
        return redirect(url_for('tag'))
    else:
        tag = request.form['tag']
        mycursor = conn.cursor()
        #insert data tag
        mycursor.execute('INSERT INTO tag (tag, created_at, updated_at) VALUES (%s, now(), now())', ( tag,))
        conn.commit()

        #update aiml file
        update_aiml_file()

        mycursor.close()
        flash('Tag successfully insert', 'success')
        return redirect(url_for('tag'))

    return render_template('content/tag.html')

 #fungsi untuk edit data tag
@app.route('/tag/edit/<int:id>', methods=['GET', 'POST'])
def edit_tag(id):
    if request.method == 'GET':
       return redirect(url_for('tag'))
    else:
        tag = request.form['tagEdit']
        mycursor = conn.cursor()
        mycursor.execute(''' UPDATE tag SET tag = %s WHERE id = %s ''',(tag, id ))
        conn.commit()

        #update aiml file
        update_aiml_file()

        mycursor.close()
        flash('Tag successfully edited', 'success')
        return redirect(url_for('tag'))

    return render_template('content/tag.html')

 #fungsi untuk delete data tag
@app.route('/tag/delete/<int:id>', methods=['GET'])
def tag_delete(id):
    if request.method == 'GET':
        mycursor = conn.cursor()
        mycursor.execute(''' DELETE FROM tag WHERE id=%s''', (id, ))
        conn.commit()
         #update aiml file
        update_aiml_file()

        mycursor.close()
        flash('Tag successfully deleted', 'success')
        return redirect(url_for('tag'))

    return render_template('content/tag.html')

 #fungsi untuk menampilakn data pattern
@app.route("/pattern")
def pattern():
    if 'loggedin' in session:
        mycursor = conn.cursor()
        mycursor.execute(''' SELECT id, pattern, tag_id FROM pattern''')
        data = mycursor.fetchall()

        mycursor.execute(''' SELECT id, tag FROM tag''')
        dataTag = mycursor.fetchall()
        mycursor.close()

        getUsername = session['username']
        id = session['id']
        return render_template('content/pattern.html', data=data, id=id,  dataTag=dataTag, getUsername = session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

 #fungsi untuk menampilakn data option select pattern
@app.route('/pattern/<int:id>', methods=['GET'])
def pattern_options(id):
    result = ""
    if request.method == 'GET':
        mycursor = conn.cursor()
        mycursor.execute(''' SELECT id, pattern FROM pattern WHERE tag_id=%s''', (id, ))
        data = mycursor.fetchall()

        for item in data:
            result += "<option value='"+ str(item[0]) +"'>"+ item[1] +"</option>"

    if id == 0:
        result = "<option value='0'>Pilih Tag terlebih dahulu</option>"
    else:
        result

    return str(result)
    
 #fungsi untuk menambahkan data pattern
@app.route("/pattern/add", methods=['GET', 'POST'])
def add_pattern():

    pattern = request.form['pattern']
    tagId = request.form['tag_id']
    mycursor = conn.cursor()

    pattern = custom_make_translation(pattern)

    if request.method == 'GET':
        return redirect(url_for('pattern'))
    else:
        mycursor.execute('SELECT * FROM pattern WHERE pattern = %s', (pattern,))
        dataPattern = mycursor.fetchone()
        # If dataPattern exists show error and validation checks
        if dataPattern:
            flash('Pattern already exists!','warning')
            return redirect(url_for('pattern'))
        else:
            mycursor.execute('INSERT INTO pattern (pattern, tag_id, created_at, updated_at) VALUES (%s, %s, now(), now())', (pattern.upper(), tagId,))
            conn.commit()
            #update aiml file
            update_aiml_file()
            mycursor.close()
            return redirect(url_for('pattern'))

    return render_template('content/pattern.html')

 #fungsi untuk edit data pattern
@app.route('/pattern/edit/<int:id>', methods=['GET', 'POST'])
def edit_pattern(id):
    if request.method == 'GET':
        
       return redirect(url_for('pattern'))
    else:
        pattern = request.form['patternEdit']
        tagId = request.form['tagId']
        pattern = custom_make_translation(pattern)
        mycursor = conn.cursor()
        mycursor.execute(''' UPDATE pattern SET pattern = %s, tag_id = %s WHERE id = %s ''',(pattern.upper(), tagId, id, ))
        conn.commit()
         #update aiml file
        update_aiml_file()
        
        mycursor.close()
        flash('Pattern successfully edited', 'success')
        return redirect(url_for('pattern'))

    return render_template('content/pattern.html')

 #fungsi untuk menghapus data pattern
@app.route('/pattern/delete/<int:id>', methods=['GET'])
def pattern_delete(id):
    if request.method == 'GET':
        mycursor = conn.cursor()
        mycursor.execute(''' DELETE FROM pattern WHERE id=%s''', (id, ))
        conn.commit()
        #update aiml file after create tag
        update_aiml_file()

        mycursor.close()
        flash('Pattern successfully deleted', 'success')
        return redirect(url_for('pattern'))

    return render_template('content/pattern.html')

 #fungsi untuk menampilkan data response
@app.route("/response")
def response():
    if 'loggedin' in session:
        mycursor = conn.cursor()
        mycursor.execute(''' SELECT id, tag_id, pattern_id, response FROM response''')
        data = mycursor.fetchall()

        mycursor.execute(''' SELECT id, tag FROM tag ''')
        dataTag = mycursor.fetchall()

        mycursor.execute(''' SELECT id, tag_id, pattern FROM pattern''')
        dataPattern = mycursor.fetchall()

        mycursor.close()

        getUsername = session['username']
        id = session['id']
        return render_template('content/response.html', data=data, id=id, dataTag=dataTag,  dataPattern=dataPattern, getUsername = session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

 #fungsi untuk menambahkan data response
@app.route("/response/add", methods=['GET', 'POST'])
def add_response():
    if request.method == 'GET':
        return redirect(url_for('response'))
    else:
        response = request.form['response']
        tagId = request.form['tag_id']
        patternId = request.form['pattern_id']
        mycursor = conn.cursor()
        mycursor.execute('INSERT INTO response (response, tag_id, pattern_id, created_at, updated_at) VALUES (%s, %s, %s, now(), now())', (response, tagId, patternId,))
        conn.commit()
          #update aiml file after create tag
        update_aiml_file()

        mycursor.close()
       
        return redirect(url_for('response'))

    return render_template('content/response.html')

 #fungsi untuk edit data response
@app.route('/response/edit/<int:id>', methods=['GET', 'POST'])
def edit_response(id):
    if request.method == 'GET':
       return redirect(url_for('response'))
    else:
        response = request.form['responseEdit']
        tagId = request.form['tagId']
        patternId = request.form['patternId']
        mycursor = conn.cursor()
        mycursor.execute(''' UPDATE response SET response = %s, tag_id = %s, pattern_id = %s WHERE id = %s ''',(response, tagId, patternId, id, ))
        conn.commit()
         #update aiml file
        update_aiml_file()
        
        mycursor.close()
        flash('response successfully edited', 'success')
        return redirect(url_for('response'))

    return render_template('content/response.html')

 #fungsi untuk menghapus data response
@app.route('/response/delete/<int:id>', methods=['GET'])
def response_delete(id):
    if request.method == 'GET':
        mycursor = conn.cursor()
        mycursor.execute(''' DELETE FROM response WHERE id=%s''', (id, ))
        conn.commit()
          #update aiml file after create tag
        update_aiml_file()
        
        mycursor.close()
       
        return redirect(url_for('response'))

    return render_template('content/response.html')


DEFAULT_RESPONSES = ["Maaf, saya tidak dapat memahami pertanyaan Anda🙏 mohon sertakan konteks/informasi dasar pada pertanyaan anda🙏"]
excluded_patterns = ['nama ', 'nama saya ', 'aku ', 'saya ', 'namamu', 'siapa', 'kamu', 'namaku']

# membuat stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Mendefinisikan path ke file kamus kata dasar
kamus_path = 'helper/kata-dasar.txt'

# Memuat kamus kata dasar dari file
with open(kamus_path, 'r') as file:
    kamus_kata_dasar = file.read().splitlines()

@app.route("/get")
def get_bot_response():
    query = request.args.get('msg')
    print('User Input: ', query)

    # Memeriksa apakah input pengguna cocok dengan pola yang harus dikecualikan
    should_exclude = any(query.lower().startswith(pattern) for pattern in excluded_patterns)
    if should_exclude:
        response = kernel.respond(query)
    else:
        # Preprocessing
        preprocessed_query = preprocess(query)

        # Call AIML kernel
        response = kernel.respond(preprocessed_query)

    x = response.replace("((", "<").replace("))", ">").replace("]", "").replace("'", "")
    print('Bot Response = ', x)
    if x is None or x == '':
        return random.choice(DEFAULT_RESPONSES)
    return x

def preprocess(text):
    # melakukan case folding
    text = text.lower()
   
    # menghilangkan nomor dan tanda baca
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
   
    # melakukan tokenizing
    words = text.split()
   
    # melakukan spell check
    corrected_words = []
    for word in words:
        corrected_words.append(correction(word))

    # melakukan stemming dengan kamus kata dasar
    stemmed_words = []
    for word in corrected_words:
        if word in kamus_kata_dasar:
            stemmed_words.append(word)
        else: 
            stemmed_words.append(stemmer.stem(word))
       
    # melakukan filtering stopwords
    with open('helper/data-stopword.txt', 'r') as file:
        stopwords = file.read().splitlines()
    filtered_words = [word for word in stemmed_words if word not in stopwords]
   
    print("Hasil case folding: ", text)
    print("Hasil penghilangan nomor dan tanda baca: ", text)
    print("Hasil tokenizing: ", words)
    print("Hasil koreksi : ", corrected_words)
    print("Hasil stemming: ", stemmed_words)
    print("Hasil filtering stopwords: ", filtered_words)
    
    # menggabungkan kata yang telah dilakukan preprocessing
    preprocessed_text = ' '.join(filtered_words)

    print("Pattern :",preprocessed_text)
    return preprocessed_text

if __name__ == "__main__":
    app.run(debug=True)



# DEFAULT_RESPONSES = ["Maaf, saya tidak dapat memahami pertanyaan Anda🙏 mohon sertakan konteks/informasi dasar pada pertanyaan anda🙏"]

# @app.route("/get")
# def get_bot_response():
#     query = request.args.get('msg')
#     print('User Input: ', query)

#     # skip spell-checking for specific patterns
#     excluded_patterns = ['nama ', 'nama saya ', 'aku', 'saya']
#     if any(query.startswith(pattern) for pattern in excluded_patterns):
#         words = query.split()
#         correction_sentence = query
#     else:
#         # Case folding
#         query = query.lower()
#         query = re.sub(r'[^\w\s]', '', query)
#         print('After case folding: ', query)

#         # Tokenizing
#         words = word_tokenize(query)
#         print('After tokenizing: ', words)

#         # Spell correction
#         words = [correction(w) for w in words]
#         correction_sentence = " ".join(words)
#         print('After spell correction: ', correction_sentence)
#         print('Pattern : ', correction_sentence)

#     # Call AIML kernel
#     response = kernel.respond(correction_sentence)
#     x = response.replace("((", "<").replace("))", ">").replace("]", "").replace("'", "")
#     print('Bot Response = ', x)
#     if x is None or x=='':
#         return(random.choice(DEFAULT_RESPONSES))
#     return x
   
# if __name__ == "__main__":
#     app.run(debug=True)   

