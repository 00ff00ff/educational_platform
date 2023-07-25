#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib
import threading
import importlib
from time import sleep
import maestro
import arm_controller
import wireless_board
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
except:
    pass


file = open("Interpreted_code.py", "w")
file.write("")
file.close()

CODE = importlib.import_module("Interpreted_code")


skladnia_poj = [
    ["czytaj", "get_input"],
    ["ustaw", "set_device"],
    ["laduj", "setup"],
    ["dodaj", "add_device"],
    ["LaB", "Board_Interpreter()"],
    ["laboratorium", "wireless_board_interpreter"],
    ["importuj", "import"],
    ["prosto", "straight"],
    ["cofaj", "back"],
    ["lewo", "left"],
    ["prawo", "right"],
    ["stoj", "stop"],

    ["panel", "control_panel_interpreter"],
    ["Tester", "Panel_Interpreter()"],

    ["ramie", "arm_controller"],
    ["Ramie", "Arm_Controller()"],
    ["wczytaj", "jump_to"],
    ["stop", "stop"],

    ["i", "and"],
    ["lub", "or"],
    ["spij", "sleep"],
    ["napisz", "self.output += \"\\n\" + str"],
    ["jesli", "if"],
    ["zmienna", ""],
    ["inaczej_jesli", "elif"],
    ["inaczej", "else"],
    ["dla", "for"],
    ["w", "in"],
    ["w_zakresie", "in range"],
    ["rob", ""],
    ["prawda", "True"],
    ["falsz", "False"],
    ["glowna_petla", "while self.con"],
    ["dopoki", "while"],
    ["nie", "not"],
    ["reszta", "%"],
    ["{", ":"],
    ["}", ""],
    ["\n", ""],
]
#region-------------StałePanelu----------------

Dioda_1 = 24
Dioda_2 = 25
Dioda_3 = 5
Enkoder = [6, 12]
Silnik = [13, 16]
Przycisk_1 = 4
Przycisk_2 = 26
Przelacznik = 10



lista_czujnikow = [
    [0, "Laserowy"],
    [0, "Wstrząsów"],
    [1, "Temperatury"],
    [4, "Enkoder"],
    [9, "Przycisk_1"],
    [10, "Przycisk_2"],
    [11, "Przełącznik"],

]
lista_wyjsc = [
    [5, "Silnik"],
    [6, "Dioda_1"],
    [7, "Dioda_2"],
    [8, "Dioda_3"],
]


piny_analogowe = [
    [20, "1"],
    [21, "2"],
    [23, "3"]

]

piny_cyfrowe = [
    [17, "12"],
    [18, "13"]

]

lista_czujnikow_buf = [
    [0, "Laserowy"],
    [0, "Wstrząsów"],
    [1, "Temperatury"],
    [4, "Enkoder"],
    [9, "Przycisk_1"],
    [10, "Przycisk_2"],
    [11, "Przełącznik"],
]

lista_wyjsc_buf = [
    [5, "Silnik"],
    [6, "Dioda_1"],
    [7, "Dioda_2"],
    [8, "Dioda_3"],
]

piny_analogowe_buf = [
    [27, "1"],
    [22, "2"],
    [23, "3"]
]

piny_cyfrowe_buf = [
    [17, "4"],
    [18, "5"]
]

lista_urzadzen = []

lista_polecen = []

#endregion

#region-----------TablicePlytki------------------

b_silnik = [4, 5, 6, 7]

s_lista_czujnikow = [
    [0, "Laserowy"],
    [0,  "Wstrząsów"],
    [1,  "Temperatury"],
    [1,  "Dźwięku"],
    [1, "Poziomu wody"],
    [1, "Odległości"],

]
s_lista_wyjsc = [
    [2, "Silnik"],
]

s_piny_analogowe = [
    [15, "3"],
    [16, "4"],
    [17, "5"],
    [18, "6"],
    [19, "7"],
]

s_piny_cyfrowe = [
    [2, "0"],
    [3, "1"],
    [8, "2"],
]

s_lista_czujnikow_buf = [
    [0, "Laserowy"],
    [0, "Wstrząsów"],
    [1, "Temperatury"],
    [1, "Dźwięku"],
    [1, "Poziomu wody"],
    [1, "Odległości"],
]
s_lista_wyjsc_buf = [
    [2, "Silnik"],
]

s_piny_analogowe_buf = [
    [15, "3"],
    [16, "4"],
    [17, "5"],
    [18, "6"],
    [19, "7"],
]

s_piny_cyfrowe_buf = [
    [2, "0"],
    [3, "1"],
    [8, "2"],
]



s_lista_urzadzen = []

s_lista_polecen = []

#endregion



list_box2 = Gtk.ListBox()
list_box = Gtk.ListBox()
s_listbox1 = Gtk.ListBox()
s_listbox2 = Gtk.ListBox()

IList = Gtk.ListStore(int, str)
IList.append([0, "Zczytaj wartość"])
IList.append([1, "Wyślij wartość"])
IList.append([2, "Opuźnienie(ms)"])
IIList = Gtk.ListStore(int, str)
IIIList = Gtk.ListStore(int, str)
IVList = Gtk.ListStore(int, str)


ICombo = Gtk.ComboBox.new_with_model_and_entry(IList)
ICombo.set_entry_text_column(1)
IICombo = Gtk.ComboBox.new_with_model_and_entry(IIList)
IICombo.set_entry_text_column(1)
IIICombo = Gtk.ComboBox.new_with_model_and_entry(IIIList)
IIICombo.set_entry_text_column(1)
IVCombo = Gtk.ComboBox.new_with_model_and_entry(IVList)
IVCombo.set_entry_text_column(1)




textview3 = Gtk.TextView()
textbuffer1 = textview3.get_buffer()
textbuffer3 = textview3.get_buffer()


choice = [0, "", "", ""]


stack = Gtk.Stack()




#region DIALOG

