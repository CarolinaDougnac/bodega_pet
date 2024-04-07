import datetime, csv
from pyexpat.errors import messages
from random import randrange
from django.db.models import Sum, F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import StockProductos, Tiendas, Bodegas, EstadoProducto, EstadoFacturas, Proveedores, Marcas, Productos, Facturas, IngresoProductos, Import_csv 
from .forms import StockProductosForm
from .forms import *
from django.db.models import Q
from datetime import date
from django.shortcuts import render, get_object_or_404


# Create your views here.
#inicio informativo
def inicio(request):
    ingresos = IngresoProductos.objects.all()
    for ingreso in ingresos:
        ingreso.actualizar_estado()
        
    try:
        # Contar productos con estado "Vencido"
        suma_cantidad_vencido = IngresoProductos.objects.filter(estado__estado='Vencido').aggregate(total=Sum('cantidad_restante'))['total']

        # Contar productos con estado "por Vencer"
        suma_cantidad_por_vencer = IngresoProductos.objects.filter(estado__estado='por Vencer').aggregate(total=Sum('cantidad_restante'))['total']


        # Calcular la cantidad total de stock
        total_cantidad_stock = IngresoProductos.objects.filter(estado__estado='OK').aggregate(total=Sum('cantidad_restante'))['total']


        context = {
            'productos_vencidos': suma_cantidad_vencido,
            'productos_por_vencer': suma_cantidad_por_vencer,
            'total_cantidad_stock': total_cantidad_stock,
        }
        
        return render(request, 'paginas/inicio.html', context)

    except Exception as e:
        return render(request, 'paginas/inicio.html', {'error': str(e)})
    
    #return render(request, 'paginas/inicio.html')

#--------------------------------------------------------
# Graficos
def get_chart(_request):
    serie=[]
    counter=0
    while counter<12:
        serie.append(randrange(21, 30))
        counter+=1
    
    chart = {
        'tooltip': {
            'show': True,
            'trigger': "axis",
            'triggerOn': "mousemove|click"
        },
        'xAxis': [
            {
                'type': 'category',
                'data': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep','Oct','Nov','Dic']
            }
        ],
        'yAxis': [
            {
                'type': 'value',
                'min': 20,
                'name': 'Millones de Pesos',
            }
        ],
        'series': [
            {
                'data': serie,
                'type': 'bar',
                'showBackground': 'true',
                
            }
        ],
    }
    return JsonResponse(chart)
#--------------------------------------------------------
# Estadisticas de los grafico Torta
def obtener_estadisticas(request):
    try:
        # Contar productos con estado "Vencido"
        suma_cantidad_vencido = IngresoProductos.objects.filter(estado__estado='Vencido').aggregate(total=Sum('cantidad_restante'))['total']

        # Contar productos con estado "por Vencer"
        suma_cantidad_por_vencer = IngresoProductos.objects.filter(estado__estado='por Vencer').aggregate(total=Sum('cantidad_restante'))['total']


        # Calcular la cantidad total de stock
        total_cantidad_stock = IngresoProductos.objects.filter(estado__estado='OK').aggregate(total=Sum('cantidad_restante'))['total']


        data = {
            'productos_vencidos': suma_cantidad_vencido,
            'productos_por_vencer': suma_cantidad_por_vencer,
            'total_cantidad_stock': total_cantidad_stock,
        }

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'error': str(e)})

#--------------------------------------------------------
def nosotros(request):
    return render(request, 'paginas/nosotros.html')
#--------------------------------------------------------
#table proveedores
def proveedores(request):
    proveedores = Proveedores.objects.all()
    return render(request, 'proveedores/index.html', {'proveedores': proveedores})

def crear_proveedor(request):
    formulario = ProveedoresForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('proveedores')
    return render(request, 'proveedores/crear.html', {'formulario': formulario})

def editar_proveedor(request, id):
    proveedores = Proveedores.objects.get(id=id)
    formulario = ProveedoresForm(request.POST or None, instance=proveedores)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('proveedores')
    return render(request, 'proveedores/editar.html', {'formulario': formulario})

def eliminar_proveedor(request, id):
    proveedores = Proveedores.objects.get(id=id)
    proveedores.delete()
    return redirect('proveedores')

#--------------------------------------------------------
#table bodegas
def bodegas(request):
    bodegas = Bodegas.objects.all()
    return render(request, 'bodegas/index.html', {'bodegas': bodegas})

