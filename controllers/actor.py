from flask import request
from middleware import is_auth, is_admin
from mongoengine.errors import ValidationError, DoesNotExist
import cloudinary.uploader
from models.actor import Actors
from util import generatedata, upload_image_to_cloud, format_actor, isValidImage, SUCCESS, ERROR


@is_auth
@is_admin
def create_actor():
    if str(request.user['role']) != 'admin':
        return generatedata(ERROR, {},  'user not logged in'), 401
    data = request.form
    file = request.files['avatar'] if request.files else None
    
    newActor = Actors(**data)

    if file:
        if not isValidImage(file):
            return generatedata(ERROR, {},  'Supported only image file'), 401
        newActor.avatar = upload_image_to_cloud(file)

    try:
        newActor.save()
    except ValidationError as e:
        #(key, value), = e.errors.items()
        print(e)
        return generatedata(ERROR, {},  " "), 401

    return generatedata(SUCCESS, format_actor(newActor), 'actor created'), 201


def update_actor(actorId):
    data = request.form
    file = request.files['avatar'] if request.files else None

    try:
        actor = Actors.objects.get(id__exact=actorId)
    except ValidationError:
        return generatedata(ERROR, {}, 'Invalid actor'), 401
    except DoesNotExist:
        return generatedata(ERROR, {}, 'actor not found'), 404

    # remive old image if there was one!
    public_id = actor.avatar['public_id'] if actor.avatar else None

    if public_id and file:
        res = cloudinary.uploader.destroy(public_id)
        if res['result'] != 'ok':
            return generatedata(res, ERROR, {}, 'Could not remove image'), 401

    if file:
        if not isValidImage(file):
            return generatedata(ERROR, {},  'Supported only image file'), 401
        actor.avatar = upload_image_to_cloud(file)

    actor.name = data['name']
    actor.about = data['about']
    actor.about = data['about']

    try:
        actor.save()
    except ValidationError as e:
        (key, value), = e.errors.items()
        return generatedata(ERROR, {},  value.field_name + ' ' + value.message), 401

    return generatedata(SUCCESS, format_actor(actor), 'actor created'), 201


def delete_actor(actorId):
    try:
        actor = Actors.objects.get(id__exact=actorId)
    except ValidationError:
        return generatedata(ERROR, {}, 'Invalid actor'), 401
    except DoesNotExist:
        return generatedata(ERROR, {}, 'actor not found'), 404

    # remive old image if there was one!
    public_id = actor.avatar['public_id'] if actor.avatar else None
    if public_id:
        res = cloudinary.uploader.destroy(public_id)
        if res['result'] != 'ok':
            return generatedata(res, ERROR, {}, 'Could not remove image'), 401

    actor.delete()
    return generatedata(SUCCESS, {}, 'actor deleted'), 201


def search_actors():
    name = request.args.get('name')
    name = '"' + name + '"'
    results = Actors.objects(__raw__={'$text': {'$search': name}})
    search_result = []
    for actor in results:
        search_result.append(format_actor(actor))
    return generatedata(SUCCESS, search_result, 'actor created'), 201


def get_latest_actors():
    results = Actors.objects(__raw__={}).order_by('-createdAt')[:12]
    search_result = []
    for actor in results:
        search_result.append(format_actor(actor))
    return generatedata(SUCCESS, search_result, 'actor created'), 201


def get_single_actor(actorId):
    try:
        result = Actors.objects.get(id__exact=actorId)
    except ValidationError:
        return generatedata(ERROR, {}, 'Invalid actor'), 401
    except DoesNotExist:
        return generatedata(ERROR, {}, 'actor not found'), 404

    return generatedata(SUCCESS, format_actor(result), 'actor created'), 201
