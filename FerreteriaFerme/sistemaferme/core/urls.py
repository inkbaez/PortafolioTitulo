from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home, login, mostrar_registro_cliente, registrar_cliente, mostrar_datos_cuenta
urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='core/Home.html'), name='logout'),
    path('registro/', mostrar_registro_cliente, name='registro'),
    path('registro_cliente/', registrar_cliente, name='registro_cliente'),
    path('micuenta/', mostrar_datos_cuenta, name='micuenta'),
    
]