# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class Boleta(models.Model):
    id_boleta = models.BigIntegerField(primary_key=True)
    fecha_ingreso = models.DateField()
    iva = models.DecimalField(max_digits=10, decimal_places=5)
    sub_total = models.FloatField()
    total = models.BigIntegerField()
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    id_estado = models.ForeignKey('EstadoCompra', models.DO_NOTHING, db_column='id_estado', blank=True, null=True)
    id_pago = models.ForeignKey('MetodoPago', models.DO_NOTHING, db_column='id_pago')

    class Meta:
        managed = False
        db_table = 'boleta'


class Cargo(models.Model):
    id_cargo = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'cargo'


class Carrito(models.Model):
    id_carrito = models.BigIntegerField(primary_key=True)
    cantidad_prod = models.BigIntegerField()
    id_usuario = models.BigIntegerField()
    id_producto = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'carrito'


class Cliente(models.Model):
    id_cliente = models.FloatField(primary_key=True)
    rut_cli = models.CharField(max_length=40)
    nombres = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)
    nacimiento = models.DateField(blank=True, null=True)
    fono = models.BigIntegerField(blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    id_tipo = models.ForeignKey('TipoCliente', models.DO_NOTHING, db_column='id_tipo')
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')

    class Meta:
        managed = False
        db_table = 'cliente'


class DetalleBoleta(models.Model):
    id_detalle = models.BigIntegerField(primary_key=True)
    cantidad_prod = models.BigIntegerField()
    precio_uni = models.BigIntegerField()
    precio_total = models.BigIntegerField()
    id_producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='id_producto')
    id_boleta = models.ForeignKey(Boleta, models.DO_NOTHING, db_column='id_boleta')

    class Meta:
        managed = False
        db_table = 'detalle_boleta'


class DetalleFactura(models.Model):
    id_detalle = models.BigIntegerField(primary_key=True)
    cantidad_prod = models.BigIntegerField()
    precio_uni = models.BigIntegerField()
    precio_total = models.BigIntegerField()
    id_producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='id_producto')
    id_factura = models.ForeignKey('Factura', models.DO_NOTHING, db_column='id_factura')

    class Meta:
        managed = False
        db_table = 'detalle_factura'


class DetalleOrden(models.Model):
    id_detalle = models.BigIntegerField(primary_key=True)
    cantidad_prod = models.BigIntegerField()
    precio_uni = models.BigIntegerField()
    precio_total = models.BigIntegerField()
    id_orden = models.ForeignKey('OrdenCompra', models.DO_NOTHING, db_column='id_orden')
    id_producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='id_producto')

    class Meta:
        managed = False
        db_table = 'detalle_orden'


class Domicilio(models.Model):
    id_domicilio = models.BigIntegerField(primary_key=True)
    region = models.CharField(max_length=30)
    comuna = models.CharField(max_length=30)
    direccion = models.CharField(max_length=200)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domicilio'


class Empleado(models.Model):
    id_empleado = models.FloatField(primary_key=True)
    rut_emp = models.CharField(max_length=20)
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=40)
    id_cargo = models.ForeignKey(Cargo, models.DO_NOTHING, db_column='id_cargo')
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')

    class Meta:
        managed = False
        db_table = 'empleado'


class EstadoCompra(models.Model):
    id_estado = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado_compra'


class EstadoOrden(models.Model):
    id_estado = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'estado_orden'


class Factura(models.Model):
    id_factura = models.BigIntegerField(primary_key=True)
    fecha_ingreso = models.DateField()
    iva = models.DecimalField(max_digits=10, decimal_places=5)
    sub_total = models.FloatField()
    total = models.BigIntegerField()
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    id_estado = models.ForeignKey(EstadoCompra, models.DO_NOTHING, db_column='id_estado', blank=True, null=True)
    id_pago = models.ForeignKey('MetodoPago', models.DO_NOTHING, db_column='id_pago')

    class Meta:
        managed = False
        db_table = 'factura'


class FamiliaProd(models.Model):
    id_familia = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'familia_prod'


class FotoProd(models.Model):
    id_foto = models.BigIntegerField(primary_key=True)
    id_producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='id_producto', blank=True, null=True)
    foto = models.ImageField(upload_to='Productos/', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'foto_prod'


class MetodoPago(models.Model):
    id_pago = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'metodo_pago'


class OrdenCompra(models.Model):
    id_orden = models.BigIntegerField(primary_key=True)
    fecha_ingreso = models.DateField()
    total = models.BigIntegerField()
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    id_estado = models.ForeignKey(EstadoOrden, models.DO_NOTHING, db_column='id_estado', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orden_compra'


class Producto(models.Model):
    id_producto = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=200)
    vencimiento = models.CharField(max_length=20, null=False, blank=False)
    precio = models.BigIntegerField()
    stock = models.BigIntegerField()
    stock_critico = models.BigIntegerField()
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    id_familia = models.ForeignKey(FamiliaProd, models.DO_NOTHING, db_column='id_familia')
    id_tipo = models.ForeignKey('TipoProd', models.DO_NOTHING, db_column='id_tipo')

    class Meta:
        managed = False
        db_table = 'producto'


class Proveedor(models.Model):
    id_proveedor = models.FloatField(primary_key=True)
    rut_provee = models.CharField(max_length=20)
    nombre = models.CharField(max_length=40)
    celular = models.BigIntegerField()
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    id_rubro = models.ForeignKey('Rubro', models.DO_NOTHING, db_column='id_rubro')

    class Meta:
        managed = False
        db_table = 'proveedor'


class Rubro(models.Model):
    id_rubro = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'rubro'


class TipoCliente(models.Model):
    id_tipo = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'tipo_cliente'


class TipoProd(models.Model):
    id_tipo = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=20)
    id_familia = models.ForeignKey(FamiliaProd, models.DO_NOTHING, db_column='id_familia')

    class Meta:
        managed = False
        db_table = 'tipo_prod'


class Usuario(models.Model):
    id_usuario = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=20)
    
    class Meta:
        managed = False
        db_table = 'usuario'
