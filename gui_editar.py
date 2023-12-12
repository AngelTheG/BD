"""
El "main" de la interfaz
"""
import psycopg2
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class EditWindow(Gtk.Dialog):
    def __init__(self,parent):
        super().__init__(title=("Editar - "+parent.getBDName()), transient_for=parent)

        self.set_default_size(1080,720)
        self.set_border_width(10)

        # Parametros
        self.parent = parent
        
        """
        A continuación se encuentran las 3 entidades dinámicas
        accesibles por el usuario, estas son especiales ya que sus 
        datos se conforman por referencias de otras entidades
        """
        #<-- Enfermedad Genetica -->#
        lbl_enf = Gtk.Label()
        lbl_enf.set_xalign(0)
        lbl_enf.set_markup("<b><big>Enfermedades Genéticas</big></b>")
        btn_enf_add = Gtk.Button(label="+")
        
        box_lbl_enf = Gtk.Box()
        box_lbl_enf.pack_start(lbl_enf, False, True, 1)
        box_lbl_enf.pack_end(btn_enf_add, False, True, 1)

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

        box_enf = Gtk.Box(orientation=1,spacing=5)
        box_enf.add(box_lbl_enf)
        box_enf.add(scr_enf)

        #<-- Mutación -->#
        lbl_mut = Gtk.Label()
        lbl_mut.set_xalign(0)
        lbl_mut.set_markup("<b><big>Mutaciones</big></b>")
        btn_mut_add = Gtk.Button(label="+")
        
        box_lbl_mut = Gtk.Box()
        box_lbl_mut.pack_start(lbl_mut, False, True, 1)
        box_lbl_mut.pack_end(btn_mut_add, False, True, 1)

        self.lss_mut = Gtk.ListStore(str,   #HGVS
                                     int,   #Tipo
                                     str,   #Proteina
                                     str,   #Codon
                                     int)   #Codigo Gen
                                           
        
        trv_mut = Gtk.TreeView(model=self.lss_mut)

        for i, column_title in enumerate(["HGVS",
                                          "Tipo",
                                          "Proteina",
                                          "Codon",
                                          "Codigo Gen"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            trv_mut.append_column(column)

        scr_mut = Gtk.ScrolledWindow()
        scr_mut.set_vexpand(True)
        scr_mut.set_hexpand(True)
        scr_mut.add(trv_mut)

        box_mut = Gtk.Box(orientation=1,spacing=5)
        box_mut.add(box_lbl_mut)
        box_mut.add(scr_mut)

        #<-- AGE -->#
        lbl_age = Gtk.Label()
        lbl_age.set_xalign(0)
        lbl_age.set_markup("<b>Asociación Genetica de Enfermedad</b>")
        btn_age_add = Gtk.Button(label="+")
        
        box_lbl_age = Gtk.Box()
        box_lbl_age.pack_start(lbl_age, False, True, 1)
        box_lbl_age.pack_end(btn_age_add, False, True, 1)

        self.lss_age = Gtk.ListStore(int,   #ID
                                     str,   #Codigo Mutacion
                                     int)   #Codigo Enfermedad
        
        trv_age = Gtk.TreeView(model=self.lss_age)

        for i, column_title in enumerate(["ID",
                                          "Codigo Mutacion",
                                          "Codigo Enfermedad"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            trv_age.append_column(column)

        scr_age = Gtk.ScrolledWindow()
        scr_age.set_vexpand(True)
        scr_age.set_hexpand(True)
        scr_age.add(trv_age)

        box_age = Gtk.Box(orientation=1,spacing=5)
        box_age.add(box_lbl_age)
        box_age.add(scr_age)

        """
        A continuación se encuentran las 5 entidades planas
        accesibles por el usuario, estas son especiales ya que sus 
        datos se conforman únicamente por información plana, o sea
        sin referencias
        """
        #<-- Gen -->#
        lbl_gen = Gtk.Label()
        lbl_gen.set_xalign(0)
        lbl_gen.set_markup("<b>Gen</b>")
        btn_gen_add = Gtk.Button(label="+")
        
        box_lbl_gen = Gtk.Box()
        box_lbl_gen.pack_start(lbl_gen, False, True, 1)
        box_lbl_gen.pack_end(btn_gen_add, False, True, 1)

        self.lss_gen = Gtk.ListStore(str,   #Codigo Mutacion
                                     int)   #Codigo Enfermedad
        
        trv_gen = Gtk.TreeView(model=self.lss_gen)

        for i, column_title in enumerate(["Nombre",
                                          "N°MIM"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            trv_gen.append_column(column)

        scr_gen = Gtk.ScrolledWindow()
        scr_gen.set_vexpand(True)
        scr_gen.set_hexpand(True)
        scr_gen.add(trv_gen)

        box_gen = Gtk.Box(orientation=1,spacing=5)
        box_gen.add(box_lbl_gen)
        box_gen.add(scr_gen)

        #<-- Sintoma -->#
        lbl_sim = Gtk.Label()
        lbl_sim.set_xalign(0)
        lbl_sim.set_markup("<b><big>Síntoma</big></b>")
        btn_sim_add = Gtk.Button(label="+")
        
        box_lbl_sim = Gtk.Box()
        box_lbl_sim.pack_start(lbl_sim, False, True, 1)
        box_lbl_sim.pack_end(btn_sim_add, False, True, 1)

        self.lss_sim = Gtk.ListStore(int,   #ID
                                     str,   #Tratamiento
                                     str)   #Descripcion
        
        trv_sim = Gtk.TreeView(model=self.lss_sim)

        for i, column_title in enumerate(["ID",
                                          "Tratamiento",
                                          "Descripcion"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
            column.set_expand(True)
            trv_sim.append_column(column)

        scr_sim = Gtk.ScrolledWindow()
        scr_sim.set_vexpand(True)
        scr_sim.set_hexpand(True)
        scr_sim.add(trv_sim)

        box_sim = Gtk.Box(orientation=1,spacing=5)
        box_sim.add(box_lbl_sim)
        box_sim.add(scr_sim)

        #<-- Cigosidad -->#
        lbl_cig = Gtk.Label()
        lbl_cig.set_xalign(0)
        lbl_cig.set_markup("<b>Cigosidad</b>")
        btn_cig_add = Gtk.Button(label="+")
        
        box_lbl_cig = Gtk.Box()
        box_lbl_cig.pack_start(lbl_cig, False, True, 1)
        box_lbl_cig.pack_end(btn_cig_add, False, True, 1)

        self.lss_cig = Gtk.ListStore(int,   #Id
                                     str)   #Tipo
        
        trv_cig = Gtk.TreeView(model=self.lss_cig)

        for i, column_title in enumerate(["ID",
                                          "Tipo"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            trv_cig.append_column(column)

        scr_cig = Gtk.ScrolledWindow()
        scr_cig.set_vexpand(True)
        scr_cig.set_hexpand(True)
        scr_cig.add(trv_cig)

        box_cig = Gtk.Box(orientation=1,spacing=5)
        box_cig.add(box_lbl_cig)
        box_cig.add(scr_cig)
        
        #<-- Tipo de Mutación -->#
        lbl_tmt = Gtk.Label()
        lbl_tmt.set_xalign(0)
        lbl_tmt.set_markup("<b>Tipo de Mutación</b>")
        btn_tmt_add = Gtk.Button(label="+")
        
        box_lbl_tmt = Gtk.Box()
        box_lbl_tmt.pack_start(lbl_tmt, False, True, 1)
        box_lbl_tmt.pack_end(btn_tmt_add, False, True, 1)

        self.lss_tmt = Gtk.ListStore(int,   #ID
                                     str)   #Tipo
        
        trv_tmt = Gtk.TreeView(model=self.lss_tmt)

        for i, column_title in enumerate(["ID",
                                          "Tipo"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            trv_tmt.append_column(column)

        scr_tmt = Gtk.ScrolledWindow()
        scr_tmt.set_vexpand(True)
        scr_tmt.set_hexpand(True)
        scr_tmt.add(trv_tmt)

        box_tmt = Gtk.Box(orientation=1,spacing=5)
        box_tmt.add(box_lbl_tmt)
        box_tmt.add(scr_tmt)

        #<-- Origen -->#
        lbl_ori = Gtk.Label()
        lbl_ori.set_xalign(0)
        lbl_ori.set_markup("<b>Origen</b>")
        btn_ori_add = Gtk.Button(label="+")
        
        box_lbl_ori = Gtk.Box()
        box_lbl_ori.pack_start(lbl_ori, False, True, 1)
        box_lbl_ori.pack_end(btn_ori_add, False, True, 1)

        self.lss_ori = Gtk.ListStore(int,   #ID
                                     str)   #Tipo
        
        trv_ori = Gtk.TreeView(model=self.lss_ori)

        for i, column_title in enumerate(["ID",
                                          "Tipo"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            trv_ori.append_column(column)

        scr_ori = Gtk.ScrolledWindow()
        scr_ori.set_vexpand(True)
        scr_ori.set_hexpand(True)
        scr_ori.add(trv_ori)

        box_ori = Gtk.Box(orientation=1,spacing=5)
        box_ori.add(box_lbl_ori)
        box_ori.add(scr_ori)

        # Contenedores
        left_box = Gtk.Box(orientation=1,spacing=20)
        left_box.add(box_enf)
        left_box.add(box_mut)
        left_box.add(box_sim)

        right_a_box= Gtk.Box(orientation=1,spacing=15)
        right_a_box.add(box_age)
        right_a_box.add(box_gen)

        right_b_box= Gtk.Box(orientation=1,spacing=10)
        right_b_box.add(box_cig)
        right_b_box.add(box_tmt)
        right_b_box.add(box_ori)


        right_box= Gtk.Box(spacing=20)
        right_box.add(right_a_box)
        right_box.add(right_b_box)


        main_box = Gtk.Box(spacing=25)
        main_box.add(left_box)
        main_box.add(right_box)

        box_dialog = self.get_content_area()
        box_dialog.add(main_box)

        # Cargar datos antes de desplegar la ventana
        self.loadData()
        self.show_all()

    #Cargar los datos de la base de datos en los treeview
    def loadData(self):
        conexion = psycopg2.connect(
            user="enfgen",
            password="enfgen1",
            host="localhost",
            port=5432,
            database="bd_enfgen"
        )

        tablas = [
            "enfermedad_genetica",
            "mutacion",
            "sintoma",
            "asociacion_genetica_de_enfermedad",
            "gen",
            "cigosidad",
            "tipo_mutacion",
            "origen"
        ]
        
        lss = [
            self.lss_enf,
            self.lss_mut,
            self.lss_sim,
            self.lss_age,
            self.lss_gen,
            self.lss_cig,
            self.lss_tmt,
            self.lss_ori
        ]

        for i,tabla in enumerate(tablas):
            lss[i].clear()
            consulta = ("SELECT * FROM "+tabla)
            cursor = conexion.cursor()
            cursor.execute(consulta)
            rows = cursor.fetchall()
            for row in rows:
                lss[i].append(row)
                
        cursor.close()
        conexion.close()

    def get_ultimo_id(self, tabla):
        conexion = psycopg2.connect(
            user="enfgen",
            password="enfgen1",
            host="localhost",
            port=5432,
            database="bd_enfgen"
        )

        consulta = f"SELECT COUNT(*) FROM {tabla}"

        cursor = conexion.cursor()
        cursor.execute(consulta)
        ultimo_id = cursor.fetchone()[0]

        cursor.close()
        conexion.close()

        return ultimo_id


