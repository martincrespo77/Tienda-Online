from ComprasOnline import (
    Producto,
    ProductoRegulado,
    Usuario,
    TiendaVirtual,
    Pesado,
    Promocion,
    RecargoFijo,
    IVA,
)

# Fábricas ---------------------------------------------------------
def crear_mueble(nombre, precio_base, modificadores=[], taxfree=False):
    iva=IVA()
    iva.taxfree=taxfree
    mods = modificadores + [RecargoFijo(1000.0)]
    return Producto(nombre=nombre, precio_base=precio_base, iva=iva, modificadores=mods)

def crear_indumentaria(nombre, precio_base, modificadores=[], taxfree=False):
    iva = IVA(); 
    iva.taxfree = taxfree
    return Producto(nombre=nombre, precio_base=precio_base, iva=iva, modificadores=modificadores)

def crear_bebida_alcoholica(nombre, precio_base, modificadores=[], taxfree=False):
    iva = IVA(); 
    iva.taxfree = taxfree
    return ProductoRegulado(nombre=nombre, precio_base=precio_base, edad_minima=18, iva=iva, modificadores=modificadores)

# Requerimientos ---------------------------------------------------------
def punto_1_mueble_pesado_taxfree_promocion():
    print("=== Punto 1: Probar que un mueble pesado, tax-free y de promoción muestre etiqueta correcta. ===")
    mueble = crear_mueble(
        nombre="Mesa Premium", 
        precio_base=60000.0, 
        modificadores=[Pesado(), Promocion(30)],
        taxfree=True
    )
    print("Etiqueta:", mueble.etiqueta("Cliente Prueba"))

def punto_2_mueble_pesado_60000_30_descuento():
    print("\n=== Punto 2: Probar que un mueble pesado de $60.000 con 30% de descuento tenga recargos correctos. ===")
    mueble = crear_mueble(
        nombre="Escritorio Ejecutivo", 
        precio_base=60000.0, 
        modificadores=[Promocion(30), Pesado()]
    )
    cliente = Usuario(nombre="Cliente de Prueba", edad=30, dinero=1000.0)
    print("Etiqueta:", mueble.etiqueta(cliente.nombre))
    print("Precio base:", mueble.precio_base)
    print("Precio final:", mueble.precio_final(cliente))

def punto_3_usuario_bronce_mochila_5000():
    print("\n=== Punto 3: Probar que usuario Bronce con $5000 de saldo cuando compra una mochila suma 1000 puntos y queda con saldo $0. ===")
    u = Usuario(nombre="Juan", edad=25, dinero=5000.0, puntos=0)
    print("Saldo inicial:", u.dinero)
    mochila = crear_indumentaria(nombre="Mochila", precio_base=4132.23)
    u.agregar_producto(mochila)
    total_pagado = u.comprar()
    print("Total pagado:", total_pagado)
    print("Puntos ganados:", u.puntos)
    print("Saldo final:", u.dinero)
    print("Nivel:", u.nivel.nombre)

def punto_4_penalizacion_morosidad():
    print("\n=== Punto 4: Probar que el negocio aplique correctamente la penalización de morosidad. ===")
    u = Usuario(nombre="María", edad=30, dinero=-100.0, puntos=500)
    tienda = TiendaVirtual(usuarios=[u])
    print("Puntos antes de penalización:", u.puntos)
    tienda.penalizar_morosos()
    print("Puntos después de penalización:", u.puntos)

def punto_5_bronce_a_plata_5000_puntos():
    print("\n=== Punto 5: Probar que usuario Bronce con 1 punto pase a Plata al darle 5000 puntos. ===")
    u = Usuario(nombre="Carlos", edad=28, dinero=1000.0, puntos=1)
    print("Nivel inicial:", u.nivel.nombre)
    u.puntos = 5000
    u.actualizar_nivel()
    print("Nivel después de 5000 puntos:", u.nivel.nombre)