class AddDialog(Gtk.Dialog):

    def __init__(self, parent, c):
        Gtk.Dialog.__init__(self, "Dodaj urządzenie", parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        self.c = c

        List = Gtk.ListStore(int, str)
        List.append([1, "Czujnik"])
        List.append([2, "Urządzenie wyjścia"])

        self.ComboII = Gtk.ComboBox.new_with_model_and_entry(Gtk.ListStore())
        self.ComboIII = Gtk.ComboBox.new_with_model_and_entry(Gtk.ListStore())
        self.ComboI = Gtk.ComboBox.new_with_model_and_entry(List)
        self.ComboI.set_entry_text_column(1)
        self.ComboI.connect("changed", self.on_ComboI_changed)
        self.ComboII.connect("changed", self.on_ComboII_changed)
        self.ComboIII.connect("changed", self.on_ComboIII_changed)
        self.entry = Gtk.Entry()
        self.entry.set_editable(False)
        buffer = self.entry.get_buffer()
        choice = [0, "", "", ""]
        self.button = Gtk.Button(label="Dodaj")
        self.button.connect("clicked", self.on_add_device_button)

        area = self.get_content_area()
        self.box = Gtk.Box()
        self.box.pack_start(self.ComboI, True, True, 0)
        self.box.pack_start(self.ComboII, True, True, 0)
        self.box.pack_start(self.ComboIII, True, True, 0)
        self.box.pack_start(self.entry, True, True, 0)
        self.box.pack_start(self.button, True, True, 0)

        area.add(self.box)
        self.update_lists()
        self.show_all()

    def update_lists(self):
        if self.c == 0:
            self.Lista_czujnikow = Gtk.ListStore(int, str)
            lista_czujnikow_buf.sort()
            for e in lista_czujnikow_buf:
                self.Lista_czujnikow.append(e)

            self.Lista_wyjsc = Gtk.ListStore(int, str)
            lista_wyjsc_buf.sort()
            for e in lista_wyjsc_buf:
                self.Lista_wyjsc.append(e)

            self.Lista_analog = Gtk.ListStore(int, str)
            piny_analogowe_buf.sort()
            for e in piny_analogowe_buf:
                self.Lista_analog.append(e)

            self.Lista_cyf = Gtk.ListStore(int, str)
            piny_cyfrowe_buf.sort()
            for e in piny_cyfrowe_buf:
                self.Lista_cyf.append(e)
        if self.c == 1:
            self.Lista_czujnikow = Gtk.ListStore(int, str)
            s_lista_czujnikow_buf.sort()
            for e in s_lista_czujnikow_buf:
                self.Lista_czujnikow.append(e)

            self.Lista_wyjsc = Gtk.ListStore(int, str)
            s_lista_wyjsc_buf.sort()
            for e in s_lista_wyjsc_buf:
                self.Lista_wyjsc.append(e)

            self.Lista_analog = Gtk.ListStore(int, str)
            s_piny_analogowe_buf.sort()
            for e in s_piny_analogowe_buf:
                self.Lista_analog.append(e)

            self.Lista_cyf = Gtk.ListStore(int, str)
            s_piny_cyfrowe_buf.sort()
            for e in s_piny_cyfrowe_buf:
                self.Lista_cyf.append(e)

        self.ComboII.set_model(model=Gtk.ListStore())
        self.ComboIII.set_model(model=Gtk.ListStore())


    def on_add_device_button(self, widget):
        if self.entry.get_text() != "":
            if self.c == 0:
                row = Gtk.ListBoxRow()
                vbox = Gtk.Box()
                if choice[0] == 0:
                    for e in lista_czujnikow_buf:
                        if e[1] == choice[1]:
                            vbox.pack_start(Gtk.Label(e[1]), True, True, 0)
                            if e[0] == 0:
                                for e1 in piny_cyfrowe_buf:
                                    if e1[1] == choice[2]:
                                        vbox.pack_start(Gtk.Label(e1[1]), True, True, 0)
                                        lista_urzadzen.append([choice[0], e1[0], self.entry.get_text(), e[1]])
                                        piny_cyfrowe_buf.remove(e1)
                                        break
                            elif e[0] == 1:
                                for e1 in piny_analogowe_buf:
                                    if e1[1] == choice[2]:
                                        vbox.pack_start(Gtk.Label(e1[1]), True, True, 0)
                                        lista_urzadzen.append([choice[0], e1[0], self.entry.get_text(), e[1]])
                                        piny_analogowe_buf.remove(e1)
                                        break
                            elif e[0] == 4:
                                vbox.pack_start(Gtk.Label(4), True, True, 0)
                                lista_urzadzen.append([choice[0], Enkoder, self.entry.get_text(), 4])
                            elif e[0] == 9:
                                vbox.pack_start(Gtk.Label(9), True, True, 0)
                                lista_urzadzen.append([choice[0], Przycisk_1, self.entry.get_text(), 9])
                            elif e[0] == 10:
                                vbox.pack_start(Gtk.Label(10), True, True, 0)
                                lista_urzadzen.append([choice[0], Przycisk_2, self.entry.get_text(), 10])
                            elif e[0] == 11:
                                vbox.pack_start(Gtk.Label(11), True, True, 0)
                                lista_urzadzen.append([choice[0], Przelacznik, self.entry.get_text(), 11])


                            lista_czujnikow_buf.remove(e)

                            break
                elif choice[0] == 1:
                    for e in lista_wyjsc_buf:
                        if e[1] == choice[1]:
                            vbox.pack_start(Gtk.Label(e[1]), True, True, 0)
                            if e[0] == 0:
                                for e1 in piny_cyfrowe_buf:
                                    if e1[1] == choice[2]:
                                        vbox.pack_start(Gtk.Label(e1[1]), True, True, 0)
                                        lista_urzadzen.append([choice[0], e1[0], self.entry.get_text(), e[1]])
                                        piny_cyfrowe_buf.remove(e1)
                                        break
                            elif e[0] == 1:
                                for e1 in piny_analogowe_buf:
                                    if e1[1] == choice[2]:
                                        vbox.pack_start(Gtk.Label(e1[1]), True, True, 0)
                                        lista_urzadzen.append([choice[0], e1[0], self.entry.get_text(), e[1]])
                                        piny_analogowe_buf.remove(e1)
                                        break

                            elif e[0] == 5:
                                vbox.pack_start(Gtk.Label(5), True, True, 0)
                                lista_urzadzen.append([choice[0], Silnik, self.entry.get_text(), 5])
                            elif e[0] == 6:
                                vbox.pack_start(Gtk.Label(6), True, True, 0)
                                lista_urzadzen.append([choice[0], Dioda_1, self.entry.get_text(), 6])
                            elif e[0] == 7:
                                vbox.pack_start(Gtk.Label(7), True, True, 0)
                                lista_urzadzen.append([choice[0], Dioda_2, self.entry.get_text(), 7])
                            elif e[0] == 8:
                                vbox.pack_start(Gtk.Label(8), True, True, 0)
                                lista_urzadzen.append([choice[0], Dioda_3, self.entry.get_text(), 8])

                            lista_wyjsc_buf.remove(e)

                            break
                vbox.pack_start(Gtk.Label(self.entry.get_text()), True, True, 0)
                row.add(vbox)
                list_box.add(row)
                list_box.show_all()
                self.update_lists()
                self.ComboI = Gtk.ComboBox()
                self.ComboI.show_all()

            if self.c == 1:
                row = Gtk.ListBoxRow()
                vbox = Gtk.Box()
                if choice[0] == 0:
                    for e in s_lista_czujnikow_buf:
                        if e[1] == choice[1]:
                            vbox.pack_start(Gtk.Label(e[1]), True, True, 0)
                            if e[0] == 0:
                                for e1 in s_piny_cyfrowe_buf:
                                    if e1[1] == choice[2]:
                                        vbox.pack_start(Gtk.Label(e1[1]), True, True, 0)
                                        s_lista_urzadzen.append([choice[0], e1[0], self.entry.get_text(), e[1]])
                                        s_piny_cyfrowe_buf.remove(e1)
                                        break
                            elif e[0] == 1:
                                for e1 in s_piny_analogowe_buf:
                                    if e1[1] == choice[2]:
                                        vbox.pack_start(Gtk.Label(e1[1]), True, True, 0)
                                        s_lista_urzadzen.append([choice[0], e1[0], self.entry.get_text(), e[1]])
                                        s_piny_analogowe_buf.remove(e1)
                                        break
                            s_lista_czujnikow_buf.remove(e)
                            break
                elif choice[0] == 1:
                    for e in s_lista_wyjsc_buf:
                        if e[1] == choice[1]:
                            vbox.pack_start(Gtk.Label(e[1]), True, True, 0)
                            if e[0] == 0:
                                for e1 in s_piny_cyfrowe_buf:
                                    if e1[1] == choice[2]:
                                        vbox.pack_start(Gtk.Label(e1[1]), True, True, 0)
                                        s_lista_urzadzen.append([choice[0], e1[0], self.entry.get_text(), e[1]])
                                        s_piny_cyfrowe_buf.remove(e1)
                                        break
                            elif e[0] == 1:
                                for e1 in s_piny_analogowe_buf:
                                    if e1[1] == choice[2]:
                                        vbox.pack_start(Gtk.Label(e1[1]), True, True, 0)
                                        s_lista_urzadzen.append([choice[0], e1[0], self.entry.get_text(), e[1]])
                                        s_piny_analogowe_buf.remove(e1)
                                        break

                            elif e[0] == 2:
                                vbox.pack_start(Gtk.Label(9), True, True, 0)
                                s_lista_urzadzen.append([choice[0], b_silnik, self.entry.get_text(), 9])

                            s_lista_wyjsc_buf.remove(e)
                            break
                vbox.pack_start(Gtk.Label(self.entry.get_text()), True, True, 0)
                row.add(vbox)
                s_listbox1.add(row)
                s_listbox1.show_all()
                self.update_lists()

    def on_ComboI_changed(self, combo):

        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]

        if int(row_id) == 1:
            self.ComboII.set_model(model=self.Lista_czujnikow)
            choice[0] = 0

        if int(row_id) == 2:
            self.ComboII.set_model(model=self.Lista_wyjsc)
            choice[0] = 1

        self.ComboII.set_entry_text_column(1)
        self.ComboII.show_all()

    def on_ComboII_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]

        if int(row_id) == 0:
            self.ComboIII.set_model(model=self.Lista_cyf)
            choice[1] = name

        if int(row_id) == 1:
            self.ComboIII.set_model(model=self.Lista_analog)
            choice[1] = name


        if int(row_id) == 4 or int(row_id) == 5 or int(row_id) == 6 or int(row_id) == 7 or int(row_id) == 8 or int(row_id) == 9 or int(row_id) == 10 or int(row_id) == 11:
            l = Gtk.ListStore(int, str)
            l.append([int(row_id), str(row_id)])
            self.ComboIII.set_model(model=l)
            choice[1] = name

        if int(row_id) == 2:
            l = Gtk.ListStore(int, str)
            l.append([9, "9"])
            self.ComboIII.set_model(model=l)
            choice[1] = name


        self.ComboIII.set_entry_text_column(1)
        self.ComboIII.show_all()

    def on_ComboIII_changed(self, combo):
        self.entry.set_editable(True)

        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            choice[2] = name

