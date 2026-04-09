# cosmos_ui.py - Graphical user interface (Tkinter)
# All user-facing text is in Spanish. All code identifiers are in English.

import tkinter as tk
from tkinter import ttk, messagebox, font
from stellar_core import StellarCore
from models import Vortex


# ── Color palette ─────────────────────────────────────────────────────────────

DEEP_SPACE   = "#0B0F1A"   # main background
COSMOS_DARK  = "#111827"   # panel background
NEBULA_CARD  = "#1C2333"   # card / frame background
STAR_WHITE   = "#E8EDF7"   # primary text
MOON_GREY    = "#8B9BB4"   # secondary text
AURORA_CYAN  = "#38BDF8"   # accent / highlight
PULSAR_PINK  = "#F472B6"   # action accent
ORBIT_GREEN  = "#34D399"   # success / completed
COMET_AMBER  = "#FBBF24"   # warning / pending
VOID_RED     = "#F87171"   # danger / delete
BORDER_LINE  = "#2A3450"   # subtle border


# ── Fonts (resolved at runtime) ───────────────────────────────────────────────

def make_fonts():
    return {
        "title":    ("Courier New", 20, "bold"),
        "heading":  ("Courier New", 13, "bold"),
        "subhead":  ("Courier New", 11, "bold"),
        "body":     ("Courier New", 10),
        "small":    ("Courier New",  9),
        "mono":     ("Courier New", 10),
        "badge":    ("Courier New",  8, "bold"),
    }


# ─────────────────────────────────────────────────────────────────────────────
# CosmosUI — Main application window
# ─────────────────────────────────────────────────────────────────────────────

