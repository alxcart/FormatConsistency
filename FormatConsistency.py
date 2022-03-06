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
from .main_format_consistency import *

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

    def run(self):
    #     """Run method that performs all the real work"""
    #     # show the dialog
        self.dlg.show()
    #
        self.dlg.pushButton.clicked.connect(self.check)

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
        info_camadas = list_layers(layers)

        #class LayerInfo:
        #    name = ""
        #    crs = ""
        #    econding = ""
        #    count_ = ""
        #    formato = ""
        #    is_Valid = ""

        # Generate data table
        mostrar_tabela(self, layers)
       
        self.dlg1.show()
        #self.dlg1.pushButton.clicked.connect(save_to_file)    