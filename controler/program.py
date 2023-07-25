import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

skladnia_poj = [
    ["jesli", "if"],
    ["inaczej", "else"],
    ["dla", "for"],
    ["w", "in"],
    ["zakres", "range"],
    ["rob", ""],
    ["prawda", "True"],
    ["falsz", "False"],
    ["wlacz", "HIGH"],
    ["wylacz", "LOW"],
    ["nieskonczonosc", "True"],
    ["dopoki", "while"],
    ["nie", "not"],
    ["reszta", "%"],
    ["{", ":"],
    ["}", ""],
    ["\n", ""],
]

textview = Gtk.TextView()
textbuffer = textview.get_buffer()
textview2 = Gtk.TextView()
textbuffer2 = textview2.get_buffer()


def interpretuj(word):
    for s in skladnia_poj:
        if s[0] == word:
            return s[1]
    return word


class TextViewWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Program_kropka_egze")

        self.set_default_size(400, 350)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.create_textview()

        self.create_buttons()

    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, 2, 1)

        textbuffer.set_text("dopoki nieskonczonosc{\ncos\njesli wart == prawda{\ncos\ncos\ncos\n}\ncos\n}")

        scrolledwindow.add(textview)

        scrolledwindow2 = Gtk.ScrolledWindow()
        scrolledwindow2.set_hexpand(True)
        scrolledwindow2.set_vexpand(True)
        self.grid.attach_next_to(scrolledwindow2, scrolledwindow, Gtk.PositionType.RIGHT, 5, 1)

        scrolledwindow2.add(textview2)

    def create_buttons(self):
        textview.set_wrap_mode(Gtk.WrapMode.WORD)
        textview2.set_wrap_mode(Gtk.WrapMode.WORD)

        check_editable = Gtk.CheckButton("Editable")
        check_editable.set_active(True)
        check_editable.connect("toggled", self.on_editable_toggled)
        self.grid.attach(check_editable, 0, 2, 1, 1)

        check_cursor = Gtk.CheckButton("Cursor Visible")
        check_cursor.set_active(True)
        check_editable.connect("toggled", self.on_cursor_toggled)
        self.grid.attach_next_to(check_cursor, check_editable,
                                 Gtk.PositionType.RIGHT, 1, 1)

        button = Gtk.Button(label="Interpretuj")
        button.connect("clicked", self.on_interpreter_click)
        self.grid.attach_next_to(button, check_cursor, Gtk.PositionType.RIGHT, 1, 2)

    def on_interpreter_click(self, widget):
        textbuffer2.set_text("")
        word = ""
        text = textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter(), include_hidden_chars=True)
        text.rstrip()
        text.lstrip()
        licznik = 0;
        for letter in text:
            if letter == "{":
                licznik += 1
            if letter == "}":
                licznik -= 1
                continue

            if letter != ")" and letter != "(" and letter != "{" and letter != "}" and letter != " " and letter != "\n" and letter != ";" and letter != "\t" and letter != "=" and letter != "+" and letter != "-" and letter != ">" and letter != "<":
                word += letter
            else:

                textbuffer2.insert_at_cursor(interpretuj(word))
                if letter != " " and letter != "\t" and letter != "\n":
                    textbuffer2.insert_at_cursor(interpretuj(letter))
                if word != "" and letter == " ":
                    textbuffer2.insert_at_cursor(" ")
                if letter == "\n":
                    textbuffer2.insert_at_cursor("\n")
                    for e in range(0, licznik):
                        textbuffer2.insert_at_cursor("\t")
                word = ""

    def on_editable_toggled(self, widget):
        textview.set_editable(widget.get_active())

    def on_cursor_toggled(self, widget):
        textview.set_cursor_visible(widget.get_active())


win = TextViewWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()