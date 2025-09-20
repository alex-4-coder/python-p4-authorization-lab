from flask import Flask, request, jsonify, session
from flask_migrate import Migrate
from models import db, User, Article

app = Flask(__name__)

# ---------- Config ----------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "super-secret"  # Needed for sessions

db.init_app(app)
migrate = Migrate(app, db)


# ---------- Utility Routes ----------

@app.route("/clear")
def clear_session():
    session.clear()
    return {}, 200


# ---------- Auth Routes ----------

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Invalid username"}), 401

    # Save user_id in session
    session["user_id"] = user.id
    return jsonify({"message": f"Logged in as {user.username}"}), 200


@app.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"}), 200


# ---------- Member-only Routes ----------

@app.route("/members_only_articles")
def member_only_articles():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    articles = Article.query.filter_by(is_member_only=True).all()
    return jsonify([{
        "id": a.id,
        "title": a.title,
        "content": a.content,
        "is_member_only": a.is_member_only
    } for a in articles]), 200


@app.route("/members_only_articles/<int:id>")
def member_only_article(id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    article = Article.query.get(id)
    if not article:
        return jsonify({"error": "Article not found"}), 404

    return jsonify({
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "is_member_only": article.is_member_only
    }), 200


# ---------- Home ----------

@app.route("/")
def index():
    return {"message": "Flask API with session auth running!"}, 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