def crear_bodega(request):
    formulario = BodegaForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('bodegas')
    return render(request, 'bodegas/crear.html', {'formulario': formulario})

def editar_bodega(request, id):
    bodega = Bodegas.objects.get(id=id)
    formulario = BodegaForm(request.POST or None, instance=bodega)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('bodegas')
    return render(request, 'bodegas/editar.html', {'formulario': formulario})

def eliminar_bodega(request, id):
    bodega = Bodegas.objects.get(id=id)
    bodega.delete()
    return redirect('bodegas')
      
#--------------------------------------------------------
#tabla tiendas
def tiendas(request):
    tiendas = Tiendas.objects.all()
    return render(request, 'tiendas/index.html', {'tiendas': tiendas})

def crear_tienda(request):
    formulario = TiendaForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('tiendas')
    return render(request, 'tiendas/crear.html', {'formulario': formulario})

def editar_tienda(request, id):
    tienda = Tiendas.objects.get(id=id)
    formulario = TiendaForm(request.POST or None, instance=tienda)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('tiendas')
    return render(request, 'tiendas/editar.html', {'formulario': formulario})

def eliminar_tienda(request, id):
    tienda = Tiendas.objects.get(id=id)
    tienda.delete()
    return redirect('tiendas')

#--------------------------------------------------------
#tabla estado productos
def estadoProductos(request):
    estadoProductos = EstadoProducto.objects.all()
    return render(request, 'estadoProductos/index.html', {'estadoProductos': estadoProductos})

def crear_estadoProducto(request):
    formulario = EstadoProductoForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('estadoProductos')
    return render(request, 'estadoProductos/crear.html', {'formulario': formulario})

def editar_estadoProducto(request, id):
    estadoProductos = EstadoProducto.objects.get(id=id)
    formulario = EstadoProductoForm(request.POST or None, instance=estadoProductos)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('estadoProductos')
    return render(request, 'estadoProductos/editar.html', {'formulario': formulario})

def eliminar_estadoProducto(request, id):
    estadoProductos = EstadoProducto.objects.get(id=id)
    estadoProductos.delete()
    return redirect('estadoProductos')

#--------------------------------------------------------
#tabla estado facturas
def estadoFacturas(request):
    estadoFacturas = EstadoFacturas.objects.all()
    return render(request, 'estadoFacturas/index.html', {'estadoFacturas': estadoFacturas})

def crear_estadoFactura(request):
    formulario = EstadoFacturasForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('estadoFacturas')
    return render(request, 'estadoFacturas/crear.html', {'formulario': formulario})

def editar_estadoFactura(request, id):
    estadoFacturas = EstadoFacturas.objects.get(id=id)
    formulario = EstadoFacturasForm(request.POST or None, instance=estadoFacturas)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('estadoFacturas')
    return render(request, 'estadoFacturas/editar.html', {'formulario': formulario})

def eliminar_estadoFactura(request, id):
    estadoFacturas = EstadoFacturas.objects.get(id=id)
    estadoFacturas.delete()
    return redirect('estadoFacturas')

#-------------------------------------------------------- 
#tabla marcas
def marcas(request):
    marcas = Marcas.objects.all()
    return render(request, 'marcas/index.html', {'marcas': marcas})

def crear_marca(request):
    formulario = MarcasForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('marcas')
    return render(request, 'marcas/crear.html', {'formulario': formulario})

def editar_marca(request, id):
    marcas = Marcas.objects.get(id=id)
    formulario = MarcasForm(request.POST or None, instance=marcas)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('marcas')
    return render(request, 'marcas/editar.html', {'formulario': formulario})


def eliminar_marca(request, id):
    marcas = Marcas.objects.get(id=id)
    marcas.delete()
    return redirect('marcas')


#--------------------------------------------------------
#tabla productos
def productos(request):
    productos = Productos.objects.all()
    return render(request, 'productos/index.html', {'productos': productos})

def crear_producto(request):
    formulario = ProductosForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('productos')
    return render(request, 'productos/crear.html', {'formulario': formulario})

def editar_producto(request, id):
    productos = Productos.objects.get(id=id)
    formulario = ProductosForm(request.POST or None, instance=productos)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('productos')
    return render(request, 'productos/editar.html', {'formulario': formulario})

