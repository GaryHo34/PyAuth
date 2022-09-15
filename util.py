import random
from flask_mail import Mail, Message
import cloudinary.uploader
from werkzeug.utils import secure_filename
import os

UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mpeg']
SUCCESS = 'success'
ERROR = 'error'


def generateOTP(length=6):
    OTP = ''
    for _ in range(length):
        num = random.randrange(10)
        OTP += str(num)
    return OTP


def generatedata(status, data, message):
    payload = {
        'status': status,
        'data': data,
        'message': message
    }
    return payload


mail = Mail()


def sendEmailMessage(subject, html, recipient):
    msg = Message(subject=subject,
                  html=html,
                  recipients=[recipient],
                  sender='security@mailtrap.io')
    mail.send(msg)
    return


def isValidImage(file):
    filename = secure_filename(file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext in UPLOAD_EXTENSIONS:
            return True
    return False


def upload_image_to_cloud(file):
    res = cloudinary.uploader.upload(
        file,
        gravity="face",
        height=500,
        width=500,
        crop="thumb",
        folder="ComicReview/flask"
    )
    return {'url': res['secure_url'], 'public_id': res['public_id']}

def isValidVideo(file):
    filename = secure_filename(file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        print(file_ext)
        if file_ext in UPLOAD_EXTENSIONS:
            return True
    return False

def upload_video_to_cloud(file):
    res = cloudinary.uploader.upload(file, folder="ComicReview/flask", resource_type='auto')
    return {'url': res['secure_url'], 'public_id': res['public_id']}

def format_actor(actor):
    return ({
        'id': str(actor.id),
        'name': actor.name,
        'about': actor.about,
        'gender': actor.gender,
        'avatar': actor.avatar['url']
    } if actor.avatar else {
        'id': str(actor.id),
        'name': actor.name,
        'about': actor.about,
        'gender': actor.gender
    })
