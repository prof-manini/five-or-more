# -*- coding: iso-latin-1 -*-

import os
import random
import time

import gtk

import common
import gui_base
import board
import utils

image_dir = "./images"
images = [ "empty.png", "blue.png", "light-blue.png", "purple.png",
           "yellow.png", "green.png", "orange.png", "red.png"]

def get_image(value):
    path = os.path.join(image_dir, images[value])
    #print path
    return path

class StoneCell(gtk.Button):

    "Il widget che mostra le pedine in attesa di inserimento"

    def __init__(self):
        gtk.Button.__init__(self, None) #"%d:%d" % (row, col))

        self.set_size_request(40,40)
        self.image = gtk.Image()
        self.add(self.image)

    def set_value(self, value):
        #print value
        self.image.set_from_file(get_image(value))
    
class ButtonCell(gtk.Button):

    "Il widget per le pedine sulla scacchiera"

    def __init__(self, pos, back):
        gtk.Button.__init__(self, None)

        self.image = gtk.Image()
        #pixbuf = gtk.gdk.pixbuf_new_from_file(get_image(0))
        #pixbuf = pixbuf.scale_simple(8, 8, gtk.gdk.INTERP_BILINEAR)
        #self.image = gtk.image_new_from_pixbuf(pixbuf)
        self.add(self.image)

        self.pos = pos
        self.set_value(0)

        # self.connect("clicked", back, None)
        self.connect("pressed", back, None)

    def get_pos(self):
        return self.pos
    
    def set_value(self, value):
        self.value = value
        self.image.set_from_file(get_image(value))

    def __str__(self):
        return str(self.pos())
    
Cell = ButtonCell

class Grid(gtk.Table):
    "La griglia che fa da GUI per la scacchiera"

    def __init__(self, size, back):
        "Griglia di dimensione SIZE, BACK è il gestore dei click delle celle"
        self.size = size
        r,c = size
        gtk.Table.__init__(self, r, c, gtk.TRUE)
        self.set_homogeneous(gtk.TRUE)
        self.set_size_request(400,400)

        self.cells = mat = board.Board( size )
        for r,c,v in mat:
            o = Cell( (r,c), back)
            mat.set_value( (r,c), o)
            self.attach(o, r, r+1, c, c+1)

    def size(self):
        "Le dimensioni della scacchiera"
        return self.cells.size()
    
    def update_from_boss(self, boss):
        "Aggiorna la scacchiera con i dati della BOARD"
        cell = self.cells.get_value ## ????
        for r,c,v in boss.get_data():
            pos = r,c
            # print "Setting %s to %d" % (str(pos), v)
            cell(pos).set_value(v)

    def animation_stone(self, path, delay=500):
        cell = self.cells.get_value

        v = cell(path[0]).value
        cell(path[0]).set_value(0) # tolgo stone
        time.sleep(delay/1000)
        for c in path[1:-1]:
            cell(c).set_value(v)
            time.sleep(delay/1000)

    def step_cell(self, fc, tc):
        #raise "NotImplemented"
        cell = self.cells.get_value
        cell(tc).set_value(cell(fc).value)
        cell(fc).set_value(0)
        x = 400
        cell(tc).queue_draw_area(0, 0, x, x)
        cell(fc).queue_draw_area(0, 0, x, x)