#endregion

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="MM_BotLab")

        main_grid = Gtk.Grid()
        self.add(main_grid)
        self.set_default_size(1000, 800)

        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(500)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.textview1 = Gtk.TextView()
        scrolledwindow.add(self.textview1)

        scrolledwindow2 = Gtk.ScrolledWindow()
        scrolledwindow2.set_hexpand(True)
        scrolledwindow2.set_vexpand(True)
        self.textview2 = Gtk.TextView()
        scrolledwindow2.add(self.textview2)

        self.textbuffer = self.textview1.get_buffer()
        self.textbuffer2 = self.textview2.get_buffer()

        stack.add_titled(scrolledwindow, "check1", "Interpreter")
        stack.add_titled(scrolledwindow2, "check2", "Python")


        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        frame1 = Gtk.Frame()
        frame1.add(stack)
        main_grid.add(stack_switcher)
        main_grid.attach(frame1, 0, 1, 40, 30)

        box1 = Gtk.Box(spacing=500)
        main_grid.attach(box1, 0, 32, 1, 30)

        button1 = Gtk.Button(label="Interpretuj")
        button1.connect("clicked", self.on_interpreter_click)
        self.button2 = Gtk.Button(label="Uruchom program użytkownika")
        self.button2.connect("clicked", self.on_run_user_code_clicked)

        box1.pack_start(button1, True, True, 0)
        box1.pack_start(self.button2, True, True, 0)

        box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        s_box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=7)
        s_box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        stack2 = Gtk.Stack()

        stack2.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack2.set_transition_duration(500)

        stack2.add_titled(box2, "check1", "Panel edukacyjny")
        stack2.add_titled(s_box2, "check2", "Zdalne laboratorium")
        stack2.add_titled(s_box3, "check3", "Sterowanie ramieniem")
        stack_switcher2 = Gtk.StackSwitcher()
        stack_switcher2.set_stack(stack2)
        main_grid.attach(stack_switcher2, 40, 1, 1, 1)

        main_grid.attach(stack2, 40, 2, 1, 29)



