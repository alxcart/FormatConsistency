# -*- coding: utf-8 -*-
#/***************************************************************************
# Format consistency
#
# This plugin elaborates the area-oriented sampling plan, 
# it is based on the ISO 2859 series of standards. 
#							 -------------------
#		begin				: 2019-08-03
#		git sha				: $Format:%H$
#		copyright			: (C) 2019 by Alex Santos
#		email				: alxcart@gmail.com
# ***************************************************************************/
#
#/***************************************************************************
# *																		 *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or	 *
# *   (at your option) any later version.								   *
# *																		 *
# ***************************************************************************/
import os.path
import sys 
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo, QFile
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog, QTableWidgetItem, QApplication
from qgis.core import QgsProject, QgsVectorFileWriter,QgsCoordinateReferenceSystem, QgsVectorLayer
from qgis.core import QgsCoordinateReferenceSystem as Hoh

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .FormatConsistency_dialog import FormatConsistencyDialog

class FormatConsistency:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # Initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # Initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'FormatConsistency_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg1 = FormatConsistencyDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Format consistency') ###
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'FormatConsistency')
        self.toolbar.setObjectName(u'FormatConsistency')

        ###Select output
        #self.dlg1.lineEdit.clear()
        #self.dlg1.toolButton.clicked.connect(self.select_output)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('FormatConsistency', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        # icon_path = ':/plugins/FormatConsistency/icon.ico'
        # self.add_action(
        #     icon_path,
        #     text=self.tr(u'Format consistency'),
        #     callback=self.check,
        #     #callback=self.run,
        #     parent=self.iface.mainWindow())
        
        # will be set False in run() define check convert
        #self.first_start = True

        self.add_action(
            ':/plugins/FormatConsistency/icon.ico',
            text=QApplication.translate('Format consistency', u'Format consistency'),
            callback=self.check,
            parent=self.iface.mainWindow(),
            status_tip=QApplication.translate('Format consistency', 'Format consistency'))

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Format consistency'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    # Select output file
    # def select_output(self):
    #     output_dir = QFileDialog.getExistingDirectory(self.dlg1, "Select folder", "")
    #     #self.dlg1.lineEdit.setText(output_dir)

    # def run(self):
    #     """Run method that performs all the real work"""
    #     # show the dialog
    #     self.dlg.show()
    #
    #     self.dlg.pushButton.clicked.connect(self.check)

    def check(self):
        ### Begin to simulate in the python terminal
        # layers = QgsProject.instance().mapLayers().values() 
        #ly = iface.activeLayer()
        #ly.name()
        #selection = ly
        #dp = ly.dataProvider()
        #lyrInput = selection
        #Nivel_de_Inspecao = 1
        #path_project = QgsProject.instance().fileName()
        #path_project = path_project[:path_project.rfind("/"):]
        #directory = path_project + "/samples"
        ### End to simulate in the python terminal
        
        # Create layer list
        layers = QgsProject.instance().mapLayers().values()

        class LayerInfo:
            name = ""
            crs = ""
            econding = ""
            count_ = ""
            formato = ""
            is_Valid = ""

        # Generate data table
        self.dlg1.tableWidget.clear()
        self.dlg1.tableWidget.setRowCount(len(layers))
        self.dlg1.tableWidget.setColumnCount(6)
        self.dlg1.tableWidget.setColumnWidth(0, 200)
        self.dlg1.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.dlg1.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Layer"))
        self.dlg1.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("SRC"))
        self.dlg1.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Econding"))
        self.dlg1.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Count"))
        self.dlg1.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem("Format"))
        self.dlg1.tableWidget.setHorizontalHeaderItem(5, QTableWidgetItem("isValid"))

        # Iterate over all loaded layers
        layer_list = []
        layer_count = 0

        for layer in layers:
            layer_count += 1

            layer_list.append(LayerInfo)
            layer_list[layer_count - 1].name = layer.name()
            layer_list[layer_count - 1].crs = layer.crs().description()
            try:
                layer_list[layer_count - 1].econding = layer.dataProvider().encoding()
                layer_list[layer_count - 1].count_ = layer.featureCount()
                layer_list[layer_count - 1].formato = layer.storageType()
            except AttributeError:
                pass
            
            layer_list[layer_count - 1].is_Valid = layer.isValid()
            
            self.dlg1.tableWidget.setItem(layer_count - 1, 0, QTableWidgetItem(layer.name()))
            self.dlg1.tableWidget.setItem(layer_count - 1, 1, QTableWidgetItem(layer.crs().description()))
            try: 
                self.dlg1.tableWidget.setItem(layer_count - 1, 2, QTableWidgetItem(layer.dataProvider().encoding()))
                self.dlg1.tableWidget.setItem(layer_count - 1, 3, QTableWidgetItem(str(layer.featureCount())))
                self.dlg1.tableWidget.setItem(layer_count - 1, 4, QTableWidgetItem(layer.storageType()))
            except AttributeError:
                pass
            
            self.dlg1.tableWidget.setItem(layer_count - 1, 5, QTableWidgetItem(str(layer.isValid())))

        self.dlg1.tableWidget.move(0, 0)

        def save_to_file():
            dialog = QFileDialog()
            name = dialog.getSaveFileName(None, "Export result to CSV", "", "CSV file (*.csv)")
            if name[0] == "":
                return None
        
            save_file = open(name[0], 'w')
        
            for i in layer_list:
                save_file.write("%s,%s\n" % (i.name, i.crs))
        
            save_file.close()

        self.dlg1.show()
        #self.dlg1.pushButton.clicked.connect(save_to_file)    