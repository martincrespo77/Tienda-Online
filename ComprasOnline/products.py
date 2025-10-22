class Producto:
    def __init__(self, nombre, precio_base, iva, modificadores=[]):
        self.nombre = nombre
        self.precio_base = precio_base
        self.modificadores = [iva] + modificadores

    def puede_comprar(self, usuario):
        return True

    def precio_final(self, usuario):
        total = self.precio_base
        for m in reversed(self.modificadores):
            total = m.aplicar_precio(total, usuario)
        return total

    def etiqueta(self, nombre_cliente):
        fragmentos = []
        for m in self.modificadores:
            fragmentos.append(m.etiqueta_fragment())
        advertencias = " - " + ", ".join(fragmentos) if fragmentos else ""
        return f"Para {nombre_cliente}: {self.nombre}{advertencias}"

class ProductoRegulado(Producto):
    def __init__(self, nombre, precio_base, edad_minima, iva, modificadores=[]):
        self.edad_minima = edad_minima
        super().__init__(nombre=nombre, precio_base=precio_base, iva=iva, modificadores=modificadores)

    def puede_comprar(self, usuario):
        return usuario.edad >= self.edad_minima

# Modificadores ---------------------------------------------------------
class Modificador:
    def aplicar_precio(self, precio_actual, usuario):
        return precio_actual
    def etiqueta_fragment(self):
        return "" # No se muestra en la etiqueta

class RecargoFijo(Modificador):
    def __init__(self, recargo):
        self.recargo = recargo
    def aplicar_precio(self, precio_actual, _):
        return precio_actual + self.recargo

class IVA(Modificador):
    PORCENTAJE = 0.21
    taxfree = False
    def aplicar_precio(self, precio_actual, usuario):
        if self.taxfree and usuario.extranjero:
            return precio_actual
        else:
            return round(precio_actual * (1 + self.PORCENTAJE), 2)
    def etiqueta_fragment(self):
        if self.taxfree:
            return "Tax-Free"
        else:
            return ""

class Pesado(Modificador):
    def aplicar_precio(self, precio_actual, _):
        return precio_actual + 3000.0
    def etiqueta_fragment(self):
        return "PESADO"

class Promocion(Modificador):
    def __init__(self, descuento):
        self.descuento = descuento
    def etiqueta_fragment(self):
        return f"PROMO {int(self.descuento)}%"
    def aplicar_precio(self, precio_actual, _):
        return round(precio_actual * (1 - self.descuento / 100.0), 2)