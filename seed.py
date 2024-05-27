from app.extensions import db, bcrypt
from app.models.posts import Post
from app.models.users import User

db.drop_all()
db.create_all()
