from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home, login, mostrar_registro_cliente, registrar_cliente, mostrar_datos_cuenta, actualizar_datos_cuenta, mostrar_agregar_producto, mostrar_agregar_usuario, agregar_proveedor, agregar_empleado, mostrar_actualizar_empleado
urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='core/Home.html'), name='logout'),
    path('registro/', mostrar_registro_cliente, name='registro'),
    path('registro_cliente/', registrar_cliente, name='registro_cliente'),
    path('micuenta/', mostrar_datos_cuenta, name='micuenta'),
    path('actualizar-datos/', actualizar_datos_cuenta, name='actualizar-datos'),
    path('nuevo-producto/', mostrar_agregar_producto, name='nuevo-producto'),
    path('nuevo-usuario/', mostrar_agregar_usuario, name='nuevo-usuario'),
    path('nuevo-proveedor/', agregar_proveedor, name='nuevo-proveedor'),
    path('nuevo-empleado/', agregar_empleado, name='nuevo-empleado'),
    path('actualizar-empleado/<id>/', mostrar_actualizar_empleado, name='actualizar-empleado')
]