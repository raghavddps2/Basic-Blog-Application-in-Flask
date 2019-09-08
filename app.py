from flask import Flask, flash,redirect,url_for,session,logging,request
# Flask is basically for creating the flask app
#flash is basically for creating the flash messages.
#redirect is basically for redirecting.
#session is basically for logging in and logging out.
#request is basically for creating request.

from flask import render_template
#render_template is just to render the templates.
# from data import Articles

from flask_mysqldb import MySQL
#MySQL from flask_mysqldb is basically for using the database.

from wtforms import Form,StringField,TextAreaField,PasswordField,validators
#wtforms basically provides All the required validators.

from passlib.hash import sha256_crypt
#This is basically for hashing the password.

from functools import wraps
# Have to understand the logic.

#get an instance of the flask class.
app = Flask(__name__)

#Config MySQL;
app.config['MYSQL_HOST'] = 'db'  #This basically tells the host.
app.config['MYSQL_USER'] = 'root' #This is basically the user.
app.config['MYSQL_PASSWORD'] = 'example' #This is the password for the same
app.config['MYSQL_DB'] = 'myflaskapp' #This tells the dataabse name.
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #For converting to dictionary.

mysql =  MySQL(app)
#We set the default cursor class to dictionary, helps us set connection and execute queries.


# art = Articles()

#The below one actually defines the route to which we gonna go.
@app.route('/')
def index():
    # return "INDEX2"
    return render_template('home.html')
    #We do the above if we wanna server the HTML file.

@app.route('/about')
def about():
    return render_template('about.html')
    #The above just returns the about page.

@app.route('/articles')
def articles():
        #create cursor.
    cursor = mysql.connection.cursor()
    
    #Get the articles.
    result = cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()

    if result > 0:
        return render_template('articles.html',articles=articles)
    else:
        msg = "No articles found"
        return render_template('articles.html',msg=msg)

    cursor.close()
#Single article.
@app.route('/article1/<string:id>/')
def article1(id):
    
    cursor = mysql.connection.cursor()
    
    #Get the articles.
    result = cursor.execute("SELECT * FROM articles WHERE id = %s",[id])
    article = cursor.fetchone()
    # print(article['title'])
    return render_template('article.html',article=article)
    cursor.close()


#This one basically sets up all the params required for the form.
class RegisterForm(Form):

    #The below gives the structure of the web page.
    name = StringField('Name',[validators.length(min=1,max=50)])
    username = StringField('username',[validators.length(min=4,max=25)])
    email = StringField('email',[validators.length(min=6,max=50)])
    country = StringField('country', [validators.length(min=2, max=50)])
    password = PasswordField('password',[
        #This will necessarily see that the Data is filled and the passwords do match.
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Passwords do not match')
    ])
    confirm = PasswordField('confirm Password')

@app.route('/register',methods=['GET','POST'])
def register():
    #This gets 
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate(): #This checks if it is a post request and if the form is validated as well.
        #Now, we should first send the things in the database.
        #We will first get the values.
        name = form.name.data
        email = form.email.data
        username = form.username.data
        country = form.country.data

        #Here, we will encrypt the password.
        password = sha256_crypt.encrypt(str(form.password.data))


        #we will set up the cursor.
        cur = mysql.connection.cursor()
        #following to execute the query.
        cur.execute("INSERT INTO users(name,email,username,country, password) VALUES(%s,%s,%s,%s,%s)", (name,email,username,country, password))

        #Following will commit to DB.
        mysql.connection.commit()

        #This just closes the cursor.
        cur.close()

        #The below will use flash to flash the message.
        flash('You are now registered','success')
        
        #We need to redirect it to the index.
        redirect(url_for('index'))      

    #The below happens if it is a get request.
    return render_template('register.html',form=form)
#This runs if the app is same as the main

