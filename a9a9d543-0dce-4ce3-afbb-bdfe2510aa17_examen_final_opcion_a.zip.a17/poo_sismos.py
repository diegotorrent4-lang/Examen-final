"""
Ejercicio 5 — Programación Orientada a Objetos
Examen Final — Programación 1 (F12) — Variante A: Sismos USGS

Instrucciones:
    Implementa todos los métodos marcados con  # TU CÓDIGO AQUÍ
    No modifiques los métodos ya implementados ni los __init__.
    Cuando termines, regresa al notebook y ejecuta el Ejercicio 5.
"""


class EventoSismico:
    """Representa un evento sísmico genérico registrado en algún lugar del mundo."""

    def __init__(self, lugar, fecha):
        self.lugar = lugar
        self.fecha = fecha

    def clasificar(self):
        """
        Clasifica el evento según su intensidad.
        Este método debe ser sobreescrito en la clase hija.

        Retorna:
            str: categoría del evento
        """
        pass

    def descripcion(self):
        """
        Retorna una descripción legible del evento.
        Este método debe ser sobreescrito en la clase hija.

        Retorna:
            str: descripción del evento
        """
        pass

    def __str__(self):
        return self.descripcion() or f"EventoSismico en {self.lugar}"

    def __repr__(self):
        return f"{self.__class__.__name__}(lugar={self.lugar!r}, fecha={self.fecha!r})"


class Sismo(EventoSismico):
    """
    Representa un sismo con sus atributos medidos.

    Atributos:
        lugar       (str)   : descripción del lugar (columna 'place' del DataFrame)
        fecha       (str)   : fecha y hora UTC del evento (columna 'time')
        magnitud    (float) : magnitud del sismo (columna 'mag')
        profundidad (float) : profundidad del foco en km (columna 'depth')
        tipo_escala (str)   : escala de magnitud usada (columna 'magType')
    """

    def __init__(self, lugar, fecha, magnitud, profundidad, tipo_escala="mww"):
        super().__init__(lugar, fecha)
        self.magnitud    = magnitud
        self.profundidad = profundidad
        self.tipo_escala = tipo_escala

    def clasificar(self):
        """
        Clasifica el sismo según su magnitud.

        Usa la misma escala que aplicaste en el Ejercicio 3:
            5.5 ≤ magnitud < 6.0  →  'Moderado-Fuerte'
            6.0 ≤ magnitud < 7.0  →  'Fuerte'
            7.0 ≤ magnitud < 8.0  →  'Mayor'
            magnitud ≥ 8.0        →  'Gran terremoto'

        Hint: usa if / elif / elif / else sobre self.magnitud

        Retorna:
            str: categoría del sismo
        """
        # TU CÓDIGO AQUÍ
        if 5.5 <= self.magnitud < 6.0:
            return 'Moderado-Fuerte'
        elif 6.0 <= self.magnitud < 7.0:
            return 'Fuerte'
        elif 7.0 <= self.magnitud < 8.0:
            return 'Mayor'
        elif self.magnitud >= 8.0:
            return 'Gran terremoto'
        else:
            return 'Menor o No Clasificado'

    def clasificar_profundidad(self):
        """
        Clasifica el sismo según la profundidad del foco.

        Escala vista en el enunciado del examen:
            profundidad < 70 km          →  'Superficial'
            70 ≤ profundidad < 300 km    →  'Intermedio'
            profundidad ≥ 300 km         →  'Profundo'

        Hint: usa if / elif / else sobre self.profundidad

        Retorna:
            str: tipo de sismo por profundidad
        """
        # TU CÓDIGO AQUÍ
        if self.profundidad < 70:
            return 'Superficial'
        elif 70 <= self.profundidad < 300:
            return 'Intermedio'
        else:
            return 'Profundo'

    def es_peligroso(self):
        """
        Determina si el sismo es potencialmente peligroso en superficie.

        Criterio: magnitud >= 7.0  Y  profundidad < 70 km
        (un sismo Mayor o Gran terremoto que además es superficial)

        Hint: combina dos condiciones con 'and'

        Retorna:
            bool: True si cumple ambos criterios, False en caso contrario
        """
        # TU CÓDIGO AQUÍ
        if self.magnitud >= 7.0 and self.profundidad < 70:
            return True
        else:
            return False

    def descripcion(self):
        """
        Retorna una cadena con el resumen del sismo.

        Formato esperado (usa los métodos clasificar y clasificar_profundidad):
            "Sismo mag=7.10 | Mayor | Superficial | Lugar: Tonga Region | Escala: mww"

        Hint: llama a self.clasificar() y self.clasificar_profundidad() dentro del f-string

        Retorna:
            str: descripción formateada del sismo
        """
        # TU CÓDIGO AQUÍ
        return f"Sismo mag={self.magnitud:.2f} | {self.clasificar()} | {self.clasificar_profundidad()} | Lugar: {self.lugar} | Escala: {self.tipo_escala}"


    def __str__(self):
        return self.descripcion()

    def __repr__(self):
        return (
            f"Sismo(lugar={self.lugar!r}, magnitud={self.magnitud}, "
            f"profundidad={self.profundidad}, tipo_escala={self.tipo_escala!r})"
        )


