from django.forms import model_to_dict
from django.http.response import HttpResponseNotAllowed, JsonResponse, HttpResponse, HttpResponseNotFound
from django.contrib.auth import authenticate
import django.contrib.auth.models as user_model
from .models import User, Photo
import requests
import json


def sign_up(request):
    if request.method == 'POST':
        # request.body will have 'username', 'password', and 'g-recaptcha-response' attribute.
        # If username or password is empty, return code '1'.
        # If password fields are not matching, return code '2'.
        # If reCAPTCHA is not done, return code '3'.
        # If reCAPTCHA is done but failed, return code '4'.
        # If username is already occupied, return code '5'.
        # If login succeeded, return code '0'.

        request_data = json.loads(request.body.decode())

        # Check the username or password is empty
        username = request_data['username']
        password = request_data['password']
        password_check = request_data['password_check']

        if len(username) == 0 or len(password) == 0 or len(password_check) == 0:
            return JsonResponse({'success': False, 'error-code': 1})

        # Check the password field is matching
        if password != password_check:
            return JsonResponse({'success': False, 'error-code': 2})

        # Check the reCAPTCHA status
        if 'g-recaptcha-response' not in request_data:
            # User didn't finished reCAPTCHA.
            return JsonResponse({'success': False, 'error-code': 3})
        else:
            # Check reCAPTCHA succeeded or not.
            post_data = {'secret': '6Lf5TDcUAAAAAJKCf060w7eduUXl9P677tqXL1Cg',
                         'response': request_data['g-recaptcha-response']}
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=post_data)
            response_data = json.loads(response.content)
            if not response_data['success']:
                return JsonResponse({'success': False, 'error-code': 4})

        # Check the username is available
        try:
            user_model.User.objects.get(username=username)
            return JsonResponse({'success': False, 'error-code': 5})
        except user_model.User.DoesNotExist:
            # Can be signed up at this point.
            user = user_model.User(username=username, password=password)
            user.save()

            # TODO: Change User Creation. Maybe Using the level, and call initializers after initializing and save?
            User.objects.create(user=user, today_write_count=3, today_reply_count=3, total_likes=2)
            return JsonResponse({'success': True, 'error-code': 0})

    else:
        return HttpResponseNotAllowed(['POST'])


def sign_in(request):
    if request.method == 'POST':
        # request.body will have 'username', 'password', and 'g-recaptcha-response' attribute.
        # If username or password is empty, return code '1'.
        # If reCAPTCHA is not done, return code '2'.
        # If reCAPTCHA is done but failed, return code '3'.
        # If username and password is not matching, return code '4'.
        # If login succeeded, return code '0'.

        request_data = json.loads(request.body.decode())

        # Check the username or password is empty
        username = request_data['username']
        password = request_data['password']

        if len(username) == 0 or len(password) == 0:
            return JsonResponse({'success': False, 'error-code': 1})

        # Check the reCAPTCHA status
        if 'g-recaptcha-response' not in request_data:
            # User didn't finished reCAPTCHA.
            return JsonResponse({'success': False, 'error-code': 2})
        else:
            # Check reCAPTCHA succeeded or not.
            post_data = {'secret': '6LdqTDcUAAAAAMg6MerfUa0BZAnpVb7NnerIfZgE',
                         'response': request_data['g-recaptcha-response']}
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=post_data)
            if not response.content['success']:
                return JsonResponse({'success': False, 'error-code': 3})

        # Check the username and password matches.
        user = authenticate(request, username=username, password=password)
        if user is None:
            # username and password doesn't match.
            return JsonResponse({'success': False, 'error-code': 4})
        else:
            # login succeeded.
            return JsonResponse({'success': False, 'error-code': 0})

    else:
        return HttpResponseNotAllowed(['POST'])


def photo_list(request):
    if request.method == 'GET':
        # get random 9 photos of a specific color
        return JsonResponse(list(Photo.objects.all().values().order_by('?')[:9]), safe=False)

    elif request.method == 'POST':
        request_data = json.loads(request.body.decode())

        # image
        author = request.user
        color = json.loads(request.body.decode())['color']

        new_photo = Photo(author=author, color=color)
        new_photo.save()
        return HttpResponse(status=201)

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


def photo_list_color(request, photo_color):
    # get random 9 photos of a specific color
    if request.method == 'GET':
        return JsonResponse(list(Photo.objects.all().values()
                                 .filter(lambda photo: photo.color == photo_color)
                                 .order_by('?')[:9])
                            , safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])


def photo_detail(request, photo_id):
    photo_id = int(photo_id)
    try:
        photo = Photo.objects.get(id=photo_id)
    except Photo.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == 'GET':
        photo_dict = model_to_dict(photo)
        return JsonResponse(photo_dict)
    elif request.method == 'PUT':
        is_reported = json.loads(request.body.decode())['is_report']
        photo.is_reported = True
        photo.save()
        return HttpResponse(status=204)   # 204: No content
    elif request.method == 'DELETE':
        if request.user != photo.author:
            return HttpResponse(status=403)

        photo.delete()
        return HttpResponse(status=204)   # 204: No content
    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])