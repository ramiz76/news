from datetime import datetime
from os import environ
from dotenv import load_dotenv

from psycopg2 import extensions, connect, extras, DatabaseError, sql
from flask import Flask, current_app, jsonify, request


PATH = "stories.json"
DATE = formatted_time = datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
app = Flask(__name__)


def db_connection() -> extensions.connection:
    """Establish connection with the media-sentiment RDS"""
    try:
        return connect(database=environ['DBNAME'],
                       user=environ['DBUSER'],
                       host=environ['DBHOST'],
                       password=environ['DBPASS'],
                       port=environ['DBPORT'],
                       cursor_factory=extras.RealDictCursor)
    except DatabaseError:
        print("Error connecting to database.")


def create_story(args) -> None:
    """Add new story to the stories table of the database."""
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO stories (title, url,created) VALUES (%s,%s,%s)""", [
                        args.get("title"), args.get("url"), DATE])
        conn.commit()
    return None


@app.route("/", methods=["GET"])
def index():
    return current_app.send_static_file("index.html")


@app.route("/add", methods=["GET"])
def addstory():
    return current_app.send_static_file("./addstory/index.html")


@app.route("/scrape", methods=["GET"])
def scrape():
    return current_app.send_static_file("./scrape/index.html")


def select_stories(sort="title", order="ASC", search=""):
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql.SQL("""SELECT stories.*,
                        GREATEST(0,SUM(CASE direction WHEN 'up' THEN 1 ELSE -1 END)) AS score
                        FROM stories
                        LEFT JOIN votes ON votes.id = stories.id
                        GROUP BY stories.id
                        ORDER BY {} {};""").format(sql.Identifier(sort), sql.SQL(order)))
            stories = cur.fetchall()
    if search:
        stories = [story for story in stories if search in story["title"].lower()]
    return stories


@app.route("/stories", methods=["GET", "POST"])
def get_stories():
    args = request.args.to_dict()
    if request.method == "GET":
        order = args.get("order")
        order = "ASC" if order == "ascending" else "DESC"
        stories = select_stories(args.get("sort"), order, args.get("search"))
        if stories:
            return jsonify(stories), 200
        else:
            return jsonify({"error": True, "message": "No stories were found"}), 500
    elif request.method == "POST":
        new_story = request.json
        if new_story.get("url") and new_story.get("title"):
            create_story(new_story)
            return jsonify({"error": False, "message": "Story created"}), 200
        return jsonify({"error": True, "message": "Please enter title AND url."}), 500


@app.route("/stories/<int:id>/votes", methods=["POST"])
def update_votes(id):
    data = request.json
    if request.method == "POST":
        stories = select_stories()
        story = [story for story in stories if story['id'] == id][0]
        if story.get('score') <= 0 and data.get('direction') == 'down':
            return jsonify({"error": True, "message": "Score cannot be below 0"}), 500
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO votes (id, direction, created, modified) VALUES (%s,%s,%s,%s);""", [id, data.get("direction"), DATE, DATE])
                conn.commit()
    return jsonify({"error": False, "message": "Score Updated"}), 200


def patch_story(data, id):
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        UPDATE stories SET title = %s, url = %s, modified = %s WHERE id = %s;""", [data.get('title'), data.get('url'), DATE, id])
            conn.commit()
    return None


def delete_story(id: int):
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""DELETE FROM stories WHERE id = %s""", [id])
            conn.commit()
    return None


@app.route("/stories/<int:id>", methods=["PATCH", "DELETE"])
def edit(id):
    if request.method == "PATCH":
        edit_request = request.json
        if not (edit_request["title"] and edit_request["url"]):
            return {"error": True, "message": "Title and URL must have input"}
        patch_story(edit_request, id)
        return jsonify({"error": False, "message": "Story Updated"}), 200
    elif request.method == "DELETE":
        delete_story(id)
        return jsonify({"error": False, "message": "Story Deleted"}), 200


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True, host="0.0.0.0", port=5000)
