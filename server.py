from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder="public")

POSTS = {
    "A9F3QK": {
        "id": "A9F3QK",
        "community": "tech",
        "slug": "best-programming-language",
        "title": "Best programming language?",
        "type": "poll",
        "options": ["JavaScript", "Python", "Rust", "Other"]
    }
}

@app.route("/api/post/<post_id>")
def get_post(post_id):
    post = POSTS.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    return send_from_directory("public", "index.html")

app.run(debug=True)
