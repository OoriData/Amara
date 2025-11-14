# SPDX-FileCopyrightText: 2008-present Uche Ogbuji & Oori Data <info@oori.dev>
#
# SPDX-License-Identifier: Apache-2.0
# amara.uxml
'''
Parse an input source with MicroXML (or full XML) into an Amara 3 tree

>>> from amara.uxml import parse
>>> top = parse('<a><b i="1.1">+2+</b></a>')

Warning: if you pass a string, make sure it's a byte string,
not a Unicode object. You might also want to wrap it with
amara.lib.inputsource.text if it's not obviously XML
(to avoid e.g. its getting confused for a file name)
'''

from amara.uxml import tree

TB = tree.treebuilder()
parse = TB.parse


try:
    import amara.cmodules.cxmlstring
    isxml = amara.cmodules.cxmlstring.isxml
except ImportError:
    pass

