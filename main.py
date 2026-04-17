

import tkinter as tk
import customtkinter as ctk
import requests
import os
import subprocess
import threading
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

LANGUAGES = {
    "English 🇬🇧": {
        "title": "Tasmota Backup System", "subnet": "Subnet (ex: 192.168.1)", "auto_ip": "Auto-Detect",
        "user": "Username", "pass": "Password", "format": "File Name Format:", "start": "START", "stop": "STOP",
        "open": "Open Folder", "font": "Font Style:", "status_ready": "Ready", "status_scan": "Scanning...",
        "status_stop": "Stopped!", "status_done": "Finished!", "opts": ["IP Only", "Tasmota Name", "Both"],
        "footer": "Created by Cristian Florea", "rep_title": "Tasmota Backup Report", "rep_found": "Devices found:",
        "err_net": "Error: Could not detect local IP."
    },
    "Română 🇷🇴": {
        "title": "Sistem Backup Tasmota", "subnet": "Clasă IP (ex: 192.168.1)", "auto_ip": "Detectare Automată",
        "user": "Utilizator", "pass": "Parolă", "format": "Format Nume Fișier:", "start": "START", "stop": "STOP",
        "open": "Deschide Folder", "font": "Stil Font:", "status_ready": "Pregătit", "status_scan": "Scanare...",
        "status_stop": "Oprit!", "status_done": "Finalizat!", "opts": ["Doar IP", "Nume Tasmota", "Ambele"],
        "footer": "Creat de Cristian Florea", "rep_title": "Raport Backup Tasmota", "rep_found": "Dispozitive găsite:",
        "err_net": "Eroare: Nu s-a putut detecta IP-ul local."
    },
    "Italiano 🇮🇹": {"title": "Sistema Backup", "subnet": "Sottorete", "auto_ip": "Auto-Rilevamento", "user": "Utente",
                    "pass": "Password", "format": "Formato:", "start": "AVVIA", "stop": "STOP", "open": "Apri Cartella",
                    "font": "Carattere:", "status_ready": "Pronto", "status_scan": "Scansione...",
                    "status_stop": "Fermato!", "status_done": "Finito!", "opts": ["Solo IP", "Nome", "Entrambi"],
                    "footer": "Creato da Cristian Florea", "rep_title": "Rapporto Tasmota", "rep_found": "Dispositivi:",
                    "err_net": "Errore: IP non trovato."},
    "Français 🇫🇷": {"title": "Système Sauvegarde", "subnet": "Sous-réseau", "auto_ip": "Auto-Détection",
                    "user": "Utilisateur", "pass": "Mot de passe", "format": "Format:", "start": "LANCER",
                    "stop": "STOP", "open": "Ouvrir Dossier", "font": "Police:", "status_ready": "Prêt",
                    "status_scan": "Analyse...", "status_stop": "Arrêté!", "status_done": "Terminé!",
                    "opts": ["IP", "Nom", "Les deux"], "footer": "Créé par Cristian Florea", "rep_title": "Rapport",
                    "rep_found": "Trouvés:", "err_net": "Erreur IP."},
    "Deutsch 🇩🇪": {"title": "Backup System", "subnet": "Subnetz", "auto_ip": "Auto-Erkennung", "user": "Benutzer",
                   "pass": "Passwort", "format": "Format:", "start": "STARTEN", "stop": "STOPP",
                   "open": "Ordner öffnen", "font": "Schriftart:", "status_ready": "Bereit",
                   "status_scan": "Scannen...", "status_stop": "Gestopped!", "status_done": "Fertig!",
                   "opts": ["Nur IP", "Name", "Beides"], "footer": "Erstellt von Cristian Florea",
                   "rep_title": "Bericht", "rep_found": "Gefunden:", "err_net": "IP Fehler."},
    "Español 🇪🇸": {"title": "Sistema Respaldo", "subnet": "Subred", "auto_ip": "Auto-Detección", "user": "Usuario",
                   "pass": "Clave", "format": "Format:", "start": "INICIAR", "stop": "PARAR", "open": "Abrir",
                   "font": "Fuente:", "status_ready": "Listo", "status_scan": "Buscando...", "status_stop": "Parado!",
                   "status_done": "Hecho!", "opts": ["Solo IP", "Nombre", "Ambos"],
                   "footer": "Creado por Cristian Florea", "rep_title": "Informe", "rep_found": "Encontrados:",
                   "err_net": "Error de IP."},
    "Polski 🇵🇱": {"title": "System Kopii", "subnet": "Podsieć", "auto_ip": "Auto-Wykrywanie", "user": "Użytkownik",
                  "pass": "Hasło", "format": "Format:", "start": "START", "stop": "STOP", "open": "Otwórz",
                  "font": "Czcionka:", "status_ready": "Gotowy", "status_scan": "Skanowanie...",
                  "status_stop": "Zatrzymany!", "status_done": "Gotowe!", "opts": ["Tylko IP", "Nazwa", "Oba"],
                  "footer": "Stworzone przez Cristian Florea", "rep_title": "Raport", "rep_found": "Znaleziono:",
                  "err_net": "Błąd IP."}
}