class CatalogoSismos:
    """
    Colección de objetos Sismo con métodos de consulta y resumen.

    Atributos:
        nombre  (str)  : nombre descriptivo del catálogo
        _sismos (list) : lista interna de objetos Sismo
    """

    def __init__(self, nombre="Catálogo de Sismos"):
        self.nombre  = nombre
        self._sismos = []

    def agregar(self, sismo):
        """Agrega un objeto Sismo al catálogo."""
        self._sismos.append(sismo)

    def __len__(self):
        """Retorna el total de sismos en el catálogo."""
        return len(self._sismos)

    def el_mas_intenso(self):
        """
        Encuentra el sismo con la mayor magnitud.

        Usa un ciclo for para iterar sobre self._sismos.
        Guarda el mayor encontrado en una variable auxiliar.
        Compara con sismo.magnitud en cada iteración.

        Retorna:
            Sismo : el objeto con la magnitud más alta
            None  : si el catálogo está vacío
        """
        if not self._sismos:
            return None
        # TU CÓDIGO AQUÍ
        max_sismo = self._sismos[0]

        for sismo in self._sismos:
            if sismo.magnitud > max_sismo.magnitud:
                max_sismo = sismo
        return max_sismo

    def filtrar_por_categoria(self, categoria):
        """
        Retorna una lista con todos los sismos de la categoría dada.

        Parámetro:
            categoria (str): 'Moderado-Fuerte', 'Fuerte', 'Mayor' o 'Gran terremoto'

        Hint: usa un ciclo for y llama a sismo.clasificar() en cada iteración.
              Agrega a una lista auxiliar los que coincidan.

        Retorna:
            list: lista de objetos Sismo filtrada (puede estar vacía)
        """
        # TU CÓDIGO AQUÍ
        sismos_filtrados = []
        for sismo in self._sismos:
            if sismo.clasificar() == categoria:
                sismos_filtrados.append(sismo)

        return sismos_filtrados

    def resumen(self):
        """
        Imprime un resumen del catálogo.

        Debe mostrar:
            1. Nombre del catálogo y total de sismos  (usa len(self))
            2. El sismo más intenso                   (usa el_mas_intenso())
            3. Cantidad de sismos en cada categoría   (usa filtrar_por_categoria())

        Hint: itera sobre las categorías con un for:
            categorias = ['Moderado-Fuerte', 'Fuerte', 'Mayor', 'Gran terremoto']
        """
        # TU CÓDIGO AQUÍ
        print(f"Catálogo: {self.nombre}")
        print(f"Total de sismos registrados: {len(self)}")
        print("-" * 40)

        sismo_max = self.el_mas_intenso()
        if sismo_max is not None:
            print(f"Sismo más intenso: {sismo_max.descripcion()}")
        else:
            print("Sismo más intenso: No hay sismos en el catálogo.")
        print("-" * 40)

        print("Cantidad de sismos por categoría:")
        categorias = ['Moderado-Fuerte', 'Fuerte', 'Mayor', 'Gran terremoto']
        for cat in categorias:
            sismos_en_categoria = self.filtrar_por_categoria(cat)
            conteo = len(sismos_en_categoria)
            print(f" - {cat}: {conteo}")