def eliminar_producto(request, id):
    productos = Productos.objects.get(id=id)
    productos.delete()
    return redirect('productos')

#--------------------------------------------------------
#tabla Facturas
def facturas(request):
    #obtener el estado
    estado_pendiente = EstadoFacturas.objects.get(estado='Pendiente')
    estado_ingresado = EstadoFacturas.objects.get(estado='Ingresada')
    
    # filtrar y ordenar las tablas
    facturas_pendientes = Facturas.objects.filter(estado=estado_pendiente).order_by('-fecha_recepcion')
    facturas_ingresadas = Facturas.objects.filter(estado=estado_ingresado).order_by('-fecha_recepcion')
    
    return render(request, 'facturas/index.html', {
        'facturas_pendientes': facturas_pendientes,
        'facturas_ingresadas': facturas_ingresadas,
        })

def cambiar_estado_factura(request, factura_id):
    factura = Facturas.objects.get(id=factura_id)
    
    # Obtener las instancias de EstadoFacturas correspondientes a los estados 'Pendiente' e 'Ingresada'
    estado_pendiente = EstadoFacturas.objects.get(estado='Pendiente')
    estado_ingresada = EstadoFacturas.objects.get(estado='Ingresada')
    
    # Verificar el estado actual de la factura y cambiarlo al estado opuesto
    if factura.estado == estado_pendiente:
        # Si la factura está pendiente, cambia su estado a ingresada
        factura.estado = estado_ingresada
    elif factura.estado == estado_ingresada:
        # Si la factura está ingresada, cambia su estado a pendiente
        factura.estado = estado_pendiente
    
    factura.save()
    
    # Redireccionar de vuelta a la página de facturas
    return redirect('facturas')

def crear_factura(request):
    formulario = FacturasForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('facturas')
    return render(request, 'facturas/crear.html', {'formulario': formulario})

def editar_factura(request, id):
    facturas = Facturas.objects.get(id=id)
    formulario = FacturasForm(request.POST or None, instance=facturas)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('facturas')
    return render(request, 'facturas/editar.html', {'formulario': formulario})
    #return render(request, 'facturas/edicionModal.html', {'formulario': formulario})

def eliminar_factura(request, id):
    facturas = Facturas.objects.get(id=id)
    facturas.delete()
    return redirect('facturas') 



#--------------------------------------------------------
#tabla ingreso productos
def ingresoProductos(request):
    ingresoProductos = IngresoProductos.objects.all()
    return render(request, 'ingresoProductos/index.html', {'ingresoProductos': ingresoProductos})

def crear_ingresoProducto(request):
    formulario = IngresoProductosForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('ingresoProductos')
    return render(request, 'ingresoProductos/crear.html', {'formulario': formulario})

def editar_ingresoProducto(request, id):
    ingresoProductos = IngresoProductos.objects.get(id=id)
    formulario = IngresoProductosForm(request.POST or None, instance=ingresoProductos)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('ingresoProductos')
    return render(request, 'ingresoProductos/editar.html', {'formulario': formulario})

def eliminar_ingresoProducto(request, id):
    ingresoProductos = IngresoProductos.objects.get(id=id)
    ingresoProductos.delete()
    return redirect('ingresoProductos')

#--------------------------------------------------------
#ingreso Productos_f desde la factura

#todos los productos ingresados al sistema
def ingresoProductos_f(request):
    ingresoProductos = IngresoProductos.objects.all()
    return render(request, 'ingresoProductos_f/index.html', {'ingresoProductos': ingresoProductos})

def crear_ingresoProducto_f(request, factura_id):
    # Obtener el código de barras del formulario
    query = request.GET.get('q', '')
    
    error_message = None

    # Variable para almacenar el producto encontrado
    productoss = None

    # Buscar productos por el código de barras ingresado
    if query:
        try:
            productoss = Productos.objects.get(codigo_barras=query)
        except Productos.DoesNotExist:
            # Si no se encuentra el producto, mostrar un mensaje de error
            productoss = None
            error_message = 'Producto no encontrado'
    else:
        error_message = None  

    # Obtener la factura correspondiente al ID proporcionado
    factura = get_object_or_404(Facturas, id=factura_id)

    # Obtener el folio de la factura
    folio = factura.folio

    # Obtener todos los ingresos de productos
    ingresoProductos = IngresoProductos.objects.all()
    
    # Crear el formulario de ingreso de productos con datos iniciales
    formulario = IngresoProductosForm(request.POST or None, initial={'factura': factura_id, 'folio': folio})
    
    # Guardar el formulario si es válido
    if formulario.is_valid():
        formulario.save()
    
    # Renderizar la plantilla con los datos necesarios
    return render(request, 'ingresoProductos_f/crear.html', {
        'formulario': formulario,
        'folio': folio,
        'ingresoProductos': ingresoProductos,
        'id_factura': factura_id,
        'productoss': productoss,
        'error_message': error_message,
    })

