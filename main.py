import os
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk

from gui_about import About
from gui_editar import EditWindow
from gui_busqueda import SearchWindow

class Core(Gtk.Window):
    """
    Creación de la ventana núcleo del programa
    """
    def __init__(self):
        super().__init__()
        self.set_default_size(1080,720)
        self.set_border_width(10)
        self.set_resizable(False)

        # === Contrucción de la Interfaz === #
        # Boton - About
        btn_about_icono = Gtk.Image.new_from_icon_name("system-users", Gtk.IconSize.MENU)
        btn_about = Gtk.Button()
        btn_about.set_image(btn_about_icono)
        btn_about.connect('clicked', self.about)

        # Boton - Cargar Base de Datos
        btn_dato_cargar = Gtk.Button(label='Cargar')
        btn_dato_cargar.connect('clicked', self.cargar)

        # Boton de Menu - Base de Datos
        btn_editar_icono = Gtk.Image.new_from_icon_name("applications-engineering", Gtk.IconSize.MENU)
        btn_editar = Gtk.Button()
        btn_editar.connect('clicked',self.editar)
        btn_editar.set_image(btn_editar_icono)

        # HeaderBar
        self.filename = 'EnfGen v.11.12.23'
        self.header = Gtk.HeaderBar(title= "EnfGen")
        self.header.set_subtitle(("Base de Datos: "+self.filename))
        self.header.props.show_close_button = True

        """
        Corresponde a una opción que se agregará con el tiempo...
        #self.header.pack_start(btn_dato_cargar)
        """
        
        self.header.pack_start(btn_editar)
        self.header.pack_end(btn_about)

        self.set_titlebar(self.header)

        # Label - Título del proyecto
        lbl_titulo_proyecto = Gtk.Label(justify=2)
        lbl_titulo_proyecto.set_markup(("<span font_desc='Ubuntu 80'><b>EnfGen</b></span>\n"+
                                        "<span foreground='grey' font_desc='Ubuntu 15'>Base "+
                                        "de Datos de Enfermedades Genéticas</span>"))
        #lbl_subtitulo_proyecto = Gtk.Label()
        #lbl_subtitulo_proyecto.set_markup()

        # SearchEntry - Barra de Búsqueda
        self.ent_busqueda = Gtk.SearchEntry()
        self.ent_busqueda.set_placeholder_text('Busca por palabras clave')
        self.ent_busqueda.connect('activate',self.Busqueda)

        # Buton - Busqueda Avanzada
        lbl_busqueda_avanzada = Gtk.Label()
        lbl_busqueda_avanzada.set_markup("<span foreground='yellow'>Búsqueda avanzada</span>")
        box_busqueda_avanzada = Gtk.Box()
        box_busqueda_avanzada.pack_start(lbl_busqueda_avanzada,True,True,0)
        btn_busqueda_avanzada = Gtk.Button()
        btn_busqueda_avanzada.add(box_busqueda_avanzada)

        # Label - Información
        self.lbl_estado = Gtk.Label()
        self.lbl_estado.set_markup("<span foreground='grey'>Hola, recuerda pasarte por el repositorio de la app :)</span>")

        # Box - Contenedor Vertical Principal
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.pack_start(lbl_titulo_proyecto, False, True, 120)
        main_box.pack_start(self.ent_busqueda, False, True, 10)
        #main_box.pack_start(btn_busqueda_avanzada, False, False, 10)
        main_box.pack_end(self.lbl_estado, False, True, 10)

        self.add(main_box)

    # === Funciones dentro de la Aplicación === #

    # Obtener el nombre de la base de datos
    def getBDName(self):
        return self.filename

    # Establecer nuevo estado de la app
    def estado(self,color=0,info_estado="test"):
        """
        Colores:
        [0 - Gris (Defecto)]
        [1 - Azul]
        [2 - Verde]
        [3 - Rojo]
        [4 - Amarillo]
        [5 - Rosado]
        """
        # Asigna un color al mensaje de estado
        if color == 0:
            estado_color = 'grey'
        if color == 1:
            estado_color = 'cornflowerblue'
        if color == 2:
            estado_color = 'limegreen'
        if color == 3:
            estado_color = 'tomato'
        if color == 4:
            estado_color = 'gold'
        if color == 5:
            estado_color = 'hotpink'
        
        nuevo_estado = "<span foreground='" + estado_color + "'>" + info_estado + "</span>"
        self.lbl_estado.set_markup(nuevo_estado)


    # Check de compatibilidad del archivo
    def esComptaible(self,file):
        for index,line in enumerate(file):
            if index == 0:
                if "#forg" in line:
                    return True
                else:
                    return False

    # Abrir un archivo nuevo de base de datos
    def cargar(self, widget):
        self.estado(0,"Cargando una base de datos nueva")
        fileDialog = Gtk.FileChooserDialog(title="Seleccion de archivo de base de datos",
                                            parent=self,
                                            action=Gtk.FileChooserAction.OPEN)
            
        fileDialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        # Filtro de archivos
        filter_txt = Gtk.FileFilter()
        filter_txt.set_name("Archivo separado por comas(.csv)")
        filter_txt.add_pattern("*csv")

        fileDialog.add_filter(filter_txt)

        response = fileDialog.run()
        if response == Gtk.ResponseType.OK:
            # Almacenamiento del archivo en una varible
            file = open(fileDialog.get_filename(), "r+")
            filename_raw = (fileDialog.get_filename().split("/"))[-1]

            # Procesado del archivo
            if self.esComptaible(file):
                self.filename = filename_raw
                # Contenedor de datos
                file_data = []

                for index,line in enumerate(file):
                    if index != 0:
                        line_text = line.replace("\n","")
                        file_data.append(line_text)

                # Guardado de nombre en el subtítulo
                self.header.set_subtitle(("Base de Datos : " + self.filename))
                self.estado(2,("¡Base de Datos <b>" + self.filename + "</b> cargada exitosamente!"))

            else:
                self.estado(3,"El archivo <b>" + filename_raw + "</b> no es compatible")

            fileDialog.destroy()
        else:
            self.estado(5,"Operación <b>CARGA DE BASE DE DATOS</b> cancelada por el usuario")
            fileDialog.destroy()

    # Editar la base de datos
    def editar(self,widget):
        self.estado(5,("Modificando <b>"+self.filename+"</b>"))
        edicion = EditWindow(self)
        edicion.run()
        edicion.destroy()

    # Iniciar la Búsqueda
    def Busqueda(self,widget):
        objetivo = self.ent_busqueda.get_text().upper()
        self.estado(4,("Iniciando la búsqueda de <b>"+objetivo+"</b>"))
        ventana_busqueda = SearchWindow(self,objetivo)
        ventana_busqueda.run()
        ventana_busqueda.destroy()
        pass

    def modificar(self):
        if "modificado" in self.filename:
            pass
        else:
            self.filename = self.filename + " - modificado"
        self.header.set_subtitle(self.filename)

    # Abrir el dialogo about
    def about(self,widget):
        if self.ent_busqueda.get_text() == "forg":
            self.forg()
        else:
            config = About(self)
            config.run()
            config.destroy()

    def forg(self):
        os.system("sensible-browser https://i.imgur.com/Bs2Z5np.jpeg")

# Ejecución principal
main = Core()
main.connect("destroy", Gtk.main_quit)
main.show_all()
Gtk.main()
