"""
╔══════════════════════════════════════════════════════════════════╗
║         FILTRADO DE PAQUETES - SIMULADOR DE AUTÓMATA             ║
║    Alcaraz Méndez Fernando Isai                                   ║
║                                     ║
║                                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import messagebox
import time, random, threading

# ─── Paleta ──────────────────────────────────────────────────────────────────
BG     = "#0d1117"; BG2 = "#161b22"; BG3 = "#1c2128"
BORDER = "#30363d"; BLUE = "#58a6ff"; GREEN = "#3fb950"
RED    = "#f78166"; YELLOW = "#ffa657"; PURPLE = "#bc8cff"
WHITE  = "#e6edf3"; DIM = "#8b949e"; CYAN = "#39d353"

# ─── KMP ─────────────────────────────────────────────────────────────────────
def build_kmp_fail(pattern):
    fail = [0]*len(pattern); j = 0
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]: j = fail[j-1]
        if pattern[i] == pattern[j]: j += 1
        fail[i] = j
    return fail

def simulate_automaton(header_bits, pattern):
    fail = build_kmp_fail(pattern); j = 0; trace = []
    for i, bit in enumerate(header_bits):
        while j > 0 and bit != pattern[j]: j = fail[j-1]
        if bit == pattern[j]: j += 1
        trace.append((i, bit, j))
        if j == len(pattern): return True, i-len(pattern)+1, trace
    return False, -1, trace

# ─── Generación de paquetes ───────────────────────────────────────────────────
def random_header(n=12):
    return [random.choice(['0','1']) for _ in range(n)]

def safe_clean_header(block_patterns):
    for _ in range(300):
        h = random_header(12)
        joined = "".join(h)
        if all(p not in joined for p in block_patterns): return h
    return list("000100010001")

def inject_pattern_into_header(pattern, block_patterns):
    other = [p for p in block_patterns if p != pattern]
    for _ in range(100):
        header = random_header(14)
        pos = random.randint(0, len(header)-len(pattern))
        header[pos:pos+len(pattern)] = list(pattern)
        joined = "".join(header)
        if all(op not in joined for op in other): return header
    return ['0','0','0'] + list(pattern) + ['0','0','0']

def default_packets(block_patterns):
    pats = list(block_patterns.keys())
    def get_pat(i): return pats[i] if i < len(pats) else None
    packets = [
        {"id":1,"src_ip":"192.168.1.10",   "dst_ip":"10.0.0.1",  "port":80,  "proto":"TCP",
         "header": safe_clean_header(block_patterns)},
        {"id":2,"src_ip":"203.0.113.42",   "dst_ip":"10.0.0.1",  "port":443, "proto":"TCP",
         "header": inject_pattern_into_header(get_pat(0), block_patterns) if get_pat(0) else safe_clean_header(block_patterns)},
        {"id":3,"src_ip":"172.16.5.8",     "dst_ip":"10.0.0.5",  "port":22,  "proto":"SSH",
         "header": safe_clean_header(block_patterns)},
        {"id":4,"src_ip":"198.51.100.7",   "dst_ip":"10.0.0.1",  "port":0,   "proto":"UDP",
         "header": inject_pattern_into_header(get_pat(1), block_patterns) if get_pat(1) else safe_clean_header(block_patterns)},
        {"id":5,"src_ip":"255.255.255.255","dst_ip":"10.0.0.255","port":9,   "proto":"UDP",
         "header": inject_pattern_into_header(get_pat(2), block_patterns) if get_pat(2) else safe_clean_header(block_patterns)},
        {"id":6,"src_ip":"10.0.0.20",      "dst_ip":"10.0.0.1",  "port":8080,"proto":"HTTP",
         "header": safe_clean_header(block_patterns)},
    ]
    return packets

# ═══════════════════════════════════════════════════════════════════════════════
# VENTANA EDITOR
# ═══════════════════════════════════════════════════════════════════════════════
class EditorWindow(tk.Toplevel):
    def __init__(self, parent, packets, block_patterns, on_save):
        super().__init__(parent)
        self.title("✏  Editor de Paquetes y Patrones")
        self.configure(bg=BG)
        self.geometry("860x660")
        self.resizable(True, True)
        self.grab_set()

        self.packets = [dict(p) for p in packets]
        self.block_patterns = dict(block_patterns)
        self.on_save = on_save
        for p in self.packets:
            p["header_str"] = "".join(p["header"])

        self._build()

    def _entry(self, parent, width=18, **kw):
        return tk.Entry(parent, bg=BG3, fg=WHITE, insertbackground=WHITE,
                        font=("Courier New", 10), relief=tk.FLAT,
                        highlightthickness=1, highlightbackground=BORDER,
                        highlightcolor=BLUE, width=width, **kw)

    def _build(self):
        tk.Label(self, text="✏  EDITOR DE CONFIGURACIÓN", bg=BG2, fg=BLUE,
                 font=("Courier New", 14, "bold"), pady=10).pack(fill=tk.X)
        tk.Frame(self, bg=BORDER, height=1).pack(fill=tk.X)

        nb = tk.Frame(self, bg=BG)
        nb.pack(fill=tk.BOTH, expand=True)

        self.tab_bar = tk.Frame(nb, bg=BG2)
        self.tab_bar.pack(fill=tk.X)
        self.tab_content = tk.Frame(nb, bg=BG)
        self.tab_content.pack(fill=tk.BOTH, expand=True)

        self.tab_frames = {}
        for label, key in [("📦  Paquetes","packets"),("🛡  Patrones","patterns")]:
            btn = tk.Button(self.tab_bar, text=label, bg=BG3, fg=DIM,
                            font=("Courier New",10,"bold"), relief=tk.FLAT,
                            padx=14, pady=6, cursor="hand2",
                            command=lambda k=key: self._switch_tab(k))
            btn.pack(side=tk.LEFT, padx=2, pady=4)
            self.tab_frames[key] = {"btn": btn, "frame": tk.Frame(self.tab_content, bg=BG)}

        self._build_packets_tab()
        self._build_patterns_tab()
        self._switch_tab("packets")

        tk.Frame(self, bg=BORDER, height=1).pack(fill=tk.X)
        btn_row = tk.Frame(self, bg=BG2, pady=8)
        btn_row.pack(fill=tk.X)
        bc = {"font":("Courier New",11,"bold"),"relief":tk.FLAT,"padx":14,"pady":5,"cursor":"hand2"}
        tk.Button(btn_row, text="💾  Guardar y Aplicar", bg=GREEN, fg=BG,
                  command=self._save, **bc).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_row, text="🎲  Regenerar Aleatorio", bg=PURPLE, fg=BG,
                  command=self._randomize, **bc).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_row, text="✖  Cancelar", bg=BG3, fg=WHITE,
                  command=self.destroy, **bc).pack(side=tk.LEFT, padx=4)
        tk.Label(btn_row, text="Cabecera: solo 0s y 1s  |  Puerto: número entero",
                 bg=BG2, fg=DIM, font=("Courier New",8)).pack(side=tk.RIGHT, padx=12)

    def _switch_tab(self, key):
        for k, v in self.tab_frames.items():
            v["frame"].pack_forget()
            v["btn"].config(bg=BG3, fg=DIM)
        self.tab_frames[key]["frame"].pack(fill=tk.BOTH, expand=True)
        self.tab_frames[key]["btn"].config(bg=BLUE, fg=BG)

    # ── Tab Paquetes ──────────────────────────────────────────────────────────
    def _build_packets_tab(self):
        frame = self.tab_frames["packets"]["frame"]
        canvas = tk.Canvas(frame, bg=BG, highlightthickness=0)
        sb = tk.Scrollbar(frame, orient="vertical", command=canvas.yview, bg=BG2)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        inner = tk.Frame(canvas, bg=BG)
        wid = canvas.create_window((0,0), window=inner, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(wid, width=e.width))
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Cabecera de tabla
        hrow = tk.Frame(inner, bg=BG2, pady=5)
        hrow.pack(fill=tk.X, padx=8)
        for txt, w in [("ID",4),("IP Origen",16),("IP Destino",16),("Puerto",7),("Proto",7),("Cabecera (bits)",20)]:
            tk.Label(hrow, text=txt, bg=BG2, fg=BLUE,
                     font=("Courier New",9,"bold"), width=w, anchor="w").pack(side=tk.LEFT, padx=3)
        tk.Frame(inner, bg=BORDER, height=1).pack(fill=tk.X, padx=8)

        self.pkt_entries = []
        for p in self.packets:
            row = tk.Frame(inner, bg=BG3, pady=4)
            row.pack(fill=tk.X, padx=8, pady=2)
            entries = {}
            tk.Label(row, text=str(p["id"]), bg=BG3, fg=YELLOW,
                     font=("Courier New",10,"bold"), width=4, anchor="w").pack(side=tk.LEFT, padx=3)
            for field, w in [("src_ip",16),("dst_ip",16),("port",7),("proto",7)]:
                e = self._entry(row, width=w)
                e.insert(0, str(p[field]))
                e.pack(side=tk.LEFT, padx=3)
                entries[field] = e
            e_hdr = self._entry(row, width=20)
            e_hdr.insert(0, p["header_str"])
            e_hdr.pack(side=tk.LEFT, padx=3)
            entries["header_str"] = e_hdr
            tk.Button(row, text="🎲", bg=BG2, fg=YELLOW, relief=tk.FLAT,
                      font=("Courier New",9), cursor="hand2",
                      command=lambda e=e_hdr: self._rand_header(e)).pack(side=tk.LEFT, padx=3)
            self.pkt_entries.append(entries)

        tk.Label(inner, text="  🎲 = genera cabecera aleatoria para esa fila",
                 bg=BG, fg=DIM, font=("Courier New",8)).pack(anchor="w", padx=8, pady=6)

    def _rand_header(self, e):
        e.delete(0, tk.END)
        e.insert(0, "".join(random.choice("01") for _ in range(12)))

    # ── Tab Patrones ──────────────────────────────────────────────────────────
    def _build_patterns_tab(self):
        frame = self.tab_frames["patterns"]["frame"]
        tk.Label(frame, text="  Patrones de bits que el firewall detectará y bloqueará:",
                 bg=BG, fg=DIM, font=("Courier New",9)).pack(anchor="w", pady=(10,4), padx=12)
        hrow = tk.Frame(frame, bg=BG2, pady=4)
        hrow.pack(fill=tk.X, padx=12)
        tk.Label(hrow, text="Patrón (solo 0/1)", bg=BG2, fg=BLUE,
                 font=("Courier New",9,"bold"), width=22, anchor="w").pack(side=tk.LEFT, padx=4)
        tk.Label(hrow, text="Descripción del ataque", bg=BG2, fg=BLUE,
                 font=("Courier New",9,"bold"), anchor="w").pack(side=tk.LEFT, padx=4)
        tk.Frame(frame, bg=BORDER, height=1).pack(fill=tk.X, padx=12)

        self.pat_entries = []
        self.pat_rows_frame = tk.Frame(frame, bg=BG)
        self.pat_rows_frame.pack(fill=tk.X, padx=12)
        for pat, desc in self.block_patterns.items():
            self._add_pattern_row(pat, desc)

        tk.Button(frame, text="➕  Agregar patrón", bg=BG3, fg=GREEN,
                  font=("Courier New",10,"bold"), relief=tk.FLAT,
                  padx=10, pady=4, cursor="hand2",
                  command=lambda: self._add_pattern_row("","")).pack(anchor="w", padx=12, pady=8)
        tk.Label(frame,
                 text="  ℹ  Longitud recomendada: 4 bits  |  Máx: 8 bits  |  Mín: 2 bits\n"
                      "  ℹ  Patrones muy cortos (ej: '1') bloquearán casi todo.",
                 bg=BG, fg=DIM, font=("Courier New",8), justify="left").pack(anchor="w", padx=12)

    def _add_pattern_row(self, pat, desc):
        row = tk.Frame(self.pat_rows_frame, bg=BG3, pady=4)
        row.pack(fill=tk.X, pady=2)
        e_pat = self._entry(row, width=22)
        e_pat.insert(0, pat)
        e_pat.pack(side=tk.LEFT, padx=4)
        e_desc = self._entry(row, width=38)
        e_desc.insert(0, desc)
        e_desc.pack(side=tk.LEFT, padx=4)
        pair = (e_pat, e_desc)
        def remove():
            row.destroy()
            if pair in self.pat_entries: self.pat_entries.remove(pair)
        tk.Button(row, text="🗑", bg=BG2, fg=RED, relief=tk.FLAT,
                  font=("Courier New",10), cursor="hand2",
                  command=remove).pack(side=tk.LEFT, padx=4)
        self.pat_entries.append(pair)

    # ── Guardar / Aleatorio ───────────────────────────────────────────────────
    def _validate_bits(self, s, name):
        s = s.strip().replace(" ","")
        if not s: raise ValueError(f"'{name}' está vacío.")
        if not all(c in "01" for c in s): raise ValueError(f"'{name}' debe contener solo 0s y 1s.")
        return s

    def _save(self):
        try:
            new_patterns = {}
            for e_pat, e_desc in self.pat_entries:
                pat = self._validate_bits(e_pat.get(), "Patrón")
                if len(pat) < 2: raise ValueError("El patrón debe tener al menos 2 bits.")
                if len(pat) > 8: raise ValueError("El patrón no debe exceder 8 bits.")
                new_patterns[pat] = e_desc.get().strip() or "Ataque desconocido"
            if not new_patterns: raise ValueError("Debes tener al menos un patrón.")

            new_packets = []
            for i, entries in enumerate(self.pkt_entries):
                port = entries["port"].get().strip()
                if not port.isdigit(): raise ValueError(f"Puerto #{i+1} debe ser numérico.")
                hdr = self._validate_bits(entries["header_str"].get(), f"Cabecera #{i+1}")
                if len(hdr) < 4: raise ValueError(f"Cabecera #{i+1} debe tener al menos 4 bits.")
                new_packets.append({
                    "id": i+1,
                    "src_ip": entries["src_ip"].get().strip(),
                    "dst_ip": entries["dst_ip"].get().strip(),
                    "port": int(port),
                    "proto": entries["proto"].get().strip().upper(),
                    "header": list(hdr)
                })

            self.on_save(new_packets, new_patterns)
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e), parent=self)

    def _randomize(self):
        pats = {}
        for e_pat, e_desc in self.pat_entries:
            p = e_pat.get().strip().replace(" ","")
            d = e_desc.get().strip()
            if p and all(c in "01" for c in p): pats[p] = d or "Ataque"
        if not pats:
            messagebox.showwarning("Sin patrones", "Agrega al menos un patrón primero.", parent=self)
            return
        pat_list = list(pats.keys())
        for i, entries in enumerate(self.pkt_entries):
            h = safe_clean_header(pats) if i % 2 == 0 else inject_pattern_into_header(pat_list[i % len(pat_list)], pats)
            entries["header_str"].delete(0, tk.END)
            entries["header_str"].insert(0, "".join(h))
        messagebox.showinfo("¡Listo!", "Cabeceras regeneradas.\nPresiona 'Guardar y Aplicar' para confirmar.", parent=self)


# ═══════════════════════════════════════════════════════════════════════════════
# APP PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════
class FirewallApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 Simulador de Firewall — Autómata Finito")
        self.root.configure(bg=BG)
        self.root.geometry("1050x760")
        self.root.resizable(True, True)

        self.block_patterns = {"1010":"DoS / Flood Attack","1100":"Port Scan","1111":"Broadcast Malicioso"}
        self.packets = default_packets(self.block_patterns)
        self.current_idx = 0; self.results = []; self.running = False

        self._build_ui()
        self._show_welcome()

    def _build_ui(self):
        hdr = tk.Frame(self.root, bg=BG2, pady=10)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="🔥  SIMULADOR DE FIREWALL", bg=BG2, fg=BLUE,
                 font=("Courier New",18,"bold")).pack()
        tk.Label(hdr, text="Filtrado de Paquetes mediante Autómata Finito (KMP)",
                 bg=BG2, fg=DIM, font=("Courier New",10)).pack()
        tk.Label(hdr, text="Alcaraz Méndez F.I.",
                 bg=BG2, fg=DIM, font=("Courier New",9)).pack(pady=(2,0))
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill=tk.X)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill=tk.BOTH, expand=True)

        # ── Panel izquierdo ──
        left = tk.Frame(body, bg=BG2, width=300, padx=14, pady=14)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)

        def sec(t): 
            tk.Label(left, text=t, bg=BG2, fg=BLUE, font=("Courier New",10,"bold")).pack(anchor="w")
            tk.Frame(left, bg=BORDER, height=1).pack(fill=tk.X, pady=4)

        sec("PAQUETE ACTUAL")
        self.pkt_labels = {}
        for key in ["ID","Origen","Destino","Puerto","Proto","Cabecera"]:
            row = tk.Frame(left, bg=BG2); row.pack(fill=tk.X, pady=1)
            tk.Label(row, text=f"{key}:", bg=BG2, fg=DIM,
                     font=("Courier New",9), width=9, anchor="w").pack(side=tk.LEFT)
            lbl = tk.Label(row, text="—", bg=BG2, fg=WHITE,
                           font=("Courier New",9,"bold"), anchor="w", wraplength=190, justify="left")
            lbl.pack(side=tk.LEFT)
            self.pkt_labels[key] = lbl

        tk.Frame(left, bg=BORDER, height=1).pack(fill=tk.X, pady=8)
        sec("PATRONES BLOQUEADOS")
        self.pat_list_frame = tk.Frame(left, bg=BG2)
        self.pat_list_frame.pack(fill=tk.X)
        self._refresh_pattern_list()

        tk.Frame(left, bg=BORDER, height=1).pack(fill=tk.X, pady=8)
        sec("RESULTADOS")
        rr = tk.Frame(left, bg=BG2); rr.pack(fill=tk.X)
        tk.Label(rr, text="✅  Aceptados:", bg=BG2, fg=GREEN, font=("Courier New",10)).pack(side=tk.LEFT)
        self.lbl_accepted = tk.Label(rr, text="0", bg=BG2, fg=GREEN, font=("Courier New",14,"bold"))
        self.lbl_accepted.pack(side=tk.LEFT, padx=6)
        rr2 = tk.Frame(left, bg=BG2); rr2.pack(fill=tk.X, pady=3)
        tk.Label(rr2, text="🚫  Bloqueados:", bg=BG2, fg=RED, font=("Courier New",10)).pack(side=tk.LEFT)
        self.lbl_blocked = tk.Label(rr2, text="0", bg=BG2, fg=RED, font=("Courier New",14,"bold"))
        self.lbl_blocked.pack(side=tk.LEFT, padx=6)

        # ── Panel derecho ──
        right = tk.Frame(body, bg=BG, padx=12, pady=12)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(right, text="TRANSICIONES DEL AUTÓMATA", bg=BG, fg=BLUE,
                 font=("Courier New",10,"bold")).pack(anchor="w")
        self.canvas = tk.Canvas(right, bg=BG3, height=118,
                                highlightthickness=1, highlightbackground=BORDER)
        self.canvas.pack(fill=tk.X, pady=(4,10))
        self._draw_automaton_base()

        tk.Label(right, text="LOG DE ANÁLISIS", bg=BG, fg=BLUE,
                 font=("Courier New",10,"bold")).pack(anchor="w")
        lf = tk.Frame(right, bg=BG); lf.pack(fill=tk.BOTH, expand=True)
        sb = tk.Scrollbar(lf, bg=BG2); sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.log = tk.Text(lf, bg=BG3, fg=WHITE, insertbackground=WHITE,
                           font=("Courier New",10), wrap=tk.WORD, yscrollcommand=sb.set,
                           relief=tk.FLAT, state=tk.DISABLED, pady=8, padx=8)
        self.log.pack(fill=tk.BOTH, expand=True)
        sb.config(command=self.log.yview)
        for tag, fg, extra in [
            ("title", BLUE, {"font":("Courier New",11,"bold")}),
            ("ok", GREEN, {}), ("block", RED, {"font":("Courier New",10,"bold")}),
            ("warn", YELLOW, {}), ("dim", DIM, {}),
            ("pat", YELLOW, {"font":("Courier New",10,"bold")}),
            ("header", CYAN, {"font":("Courier New",10,"bold")}),
            ("white", WHITE, {}),
            ("match", RED, {"font":("Courier New",10,"bold"), "background":"#3d0000"}),
        ]:
            self.log.tag_config(tag, foreground=fg, **extra)

        # ── Botones ──
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill=tk.X, side=tk.BOTTOM)
        bf = tk.Frame(self.root, bg=BG2, pady=8); bf.pack(fill=tk.X, side=tk.BOTTOM)
        bc = {"font":("Courier New",11,"bold"),"relief":tk.FLAT,"padx":14,"pady":5,"cursor":"hand2"}
        self.btn_next = tk.Button(bf, text="▶  Analizar Paquete", bg=BLUE, fg=BG,
                                  command=self._next_packet, **bc)
        self.btn_next.pack(side=tk.LEFT, padx=10)
        self.btn_auto = tk.Button(bf, text="⚡  Auto (todos)", bg=PURPLE, fg=BG,
                                  command=self._run_all, **bc)
        self.btn_auto.pack(side=tk.LEFT, padx=4)
        tk.Button(bf, text="✏  Editar", bg=YELLOW, fg=BG,
                  command=self._open_editor, **bc).pack(side=tk.LEFT, padx=4)
        tk.Button(bf, text="↺  Reiniciar", bg=BG3, fg=WHITE,
                  command=self._reset, **bc).pack(side=tk.LEFT, padx=4)
        self.status_lbl = tk.Label(bf, text=f"Paquete 0/{len(self.packets)}",
                                   bg=BG2, fg=DIM, font=("Courier New",10))
        self.status_lbl.pack(side=tk.RIGHT, padx=16)

    def _refresh_pattern_list(self):
        for w in self.pat_list_frame.winfo_children(): w.destroy()
        for pat, reason in self.block_patterns.items():
            pr = tk.Frame(self.pat_list_frame, bg=BG2); pr.pack(fill=tk.X, pady=2)
            tk.Label(pr, text=f"  {pat}", bg=BG3, fg=YELLOW,
                     font=("Courier New",10,"bold"), padx=5, pady=1).pack(side=tk.LEFT)
            tk.Label(pr, text=f"  {reason}", bg=BG2, fg=DIM,
                     font=("Courier New",8)).pack(side=tk.LEFT)

    def _draw_automaton_base(self, active_state=0, matched=False, pattern=""):
        c = self.canvas; c.delete("all")
        w = c.winfo_width() or 700; n = 5; spacing = w//(n+1); cy = 58; r = 24
        colors = [BORDER]*n
        colors[min(active_state, n-1)] = GREEN if not matched else RED
        for i in range(n-1):
            x1 = spacing*(i+1)+r; x2 = spacing*(i+2)-r
            c.create_line(x1, cy, x2, cy, fill=DIM, width=2, arrow=tk.LAST)
            if pattern and i < len(pattern):
                c.create_text((x1+x2)//2, cy-14, text=pattern[i],
                              fill=YELLOW, font=("Courier New",11,"bold"))
        for i in range(n):
            x = spacing*(i+1)
            c.create_oval(x-r, cy-r, x+r, cy+r, fill=BG3, outline=colors[i], width=2)
            c.create_text(x, cy, text=f"q{i}", fill=WHITE, font=("Courier New",11,"bold"))
            if i == 0: c.create_text(x, cy+r+13, text="inicio", fill=DIM, font=("Courier New",8))
            if i == n-1:
                c.create_oval(x-r+4, cy-r+4, x+r-4, cy+r-4,
                              outline=RED if matched else GREEN, width=1)
                c.create_text(x, cy+r+13, text="BLOQUEO" if matched else "ACCEPT",
                              fill=RED if matched else GREEN, font=("Courier New",8,"bold"))
        c.create_line(8, cy, spacing-r, cy, fill=GREEN, width=2, arrow=tk.LAST)

    def _animate_automaton(self, pattern, trace, found):
        self.canvas.update()
        for _, (pos, bit, state) in enumerate(trace):
            self.root.after(0, lambda s=min(state,4), f=(found and state==len(pattern)),
                            p=pattern: self._draw_automaton_base(s, f, p))
            time.sleep(0.10)
        time.sleep(0.2)

    def _log(self, text, tag="white", newline=True):
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, text+("\n" if newline else ""), tag)
        self.log.see(tk.END); self.log.config(state=tk.DISABLED)
        self.root.update_idletasks()

    def _log_sep(self): self._log("─"*60, "dim")

    def _show_welcome(self):
        self._log("🔥  SIMULADOR DE FILTRADO DE PAQUETES", "title")
        self._log("Autómata Finito con búsqueda KMP\n", "dim")
        self._log("▶ Analizar Paquete → procesa uno a uno", "dim")
        self._log("⚡ Auto (todos)     → procesa todos seguidos", "dim")
        self._log("✏ Editar           → modifica paquetes y patrones\n", "dim")
        self._log_sep()

    def _update_pkt_info(self, pkt):
        self.pkt_labels["ID"].config(text=str(pkt["id"]), fg=WHITE)
        self.pkt_labels["Origen"].config(text=pkt["src_ip"])
        self.pkt_labels["Destino"].config(text=pkt["dst_ip"])
        self.pkt_labels["Puerto"].config(text=str(pkt["port"]))
        self.pkt_labels["Proto"].config(text=pkt["proto"])
        self.pkt_labels["Cabecera"].config(text=" ".join(pkt["header"]))

    def _update_counters(self):
        acc = sum(1 for r in self.results if r)
        self.lbl_accepted.config(text=str(acc))
        self.lbl_blocked.config(text=str(len(self.results)-acc))

    def _analyze(self, pkt):
        self._update_pkt_info(pkt)
        header = pkt["header"]
        self._log(f"\n📦  Paquete #{pkt['id']}  ·  {pkt['src_ip']} → {pkt['dst_ip']}  [{pkt['proto']}:{pkt['port']}]", "title")
        self._log("   Cabecera: ", "dim", newline=False)
        self._log(" ".join(header), "header")
        blocked = False; block_reason = ""
        for pattern_str, reason in self.block_patterns.items():
            pattern = list(pattern_str)
            self._log(f"\n   🔍 Revisando patrón [ ", "dim", newline=False)
            self._log(pattern_str, "pat", newline=False)
            self._log(f" ] → {reason}", "dim")
            found, pos, trace = simulate_automaton(header, pattern)
            self._animate_automaton(pattern_str, trace, found)
            for _, (i, bit, state) in enumerate(trace):
                progress = pattern_str[:state] + ("·"*(len(pattern_str)-state))
                tag = "match" if state == len(pattern_str) else "dim"
                self._log(f"     paso {i+1}: bit={bit}  q{state}  [{progress}]", tag)
                if state == len(pattern_str): break
            if found:
                blocked = True; block_reason = reason
                self._log(f"\n   ⚠  Patrón '{pattern_str}' encontrado en posición {pos}!", "warn")
                break
            else:
                self._log("   ✓  Patrón no encontrado.", "ok")
        self._log("")
        if blocked:
            self._log(f"🚫  PAQUETE #{pkt['id']} BLOQUEADO  ——  {block_reason}", "block")
            self.pkt_labels["ID"].config(fg=RED)
        else:
            self._log(f"✅  PAQUETE #{pkt['id']} ACEPTADO  ——  Reenviando al destino...", "ok")
            self.pkt_labels["ID"].config(fg=GREEN)
        self._log_sep()
        return not blocked

    def _set_buttons(self, enabled):
        s = tk.NORMAL if enabled else tk.DISABLED
        self.btn_next.config(state=s); self.btn_auto.config(state=s)

    def _next_packet(self):
        if self.running or self.current_idx >= len(self.packets): return
        self.running = True; self._set_buttons(False)
        def task():
            result = self._analyze(self.packets[self.current_idx])
            self.results.append(result); self.current_idx += 1
            self._update_counters()
            self.status_lbl.config(text=f"Paquete {self.current_idx}/{len(self.packets)}")
            self.running = False
            done = self.current_idx >= len(self.packets)
            self._set_buttons(not done)
            if done: self._show_summary()
        threading.Thread(target=task, daemon=True).start()

    def _run_all(self):
        if self.running: return
        self.running = True; self._set_buttons(False)
        def task():
            while self.current_idx < len(self.packets):
                result = self._analyze(self.packets[self.current_idx])
                self.results.append(result); self.current_idx += 1
                self._update_counters()
                self.status_lbl.config(text=f"Paquete {self.current_idx}/{len(self.packets)}")
                time.sleep(0.2)
            self.running = False; self._show_summary()
        threading.Thread(target=task, daemon=True).start()

    def _open_editor(self):
        if self.running: return
        EditorWindow(self.root, self.packets, self.block_patterns, self._apply_edits)

    def _apply_edits(self, new_packets, new_patterns):
        self.block_patterns = new_patterns
        self.packets = new_packets
        self._refresh_pattern_list()
        self._reset(keep_packets=True)
        self._log("✏  Configuración actualizada desde el editor.\n", "warn")
        self._log_sep()

    def _reset(self, keep_packets=False):
        if self.running: return
        if not keep_packets: self.packets = default_packets(self.block_patterns)
        self.current_idx = 0; self.results = []
        self._update_counters()
        self.status_lbl.config(text=f"Paquete 0/{len(self.packets)}")
        self._set_buttons(True)
        for lbl in self.pkt_labels.values(): lbl.config(text="—", fg=WHITE)
        self._draw_automaton_base()
        self.log.config(state=tk.NORMAL); self.log.delete("1.0", tk.END); self.log.config(state=tk.DISABLED)
        if not keep_packets: self._show_welcome()

    def _show_summary(self):
        acc = sum(1 for r in self.results if r); blk = len(self.results)-acc
        self._log("\n"+"═"*60, "dim")
        self._log("  RESUMEN FINAL DEL FIREWALL", "title")
        self._log("═"*60, "dim")
        self._log(f"  Paquetes analizados : {len(self.results)}", "white")
        self._log(f"  ✅  Aceptados         : {acc}", "ok")
        self._log(f"  🚫  Bloqueados        : {blk}", "block")
        self._log("═"*60, "dim")


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(800, 600)
    FirewallApp(root)
    root.mainloop()
