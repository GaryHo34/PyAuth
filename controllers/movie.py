from flask import request
from middleware import is_auth, is_admin
from mongoengine.errors import ValidationError, DoesNotExist
import cloudinary.uploader
from models.actor import Actors
from util import generatedata, upload_video_to_cloud, isValidVideo, SUCCESS, ERROR


@is_auth
@is_admin
def upload_trailer():

    file = request.files['video'] if request.files else None

    if file:
        if not isValidVideo(file):
            return generatedata(ERROR, {},  'Supported only video file'), 401
        res = upload_video_to_cloud(file)

    return generatedata(SUCCESS, res, 'video created'), 201