#region-----------------PANEL EDUKACYJNY------------------------------------------------------------



        scrolledwindow3 = Gtk.ScrolledWindow()
        scrolledwindow3.set_hexpand(True)
        scrolledwindow3.set_vexpand(True)
        scrolledwindow3.add(list_box)
        frame = Gtk.Frame(label="Lista urządzeń")
        frame.add(scrolledwindow3)
        ibox2 = Gtk.Box(spacing=2)
        button6 = Gtk.Button(label="Dodaj")
        button6.connect("clicked", self.on_add_device_clicked)
        button7 = Gtk.Button(label="Usuń")
        button7.connect("clicked", self.on_delete_row_button_clicked)
        iibox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        iibox.pack_start(button6, True, True, 0)
        iibox.pack_start(button7, True, True, 0)
        ibox2.pack_start(frame, True, True, 0)
        ibox2.pack_start(iibox, False, False, 3)
        box2.pack_start(ibox2, True, True, 0)

        ibox1 = Gtk.Box(spacing=5)
        frame2 = Gtk.Frame(label="Dodaj działanie")
        frame2.add(ibox1)
        box2.pack_start(frame2, False, True, 0)
        button3 = Gtk.Button(label="+")
        button3.connect("clicked", self.on_add_activity)



        ICombo.connect("changed", self.on_ICombo_changed)
        IICombo.connect("changed", self.on_IICombo_changed)
        IIICombo.connect("changed", self.on_IIICombo_changed)
        IVCombo.connect("changed", self.on_IVCombo_changed)

        ibox1.pack_start(ICombo, False, True, 0)
        ibox1.pack_start(IICombo, False, True, 0)
        ibox1.pack_start(IIICombo, False, True, 0)
        ibox1.pack_start(IVCombo, False, True, 0)
        ibox1.pack_start(button3, False, True, 0)




        scrolledwindow4 = Gtk.ScrolledWindow()
        scrolledwindow4.set_hexpand(True)
        scrolledwindow4.set_vexpand(True)
        scrolledwindow4.add(list_box2)
        frame3 = Gtk.Frame(label="Lista poleceń")
        frame3.add(scrolledwindow4)
        ibox4 = Gtk.Box(spacing=3)
        button8 = Gtk.Button(label="Usuń")
        button8.connect("clicked", self.on_delete_activity_clicked)
        ibox4.pack_start(frame3, True, True, 0)
        ibox4.pack_start(button8, False, True, 3)
        box2.pack_start(ibox4, True, True, 0)

        button4 = Gtk.Button(label="Załaduj")
        button4.connect("clicked", self.on_load_clicked)


        box2.pack_start(button4, False, False, 0)

        scrolledwindow5 = Gtk.ScrolledWindow()
        scrolledwindow5.set_hexpand(True)
        scrolledwindow5.set_vexpand(True)


        textview3.set_editable(False)
        textview3.set_cursor_visible(False)


        scrolledwindow5.add(textview3)
        frame4 = Gtk.Frame(label="Konsola")
        frame4.add(scrolledwindow5)
        box2.pack_start(frame4, True, True, 0)

        scrolledwindow5.connect('size-allocate', self.treeview_changed2)
#endregion --------------------------------------------------------------------------------------------


#region -----------------LABORATORIUM--------------------------------------------------------

        self.s_serial_switch = Gtk.Button(label="Połącz z urządzeniem")

        s_box2.pack_start(self.s_serial_switch, False, True, 3)

        self.s_frame1 = Gtk.Frame(label="Lista peryferiów")
        self.scrolledwindow3 = Gtk.ScrolledWindow()
        self.scrolledwindow3.set_hexpand(True)
        self.scrolledwindow3.set_vexpand(True)
        self.scrolledwindow3.add(s_listbox1)
        self.s_frame1.add(self.scrolledwindow3)
        self.s_button1 = Gtk.Button(label="Dodaj")
        self.s_button2 = Gtk.Button(label="Usuń")
        self.s_iiBox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.s_iiBox1.pack_start(self.s_button1, True, True, 0)
        self.s_iiBox1.pack_start(self.s_button2, True, True, 0)
        self.s_iBox1 = Gtk.Box(spacing=2)
        self.s_iBox1.pack_start(self.s_frame1, True, True, 0)
        self.s_iBox1.pack_start(self.s_iiBox1, False, False, 3)
        s_box2.pack_start(self.s_iBox1, True, True, 0)

        self.s_button3 = Gtk.Button(label="Zaprogramuj gniazda")
        s_box2.pack_start(self.s_button3, False, False, 0)

        self.s_iiBox2 = Gtk.Box(spacing=5)
        self.IList = Gtk.ListStore(int, str)
        self.IList.append([0, "Zczytaj wartość"])
        self.IList.append([1, "Wyślij wartość"])
        self.IList.append([2, "Opóźnienie(ms)"])
        self.IIList = Gtk.ListStore(int, str)
        self.IIIList = Gtk.ListStore(int, str)
        self.IVList = Gtk.ListStore(int, str)

        self.ICombo = Gtk.ComboBox.new_with_model_and_entry(self.IList)
        self.ICombo.set_entry_text_column(1)
        self.IICombo = Gtk.ComboBox.new_with_model_and_entry(self.IIList)
        self.IICombo.set_entry_text_column(1)
        self.IIICombo = Gtk.ComboBox.new_with_model_and_entry(self.IIIList)
        self.IIICombo.set_entry_text_column(1)
        self.IVCombo = Gtk.ComboBox.new_with_model_and_entry(self.IVList)
        self.IVCombo.set_entry_text_column(1)
        self.s_button4 = Gtk.Button(label="+")
        self.s_iiBox2.pack_start(self.ICombo, False, True, 0)
        self.s_iiBox2.pack_start(self.IICombo, False, True, 0)
        self.s_iiBox2.pack_start(self.IIICombo, False, True, 0)
        self.s_iiBox2.pack_start(self.IVCombo, False, True, 0)
        self.s_iiBox2.pack_start(self.s_button4, False, True, 0)
        self.s_frame2 = Gtk.Frame(label="Dodaj działanie")
        self.s_frame2.add(self.s_iiBox2)
        s_box2.pack_start(self.s_frame2, False, False, 0)

        self.s_sc = Gtk.ScrolledWindow()
        self.s_sc.set_hexpand(True)
        self.s_sc.set_vexpand(True)
        self.s_sc.add(s_listbox2)
        self.s_frame3 = Gtk.Frame(label="Lista kroków")
        self.s_frame3.add(self.s_sc)
        self.s_iiBox3 = Gtk.Box(spacing=2)
        self.s_button5 = Gtk.Button(label="Usuń")
        self.s_iiBox3.pack_start(self.s_frame3, True, True, 0)
        self.s_iiBox3.pack_start(self.s_button5, False, False, 3)
        s_box2.pack_start(self.s_iiBox3, True, True, 0)

        self.s_button6 = Gtk.Button(label="Uruchom")
        s_box2.pack_start(self.s_button6, False, True, 0)

        self.s_sc2 = Gtk.ScrolledWindow()
        self.s_sc2.set_hexpand(True)
        self.s_sc2.set_vexpand(True)
        self.s_textview1 = Gtk.TextView()
        self.s_textview1.set_editable(False)
        self.s_textview1.set_cursor_visible(False)
        self.s_textbuffer1 = self.s_textview1.get_buffer()
        self.s_sc2.add(self.s_textview1)
        self.s_frame4 = Gtk.Frame(label="Konsola")
        self.s_frame4.add(self.s_sc2)
        s_box2.pack_start(self.s_frame4, True, True, 0)

        self.s_serial_switch.connect("clicked", self.serial_switcher)
        self.s_button1.connect("clicked", self.on_add_device_board_clicked)
        self.s_button2.connect("clicked", self.on_delete_device_board_clicked)
        self.ICombo.connect("changed", self.on_comboI_board_changed)
        self.IICombo.connect("changed", self.on_comboII_board_changed)
        self.s_button4.connect("clicked", self.on_add_board_activity)
        self.s_button5.connect("clicked", self.on_delete_board_activity)
        self.s_button3.connect("clicked", self.on_setup_board)
        self.s_button6.connect("clicked", self.on_run_board_clicked)
        self.s_sc2.connect('size-allocate', self.treeview_changed)


