from flask import request, session
from mongoengine.errors import ValidationError, DoesNotExist
from models.user import Users, EmailToken, PasswordToken
from secrets import token_hex
from util import generateOTP, sendEmailMessage, generatedata, SUCCESS, ERROR
import bcrypt


def create_user():
    body = request.get_json()
    for key, value in body.items():
        body[key] = body[key].strip()
    try:
        oldUser = Users.objects.get(email=body['email'])
    except:
        oldUser = None

    if oldUser:
        return generatedata(ERROR, {}, 'This email is already in used!'), 401

    newUser = Users(**body)
    newUser.password = bcrypt.hashpw(newUser.password.encode(
        'utf-8'), bcrypt.gensalt(10)).decode('utf-8')

    try:
        newUser.save()
    except ValidationError as e:
        (key, value), = e.errors.items()
        return generatedata(ERROR, {},  value.message), 401

    OTP = generateOTP()
    hashed = bcrypt.hashpw(OTP.encode('utf-8'), bcrypt.gensalt(10))

    email_token = EmailToken(owner=newUser, token=hashed)
    email_token.save()

    subject = "Email Verification"
    html = "<div className=\"p\"> Your verification OTP </div><h1 className="" >{OTP}</h1>".format(
        OTP=OTP)
    sendEmailMessage(subject, html, newUser.email)
    userinfo = {
        'id': str(newUser.id),
        'name': newUser.name,
        'email': newUser.email,
    }
    return generatedata(SUCCESS, userinfo,  'user created'), 201


def email_verification():
    body = request.get_json()
    try:
        user = Users.objects.get(id__exact=body['userId'])

    except ValidationError:
        return generatedata(ERROR, {},  'Invalid user'), 401
    except DoesNotExist:
        return generatedata(ERROR, {},  'user not found'), 404

    if user.isVerified:
        return generatedata(ERROR, {},  'user is already verified'), 401

    try:
        email_token = EmailToken.objects.get(owner=user)

    except DoesNotExist:
        return generatedata(ERROR, {},  'token not found'), 404

    if not bcrypt.checkpw(body['OTP'].encode('utf-8'), email_token.token.encode('utf-8')):
        return generatedata(ERROR, {},  'Invalid OTP'), 401

    user.isVerified = True
    user.save()

    email_token.delete()

    subject = "Welcome to APP"
    html = "<div className=\"p\"> Thanks for sign up </div>"
    sendEmailMessage(subject, html, user.email)

    userinfo = {
        'id': str(user.id),
        'name': user.name,
        'email': user.email,
        'isVerified': user.isVerified,
        'role': user.role
    }
    session['user'] = userinfo
    return generatedata(SUCCESS, userinfo, 'Email is verified'), 201


def resendEmailToken():
    body = request.get_json()

    try:
        user = Users.objects.get(id__exact=body['userId'])
    except ValidationError:
        return generatedata(ERROR, {}, 'Invalid user'), 401
    except DoesNotExist:
        return generatedata(ERROR, {}, 'user not found'), 404

    if user.isVerified:
        return generatedata(ERROR, {}, 'user is already verified'), 401

    try:
        email_token = EmailToken.objects.get(owner=user)
    except DoesNotExist:
        email_token = None

    if email_token:
        return generatedata(ERROR, {}, 'please request a new OTP after one hour'), 401

    OTP = generateOTP()
    hashed = bcrypt.hashpw(OTP.encode('utf-8'), bcrypt.gensalt(10))

    new_email_token = EmailToken(owner=user, token=hashed)
    new_email_token.save()

    subject = "Email Verification"
    html = "<div className=\"p\"> Your verification OTP </div><h1 className="" >{OTP}</h1>".format(
        OTP=OTP)
    sendEmailMessage(subject, html, user.email)

    return generatedata(SUCCESS, {}, 'New OTP has been sent'), 201


def forget_password():
    body = request.get_json()

    if not body['email']:
        return generatedata(ERROR, {}, 'Email is missing'), 401

    try:
        user = Users.objects.get(email=body['email'])
    except ValidationError:
        return generatedata(ERROR, {}, 'invalid email'), 401
    except DoesNotExist:
        return generatedata(ERROR, {}, 'user not found'), 404

    new_token = token_hex(30)
    new_password_token = PasswordToken(owner=user, token=new_token)
    try:
        new_password_token.save()

    except ValidationError as e:
        (key, value), = e.errors.items()
        return generatedata(ERROR, {}, value.message), 401

    reset_password_url = 'http://localhost:3000/auth/reset-password?token={}&id={}'.format(
        new_token, user.id)

    subject = "Reset Password Link"
    html = "<div className=\"p\"> Reset password URL: </div><a href={} >Reset Password</a>".format(
        reset_password_url)
    sendEmailMessage(subject, html, user.email)

    return generatedata(SUCCESS, {}, 'Reset link has been sent'), 201


def reset_token_status():
    body = request.get_json()
    userId, token = body['userId'], body['token']

    try:
        reset_token = PasswordToken.objects.get(owner__exact=userId)
    except DoesNotExist:
        return generatedata(ERROR, {}, 'invalid request'), 401
    if reset_token.token != token:
        return generatedata(ERROR, {}, 'invalid request'), 401

    return generatedata(SUCCESS, {'valid': True}, 'Token is verified'), 201


def reset_password():
    body = request.get_json()

    user = Users.objects.get(id__exact=body['userId'])

    if bcrypt.checkpw(body['password'].encode('utf-8'), user.password.encode('utf-8')):
        return generatedata(ERROR, {}, 'New password must be different from the old one'), 401

    user.password = bcrypt.hashpw(body['password'].encode(
        'utf-8'), bcrypt.gensalt(10)).decode('utf-8')
    user.save()
    old_token = PasswordToken.objects.get(owner=user)
    old_token.delete()

    subject = "Password Reset Success"
    html = "<div className=\"p\">Password has reset!</div>"
    sendEmailMessage(subject, html, user.email)

    return generatedata(SUCCESS, {}, 'Password is reset, please log in again'), 201


def log_in():
    body = request.get_json()

    try:
        user = Users.objects.get(email__exact=body['email'])
    except DoesNotExist:
        return generatedata(ERROR, {}, 'Invalid Email/Password'), 401

    if not bcrypt.checkpw(body['password'].encode('utf-8'), user.password.encode('utf-8')):
        return generatedata(ERROR, {}, 'Invalid Email/Password'), 401

    userinfo = {
        'id': str(user.id),
        'name': user.name,
        'email': user.email,
        'isVerified': user.isVerified,
        'role': user.role
    }
    session['user'] = userinfo
    return generatedata(SUCCESS, userinfo, 'Log in success'), 201


def log_out():
    if 'user' not in session:
        return generatedata(ERROR, {}, 'cannot log out'), 401
    session.pop('user')
    return generatedata(SUCCESS, {}, 'logged out'), 201