def crear_ingresoProducto_f_old(request, id):
# fucion para buscar productos
    query = request.GET.get('q', '')
    if query:
      #  productoss = Productos.objects.filter(codigo_barras=query)
      productoss = Productos.objects.get(codigo_barras=query)
      #print(productoss.id)  # Esto imprimirá el ID del producto
      #print(productoss.nombre)  # Esto imprimirá el nombre del producto
    else:
        productoss = []  
    # fin de la funcion para buscar productos

    id_factura = id
    facturas_f = Facturas.objects.get(id=id_factura)
    folio = facturas_f.folio

    ingresoProductos = IngresoProductos.objects.all()
    
    formulario = IngresoProductosForm(request.POST or None, initial={'factura': id_factura, 'folio': folio})
    
    if formulario.is_valid():
        formulario.save()
    
    return render(request, 'ingresoProductos_f/crear.html', {
        'formulario': formulario, 
        'folio': folio, 
        'ingresoProductos': ingresoProductos, 
        'id_factura': id_factura, 
        'productoss': productoss})


def editar_ingresoProducto_f(request, ingresoProducto_id):
    # Obtener el objeto de IngresoProductos con el ID proporcionado
    ingresoProducto = get_object_or_404(IngresoProductos, id=ingresoProducto_id)
  
    id=ingresoProducto_id
    ingresoProductos = IngresoProductos.objects.get(id=id)
    factura_id = ingresoProductos.factura.id
    formulario = IngresoProductosForm(request.POST or None, instance=ingresoProductos)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('crear_ingresoProducto_f', factura_id=factura_id)
    return render(request, 'ingresoProductos_f/editar.html', {'formulario': formulario, 'ingresoProducto': ingresoProductos})



def eliminar_ingresoProducto_f(request, ingresoProducto_id):
    # Obtener el objeto de IngresoProductos con el ID proporcionado
    ingresoProducto = get_object_or_404(IngresoProductos, id=ingresoProducto_id)
    
    # Guardar el ID de la factura antes de eliminar el ingreso del producto
    factura_id = ingresoProducto.factura.id
    
    # Eliminar el ingreso del producto
    ingresoProducto.delete()    
    
    # Redirigir a la vista crear_ingresoProducto_f con el ID de la factura
    return redirect('crear_ingresoProducto_f', factura_id=factura_id)

    
#---------------------------------------------- 
#generacion de informes

def informes(request):
    # Actualizar el estado de todos los ingresos
    ingresos = IngresoProductos.objects.all()
    for ingreso in ingresos:
        ingreso.actualizar_estado()
    
      # Obtener los estados "OK", "por vencer" y "vencido"
    estado_ok = EstadoProducto.objects.get(estado='OK')
    estado_por_vencer = EstadoProducto.objects.get(estado='por vencer')
    estado_vencido = EstadoProducto.objects.get(estado='vencido')

    # Filtrar los ingresos con estado "Vencido" o "Por vencer" y fecha de vencimiento menor o igual a la fecha actual
    ingresos_por_vencer = IngresoProductos.objects.filter(estado__in=[estado_por_vencer]).exclude(cantidad_restante=0).order_by('fecha_vencimiento')
    ingresos_vencidos = IngresoProductos.objects.filter(estado__in=[estado_vencido]).exclude(cantidad_restante=0).order_by('fecha_vencimiento')
    ingresos_ok = IngresoProductos.objects.filter(estado__in=[estado_ok]).order_by('fecha_vencimiento')
    
    return render(request, 'informes/index.html', {
        'ingresos_por_vencer': ingresos_por_vencer,
        'ingresos_vencidos': ingresos_vencidos,
        'ingresos_ok': ingresos_ok,
    })
    
