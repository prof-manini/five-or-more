#!/usr/bin/env python
# -*- coding: iso-latin-1 -*-
# Copyright: Luca Manini (2005)

if __name__ == "__main__":

    from lines import gui, boss

    b = boss.Boss()
    g = gui.get_gui_for_boss(b)
    g.run()
