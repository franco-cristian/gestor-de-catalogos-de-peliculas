import sys
import os
import shutil
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QListWidget, QFileDialog, QMessageBox, QStackedWidget, QSizePolicy,
                             QListWidgetItem, QTextEdit)
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt, QSize

from pelicula import Pelicula
from catalogo import Catalogo

class GestorCatalogoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Catálogos de Películas")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(800, 600)
        
        try:
            self.setWindowIcon(QIcon("icon.png"))
        except:
            pass
        
        os.makedirs("catalogos", exist_ok=True)
        
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        self.pagina_inicio = self.crear_pagina_inicio()
        self.pagina_menu = self.crear_pagina_menu()
        self.pagina_agregar = self.crear_pagina_agregar()
        self.pagina_listar = self.crear_pagina_listar()
        self.pagina_detalle = self.crear_pagina_detalle()
        
        self.central_widget.addWidget(self.pagina_inicio)
        self.central_widget.addWidget(self.pagina_menu)
        self.central_widget.addWidget(self.pagina_agregar)
        self.central_widget.addWidget(self.pagina_listar)
        self.central_widget.addWidget(self.pagina_detalle)
        
        self.catalogo_actual = None
        self.ruta_portada_temporal = ""
        
        self.central_widget.setCurrentIndex(0)
    
    def crear_pagina_inicio(self):
        pagina = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        titulo = QLabel("GESTOR DE CATÁLOGOS DE PELÍCULAS")
        titulo.setFont(QFont("Arial", 20, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        entrada_layout = QHBoxLayout()
        entrada_layout.setAlignment(Qt.AlignCenter)
        
        label = QLabel("Nombre del Catálogo:")
        label.setFont(QFont("Arial", 12))
        entrada_layout.addWidget(label)
        
        self.entrada_catalogo = QLineEdit()
        self.entrada_catalogo.setFont(QFont("Arial", 12))
        self.entrada_catalogo.setMinimumWidth(300)
        self.entrada_catalogo.setPlaceholderText("Ej: Favoritas, Terror, Comedia...")
        entrada_layout.addWidget(self.entrada_catalogo)
        
        layout.addLayout(entrada_layout)
        
        botones_layout = QHBoxLayout()
        botones_layout.setAlignment(Qt.AlignCenter)
        
        btn_crear = QPushButton("Crear/Abrir Catálogo")
        btn_crear.setFont(QFont("Arial", 12))
        btn_crear.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        btn_crear.clicked.connect(self.abrir_catalogo)
        btn_crear.setMinimumSize(200, 50)
        botones_layout.addWidget(btn_crear)
        
        layout.addLayout(botones_layout)
        
        self.lista_catalogos = QListWidget()
        self.lista_catalogos.setFont(QFont("Arial", 11))
        self.lista_catalogos.setMinimumHeight(150)
        self.lista_catalogos.itemDoubleClicked.connect(self.seleccionar_catalogo_existente)
        layout.addWidget(QLabel("Catálogos existentes:"))
        layout.addWidget(self.lista_catalogos)
        
        self.actualizar_lista_catalogos()
        
        pagina.setLayout(layout)
        return pagina
    
    def crear_pagina_menu(self):
        pagina = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        self.titulo_catalogo = QLabel()
        self.titulo_catalogo.setFont(QFont("Arial", 18, QFont.Bold))
        self.titulo_catalogo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.titulo_catalogo)
        
        self.estadisticas = QLabel()
        self.estadisticas.setFont(QFont("Arial", 10))
        self.estadisticas.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.estadisticas)
        
        btn_agregar = QPushButton("Agregar Película")
        btn_agregar.setFont(QFont("Arial", 12))
        btn_agregar.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        btn_agregar.clicked.connect(self.mostrar_agregar_pelicula)
        btn_agregar.setMinimumSize(250, 60)
        layout.addWidget(btn_agregar)
        
        btn_listar = QPushButton("Listar Películas")
        btn_listar.setFont(QFont("Arial", 12))
        btn_listar.setStyleSheet("background-color: #FF9800; color: white; padding: 10px;")
        btn_listar.clicked.connect(self.mostrar_lista_peliculas)
        btn_listar.setMinimumSize(250, 60)
        layout.addWidget(btn_listar)
        
        btn_eliminar = QPushButton("Eliminar Catálogo")
        btn_eliminar.setFont(QFont("Arial", 12))
        btn_eliminar.setStyleSheet("background-color: #F44336; color: white; padding: 10px;")
        btn_eliminar.clicked.connect(self.eliminar_catalogo)
        btn_eliminar.setMinimumSize(250, 60)
        layout.addWidget(btn_eliminar)
        
        btn_volver = QPushButton("Cambiar de Catálogo")
        btn_volver.setFont(QFont("Arial", 11))
        btn_volver.clicked.connect(self.volver_a_inicio)
        btn_volver.setMinimumSize(200, 40)
        layout.addWidget(btn_volver)
        
        pagina.setLayout(layout)
        return pagina
    
    def crear_pagina_agregar(self):
        pagina = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        titulo = QLabel("Agregar Nueva Película")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        campos = [
            ("Título:", "entrada_titulo"),
            ("Género:", "entrada_genero"),
            ("Año:", "entrada_anio"),
            ("Director:", "entrada_director")
        ]
        
        for etiqueta, nombre in campos:
            campo_layout = QHBoxLayout()
            label = QLabel(etiqueta)
            label.setFont(QFont("Arial", 11))
            campo_layout.addWidget(label)
            
            entrada = QLineEdit()
            entrada.setFont(QFont("Arial", 11))
            setattr(self, nombre, entrada)
            campo_layout.addWidget(entrada)
            
            layout.addLayout(campo_layout)
        
        layout.addWidget(QLabel("Sinopsis:"))
        self.entrada_sinopsis = QTextEdit()
        self.entrada_sinopsis.setFont(QFont("Arial", 11))
        self.entrada_sinopsis.setMaximumHeight(100)
        layout.addWidget(self.entrada_sinopsis)
        
        portada_layout = QHBoxLayout()
        self.etiqueta_portada = QLabel("Sin portada seleccionada")
        self.etiqueta_portada.setFont(QFont("Arial", 10))
        portada_layout.addWidget(self.etiqueta_portada)
        
        btn_portada = QPushButton("Seleccionar Portada")
        btn_portada.setFont(QFont("Arial", 10))
        btn_portada.clicked.connect(self.seleccionar_portada)
        portada_layout.addWidget(btn_portada)
        
        layout.addLayout(portada_layout)
        
        botones_layout = QHBoxLayout()
        
        btn_guardar = QPushButton("Guardar Película")
        btn_guardar.setFont(QFont("Arial", 11))
        btn_guardar.setStyleSheet("background-color: #4CAF50; color: white;")
        btn_guardar.clicked.connect(self.guardar_pelicula)
        botones_layout.addWidget(btn_guardar)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setFont(QFont("Arial", 11))
        btn_cancelar.setStyleSheet("background-color: #9E9E9E; color: white;")
        btn_cancelar.clicked.connect(self.volver_al_menu)
        botones_layout.addWidget(btn_cancelar)
        
        layout.addLayout(botones_layout)
        
        pagina.setLayout(layout)
        return pagina
    
    def crear_pagina_listar(self):
        pagina = QWidget()
        layout = QVBoxLayout()
        
        titulo = QLabel("Películas en el Catálogo")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        self.lista_peliculas = QListWidget()
        self.lista_peliculas.setFont(QFont("Arial", 12))
        self.lista_peliculas.itemDoubleClicked.connect(self.mostrar_detalle_pelicula)
        layout.addWidget(self.lista_peliculas)
        
        botones_layout = QHBoxLayout()
        
        btn_eliminar = QPushButton("Eliminar Seleccionada")
        btn_eliminar.setFont(QFont("Arial", 11))
        btn_eliminar.setStyleSheet("background-color: #F44336; color: white;")
        btn_eliminar.clicked.connect(self.eliminar_pelicula_seleccionada)
        botones_layout.addWidget(btn_eliminar)
        
        btn_volver = QPushButton("Volver al Menú")
        btn_volver.setFont(QFont("Arial", 11))
        btn_volver.setStyleSheet("background-color: #2196F3; color: white;")
        btn_volver.clicked.connect(self.volver_al_menu)
        botones_layout.addWidget(btn_volver)
        
        layout.addLayout(botones_layout)
        
        pagina.setLayout(layout)
        return pagina
    
    def crear_pagina_detalle(self):
        pagina = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.titulo_detalle = QLabel()
        self.titulo_detalle.setFont(QFont("Arial", 18, QFont.Bold))
        self.titulo_detalle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.titulo_detalle)
        
        contenedor = QHBoxLayout()
        
        self.portada_detalle = QLabel()
        self.portada_detalle.setAlignment(Qt.AlignCenter)
        self.portada_detalle.setMinimumSize(300, 400)
        self.portada_detalle.setStyleSheet("background-color: #F0F0F0; border: 1px solid #CCCCCC;")
        contenedor.addWidget(self.portada_detalle)
        
        info_layout = QVBoxLayout()
        
        campos = [
            ("Género:", "genero_detalle"),
            ("Año:", "anio_detalle"),
            ("Director:", "director_detalle"),
            ("Agregada:", "fecha_detalle")
        ]
        
        for etiqueta, nombre in campos:
            campo_layout = QHBoxLayout()
            label = QLabel(etiqueta)
            label.setFont(QFont("Arial", 11, QFont.Bold))
            campo_layout.addWidget(label)
            
            valor = QLabel()
            valor.setFont(QFont("Arial", 11))
            setattr(self, nombre, valor)
            campo_layout.addWidget(valor)
            
            info_layout.addLayout(campo_layout)
        
        info_layout.addWidget(QLabel("Sinopsis:"))
        self.sinopsis_detalle = QTextEdit()
        self.sinopsis_detalle.setFont(QFont("Arial", 11))
        self.sinopsis_detalle.setReadOnly(True)
        info_layout.addWidget(self.sinopsis_detalle)
        
        contenedor.addLayout(info_layout)
        layout.addLayout(contenedor)
        
        botones_layout = QHBoxLayout()
        
        btn_volver = QPushButton("Volver a la Lista")
        btn_volver.setFont(QFont("Arial", 11))
        btn_volver.setStyleSheet("background-color: #2196F3; color: white;")
        btn_volver.clicked.connect(self.volver_a_lista)
        botones_layout.addWidget(btn_volver)
        
        layout.addLayout(botones_layout)
        
        pagina.setLayout(layout)
        return pagina
    
    def abrir_catalogo(self):
        nombre = self.entrada_catalogo.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "Debe ingresar un nombre para el catálogo")
            return
        
        self.catalogo_actual = Catalogo(nombre)
        self.titulo_catalogo.setText(f"Catálogo: {nombre}")
        self.actualizar_estadisticas()
        self.central_widget.setCurrentIndex(1)
    
    def seleccionar_catalogo_existente(self, item):
        self.entrada_catalogo.setText(item.text())
        self.abrir_catalogo()
    
    def actualizar_lista_catalogos(self):
        self.lista_catalogos.clear()
        if os.path.exists("catalogos"):
            for nombre in os.listdir("catalogos"):
                if os.path.isdir(os.path.join("catalogos", nombre)):
                    self.lista_catalogos.addItem(nombre)
    
    def actualizar_estadisticas(self):
        count = len(self.catalogo_actual.peliculas)
        self.estadisticas.setText(f"Total de películas: {count}")
    
    def mostrar_agregar_pelicula(self):
        self.entrada_titulo.clear()
        self.entrada_genero.clear()
        self.entrada_anio.clear()
        self.entrada_director.clear()
        self.entrada_sinopsis.clear()
        self.etiqueta_portada.setText("Sin portada seleccionada")
        self.ruta_portada_temporal = ""
        
        self.central_widget.setCurrentIndex(2)
    
    def seleccionar_portada(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self, 
            "Seleccionar Imagen de Portada", 
            "", 
            "Archivos de Imagen (*.png *.jpg *.jpeg)"
        )
        if ruta:
            self.ruta_portada_temporal = ruta
            nombre_archivo = os.path.basename(ruta)
            self.etiqueta_portada.setText(f"Portada: {nombre_archivo}")
    
    def guardar_pelicula(self):
        titulo = self.entrada_titulo.text().strip()
        if not titulo:
            QMessageBox.warning(self, "Error", "El título es obligatorio")
            return
        
        if self.catalogo_actual.get_pelicula(titulo):
            QMessageBox.warning(self, "Error", f"Ya existe una película con el título '{titulo}'")
            return
        
        nueva_pelicula = Pelicula(
            titulo=titulo,
            genero=self.entrada_genero.text().strip(),
            anio=self.entrada_anio.text().strip(),
            director=self.entrada_director.text().strip(),
            sinopsis=self.entrada_sinopsis.toPlainText().strip(),
            ruta_portada=self.ruta_portada_temporal
        )
        
        self.catalogo_actual.agregar_pelicula(nueva_pelicula)
        self.actualizar_estadisticas()
        QMessageBox.information(self, "Éxito", f"Película '{titulo}' agregada al catálogo")
        self.volver_al_menu()
    
    def mostrar_lista_peliculas(self):
        self.lista_peliculas.clear()
        peliculas = self.catalogo_actual.listar_peliculas()
        
        if not peliculas:
            self.lista_peliculas.addItem("El catálogo está vacío")
            return
        
        for pelicula in peliculas:
            item = QListWidgetItem(pelicula.titulo)
            item.setData(Qt.UserRole, pelicula.titulo)
            self.lista_peliculas.addItem(item)
        
        self.central_widget.setCurrentIndex(3)
    
    def eliminar_pelicula_seleccionada(self):
        item = self.lista_peliculas.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "Seleccione una película para eliminar")
            return
        
        titulo = item.data(Qt.UserRole)
        if not titulo:
            return
        
        respuesta = QMessageBox.question(
            self, 
            "Confirmar Eliminación", 
            f"¿Está seguro que desea eliminar la película '{titulo}'?", 
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            if self.catalogo_actual.eliminar_pelicula(titulo):
                self.mostrar_lista_peliculas()
                self.actualizar_estadisticas()
                QMessageBox.information(self, "Éxito", f"Película '{titulo}' eliminada")
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar la película")
    
    def mostrar_detalle_pelicula(self, item):
        titulo = item.data(Qt.UserRole)
        pelicula = self.catalogo_actual.get_pelicula(titulo)
        
        if not pelicula:
            return
        
        self.titulo_detalle.setText(pelicula.titulo)
        self.genero_detalle.setText(pelicula.genero or "No especificado")
        self.anio_detalle.setText(pelicula.anio or "No especificado")
        self.director_detalle.setText(pelicula.director or "No especificado")
        self.fecha_detalle.setText(pelicula.fecha_agregada)
        self.sinopsis_detalle.setText(pelicula.sinopsis or "Sin sinopsis disponible")
        
        if pelicula.ruta_portada and os.path.exists(pelicula.ruta_portada):
            pixmap = QPixmap(pelicula.ruta_portada)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(300, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.portada_detalle.setPixmap(pixmap)
                return
        
        self.portada_detalle.setText("Portada no disponible")
        
        self.central_widget.setCurrentIndex(4)
    
    def eliminar_catalogo(self):
        respuesta = QMessageBox.question(
            self, 
            "Confirmar Eliminación", 
            f"¿Está seguro que desea eliminar el catálogo '{self.catalogo_actual.nombre}' y todas sus películas?", 
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            if self.catalogo_actual.eliminar_catalogo():
                QMessageBox.information(self, "Éxito", "Catálogo eliminado")
                self.volver_a_inicio()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el catálogo")
    
    def volver_a_inicio(self):
        self.central_widget.setCurrentIndex(0)
        self.actualizar_lista_catalogos()
    
    def volver_al_menu(self):
        self.central_widget.setCurrentIndex(1)
    
    def volver_a_lista(self):
        self.central_widget.setCurrentIndex(3)