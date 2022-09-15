from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_mail import Mail
import cloudinary
import cloudinary.uploader
import cloudinary.api
from routes import userRoutes, actorRoutes, movieRoutes
from dotenv import load_dotenv
import os

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_KEY'),
    api_secret=os.getenv('CLOUDINARY_SECRET'),
    secure=True
)

app = Flask("ComicReview")

CORS_ALLOW_ORIGIN = "*,*"
CORS_EXPOSE_HEADERS = "*,*"
CORS_ALLOW_HEADERS = "content-type,*"
cors = CORS(app,
            origins=CORS_ALLOW_ORIGIN.split(","),
            allow_headers=CORS_ALLOW_HEADERS.split(","),
            expose_headers=CORS_EXPOSE_HEADERS.split(","),
            supports_credentials=True)

app.config['MONGODB_SETTINGS'] = {'host': os.environ.get("MONGO_ALTAS_URI")}
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '660d4f20e06ff8'
app.config['MAIL_PASSWORD'] = 'b805cf6edb2c66'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET')

db = MongoEngine()
db.init_app(app)
app.session_interface = MongoEngineSessionInterface(db, collection="sessions")

mail = Mail()
mail.init_app(app)

app.register_blueprint(userRoutes)
app.register_blueprint(actorRoutes)
app.register_blueprint(movieRoutes)

if __name__ == "__main__":
    app.run()
