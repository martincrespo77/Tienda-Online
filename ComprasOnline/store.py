class TiendaVirtual:
    def __init__(self, usuarios=[], productos=[]):
        self.usuarios = usuarios
        self.productos = usuarios

    def penalizar_morosos(self):
        for u in self.usuarios:
            if u.dinero < 0:
                u.puntos = max(0, u.puntos - 100)
                u.actualizar_nivel()

    def actualizar_niveles_usuarios(self):
        for u in self.usuarios:
            u.actualizar_nivel()

    def gestionar_venta(self, usuario):
        # Remueve productos que el usuario no puede comprar (por ejemplo, bebidas alcohólicas a menores)
        restantes = []
        devueltos = []
        for p in usuario.carrito:
            if not p.puede_comprar(usuario):
                devueltos.append(p)
            else:
                restantes.append(p)
        if devueltos:
            self.productos.extend(devueltos)
            usuario.carrito = restantes
        return usuario.comprar()