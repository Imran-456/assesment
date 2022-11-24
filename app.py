from src import app, db
from src.models.db_models import user, posts

if __name__ == '__main__':
    # Initilize DB
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(debug=True)
