# Create your models here.
from django.db import models
from django.db.models import Sum, Prefetch
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from datetime import date, timedelta
from django.db.models.functions import Coalesce




class Tiendas(models.Model):
    id = models.AutoField(primary_key=True)
    posicion = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + ' - ' + self.posicion

class Bodegas(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + ' - ' + self.nombre


class EstadoProducto(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.estado



class EstadoFacturas(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + ' - ' + self.estado


class Proveedores(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    rut = models.CharField(max_length=20)

    def __str__(self):
        return str(self.id) + ' - ' + self.nombre

class Marcas(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=50)
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.nombre_marca


class Productos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    codigo_barras = models.CharField(max_length=50)
    stock_min_tienda = models.IntegerField(default=1)
    marca = models.ForeignKey(Marcas, on_delete=models.CASCADE)
    tienda = models.ForeignKey(Tiendas, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodegas, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Facturas(models.Model):
    id = models.AutoField(primary_key=True)
    folio = models.CharField(max_length=50)
    fecha_emision = models.DateField()
    fecha_recepcion = models.DateField()
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoFacturas, on_delete=models.CASCADE)

    def __str__(self):
        return self.folio

class IngresoProductos(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    factura = models.ForeignKey(Facturas, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_vencimiento = models.DateField()
    estado = models.ForeignKey(EstadoProducto, on_delete=models.CASCADE)
    precio_compra = models.IntegerField()
    precio_venta = models.IntegerField()
    cantidad_restante = models.IntegerField(default=0)


    def __str__(self):
        return str(self.id) + ' - ' + str(self.producto)
    
    @classmethod
    def get_last_price(cls, producto):
        ultima_entrada = cls.objects.filter(producto=producto).order_by('-id').first()
        if ultima_entrada:
            return ultima_entrada.precio_venta
        return None
    
    def actualizar_estado(self):
        fecha_actual = date.today()
        fecha_vencimiento = self.fecha_vencimiento

        # Calcular la diferencia de días entre la fecha de vencimiento y la fecha actual
        diferencia_dias = (fecha_vencimiento - fecha_actual).days

        # Actualizar el estado en función de la diferencia de días
        if diferencia_dias <= 0:
            self.estado = EstadoProducto.objects.get(estado='vencido')
        elif 0 < diferencia_dias <= 30:
            self.estado = EstadoProducto.objects.get(estado='por vencer')
        else:
            self.estado = EstadoProducto.objects.get(estado='OK')

        # Guardar el cambio de estado
        self.save()
    

class ProductoFactura(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    ingreso_producto = models.ForeignKey(IngresoProductos, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.producto)
    
class SalidaProductos(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    fecha = models.DateField()
    motivo = models.CharField(max_length=40)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.producto)

class Import_csv(models.Model):
    id = models.AutoField(primary_key=True)
    codigo_barras = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    fecha = models.DateField()

    def __str__(self):
        return str(self.producto) + ' - ' + str(self.cantidad)
    
    
    
    
class StockProductos(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey('Productos', on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    precio = models.IntegerField(default=0)
    # Variable de clase para mantener el contador
    #contador=0

    def __str__(self):
        return f"{self.id} - {self.producto}"

    def actualizar_stock(self):
        try:
            if self.producto is not None:
                # Actualizar precio
                self.actualizar_precio()
                
                # Actualizar cantidad restante de cada ingreso de producto
                self.actualizar_cantidad_restante()
                
                # Calcular stock
        #        entradas = IngresoProductos.objects.filter(producto=self.producto).aggregate(total_entradas=models.Sum('cantidad'))
                
        #        salidas_import_csv = Import_csv.objects.filter(codigo_barras=self.producto.codigo_barras).aggregate(total_salidas_import_csv=models.Sum('cantidad'))['total_salidas_import_csv'] or 0
        #        salidas_salida_productos = SalidaProductos.objects.filter(producto=self.producto).aggregate(total_salidas_salida_productos=models.Sum('cantidad'))['total_salidas_salida_productos'] or 0
        #        total_salidas = salidas_import_csv + salidas_salida_productos

        #        total_entradas = entradas['total_entradas'] if entradas['total_entradas'] else 0
        #        self.cantidad = total_entradas - total_salidas
                
        #        self.save()
                # Llamar al método para actualizar el stock total
                self.actualizar_stock_total()
                self.save()
                
            else:
                print("------------- ELSE:", self.producto)
        except Productos.DoesNotExist:
            # Maneja el caso en que no hay un producto relacionado
            #pass
            print("No existe")
            
        

    def actualizar_precio(self):
        ingreso_productos = IngresoProductos.objects.filter(producto=self.producto)
        if ingreso_productos.exists():
            ultimo_precio = ingreso_productos.latest('fecha_vencimiento').precio_venta
            self.precio = ultimo_precio
        else:
            self.precio = 0
            
    def actualizar_cantidad_restante(self):
        ingresos = IngresoProductos.objects.filter(producto=self.producto).order_by('fecha_vencimiento')
        salidas_import_csv = Import_csv.objects.filter(codigo_barras=self.producto.codigo_barras).aggregate(total_salidas_import_csv=models.Sum('cantidad'))['total_salidas_import_csv'] or 0
        salidas_salida_productos = SalidaProductos.objects.filter(producto=self.producto).aggregate(total_salidas_salida_productos=models.Sum('cantidad'))['total_salidas_salida_productos'] or 0
        total_salidas = salidas_import_csv + salidas_salida_productos

        a=0
        
        for ingreso in ingresos:
            if a == 0:
                cantidad_restante = ingreso.cantidad - total_salidas
                if cantidad_restante < 0:
                    cantidad_restante = 0
                    a=0
                else:
                    a=1
                ingreso.cantidad_restante = cantidad_restante
                ingreso.save()
                total_salidas = ingreso.cantidad - total_salidas
                
            else:
                cantidad_restante = ingreso.cantidad
                ingreso.cantidad_restante = cantidad_restante
                ingreso.save()
            
            
    @classmethod
    def actualizar_stock_total(cls):
        try:
            # Obtener todos los productos con las entradas y salidas asociadas
            productos = Productos.objects.prefetch_related(
                Prefetch('ingresoproductos_set', queryset=IngresoProductos.objects.annotate(total_entradas=Sum('cantidad_restante'))),
            )

            for producto in productos:
                # Calcular el total de entradas
                total_entradas = sum([ingreso.total_entradas for ingreso in producto.ingresoproductos_set.all()])
                
                # Calcular el stock
                stock = total_entradas
                
                # Actualizar o crear la entrada en StockProductos
                stock_producto, created = cls.objects.get_or_create(producto=producto)
                stock_producto.cantidad = stock
                
        except Productos.DoesNotExist:
            print("No hay productos en la base de datos.")
            return 0
        
        
        
        
        
        
    @classmethod
    def actualizar_stock_total_old(cls):
        try:
            # Obtener todos los productos con las entradas y salidas asociadas
            productos = Productos.objects.prefetch_related(
                Prefetch('ingresoproductos_set', queryset=IngresoProductos.objects.annotate(total_entradas=Sum('cantidad'))),
                Prefetch('salidaproductos_set', queryset=SalidaProductos.objects.annotate(total_salidas=Sum('cantidad')))
            )
            
            progreso_total = productos.count()
            progreso_actual = 0

            for producto in productos:
                # Calcular el total de entradas
                total_entradas = sum([ingreso.total_entradas for ingreso in producto.ingresoproductos_set.all()])
                
                # Calcular el total de salidas
                total_salidas = sum([salida.total_salidas for salida in producto.salidaproductos_set.all()])
                
                # Calcular el stock
                stock = total_entradas - total_salidas
                
                # Actualizar o crear la entrada en StockProductos
                stock_producto, created = cls.objects.get_or_create(producto=producto)
                stock_producto.cantidad = stock
                
        except Productos.DoesNotExist:
            print("No hay productos en la base de datos.")
            return 0
