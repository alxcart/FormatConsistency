import os.path
import sys 
#from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo, QFile
#from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem, QAction, QFileDialog, QApplication, QTableWidget
from qgis.core import QgsProject, QgsVectorFileWriter,QgsCoordinateReferenceSystem, QgsVectorLayer

from datetime import datetime
# from .FormatConsistency_dialog import FormatConsistencyDialog
# from .FormatConsistency import FormatConsistency

# classe_camadas():
class LayerInfo: 
    ano_atual = int(datetime.strftime(datetime.now(), '%Y'))
    def __init__(self, layer):
        self.name = str(layer.name())
        self.crs = str(layer.crs().description())
        try:
            self.encoding = str(layer.dataProvider().encoding())
            self.count = float(layer.featureCount())
            self.formato = str(layer.storageType())
        except AttributeError:
            self.encoding = 'NA'
            self.count = 'NA'
            self.formato = 'Raster'
        self.isValid = layer.isValid()

    def adicionaName(self, object):
        self.name.append(self.object)
    def adicionaCRS(self, object):
        self.crs.append(self.object)
    def adicionaCount(self, object):
        self.count.append(self.object)
    def adicionaFormato(self, object):
        self.formato.append(self.object)
    def adicionaIs_Valid(self, object):
        self.is_Valid.append(self.object)

def cria_lista(lista_layers_txt, path_project):
    lista = list(range(len(lista_layers_txt)))
    for id, i in enumerate(lista_layers_txt):
        camada = QgsVectorLayer(path_project + i  + ".shp",  i, "ogr")
        lista[id] = camada
    return lista

# Iterate over all loaded layers
def list_layers(lista_layers):
    layer_list = [] #vazia
    layer_count = 0
    
    # Create layer list
    layers = QgsProject.instance().mapLayers().values()
    if len(layers)==0:
        layers = cria_lista(lista_layers)
    if len(layers)>0:
        for layer in layers:
            layer_count += 1
            layer_list.append(LayerInfo(layer))
    return layer_list 


def mostrar_tabela(self, layers):
    camadas_info = list_layers(layers)
    # Generate data table
    self.dlg1.tableWidget.clear()
    self.dlg1.tableWidget.setRowCount(len(layers))
    self.dlg1.tableWidget.setColumnCount(6)
    self.dlg1.tableWidget.setColumnWidth(0, 200)
    self.dlg1.tableWidget.horizontalHeader().setStretchLastSection(True)

    self.dlg1.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Layer"))
    self.dlg1.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("SRC"))
    self.dlg1.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Encoding"))
    self.dlg1.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Count"))
    self.dlg1.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem("Format"))
    self.dlg1.tableWidget.setHorizontalHeaderItem(5, QTableWidgetItem("isValid"))

    #for layer in camadas_info:
    for id, layer in enumerate(camadas_info):            
        self.dlg1.tableWidget.setItem(id, 0, QTableWidgetItem(layer.name))
        self.dlg1.tableWidget.setItem(id, 1, QTableWidgetItem(layer.crs))
        #try:
        self.dlg1.tableWidget.setItem(id, 2, QTableWidgetItem(layer.encoding))
        self.dlg1.tableWidget.setItem(id, 3, QTableWidgetItem(layer.count))
        self.dlg1.tableWidget.setItem(id, 4, QTableWidgetItem(str(layer.formato)))
        #except AttributeError:
        #    pass
        self.dlg1.tableWidget.setItem(id, 5, QTableWidgetItem(str(layer.isValid)))

    self.dlg1.tableWidget.move(0, 0)

