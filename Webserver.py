from flask import Flask, render_template, request, session, redirect
from flask_sock import Sock
from movies import MovieAPI
import database
import mlmodel
import os
from werkzeug.utils import secure_filename
import json
import hashlib

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "files/"
app.config['SECRET_KEY'] = "Your_secret_string"
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
sock = Sock(app)
movie = MovieAPI()

liked_movies = []
disliked_movies = []
user_movies = []


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect('/login')

    if request.method == "POST":
        if request.form.get("query"):
            query = request.form.get('query')
            print("Querying " + query + "...")
            # movie.query_movie(query)
            movielist = database.get_all_type_title_strict(query)
            return render_template("index.html", len=len(movielist), movielist=movielist, disabled="false", username=session['username'])
        elif request.form.get("submit-likes"):
            for i in request.form.keys():
                temp = i
                print(i)
                if i != "submit-likes":
                    i = i.replace('(', '\\(')
                    i = i.replace(')', '\\)')
                    newmovie = database.get_all_type_title_strict(i)[0]
                    newmovie["Likes"] = request.form.get(temp)

                    with open('users/' + str(session['username']).lower() + '/user.json') as update_user:
                        data = json.load(update_user)
                    update_user.close()

                    if request.form.get(temp) == "1":
                        data[0]['liked_movies'].append(newmovie)
                    else:
                        data[0]['disliked_movies'].append(newmovie)
                    with open('users/' + str(session['username']).lower() + '/user.json', 'w') as new_user:
                        json.dump(data, new_user, indent=4, separators=(',', ': '))
                    new_user.close()
            return render_template("index.html", len=0, movielist=[], disabled="false", username=session['username'])
        else:
            return render_template("index.html", len=0, movielist=[], disabled="true", username=session['username'])
    else:
        return render_template("index.html", len=0, movielist=[], disabled="true", username=session['username'])


@app.route('/results', methods=['GET', 'POST'])
def results():
    with open('users/' + str(session['username']).lower() + '/user.json') as get_user:
        data = json.load(get_user)
    get_user.close()
    print(data[0]['liked_movies'])
    print(data[0]['disliked_movies'])
    if len(data[0]['liked_movies']) != 0 or len(data[0]['disliked_movies']) != 0:
        movies = mlmodel.find_best(data[0]['liked_movies'], data[0]['disliked_movies'])
        return render_template("index.html", len=1, movielist=[movies], disabled="false", username=session['username'])
    else:
        movies = ''
        return render_template("index.html", len=1, movielist=[movies], disabled="false", username=session['username'])


@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'username' in session:
        return redirect('/')

    # Handle request
    if request.method == "POST":

        # Get user inputs
        username = secure_filename(str(request.form.get('username')))
        password = secure_filename(str(request.form.get('password')))

        # Handle user login
        if len(username) != 0 and len(password) != 0:
            if username.lower() not in os.listdir('users/'):
                print("No such username")
                return render_template('login.html')
            with open('users/' + username.lower() + '/user.json') as json_file_user_login:
                data_user_login = json.load(json_file_user_login)
            json_file_user_login.close()
            for user_login in data_user_login:
                salt_file = open("salt.txt", 'r')
                salt = salt_file.readlines()[0]
                salt_file.close()
                if username.lower() == user_login['username'].lower() and hashlib.sha512(
                        (password + salt).encode('UTF-8')).hexdigest() == user_login['password']:
                    print("correct")
                    session["username"] = user_login['username']
                    return redirect('/')
                else:
                    print("incorrect")
                    return render_template('login.html')
    # If user is not logged in or is logged in somewhere else
    if 'username' not in session:
        print("not logged in")
        return render_template('login.html')
    # If user is logged in
    else:
        return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():

    if 'username' in session:
        return redirect('/')

    if request.method == "POST":
        # Get user inputs
        username = secure_filename(str(request.form.get('username')))
        password = secure_filename(str(request.form.get('password')))

        if len(username.lower()) > 64 or len(password) == 0:
            print("Username needs to be < 64 and > 0")
            return render_template('signup.html')

        # Checks username and passwords for issues
        list_names = os.listdir('users/')
        if username.lower() in list_names or username == '':
            print("Duplicate or blank name")
            return render_template('signup.html')
        if len(password) > 64 or len(password) == 0:
            print("Password needs to be < 64 and > 0")
            return render_template('signup.html')
        print("Success")
        session["username"] = username
        print(session["username"])
        if not os.path.exists('users/' + username.lower()):
            os.mkdir('users/' + username.lower())

        # Add username and password to Json file
        file = open('users/' + username.lower() + '/user.json', 'w')
        file.write('[\n]')
        file.close()
        with open('users/' + username.lower() + '/user.json') as json_file_user_signup:
            data_user_signup = json.load(json_file_user_signup)
        salt_file = open("salt.txt", 'r')
        salt = salt_file.readlines()[0]
        salt_file.close()
        data_user_signup.append({
            "username": username,
            "password": hashlib.sha512((password + salt).encode('UTF-8')).hexdigest(),
            "liked_movies": [],
            "disliked_movies": [],
        })
        json_file_user_signup.close()
        with open('users/' + username.lower() + '/user.json', 'w') as json_file_user_signup:
            json.dump(data_user_signup, json_file_user_signup, indent=4, separators=(',', ': '))
        json_file_user_signup.close()
        return redirect('/')
    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=25565, threaded=True)
