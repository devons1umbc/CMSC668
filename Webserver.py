from flask import Flask, render_template, request, session, redirect
from flask_sock import Sock
from movies import MovieAPI
import database

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "files/"
app.config['SECRET_KEY'] = "Your_secret_string"
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
sock = Sock(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        query = request.form.get('query')
        print(query)
        movielist = database.get_all_type_title_loose(query)
        return render_template("index.html", len=len(movielist), movielist=movielist)

    else:
        return render_template("index.html", len=0, movielist=[])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=25565, threaded=True)
