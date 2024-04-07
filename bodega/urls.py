from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('get_chart/', views.get_chart, name='get_chart'),
    path('obtener_estadisticas/', views.obtener_estadisticas, name='obtener_estadisticas'),
    path('nosotros/', views.nosotros, name='nosotros'),
    
    path('proveedores/', views.proveedores, name='proveedores'),
    path('proveedores/crear', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/editar/<int:id>', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>', views.eliminar_proveedor, name='eliminar_proveedor'),
    
    path('bodegas/', views.bodegas, name='bodegas'),
    path('bodegas/crear', views.crear_bodega, name='crear_bodega'),
    path('bodegas/editar', views.editar_bodega, name='editar_bodega'),
    path('bodegas/editar/<int:id>', views.editar_bodega, name='editar_bodega'),
    path('bodegas/eliminar/<int:id>', views.eliminar_bodega, name='eliminar_bodega'),
    
    path('tiendas/', views.tiendas, name='tiendas'),
    path('tiendas/crear', views.crear_tienda, name='crear_tienda'),
    path('tiendas/editar', views.editar_tienda, name='editar_tienda'),
    path('tiendas/editar/<int:id>', views.editar_tienda, name='editar_tienda'),
    path('tiendas/eliminar/<int:id>', views.eliminar_tienda, name='eliminar_tienda'),
    
    path('estadoProductos/', views.estadoProductos, name='estadoProductos'),
    path('estadoProductos/crear', views.crear_estadoProducto, name='crear_estadoProducto'),
    path('estadoProductos/editar', views.editar_estadoProducto, name='editar_estadoProducto'),
    path('estadoProductos/editar/<int:id>', views.editar_estadoProducto, name='editar_estadoProducto'),
    path('estadoProductos/eliminar/<int:id>', views.eliminar_estadoProducto, name='eliminar_estadoProducto'),
    
    path('estadoFacturas/', views.estadoFacturas, name='estadoFacturas'),
    path('estadoFacturas/crear', views.crear_estadoFactura, name='crear_estadoFactura'),
    path('estadoFacturas/editar', views.editar_estadoFactura, name='editar_estadoFactura'),
    path('estadoFacturas/editar/<int:id>', views.editar_estadoFactura, name='editar_estadoFactura'),
    path('estadoFacturas/eliminar/<int:id>', views.eliminar_estadoFactura, name='eliminar_estadoFactura'),

    path('marcas/', views.marcas, name='marcas'),
    path('marcas/crear', views.crear_marca, name='crear_marca'),
    path('marcas/editar', views.editar_marca, name='editar_marca'),
    path('marcas/editar/<int:id>', views.editar_marca, name='editar_marca'),
    path('marcas/eliminar/<int:id>', views.eliminar_marca, name='eliminar_marca'),

    path('productos/', views.productos, name='productos'),
    path('productos/crear', views.crear_producto, name='crear_producto'),
    path('productos/editar', views.editar_producto, name='editar_producto'),
    path('productos/editar/<int:id>', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>', views.eliminar_producto, name='eliminar_producto'),

    path('facturas/', views.facturas, name='facturas'),
    path('facturas/crear', views.crear_factura, name='crear_factura'),
    path('facturas/editar', views.editar_factura, name='editar_factura'),
    path('facturas/editar/<int:id>', views.editar_factura, name='editar_factura'),
    path('facturas/eliminar/<int:id>', views.eliminar_factura, name='eliminar_factura'),
    path('facturas/<int:factura_id>/cambiar_estado/', views.cambiar_estado_factura, name='cambiar_estado_factura'),
   

    path('ingresoProductos/', views.ingresoProductos, name='ingresoProductos'),
    path('ingresoProductos/crear', views.crear_ingresoProducto, name='crear_ingresoProducto'),
    path('ingresoProductos/editar', views.editar_ingresoProducto, name='editar_ingresoProducto'),
    path('ingresoProductos/editar/<int:id>', views.editar_ingresoProducto, name='editar_ingresoProducto'),
    path('ingresoProductos/eliminar/<int:id>', views.eliminar_ingresoProducto, name='eliminar_ingresoProducto'),
    path('ingresoProductos/crear/<int:id>', views.crear_ingresoProducto, name='crear_ingresoProducto'),
    
    
    path('ingresoProductos_f/', views.ingresoProductos_f, name='ingresoProductos_f'),
    path('ingresoProductos_f/crear', views.crear_ingresoProducto_f, name='crear_ingresoProducto_f'),
    path('ingresoProductos_f/editar', views.editar_ingresoProducto_f, name='editar_ingresoProducto_f'),
    path('ingresoProductos_f/editar/<int:ingresoProducto_id>', views.editar_ingresoProducto_f, name='editar_ingresoProducto_f'),
    path('ingresoProductos_f/eliminar/<int:ingresoProducto_id>', views.eliminar_ingresoProducto_f, name='eliminar_ingresoProducto_f'),
    path('ingresoProductos_f/crear/<int:factura_id>', views.crear_ingresoProducto_f, name='crear_ingresoProducto_f'),
   


    path('stockProductos/', views.stockProductos, name='stockProductos'),
    path('actualizar_stock/', views.actualizar_stock, name='actualizar_stock'),
    path('informes/', views.informes, name='informes'),
    path('buscarProductos/', views.buscarProductos, name='buscarProductos'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('import_csv/', views.import_csv, name='import_csv'),
    path('sacar_del_inventario/', views.sacar_del_inventario, name='sacar_del_inventario'),

    
]