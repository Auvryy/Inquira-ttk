import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from components.primary_button import PrimaryButton
from components.primary_entry import PrimaryEntry
from app.theme_colors import Colors

class LoginPage(ttk.Frame):
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
            card_frame,
            text="Welcome Back",
            font=("Segoe UI", 24, "bold"),
            foreground=Colors.TEXT_PRIMARY,
            style="Card.TLabel"
        ).pack(pady=(0, 10))
        
        ttk.Label(
            card_frame,
            text="Please enter your details to sign in.",
            font=("Segoe UI", 11),
            foreground=Colors.TEXT_SECONDARY,
            style="Card.TLabel"
        ).pack(pady=(0, 30))
        
        self.email_entry = PrimaryEntry(card_frame, placeholder="Email or Username")
        self.email_entry.pack(fill=X, pady=(0, 20), ipady=8)
        
        self.password_entry = PrimaryEntry(card_frame, placeholder="Password", is_password=True)
        self.password_entry.pack(fill=X, pady=(0, 10), ipady=8)
        
        options_frame = ttk.Frame(card_frame, style="Card.TFrame")
        options_frame.pack(fill=X, pady=(0, 25))
        
        self.show_password = ttk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Show password",
            variable=self.show_password,
            command=self._toggle_password,
            bootstyle="primary-round-toggle"
        ).pack(side=LEFT)
        
        ttk.Label(
            options_frame,
            text="Forgot password?",
            font=("Segoe UI", 10),
            foreground=Colors.PRIMARY,
            cursor="hand2",
            style="Card.TLabel"
        ).pack(side=RIGHT)
        
        login_btn = PrimaryButton(card_frame, text="Sign In", command=self._on_login)
        login_btn.pack(fill=X, pady=(0, 20), ipady=5)
        
        register_frame = ttk.Frame(card_frame, style="Card.TFrame")
        register_frame.pack()
        
        ttk.Label(
            register_frame,
            text="Don't have an account?",
            font=("Segoe UI", 10),
            foreground=Colors.TEXT_SECONDARY,
            style="Card.TLabel"
        ).pack(side=LEFT, padx=(0, 5))
        
        register_link = ttk.Label(
            register_frame,
            text="Create one",
            font=("Segoe UI", 10, "bold"),
            foreground=Colors.PRIMARY,
            cursor="hand2",
            style="Card.TLabel"
        )
        register_link.pack(side=LEFT)
        register_link.bind("<Button-1>", lambda e: self.app.show_page("RegisterPage"))

    def _resize_image(self, event):
        if not hasattr(self, "image_label"):
            return
        
        try:
            # We want to crop/scale image to fill the frame
            pil_image = Image.open("assets/images/geometry.jpeg")
            
            # Simple resize for now to fit the frame dimensions
            # For a proper cover effect, more complex math is needed. 
            # Doing basic resize to frame height and width maintaining aspect ratio might warp or leave spaces,
            # so stretching it:
            new_image = pil_image.resize((event.width, event.height), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(new_image)
            self.image_label.configure(image=self.bg_image)
        except Exception:
            pass

    def _toggle_password(self):
        self.password_entry.set_password_mode(not self.show_password.get())

    def _on_login(self):
        pass
