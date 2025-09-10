import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
from datetime import datetime

# --- MODÈLE (Model) ---
class DataStore:
    def __init__(self):
        # Utilisateurs par défaut
        self.users = [
            {'id': 1, 'username': 'admin', 'password': 'admin123', 'role': 'admin', 'prenom': 'Administrateur', 'telephone': '', 'adresse': '', 'photo_path': ''},
            {'id': 2, 'username': 'client', 'password': 'client123', 'role': 'client', 'prenom': 'Basma', 'telephone': '123456789', 'adresse': 'Tunis', 'photo_path': 'photos_clients/basma.png'}

        ]
        
        # Comptes par défaut
        self.accounts = [
            {'id': 1, 'user_id': 2, 'numero_compte': 'TN001', 'type_compte': 'Courant', 'solde': 5000.0},
            {'id': 2, 'user_id': 2, 'numero_compte': 'TN002', 'type_compte': 'Épargne', 'solde': 15000.0}
        ]
        
        # Activités par défaut
        self.activities = [
            {'id': 1, 'compte_id': 1, 'type_transaction': 'Dépôt', 'montant': 5000.0, 'description': 'Dépôt initial', 'date_transaction': datetime.now()},
            {'id': 2, 'compte_id': 2, 'type_transaction': 'Dépôt', 'montant': 15000.0, 'description': 'Dépôt initial', 'date_transaction': datetime.now()}
        ]
        
        # Compteurs pour les nouveaux IDs
        self.next_user_id = 3
        self.next_account_id = 3
        self.next_activity_id = 3

    def get_user(self, username):
        for user in self.users:
            if user['username'] == username:
                return user
        return None

    def get_clients(self):
        return [user for user in self.users if user['role'] == 'client']

    def get_client(self, user_id):
        for user in self.users:
            if user['id'] == int(user_id) and user['role'] == 'client':
                return user
        return None

    def add_client(self, username, password, prenom, telephone, adresse, photo_path):
        new_client = {
            'id': self.next_user_id,
            'username': username,
            'password': password,
            'role': 'client',
            'prenom': prenom,
            'telephone': telephone,
            'adresse': adresse,
            'photo_path': photo_path
        }
        self.users.append(new_client)
        self.next_user_id += 1
        return new_client['id']

    def update_client(self, user_id, username, prenom, telephone, adresse, photo_path):
        for user in self.users:
            if user['id'] == int(user_id) and user['role'] == 'client':
                user['username'] = username
                user['prenom'] = prenom
                user['telephone'] = telephone
                user['adresse'] = adresse
                user['photo_path'] = photo_path
                return True
        return False

    def delete_client(self, user_id):
        user_id = int(user_id)
        
        # Vérifier si le client a des comptes
        client_accounts = [acc for acc in self.accounts if acc['user_id'] == user_id]
        
        if client_accounts:
            # Supprimer toutes les activités de tous les comptes du client
            for account in client_accounts:
                self.activities = [act for act in self.activities if act['compte_id'] != account['id']]
            
            # Supprimer tous les comptes du client
            self.accounts = [acc for acc in self.accounts if acc['user_id'] != user_id]
        
        # Supprimer le client
        self.users = [user for user in self.users if not (user['id'] == user_id and user['role'] == 'client')]
        return True

    def get_accounts(self):
        result = []
        for account in self.accounts:
            user = next((u for u in self.users if u['id'] == account['user_id']), None)
            if user:
                result.append({
                    'id': account['id'],
                    'user_id': account['user_id'],
                    'numero_compte': account['numero_compte'],
                    'type_compte': account['type_compte'],
                    'solde': account['solde'],
                    'username': user['username'],
                    'prenom': user['prenom']
                })
        return result

    def get_account(self, account_id):
        for account in self.accounts:
            if account['id'] == int(account_id):
                return account
        return None

    def add_account(self, user_id, numero_compte, type_compte, solde):
        new_account = {
            'id': self.next_account_id,
            'user_id': int(user_id),
            'numero_compte': numero_compte,
            'type_compte': type_compte,
            'solde': float(solde)
        }
        self.accounts.append(new_account)
        self.next_account_id += 1
        return new_account['id']

    def update_account(self, account_id, user_id, numero_compte, type_compte, solde):
        for account in self.accounts:
            if account['id'] == int(account_id):
                account['user_id'] = int(user_id)
                account['numero_compte'] = numero_compte
                account['type_compte'] = type_compte
                account['solde'] = float(solde)
                return True
        return False

    def delete_account(self, account_id):
        account_id = int(account_id)
        
        # Vérifier si le compte existe
        account = next((acc for acc in self.accounts if acc['id'] == account_id), None)
        if not account:
            return False
        
        # Supprimer toutes les activités du compte
        self.activities = [act for act in self.activities if act['compte_id'] != account_id]
        
        # Supprimer le compte
        self.accounts = [acc for acc in self.accounts if acc['id'] != account_id]
        return True

    def get_activities(self, account_id):
        return [act for act in self.activities if act['compte_id'] == int(account_id)]

    def add_activity(self, compte_id, type_transaction, montant, description):
        new_activity = {
            'id': self.next_activity_id,
            'compte_id': int(compte_id),
            'type_transaction': type_transaction,
            'montant': float(montant),
            'description': description,
            'date_transaction': datetime.now()
        }
        self.activities.append(new_activity)
        self.next_activity_id += 1
        return new_activity['id']

    def update_account_solde(self, account_id, new_solde):
        for account in self.accounts:
            if account['id'] == int(account_id):
                account['solde'] = float(new_solde)
                return True
        return False

    def can_delete_client(self, user_id):
        """Vérifie si un client peut être supprimé"""
        user_id = int(user_id)
        
        # Vérifier si c'est un admin (ne pas supprimer les admins)
        user = next((u for u in self.users if u['id'] == user_id), None)
        if not user or user['role'] == 'admin':
            return False, "Impossible de supprimer un administrateur."
        
        # Vérifier si le client a des comptes avec des activités récentes
        client_accounts = [acc for acc in self.accounts if acc['user_id'] == user_id]
        if client_accounts:
            # Vérifier s'il y a des activités dans les 30 derniers jours
            from datetime import datetime, timedelta
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            recent_activities = []
            for account in client_accounts:
                account_activities = [act for act in self.activities if act['compte_id'] == account['id']]
                recent_activities.extend([act for act in account_activities if act['date_transaction'] > thirty_days_ago])
            
            if recent_activities:
                return False, f"Ce client a {len(recent_activities)} activité(s) récente(s). La suppression n'est pas autorisée."
        
        return True, "Client peut être supprimé."

    def can_delete_account(self, account_id):
        """Vérifie si un compte peut être supprimé"""
        account_id = int(account_id)
        
        account = next((acc for acc in self.accounts if acc['id'] == account_id), None)
        if not account:
            return False, "Compte introuvable."
        
        # Vérifier s'il y a des activités récentes (7 derniers jours)
        from datetime import datetime, timedelta
        seven_days_ago = datetime.now() - timedelta(days=7)
        
        recent_activities = [act for act in self.activities 
                           if act['compte_id'] == account_id and act['date_transaction'] > seven_days_ago]
        
        if recent_activities:
            return False, f"Ce compte a {len(recent_activities)} activité(s) récente(s). La suppression n'est pas autorisée."
        
        return True, "Compte peut être supprimé." 

