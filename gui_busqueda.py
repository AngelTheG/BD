import gi
import psycopg2

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class SearchWindow(Gtk.Dialog):
    def __init__(self,parent,target):
        super().__init__(title=(f"Resultados de la búsqueda - {target}"), transient_for=parent)

        #self.set_default_size(720., 480)
        self.set_default_size(1080,720)
        self.set_border_width(10)

        self.ent_busqueda = Gtk.SearchEntry()
        self.ent_busqueda.set_text(target)
        self.ent_busqueda.set_placeholder_text('Busca por palabras clave')
        self.ent_busqueda.connect('activate',self.widget_buscar)
        self.objetivo = self.ent_busqueda.get_text().upper()
        

        self.lss_enf = Gtk.ListStore(int,    #ID
                                     int,    #N_MIM
                                     str,    #GENBANK
                                     str,    #NOMBRE
                                     int,    #COD_ORIGEN
                                     int)    #COD_CIGOSIDAD
        
        trv_enf = Gtk.TreeView(model=self.lss_enf)

        for i, column_title in enumerate(["ID",
                                          "N°MIM",
                                          "ID GenBank",
                                          "Nombre",
                                          "Origen",
                                          "Cigosidad"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            trv_enf.append_column(column)

        scr_enf = Gtk.ScrolledWindow()
        scr_enf.set_vexpand(True)
        scr_enf.set_hexpand(True)
        scr_enf.add(trv_enf)

        box_main = Gtk.Box(orientation=1,spacing=5)
        box_main.add(self.ent_busqueda)
        box_main.add(scr_enf)

        box_dialog = self.get_content_area()
        box_dialog.add(box_main)

        self.buscar()

        self.show_all()

    ####    Funciones de la Interfaz    ####
    #Buscar
    def buscar(self):
        self.lss_enf.clear()
        self.ent_busqueda.set_text(self.objetivo)
        
        columnas = [
            "id",
            "n°mim",
            "n°genbank",
            "nombre",
            "cod_origen",
            "cod_cigosidad"
        ]

        conexion = psycopg2.connect(
            user="enfgen",
            password="enfgen1",
            host="localhost",
            port=5432,
            database="bd_enfgen"
        )

        white_list = [2,3]
        for index,columna in enumerate(columnas):
            if index in white_list:
                consulta = (f"SELECT * FROM enfermedad_genetica where {columna} like '%{self.objetivo}%'")
                cursor = conexion.cursor()
                cursor.execute(consulta)
                rows = cursor.fetchall()
                for row in rows:
                    self.lss_enf.append(row)
            
                
        cursor.close()
        conexion.close()

    def widget_buscar(self,widget):
        self.objetivo = self.ent_busqueda.get_text().upper()
        self.buscar()