#endregion --------------------------------------------------------------------------------------

#region ---------------STEROWANIE-RAMIENIEM----------------------------------------------------------------------

        self.r_onbutton = Gtk.Button(label="Połącz z ramieniem")
        s_box3.pack_start(self.r_onbutton, False, True, 0)

        self.grid = Gtk.Grid()
        self.r_box = Gtk.Box()
        self.r_box.pack_start(self.grid, True, False, 0)
        s_box3.pack_start(self.r_box, True, False, 0)

        self.r_button1 = Gtk.Button(label="GÓRA")
        self.r_button2 = Gtk.Button(label="LEWO")
        self.r_button3 = Gtk.Button(label="PRAWO")
        self.r_button4 = Gtk.Button(label="DÓŁ")
        self.r_button5 = Gtk.Button(label="OBRÓT W LEWO")
        self.r_button6 = Gtk.Button(label="OBRÓT W PRAWO")
        self.r_button7 = Gtk.Button(label="ZACIŚNIĘCIE CHWYTAKA")
        self.r_button8 = Gtk.Button(label="POLUZOWANIE CHWYTAKA")

        self.grid.attach(self.r_button8, 0, 6, 1, 2)
        self.grid.attach(self.r_button7, 0, 4, 1, 2)
        self.grid.attach(self.r_button5, 4, 4, 1, 2)
        self.grid.attach(self.r_button6, 4, 6, 1, 2)

        self.grid.attach(self.r_button1, 2, 0, 1, 1)
        self.grid.attach(self.r_button2, 1, 1, 1, 1)
        self.grid.attach(self.r_button3, 3, 1, 1, 1)
        self.grid.attach(self.r_button4, 2, 2, 1, 1)


        self.r_save_button = Gtk.Button(label="Zapisz stan")
        s_box3.pack_start(self.r_save_button, False, True, 0)
        self.r_delete_button = Gtk.Button(label="Usuń")
        self.r_frame = Gtk.Frame(label="Zapisane stany")
        self.r_listbox = Gtk.ListBox()
        self.r_sc = Gtk.ScrolledWindow()
        self.r_sc.set_hexpand(True)
        self.r_sc.set_vexpand(True)
        self.r_sc.add(self.r_listbox)
        self.r_frame.add(self.r_sc)
        self.r_ibox = Gtk.Box(spacing=2)
        self.r_ibox.pack_start(self.r_frame, True, True, 0)
        self.r_ibox.pack_start(self.r_delete_button, False, False, 3)
        s_box3.pack_start(self.r_ibox, True, True, 0)

        self.r_onbutton.connect("clicked", self.on_connect_with_arm)
        self.r_button4.connect("pressed", self.on_r_button_pressed4)
        self.r_button4.connect("released", self.on_r_button_realeased)
        self.r_button1.connect("pressed", self.on_r_button_pressed)
        self.r_button1.connect("released", self.on_r_button_realeased)
        self.r_button2.connect("pressed", self.on_r_button_pressed2)
        self.r_button2.connect("released", self.on_r_button_realeased)
        self.r_button3.connect("pressed", self.on_r_button_pressed3)
        self.r_button3.connect("released", self.on_r_button_realeased)
        self.r_button5.connect("pressed", self.on_r_button_pressed5)
        self.r_button5.connect("released", self.on_r_button_realeased)
        self.r_button6.connect("pressed", self.on_r_button_pressed6)
        self.r_button6.connect("released", self.on_r_button_realeased)
        self.r_button7.connect("pressed", self.on_r_button_pressed7)
        self.r_button7.connect("released", self.on_r_button_realeased)
        self.r_button8.connect("pressed", self.on_r_button_pressed8)
        self.r_button8.connect("released", self.on_r_button_realeased)
        self.r_save_button.connect("clicked", self.on_r_save_button_clicked)
        self.r_delete_button.connect("clicked", self.on_r_delete_button_clicked)




#endregion ----------------------------------------------------------------------------------------------


        self.stan = False
        self.stan2 = False
        self.licznik = -1
        self.s_stan = False
        self.pressed_state = False
        self.s_stan2 = False
        self.servo_run = False
        self.r_row_count = 0
        self.r_step_list = []


