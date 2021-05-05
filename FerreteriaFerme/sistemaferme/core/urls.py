from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home, login, mostrar_registro_cliente, registrar_cliente, mostrar_datos_cuenta, actualizar_datos_cuenta, mostrar_agregar_producto, mostrar_agregar_usuario, agregar_proveedor, agregar_empleado, mostrar_actualizar_empleado, actualizar_empleado, mostrar_actualizar_proveedor, actualizar_proveedor, eliminar_empleado, eliminar_proveedor, tipo_producto_por_familia,agregar_producto, mostrar_productos, mostrar_detalle_producto, mostrar_actualizar_producto
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
    path('actualizar-empleado/<id>/', mostrar_actualizar_empleado, name='actualizar-empleado'), 
    path('edit_empleado/', actualizar_empleado, name='edit_empleado'),
    path('actualizar-proveedor/<id>/', mostrar_actualizar_proveedor, name='actualizar-proveedor'),
    path('edit_proveedor/', actualizar_proveedor, name='edit_proveedor'),
    path('eliminar_empleado/<id>/', eliminar_empleado, name='eliminar_empleado'),
    path('eliminar_proveedor/<id>/', eliminar_proveedor, name='eliminar_proveedor'),
    path('tipoProducto_por_familia/', tipo_producto_por_familia, name='tipoProducto_por_familia'),
    path('agregar-producto/', agregar_producto, name='agregar-producto'),
    path('listado-producto/', mostrar_productos, name='listado-producto'),
    path('detalle-producto/<id>/', mostrar_detalle_producto, name='detalle-producto'),
    path('actualizar-producto/<id>/', mostrar_actualizar_producto, name='actualizar-producto')
]