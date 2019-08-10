# -*- coding: utf-8 -*-
#/***************************************************************************
# Format consistency
#
# This plugin elaborates the area-oriented sampling plan, 
# it is based on the ISO 2859 series of standards. 
#							 -------------------
#		begin				: 2019-08-03
#		git sha			: $Format:%H$
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

# def classFactory(iface):  # pylint: disable=invalid-name
#     """Load FormatConsistency class from file FormatConsistency.

#     :param iface: A QGIS interface instance.
#     :type iface: QgsInterface
#     """
#     #
#     from .crs_tools import CheckDefConv
#     return CheckDefConv(iface)

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load FormatConsistency class from file FormatConsistency.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .FormatConsistency import FormatConsistency
    return FormatConsistency(iface)