from gi.repository.Gtk import PrintOperation, PageSetup
from gi.repository import GObject as gobject

########################
###
###   SEARCH
###
########################

def search(act):
    act.vibase.view.emit("start_interactive_search")
   
def search_cursor(act, forward=True):
    """search for token under cursor"""
    doc = act.vibase.doc
    view = act.vibase.view
    buf = view.get_buffer()

    start, end = act.pos.buffer_token_boundary(buf)
    token = doc.get_text(start, end).strip()
    
    #don't search for whitespace
    if token:
        doc.set_search_text(token, 0)

    if forward:
        ret = end.forward_search(token, 0)

        #if nothing was found, search again from start
        if not ret:
            ret = buf.get_bounds()[0].forward_search(token, 0)
    else:
        ret = start.backward_search(token, 0)

        if not ret:
            ret = buf.get_bounds()[1].backward_search(token, 0)
    act.pos.moveInsert(act, ret[0])

def search_cursor_backward(act):
    search_cursor(act, forward=False)

########################
###
###   UNDO/REDO
###
########################

def undo(act):
    act.vibase.view.emit("undo")
    
def redo(act):
    act.vibase.view.emit("redo")

def redoLastOperation(act):
    act.vibase.lastOperation(act)

def getTerminal(act):
    # Get the terminal
    # TODO Probably needs a more sophisticated lookup, e.g., python terminal not installed, etc.
    window = act.vigtk.window
    bottom_panel = window.get_bottom_panel()
    notebook = bottom_panel.get_children()[0].get_children()[0]
    if len(notebook.get_children()) != 0:
        terminal = notebook.get_children()[1]
        return terminal
    return None

########################
###
###   PRINTING
###
########################

def draw_page(operation, context, page_nr, compositor):
    compositor.draw_page(context, page_nr)
    
def begin_print(operation, context, compositor):
    n_pages = 1
    while not compositor.paginate(context):
        pass
    
    n_pages = compositor.get_n_pages()
    operation.set_n_pages(n_pages)
    
def printall(act, location):
    views = [view for view in act.vigtk.window.get_views()]

    count = 1
    for view in views:
            
        po = PrintOperation()
        setup = PageSetup()
        po.set_default_page_setup(setup)
        
        po.set_export_filename("%s/%d.pdf" % (location, count))
        count += 1
        
        pc = gtksourceview2.print_compositor_new_from_view(view)
        
        po.connect("begin_print", begin_print, pc)
        po.connect("draw_page", draw_page, pc)
    
        res = po.run(act.gtk.PRINT_OPERATION_ACTION_EXPORT)