class CosmosUI:
    """
    Main GUI class. Builds and manages all screens of the veterinary system.
    Uses a sidebar navigation pattern with frame swapping.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.core = StellarCore()
        self.fonts = make_fonts()
        self._configure_root()
        self._build_layout()
        self._show_dashboard()

    # ── Window setup ──────────────────────────────────────────

    def _configure_root(self):
        self.root.title("🌌 AstroVet — Sistema Veterinario")
        self.root.geometry("1180x720")
        self.root.minsize(1000, 650)
        self.root.configure(bg=DEEP_SPACE)
        self.root.resizable(True, True)

    # ── Layout skeleton ───────────────────────────────────────

    def _build_layout(self):
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._build_sidebar()

        # Main content area
        self.content_frame = tk.Frame(self.root, bg=DEEP_SPACE)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=16, pady=16)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

        self.active_frame = None

    def _build_sidebar(self):
        sidebar = tk.Frame(self.root, bg=COSMOS_DARK, width=220)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        # Logo / brand
        logo_frame = tk.Frame(sidebar, bg=COSMOS_DARK)
        logo_frame.pack(pady=(28, 8), padx=16, fill="x")

        tk.Label(logo_frame, text="✦ ASTROVET", font=self.fonts["title"],
                 bg=COSMOS_DARK, fg=AURORA_CYAN).pack(anchor="w")
        tk.Label(logo_frame, text="Clínica Veterinaria Espacial",
                 font=self.fonts["small"], bg=COSMOS_DARK, fg=MOON_GREY).pack(anchor="w")

        tk.Frame(sidebar, bg=BORDER_LINE, height=1).pack(fill="x", pady=16, padx=12)

        # Navigation buttons
        nav_items = [
            ("◎  Panel Principal",   self._show_dashboard),
            ("◈  Pacientes",         self._show_patients),
            ("⊕  Nuevo Paciente",    self._show_register_patient),
            ("◷  Citas",             self._show_appointments),
            ("⊞  Nueva Cita",        self._show_schedule_appointment),
            ("≋  Estructura Lista",  self._show_list_structure),
        ]

        self.nav_buttons = []
        for label, command in nav_items:
            btn = tk.Button(
                sidebar, text=label, font=self.fonts["body"],
                bg=COSMOS_DARK, fg=STAR_WHITE,
                activebackground=NEBULA_CARD, activeforeground=AURORA_CYAN,
                relief="flat", anchor="w", padx=20, pady=10,
                cursor="hand2", command=command
            )
            btn.pack(fill="x", pady=1)
            self.nav_buttons.append(btn)

        # Bottom info
        tk.Frame(sidebar, bg=BORDER_LINE, height=1).pack(
            fill="x", pady=16, padx=12, side="bottom")
        tk.Label(sidebar, text="Lista Doblemente Enlazada\nPOO · Python 3",
                 font=self.fonts["small"], bg=COSMOS_DARK,
                 fg=MOON_GREY, justify="left").pack(
            side="bottom", padx=16, pady=12, anchor="w")

    # ── Frame switching ───────────────────────────────────────

    def _switch_frame(self, builder_fn):
        if self.active_frame:
            self.active_frame.destroy()
        self.active_frame = tk.Frame(self.content_frame, bg=DEEP_SPACE)
        self.active_frame.grid(row=0, column=0, sticky="nsew")
        self.active_frame.columnconfigure(0, weight=1)
        self.active_frame.rowconfigure(1, weight=1)
        builder_fn(self.active_frame)

    # ── Helpers ───────────────────────────────────────────────

    def _section_title(self, parent, text, subtitle=""):
        header = tk.Frame(parent, bg=DEEP_SPACE)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        tk.Label(header, text=text, font=self.fonts["heading"],
                 bg=DEEP_SPACE, fg=AURORA_CYAN).pack(anchor="w")
        if subtitle:
            tk.Label(header, text=subtitle, font=self.fonts["small"],
                     bg=DEEP_SPACE, fg=MOON_GREY).pack(anchor="w")

    def _card(self, parent, row=0, col=0, colspan=1, rowspan=1):
        frame = tk.Frame(parent, bg=NEBULA_CARD,
                         highlightbackground=BORDER_LINE, highlightthickness=1)
        frame.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan,
                   sticky="nsew", padx=6, pady=6)
        return frame

    def _label_value(self, parent, label, value, row):
        tk.Label(parent, text=label, font=self.fonts["small"],
                 bg=NEBULA_CARD, fg=MOON_GREY).grid(
            row=row, column=0, sticky="w", padx=14, pady=3)
        tk.Label(parent, text=value, font=self.fonts["body"],
                 bg=NEBULA_CARD, fg=STAR_WHITE).grid(
            row=row, column=1, sticky="w", padx=14, pady=3)

    def _input_field(self, parent, label, row, default=""):
        tk.Label(parent, text=label, font=self.fonts["small"],
                 bg=NEBULA_CARD, fg=MOON_GREY).grid(
            row=row, column=0, sticky="w", padx=14, pady=5)
        var = tk.StringVar(value=default)
        entry = tk.Entry(parent, textvariable=var, font=self.fonts["body"],
                         bg=COSMOS_DARK, fg=STAR_WHITE, insertbackground=AURORA_CYAN,
                         relief="flat", highlightbackground=BORDER_LINE,
                         highlightthickness=1, width=28)
        entry.grid(row=row, column=1, sticky="ew", padx=14, pady=5)
        return var

    def _accent_button(self, parent, text, command, color=AURORA_CYAN):
        return tk.Button(
            parent, text=text, font=self.fonts["subhead"],
            bg=color, fg=DEEP_SPACE,
            activebackground=STAR_WHITE, activeforeground=DEEP_SPACE,
            relief="flat", padx=16, pady=8, cursor="hand2", command=command
        )

    def _build_tree(self, parent, columns, headings, row=0, col=0, colspan=1):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Space.Treeview",
                        background=NEBULA_CARD, foreground=STAR_WHITE,
                        fieldbackground=NEBULA_CARD, rowheight=30,
                        font=("Courier New", 9))
        style.configure("Space.Treeview.Heading",
                        background=COSMOS_DARK, foreground=AURORA_CYAN,
                        font=("Courier New", 9, "bold"), relief="flat")
        style.map("Space.Treeview",
                  background=[("selected", BORDER_LINE)],
                  foreground=[("selected", AURORA_CYAN)])

        wrapper = tk.Frame(parent, bg=NEBULA_CARD)
        wrapper.grid(row=row, column=col, columnspan=colspan,
                     sticky="nsew", padx=6, pady=6)
        wrapper.columnconfigure(0, weight=1)
        wrapper.rowconfigure(0, weight=1)

        tree = ttk.Treeview(wrapper, columns=columns, show="headings",
                            style="Space.Treeview")
        for col_id, heading in zip(columns, headings):
            tree.heading(col_id, text=heading)
            tree.column(col_id, width=130, anchor="w")

        vsb = ttk.Scrollbar(wrapper, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        return tree, wrapper

    # ─────────────────────────────────────────────────────────
    # SCREENS
    # ─────────────────────────────────────────────────────────

    # ── Dashboard ─────────────────────────────────────────────

    def _show_dashboard(self):
        def build(frame):
            self._section_title(frame, "✦ Panel Principal",
                                "Bienvenido al sistema AstroVet")
            body = tk.Frame(frame, bg=DEEP_SPACE)
            body.grid(row=1, column=0, sticky="nsew")
            body.columnconfigure((0, 1, 2), weight=1)

            info = self.core.get_list_structure_info()
            stats = [
                ("Pacientes Registrados", str(self.core.total_patients()),  AURORA_CYAN),
                ("Citas Agendadas",       str(self.core.total_appointments()), PULSAR_PINK),
                ("Especies Disponibles",  str(len(self.core.get_all_species())), ORBIT_GREEN),
            ]
            for i, (title, value, color) in enumerate(stats):
                card = self._card(body, row=0, col=i)
                card.columnconfigure(0, weight=1)
                tk.Label(card, text=value, font=("Courier New", 34, "bold"),
                         bg=NEBULA_CARD, fg=color).pack(pady=(20, 4))
                tk.Label(card, text=title, font=self.fonts["small"],
                         bg=NEBULA_CARD, fg=MOON_GREY).pack(pady=(0, 20))

            # List structure info card
            list_card = self._card(body, row=1, col=0, colspan=3)
            list_card.columnconfigure((0, 1, 2, 3), weight=1)
            tk.Label(list_card, text="◈ Estado de la Lista Doblemente Enlazada",
                     font=self.fonts["subhead"], bg=NEBULA_CARD,
                     fg=AURORA_CYAN).grid(row=0, column=0, columnspan=4,
                                          sticky="w", padx=14, pady=(14, 8))
            meta = [
                ("Cabeza (HEAD)", info["head"]),
                ("Cola (TAIL)",   info["tail"]),
                ("Nodos totales", str(info["size"])),
                ("Dirección",     "Bidireccional ⟺"),
            ]
            for i, (lbl, val) in enumerate(meta):
                tk.Label(list_card, text=lbl, font=self.fonts["small"],
                         bg=NEBULA_CARD, fg=MOON_GREY).grid(
                    row=1, column=i, padx=14, pady=4, sticky="w")
                tk.Label(list_card, text=val, font=self.fonts["body"],
                         bg=NEBULA_CARD, fg=STAR_WHITE).grid(
                    row=2, column=i, padx=14, pady=(0, 14), sticky="w")

            # Recent patients
            recent_card = self._card(body, row=2, col=0, colspan=3)
            recent_card.columnconfigure(0, weight=1)
            recent_card.rowconfigure(1, weight=1)
            tk.Label(recent_card, text="Últimos Pacientes (recorrido hacia atrás)",
                     font=self.fonts["subhead"], bg=NEBULA_CARD,
                     fg=AURORA_CYAN).grid(row=0, column=0, sticky="w",
                                           padx=14, pady=(14, 6))
            patients_reversed = self.core.get_patients_reversed()[:5]
            for j, p in enumerate(patients_reversed):
                row_bg = NEBULA_CARD if j % 2 == 0 else COSMOS_DARK
                tk.Label(recent_card,
                         text=f"  ◂  {p.patient_id}  {p.name:<14} {p.species.species_name:<10} Dueño: {p.owner_name}",
                         font=self.fonts["mono"], bg=row_bg, fg=STAR_WHITE,
                         anchor="w").grid(row=j + 1, column=0, sticky="ew", padx=4, pady=1)

        self._switch_frame(build)

    # ── Patient list ──────────────────────────────────────────

    def _show_patients(self):
        def build(frame):
            frame.rowconfigure(2, weight=1)
            self._section_title(frame, "◈ Pacientes Registrados",
                                "Lista doblemente enlazada — recorrido hacia adelante")

            # Search bar
            search_frame = tk.Frame(frame, bg=DEEP_SPACE)
            search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
            tk.Label(search_frame, text="Buscar:", font=self.fonts["small"],
                     bg=DEEP_SPACE, fg=MOON_GREY).pack(side="left")
            search_var = tk.StringVar()
            tk.Entry(search_frame, textvariable=search_var,
                     font=self.fonts["body"], bg=NEBULA_CARD, fg=STAR_WHITE,
                     insertbackground=AURORA_CYAN, relief="flat",
                     highlightbackground=BORDER_LINE, highlightthickness=1,
                     width=30).pack(side="left", padx=8)

            columns = ("id", "nombre", "especie", "edad", "peso", "dueño", "teléfono")
            headings = ("ID", "Nombre", "Especie", "Edad", "Peso (kg)", "Dueño", "Teléfono")
            tree, wrapper = self._build_tree(frame, columns, headings, row=2, col=0)
            wrapper.rowconfigure(0, weight=1)

            def populate(patients):
                for item in tree.get_children():
                    tree.delete(item)
                for p in patients:
                    tree.insert("", "end", values=(
                        p.patient_id, p.name, p.species.species_name,
                        f"{p.age} años", f"{p.weight} kg",
                        p.owner_name, p.owner_phone
                    ))

            populate(self.core.get_all_patients())

            def on_search(*_):
                term = search_var.get().strip()
                if term:
                    populate(self.core.search_patients_by_name(term))
                else:
                    populate(self.core.get_all_patients())

            search_var.trace_add("write", on_search)

            # Action bar below table
            action_bar = tk.Frame(frame, bg=DEEP_SPACE)
            action_bar.grid(row=3, column=0, sticky="ew", pady=8)

            def delete_selected():
                selected = tree.focus()
                if not selected:
                    messagebox.showwarning("Sin selección", "Selecciona un paciente.")
                    return
                pid = tree.item(selected)["values"][0]
                if messagebox.askyesno("Confirmar eliminación",
                                       f"¿Eliminar paciente {pid}?"):
                    self.core.delete_patient(pid)
                    populate(self.core.get_all_patients())

            def show_history():
                selected = tree.focus()
                if not selected:
                    return
                pid = tree.item(selected)["values"][0]
                patient = self.core.search_patient_by_id(pid)
                if patient:
                    history = patient.medical_history
                    msg = "\n".join(history) if history else "Sin historial médico."
                    messagebox.showinfo(f"Historial de {patient.name}", msg)

            self._accent_button(action_bar, "Ver Historial Médico",
                                show_history, AURORA_CYAN).pack(side="left", padx=4)
            self._accent_button(action_bar, "Eliminar Paciente",
                                delete_selected, VOID_RED).pack(side="left", padx=4)

        self._switch_frame(build)

    # ── Register patient ──────────────────────────────────────

    def _show_register_patient(self):
        def build(frame):
            self._section_title(frame, "⊕ Registrar Nuevo Paciente",
                                "Inserta un nuevo nodo al final de la lista")
            card = self._card(frame, row=1, col=0)
            card.columnconfigure(1, weight=1)

            fields = {}
            labels = ["Nombre del animal", "Edad (años)", "Peso (kg)",
                      "Nombre del dueño", "Teléfono"]
            keys   = ["name", "age", "weight", "owner_name", "owner_phone"]
            for i, (lbl, key) in enumerate(zip(labels, keys)):
                fields[key] = self._input_field(card, lbl, i)

            # Species selector
            tk.Label(card, text="Especie", font=self.fonts["small"],
                     bg=NEBULA_CARD, fg=MOON_GREY).grid(
                row=5, column=0, sticky="w", padx=14, pady=5)
            species_list = self.core.get_all_species()
            species_var = tk.StringVar()
            species_map = {sp.species_name: sp.species_id for sp in species_list}
            combo = ttk.Combobox(card, textvariable=species_var,
                                 values=list(species_map.keys()),
                                 state="readonly", width=26,
                                 font=self.fonts["body"])
            combo.grid(row=5, column=1, sticky="ew", padx=14, pady=5)
            if species_list:
                combo.set(species_list[0].species_name)

            result_label = tk.Label(card, text="", font=self.fonts["small"],
                                    bg=NEBULA_CARD, fg=ORBIT_GREEN)
            result_label.grid(row=7, column=0, columnspan=2, pady=8)

            def submit():
                name       = fields["name"].get().strip()
                age        = fields["age"].get().strip()
                weight     = fields["weight"].get().strip()
                owner_name = fields["owner_name"].get().strip()
                owner_phone= fields["owner_phone"].get().strip()
                sp_name    = species_var.get()

                if not all([name, age, weight, owner_name, owner_phone, sp_name]):
                    result_label.config(text="⚠ Completa todos los campos.", fg=COMET_AMBER)
                    return
                try:
                    float(age); float(weight)
                except ValueError:
                    result_label.config(text="⚠ Edad y peso deben ser números.", fg=COMET_AMBER)
                    return

                patient, msg = self.core.register_patient(
                    name, age, weight, species_map[sp_name], owner_name, owner_phone)
                if patient:
                    result_label.config(text=f"✓ {msg} ID: {patient.patient_id}", fg=ORBIT_GREEN)
                    for var in fields.values():
                        var.set("")
                else:
                    result_label.config(text=f"✗ {msg}", fg=VOID_RED)

            self._accent_button(card, "Registrar Paciente →",
                                submit, AURORA_CYAN).grid(
                row=6, column=0, columnspan=2, pady=12)

        self._switch_frame(build)

    # ── Appointments list ─────────────────────────────────────

    def _show_appointments(self):
        def build(frame):
            frame.rowconfigure(2, weight=1)
            self._section_title(frame, "◷ Citas Agendadas",
                                "Gestión de citas médicas")

            columns = ("id", "paciente", "fecha", "motivo", "veterinario", "estado")
            headings = ("ID Cita", "Paciente", "Fecha", "Motivo", "Veterinario", "Estado")
            tree, wrapper = self._build_tree(frame, columns, headings, row=2, col=0)
            wrapper.rowconfigure(0, weight=1)

            def populate():
                for item in tree.get_children():
                    tree.delete(item)
                for a in self.core.get_all_appointments():
                    color_tag = "pending"
                    if a.status == Vortex.COMPLETED:
                        color_tag = "done"
                    elif a.status == Vortex.CANCELLED:
                        color_tag = "cancel"
                    tree.insert("", "end", values=(
                        a.appointment_id, a.patient.name, a.date,
                        a.reason, a.veterinarian, a.status
                    ), tags=(color_tag,))

            tree.tag_configure("done",   foreground=ORBIT_GREEN)
            tree.tag_configure("cancel", foreground=VOID_RED)
            tree.tag_configure("pending",foreground=COMET_AMBER)
            populate()

            action_bar = tk.Frame(frame, bg=DEEP_SPACE)
            action_bar.grid(row=3, column=0, sticky="ew", pady=8)

            def update_status(new_status):
                selected = tree.focus()
                if not selected:
                    messagebox.showwarning("Sin selección", "Selecciona una cita.")
                    return
                appt_id = tree.item(selected)["values"][0]
                self.core.update_appointment_status(appt_id, new_status)
                populate()

            self._accent_button(action_bar, "✓ Marcar Completada",
                lambda: update_status(Vortex.COMPLETED), ORBIT_GREEN).pack(side="left", padx=4)
            self._accent_button(action_bar, "✗ Cancelar Cita",
                lambda: update_status(Vortex.CANCELLED), VOID_RED).pack(side="left", padx=4)

        self._switch_frame(build)

    # ── Schedule appointment ───────────────────────────────────

    def _show_schedule_appointment(self):
        def build(frame):
            self._section_title(frame, "⊞ Agendar Nueva Cita",
                                "Crea una cita vinculada a un paciente existente")
            card = self._card(frame, row=1, col=0)
            card.columnconfigure(1, weight=1)

            pid_var  = self._input_field(card, "ID del Paciente",  0, "PAC001")
            date_var = self._input_field(card, "Fecha (AAAA-MM-DD)", 1, "2025-08-20")
            reas_var = self._input_field(card, "Motivo de la cita", 2)
            vet_var  = self._input_field(card, "Veterinario",       3, "Dra. Solano")

            result_label = tk.Label(card, text="", font=self.fonts["small"],
                                    bg=NEBULA_CARD, fg=ORBIT_GREEN)
            result_label.grid(row=5, column=0, columnspan=2, pady=8)

            def submit():
                pid  = pid_var.get().strip()
                date = date_var.get().strip()
                reas = reas_var.get().strip()
                vet  = vet_var.get().strip()
                if not all([pid, date, reas, vet]):
                    result_label.config(text="⚠ Completa todos los campos.", fg=COMET_AMBER)
                    return
                appt, msg = self.core.schedule_appointment(pid, date, reas, vet)
                if appt:
                    result_label.config(text=f"✓ {msg} ID: {appt.appointment_id}",
                                        fg=ORBIT_GREEN)
                else:
                    result_label.config(text=f"✗ {msg}", fg=VOID_RED)

            self._accent_button(card, "Agendar Cita →",
                                submit, PULSAR_PINK).grid(
                row=4, column=0, columnspan=2, pady=12)

        self._switch_frame(build)

    # ── List structure visualizer ──────────────────────────────

    def _show_list_structure(self):
        def build(frame):
            frame.rowconfigure(1, weight=1)
            self._section_title(frame, "≋ Estructura de la Lista Doble",
                                "Visualización de nodos Quasar conectados bidireccialmente")

            canvas_frame = tk.Frame(frame, bg=NEBULA_CARD,
                                    highlightbackground=BORDER_LINE, highlightthickness=1)
            canvas_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)

            canvas = tk.Canvas(canvas_frame, bg=NEBULA_CARD, highlightthickness=0)
            hscroll = tk.Scrollbar(canvas_frame, orient="horizontal",
                                   command=canvas.xview)
            canvas.configure(xscrollcommand=hscroll.set)
            hscroll.pack(side="bottom", fill="x")
            canvas.pack(fill="both", expand=True)

            patients = self.core.get_all_patients()
            node_w, node_h = 140, 70
            gap = 60
            y_center = 120
            padding_x = 40

            total_width = padding_x * 2 + len(patients) * (node_w + gap)
            canvas.configure(scrollregion=(0, 0, total_width, 260))

            # NULL head label
            canvas.create_text(padding_x - 10, y_center, text="NULL",
                                font=("Courier New", 9, "bold"),
                                fill=MOON_GREY, anchor="e")

            for i, patient in enumerate(patients):
                x = padding_x + i * (node_w + gap)
                y = y_center - node_h // 2

                is_head = i == 0
                is_tail = i == len(patients) - 1
                border = AURORA_CYAN if is_head else (PULSAR_PINK if is_tail else BORDER_LINE)

                # Node box
                canvas.create_rectangle(x, y, x + node_w, y + node_h,
                                         fill=COSMOS_DARK, outline=border, width=2)

                # Labels inside node
                canvas.create_text(x + node_w // 2, y + 14,
                                   text=f"[{patient.patient_id}]",
                                   font=("Courier New", 8, "bold"),
                                   fill=AURORA_CYAN)
                canvas.create_text(x + node_w // 2, y + 30,
                                   text=patient.name,
                                   font=("Courier New", 10, "bold"),
                                   fill=STAR_WHITE)
                canvas.create_text(x + node_w // 2, y + 46,
                                   text=patient.species.species_name,
                                   font=("Courier New", 8),
                                   fill=MOON_GREY)
                canvas.create_text(x + node_w // 2, y + 60,
                                   text="Quasar",
                                   font=("Courier New", 7, "italic"),
                                   fill=PULSAR_PINK)

                # HEAD / TAIL badges
                if is_head:
                    canvas.create_text(x + node_w // 2, y - 14,
                                       text="◀ HEAD", font=("Courier New", 8, "bold"),
                                       fill=AURORA_CYAN)
                if is_tail:
                    canvas.create_text(x + node_w // 2, y - 14,
                                       text="TAIL ▶", font=("Courier New", 8, "bold"),
                                       fill=PULSAR_PINK)

                # Arrows between nodes
                if i < len(patients) - 1:
                    ax = x + node_w
                    ay = y_center
                    bx = ax + gap
                    # Forward arrow
                    canvas.create_line(ax, ay - 7, bx, ay - 7,
                                       fill=AURORA_CYAN, arrow="last", width=2)
                    # Backward arrow
                    canvas.create_line(bx, ay + 7, ax, ay + 7,
                                       fill=PULSAR_PINK, arrow="last", width=2)

            # NULL tail label
            last_x = padding_x + len(patients) * (node_w + gap) - gap
            canvas.create_text(last_x + 10, y_center, text="NULL",
                                font=("Courier New", 9, "bold"),
                                fill=MOON_GREY, anchor="w")

            # Legend
            legend_y = 210
            canvas.create_text(padding_x, legend_y, text="◀  next (→)",
                                font=("Courier New", 9), fill=AURORA_CYAN, anchor="w")
            canvas.create_text(padding_x + 130, legend_y, text="▶  previous (←)",
                                font=("Courier New", 9), fill=PULSAR_PINK, anchor="w")

        self._switch_frame(build)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = CosmosUI(root)
    root.mainloop()
