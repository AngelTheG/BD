import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class About(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Acerca del proyecto", transient_for=parent, flags=0)

        self.set_default_size(400, 100)
        self.set_border_width(5)

        # Labels
        lbl_projectName = Gtk.Label(justify=2)
        lbl_projectName.set_markup(("<span font_desc='Ubuntu 45'><b>EnfGen</b></span>\n"+
                                    "<span foreground='grey' font_desc='Ubuntu 8'>Base "+
                                    "de Datos de Enfermedades Genéticas</span>"))

        lbl_projectInfo = Gtk.Label()
        lbl_projectInfo.set_text("Este proyecto es básicamente una herramienta de fácil acceso "+
                                 "y modificación sencilla, para todo tipo de usuarios, "+
                                 "de una base de datos que posee información sobre enfermedades "+
                                 "genéticas y sus datos asociados.")
        lbl_projectInfo.set_line_wrap(True)

        lbl_projectAuthor = Gtk.Label(justify=2)
        author = "<b>Creado por</b>\nPatricia Fuentes\nAngel Guerrero\nJosefa Pinto"
        lbl_projectAuthor.set_markup(author)

        btn_authorPage = Gtk.Button(label="[⏣]  GitHub  [⏣]")
        btn_authorPage.connect("clicked", self.openGit)

        # Agregación
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(lbl_projectName,False, True, 20)
        box.pack_start(lbl_projectInfo,False, True, 5)
        box.pack_start(lbl_projectAuthor,False, True, 20)
        box.pack_end(btn_authorPage,False, True, 10)

        dialogBox = self.get_content_area()
        dialogBox.add(box)

        self.show_all()

    def openGit(self, widget):
        os.system("sensible-browser https://github.com/callmeDem/BD_Enfermedades_Geneticas/")