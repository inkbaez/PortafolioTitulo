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

    if User.objects.filter(username=usernamee).exists():
        print('===========USUARIO EXISTE EN USER TABLA DJANGO===========')
        messages.error(
            request, "El Nombre de Usuario ya se encuentra asignado a otra cuenta")
        return redirect('registro')
    if User.objects.filter(email=email).exists():
        print(
            '===========EMAIL DE USUARIO EXISTE EN USER TABLA DJANGO===========')
        messages.error(
            request, "Correo Electronico ya se encuentra vinculado a otro usuario")
        return redirect('registro')
    if password1 != password2:
        print(
            '===========LA CONTRASEÑA NO ES IGUAL A SU CONFIRMACION===========')
        messages.error(
            request, "LA CONTRASEÑA NO ES IGUAL A SU CONFIRMACION")
        return redirect('registro')
    try:
        salida = sp_agregar_cliente(
            usernamee, rut, nombres, apellidos, fecha, fono, email, tipo)
        print('=================creado tabla cliente')
        user = User.objects.create_user(
            username=usernamee, email=email, password=password2)
        print('=================creado tabla user django')
        groupCliente = Group.objects.get(name='ClienteGrupo')
        user.groups.add(groupCliente)
        print('=================grupo asignado user django')

        if salida == 1:
            messages.success(request, "Registrado Correctamente")
            return redirect('login')
        else:
            messages.error(request, "Error Al registrar al Usuario")
            return redirect('registro')
    except:
        messages.error(request, "Error Al registrar al Usuario")
    return redirect('registro')


def sp_agregar_cliente(username, rut, nombres, apellidos, macimeinto, fono, email, tipo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREATE_CLIENTE', [
                    username, rut, nombres, apellidos, macimeinto, fono, email, tipo, salida])
    return salida.getvalue()


def change_date_format(dt):
    return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', dt)


def mostrar_datos_cuenta(request):

    id_usuario = Usuario.objects.get(username=request.user.username)
    cliente = Cliente.objects.get(id_usuario=id_usuario)
    print(cliente.id_tipo.id_tipo)

    data = {
        'id_usuario': id_usuario,
        'cliente': cliente

    }

    return render(request, 'core/Datos_cuenta.html', data)


def actualizar_datos_cuenta(request):

    nombres = request.POST['nombre']
    ape = request.POST['apellido']
    fecha = request.POST['nacimiento']
    fono = request.POST['fono']
    email = request.POST['email']

    usermail = User.objects.get(email=email)
    if usermail.username != request.user.username:
        messages.error(
            request, "El Correo Electronico ya le pertenece a otra Cuenta")
        return redirect('micuenta')

    try:
        User.objects.filter(username=request.user.username).update(email=email)

        user = Usuario.objects.filter(username=request.user.username).first()

        id_user = user.id_usuario
        print(id_user)

        Cliente.objects.filter(id_usuario=user).update(
            nombres=nombres, apellidos=ape, nacimiento=fecha, fono=fono, email=email)

        messages.success(request, "Actualizado Correctamente")
    except:
        messages.error(request, "No se ha podido Actualizar los datos")
    return redirect('micuenta')


def mostrar_agregar_usuario(request):
    cargo = Cargo.objects.all()
    rubro = Rubro.objects.all()
    empleados = Empleado.objects.all()
    proveedores = Proveedor.objects.all()

    data = {
        'cargo': cargo,
        'rubro': rubro,
        'empleados': empleados,
        'proveedores': proveedores
    }

    return render(request, 'core/Agregar_usuario.html', data)


def agregar_proveedor(request):
    if request.method == 'POST':
        rut = request.POST['rut_pro']
        nombre = request.POST['nombre_pro']
        usernamee = request.POST['username_pro']
        password = request.POST['password_pro']
        password2 = request.POST['password2_pro']
        email = request.POST['mail_pro']
        fono = request.POST['fono_pro']
        rubro = request.POST['rubro_pro']
        
    if password != password2:
        messages.error(
            request, "LA CONTRASEÑA NO ES IGUAL A SU CONFIRMACION")
        return redirect('nuevo-usuario')

    try:
        salida = sp_agregar_proveedor(
            usernamee, rut, nombre, fono, rubro)
        print('=================creado tabla proveedor')
        user = User.objects.create_user(
            username=usernamee, email=email, password=password2)
        print('=================creado tabla user django')
        groupProo = Group.objects.get(name='ProveedorGrupo')
        user.groups.add(groupProo)
        print('=================grupo asignado user django')

        if salida == 1:
            messages.success(request, "Registrado Correctamente")
            return redirect('nuevo-usuario')
        else:
            messages.error(request, "Error Al registrar al Usuario")
            return redirect('nuevo-usuario')
    except:
        messages.error(request, "Error Al registrar al Usuario")
    return redirect('nuevo-usuario')

def agregar_empleado(request):
    if request.method == 'POST':
        rut = request.POST['rut_emp']
        nombres = request.POST['nombres_emp']
        apellidos = request.POST['apellidos_emp']
        usernamee = request.POST['username_emp']
        password = request.POST['password_emp']
        password2 = request.POST['password2_emp']
        email = request.POST['mail_emp']
        cargo = request.POST['cargo_emp']
        
    if password != password2:
        messages.error(
            request, "LA CONTRASEÑA NO ES IGUAL A SU CONFIRMACION")
        return redirect('nuevo-usuario')

    try:
        salida = sp_agregar_empleado(
            usernamee, rut, nombres, apellidos, cargo)
        print('=================creado tabla proveedor')
        user = User.objects.create_user(
            username=usernamee, email=email, password=password2)
        print('=================creado tabla user django')
        groupEmp = Group.objects.get(name='EmpleadoGrupo')
        user.groups.add(groupEmp)
        print('=================grupo asignado user django')

        if salida == 1:
            messages.success(request, "Registrado Correctamente")
            return redirect('nuevo-usuario')
        else:
            messages.error(request, "Error Al registrar al Usuario")
            return redirect('nuevo-usuario')
    except:
        messages.error(request, "Error Al registrar al Usuario")
    return redirect('nuevo-usuario')

def sp_agregar_proveedor(username, rut, nombre, fono, rubro):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREATE_PROVEEDOR', [
                    username, rut, nombre, fono, rubro, salida])
    return salida.getvalue()

def sp_agregar_empleado(username, rut, nombres, apellidos, cargo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREATE_EMPLEADO', [
                    username, rut, nombres, apellidos, cargo, salida])
    return salida.getvalue()

def mostrar_actualizar_empleado(request, id):
    
    empleado = Empleado.objects.get(id_empleado=id)
    cargo = Cargo.objects.all()

    data = {
        'empleado':empleado,
        'cargo':cargo
    }

    return render(request, 'modal/actualizar_usuario.html', data)






def mostrar_agregar_producto(request):
    familia = FamiliaProd.objects.all()
    tipo = TipoProd.objects.all()
    proveedor = Proveedor.objects.all()

    data = {
        'familia': familia,
        'tipo': tipo,
        'proveedor':proveedor
    }

    return render(request, 'core/Agregar_producto.html', data)
