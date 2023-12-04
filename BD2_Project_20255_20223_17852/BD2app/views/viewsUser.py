import json

from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from lxml import etree

from ..database.users import *


def index(request):
    context = {}
    return render(request, 'index.html', context=context)


def register(request):
    if request.method == 'POST':
        user = {
            'name': request.POST['name'],
            'username': request.POST['username'],
            'password': request.POST['password'],
            'role': request.POST['role'],
        }
        print(user)
        result = insertUser(user['name'], user['username'],
                            user['password'], user['role'])
        print(result)
        if result:
            print('User added successfully')
            messages.success(request, 'Conta criada com sucesso')
        else:
            messages.error(request, 'Erro ao criar conta. Username já em uso.')
    context = {}
    return render(request, 'register.html', context=context)


def registerClient(request):
    if request.method == 'POST':
        user = {
            'name': request.POST['name'],
            'username': request.POST['username'],
            'password': request.POST['password'],
            'role': 0,
        }
        result = insertUser(user['name'], user['username'],
                            user['password'], user['role'])
        if result:
            print('User added successfully')
            login(request)
            if login(request):
                return redirect('index')
        else:
            messages.error(request, 'Erro ao criar conta. Username já em uso.')

    context = {}
    return render(request, 'registerClient.html', context=context)


def generate_login_token():
    # Generate a UUID
    token = uuid.uuid4().hex
    # Return the token as a string
    return token


def login(request):
    context = {}
    if request.method == 'POST':
        user = {
            'username': request.POST['username'],
            'password': request.POST['password'],
        }
        result = getUser(user['username'], user['password'])
        if result:
            token = generate_login_token()
            request.session['login_token'] = token
            request.session['user_id'] = result
            print('User logged in successfully')
            print("User ID:", result)
            return redirect('index')
        else:
            print('Invalid credentials')
            messages.error(request, 'Credenciais inválidas')
    return render(request, 'login.html', context=context)


def logout(request):
    if request.method == 'GET':
        request.session.flush()
        request.session.delete(request.session.session_key)
        if 'csrftoken' in request.COOKIES:
            response = render(request, 'index.html')
            response.delete_cookie('csrftoken')
            return response and redirect('index')
        print('User logged out successfully')
    context = {}
    return render(request, 'login.html', context=context)


def profile(request):
    context = {}
    if request.method == 'GET':
        token = request.session.get('login_token')
        if token is not None:
            userId = request.session.get('user_id')
            user = getUserByID(userId)
            context = {'user': user}
        else:
            return redirect('login')
    if request.method == 'POST':
        token = request.session.get('login_token')
        if token is not None:
            userId = request.session.get('user_id')
            user = {
                'username': request.POST['username'],
                'password': request.POST['password'],
            }
            context = {'user': user}
            print(user)
            userProfile = getUserByID(userId)
            if user['username'] == userProfile['username']:
                updateUserPassword(userId, user['password'])
                messages.success(request, 'Utilizador atualizado com sucesso')
                print('User updated successfully')
            else:
                result = updateUser(userId, user['username'], user['password'])
                print(result)
                if result:
                    print('User updated successfully')
                    messages.success(
                        request, 'Utilizador atualizado com sucesso')
                    return redirect('profile')
                else:
                    print('User update failed')
                    messages.error(
                        request, 'Erro ao atualizar utilizador. Nome de utilizador já existe.')
        else:
            return redirect('login')

    return render(request, 'profile.html', context=context)


def downloadUsersJsonFile(request):
    if request.method == 'GET':
        result = exportUsersToJson()
        if result is not False:
            file_path = result
            try:
                with open(file_path, 'rb') as json_file:
                    data = json.load(json_file)
                response = HttpResponse(json.dumps(
                    data, indent=4), content_type="application/json")
                file_name = file_path.split('\\json\\')[1]
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                print('Products exported successfully')
                return response
            except FileNotFoundError:
                raise Http404("File does not exist")
        else:
            print('Error in export products')
    return render(request, 'listAllProducts.html')


def downloadUsersXMLFile(request):
    if request.method == 'GET':
        result = exportUsersToXML()
        if result is not False:
            file_path = result
            try:
                with open(file_path, 'rb') as xml_file:
                    data = etree.fromstring(xml_file.read())
                response = HttpResponse(etree.tostring(
                    data, pretty_print=True), content_type="application/xml")
                file_name = file_path.split('\\xml\\')[1]
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                print('Products exported successfully')
                return response
            except FileNotFoundError:
                raise Http404("File does not exist")
        else:
            print('Error in export products')
    return render(request, 'listAllProducts.html')
