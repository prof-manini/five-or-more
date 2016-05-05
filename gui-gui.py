#!/usr/bin/env python
# -*- coding: iso-latin-1 -*-
# Copyright: Luca Manini (2005)

if __name__ == "__main__":

    from lines import gui, boss

    b = boss.Boss()

    # controllo che non ci siano state sessioni di gioco interrotte
    tmp_data = b.get_tmp_data()
    if tmp_data:
        ## chiedere all'utente se vuole ripristinare la precedente sessione di gioco
        print("Last session has been interrupted!")
        ripristinate = raw_input("Do you want to ripristinate last session?(Y/n): ")
        
        if ripristinate.lower() in ("y", "yes") or not ripristinate:
        	b.load_tmp(tmp_data)

    g = gui.get_gui_for_boss(b)
    g.run()
