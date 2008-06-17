# -*- coding: utf-8 -*-

#  vigtk.py - Vi Keybindings for gtk.TextView.
#  
#  Copyright (C) 2008 - Joseph Method
#  Copyright (C) 2006 - Trond Danielsen
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#   
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#   
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330,
#  Boston, MA 02111-1307, USA.

import gtk
from actions.menus import Menus
        
class ViGtk:

    (COMMAND_MODE, VISUAL_MODE, DELETE_MODE, 
    INSERT_MODE, EX_MODE, YANK_MODE, GMODE, 
    CMODE, RMODE, TMODE, SELECTION_MODE, INDENT_MODE) = range(12)

    modes = { 0 : 'command', 1 : 'visual', 
              2: 'delete',   3 : 'insert', 
              4: 'ex', 5: 'yank', 6: 'gmode', 
              7:'cmode', 8: 'rmode', 9: 'tmode',
              10:'selection', 11:'indent'}    
              
    def get_mode(self, mode):
        """ Get mode text """
        return { 
                ViGtk.COMMAND_MODE: _("Command Mode"),
                ViGtk.VISUAL_MODE: _("Visual Mode"),
                ViGtk.DELETE_MODE: _("Delete Mode"),
                ViGtk.INSERT_MODE:_("Insert Mode"),
                ViGtk.EX_MODE: _(": "),
                ViGtk.YANK_MODE: _("Yank Mode"),
                ViGtk.GMODE: _("G Mode"),
                ViGtk.CMODE: _("C Mode"),
                ViGtk.RMODE: _("R Mode"),
                ViGtk.TMODE: _("T Mode"),
                ViGtk.SELECTION_MODE: _("Selection Mode"),
                ViGtk.INDENT_MODE: _("Indent Mode")
                }.get(mode)
              
    initial = True
    
    def __init__(self, statusbar, view, window, bindings):
        self.update_vigtk(view, window, bindings, statusbar)
        
        if ViGtk.initial:
            ViGtk.initial = False
            ViGtk.last_search = None
            ViGtk.menus = Menus(ViGtk.window)
            ViGtk.ignored_keys = map( gtk.gdk.keyval_from_name, \
                    ['Up', 'Down', 'Left', 'Right', 'Page_Up', 'Page_Down', 'Home', 'End'] + \
                    ["F%d" % n for n in range(1,13)] )
            ViGtk.bindings = bindings
            ViGtk.bindings.init_modes()
        
        print "__init__:" #     %s in %s" % (self, ViGtk.view)
        
        
    def update_vigtk(self, view, window, bindings, statusbar):
        ViGtk.window = window
        ViGtk.view = view
        ViGtk.doc = view.get_buffer()
        ViGtk.selection_start = None
        ViGtk.selection_end = None
        ViGtk.select = True
        ViGtk.acc = []
        ViGtk.number = 0
        ViGtk.numLines = 0
        ViGtk.old_mode = ViGtk.COMMAND_MODE
        ViGtk.already_selected = False
        ViGtk.returnToMode = None
        ViGtk.statusbar = statusbar
        ViGtk.mode = ViGtk.COMMAND_MODE