#region-------ServoFUNC----------------------

    def on_r_save_button_clicked(self, widget):
        e = Gtk.ListBoxRow()
        b = Gtk.Box()
        b.pack_start(Gtk.Label(str(self.r_row_count)), True, True, 10)
        b.pack_start(Gtk.Label(str(self.servo.pos[0]) + '/' + str(self.servo.pos[1]) + '/' + str(self.servo.pos[2]) + '/' + str(self.servo.pos[3]) + '/' + str(self.servo.pos[4]) + '/' + str(self.servo.pos[5]) + '/' + str(self.servo.pos[6]) + '/' + str(self.servo.step_count)), True, True, 0)
        self.r_row_count += 1
        e.add(b)
        self.r_listbox.add(e)
        self.r_listbox.show_all()
        self.servo.step_list.append([self.servo.pos[0], self.servo.pos[1], self.servo.pos[2], self.servo.pos[3], self.servo.pos[4], self.servo.pos[5], self.servo.pos[6], self.servo.step_count])

    def on_r_delete_button_clicked(self, widget):
        index = self.r_listbox.get_selected_row()
        del self.r_step_list[index.get_index()]




    def on_connect_with_arm(self, widget):
        #   0. szczypce
        #   1. rotacja szczycami
        #   2. pierwszy czlon
        #   3. drugi czlon prawe serwo norm
        #   4. drugi czlon lewe serwo odw
        #   5. podstawa prawe serwo norm
        #   6. podstawa lewe odw

        #   27 - dir
        #   22 - step
        self.servo_run = not self.servo_run

        if self.servo_run:
            self.r_onbutton.set_label("Rozłącz ramię")
            self.servo = arm_controller.Arm_Controller()
        else:
            self.servo.stop()
            self.r_onbutton.set_label("Połącz z ramieniem")


    def on_r_button_realeased(self, widget):
        self.servo.pressed_state = False

    def on_r_button_pressed(self, widget):
        self.servo.pressed_state = True
        GLib.idle_add(self.servo.continous_func, 1)

    def on_r_button_pressed2(self, widget):
        self.servo.pressed_state = True
        GLib.idle_add(self.servo.continous_func, 2)

    def on_r_button_pressed3(self, widget):
        self.servo.pressed_state = True
        GLib.idle_add(self.servo.continous_func, 3)

    def on_r_button_pressed4(self, widget):
        self.servo.pressed_state = True
        GLib.idle_add(self.servo.continous_func, 4)

    def on_r_button_pressed5(self, widget):
        self.servo.pressed_state = True
        GLib.idle_add(self.servo.continous_func, 5)

    def on_r_button_pressed6(self, widget):
        self.servo.pressed_state = True
        GLib.idle_add(self.servo.continous_func, 6)

    def on_r_button_pressed7(self, widget):
        self.servo.pressed_state = True
        GLib.idle_add(self.servo.continous_func, 7)

    def on_r_button_pressed8(self, widget):
        self.servo.pressed_state = True
        GLib.idle_add(self.servo.continous_func, 8)


#endregion

#region---------BoardFUNC------------

    def treeview_changed(self, widget, event, data=None):
        adj = self.s_sc2.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())



    def on_setup_board(self, widget):
        self.ser.setup(s_lista_urzadzen)

        self.s_textbuffer1.insert_at_cursor("\nZaprogramowano płytkę")


    def on_run_board_clicked(self, widget):
        if self.s_stan2:
            self.s_stan = not self.s_stan
            if self.s_stan:
                self.s_button6.set_label("Zatrzymaj")
                GLib.idle_add(self.read_input)
                self.ser.send_command(s_lista_polecen)

            else:
                self.ser.stop()
                self.s_button6.set_label("Uruchom")



    def read_input(self):
        if not self.s_stan:
            return False
        if not self.ser.delay:
            inp = self.ser.proceed_input(s_lista_urzadzen)
            if inp != None:
                self.s_textbuffer1.insert_at_cursor(inp)
        return True




    def serial_switcher(self, widget):
        self.s_stan2 = not self.s_stan2
        if self.s_stan2:
            try:
                self.ser = wireless_board.Wireless_board()
                self.s_serial_switch.set_label("Rozłącz urządzenie")
                self.s_textbuffer1.insert_at_cursor("\nPołączono z urządzeniem")
            except:
                self.s_textbuffer1.insert_at_cursor("\nBłąd")

        else:
            self.s_serial_switch.set_label("Połącz z urządzeniem")
            self.s_textbuffer1.insert_at_cursor("\nRozłączono z urządzeniem")
            self.ser.stop()
            self.ser.close()





    def on_delete_board_activity(self, widget):
        index = s_listbox2.get_selected_row()
        del s_lista_polecen[index.get_index()]
        s_listbox2.remove(index)


    def on_add_board_activity(self, widget):
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)

        tree_iter = self.ICombo.get_active_iter()
        if tree_iter != None:
            model = self.ICombo.get_model()
            id1, name = model[tree_iter][:2]
        else:
            name = ""

        tree_iter = self.IICombo.get_active_iter()
        if tree_iter != None:
            model = self.IICombo.get_model()
            id2, name2 = model[tree_iter][:2]
        else:
            name2 = ""

        tree_iter = self.IIICombo.get_active_iter()
        if tree_iter != None:
            model = self.IIICombo.get_model()
            id3, name3 = model[tree_iter][:2]
        else:
            name3 = ""
            id3 = -1

        tree_iter = self.IVCombo.get_active_iter()
        if tree_iter != None:
            model = self.IVCombo.get_model()
            id4, name4 = model[tree_iter][:2]
        else:
            name4 = ""
            id4 = -1

        s_lista_polecen.append([id1, id2, id3, name4])

        hbox.pack_start(Gtk.Label("%s %s %s %s %s" % (name, " -> ", name2, name3, name4)), True, True, 0)
        row.add(hbox)
        s_listbox2.add(row)
        s_listbox2.show_all()

    def on_comboI_board_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]

        if int(row_id) == 0:
            self.IIList = Gtk.ListStore(int, str)
            for e in filter(lambda x: x[0] == 0, s_lista_urzadzen):
                self.IIList.append([e[1], e[2]])

        if int(row_id) == 1:
            self.IIList = Gtk.ListStore(int, str)
            for e in filter(lambda x: x[0] == 1, s_lista_urzadzen):
                #to nie jest uniwersalne, tylko na potrzeby prezentacji
                self.IIList.append([e[3], e[2]])
        if int(row_id) == 2:
            self.IIList = Gtk.ListStore(int, str)
            self.IIList.append([100, str(100)])
            for e in range(500, 5500, 500):
                self.IIList.append([e, str(e)])


        self.IICombo.set_model(model=self.IIList)
        self.IICombo.set_entry_text_column(1)
        self.IICombo.show_all()

    def on_comboII_board_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]

        if row_id == 9:
            self.IIIList = Gtk.ListStore(int, str)
            self.IIIList.append([0, "Jedź prosto"])
            self.IIIList.append([1, "Jedź w tył"])
            self.IIIList.append([2, "Zatrzymaj się"])
            self.IIIList.append([3, "Jedź w lewo"])
            self.IIIList.append([4, "Jedź w prawo"])
            self.IIICombo.set_model(model=self.IIIList)
            self.IIICombo.set_entry_text_column(1)
            self.IIICombo.show_all()




    def on_delete_device_board_clicked(self, widget):
        index = s_listbox1.get_selected_row().get_index()
        ancyf = -1
        if s_lista_urzadzen[index][0] == 0:
            for e in s_lista_czujnikow:
                if e[1] == s_lista_urzadzen[index][3]:
                    ancyf = e[0]
                    s_lista_czujnikow_buf.append(e)
                    break
        elif s_lista_urzadzen[index][0] == 1:
            for e in s_lista_wyjsc:
                if e[1] == s_lista_urzadzen[index][3]:
                    ancyf = e[0]
                    s_lista_wyjsc_buf.append(e)
                    break
        if ancyf == 0:
            for e in s_piny_cyfrowe:
                if e[0] == s_lista_urzadzen[index][1]:
                    s_piny_cyfrowe_buf.append(e)
        elif ancyf == 1:
            for e in s_piny_analogowe:
                if e[0] == s_lista_urzadzen[index][1]:
                    s_piny_analogowe_buf.append(e)
        del s_lista_urzadzen[index]

        s_listbox1.remove(s_listbox1.get_selected_row())



    def on_add_device_board_clicked(self, widget):
        dialog = AddDialog(self, 1)
        response = dialog.run()

        dialog.destroy()






