from django import forms

from .models import Import_csv, Tiendas, Bodegas, EstadoProducto, EstadoFacturas, Proveedores, Marcas, Productos, Facturas, IngresoProductos, ProductoFactura, SalidaProductos, StockProductos


class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodegas
        fields = ['id', 'nombre']

class ProveedoresForm(forms.ModelForm):
    class Meta:
        model = Proveedores
        fields = ['id', 'nombre', 'rut']

class TiendaForm(forms.ModelForm):
    class Meta:
        model = Tiendas
        fields = ['id', 'posicion']

class EstadoProductoForm(forms.ModelForm):
    class Meta:
        model = EstadoProducto
        fields = ['id', 'estado']

class EstadoFacturasForm(forms.ModelForm):
    class Meta:
        model = EstadoFacturas
        fields = ['id', 'estado']

class MarcasForm(forms.ModelForm):
    class Meta:
        model = Marcas
        fields = ['id', 'nombre_marca', 'proveedor']

class ProductosForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['id', 'nombre', 'codigo_barras', 'stock_min_tienda', 'marca', 'tienda', 'bodega']

class FacturasForm(forms.ModelForm):
    class Meta:
        model = Facturas
        fields = ['id', 'folio', 'fecha_emision', 'fecha_recepcion', 'proveedor', 'estado']

class IngresoProductosForm(forms.ModelForm):
    class Meta:
        model = IngresoProductos
        fields = ['id', 'producto', 'factura', 'cantidad', 'fecha_vencimiento', 'estado', 'precio_compra', 'precio_venta']

class Import_csvForm(forms.ModelForm):
    class Meta:
        model = Import_csv
        fields = ['id','codigo_barras', 'nombre', 'cantidad', 'fecha']

class StockProductosForm(forms.ModelForm):
    class Meta:
        model = StockProductos
        fields = ['id', 'producto', 'cantidad', 'precio']
        