# --- VUE + CONTRÔLEUR (View + Controller) ---
class BanqueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banque Zitouna - Application Desktop")
        self.root.geometry("1200x750")
        self.root.configure(bg="#f4f7f6")
        self.model = DataStore()  # Utilise DataStore au lieu de BanqueModel

        self.user_role = None
        self.user_id = None
        self.username = None

        self.client_photo_img = None
        self.bg_img = None
        self.bg_label = None
        self.bg_path = os.path.join('photos_clients', 'fon.jpg')
        self.root.bind('<Configure>', self.on_resize_bg)
        self.setup_styles()
        self.show_login()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        vert_zitouna = "#009639"
        gris_fond = "#f4f7f6"
        style.configure('TFrame', background=gris_fond)
        style.configure('TLabel', background=gris_fond, foreground="#222", font=('Segoe UI', 10))
        style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), foreground=vert_zitouna, background=gris_fond)
        style.configure('TButton', background=vert_zitouna, foreground="white", font=('Segoe UI', 10, 'bold'), borderwidth=0, relief="flat")
        style.map('TButton', background=[('active', '#007a4d')])
        style.configure('Card.TLabelframe', background="white", relief="raised", borderwidth=1)
        style.configure('Card.TLabelframe.Label', background="white", foreground=vert_zitouna, font=('Segoe UI', 12, 'bold'))
        style.configure('Treeview', font=('Segoe UI', 9), background="white", foreground="#222", fieldbackground="white")
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background=vert_zitouna, foreground="white")
        style.configure('Rounded.TFrame', background="white", relief="raised", borderwidth=1)
        style.configure('LoginCard.TFrame', background="white", relief="raised", borderwidth=1)

    def on_resize_bg(self, event):
        if not os.path.exists(self.bg_path):
            return
        w, h = self.root.winfo_width(), self.root.winfo_height()
        try:
            img = Image.open(self.bg_path).resize((w, h))
            self.bg_img = ImageTk.PhotoImage(img)
            if hasattr(self, 'bg_label') and self.bg_label:
                self.bg_label.config(image=self.bg_img)
            else:
                self.bg_label = tk.Label(self.root, image=self.bg_img, bg="#f4f7f6", bd=0)
                self.bg_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                self.bg_label.lower()
        except Exception as e:
            print(f"Erreur chargement image de fond dynamique: {e}")

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.bg_img = None
        self.bg_label = None
        if os.path.exists(self.bg_path):
            try:
                w, h = self.root.winfo_width(), self.root.winfo_height()
                if w < 100 or h < 100:
                    w, h = 1200, 750
                img = Image.open(self.bg_path).resize((w, h))
                self.bg_img = ImageTk.PhotoImage(img)
                self.bg_label = tk.Label(self.root, image=self.bg_img, bg="#f4f7f6", bd=0)
                self.bg_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                self.bg_label.lower()
            except Exception as e:
                print(f"Erreur chargement image de fond: {e}")

    # --- LOGIN ---
    def show_login(self):
        self.clear_root()
        
        # Frame principal avec navigation
        main_frame = tk.Frame(self.root, bg="white", bd=0, highlightthickness=0)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=500)
        main_frame.configure(highlightbackground="#ddd", highlightcolor="#ddd")
        main_frame.pack_propagate(False)
        
        shadow = tk.Frame(self.root, bg="#bbb", bd=0)
        shadow.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=460, height=510)
        shadow.lower(main_frame)
        
        # Boutons de navigation
        nav_frame = tk.Frame(main_frame, bg="white")
        nav_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.quick_login_btn = tk.Button(nav_frame, text="Connexion Rapide", 
                                        font=("Segoe UI", 10, "bold"), 
                                        bg="#009639", fg="white", relief="flat", bd=0, 
                                        padx=15, pady=8,
                                        activebackground="#007a4d", activeforeground="white",
                                        command=self.show_quick_login_section)
        self.quick_login_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 2))
        
        self.manual_login_btn = tk.Button(nav_frame, text="Connexion Manuelle", 
                                         font=("Segoe UI", 10, "bold"), 
                                         bg="#ddd", fg="#666", relief="flat", bd=0, 
                                         padx=15, pady=8,
                                         activebackground="#ccc", activeforeground="#333",
                                         command=self.show_manual_login_section)
        self.manual_login_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 5))
        
        # Container pour les sections
        self.section_container = tk.Frame(main_frame, bg="white")
        self.section_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Afficher la section de connexion rapide par défaut
        self.show_quick_login_section()
    
    def show_quick_login_section(self):
        """Affiche la section de connexion rapide avec les boutons admin/client"""
        # Mettre à jour les boutons de navigation
        self.quick_login_btn.config(bg="#009639", fg="white")
        self.manual_login_btn.config(bg="#ddd", fg="#666")
        
        # Nettoyer le container
        for widget in self.section_container.winfo_children():
            widget.destroy()
        
        # Logo
        if os.path.exists("logo_zitouna.png"):
            logo_img = Image.open("logo_zitouna.png").resize((80, 80))
            self.login_logo_img = ImageTk.PhotoImage(logo_img)
            tk.Label(self.section_container, image=self.login_logo_img, bg="white").pack(pady=(20, 10))
        
        # Titre
        tk.Label(self.section_container, text="Connexion Rapide", 
                font=("Segoe UI", 16, "bold"), fg="#009639", bg="white").pack(pady=(0, 20))
        
        # Boutons de connexion rapide
        btn_frame = tk.Frame(self.section_container, bg="white")
        btn_frame.pack(pady=10)
        
        # Bouton Admin
        admin_btn = tk.Button(btn_frame, text="🔐 Admin\nadmin / admin123", 
                             font=("Segoe UI", 11, "bold"), 
                             bg="#009639", fg="white", relief="flat", bd=0, 
                             padx=25, pady=15, width=18,
                             activebackground="#007a4d", activeforeground="white",
                             command=lambda: self.quick_login("admin", "admin123"))
        admin_btn.pack(pady=10)
        
        # Bouton Client
        client_btn = tk.Button(btn_frame, text="👤 Client\nclient / client123", 
                              font=("Segoe UI", 11, "bold"), 
                              bg="#007acc", fg="white", relief="flat", bd=0, 
                              padx=25, pady=15, width=18,
                              activebackground="#005a99", activeforeground="white",
                              command=lambda: self.quick_login("client", "client123"))
        client_btn.pack(pady=10)
    
    def show_manual_login_section(self):
        """Affiche la section de connexion manuelle avec le formulaire"""
        # Mettre à jour les boutons de navigation
        self.quick_login_btn.config(bg="#ddd", fg="#666")
        self.manual_login_btn.config(bg="#009639", fg="white")
        
        # Nettoyer le container
        for widget in self.section_container.winfo_children():
            widget.destroy()
        
        # Logo
        if os.path.exists("logo_zitouna.png"):
            logo_img = Image.open("logo_zitouna.png").resize((80, 80))
            self.login_logo_img = ImageTk.PhotoImage(logo_img)
            tk.Label(self.section_container, image=self.login_logo_img, bg="white").pack(pady=(20, 10))
        
        # Titre
        tk.Label(self.section_container, text="Connexion Manuelle", 
                font=("Segoe UI", 16, "bold"), fg="#009639", bg="white").pack(pady=(0, 20))
        
        # Formulaire de connexion
        form_frame = tk.Frame(self.section_container, bg="white")
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Nom d'utilisateur:", bg="white", font=("Segoe UI", 10)).pack(pady=5)
        self.login_username = ttk.Entry(form_frame, font=("Segoe UI", 10))
        self.login_username.pack(pady=5, ipadx=15, ipady=5)
        
        tk.Label(form_frame, text="Mot de passe:", bg="white", font=("Segoe UI", 10)).pack(pady=5)
        self.login_password = ttk.Entry(form_frame, show="*", font=("Segoe UI", 10))
        self.login_password.pack(pady=5, ipadx=15, ipady=5)
        
        # Bouton de connexion
        ttk.Button(form_frame, text="Se connecter", command=self.handle_login, 
                  style='TButton').pack(pady=20)

    def quick_login(self, username, password):
        """Connexion rapide avec les identifiants par défaut"""
        user = self.model.get_user(username)
        if not user:
            messagebox.showerror("Erreur", "Nom d'utilisateur incorrect.")
            return
        if user['password'] != password:
            messagebox.showerror("Erreur", "Mot de passe incorrect.")
            return

        self.user_role = user['role']
        self.user_id = user['id']
        self.username = user['username']
        messagebox.showinfo("Succès", f"Bienvenue {self.username} ({self.user_role})")
        self.show_dashboard()

    def handle_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        user = self.model.get_user(username)
        if not user:
            messagebox.showerror("Erreur", "Nom d'utilisateur incorrect.")
            return
        if user['password'] != password:
            messagebox.showerror("Erreur", "Mot de passe incorrect.")
            return

        self.user_role = user['role']
        self.user_id = user['id']
        self.username = user['username']
        messagebox.showinfo("Succès", f"Bienvenue {self.username} ({self.user_role})")
        self.show_dashboard()

    # --- DASHBOARD ---
    def show_dashboard(self):
        self.clear_root()
        canvas = tk.Canvas(self.root, bg="#f4f7f6", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb_main = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        vsb_main.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=vsb_main.set)
        
        scrollable_frame = ttk.Frame(canvas, style='TFrame')
        scrollable_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", on_configure)
        def resize_canvas(event):
            canvas.itemconfig(scrollable_frame_id, width=event.width)
        canvas.bind("<Configure>", resize_canvas)
        
        header = ttk.Frame(scrollable_frame, padding=15, style='TFrame')
        header.pack(fill=tk.X, padx=20, pady=(20, 10))
        if os.path.exists("logo_zitouna.png"):
            logo_img = Image.open("logo_zitouna.png").resize((40, 40))
            self.header_logo_img = ImageTk.PhotoImage(logo_img)
            tk.Label(header, image=self.header_logo_img, bg="#f4f7f6").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(header, text="Banque Zitouna - Dashboard", style='Header.TLabel').pack(side=tk.LEFT)
        nb_clients = len(self.model.get_clients())
        nb_comptes = len(self.model.get_accounts())
        stats = f"Clients: {nb_clients}   |   Comptes: {nb_comptes}"
        ttk.Label(header, text=stats, font=("Segoe UI", 11, "bold"), foreground="#009639", background="#f4f7f6").pack(side=tk.LEFT, padx=20)
        ttk.Button(header, text="Déconnexion", command=self.show_login).pack(side=tk.RIGHT)
        
        main_frame = ttk.Frame(scrollable_frame, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        main_frame.grid_columnconfigure(0, weight=7)
        main_frame.grid_columnconfigure(1, weight=13)
        
        client_frame = ttk.LabelFrame(main_frame, text="Gestion Clients", style='Card.TLabelframe', padding=15)
        client_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5), pady=0)
        
        account_frame = ttk.LabelFrame(main_frame, text="Gestion Comptes & Activités", style='Card.TLabelframe', padding=15)
        account_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0), pady=0)
        
        self.build_client_section(client_frame, show_activities=True)
        self.build_account_section(account_frame)
        
        self.selected_account_id = None
        
        if self.user_role == 'client':
            self.show_client_dashboard()

    # --- CLIENTS ---
    def build_client_section(self, parent, show_activities=True):
        form_frame = ttk.Frame(parent)
        form_frame.pack(fill=tk.X, pady=5)
        labels = ['Username', 'Mot de passe', 'Prénom', 'Téléphone', 'Adresse', 'Photo']
        self.client_vars = {}
        self.client_entries = {}
        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=label + ":").grid(row=i, column=0, sticky='w', pady=2, padx=2)
            if label == 'Photo':
                self.client_vars['photo'] = tk.StringVar()
                entry = ttk.Entry(form_frame, textvariable=self.client_vars['photo'])
                entry.grid(row=i, column=1, sticky='ew', pady=2, padx=2)
                self.client_entries['photo'] = entry
                ttk.Button(form_frame, text="Parcourir", command=self.upload_client_photo).grid(row=i, column=2, padx=5)
            elif label == 'Mot de passe':
                entry = ttk.Entry(form_frame, show="*")
                entry.grid(row=i, column=1, sticky='ew', pady=2, padx=2)
                self.client_entries['password'] = entry
            else:
                entry = ttk.Entry(form_frame)
                entry.grid(row=i, column=1, sticky='ew', pady=2, padx=2)
                self.client_entries[label.lower()] = entry
        form_frame.columnconfigure(1, weight=1)
        
        self.client_photo_preview = ttk.Label(form_frame)
        self.client_photo_preview.grid(row=6, column=0, columnspan=3, pady=5)
        
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Ajouter", command=self.add_client).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Modifier", command=self.modify_client).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Supprimer", command=self.delete_client).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Effacer", command=self.clear_client_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Info Suppression", command=self.show_delete_info).pack(side=tk.LEFT, padx=5)
        
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        columns = ('id', 'username', 'prenom', 'telephone', 'adresse', 'photo_path', 'role')
        self.client_tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='browse')
        vsb_clients = ttk.Scrollbar(list_frame, orient="vertical", command=self.client_tree.yview)
        self.client_tree.configure(yscrollcommand=vsb_clients.set)
        for col in columns:
            self.client_tree.heading(col, text=col.capitalize())
            self.client_tree.column(col, width=120)
        self.client_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        vsb_clients.pack(side=tk.RIGHT, fill=tk.Y)
        self.client_tree.bind('<<TreeviewSelect>>', self.on_client_select)
        self.selected_client_id = None
        self.load_clients()

    def upload_client_photo(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.gif")])
        if path:
            os.makedirs('photos_clients', exist_ok=True)
            filename = os.path.basename(path)
            dest = os.path.join('photos_clients', filename)
            try:
                img = Image.open(path)
                img.save(dest)
                self.client_vars['photo'].set(dest)
                img.thumbnail((100, 100))
                self.client_photo_img = ImageTk.PhotoImage(img)
                self.client_photo_preview.config(image=self.client_photo_img)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger l'image: {e}")

    def add_client(self):
        username = self.client_entries['username'].get().strip()
        password = self.client_entries['password'].get().strip() or 'clientpass'
        prenom = self.client_entries['prénom'].get().strip()
        telephone = self.client_entries['téléphone'].get().strip()
        adresse = self.client_entries['adresse'].get().strip()
        photo = self.client_vars['photo'].get().strip()

        if not username or not password or not prenom:
            messagebox.showerror("Erreur", "Username, mot de passe et prénom obligatoires.")
            return

        if self.model.add_client(username, password, prenom, telephone, adresse, photo):
            messagebox.showinfo("Succès", "Client ajouté.")
            self.load_clients()
            self.load_clients_combobox()
            self.clear_client_form()
        else:
            messagebox.showerror("Erreur", "Erreur lors de l'ajout du client.")

    def load_clients(self):
        for row in self.client_tree.get_children():
            self.client_tree.delete(row)
        clients = self.model.get_clients()
        if clients:
            for c in clients:
                self.client_tree.insert('', tk.END, iid=c['id'], values=(c['id'], c['username'], c['prenom'], c['telephone'], c['adresse'], c['photo_path'], c['role']))

    def on_client_select(self, event):
        sel = self.client_tree.selection()
        if sel:
            uid = sel[0]
            client = self.model.get_client(uid)
            if client:
                self.selected_client_id = uid
                self.client_entries['username'].delete(0, tk.END)
                self.client_entries['username'].insert(0, client['username'])
                self.client_entries['password'].delete(0, tk.END)
                self.client_entries['password'].insert(0, '')
                self.client_entries['prénom'].delete(0, tk.END)
                self.client_entries['prénom'].insert(0, client['prenom'])
                self.client_entries['téléphone'].delete(0, tk.END)
                self.client_entries['téléphone'].insert(0, client['telephone'] or '')
                self.client_entries['adresse'].delete(0, tk.END)
                self.client_entries['adresse'].insert(0, client['adresse'] or '')
                self.client_vars['photo'].set(client['photo_path'] if client['photo_path'] else "")
                
                if client['photo_path'] and os.path.exists(client['photo_path']):
                    try:
                        img = Image.open(client['photo_path'])
                        img.thumbnail((100, 100))
                        self.client_photo_img = ImageTk.PhotoImage(img)
                        self.client_photo_preview.config(image=self.client_photo_img)
                    except Exception:
                        self.client_photo_preview.config(image='')
                else:
                    self.client_photo_preview.config(image='')
            else:
                self.clear_client_form()

    def modify_client(self):
        if not self.selected_client_id:
            messagebox.showerror("Erreur", "Sélectionnez un client à modifier.")
            return
        username = self.client_entries['username'].get().strip()
        prenom = self.client_entries['prénom'].get().strip()
        telephone = self.client_entries['téléphone'].get().strip()
        adresse = self.client_entries['adresse'].get().strip()
        photo = self.client_vars['photo'].get().strip()
        if not username or not prenom:
            messagebox.showerror("Erreur", "Username et prénom obligatoires.")
            return
        if self.model.update_client(self.selected_client_id, username, prenom, telephone, adresse, photo):
            messagebox.showinfo("Succès", "Client modifié.")
            self.load_clients()
            self.load_clients_combobox()
            self.clear_client_form()
        else:
            messagebox.showerror("Erreur", "Erreur lors de la modification.")

    def delete_client(self):
        if not self.selected_client_id:
            messagebox.showerror("Erreur", "Sélectionnez un client à supprimer.")
            return
        
        # Vérifier si le client peut être supprimé
        can_delete, message = self.model.can_delete_client(self.selected_client_id)
        if not can_delete:
            messagebox.showerror("Suppression impossible", message)
            return
        
        # Récupérer les informations du client
        client = self.model.get_client(self.selected_client_id)
        if not client:
            messagebox.showerror("Erreur", "Client introuvable.")
            return
        
        # Vérifier si le client a des comptes
        client_accounts = [acc for acc in self.model.accounts if acc['user_id'] == int(self.selected_client_id)]
        
        # Préparer le message de confirmation
        if client_accounts:
            nb_comptes = len(client_accounts)
            total_activites = 0
            for account in client_accounts:
                account_activities = [act for act in self.model.activities if act['compte_id'] == account['id']]
                total_activites += len(account_activities)
            
            message = f"⚠️ ATTENTION : Suppression en cascade\n\n"
            message += f"Client : {client['username']} ({client['prenom']})\n"
            message += f"Comptes : {nb_comptes} compte(s)\n"
            message += f"Activités : {total_activites} activité(s)\n\n"
            message += f"Cette action supprimera définitivement :\n"
            message += f"• Le client et ses informations\n"
            message += f"• Tous ses comptes bancaires\n"
            message += f"• Toutes les activités associées\n\n"
            message += f"Êtes-vous sûr de vouloir continuer ?"
        else:
            message = f"Supprimer le client {client['username']} ({client['prenom']}) ?\n\nCe client n'a aucun compte associé."
        
        if messagebox.askyesno("Confirmation de suppression", message):
            if self.model.delete_client(self.selected_client_id):
                messagebox.showinfo("Succès", "Client et toutes ses données supprimés avec succès.")
                self.load_clients()
                self.load_clients_combobox()
                self.clear_client_form()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la suppression.")

    def clear_client_form(self):
        self.selected_client_id = None
        for key in ['username', 'password', 'prénom', 'téléphone', 'adresse']:
            self.client_entries[key].delete(0, tk.END)
        self.client_vars['photo'].set("")
        self.client_photo_preview.config(image='')

    def show_delete_info(self):
        """Affiche les informations sur les contraintes de suppression"""
        if not self.selected_client_id:
            messagebox.showinfo("Information", "Sélectionnez d'abord un client pour voir les informations de suppression.")
            return
        
        client = self.model.get_client(self.selected_client_id)
        if not client:
            messagebox.showerror("Erreur", "Client introuvable.")
            return
        
        # Vérifier les contraintes
        can_delete, message = self.model.can_delete_client(self.selected_client_id)
        
        # Récupérer les statistiques
        client_accounts = [acc for acc in self.model.accounts if acc['user_id'] == int(self.selected_client_id)]
        nb_comptes = len(client_accounts)
        total_activites = 0
        
        for account in client_accounts:
            account_activities = [act for act in self.model.activities if act['compte_id'] == account['id']]
            total_activites += len(account_activities)
        
        # Préparer le message d'information
        info_message = f"📊 INFORMATIONS DE SUPPRESSION\n\n"
        info_message += f"Client : {client['username']} ({client['prenom']})\n"
        info_message += f"Comptes : {nb_comptes} compte(s)\n"
        info_message += f"Activités totales : {total_activites} activité(s)\n\n"
        
        if can_delete:
            info_message += f"✅ SUPPRESSION AUTORISÉE\n\n"
            info_message += f"Ce client peut être supprimé car :\n"
            info_message += f"• Aucune activité récente (30 derniers jours)\n"
            info_message += f"• N'est pas un administrateur\n\n"
            info_message += f"La suppression supprimera :\n"
            info_message += f"• Le client et ses informations\n"
            info_message += f"• Tous ses comptes ({nb_comptes})\n"
            info_message += f"• Toutes ses activités ({total_activites})"
        else:
            info_message += f"❌ SUPPRESSION IMPOSSIBLE\n\n"
            info_message += f"Raison : {message}\n\n"
            info_message += f"Pour permettre la suppression :\n"
            info_message += f"• Attendez que les activités récentes soient plus anciennes\n"
            info_message += f"• Ou contactez l'administrateur"
        
        messagebox.showinfo("Contraintes de Suppression", info_message)

    # --- COMPTES & ACTIVITÉS ---
    def build_account_section(self, parent):
        form_frame = ttk.Frame(parent)
        form_frame.pack(fill=tk.X, pady=5)

        ttk.Label(form_frame, text="Client:").grid(row=0, column=0, sticky='w', pady=2)
        self.account_client_cb = ttk.Combobox(form_frame, state='readonly')
        self.account_client_cb.grid(row=0, column=1, sticky='ew', pady=2)

        ttk.Label(form_frame, text="Numéro Compte:").grid(row=1, column=0, sticky='w', pady=2)
        self.account_num_entry = ttk.Entry(form_frame)
        self.account_num_entry.grid(row=1, column=1, sticky='ew', pady=2)

        ttk.Label(form_frame, text="Type Compte:").grid(row=2, column=0, sticky='w', pady=2)
        self.account_type_cb = ttk.Combobox(form_frame, values=["Courant", "Epargne"], state='readonly')
        self.account_type_cb.grid(row=2, column=1, sticky='ew', pady=2)

        ttk.Label(form_frame, text="Solde Initial:").grid(row=3, column=0, sticky='w', pady=2)
        self.account_solde_entry = ttk.Entry(form_frame)
        self.account_solde_entry.grid(row=3, column=1, sticky='ew', pady=2)

        form_frame.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Ajouter", command=self.add_account).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Modifier", command=self.modify_account).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Supprimer", command=self.delete_account).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Effacer", command=self.clear_account_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Info Suppression", command=self.show_account_delete_info).pack(side=tk.LEFT, padx=5)

        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns = ('client', 'numero_compte', 'type_compte', 'solde')
        self.account_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        vsb_accounts = ttk.Scrollbar(list_frame, orient="vertical", command=self.account_tree.yview)
        self.account_tree.configure(yscrollcommand=vsb_accounts.set)
        for col in columns:
            self.account_tree.heading(col, text=col.replace('_', ' ').capitalize())
            self.account_tree.column(col, width=100)
        self.account_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb_accounts.pack(side=tk.RIGHT, fill=tk.Y)
        self.account_tree.bind('<<TreeviewSelect>>', self.on_account_select_admin)

        act_frame = ttk.LabelFrame(parent, text="Ajouter Activité", padding=10)
        act_frame.pack(fill=tk.X, pady=5)

        ttk.Label(act_frame, text="Type:").grid(row=0, column=0, sticky='w', pady=2)
        self.act_type_cb = ttk.Combobox(act_frame, values=["Versement", "Retrait"], state='readonly')
        self.act_type_cb.grid(row=0, column=1, sticky='ew', pady=2)

        ttk.Label(act_frame, text="Montant:").grid(row=1, column=0, sticky='w', pady=2)
        self.act_montant_entry = ttk.Entry(act_frame)
        self.act_montant_entry.grid(row=1, column=1, sticky='ew', pady=2)

        ttk.Label(act_frame, text="Description:").grid(row=2, column=0, sticky='w', pady=2)
        self.act_desc_entry = ttk.Entry(act_frame)
        self.act_desc_entry.grid(row=2, column=1, sticky='ew', pady=2)

        act_frame.columnconfigure(1, weight=1)

        ttk.Button(act_frame, text="Enregistrer", command=self.add_activity).grid(row=3, column=0, columnspan=2, pady=10)

        act_list_frame = ttk.Frame(parent)
        act_list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns_act = ('type_transaction', 'montant', 'date_transaction', 'description')
        self.activity_tree = ttk.Treeview(act_list_frame, columns=columns_act, show='headings')
        vsb_acts = ttk.Scrollbar(act_list_frame, orient="vertical", command=self.activity_tree.yview)
        hsb_acts = ttk.Scrollbar(act_list_frame, orient="horizontal", command=self.activity_tree.xview)
        self.activity_tree.configure(yscrollcommand=vsb_acts.set, xscrollcommand=hsb_acts.set)
        for col in columns_act:
            self.activity_tree.heading(col, text=col.replace('_', ' ').capitalize())
            if col == 'description':
                self.activity_tree.column(col, width=300)
            else:
                self.activity_tree.column(col, width=120)
        self.activity_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb_acts.pack(side=tk.RIGHT, fill=tk.Y)
        hsb_acts.pack(side=tk.BOTTOM, fill=tk.X)

        self.selected_account_id = None
        self.load_clients_combobox()
        self.load_accounts()

    def load_clients_combobox(self):
        clients = self.model.get_clients()
        self.client_map = {}
        if clients:
            names = []
            for c in clients:
                name = f"{c['username']} {c['prenom']}"
                names.append(name)
                self.client_map[name] = c['id']
            self.account_client_cb['values'] = names
        else:
            self.account_client_cb['values'] = []

    def add_account(self):
        client_name = self.account_client_cb.get()
        user_id = self.client_map.get(client_name)
        numero = self.account_num_entry.get().strip()
        type_compte = self.account_type_cb.get()
        solde = self.account_solde_entry.get().strip()
        if not user_id or not numero or not type_compte or not solde:
            messagebox.showerror("Erreur", "Tous les champs du compte sont obligatoires.")
            return
        try:
            solde = float(solde)
            if solde < 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Erreur", "Solde doit être un nombre positif.")
            return
        new_account_id = self.model.add_account(user_id, numero, type_compte, solde)
        if new_account_id:
            messagebox.showinfo("Succès", "Compte ajouté.")
            self.load_accounts()
            self.selected_account_id = str(new_account_id)
            self.account_tree.selection_set(str(new_account_id))
            self.load_activities(new_account_id)
            self.clear_account_form()
        else:
            messagebox.showerror("Erreur", "Erreur lors de l'ajout du compte.")

    def load_accounts(self):
        current_selection = self.account_tree.selection()
        selected_id = None
        if current_selection:
            selected_id = current_selection[0]
        
        for row in self.account_tree.get_children():
            self.account_tree.delete(row)
        accounts = self.model.get_accounts()
        if accounts:
            for acc in accounts:
                client_name = f"{acc['username']} {acc['prenom']}"
                self.account_tree.insert('', tk.END, iid=str(acc['id']),
                                         values=(client_name, acc['numero_compte'], acc['type_compte'], f"{acc['solde']:.2f} DH"))
        
        if selected_id and self.account_tree.exists(selected_id):
            self.account_tree.selection_set(selected_id)
            self.load_activities(selected_id)

    def on_account_select_admin(self, event):
        sel = self.account_tree.selection()
        if sel:
            aid = sel[0]
            self.selected_account_id = aid
            self.load_activities(aid)
            acc = self.model.get_account(aid)
            if acc:
                client_name = None
                clients = self.model.get_clients()
                for c in clients:
                    if c['id'] == acc['user_id']:
                        client_name = f"{c['username']} {c['prenom']}"
                        break
                if client_name:
                    self.account_client_cb.set(client_name)
                else:
                    self.account_client_cb.set("")
                self.account_num_entry.delete(0, tk.END)
                self.account_num_entry.insert(0, acc['numero_compte'])
                self.account_type_cb.set(acc['type_compte'])
                self.account_solde_entry.delete(0, tk.END)
                self.account_solde_entry.insert(0, str(acc['solde']))
            else:
                self.selected_account_id = None
                self.clear_activity_list()
                self.clear_account_form()
        else:
            self.selected_account_id = None
            self.clear_activity_list()
            self.clear_account_form()

    def modify_account(self):
        if not self.selected_account_id:
            messagebox.showerror("Erreur", "Sélectionnez un compte à modifier.")
            return
        client_name = self.account_client_cb.get()
        user_id = self.client_map.get(client_name)
        numero = self.account_num_entry.get().strip()
        type_compte = self.account_type_cb.get()
        solde = self.account_solde_entry.get().strip()
        if not user_id or not numero or not type_compte or not solde:
            messagebox.showerror("Erreur", "Tous les champs du compte sont obligatoires.")
            return
        try:
            solde = float(solde)
        except Exception:
            messagebox.showerror("Erreur", "Solde doit être un nombre.")
            return
        if self.model.update_account(self.selected_account_id, user_id, numero, type_compte, solde):
            messagebox.showinfo("Succès", "Compte modifié.")
            self.load_accounts()
            acc = self.model.get_account(self.selected_account_id)
            if acc:
                client_name = None
                clients = self.model.get_clients()
                for c in clients:
                    if c['id'] == acc['user_id']:
                        client_name = f"{c['username']} {c['prenom']}"
                        break
                if client_name:
                    self.account_client_cb.set(client_name)
                self.account_num_entry.delete(0, tk.END)
                self.account_num_entry.insert(0, acc['numero_compte'])
                self.account_type_cb.set(acc['type_compte'])
                self.account_solde_entry.delete(0, tk.END)
                self.account_solde_entry.insert(0, str(acc['solde']))
        else:
            messagebox.showerror("Erreur", "Erreur lors de la modification.")

    def delete_account(self):
        if not self.selected_account_id:
            messagebox.showerror("Erreur", "Sélectionnez un compte à supprimer.")
            return
        
        # Vérifier si le compte peut être supprimé
        can_delete, message = self.model.can_delete_account(self.selected_account_id)
        if not can_delete:
            messagebox.showerror("Suppression impossible", message)
            return
        
        # Récupérer les informations du compte
        account = self.model.get_account(self.selected_account_id)
        if not account:
            messagebox.showerror("Erreur", "Compte introuvable.")
            return
        
        # Récupérer les informations du client
        client = self.model.get_client(account['user_id'])
        client_name = f"{client['username']} {client['prenom']}" if client else "Client inconnu"
        
        # Vérifier les activités du compte
        account_activities = [act for act in self.model.activities if act['compte_id'] == int(self.selected_account_id)]
        nb_activites = len(account_activities)
        
        # Préparer le message de confirmation
        message = f"⚠️ ATTENTION : Suppression en cascade\n\n"
        message += f"Compte : {account['numero_compte']}\n"
        message += f"Type : {account['type_compte']}\n"
        message += f"Solde : {account['solde']:.2f} DH\n"
        message += f"Client : {client_name}\n"
        message += f"Activités : {nb_activites} activité(s)\n\n"
        message += f"Cette action supprimera définitivement :\n"
        message += f"• Le compte bancaire\n"
        message += f"• Toutes les activités associées\n\n"
        message += f"Êtes-vous sûr de vouloir continuer ?"
        
        if messagebox.askyesno("Confirmation de suppression", message):
            if self.model.delete_account(self.selected_account_id):
                messagebox.showinfo("Succès", "Compte et toutes ses activités supprimés avec succès.")
                self.load_accounts()
                self.clear_account_form()
                self.clear_activity_list()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la suppression.")

    def clear_account_form(self):
        self.selected_account_id = None
        self.account_client_cb.set("")
        self.account_num_entry.delete(0, tk.END)
        self.account_type_cb.set("")
        self.account_solde_entry.delete(0, tk.END)
        self.clear_activity_form()
        self.clear_activity_list()

    def add_activity(self):
        if not self.selected_account_id:
            messagebox.showerror("Erreur", "Sélectionnez un compte pour ajouter une activité.")
            return
        type_act = self.act_type_cb.get()
        montant = self.act_montant_entry.get().strip()
        desc = self.act_desc_entry.get().strip()

        if not type_act or not montant:
            messagebox.showerror("Erreur", "Type et montant obligatoires.")
            return
        try:
            montant = float(montant)
            if montant <= 0:
                raise ValueError
        except:
            messagebox.showerror("Erreur", "Montant doit être un nombre positif.")
            return

        acc = self.model.get_account(self.selected_account_id)
        if not acc:
            messagebox.showerror("Erreur", "Compte introuvable.")
            return
        solde = acc['solde']

        if type_act == 'Retrait' and montant > solde:
            messagebox.showerror("Erreur", "Solde insuffisant pour ce retrait.")
            return

        if self.model.add_activity(self.selected_account_id, type_act, montant, desc) is None:
            messagebox.showerror("Erreur", "Erreur lors de l'ajout de l'activité.")
            return

        new_solde = solde + montant if type_act == 'Versement' else solde - montant
        if self.model.update_account_solde(self.selected_account_id, new_solde) is None:
            messagebox.showerror("Erreur", "Erreur lors de la mise à jour du solde.")
            return

        messagebox.showinfo("Succès", "Activité ajoutée.")
        self.load_activities(self.selected_account_id)
        self.load_accounts()
        self.clear_activity_form()

    def load_activities(self, account_id):
        self.clear_activity_list()
        acts = self.model.get_activities(account_id)
        if acts:
            for a in acts:
                self.activity_tree.insert('', tk.END, values=(a['type_transaction'], f"{a['montant']:.2f} DH", a['date_transaction'].strftime("%Y-%m-%d %H:%M"), a['description']))

    def clear_activity_list(self):
        for row in self.activity_tree.get_children():
            self.activity_tree.delete(row)

    def clear_activity_form(self):
        self.act_type_cb.set("")
        self.act_montant_entry.delete(0, tk.END)
        self.act_desc_entry.delete(0, tk.END)

    def show_account_delete_info(self):
        """Affiche les informations sur les contraintes de suppression d'un compte"""
        if not self.selected_account_id:
            messagebox.showinfo("Information", "Sélectionnez d'abord un compte pour voir les informations de suppression.")
            return
        
        account = self.model.get_account(self.selected_account_id)
        if not account:
            messagebox.showerror("Erreur", "Compte introuvable.")
            return
        
        # Vérifier les contraintes
        can_delete, message = self.model.can_delete_account(self.selected_account_id)
        
        # Récupérer les informations du client
        client = self.model.get_client(account['user_id'])
        client_name = f"{client['username']} {client['prenom']}" if client else "Client inconnu"
        
        # Récupérer les statistiques
        account_activities = [act for act in self.model.activities if act['compte_id'] == int(self.selected_account_id)]
        nb_activites = len(account_activities)
        
        # Préparer le message d'information
        info_message = f"📊 INFORMATIONS DE SUPPRESSION\n\n"
        info_message += f"Compte : {account['numero_compte']}\n"
        info_message += f"Type : {account['type_compte']}\n"
        info_message += f"Solde : {account['solde']:.2f} DH\n"
        info_message += f"Client : {client_name}\n"
        info_message += f"Activités : {nb_activites} activité(s)\n\n"
        
        if can_delete:
            info_message += f"✅ SUPPRESSION AUTORISÉE\n\n"
            info_message += f"Ce compte peut être supprimé car :\n"
            info_message += f"• Aucune activité récente (7 derniers jours)\n\n"
            info_message += f"La suppression supprimera :\n"
            info_message += f"• Le compte bancaire\n"
            info_message += f"• Toutes ses activités ({nb_activites})"
        else:
            info_message += f"❌ SUPPRESSION IMPOSSIBLE\n\n"
            info_message += f"Raison : {message}\n\n"
            info_message += f"Pour permettre la suppression :\n"
            info_message += f"• Attendez que les activités récentes soient plus anciennes (7 jours)"
        
        messagebox.showinfo("Contraintes de Suppression", info_message)

    # --- DASHBOARD CLIENT (rôle client) ---
    def show_client_dashboard(self):
        self.clear_root()
        self.root.configure(bg="#e6f4ec")
        
        canvas = tk.Canvas(self.root, bg="#e6f4ec", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb_main = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        vsb_main.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=vsb_main.set)
        
        scrollable_frame = tk.Frame(canvas, bg="#e6f4ec")
        scrollable_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", on_configure)
        def resize_canvas(event):
            canvas.itemconfig(scrollable_frame_id, width=event.width)
        canvas.bind("<Configure>", resize_canvas)
        
        header = tk.Frame(scrollable_frame, bg="#ffffff", height=80, relief="flat", bd=0)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        logo_frame = tk.Frame(header, bg="#ffffff")
        logo_frame.pack(side=tk.LEFT, padx=(30, 0), pady=20)
        if os.path.exists("logo_zitouna.png"):
            logo_img = Image.open("logo_zitouna.png").resize((40, 40))
            self.header_logo_img = ImageTk.PhotoImage(logo_img)
            tk.Label(logo_frame, image=self.header_logo_img, bg="#ffffff").pack(side=tk.LEFT, padx=(0, 15))
        tk.Label(logo_frame, text="Banque Zitouna", font=("Segoe UI", 22, "bold"), fg="#009639", bg="#ffffff").pack(side=tk.LEFT, pady=(0,2))
        tk.Label(logo_frame, text="| Espace Client", font=("Segoe UI", 14), fg="#7f8c8d", bg="#ffffff").pack(side=tk.LEFT, padx=(10, 0), pady=(0,2))
        nav_frame = tk.Frame(header, bg="#ffffff")
        nav_frame.pack(side=tk.RIGHT, padx=(0, 30), pady=20)
        tk.Label(nav_frame, text=f"Bienvenue, {self.username}", font=("Segoe UI", 12), fg="#7f8c8d", bg="#ffffff").pack(side=tk.LEFT, padx=(0, 20))
        logout_btn = tk.Button(nav_frame, text="Déconnexion", font=("Segoe UI", 10, "bold"), 
                              bg="#009639", fg="white", relief="flat", bd=0, padx=20, pady=8,
                              activebackground="#006b2d", activeforeground="white",
                              command=self.show_login)
        logout_btn.pack(side=tk.LEFT)
        
        main_container = tk.Frame(scrollable_frame, bg="#e6f4ec")
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Récupérer infos client
        client = self.model.get_user(self.username)
        if not client:
            error_card = tk.Frame(main_container, bg="#ffffff", relief="flat", bd=0)
            error_card.pack(pady=60, ipadx=40, ipady=30)
            tk.Label(error_card, text="❌ Profil introuvable", font=("Segoe UI", 18, "bold"), 
                    fg="#e74c3c", bg="#ffffff").pack(pady=(0, 10))
            tk.Label(error_card, text="Impossible de récupérer les informations du client.", 
                    font=("Segoe UI", 12), fg="#7f8c8d", bg="#ffffff").pack()
            return
        
        # Section profil
        profile_section = tk.Frame(main_container, bg="#ffffff", relief="solid", bd=2, highlightbackground="#009639", highlightcolor="#009639", highlightthickness=2)
        profile_section.pack(pady=(0, 30), padx=0, ipadx=40, ipady=25)
        profile_section.grid_columnconfigure(0, weight=1)
        profile_section.grid_rowconfigure(0, weight=1)
        avatar_info_frame = tk.Frame(profile_section, bg="#ffffff")
        avatar_info_frame.pack(anchor='center', pady=0)
        avatar_frame = tk.Frame(avatar_info_frame, bg="#ffffff")
        avatar_frame.pack(side=tk.TOP, pady=(0, 10))
        avatar_size = 80
        border_size = 3
        from PIL import ImageDraw
        if client['photo_path'] and os.path.exists(client['photo_path']):
            try:
                img = Image.open(client['photo_path']).resize((avatar_size, avatar_size)).convert('RGBA')
                mask = Image.new('L', (avatar_size, avatar_size), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
                img.putalpha(mask)
                border = Image.new('RGBA', (avatar_size+border_size*2, avatar_size+border_size*2), (0,0,0,0))
                draw = ImageDraw.Draw(border)
                draw.ellipse((0, 0, avatar_size+border_size*2, avatar_size+border_size*2), fill="#009639")
                border.paste(img, (border_size, border_size), img)
                self.avatar_img = ImageTk.PhotoImage(border)
                tk.Label(avatar_frame, image=self.avatar_img, bg="#ffffff").pack()
            except:
                avatar = Image.new('RGBA', (avatar_size, avatar_size), (0,0,0,0))
                draw = ImageDraw.Draw(avatar)
                draw.ellipse((0,0,avatar_size,avatar_size), fill="#009639")
                self.avatar_img = ImageTk.PhotoImage(avatar)
                tk.Label(avatar_frame, image=self.avatar_img, bg="#ffffff").pack()
        else:
            avatar = Image.new('RGBA', (avatar_size, avatar_size), (0,0,0,0))
            draw = ImageDraw.Draw(avatar)
            draw.ellipse((0,0,avatar_size,avatar_size), fill="#009639")
            self.avatar_img = ImageTk.PhotoImage(avatar)
            tk.Label(avatar_frame, image=self.avatar_img, bg="#ffffff").pack()
        
        info_frame = tk.Frame(avatar_info_frame, bg="#ffffff")
        info_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
        tk.Label(info_frame, text="Profil Client", font=("Segoe UI", 18, "bold"), 
                fg="#009639", bg="#ffffff").pack(anchor='center', pady=(0, 18))
        info_grid = tk.Frame(info_frame, bg="#ffffff")
        info_grid.pack(anchor='center', pady=(0,0))
        labels = [
            ("Nom d'utilisateur", client['username']),
            ("Prénom", client['prenom']),
            ("Téléphone", client['telephone'] or "Non renseigné"),
            ("Adresse", client['adresse'] or "Non renseignée")
        ]
        for i, (label, value) in enumerate(labels):
            tk.Label(info_grid, text=f"{label} :", font=("Segoe UI", 12, "bold"), 
                    fg="#7f8c8d", bg="#ffffff", anchor='center', width=16).grid(row=i, column=0, sticky='e', padx=(0, 10), pady=6)
            tk.Label(info_grid, text=value, font=("Segoe UI", 12), 
                    fg="#222", bg="#ffffff", anchor='center', width=28).grid(row=i, column=1, sticky='w', pady=6)
        
        # Section comptes et activités
        data_section = tk.Frame(main_container, bg="#e6f4ec")
        data_section.pack(fill=tk.BOTH, expand=True, pady=(0,0))
        
        # Comptes bancaires
        accounts_frame = tk.Frame(data_section, bg="#ffffff", relief="solid", bd=2, highlightbackground="#009639", highlightcolor="#009639", highlightthickness=2)
        accounts_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 30), ipadx=30, ipady=20)
        tk.Label(accounts_frame, text="Comptes Bancaires", font=("Segoe UI", 16, "bold"), 
                fg="#009639", bg="#ffffff").pack(anchor='w', pady=(0, 18), padx=(2,0))
        
        accounts_canvas = tk.Canvas(accounts_frame, bg="#ffffff", highlightthickness=0, height=8*36)
        accounts_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        accounts_scroll = tk.Scrollbar(accounts_frame, orient="vertical", command=accounts_canvas.yview)
        accounts_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        accounts_canvas.configure(yscrollcommand=accounts_scroll.set)
        accounts_list_frame = tk.Frame(accounts_canvas, bg="#ffffff")
        accounts_list_id = accounts_canvas.create_window((0, 0), window=accounts_list_frame, anchor="nw")
        def on_accounts_configure(event):
            accounts_canvas.configure(scrollregion=accounts_canvas.bbox("all"))
        accounts_list_frame.bind("<Configure>", on_accounts_configure)
        def resize_accounts_canvas(event):
            accounts_canvas.itemconfig(accounts_list_id, width=event.width)
        accounts_canvas.bind("<Configure>", resize_accounts_canvas)
        
        accounts = [acc for acc in self.model.accounts if acc['user_id'] == client['id']]
        if accounts:
            headers_frame = tk.Frame(accounts_list_frame, bg="#e6f4ec")
            headers_frame.pack(fill=tk.X, pady=(0, 6))
            headers = ["Numéro", "Type", "Solde"]
            widths = [150, 100, 120]
            for i, (header, width) in enumerate(zip(headers, widths)):
                tk.Label(headers_frame, text=header, font=("Segoe UI", 12, "bold"), 
                        fg="#009639", bg="#e6f4ec", width=width//10, anchor='center').pack(side=tk.LEFT, padx=5, pady=8)
            for i, acc in enumerate(accounts):
                row_frame = tk.Frame(accounts_list_frame, bg="#ffffff" if i % 2 == 0 else "#e6f4ec")
                row_frame.pack(fill=tk.X, pady=1)
                tk.Label(row_frame, text=acc['numero_compte'], font=("Segoe UI", 11), 
                        fg="#222", bg=row_frame.cget("bg"), width=15, anchor='center').pack(side=tk.LEFT, padx=5, pady=8)
                tk.Label(row_frame, text=acc['type_compte'], font=("Segoe UI", 11), 
                        fg="#222", bg=row_frame.cget("bg"), width=10, anchor='center').pack(side=tk.LEFT, padx=5, pady=8)
                tk.Label(row_frame, text=f"{acc['solde']:.2f} DH", font=("Segoe UI", 11, "bold"), 
                        fg="#009639", bg=row_frame.cget("bg"), width=12, anchor='center').pack(side=tk.LEFT, padx=5, pady=8)
            total_solde = sum(acc['solde'] for acc in accounts)
            total_frame = tk.Frame(accounts_list_frame, bg="#009639")
            total_frame.pack(fill=tk.X, pady=(18, 0))
            tk.Label(total_frame, text=f"Solde Total: {total_solde:.2f} DH", 
                    font=("Segoe UI", 13, "bold"), fg="white", bg="#009639").pack(pady=10)
        else:
            tk.Label(accounts_list_frame, text="Aucun compte bancaire", font=("Segoe UI", 12), 
                    fg="#7f8c8d", bg="#ffffff").pack(pady=40)
        
        # Activités récentes
        activities_frame = tk.Frame(data_section, bg="#ffffff", relief="solid", bd=2, highlightbackground="#009639", highlightcolor="#009639", highlightthickness=2)
        activities_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(30, 0), ipadx=30, ipady=20)
        tk.Label(activities_frame, text="Activités Récentes", font=("Segoe UI", 16, "bold"), 
                fg="#009639", bg="#ffffff").pack(anchor='w', pady=(0, 18), padx=(2,0))
        
        acts_canvas = tk.Canvas(activities_frame, bg="#ffffff", highlightthickness=0, height=8*36)
        acts_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        acts_scroll = tk.Scrollbar(activities_frame, orient="vertical", command=acts_canvas.yview)
        acts_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        acts_canvas.configure(yscrollcommand=acts_scroll.set)
        acts_list_frame = tk.Frame(acts_canvas, bg="#ffffff")
        acts_list_id = acts_canvas.create_window((0, 0), window=acts_list_frame, anchor="nw")
        def on_acts_configure(event):
            acts_canvas.configure(scrollregion=acts_canvas.bbox("all"))
        acts_list_frame.bind("<Configure>", on_acts_configure)
        def resize_acts_canvas(event):
            acts_canvas.itemconfig(acts_list_id, width=event.width)
        acts_canvas.bind("<Configure>", resize_acts_canvas)
        
        acts_all = []
        if accounts:
            for acc in accounts:
                acts = self.model.get_activities(acc['id'])
                if acts:
                    for a in acts[:5]:
                        acts_all.append((acc['numero_compte'], a['type_transaction'], 
                                       f"{a['montant']:.2f} DH", 
                                       a['date_transaction'].strftime("%d/%m/%Y")))
        
        if acts_all:
            headers_frame = tk.Frame(acts_list_frame, bg="#e6f4ec")
            headers_frame.pack(fill=tk.X, pady=(0, 6))
            headers = ["Compte", "Type", "Montant", "Date"]
            widths = [120, 80, 100, 100]
            for i, (header, width) in enumerate(zip(headers, widths)):
                tk.Label(headers_frame, text=header, font=("Segoe UI", 12, "bold"), 
                        fg="#009639", bg="#e6f4ec", width=width//10, anchor='center').pack(side=tk.LEFT, padx=5, pady=8)
            for i, (compte, type_act, montant, date) in enumerate(acts_all[:10]):
                row_frame = tk.Frame(acts_list_frame, bg="#ffffff" if i % 2 == 0 else "#e6f4ec")
                row_frame.pack(fill=tk.X, pady=1)
                tk.Label(row_frame, text=compte, font=("Segoe UI", 11), 
                        fg="#222", bg=row_frame.cget("bg"), width=12, anchor='center').pack(side=tk.LEFT, padx=5, pady=8)
                tk.Label(row_frame, text=type_act, font=("Segoe UI", 11), 
                        fg="#222", bg=row_frame.cget("bg"), width=8, anchor='center').pack(side=tk.LEFT, padx=5, pady=8)
                color = "#009639" if type_act == "Ver sement" else "#e74c3c"
                tk.Label(row_frame, text=montant, font=("Segoe UI", 11, "bold"), 
                        fg=color, bg=row_frame.cget("bg"), width=10, anchor='center').pack(side=tk.LEFT, padx=5, pady=8)
                tk.Label(row_frame, text=date, font=("Segoe UI", 11), 
                        fg="#7f8c8d", bg=row_frame.cget("bg"), width=10, anchor='center').pack(side=tk.LEFT, padx=5, pady=8)
        else:
            tk.Label(acts_list_frame, text="Aucune activité récente", font=("Segoe UI", 12), 
                    fg="#7f8c8d", bg="#ffffff").pack(pady=40)

# --- LANCEMENT ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BanqueApp(root)
    root.mainloop()