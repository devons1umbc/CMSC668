from flask import Flask, render_template, request, session, redirect
from flask_sock import Sock
from movies import MovieAPI
import database
import mlmodel

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
    if request.method == "POST":
        if request.form.get("query"):
            query = request.form.get('query')
            database.add_list_to_db(movie.query_movie(query))
            movielist = database.get_all_type_title_loose(query)
            descriptionsize = []
            for i in movielist:
                j = len(i['Description'][0])
                descriptionsize.append(j/(306*16))
            return render_template("index.html", len=len(movielist), movielist=movielist, descriptionsize=descriptionsize, disabled="false")
        else:
            for i in request.form.keys():
                temp = i
                if i != "submit":
                    i = i.replace('(', '\\(')
                    i = i.replace(')', '\\)')
                    newmovie = database.get_all_type_title_strict(i)[0]
                    newmovie["Likes"] = request.form.get(temp)
                    user_movies.append(newmovie)
            return render_template("index.html", len=0, movielist=[])
    else:
        return render_template("index.html", len=0, movielist=[], disabled="true")

@app.route('/results', methods=['GET', 'POST'])
def results():
    return render_template("index.html", len=1, movielist=[mlmodel.find_best(user_movies)], disabled="false")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=25565, threaded=True)
