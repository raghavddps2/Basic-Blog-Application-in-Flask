from flask import Flask, flash,redirect,url_for,session,logging,request
from flask import render_template
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

#get an instance of the flask class.
app = Flask(__name__)

#Config MySQL;
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql =  MySQL(app)
#We set the default cursor class to dictionary, helps us set connection and execute queries.


art = Articles()

#The below one actually defines the route to which we gonna go.
@app.route('/')
def index():
    # return "INDEX2"
    return render_template('home.html')
    #We do the above if we wanna server the HTML file.

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    return render_template('articles.html',articles=art)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('articles.html',id=id)


#This one basically sets up all the params required for the form.
class RegisterForm(Form):
    name = StringField('Name',[validators.length(min=1,max=50)])
    username = StringField('username',[validators.length(min=4,max=25)])
    email = StringField('email',[validators.length(min=6,max=50)])
    password = PasswordField('password',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Passwords do not match')
    ])
    confirm = PasswordField('confirm Password')

@app.route('/register',methods=['GET','POST'])
def register():
    #This gets 
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        #Now, we should first send the things in the database.
        #We will first get the values.
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))


        #we will set up the cursor.
        cur = mysql.connection.cursor()
        #following to execute the query.
        cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s)", (name,email,username,password))

        #Following will commit to DB.
        mysql.connection.commit()
        cur.close()
        flash('You are now registered','success')
        
        #We need to redirect it to the index.
        redirect(url_for('index'))      
    return render_template('register.html',form=form)
#This runs if the app is same as the main
if __name__ == '__main__':
    app.secret_key = 'secret_123'
    app.run(debug=True) #Setting debug as true, basically, we don't have to restsrat the server.