class Window(gui_base.FullWindow):

    def __init__(self, boss):
        gui_base.FullWindow.__init__(self, "App")

        # self.boss e self.size sono usati nella costruzione della
        # grid, quindi serve settarla quanto prima
        self.boss = boss
        self.size = boss.get_size()

        # costruzione di parti dinamiche che dipendono da game
        self._make_menus()
        self.grid = None
        c = self._make_content() # create self.grid
        self.set_content(c)

        # altri setting della finestra
        self.set_size_request(400,400)
        self.set_resizable(gtk.FALSE)
        self.selected_pos = None

        # mostra la situazione iniziale del gioco
        self.update_from_boss()

        # controllo che non ci siano state sessioni di gioco interrotte
        tmp_file = self.boss.get_tmp_data()
        if tmp_file:
            ## chiedere all'utente se vuole ripristinare la precedente sessione di gioco
            print("Last session has been interrupted!")

    def _make_next_stones(self):
        h  = gtk.HBox(gtk.FALSE, 3)
        bb = []
        for c in range(3):
            b = StoneCell()
            bb.append(b)
            h.pack_end(b, gtk.FALSE, gtk.FALSE, 0)
        self._next_stones = bb
        self._score_label = gtk.Label()
        h.pack_start(self._score_label, gtk.FALSE, gtk.FALSE, 0)
        return h
            
    def _make_content(self):
        self.grid = Grid(self.size, self.on_cell_clicked)
        b = self._make_next_stones()
        v = gtk.VBox(gtk.FALSE, 2)
        v.pack_start(b,         gtk.FALSE, gtk.FALSE, 0)
        v.pack_end  (self.grid, gtk.TRUE,  gtk.TRUE,  0)
        return v    

    def on_cell_clicked(self, widget, data = None):
        old = self.selected_pos
        new = widget.get_pos()
        is_free = self.boss.is_free
        if not old:
            if is_free(new):
                self.show_message("Select a NON free cell!")
            else:
                self.show_message("Cell at %s selected" % str(new))
                self.selected_pos = new
        else:
            if new == old:
                self.show_message("Cell at %s DE-selected" % str(new))
                self.selected_pos = None
            else:
                if is_free(new):
					if self.boss.can_move(old, new):
						self.show_message("Moving %s to %s" %
							(str(old), str(new)))
						self.do_move(old, new)
						self.selected_pos = None

						if not self.boss.is_there_free_cells():
							self.show_message("Game Over! Score: %d... saved!"%self.boss.get_score())
							self.boss.save_score()
					else:
						self.show_message("NO path from %s to %s" % 
						(str(old), str(new)))
                else:
                    self.show_message("Cell at %s selected" % str(new))
                    self.selected_pos = new
        
    def _make_menus(self):

        make = self.menu_bar.easy_make_menu
        
        make("_Game", (
            ("_New",  self.on_new_game),
            ("_Load", self.on_load_game),
            ("_Save", self.on_save_game),
            ("_Records", self.on_records),
            ("Undo", self.on_undo),
            ("Redo", self.on_redo),
            ("-", None),
            ("_Quit", self.quit),
            ))
        
        make("_Help", (
            ("_Content", self.on_help),
            ("_About", self.on_about),
            ))

    def _update_next_stones(self):
        vv = self.boss.get_next_values()
        ss = self._next_stones
        for c,v in enumerate(vv):
            ss[c].set_value(v)

    def _update_score(self):
        s = self.boss.get_score()
        self._score_label.set_text("Punteggio: %3d" % s)
        
    def update_from_boss(self):
        self.grid.update_from_boss(self.boss)
        self._update_next_stones()
        self._update_score()        

    # gestori degli eventi
    def on_help(self, widget):
        self.show_message("Read the source, Luke!")

    def on_about(self, widget):
        gui_base.show_about(common.about_message)

    def on_new_game(self, widget):
        self.boss.new_empty_game(self.size)
        self.update_from_boss()
        self.show_message("New Game.")
        
    def on_load_game(self, widget):
        file = utils.choose_file_for_open(dir=common.SAVE_DIR)
        if not file:
            self.show_message("Loading aborted.")
            return

        self.show_message("Loading from: %s" % file)
        if self.boss.load_game(file):
        	self.update_from_boss()
        else:
        	self.show_message("Bad file '%s'. Chose another file."%file)
        
    def on_save_game(self, widget):
        file = utils.choose_file_for_save(dir=common.SAVE_DIR)
        if not file:
            self.show_message("Saving aborted.")
            return

        self.show_message("Saving to: %s" % file)
        self.boss.save_game(file)

    def on_records(self, widget):
    	records = self.boss.load_records()
    	s = ""
    	for i, r in enumerate(records):
    		s += "%d) %d "%(i+1,r)
    	if s:
    		self.show_message(s.strip())
    	else:
    		self.show_message("Nessun record.")

    def on_undo(self, widget):
        if self.boss.undo():
            self.show_message("Undo...")
            self.update_from_boss()
        else:
            self.show_message("Can not undo.")

    def on_redo(self, widget):
        if self.boss.redo():
            self.show_message("Redo...")
            self.update_from_boss()
        else:
            self.show_message("Can not redo.")

    def do_move(self, fc, tc):
        #paths = self.boss.get_paths(fc, tc)
        #v = self.boss._board.get_value(fc) 

        self.boss.move(fc, tc)
        #self.grid.animation_stone(paths[0], v) ## !!!!!! probema: griglia si aggiorna dopo chiamata ad evento
        #self.grid.step_cell(fc, tc)
        #self.grid.queue_draw_area(0, 0, 400, 400)
        #self.queue_draw()
        #gtk.gdk.Window.invalidate_rect(self)
        #time.sleep(3)
        self.update_from_boss()

    def quit(self, widget):
        self.boss.finalize_game()
        gtk.main_quit()
    
def get_gui_for_boss(boss):    
    return Window(boss)

