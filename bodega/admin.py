from django.contrib import admin
from .models import Tiendas, Bodegas, EstadoProducto, EstadoFacturas, Proveedores, Marcas, Productos, Facturas, IngresoProductos, ProductoFactura,SalidaProductos, StockProductos
admin.site.register(Tiendas)
admin.site.register(Bodegas)
admin.site.register(EstadoProducto)
admin.site.register(EstadoFacturas)
admin.site.register(Proveedores)
admin.site.register(Marcas)
admin.site.register(Productos)
admin.site.register(Facturas)
admin.site.register(IngresoProductos)
admin.site.register(ProductoFactura)
admin.site.register(SalidaProductos)
admin.site.register(StockProductos)