#--------------------------------------------------------
#sacar del inventario
def sacar_del_inventario(request):
    if request.method == 'GET':  # Cambiado a GET ya que estás pasando los datos por la URL
        producto_id = request.GET.get('producto_id')
        #print("producto_id: ", producto_id)
        
        ingreso_id = request.GET.get('ingreso_id')
        #print("ingreso_id: ", ingreso_id)
        
        ingreso = IngresoProductos.objects.get(id=ingreso_id)
        #print("ingreso: ", ingreso)
        
        cantidad = ingreso.cantidad_restante
        #print("cantidad: ", cantidad)
        
        producto = Productos.objects.get(id=producto_id)
        #print("producto: ", producto)
        
        fecha = date.today()
        #print(fecha)
        
        salida = SalidaProductos.objects.create(producto=producto, cantidad=cantidad, fecha=fecha, motivo="vencido")
        
        try:
            stock_producto = StockProductos.objects.get(producto=producto)
        except StockProductos.DoesNotExist:
            pass
        else:
            stock_producto.actualizar_stock()
            
    return redirect('informes')
  
#--------------------------------------------------------
#tabla productos
def buscarProductos(request):
    query = request.GET.get('q', '')
    if query:
        productoss = Productos.objects.filter(codigo_barras=query)
    else:
        productoss = []
    
    print(productoss)
    return render(request, 'buscarProductos/index.html', {'productoss': productoss, 'query': query})


#--------------------------------------------------------
# exportar a csv
def export_csv(request):
    
    # build response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stock.csv"'
    
    # create a csv writer
    writer = csv.writer(response)
    # write header (cabecera)
    writer.writerow(['codido_barra', 'producto', 'cantidad', 'precio'])
        
    
    # write data (datos)
    for obj in StockProductos.objects.all().values_list('producto__codigo_barras', 'producto__nombre', 'cantidad', 'precio'):
        writer.writerow(obj) 
    response['Content-Disposition'] = 'attachment; filename="stock.csv"'
    
    return response
    
#--------------------------------------------------------
# import a csv
def import_csv(request):
    import_csvs = Import_csv.objects.all().order_by('-fecha')
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Este no es un archivo csv')
        else:
            file_data = csv_file.read().decode('UTF-8')
            lines = file_data.splitlines()
            for line in lines:
                fields = line.split(',')
                if len(fields) >= 1:
                    data_dict = {}
                    data_dict["codigo_barras"] = fields[0]
                    data_dict["nombre"] = fields[1]
                    data_dict["cantidad"] = fields[2]
                    data_dict["fecha"] = fields[3]
                    try:
                        form = Import_csvForm(data_dict)
                        if form.is_valid():
                            form.save()
                        else:
                            print(form.errors.as_json())
                    except Exception as ex:
                        print(repr(ex))
        return redirect('import_csv')
    return render(request, 'import_csv/index.html', {'import_csvs': import_csvs})

#--------------------------------------------------------
#tabla estado productos

def actualizar_stock(request):

    ingresos = IngresoProductos.objects.all()
    contador=0 
    
    
    for ingreso in ingresos:
        ingreso.actualizar_estado()
    
    if request.method == 'POST':
        productos = StockProductos.objects.all()
        progreso = 0  # Inicializa el progreso
        
        for stock in productos:
            contador += 1
            progreso = stock.actualizar_stock()  # Actualiza el stock y obtiene el progreso
            print(contador)
    
    stock_productos = StockProductos.objects.all()  # Obtener todos los productos de stock
    return render(request, 'stockProductos/index.html', {'stockProductos': stock_productos})




#def stockProductos(request):
#    stock = StockProductos.objects.all()
#    return render(request, 'stockProductos/index.html', {'stockProductos': stock})

def stockProductos(request):
    # Obtener todos los productos
    productos = StockProductos.objects.all()
    # Contar el número de productos
    num_productos = productos.count()

    if request.method == 'POST':
        # Procesar el formulario si se envía
        form = StockProductosForm(request.POST)
        
        if form.is_valid():
                
            form.save()
            # Actualizar la lista de productos después de editar
            productos = StockProductos.objects.all()

            # Renderizar la plantilla con la lista de productos y el progreso
            return render(request, 'stockProductos/index.html', {'productos': productos, 'form': form})

    else:
        # Mostrar el formulario si no se envía
        form = StockProductosForm()

    return render(request, 'stockProductos/index.html', {'productos': productos, 'form': form})




