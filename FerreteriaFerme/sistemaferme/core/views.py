from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.db import connection
import cx_Oracle
import re
import datetime
from django.contrib import messages
from datetime import datetime
from .models import *
import cloudinary.uploader


# Create your views here.


def home(request):
    if Group.objects.filter(name='ClienteGrupo').count() < 1:
       Group.objects.create(name='ClienteGrupo')

    if Group.objects.filter(name='EmpleadoGrupo').count() < 1:
       Group.objects.create(name='EmpleadoGrupo')

    if Group.objects.filter(name='ProveedorGrupo').count() < 1:
       Group.objects.create(name='ProveedorGrupo')

    if Group.objects.filter(name='SuperUsuarioGrupo').count() < 1:
       Group.objects.create(name='SuperUsuarioGrupo')

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
        print('=================creado tabla empleado')
        user = User.objects.create_user(
            username=usernamee, email=email, password=password2)
        print('=================creado tabla user django')
        if cargo == '3':
            groupAdm = Group.objects.get(name='SuperUsuarioGrupo')
            user.groups.add(groupAdm)
            print('=================grupo asignado user django como SuperUsuarioGrupo')
        else:
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



def actualizar_empleado(request):
    if request.method == 'POST':
        id_usu = request.POST['id_usu']
        rut = request.POST['rut_emp']
        nombres = request.POST['nombres_emp']
        apellidos = request.POST['apellidos_emp']
        cargo = request.POST['cargo_emp']
        usernamee = request.POST['username_emp']
    try:
        Empleado.objects.filter(id_usuario=id_usu).update(rut_emp=rut, nombres=nombres, apellidos=apellidos, id_cargo=cargo)
        userOra = Usuario.objects.get(id_usuario=id_usu)
        userDJ = User.objects.get(username=userOra.username)
        userDJ.groups.clear()
        User.objects.filter(username=userOra.username).update(username=usernamee)
        Usuario.objects.filter(id_usuario=id_usu).update(username=usernamee)
        if cargo == '3':
            groupAdm = Group.objects.get(name='SuperUsuarioGrupo')
            userDJ.groups.add(groupAdm)
            print('=================grupo asignado user django como SuperUsuarioGrupo')
        else:
            groupEmp = Group.objects.get(name='EmpleadoGrupo')
            userDJ.groups.add(groupEmp)
            print('=================grupo asignado user django')
        
        messages.success(request, "Actualizado Correctamente")
        return redirect('nuevo-usuario')    
    except:
        messages.error(request, "Error Al Actualizar Usuario")
        return redirect('nuevo-usuario')
    return redirect('nuevo-usuario')



def actualizar_proveedor(request):
    if request.method == 'POST':
        id_usu = request.POST['id_usu']
        rut = request.POST['rut_pro']
        nombre = request.POST['nombre_pro']
        celular = request.POST['fono_pro']
        rubro = request.POST['rubro_pro']
        usernamee = request.POST['username_pro']
    try:
        Proveedor.objects.filter(id_usuario=id_usu).update(rut_provee=rut, nombre=nombre, celular=celular, id_rubro=rubro)
        userOra = Usuario.objects.get(id_usuario=id_usu)
        #userDJ = User.objects.get(username=userOra.username)
        #userDJ.groups.clear()
        User.objects.filter(username=userOra.username).update(username=usernamee)
        Usuario.objects.filter(id_usuario=id_usu).update(username=usernamee)
        
        messages.success(request, "Actualizado Correctamente")
        return redirect('nuevo-usuario')    
    except:
        messages.error(request, "Error Al Actualizar Usuario")
        return redirect('nuevo-usuario')
    return redirect('nuevo-usuario')

def eliminar_empleado(request, id):

    try:
        Empleado.objects.filter(id_usuario=id).delete()
        UserOra = Usuario.objects.get(id_usuario=id)
        User.objects.filter(username=UserOra.username).delete()
        Usuario.objects.filter(id_usuario=id).delete()

        messages.success(request, 'Usuario Eliminado Correctamente')
    except:
        messages.error(request, 'Error Al Eliminar Usuario')

    return redirect('nuevo-usuario')

