from app import app, db, User, Article

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(username="alex")
    user2 = User(username="stacey")

    a1 = Article(title="Public Post", content="Visible to everyone.", is_member_only=False)
    a2 = Article(title="Secret Post", content="Exclusive content.", is_member_only=True)

    db.session.add_all([user1, user2, a1, a2])
    db.session.commit()

    print("✅ Database seeded!")
