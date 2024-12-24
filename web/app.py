import os
from datetime import datetime
import flask
from werkzeug import security

app = flask.Flask(__name__)

class Sources:
    def __init__(self):
        self.source_one = ""
        self.source_two = ""


class Item:
    def __init__(self, name, directory):
        self.name = name
        self.path = os.path.abspath(f"{directory}/{name}").replace("\\", "/").replace("C:/", "/") # Some Windows shenaningans which need to be removed
        self.type = "file" if os.path.isfile(self.path) else "directory"
        self.date = datetime.fromtimestamp(os.path.getmtime(self.path)).strftime('%Y-%m-%d %H:%M') if self.type == "file" else "-"
        self.size = human_size(os.path.getsize(self.path)) if self.type == "file" else "-"


def human_size(num: int, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def list_items(directory):
    items = []
    items_raw = os.listdir(directory)
    for i in items_raw:
        item = Item(i, directory)
        items.append(item)

    return items

@app.route("/", defaults={"directory": ""})
@app.route("/<path:directory>", )
def home(directory):
    return flask.render_template("navigator.html", items=list_items("/" + directory), sources=sources)

@app.route("/source", methods=["POST"])
def select_sources():
    if flask.request.form.getlist("source_one"):
        sources.source_one = flask.request.form.getlist("source_one")[0]
    if flask.request.form.getlist("source_two"):
        sources.source_two = flask.request.form.getlist("source_two")[0]
    print(sources.source_one, sources.source_two)
    return flask.redirect(flask.url_for("home"))

sources = Sources()
