from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)


# Hilfsfunktion: Blogposts aus JSON-Datei laden
def load_posts():
    if not os.path.exists("posts.json"):
        return []
    with open("posts.json", "r") as f:
        return json.load(f)


# Hilfsfunktion: Blogposts speichern
def save_posts(posts):
    with open("posts.json", "w") as f:
        json.dump(posts, f, indent=4)


# Startseite
@app.route("/")
def index():
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


# Neuen Beitrag hinzufügen
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        posts = load_posts()
        new_id = max([p["id"] for p in posts], default=0) + 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content,
            "likes": 0,
        }

        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for("index"))

    return render_template("add.html")


# Blogbeitrag bearbeiten
@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        post["author"] = request.form.get("author")
        post["title"] = request.form.get("title")
        post["content"] = request.form.get("content")
        save_posts(posts)
        return redirect(url_for("index"))

    return render_template("update.html", post=post)


# Blogbeitrag löschen
@app.route("/delete/<int:post_id>")
def delete(post_id):
    posts = load_posts()
    posts = [post for post in posts if post["id"] != post_id]
    save_posts(posts)
    return redirect(url_for("index"))


# Like-Funktion
@app.route("/like/<int:post_id>")
def like(post_id):
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            post["likes"] = post.get("likes", 0) + 1
            break
    save_posts(posts)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)