#endregion

#region -----------------------------PanelSterowaniaFUNC-------------------------------

    def treeview_changed2(self, widget, event, data=None):
        adj = textview3.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    def control_Thread2(self):
        textbuffer3.insert_at_cursor(self.my_program.output)
        self.my_program.output = ""
        if self.stan2 == False or self.code.is_alive() == False:
            self.button2.set_label("Uruchom program użytkownika")
            self.stan2 = False
            textbuffer3.insert_at_cursor("\nZakończono działanie programu")
            return False
        else:
            return True

    def on_run_user_code_clicked(self, widget):
        if self.stan2 == False:
            self.licznik += 1
            file = open("Interpreted_code.py", "w")
            file.write("from time import sleep\ntry:\n\timport RPi.GPIO as GPIO\n\tGPIO.setmode(GPIO.BCM)\n\tGPIO.setwarnings(False)\nexcept:\n\tpass\n\nclass MyProgram():\n\tdef __init__(self):\n\t\tself.output = \"\"\n\t\tself.con = True\n\tdef code(self):\n")
            line = ""
            for e in self.textbuffer2.get_text(self.textbuffer2.get_start_iter(), self.textbuffer2.get_end_iter(),include_hidden_chars=True):
                if e == "\n":
                    line += e
                    file.write("\t\t" + line)
                    line = ""
                else:
                    line += e
            file.write("\t\t" + line)
            file.close()

            try:
                self.servo.stop()
                self.r_onbutton.set_label("Połącz z ramieniem")
            except:
                pass

            importlib.reload(CODE)
            self.my_program = CODE.MyProgram()
            self.code = threading.Thread(target=self.my_program.code, daemon=True)
            self.code.start()
            self.stan2 = True
            self.button2.set_label("Zatrzymaj program użytkownika")
            GLib.idle_add(self.control_Thread2)
        else:
            self.my_program.con = False
            self.stan2 = False
            try:
                GPIO.cleanup()
            except:
                pass
            self.button2.set_label("Uruchom program użytkownika")


    def on_load_clicked(self, widget):
        self.textbuffer2.set_text("")

        for e in lista_urzadzen:
            if e[3] == 5:
                self.textbuffer2.insert_at_cursor("Kanal_A" + " = " + "13" + "\n")
                self.textbuffer2.insert_at_cursor("Kanal_B" + " = " + "16" + "\n")
            elif e[3] == 4:
                self.textbuffer2.insert_at_cursor("Obrot_prawy" + " = " + "6" + "\n")
                self.textbuffer2.insert_at_cursor("Obrot_lewy" + " = " + "12" + "\n")
                self.textbuffer2.insert_at_cursor("licznik" + " = " + "0" + "\n")
            else:
                self.textbuffer2.insert_at_cursor(e[2] + " = " + str(e[1]) + "\n")

        for e in lista_urzadzen:
            if e[3] == 5:
                self.textbuffer2.insert_at_cursor("\nGPIO.setup(" + "Kanal_A" + ",GPIO.OUT)")
                self.textbuffer2.insert_at_cursor("\nGPIO.setup(" + "Kanal_B" + ",GPIO.OUT)")
                self.textbuffer2.insert_at_cursor("\nGPIO.output(" + "Kanal_B" + ",GPIO.LOW)")
                self.textbuffer2.insert_at_cursor("\nGPIO.output(" + "Kanal_A" + ",GPIO.LOW)")

            elif e[3] == 4:
                self.textbuffer2.insert_at_cursor("\nGPIO.setup(" + "Obrot_prawy" + ",GPIO.IN)")
                self.textbuffer2.insert_at_cursor("\nGPIO.setup(" + "Obrot_lewy" + ",GPIO.IN)")
            else:
                self.textbuffer2.insert_at_cursor("\nGPIO.setup(" + e[2] + ",")
                if e[0] == 0:
                    if e[3] == 9 or e[3] == 10 or e[3] == 11:
                        self.textbuffer2.insert_at_cursor("GPIO.IN, pull_up_down = GPIO.PUD_DOWN)")
                    else:
                        self.textbuffer2.insert_at_cursor("GPIO.IN)")
                else:
                    self.textbuffer2.insert_at_cursor("GPIO.OUT)")
                    self.textbuffer2.insert_at_cursor("\nGPIO.output(" + e[2] + ", GPIO.LOW)")


        self.textbuffer2.insert_at_cursor("\nwhile self.con:")

        for e in lista_polecen:
            if e[0] == 0:
                if e[1][1] == 4:
                    self.textbuffer2.insert_at_cursor("\n\tif GPIO.input(Obrot_prawy) == 1:\n\t\tlicznik += 1\n\tif GPIO.input(Obrot_lewy) == 1:\n\t\tlicznik -= 1")
                    self.textbuffer2.insert_at_cursor("\n\tself.output += \"\\nWartosc " + e[1][0] + " == \" + " + "str(licznik)")
                else:
                    self.textbuffer2.insert_at_cursor("\n\tself.output += \"\\nWartosc " + e[1][0] + " == " + "\"" + " + str(GPIO.input(" + e[1][0] + ")) + \"\\n\"")
            elif e[0] == 1:
                if e[1][1] == 5:
                    if e[2] == 0:
                        self.textbuffer2.insert_at_cursor("\n\tGPIO.output(" + "Kanal_A" + "," + "1" + ")")
                        self.textbuffer2.insert_at_cursor("\n\tGPIO.output(" + "Kanal_B" + "," + "0" + ")")
                    if e[2] == 1:
                        self.textbuffer2.insert_at_cursor("\n\tGPIO.output(" + "Kanal_A" + "," + "0" + ")")
                        self.textbuffer2.insert_at_cursor("\n\tGPIO.output(" + "Kanal_B" + "," + "1" + ")")
                else:
                    self.textbuffer2.insert_at_cursor("\n\tGPIO.output(" + e[1][0] + "," + str(e[2]) + ")")
            elif e[0] == 2:
                self.textbuffer2.insert_at_cursor("\n\tsleep(" + str(e[1][1]/1000) + ")")


        stack.set_visible_child_name("check2")



    def on_delete_activity_clicked(self, widget):
        index = list_box2.get_selected_row()
        del lista_polecen[index.get_index()]
        list_box2.remove(index)



    def on_add_activity(self, widget):
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)


        tree_iter = ICombo.get_active_iter()
        if tree_iter != None:
            model = ICombo.get_model()
            id1, name = model[tree_iter][:2]
        else:
            name = ""

        tree_iter = IICombo.get_active_iter()
        if tree_iter != None:
            model = IICombo.get_model()
            id2, name2 = model[tree_iter][:2]
        else:
            name2 = ""

        tree_iter = IIICombo.get_active_iter()
        if tree_iter != None:
            model = IIICombo.get_model()
            id3, name3 = model[tree_iter][:2]
        else:
            name3 = ""
            id3 = 0

        tree_iter = IVCombo.get_active_iter()
        if tree_iter != None:
            model = IVCombo.get_model()
            id4, name4 = model[tree_iter][:2]
        else:
            name4 = ""

        lista_polecen.append([id1, [name2, id2], id3, name4])

        hbox.pack_start(Gtk.Label("%s %s %s %s %s" % (name, " -> ", name2, name3, name4)), True, True, 0)
        row.add(hbox)
        list_box2.add(row)
        list_box2.show_all()

    def on_delete_row_button_clicked(self, widget):
        index = list_box.get_selected_row().get_index()
        ancyf = -1
        if lista_urzadzen[index][0] == 0:
            for e in lista_czujnikow:
                if e[1] == lista_urzadzen[index][3] or e[0] == lista_urzadzen[index][3]:
                    ancyf = e[0]
                    lista_czujnikow_buf.append(e)
                    break
        elif lista_urzadzen[index][0] == 1:
            for e in lista_wyjsc:
                if e[1] == lista_urzadzen[index][3] or e[0] == lista_urzadzen[index][3]:
                    ancyf = e[0]
                    lista_wyjsc_buf.append(e)
                    break
        if ancyf == 0:
              for e in piny_cyfrowe:
                  if e[0] == lista_urzadzen[index][1]:
                      piny_cyfrowe_buf.append(e)
        elif ancyf == 1:
              for e in piny_analogowe:
                  if e[0] == lista_urzadzen[index][1]:
                      piny_analogowe_buf.append(e)

        del lista_urzadzen[index]

        list_box.remove(list_box.get_selected_row())




    def on_add_device_clicked(self, widget):
        dialog = AddDialog(self, 0)
        response = dialog.run()

        dialog.destroy()


    def on_ICombo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]

        if int(row_id) == 0:
            IIList = Gtk.ListStore(int, str)
            for e in filter(lambda x: x[0] == 0, lista_urzadzen):
                if e[3] == 4 or e[3] == 9 or e[3] == 10 or e[3] == 11:
                    IIList.append([e[3], e[2]])
                else:
                    IIList.append([e[1], e[2]])

        if int(row_id) == 1:
            IIList = Gtk.ListStore(int, str)
            for e in filter(lambda x: x[0] == 1, lista_urzadzen):
                if e[3] == 5 or e[3] == 6 or e[3] == 7 or e[3] == 8:
                    IIList.append([e[3], e[2]])
                else:
                    IIList.append([e[1], e[2]])

        if int(row_id) == 2:
            IIList = Gtk.ListStore(int, str)
            IIList.append([100, str(100)])
            for e in range(500, 5500, 500):
                IIList.append([e, str(e)])

        IICombo.set_model(model=IIList)
        IICombo.set_entry_text_column(1)
        IICombo.show_all()

    def on_IICombo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]

        if int(row_id) == 5:
            IIIList = Gtk.ListStore(int, str)
            IIIList.append([0, "Obrót w prawo"])
            IIIList.append([1, "Obrót w lewo"])
            IIICombo.set_model(model=IIIList)
            IIICombo.set_entry_text_column(1)
            IIICombo.show_all()
        if int(row_id) == 6 or int(row_id) == 7 or int(row_id) == 8:
            IIIList = Gtk.ListStore(int, str)
            IIIList.append([1, "Włącz"])
            IIIList.append([0, "Wyłącz"])
            IIICombo.set_model(model=IIIList)
            IIICombo.set_entry_text_column(1)
            IIICombo.show_all()



    def on_IIICombo_changed(self, combo):
        pass

    def on_IVCombo_changed(self, combo):
        pass

    def interpretuj(self, word):
        for s in skladnia_poj:
            if s[0] == word:
                if s[0] == "Ramie":
                    z = str(s[1]) + "\nkroki = " + str(self.servo.step_list)
                    return z
                return s[1]
        return word

    def on_interpreter_click(self, widget):
        self.textbuffer2.set_text("")
        word = ""
        text = self.textbuffer.get_text(self.textbuffer.get_start_iter(), self.textbuffer.get_end_iter(), include_hidden_chars=True)
        text.rstrip()
        text.lstrip()
        licznik = 0
        for letter in text:
            if letter == "{":
                licznik += 1
            if letter == "}":
                licznik -= 1
                continue

            if letter != ")" and letter != "(" and letter != "{" and letter != "}" and letter != " " and letter != "\n" and letter != ";" and letter != "." and letter != "\t" and letter != "=" and letter != "+" and letter != "-" and letter != ">" and letter != "<":
                word += letter
            else:

                self.textbuffer2.insert_at_cursor(self.interpretuj(word))
                if letter != " " and letter != "\t" and letter != "\n":
                    self.textbuffer2.insert_at_cursor(self.interpretuj(letter))
                if word != "" and letter == " ":
                    self.textbuffer2.insert_at_cursor(" ")
                if letter == "\n":
                    self.textbuffer2.insert_at_cursor("\n")
                    for e in range(0, licznik):
                        self.textbuffer2.insert_at_cursor("\t")
                word = ""
        if word != "":
            self.textbuffer2.insert_at_cursor(self.interpretuj(word))
        stack.set_visible_child_name("check2")
    #endregion






win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
#destroy-event cza dodac
win.show_all()
Gtk.main()
