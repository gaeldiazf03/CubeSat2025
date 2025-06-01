import ttkbootstrap as ttk
from ttkbootstrap.style import Colors


class TopLevelFrame(ttk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.resizable(False, False)
        self.custom_style = ttk.Style()

        self.FONT = ("Ubuntu", 10)
        self.TITLE = ("Ubuntu", 24, "bold")

        self.color_success = self.custom_style.colors.success
        self.color_danger = self.custom_style.colors.danger
        self.color_warning = self.custom_style.colors.warning

        self.create_custom_style_buttons("CustomSuccess.TButton", self.color_success)
        self.create_custom_style_buttons("CustomDanger.TButton", self.color_danger)
        self.create_custom_style_buttons("CustomWarning.TButton", self.color_warning)

    def create_custom_style_buttons(self, custom_style: str, color_string):
        self.custom_style.configure(custom_style,
                                    font=self.FONT,
                                    background=color_string,
                                    foreground="white",
                                    borderwidth=0)
        self.custom_style.map(custom_style,
                              background=[
                                  ("active", Colors.update_hsv(color_string, vd=-0.2)),
                                  ("pressed", Colors.update_hsv(color_string, vd=-0.3))
                              ],
                              bordercolor=[
                                  ("active", Colors.update_hsv(color_string, vd=-0.2)),
                                  ("pressed", Colors.update_hsv(color_string, vd=-0.3))
                              ])