def eliminar_proveedor(request, id):

    try:
        Proveedor.objects.filter(id_usuario=id).delete()
        UserOra = Usuario.objects.get(id_usuario=id)
        User.objects.filter(username=UserOra.username).delete()
        Usuario.objects.filter(id_usuario=id).delete()

        messages.success(request, 'Usuario Eliminado Correctamente')
    except:
        messages.error(request, 'Error Al Eliminar Usuario')

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
    
    empleado = Empleado.objects.get(id_usuario=id)
    usuarioOra = Usuario.objects.get(id_usuario=id)
    cargo = Cargo.objects.all()
    data = {
        'empleado':empleado,
        'cargo':cargo,
        'usuarioOra':usuarioOra
    }

    return render(request, 'modal/actualizar_empleado.html', data)

def mostrar_actualizar_proveedor(request, id):
    
    proveedor = Proveedor.objects.get(id_usuario=id)
    usuarioOra = Usuario.objects.get(id_usuario=id)
    rubro = Rubro.objects.all()
    data = {
        'proveedor':proveedor,
        'rubro':rubro,
        'usuarioOra':usuarioOra
    }

    return render(request, 'modal/actualizar_proveedor.html', data)



def mostrar_agregar_producto(request):
    familia = FamiliaProd.objects.all()
    proveedor = Proveedor.objects.all()

    data = {
        'familia': familia,
        'proveedor':proveedor,
        'productos':listado_productos()
    }

    return render(request, 'core/Agregar_producto.html', data)

def tipo_producto_por_familia(request):
    idfamilia = request.GET.get('idfamilia')
    data = {
        'tipoProdcuto':listar_tipo_producto_por_familia(idfamilia)
    }

    return render(request, 'combobox/tipo_x_familia.html', data)

def listar_tipo_producto_por_familia(id_familia):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_TIPOPRODUCTO_POR_FAMILIA", [out_cur, id_familia])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    
    return lista

def agregar_producto(request):
    if request.method == 'POST':
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        stock = request.POST['stock']
        critico = request.POST['critico']
        vencimiento = change_date_format(request.POST['vencimiento'])
        proveedor = request.POST['proveedor']
        Familia = request.POST['Familia']
        foto_ = request.FILES.get('foto')
        
    try:
        new_id = int(sp_obtener_id_producto(proveedor, Familia, vencimiento))
        salida = sp_crear_producto(new_id, descripcion, vencimiento, precio, stock, critico, proveedor, Familia)
        foto_id = int(sp_obtener_id_foto_prod())
        FotoProd.objects.create(id_foto=foto_id, foto=foto_)
        FotoProd.objects.filter(id_foto=foto_id).update(id_producto=new_id)
        
        messages.success(request, 'Producto Registrado Correctamente')
    except:
        messages.error(request, 'Error, Al Registrar Prodcuto')

    return redirect('nuevo-producto')


def sp_crear_producto(id_producto, descripcion, vencimiento, precio, stock, stock_critico, id_proveedor, id_familia):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREATE_PRODUCTO', [
                    id_producto, descripcion, vencimiento, precio, stock, stock_critico, id_proveedor, id_familia, salida])
    return salida.getvalue()


def sp_agregar_foto_producto(id_proveedor, foto):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREATE_FOTO_PRODUCTO', [
                    id_proveedor, foto, salida])
    return salida.getvalue()

def sp_obtener_id_producto(id_proveedor, id_familia, vencimiento):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.STRING)
    cursor.callproc('SP_OBTENER_ID_PRODUCTO', [
                    id_proveedor, id_familia, vencimiento, salida])
    return salida.getvalue()

def sp_obtener_id_foto_prod():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_OBTENER_ID_FOTO_PROD', [salida])
    return salida.getvalue()

def mostrar_productos(request):

    data = {
        'productos':listado_productos()
    }

    return render(request, 'core/Productos.html', data)
    
def listado_productos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PRODUCTOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    
    return lista

def mostrar_detalle_producto(request, id):
    
    producto = Producto.objects.get(id_producto=id)
    foto = FotoProd.objects.get(id_producto=id)
    
    data = {
        'producto':producto,
        'foto':foto
    }

    return render(request, 'modal/producto_detalle.html', data)

def mostrar_actualizar_producto(request, id):
    
    producto = Producto.objects.get(id_producto=id)
    foto = FotoProd.objects.get(id_producto=id)
    proveedor = Proveedor.objects.all()
    familia = FamiliaProd.objects.all()

    data = {
        'producto':producto,
        'foto':foto,
        'proveedor':proveedor,
        'familia': familia
    }

    return render(request, 'modal/actualizar_producto.html', data)