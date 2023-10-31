"""Run Web Scraper using local JSON file as storage."""

from datetime import datetime

from flask import Flask, current_app, jsonify, request

from helper_funcs import load_json_file, write_json_file

PATH = "stories.json"
DATE = formatted_time = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
app = Flask(__name__)


def get_stories_by_title(stories, search):
    """Return stories that contains the specified input in its title."""
    matched_stories = [story for story in stories if search in story["title"]]
    if matched_stories:
        return matched_stories
    return stories


def get_stories_by_sort(stories, sort, order) -> list:
    """Return stories in specified sorting and asc/desc order."""
    sort = "created_at" if sort == "created" else sort
    sort = "updated_at" if sort == "modified" else sort
    order = False if order == "ascending" else True
    return sorted(stories, key=lambda story: story[sort], reverse=order)


def create_story(stories, args) -> None:
    """Add new story dict to the stories list."""
    unique_id = sorted(stories, key=lambda story: story["id"], reverse=True)[
        0].get("id")
    stories.append({
        "created_at": DATE,
        "id": unique_id+1,
        "score": 0,
        "title": args.get("title"),
        "updated_at": DATE,
        "url": args.get("url")})


@app.route("/", methods=["GET"])
def index():
    """Static Home Page"""
    return current_app.send_static_file("index.html")


@app.route("/add", methods=["GET"])
def addstory():
    """Static Add Story Page"""
    return current_app.send_static_file("./addstory/index.html")


@app.route("/scrape", methods=["GET"])
def scrape():
    """Static Web Scraping Page"""
    return current_app.send_static_file("./scrape/index.html")


@app.route("/stories", methods=["GET", "POST"])
def get_stories():
    """Retrieve stories and add from JSON file"""
    stories = load_json_file(PATH)
    args = request.args.to_dict()
    if request.method == "GET":
        if "search" in args.keys():
            stories = get_stories_by_title(stories, args.get("search"))
        stories = get_stories_by_sort(
            stories, args.get("sort"), args.get("order"))
        if stories:
            return jsonify(stories), 200
        else:
            return jsonify({"error": True, "message": "No stories were found"}), 500
    elif request.method == "POST":
        new_story = request.json
        if new_story.get("url") and new_story.get("title"):
            stories = create_story(stories, new_story)
            return stories
        return jsonify({"error": True, "message": "Please enter title AND url."}), 500


@app.route("/stories/<int:id>/votes", methods=["POST"])
def update_votes(id):
    """Update story votes"""
    stories = load_json_file(PATH)
    if request.method == "POST":
        data = request.json
        story = next(((i, story) for i, story in enumerate(
            stories) if story["id"] == id), None)
        try:
            if data["direction"] == "up":
                story[1]['score'] += 1
            elif data["direction"] == "down" and story[1]["score"] > 0:
                story[1]["score"] -= 1
            else:
                return jsonify({"error": True, "message": "Can't downvote for a story with a score of 0"}), 400
            story[1]["updated_at"] = DATE
            stories[story[0]] = story[1]
            stories = write_json_file(stories, PATH)
        except KeyError:
            return jsonify({"error": True, "message": "Unable to update vote."}), 500
        return jsonify(load_json_file(PATH)), 200


@app.route("/stories/<int:id>", methods=["PATCH", "DELETE"])
def edit(id):
    stories = load_json_file(PATH)
    story = next(((i, story) for i, story in enumerate(
        stories) if story["id"] == id), None)
    if request.method == "PATCH":
        if (request.json).get("url") and (request.json).get("title"):
            stories[story[0]].update({"title": (request.json).get("title")})
            stories[story[0]].update({"url": (request.json).get("url")})
            stories[story[0]].update({"updated_at": DATE})
    elif request.method == "DELETE":
        del stories[story[0]]
    stories = write_json_file(stories, PATH)
    return jsonify(stories), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