FONTS = ["Arial", "Courier New", "Verdana", "Times New Roman", "Georgia", "Impact", "Comic Sans MS", "Trebuchet MS",
         "Lucida Console", "Tahoma"]


class TasmotaBackupApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tasmota Backup Tool V 1.0.2")
        self.geometry("700x950")

        try:
            self.iconbitmap("icon.ico")
        except:
            pass

        self.stop_event = threading.Event()
        self.auto_ip_var = tk.BooleanVar(value=True)

    
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=10, fill="x", padx=20)

        self.clock_label = ctk.CTkLabel(self.top_frame, text="", font=("Arial", 14, "bold"))
        self.clock_label.pack(side="left", padx=15)
        self.update_clock()

        self.lang_menu = ctk.CTkOptionMenu(self.top_frame, values=list(LANGUAGES.keys()), command=self.update_ui_text)
        self.lang_menu.pack(side="right", padx=5)
        self.lang_menu.set("Română 🇷🇴")

        self.theme_menu = ctk.CTkOptionMenu(self.top_frame, values=["Dark", "Light"], command=self.change_system_theme)
        self.theme_menu.pack(side="right", padx=5)

        
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(pady=10, fill="both", expand=True, padx=20)

        self.label_title = ctk.CTkLabel(self.main_container, text="", font=("Arial", 28, "bold"))
        self.label_title.pack(pady=15)

        self.ctrl_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.ctrl_frame.pack(pady=5)
        self.font_label = ctk.CTkLabel(self.ctrl_frame, text="Font:")
        self.font_label.pack(side="left", padx=5)
        self.font_menu = ctk.CTkOptionMenu(self.ctrl_frame, values=FONTS, command=self.apply_font)
        self.font_menu.pack(side="left", padx=5)
        self.font_menu.set("Arial")

        # Container IP (Fixat pentru Tema Light/Dark)
        self.ip_container = ctk.CTkFrame(self.main_container)
        self.ip_container.pack(pady=10, padx=20, fill="x")

        self.ip_entry = ctk.CTkEntry(self.ip_container, width=350, height=40)
        self.ip_entry.pack(pady=(10, 5))

        self.auto_check = ctk.CTkCheckBox(self.ip_container, text="", variable=self.auto_ip_var,
                                          command=self.toggle_ip_entry)
        self.auto_check.pack(pady=(0, 10))

        self.user_entry = ctk.CTkEntry(self.main_container, width=350, height=40)
        self.user_entry.insert(0, "admin")
        self.user_entry.pack(pady=5)

        self.pass_entry = ctk.CTkEntry(self.main_container, show="*", width=350, height=40)
        self.pass_entry.pack(pady=5)

        self.label_mode = ctk.CTkLabel(self.main_container, text="")
        self.label_mode.pack(pady=5)
        self.mode_option = ctk.CTkOptionMenu(self.main_container, values=[], width=300)
        self.mode_option.pack(pady=5)

        self.btn_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.btn_frame.pack(pady=20)
        self.btn_start = ctk.CTkButton(self.btn_frame, text="START", command=self.start_backup, width=150, height=45)
        self.btn_start.pack(side="left", padx=10)
        self.btn_stop = ctk.CTkButton(self.btn_frame, text="STOP", command=self.stop_backup, fg_color="#C0392B",
                                      hover_color="#962D22", width=150, height=45)
        self.btn_stop.pack(side="left", padx=10)

        self.btn_open = ctk.CTkButton(self.main_container, text="Open Folder", command=self.open_folder)
        self.btn_open.pack(pady=5)

        self.status_label = ctk.CTkLabel(self.main_container, text="", font=("Arial", 16, "bold"))
        self.status_label.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self.main_container, width=600, height=200)
        self.textbox.pack(pady=10)

        self.footer = ctk.CTkLabel(self, text="", font=("Arial", 11, "italic"), text_color="gray")
        self.footer.pack(side="bottom", anchor="e", padx=20, pady=5)

        self.update_ui_text(self.lang_menu.get())
        self.toggle_ip_entry()
        self.apply_font("Arial")

    def toggle_ip_entry(self):
        
        if self.auto_ip_var.get():
            self.ip_entry.configure(state="disabled")
        else:
            self.ip_entry.configure(state="normal")

    def get_local_subnet(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return ".".join(local_ip.split(".")[:-1])
        except:
            return None

    def update_clock(self):
        self.clock_label.configure(text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.after(1000, self.update_clock)

    def change_system_theme(self, theme):
        ctk.set_appearance_mode(theme.lower())
        self.update_idletasks() 

    def apply_font(self, font_name):
        f_normal = (font_name, 14)
        f_bold = (font_name, 15, "bold")
        self.label_title.configure(font=(font_name, 28, "bold"))
        self.ip_entry.configure(font=f_normal)
        self.user_entry.configure(font=f_normal)
        self.pass_entry.configure(font=f_normal)
        self.textbox.configure(font=f_normal)
        self.btn_start.configure(font=f_bold)
        self.status_label.configure(font=f_bold)

    def update_ui_text(self, choice):
        l = LANGUAGES[choice]
        self.label_title.configure(text=l["title"])
        self.btn_start.configure(text=l["start"])
        self.btn_stop.configure(text=l["stop"])
        self.btn_open.configure(text=l["open"])
        self.label_mode.configure(text=l["format"])
        self.font_label.configure(text=l["font"])
        self.auto_check.configure(text=l["auto_ip"])
        self.status_label.configure(text=l["status_ready"])
        self.footer.configure(text=l["footer"])
        self.mode_option.configure(values=l["opts"])
        self.mode_option.set(l["opts"][2])

    def open_folder(self):
        path = os.path.abspath("backups")
        if not os.path.exists(path): os.makedirs(path)
        if os.name == 'nt':
            os.startfile(path)
        else:
            subprocess.Popen(['xdg-open', path])

    def stop_backup(self):
        self.stop_event.set()
        l = LANGUAGES[self.lang_menu.get()]
        self.status_label.configure(text=l["status_stop"], text_color="#E74C3C")

    def start_backup(self):
        l = LANGUAGES[self.lang_menu.get()]
        if self.auto_ip_var.get():
            subnet = self.get_local_subnet()
            if not subnet:
                self.status_label.configure(text=l["err_net"], text_color="#E74C3C")
                return
        else:
            subnet = self.ip_entry.get()

        self.stop_event.clear()
        self.btn_start.configure(state="disabled")
        self.textbox.delete("1.0", "end")
        threading.Thread(target=self.worker_process, args=(subnet,), daemon=True).start()

    def worker_process(self, subnet):
        lang_key = self.lang_menu.get()
        l = LANGUAGES[lang_key]
        user = self.user_entry.get()
        pwd = self.pass_entry.get()
        mode_val = self.mode_option.get()

        date_folder = datetime.now().strftime("%d%m%Y")
        target_dir = os.path.join("backups", date_folder)
        if not os.path.exists(target_dir): os.makedirs(target_dir)

        self.status_label.configure(text=l["status_scan"], text_color="#F39C12")
        success_count = 0
        report = []
        lock = threading.Lock()

        def download(ip):
            nonlocal success_count
            if self.stop_event.is_set(): return

            try:
                with socket.create_connection((ip, 80), timeout=0.8):
                    pass

                r = requests.get(f"http://{ip}/dl", auth=(user, pwd), timeout=5, stream=True)

                if r.status_code == 200:
                    cd = r.headers.get('Content-Disposition')
                    t_name = cd.split("filename=")[1].strip('"') if cd and "filename=" in cd else ""

                    if mode_val == l["opts"][0]:
                        fname = f"{ip}.dmp"
                    elif mode_val == l["opts"][1]:
                        fname = t_name if t_name else f"backup_{ip}.dmp"
                    else:
                        fname = t_name.replace(".dmp", f"_{ip}.dmp") if t_name else f"backup_{ip}.dmp"

                    with open(os.path.join(target_dir, fname), "wb") as f:
                        f.write(r.content)

                    with lock:
                        self.textbox.insert("end", f"✔ {ip} -> {fname}\n")
                        self.textbox.see("end")
                        success_count += 1
                        report.append(f"SUCCESS: {ip} | {fname}")
                elif r.status_code == 401:
                    with lock:
                        self.textbox.insert("end", f"⚠ {ip} -> Eroare: Utilizator/Parolă incorectă!\n")
            except:
                pass

        ips = [f"{subnet}.{i}" for i in range(1, 255)]

        with ThreadPoolExecutor(max_workers=50) as ex:
            ex.map(download, ips)

        report_path = os.path.join(target_dir, "report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"{l['rep_title']} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{l['rep_found']} {success_count}\n")
            f.write("-" * 40 + "\n")
            f.write("\n".join(report))

        if not self.stop_event.is_set():
            self.status_label.configure(text=l["status_done"], text_color="#2ECC71")
        self.btn_start.configure(state="normal")


if __name__ == "__main__":
    app = TasmotaBackupApp()
    app.mainloop()
