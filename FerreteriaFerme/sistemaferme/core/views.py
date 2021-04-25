from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.db import connection
import cx_Oracle
import re
import datetime
from django.contrib import messages
from datetime import datetime
from core.models import *

# Create your views here.


def home(request):
    return render(request, 'core/Home.html')

def login(request):
    return render(request, 'registration/login.html')

def mostrar_registro_cliente(request):
    return render(request, 'registration/registro.html')

def registrar_cliente(request):

    if request.method == 'POST':
        rut = request.POST['rut_cliente']
        nombres = request.POST['nombre']
        apellidos = request.POST['apellido']
        fecha = change_date_format(request.POST['nacimiento'])
        fono = request.POST['fono']
        email = request.POST['email']
        usernamee = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        tipo = request.POST['tipo_cliente']

        try:
            if User.objects.filter(username=usernamee).exists():
                print('===========USUARIO EXISTE EN USER TABLA DJANGO===========')
                messages.error(request, "USUARIO EXISTE EN USER TABLA DJANGO")
                return redirect('registro')
            if User.objects.filter(email=email).exists():
                print('===========EMAIL DE USUARIO EXISTE EN USER TABLA DJANGO===========')
                messages.error(request, "EMAIL DE USUARIO EXISTE EN USER TABLA DJANGO")
                return redirect('registro')
            if password1 != password2:
                print('===========LA CONTRASEÑA NO ES IGUAL A SU CONFIRMACION===========')
                messages.error(request, "LA CONTRASEÑA NO ES IGUAL A SU CONFIRMACION")
                return redirect('registro')

            user = User.objects.create_user(username=usernamee, email=email, password=password2)
            print('=================add user django')
            groupCliente = Group.objects.get(name='ClienteGrupo')
            user.groups.add(groupCliente)
            print('=================grupo asignado user django')
        
            salida = sp_agregar_cliente(usernamee, rut, nombres, apellidos, fecha, fono, email, tipo)
            if salida == 1:
                print('=================add user oracle')
            else:
                print('=================no add user oracle')
            messages.success(request, "Registrado Correctamente")
        except:
            messages.error(request, "Error Al registrar al Usuario")
            return redirect('registro')

    return redirect('login')


def sp_agregar_cliente(username, rut, nombres, apellidos, macimeinto, fono, email, tipo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREATE_CLIENTE',[username, rut, nombres, apellidos, macimeinto, fono, email, tipo, salida])
    return salida.getvalue()

def change_date_format(dt):
        return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', dt)


def mostrar_datos_cuenta(request):

    id_usuario = Usuario.objects.get(username=request.user.username)
    cliente = Cliente.objects.get(id_usuario=id_usuario)
    print(cliente.id_tipo.id_tipo)

    data= {
        'id_usuario': id_usuario,
        'cliente':cliente
        
    }

    return render(request, 'core/Datos_cuenta.html', data)



    

