from datetime import datetime

class Pelicula:
    def __init__(self, titulo, genero="", anio="", director="", sinopsis="", ruta_portada=""):
        self.__titulo = titulo  # Atributo privado
        self.genero = genero
        self.anio = anio
        self.director = director
        self.sinopsis = sinopsis
        self.ruta_portada = ruta_portada
        self.fecha_agregada = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    @property
    def titulo(self):
        return self.__titulo
    
    def to_dict(self):
        return {
            "titulo": self.titulo,
            "genero": self.genero,
            "anio": self.anio,
            "director": self.director,
            "sinopsis": self.sinopsis,
            "ruta_portada": self.ruta_portada,
            "fecha_agregada": self.fecha_agregada
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            titulo=data["titulo"],
            genero=data["genero"],
            anio=data["anio"],
            director=data["director"],
            sinopsis=data["sinopsis"],
            ruta_portada=data["ruta_portada"]
        )