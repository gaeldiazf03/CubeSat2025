import ttkbootstrap as ttk
from ttkbootstrap.style import Colors


class BaseFrame(ttk.Frame):
    def __init__(self, master, button_color="primary", **kwargs):
        super().__init__(master, **kwargs)

        self.configure(bootstyle="light")

        self.style = ttk.Style()
        self.style.configure(
            style="Custom.TButton",
            font=("Ubuntu", "12"),
            background=getattr(self.style.colors, button_color),
            foreground="white",
        )
        self.style.map(
            style="Custom.TButton",
            background=[("active", Colors.update_hsv(getattr(self.style.colors, button_color), vd=-0.1))]
        )

        self.FONT = ("Ubuntu", "12")
        self.TITLE = ("Ubuntu", "24", "bold")