#User login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':

        #Get for fields.
        username = request.form['username']
        password_candidate = request.form['password']

        # Create a cursor 
        cur = mysql.connection.cursor()
        #Get user by username.
        result = cur.execute("SELECT * FROM users WHERE username = %s",[username])
        if result >0:
            #Getting the stored hash.
            data = cur.fetchone() #This will get the first one.
            password = data['password'] #This will give us the password.
            country =  data['country'] 
            #Compare the passwords.
            #This is to verify
            if sha256_crypt.verify(password_candidate,password):
                #Lets say that can login.
                #When we login we have to create a user session.
                
                #The below is the comment as to see what to do, if things do not work.

                # app.logger.info('PASSWORD MATCHED')
                #We will start the session
                session['logged_in'] = True
                session['username'] = username
                session['country'] = country
                flash('You are now logged in','success')
                return redirect(url_for('dashboard'))

            #This if the password is wrong.
            else:
                error = "Invalid Login"
                return render_template('login.html',error=error)
        
        #This if the username does not exist nly.
        else:
            error = "Username not found"
            return render_template('login.html',error=error)
    
    #The below goes if it is a get request.
    return render_template('login.html')


def is_logged_in(f):
    #Have to figure out what the heck does this wraps do!!
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, Please login','danger')
            return redirect(url_for('login'))
    return wrap
#Logout.
@app.route('/logout')
@is_logged_in
def logout():
    session.clear() #We just have to clear the session, this will automatically set it to false.
    flash('You are now logged out','success')
    return redirect(url_for('login'))


#Dashboard.
@app.route('/dashboard')
#Allowed only if logged in.
@is_logged_in
def dashboard():

    #create cursor.
    cursor = mysql.connection.cursor()
    
    #Get the articles.
    result = cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()

    if result > 0:
        return render_template('dashboard.html',articles=articles)
    else:
        msg = "No articles found"
        return render_template('dashboard.html',msg=msg)

    cursor.close()
    return render_template('dashboard.html')


class ArticleForm(Form):
    title = StringField('Title',[validators.length(min=1,max=50)])
    body = TextAreaField('Body',[validators.length(min=30)])

#Add artcile
@app.route('/add_article',methods=['GET','POST'])
@is_logged_in
def add_article():
    form  = ArticleForm(request.form)  #This is basically to create the form instance.
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        #Create the cursor to insert the data.
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO articles(title,body,author) VALUES(%s,%s,%s)",(title,body,session['username']))


        #Now, we need to commit this to the database.
        mysql.connection.commit()
        #Now, we will close the connection.
        cursor.close()
        flash('Article Created','success')

        #We are going to redirect.
        return redirect(url_for('dashboard'))

    return render_template('add_article.html',form=form)


@app.route('/edit_article/<string:id>',methods=['GET','POST'])
@is_logged_in
def edit_article(id):

    # Create a cursor...
    cursor = mysql.connection.cursor()

    #Get the user by the id.
    result = cursor.execute("SELECT * FROM articles WHERE id=%s",[id])
    article = cursor.fetchone()
    #Get Form.
    form = ArticleForm(request.form)


    #Gets what the user edited basically.
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        #Create the cursor to insert the data.
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE articles SET title=%s,body=%s WHERE id=%s",(title,body,id))


        #Now, we need to commit this to the database.
        mysql.connection.commit()
        #Now, we will close the connection.
        cursor.close()
        flash('Article Updated','success')

        #We are going to redirect.
        return redirect(url_for('dashboard'))

    return render_template('edit_article.html',form=form)


#Delete article.
@app.route('/delete_article/<string:id>',methods=['POST'])
@is_logged_in
def delete_article(id):
    #Create the cursor.

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM articles WHERE id=%s",[id])
    mysql.connection.commit()

    cursor.close()
    flash('Article Deleted','success')
    return redirect(url_for('dashboard'))
    
if __name__ == '__main__':
    app.secret_key = 'secret_123'
    app.run(host="0.0.0.0", debug=True) #Setting debug as true, basically, we don't have to restsrat the server.
