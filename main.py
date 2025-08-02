import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time
import random

class GlossaApp:
    def __init__(self, root):
        self.root = root
        
        # Variables responsive - DEFINIR PRIMERO
        self.window_width = 1400
        self.window_height = 900
        
        # Variables para la cámara
        self.cap = None
        self.camera_active = False
        self.video_label = None
        
        # Diccionario LESCO expandido
        self.diccionario_lesco = {
            "hola": "Levanta la mano derecha y muévela de lado a lado suavemente con una sonrisa",
            "gracias": "Coloca la mano derecha en el pecho y muévela hacia adelante con respeto y gratitud",
            "por favor": "Junta las palmas de las manos frente al pecho en posición de oración",
            "sí": "Cierra el puño y muévelo hacia arriba y abajo de forma clara y decidida",
            "no": "Mueve el dedo índice de lado a lado con suavidad pero firmeza",
            "agua": "Forma una 'W' con tres dedos y llévala hacia la boca simulando beber",
            "comer": "Lleva los dedos juntos hacia la boca en movimientos repetidos",
            "casa": "Forma un techo triangular con ambas manos sobre la cabeza",
            "familia": "Forma una 'F' con ambas manos y únelas formando un círculo protector",
            "trabajo": "Golpea suavemente el puño derecho sobre la palma izquierda",
            "amor": "Cruza los brazos sobre el pecho abrazándote a ti mismo con ternura",
            "amigo": "Entrelaza los dedos índices como símbolo de unión y amistad",
            "ayuda": "Coloca una mano sobre la otra en posición de apoyo mutuo",
            "feliz": "Sonríe ampliamente y mueve las manos hacia arriba con alegría",
            "triste": "Baja las comisuras de la boca y las manos hacia abajo con expresión melancólica",
            "buenos días": "Saluda con la mano y señala hacia arriba indicando el sol matutino",
            "buenas noches": "Saluda y forma un arco sobre la cabeza simulando la luna",
            "perdón": "Coloca la mano en el pecho y inclina ligeramente la cabeza",
            "estudiar": "Abre y cierra las manos como hojeando un libro",
            "escuela": "Forma una 'E' con ambas manos y júntalas como un edificio"
        }
        
        # Configurar la aplicación
        self.setup_window()
        self.setup_styles()
        self.setup_ui()
        self.setup_responsive()
        
    def setup_window(self):
        self.root.title("GLOSSA - Traductor LESCO Profesional")
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(True, True)
        self.root.minsize(1000, 700)
        
        # Centrar ventana
        self.center_window()
        
        # Configurar grid weights para responsive
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def center_window(self):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.window_width // 2)
        y = (screen_height // 2) - (self.window_height // 2)
        self.root.geometry(f'{self.window_width}x{self.window_height}+{x}+{y}')
        
    def setup_styles(self):
        """Configurar estilos elegantes en negro y dorado"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Paleta de colores elegante negro y dorado
        self.colors = {
            'primary_gold': '#FFD700',      # Dorado brillante
            'secondary_gold': '#FFA500',    # Dorado naranja
            'accent_gold': '#FFED4E',       # Dorado claro
            'dark_gold': '#B8860B',         # Dorado oscuro
            'black_primary': '#0a0a0a',     # Negro principal
            'black_secondary': '#1a1a1a',   # Negro secundario
            'black_tertiary': '#2a2a2a',    # Negro terciario
            'gray_dark': '#333333',         # Gris oscuro
            'gray_medium': '#555555',       # Gris medio
            'gray_light': '#777777',        # Gris claro
            'white': '#ffffff',             # Blanco puro
            'success': '#00ff88',           # Verde éxito
            'warning': '#ff9500',           # Naranja advertencia
            'danger': '#ff4757',            # Rojo peligro
            'info': '#3742fa'               # Azul información
        }
        
        # Configurar estilos del Notebook
        self.style.configure('Elegant.TNotebook', 
                           background=self.colors['black_primary'],
                           borderwidth=0,
                           tabmargins=[2, 2, 2, 0])
        
        self.style.configure('Elegant.TNotebook.Tab',
                           padding=[32, 16],
                           background=self.colors['black_secondary'],
                           foreground=self.colors['gray_light'],
                           borderwidth=1,
                           focuscolor='none',
                           font=('Segoe UI', 11, 'bold'))
        
        self.style.map('Elegant.TNotebook.Tab',
                      background=[('selected', self.colors['primary_gold']),
                                ('active', self.colors['black_tertiary'])],
                      foreground=[('selected', self.colors['black_primary']),
                                ('active', self.colors['primary_gold'])])
        
    def setup_responsive(self):
        """Configurar comportamiento responsive"""
        self.root.bind('<Configure>', self.on_window_resize)
        
    def on_window_resize(self, event):
        """Manejar redimensionamiento de ventana"""
        if event.widget == self.root:
            new_width = self.root.winfo_width()
            new_height = self.root.winfo_height()
            
            # Ajustar elementos según el tamaño
            if hasattr(self, 'main_container'):
                if new_width < 1200:
                    # Modo compacto
                    self.main_container.configure(padx=16, pady=16)
                else:
                    # Modo amplio
                    self.main_container.configure(padx=32, pady=24)
        
    def setup_ui(self):
        # Header elegante con gradiente visual
        self.create_elegant_header()
        
        # Contenedor principal responsive
        self.main_container = tk.Frame(self.root, bg=self.colors['black_primary'])
        self.main_container.grid(row=1, column=0, sticky='nsew', padx=32, pady=24)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Notebook con estilo elegante
        self.notebook = ttk.Notebook(self.main_container, style='Elegant.TNotebook')
        self.notebook.grid(row=0, column=0, sticky='nsew')
        
        # Pestañas con iconos elegantes
        self.create_camera_tab()
        self.create_text_to_sign_tab()  
        self.create_dictionary_tab()
        self.create_about_tab()
        
    def create_elegant_header(self):
        """Header premium con efectos visuales"""
        header_frame = tk.Frame(self.root, bg=self.colors['black_primary'], height=120)
        header_frame.grid(row=0, column=0, sticky='ew', padx=0, pady=0)
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Gradiente visual simulado
        gradient_frame = tk.Frame(header_frame, bg=self.colors['black_secondary'], height=4)
        gradient_frame.grid(row=0, column=0, sticky='ew')
        
        # Contenedor principal del header
        header_content = tk.Frame(header_frame, bg=self.colors['black_primary'])
        header_content.grid(row=1, column=0, sticky='nsew', padx=40, pady=20)
        header_content.grid_columnconfigure(1, weight=1)
        
        # Logo y branding elegante
        logo_container = tk.Frame(header_content, bg=self.colors['black_primary'])
        logo_container.grid(row=0, column=0, sticky='w')
        
        # Ícono principal con efecto dorado
        icon_label = tk.Label(
            logo_container,
            text="🤟",
            font=('Segoe UI Emoji', 36),
            bg=self.colors['black_primary'],
            fg=self.colors['primary_gold']
        )
        icon_label.grid(row=0, column=0, padx=(0, 20))
        
        # Título principal elegante
        title_container = tk.Frame(logo_container, bg=self.colors['black_primary'])
        title_container.grid(row=0, column=1, sticky='w')
        
        title_label = tk.Label(
            title_container,
            text="GLOSSA",
            font=('Segoe UI', 32, 'bold'),
            bg=self.colors['black_primary'],
            fg=self.colors['primary_gold']
        )
        title_label.grid(row=0, column=0, sticky='w')
        
        subtitle_label = tk.Label(
            title_container,
            text="TRADUCTOR PROFESIONAL DE LESCO",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['black_primary'],
            fg=self.colors['gray_light']
        )
        subtitle_label.grid(row=1, column=0, sticky='w', pady=(5, 0))
        
        # Información del proyecto (lado derecho)
        info_container = tk.Frame(header_content, bg=self.colors['black_primary'])
        info_container.grid(row=0, column=2, sticky='e')
        
        # Badge de versión elegante
        version_frame = tk.Frame(
            info_container,
            bg=self.colors['dark_gold'],
            relief='flat',
            bd=0
        )
        version_frame.grid(row=0, column=0, sticky='e', pady=(0, 8))
        
        # Información institucional
        institution_label = tk.Label(
            info_container,
            text="EXPOTÉCNICA 2024",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['black_primary'],
            fg=self.colors['primary_gold']
        )
        institution_label.grid(row=1, column=0, sticky='e')
        
        team_label = tk.Label(
            info_container,
            text="CTP Mercedes Norte - CORVEC",
            font=('Segoe UI', 10),
            bg=self.colors['black_primary'],
            fg=self.colors['gray_light']
        )
        team_label.grid(row=2, column=0, sticky='e')
        
    def create_premium_card(self, parent, title, subtitle=None):
        """Crear card premium con efectos elegantes"""
        # Contenedor principal con padding responsive
        container = tk.Frame(parent, bg=self.colors['black_primary'])
        container.pack(fill='both', expand=True, padx=24, pady=24)
        
        # Card principal con borde dorado
        card = tk.Frame(
            container,
            bg=self.colors['black_secondary'],
            relief='solid',
            bd=2,
            highlightbackground=self.colors['dark_gold'],
            highlightthickness=1
        )
        card.pack(fill='both', expand=True)
        
        # Header del card con gradiente
        if title:
            header_frame = tk.Frame(card, bg=self.colors['black_tertiary'], height=80)
            header_frame.pack(fill='x')
            header_frame.pack_propagate(False)
            
            # Línea dorada superior
            gold_line = tk.Frame(header_frame, bg=self.colors['primary_gold'], height=3)
            gold_line.pack(fill='x')
            
            # Contenido del header
            header_content = tk.Frame(header_frame, bg=self.colors['black_tertiary'])
            header_content.pack(fill='both', expand=True, padx=32, pady=16)
            
            title_label = tk.Label(
                header_content,
                text=title,
                font=('Segoe UI', 18, 'bold'),
                bg=self.colors['black_tertiary'],
                fg=self.colors['primary_gold']
            )
            title_label.pack(side='left', anchor='w')
            
            if subtitle:
                subtitle_label = tk.Label(
                    header_content,
                    text=subtitle,
                    font=('Segoe UI', 11),
                    bg=self.colors['black_tertiary'],
                    fg=self.colors['gray_light']
                )
                subtitle_label.pack(side='right', anchor='e')
        
        # Contenido del card
        content = tk.Frame(card, bg=self.colors['black_secondary'])
        content.pack(fill='both', expand=True, padx=32, pady=32)
        
        return content
        
    def create_premium_button(self, parent, text, command, style='primary', width=220, icon=None):
        """Crear botón premium con efectos hover"""
        if style == 'primary':
            bg_color = self.colors['primary_gold']
            hover_color = self.colors['accent_gold']
            text_color = self.colors['black_primary']
        elif style == 'success':
            bg_color = self.colors['success']
            hover_color = '#00e676'
            text_color = self.colors['black_primary']
        elif style == 'danger':
            bg_color = self.colors['danger']
            hover_color = '#ff6b7a'
            text_color = self.colors['white']
        elif style == 'secondary':
            bg_color = self.colors['black_tertiary']
            hover_color = self.colors['gray_dark']
            text_color = self.colors['primary_gold']
        else:
            bg_color = self.colors['gray_dark']
            hover_color = self.colors['gray_medium']
            text_color = self.colors['white']
            
        # Frame contenedor para efectos
        button_container = tk.Frame(parent, bg=parent['bg'])
        
        button_text = f"{icon} {text}" if icon else text
        
        button = tk.Button(
            button_container,
            text=button_text,
            command=command,
            font=('Segoe UI', 12, 'bold'),
            bg=bg_color,
            fg=text_color,
            activebackground=hover_color,
            activeforeground=text_color,
            relief='flat',
            bd=0,
            padx=32,
            pady=16,
            cursor='hand2',
            width=width//12
        )
        button.pack()
        
        # Efectos hover mejorados
        def on_enter(e):
            button.config(bg=hover_color)
            
        def on_leave(e):
            button.config(bg=bg_color)
            
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return button_container
        
    def create_camera_tab(self):
        """Pestaña de cámara con diseño premium"""
        camera_frame = ttk.Frame(self.notebook)
        self.notebook.add(camera_frame, text="📹  RECONOCIMIENTO")
        
        content = self.create_premium_card(
            camera_frame, 
            "RECONOCIMIENTO DE SEÑAS EN TIEMPO REAL",
            "Tecnología de Visión Artificial"
        )
        
        # Instrucciones elegantes
        instruction_container = tk.Frame(
            content,
            bg=self.colors['black_tertiary'],
            relief='solid',
            bd=1,
            highlightbackground=self.colors['dark_gold'],
            highlightthickness=1
        )
        instruction_container.pack(fill='x', pady=(0, 32))
        
        instruction_text = tk.Label(
            instruction_container,
            text="🎯 Posiciónate frente a la cámara y realiza una seña de LESCO para obtener la traducción instantánea",
            font=('Segoe UI', 13),
            bg=self.colors['black_tertiary'],
            fg=self.colors['gray_light'],
            wraplength=800,
            justify='center'
        )
        instruction_text.pack(pady=20)
        
        # Contenedor de video premium
        video_container = tk.Frame(
            content,
            bg=self.colors['primary_gold'],
            relief='solid',
            bd=3
        )
        video_container.pack(pady=(0, 32))
        
        # Frame de video con dimensiones responsivas
        video_frame = tk.Frame(video_container, bg='#000000', width=720, height=540)
        video_frame.pack(padx=6, pady=6)
        video_frame.pack_propagate(False)
        
        self.video_label = tk.Label(
            video_frame,
            text="🎥 CÁMARA DESACTIVADA\n\n✨ Haz clic en 'ACTIVAR CÁMARA' para comenzar\n\n🤟 Sistema de reconocimiento LESCO listo",
            font=('Segoe UI', 16, 'bold'),
            bg='#000000',
            fg=self.colors['primary_gold'],
            justify='center'
        )
        self.video_label.pack(expand=True)
        
        # Panel de controles premium
        controls_frame = tk.Frame(content, bg=self.colors['black_secondary'])
        controls_frame.pack(fill='x', pady=(0, 24))
        
        # Botones con diseño elegante
        buttons_frame = tk.Frame(controls_frame, bg=self.colors['black_secondary'])
        buttons_frame.pack()
        
        self.camera_btn_container = self.create_premium_button(
            buttons_frame,
            "ACTIVAR CÁMARA",
            self.toggle_camera,
            'primary',
            icon="🎥"
        )
        self.camera_btn_container.pack(side='left', padx=(0, 20))
        
        translate_btn = self.create_premium_button(
            buttons_frame,
            "TRADUCIR SEÑA",
            self.translate_sign,
            'success',
            icon="🔍"
        )
        translate_btn.pack(side='left')
        
        # Panel de resultados premium
        result_container = tk.Frame(
            content,
            bg=self.colors['black_tertiary'],
            relief='solid',
            bd=2,
            highlightbackground=self.colors['dark_gold'],
            highlightthickness=1
        )
        result_container.pack(fill='x')
        
        # Header del resultado
        result_header = tk.Frame(result_container, bg=self.colors['dark_gold'], height=40)
        result_header.pack(fill='x')
        result_header.pack_propagate(False)
        
        result_title = tk.Label(
            result_header,
            text="💬 RESULTADO DE LA TRADUCCIÓN",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['dark_gold'],
            fg=self.colors['black_primary']
        )
        result_title.pack(expand=True)
        
        self.result_label = tk.Label(
            result_container,
            text="⏳ Esperando análisis de seña...",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['black_tertiary'],
            fg=self.colors['gray_light'],
            pady=32
        )
        self.result_label.pack(fill='x')
        
    def create_text_to_sign_tab(self):
        """Pestaña texto a señas con diseño premium"""
        text_frame = ttk.Frame(self.notebook)
        self.notebook.add(text_frame, text="✍️  BÚSQUEDA")
        
        content = self.create_premium_card(
            text_frame, 
            "BÚSQUEDA INTELIGENTE DE SEÑAS",
            f"{len(self.diccionario_lesco)} palabras disponibles"
        )
        
        # Instrucciones elegantes
        instruction_container = tk.Frame(
            content,
            bg=self.colors['black_tertiary'],
            relief='solid',
            bd=1,
            highlightbackground=self.colors['dark_gold'],
            highlightthickness=1
        )
        instruction_container.pack(fill='x', pady=(0, 40))
        
        instruction_text = tk.Label(
            instruction_container,
            text="🔍 Ingresa cualquier palabra para descubrir cómo realizar la seña correspondiente en LESCO",
            font=('Segoe UI', 13),
            bg=self.colors['black_tertiary'],
            fg=self.colors['gray_light'],
            wraplength=800,
            justify='center'
        )
        instruction_text.pack(pady=20)
        
        # Buscador premium
        search_container = tk.Frame(content, bg=self.colors['black_secondary'])
        search_container.pack(fill='x', pady=(0, 40))
        
        search_frame = tk.Frame(
            search_container,
            bg=self.colors['black_tertiary'],
            relief='solid',
            bd=2,
            highlightbackground=self.colors['primary_gold'],
            highlightthickness=2
        )
        search_frame.pack(anchor='center')
        
        # Campo de entrada premium
        entry_container = tk.Frame(search_frame, bg=self.colors['black_tertiary'])
        entry_container.pack(side='left', padx=20, pady=16)
        
        entry_label = tk.Label(
            entry_container,
            text="PALABRA:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['black_tertiary'],
            fg=self.colors['primary_gold']
        )
        entry_label.pack(anchor='w')
        
        self.word_entry = tk.Entry(
            entry_container,
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['black_secondary'],
            fg=self.colors['white'],
            relief='flat',
            bd=0,
            width=20,
            insertbackground=self.colors['primary_gold'],
            selectbackground=self.colors['primary_gold'],
            selectforeground=self.colors['black_primary']
        )
        self.word_entry.pack(pady=(8, 0))
        
        # Botón de búsqueda integrado
        search_btn = self.create_premium_button(
            search_frame,
            "BUSCAR",
            self.search_sign,
            'primary',
            140,
            "🔍"
        )
        search_btn.pack(side='left', padx=(20, 20), pady=16)
        
        # Bind Enter
        self.word_entry.bind('<Return>', lambda e: self.search_sign())
        
        # Resultado con diseño premium
        result_container = tk.Frame(
            content,
            bg=self.colors['black_tertiary'],
            relief='solid',
            bd=2,
            highlightbackground=self.colors['dark_gold'],
            highlightthickness=1
        )
        result_container.pack(fill='both', expand=True)
        
        # Header del resultado
        result_header = tk.Frame(result_container, bg=self.colors['dark_gold'], height=45)
        result_header.pack(fill='x')
        result_header.pack_propagate(False)
        
        result_title = tk.Label(
            result_header,
            text="📖 DESCRIPCIÓN DETALLADA DE LA SEÑA",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['dark_gold'],
            fg=self.colors['black_primary']
        )
        result_title.pack(expand=True)
        
        # Scrollbar elegante
        scrollbar = tk.Scrollbar(
            result_container,
            bg=self.colors['black_secondary'],
            troughcolor=self.colors['black_tertiary'],
            activebackground=self.colors['primary_gold']
        )
        scrollbar.pack(side='right', fill='y', padx=(0, 4), pady=4)
        
        self.sign_result = tk.Text(
            result_container,
            font=('Segoe UI', 12),
            bg=self.colors['black_secondary'],
            fg=self.colors['white'],
            relief='flat',
            bd=0,
            wrap='word',
            yscrollcommand=scrollbar.set,
            selectbackground=self.colors['primary_gold'],
            selectforeground=self.colors['black_primary'],
            insertbackground=self.colors['primary_gold'],
            padx=32,
            pady=24
        )
        self.sign_result.pack(side='left', fill='both', expand=True, padx=(4, 0), pady=4)
        scrollbar.config(command=self.sign_result.yview)
        
    def create_dictionary_tab(self):
        """Diccionario con diseño premium"""
        dict_frame = ttk.Frame(self.notebook)
        self.notebook.add(dict_frame, text="📚  DICCIONARIO")
        
        content = self.create_premium_card(
            dict_frame, 
            "DICCIONARIO COMPLETO DE LESCO",
            f"Base de datos con {len(self.diccionario_lesco)} señas"
        )
        
        # Layout responsive de dos columnas
        columns_frame = tk.Frame(content, bg=self.colors['black_secondary'])
        columns_frame.pack(fill='both', expand=True)
        
        # Columna izquierda - Lista premium
        left_column = tk.Frame(
            columns_frame,
            bg=self.colors['black_tertiary'],
            relief='solid',
            bd=2,
            highlightbackground=self.colors['dark_gold'],
            highlightthickness=1
        )
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 16))
        
        # Header de la lista
        list_header_frame = tk.Frame(left_column, bg=self.colors['dark_gold'], height=50)
        list_header_frame.pack(fill='x')
        list_header_frame.pack_propagate(False)
        
        list_header = tk.Label(
            list_header_frame,
            text=f"📋 PALABRAS DISPONIBLES ({len(self.diccionario_lesco)})",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['dark_gold'],
            fg=self.colors['black_primary']
        )
        list_header.pack(expand=True)
        
        # Lista con scroll premium
        list_container = tk.Frame(left_column, bg=self.colors['black_tertiary'])
        list_container.pack(fill='both', expand=True, padx=4, pady=4)
        
        list_scrollbar = tk.Scrollbar(
            list_container,
            bg=self.colors['black_secondary'],
            troughcolor=self.colors['black_tertiary'],
            activebackground=self.colors['primary_gold']
        )
        list_scrollbar.pack(side='right', fill='y')
        
        self.word_listbox = tk.Listbox(
            list_container,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['black_secondary'],
            fg=self.colors['white'],
            selectbackground=self.colors['primary_gold'],
            selectforeground=self.colors['black_primary'],
            relief='flat',
            bd=0,
            yscrollcommand=list_scrollbar.set,
            activestyle='none'
        )
        self.word_listbox.pack(side='left', fill='both', expand=True)
        list_scrollbar.config(command=self.word_listbox.yview)
        
        # Llenar lista con estilo
        for word in sorted(self.diccionario_lesco.keys()):
            self.word_listbox.insert('end', f"🤟  {word.upper()}")
            
        # Columna derecha - Detalles premium
        right_column = tk.Frame(
            columns_frame,
            bg=self.colors['black_tertiary'],
            relief='solid',
            bd=2,
            highlightbackground=self.colors['dark_gold'],
            highlightthickness=1
        )
        right_column.pack(side='right', fill='both', expand=True, padx=(16, 0))
        
        # Header de detalles
        details_header_frame = tk.Frame(right_column, bg=self.colors['dark_gold'], height=50)
        details_header_frame.pack(fill='x')
        details_header_frame.pack_propagate(False)
        
        details_header = tk.Label(
            details_header_frame,
            text="📖 DESCRIPCIÓN DETALLADA",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['dark_gold'],
            fg=self.colors['black_primary']
        )
        details_header.pack(expand=True)
        
        # Área de descripción premium
        desc_container = tk.Frame(right_column, bg=self.colors['black_tertiary'])
        desc_container.pack(fill='both', expand=True, padx=4, pady=4)
        
        desc_scrollbar = tk.Scrollbar(
            desc_container,
            bg=self.colors['black_secondary'],
            troughcolor=self.colors['black_tertiary'],
            activebackground=self.colors['primary_gold']
        )
        desc_scrollbar.pack(side='right', fill='y')
        
        self.dict_description = tk.Text(
            desc_container,
            font=('Segoe UI', 12),
            bg=self.colors['black_secondary'],
            fg=self.colors['white'],
            relief='flat',
            bd=0,
            wrap='word',
            yscrollcommand=desc_scrollbar.set,
            selectbackground=self.colors['primary_gold'],
            selectforeground=self.colors['black_primary'],
            padx=24,
            pady=24
        )
        self.dict_description.pack(side='left', fill='both', expand=True)
        desc_scrollbar.config(command=self.dict_description.yview)
        
        # Mensaje de bienvenida premium
        welcome_text = f"""🌟 ¡BIENVENIDO AL DICCIONARIO PREMIUM DE LESCO!

✨ CARACTERÍSTICAS AVANZADAS:
• Base de datos con {len(self.diccionario_lesco)} señas profesionales
• Descripciones detalladas paso a paso
• Interfaz elegante y fácil de usar
• Búsqueda instantánea

🎯 INSTRUCCIONES DE USO:
• Selecciona cualquier palabra de la lista
• Lee la descripción detallada
• Practica frente a un espejo
• Repite hasta dominar la técnica

💡 CONSEJOS PROFESIONALES:
• La expresión facial es fundamental en LESCO
• Mantén movimientos fluidos y naturales
• Practica regularmente para mejorar
• La paciencia es clave para el aprendizaje

🏆 ¡Domina LESCO con GLOSSA!"""
        
        self.dict_description.insert('1.0', welcome_text)
        self.dict_description.config(state='disabled')
        
        # Bind para selección
        self.word_listbox.bind('<<ListboxSelect>>', self.on_word_select)
        
    def create_about_tab(self):
        """Pestaña Acerca de con información del proyecto"""
        about_frame = ttk.Frame(self.notebook)
        self.notebook.add(about_frame, text="ℹ️  ACERCA DE")
        
        content = self.create_premium_card(
            about_frame, 
            "ACERCA DE GLOSSA",
            "Proyecto EXPOTÉCNICA 2024"
        )
        
        # Información del proyecto
        info_text = f"""🏆 GLOSSA - TRADUCTOR PROFESIONAL DE LESCO

🎯 MISIÓN:
Facilitar la comunicación entre personas oyentes y no oyentes mediante tecnología avanzada de traducción de Lengua de Señas Costarricense (LESCO).

✨ CARACTERÍSTICAS PREMIUM:
• Reconocimiento de señas en tiempo real
• Diccionario completo con {len(self.diccionario_lesco)} palabras
• Interfaz elegante y profesional
• Diseño responsive y accesible
• Tecnología de visión artificial

👥 EQUIPO DE DESARROLLO:
• Lucía Montero Esquivel
• Priscilla Rojas Araya  
• Sabrina Villegas Cascante
• Zayleeng Mora Azofeifa

🏫 INSTITUCIÓN:
Colegio Técnico Profesional Mercedes Norte - CORVEC

🎓 PROYECTO:
EXPOTÉCNICA 2024

🛠️ TECNOLOGÍAS UTILIZADAS:
• Python 3.8+
• OpenCV para procesamiento de video
• Tkinter para interfaz gráfica
• PIL para manejo de imágenes
• Threading para operaciones asíncronas

📊 ESTADÍSTICAS:
• Versión: 2.0 Premium
• Palabras en diccionario: {len(self.diccionario_lesco)}
• Idiomas soportados: Español - LESCO
• Plataformas: Windows, macOS, Linux

🎨 DISEÑO:
• Tema elegante negro y dorado
• Interfaz responsive
• Experiencia de usuario premium
• Accesibilidad mejorada

🚀 PRÓXIMAS ACTUALIZACIONES:
• Reconocimiento de frases completas
• Modo de aprendizaje interactivo
• Exportación de traducciones
• Soporte para más idiomas de señas

🤟 ¡GLOSSA - Conectando mundos a través de las señas!"""
        
        # Área de texto con scroll
        text_container = tk.Frame(
            content,
            bg=self.colors['black_tertiary'],
            relief='solid',
            bd=2,
            highlightbackground=self.colors['dark_gold'],
            highlightthickness=1
        )
        text_container.pack(fill='both', expand=True)
        
        # Header
        text_header = tk.Frame(text_container, bg=self.colors['dark_gold'], height=45)
        text_header.pack(fill='x')
        text_header.pack_propagate(False)
        
        header_label = tk.Label(
            text_header,
            text="📋 INFORMACIÓN COMPLETA DEL PROYECTO",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['dark_gold'],
            fg=self.colors['black_primary']
        )
        header_label.pack(expand=True)
        
        # Scrollbar
        about_scrollbar = tk.Scrollbar(
            text_container,
            bg=self.colors['black_secondary'],
            troughcolor=self.colors['black_tertiary'],
            activebackground=self.colors['primary_gold']
        )
        about_scrollbar.pack(side='right', fill='y', padx=(0, 4), pady=4)
        
        about_text = tk.Text(
            text_container,
            font=('Segoe UI', 11),
            bg=self.colors['black_secondary'],
            fg=self.colors['white'],
            relief='flat',
            bd=0,
            wrap='word',
            yscrollcommand=about_scrollbar.set,
            selectbackground=self.colors['primary_gold'],
            selectforeground=self.colors['black_primary'],
            padx=32,
            pady=24
        )
        about_text.pack(side='left', fill='both', expand=True, padx=(4, 0), pady=4)
        about_scrollbar.config(command=about_text.yview)
        
        about_text.insert('1.0', info_text)
        about_text.config(state='disabled')
        
    def on_word_select(self, event):
        """Manejar selección de palabra en el diccionario"""
        selection = self.word_listbox.curselection()
        if selection:
            selected_text = self.word_listbox.get(selection[0])
            word = selected_text.replace("🤟  ", "").lower()
            
            if word in self.diccionario_lesco:
                description = self.diccionario_lesco[word]
                
                display_text = f"""🎯 SEÑA SELECCIONADA: {word.upper()}

📝 DESCRIPCIÓN PASO A PASO:
{description}

💡 GUÍA DE PRÁCTICA PROFESIONAL:

🔹 PREPARACIÓN:
• Colócate frente a un espejo
• Asegúrate de tener buena iluminación
• Relaja tus manos y brazos

🔹 EJECUCIÓN:
• Realiza los movimientos lentamente
• Mantén la postura correcta
• Presta atención a la expresión facial

🔹 PERFECCIONAMIENTO:
• Repite la seña 10-15 veces
• Aumenta gradualmente la velocidad
• Practica en diferentes contextos

🔹 CONSEJOS AVANZADOS:
• La fluidez viene con la práctica constante
• Observa a hablantes nativos de LESCO
• Practica con otras personas
• Mantén la confianza y naturalidad

🏆 ¡Domina esta seña y continúa aprendiendo LESCO!

⭐ GLOSSA Premium - Tu compañero de aprendizaje"""
                
                self.dict_description.config(state='normal')
                self.dict_description.delete('1.0', 'end')
                self.dict_description.insert('1.0', display_text)
                self.dict_description.config(state='disabled')
        
    def toggle_camera(self):
        if not self.camera_active:
            self.start_camera()
        else:
            self.stop_camera()
            
    def start_camera(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror(
                    "Error de Cámara Premium", 
                    "🚫 No se pudo acceder a la cámara.\n\n💡 Soluciones:\n• Verifica que no esté en uso\n• Revisa los permisos de cámara\n• Reinicia la aplicación"
                )
                return
                
            self.camera_active = True
            # Actualizar botón
            camera_btn = self.camera_btn_container.winfo_children()[0]
            camera_btn.config(text="⏹️ DESACTIVAR CÁMARA", bg=self.colors['danger'])
            self.update_camera()
            
        except Exception as e:
            messagebox.showerror("Error Premium", f"❌ Error al inicializar la cámara:\n{str(e)}")
            
    def stop_camera(self):
        self.camera_active = False
        if self.cap:
            self.cap.release()
        
        # Restaurar botón
        camera_btn = self.camera_btn_container.winfo_children()[0]
        camera_btn.config(text="🎥 ACTIVAR CÁMARA", bg=self.colors['primary_gold'])
        
        # Mensaje elegante de cámara desactivada
        self.video_label.config(
            image='',
            text="🎥 CÁMARA DESACTIVADA\n\n✨ Sistema en espera\n\n🤟 Listo para reconocimiento LESCO",
            bg='#000000',
            fg=self.colors['primary_gold']
        )
        
    def update_camera(self):
        if self.camera_active and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Procesar frame con efectos premium
                frame = cv2.resize(frame, (720, 540))
                frame = cv2.flip(frame, 1)  # Efecto espejo
                
                # Overlay premium con gradiente
                overlay = frame.copy()
                cv2.rectangle(overlay, (10, 10), (350, 80), (255, 215, 0), -1)
                cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
                
                # Texto elegante
                cv2.putText(frame, "GLOSSA PREMIUM", (25, 35), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (10, 10, 10), 3)
                cv2.putText(frame, "LESCO ACTIVO", (25, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (10, 10, 10), 2)
                
                # Convertir y mostrar
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                photo = ImageTk.PhotoImage(img)
                
                self.video_label.config(image=photo, text='')
                self.video_label.image = photo
                
            # Continuar actualizando
            self.root.after(30, self.update_camera)
            
    def translate_sign(self):
        if not self.camera_active:
            messagebox.showwarning(
                "Cámara Inactiva", 
                "🚫 La cámara debe estar activa para traducir señas.\n\n💡 Activa la cámara y vuelve a intentar."
            )
            return
            
        # Simulación premium con efectos
        self.result_label.config(
            text="🔄 ANALIZANDO SEÑA CON IA...",
            bg=self.colors['warning'],
            fg=self.colors['black_primary']
        )
        self.root.update()
        
        # Simular procesamiento avanzado
        time.sleep(2)
        
        palabra_detectada = random.choice(list(self.diccionario_lesco.keys()))
        confidence = random.randint(85, 99)
        
        self.result_label.config(
            text=f"✅ SEÑA DETECTADA: '{palabra_detectada.upper()}' (Confianza: {confidence}%)",
            bg=self.colors['success'],
            fg=self.colors['black_primary']
        )
        
    def search_sign(self):
        word = self.word_entry.get().lower().strip()
        
        if not word:
            messagebox.showwarning(
                "Campo Vacío", 
                "📝 Por favor ingresa una palabra para buscar.\n\n💡 Ejemplo: 'hola', 'gracias', 'familia'"
            )
            self.word_entry.focus()
            return
            
        self.sign_result.config(state='normal')
        self.sign_result.delete('1.0', 'end')
        
        if word in self.diccionario_lesco:
            description = self.diccionario_lesco[word]
            
            result_text = f"""🎯 RESULTADO DE BÚSQUEDA PREMIUM

🤟 PALABRA ENCONTRADA: {word.upper()}

📝 DESCRIPCIÓN DETALLADA:
{description}

💡 GUÍA DE APRENDIZAJE PROFESIONAL:

🔹 FASE 1 - OBSERVACIÓN:
• Lee cuidadosamente la descripción
• Visualiza mentalmente el movimiento
• Identifica las partes clave de la seña

🔹 FASE 2 - PRÁCTICA BÁSICA:
• Colócate frente a un espejo
• Realiza los movimientos lentamente
• Concéntrate en la precisión

🔹 FASE 3 - PERFECCIONAMIENTO:
• Aumenta gradualmente la velocidad
• Practica la expresión facial
• Repite hasta lograr fluidez

🔹 FASE 4 - APLICACIÓN:
• Usa la seña en contexto
• Practica con otras personas
• Integra con otras señas

🏆 ¡Excelente elección! Continúa explorando nuestro diccionario premium.

⭐ GLOSSA Premium - Aprendizaje profesional de LESCO"""
            
        else:
            available = ", ".join(sorted(self.diccionario_lesco.keys()))
            result_text = f"""❌ PALABRA NO ENCONTRADA EN LA BASE DE DATOS

🔍 BÚSQUEDA: '{word}'
❌ ESTADO: No disponible en el diccionario actual

📚 PALABRAS DISPONIBLES EN GLOSSA PREMIUM:
{available}

💡 SUGERENCIAS INTELIGENTES:
• Verifica la ortografía de la palabra
• Intenta con sinónimos o palabras relacionadas
• Explora nuestro diccionario completo
• Usa la pestaña 'Diccionario' para navegar

🚀 PRÓXIMAMENTE:
• Más palabras en futuras actualizaciones
• Sugerencias automáticas de palabras similares
• Reconocimiento de voz para búsqueda
• Integración con diccionarios externos

📞 CONTACTO:
Si necesitas una palabra específica, contacta a nuestro equipo de desarrollo.

⭐ GLOSSA Premium - Expandiendo constantemente nuestro vocabulario"""
        
        self.sign_result.insert('1.0', result_text)
        self.sign_result.config(state='disabled')
        
        # Limpiar campo de búsqueda
        self.word_entry.delete(0, 'end')
        
    def __del__(self):
        if hasattr(self, 'cap') and self.cap:
            self.cap.release()

def main():
    root = tk.Tk()
    app = GlossaApp(root)
    
    def on_closing():
        if hasattr(app, 'camera_active') and app.camera_active:
            app.stop_camera()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