def punto_6_bronce_saldo_insuficiente():
    print("\n=== Punto 6: Probar que usuario Bronce con saldo de $4999 no puede comprar una mochila de $5000. ===")
    u = Usuario(nombre="Ana", edad=25, dinero=4999.0, puntos=0)
    mochila = crear_indumentaria(nombre="Mochila", precio_base=4132.23)  # ~5000 con IVA
    u.agregar_producto(mochila)
    try:
        u.comprar()
        print("ERROR: Debería haber fallado por saldo insuficiente")
    except Exception as e:
        print("Excepción esperada:", str(e))

def punto_7_menor_18_bebida_alcoholica():
    print("\n=== Punto 7: Probar que usuario menor de 18 años no puede comprar una botella de cerveza. ===")
    u = Usuario(nombre="Pedro", edad=17, dinero=1000.0, puntos=0)
    cerveza = crear_bebida_alcoholica(nombre="Cerveza", precio_base=100.0)
    try:
        u.agregar_producto(cerveza)
        print("ERROR: Debería haber fallado por edad")
    except Exception as e:
        print("Excepción esperada:", str(e))

def punto_8_usuario_extranjero_taxfree():
    print("\n=== Punto 8: Probar que un usuario extranjero puede aprovechar el beneficio tax-free. ===")
    u_nacional = Usuario(nombre="Nacional", edad=25, dinero=1000.0, extranjero=False)
    u_extranjero = Usuario(nombre="Extranjero", edad=25, dinero=1000.0, extranjero=True)
    producto_normal = crear_indumentaria(nombre="Camisa Normal", precio_base=100.0)
    producto_taxfree = crear_indumentaria(nombre="Camisa Tax-Free", precio_base=100.0, taxfree=True)
    print("Precio normal para nacional:", producto_normal.precio_final(u_nacional))
    print("Precio normal para extranjero:", producto_normal.precio_final(u_extranjero))
    print("Precio tax-free para nacional:", producto_taxfree.precio_final(u_nacional))
    print("Precio tax-free para extranjero:", producto_taxfree.precio_final(u_extranjero))

def punto_9_test_automatico_bronce_4900_a_plata():
    """Test automático: Usuario Bronce con 4900 pts compra $1000 y sube a Plata."""
    print("\n=== Punto 9: Test automático - Bronce 4900 a Plata ===")
    u = Usuario(nombre="Ana", edad=30, dinero=2000.0, puntos=4900)
    prod = crear_indumentaria(nombre="Remera", precio_base=826.45)  # 1000 con IVA
    u.agregar_producto(prod)
    total = u.comprar()
    print("Total pagado:", total)
    print("Puntos:", u.puntos)
    print("Nivel:", u.nivel.nombre)
    assert round(total, 2) == 1000.0
    assert u.puntos == 5000
    assert u.nivel.nombre == "Plata"
    print("✓ Test automático PASÓ")

def punto_10_test_automatico_bronce_dos_productos():
    """Test automático: Usuario Bronce no puede agregar dos productos al carrito."""
    print("\n=== Punto 10: Test automático - Bronce no puede dos productos ===")
    u = Usuario(nombre="Pepe", edad=20, dinero=10000.0, puntos=0)
    mochila = crear_indumentaria(nombre="Mochila", precio_base=5000.0)
    cartuchera = crear_indumentaria(nombre="Cartuchera", precio_base=1000.0)
    u.agregar_producto(mochila)
    try:
        u.agregar_producto(cartuchera)
        print("ERROR: Debería haber fallado por límite de carrito")
        assert False
    except Exception as e:
        print("Excepción esperada:", str(e))
        print("✓ Test automático PASÓ")

if __name__ == "__main__":
    punto_1_mueble_pesado_taxfree_promocion()
    punto_2_mueble_pesado_60000_30_descuento()
    punto_3_usuario_bronce_mochila_5000()
    punto_4_penalizacion_morosidad()
    punto_5_bronce_a_plata_5000_puntos()
    punto_6_bronce_saldo_insuficiente()
    punto_7_menor_18_bebida_alcoholica()
    punto_8_usuario_extranjero_taxfree()
    punto_9_test_automatico_bronce_4900_a_plata()
    punto_10_test_automatico_bronce_dos_productos()