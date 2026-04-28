import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from components.primary_button import PrimaryButton
from components.primary_entry import PrimaryEntry
from app.theme_colors import Colors

class RegisterPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=0, style="Container.TFrame")
        self.app = app
        
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=1)
        
        # Left Image Section (60%)
        self.image_frame = ttk.Frame(self, style="Container.TFrame")
        self.image_frame.grid(row=0, column=0, sticky="nsew")
        
        try:
            pil_image = Image.open("assets/images/geometry.jpeg")
            self.bg_image = ImageTk.PhotoImage(pil_image)
            self.image_label = ttk.Label(self.image_frame, image=self.bg_image)
            self.image_label.place(relx=0.5, rely=0.5, anchor="center")
            self.image_frame.bind("<Configure>", self._resize_image)
        except Exception as e:
            print(f"Error loading image: {e}")
            
        # Right Form Section (40%)
        form_container = ttk.Frame(self, style="Container.TFrame")
        form_container.grid(row=0, column=1, sticky="nsew")
        form_container.columnconfigure(0, weight=1)
        form_container.rowconfigure(0, weight=1)
        
        card_frame = ttk.Frame(form_container, style="Card.TFrame", padding=(40, 50))
        card_frame.grid(row=0, column=0)
        
        ttk.Label(
            card_frame, text="Create an Account", font=("Segoe UI", 24, "bold"),
            foreground=Colors.TEXT_PRIMARY, style="Card.TLabel"
        ).pack(pady=(0, 10))
        
        ttk.Label(
            card_frame, text="Sign up to get started.", font=("Segoe UI", 11),
            foreground=Colors.TEXT_SECONDARY, style="Card.TLabel"
        ).pack(pady=(0, 30))
        
        self.name_entry = PrimaryEntry(card_frame, placeholder="Full Name")
        self.name_entry.pack(fill=X, pady=(0, 20), ipady=8)
        
        self.email_entry = PrimaryEntry(card_frame, placeholder="Email Address")
        self.email_entry.pack(fill=X, pady=(0, 20), ipady=8)
        
        self.password_entry = PrimaryEntry(card_frame, placeholder="Password", is_password=True)
        self.password_entry.pack(fill=X, pady=(0, 20), ipady=8)

        self.confirm_password_entry = PrimaryEntry(card_frame, placeholder="Confirm Password", is_password=True)
        self.confirm_password_entry.pack(fill=X, pady=(0, 20), ipady=8)
        
        options_frame = ttk.Frame(card_frame, style="Card.TFrame")
        options_frame.pack(fill=X, pady=(0, 25))
        
        self.show_password = ttk.BooleanVar()
        ttk.Checkbutton(
            options_frame, text="Show passwords", variable=self.show_password,
            command=self._toggle_password, bootstyle="primary-round-toggle"
        ).pack(side=LEFT)
        
        register_btn = PrimaryButton(card_frame, text="Sign Up", command=self._on_register)
        register_btn.pack(fill=X, pady=(0, 20), ipady=5)
        
        login_frame = ttk.Frame(card_frame, style="Card.TFrame")
        login_frame.pack()
        
        ttk.Label(
            login_frame, text="Already have an account?", font=("Segoe UI", 10),
            foreground=Colors.TEXT_SECONDARY, style="Card.TLabel"
        ).pack(side=LEFT, padx=(0, 5))
        
        login_link = ttk.Label(
            login_frame, text="Log in", font=("Segoe UI", 10, "bold"),
            foreground=Colors.PRIMARY, cursor="hand2", style="Card.TLabel"
        )
        login_link.pack(side=LEFT)
        login_link.bind("<Button-1>", lambda e: self.app.show_page("LoginPage"))

    def _resize_image(self, event):
        if not hasattr(self, "image_label"):
            return
        
        try:
            pil_image = Image.open("assets/images/geometry.jpeg")
            new_image = pil_image.resize((event.width, event.height), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(new_image)
            self.image_label.configure(image=self.bg_image)
        except Exception:
            pass

    def _toggle_password(self):
        show_pwd = not self.show_password.get()
        self.password_entry.set_password_mode(show_pwd)
        self.confirm_password_entry.set_password_mode(show_pwd)

    def _on_register(self):
        pass
