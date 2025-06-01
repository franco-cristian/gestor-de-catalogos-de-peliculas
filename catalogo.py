import os
import json
import shutil
from pelicula import Pelicula

class Catalogo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.directorio = f"catalogos/{nombre}"
        self.ruta_archivo = f"{self.directorio}/catalogo.json"
        self.portadas_dir = f"{self.directorio}/portadas"
        self._inicializar_directorio()
        self.peliculas = self._cargar_peliculas()
    
    def _inicializar_directorio(self):
        os.makedirs(self.directorio, exist_ok=True)
        os.makedirs(self.portadas_dir, exist_ok=True)
    
    def _cargar_peliculas(self):
        peliculas = []
        if os.path.exists(self.ruta_archivo):
            try:
                with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for pelicula_data in data:
                        peliculas.append(Pelicula.from_dict(pelicula_data))
            except Exception as e:
                print(f"Error cargando películas: {e}")
        return peliculas
    
    def agregar_pelicula(self, pelicula):
        # Copiar imagen de portada si existe
        if pelicula.ruta_portada and os.path.isfile(pelicula.ruta_portada):
            nombre_archivo = os.path.basename(pelicula.ruta_portada)
            destino = os.path.join(self.portadas_dir, nombre_archivo)
            shutil.copy(pelicula.ruta_portada, destino)
            pelicula.ruta_portada = destino
        
        self.peliculas.append(pelicula)
        self._guardar_peliculas()
    
    def eliminar_pelicula(self, titulo):
        for i, pelicula in enumerate(self.peliculas):
            if pelicula.titulo == titulo:
                # Eliminar imagen de portada si existe
                if pelicula.ruta_portada and os.path.exists(pelicula.ruta_portada):
                    os.remove(pelicula.ruta_portada)
                del self.peliculas[i]
                self._guardar_peliculas()
                return True
        return False
    
    def _guardar_peliculas(self):
        data = [p.to_dict() for p in self.peliculas]
        print(f"Guardando {len(data)} películas")  # Debug
        with open(self.ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def eliminar_catalogo(self):
        if os.path.exists(self.directorio):
            shutil.rmtree(self.directorio)
            return True
        return False
    
    def get_pelicula(self, titulo):
        print(f"Buscando: {titulo}")  # Debug
        for pelicula in self.peliculas:
            print(f"- {pelicula.titulo}")  # Debug
            if pelicula.titulo == titulo:
                return pelicula
        return None
    
    def listar_peliculas(self):
        return sorted(self.peliculas, key=lambda x: x.titulo)
    
    def _cargar_peliculas(self):
        peliculas = []
        if os.path.exists(self.ruta_archivo):
            try:
                with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for pelicula_data in data:
                        # Usamos la clase Pelicula importada
                        peliculas.append(Pelicula.from_dict(pelicula_data))
            except Exception as e:
                print(f"Error cargando películas: {str(e)}")  # Mensaje mejorado
        return peliculas