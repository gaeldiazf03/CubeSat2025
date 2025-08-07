import ttkbootstrap as ttk
from ttkbootstrap.style import Colors


class TopLevelFrame(ttk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.resizable(False, False)
        self.custom_style = ttk.Style()

        self.FONT = ("Ubuntu", 10)
        self.TITLE = ("Ubuntu", 24, "bold")

        self.colors = self.custom_style.colors

        self._setup_base_styles()

    def _setup_base_styles(self):
        # Botones
        self.create_custom_style_buttons("CustomSuccess.TButton", self.colors.success)
        self.create_custom_style_buttons("CustomDanger.TButton", self.colors.danger)
        self.create_custom_style_buttons("CustomWarning.TButton", self.colors.warning)
        self.create_custom_style_buttons("CustomInfo.TButton", self.colors.info)

        # Labels
        self.create_custom_style_label("CustomSuccess.TLabel", self.colors.success, self.FONT)
        self.create_custom_style_label("CustomDanger.TLabel", self.colors.danger, self.FONT)
        self.create_custom_style_label("CustomWarning.TLabel", self.colors.warning, self.FONT)
        self.create_custom_style_label("CustomInfo.TLabel", self.colors.info, self.FONT)

        # Títulos
        self.create_custom_style_label("CustomSuccessTitle.TLabel", self.colors.success, self.TITLE)
        self.create_custom_style_label("CustomDangerTitle.TLabel", self.colors.danger, self.TITLE)
        self.create_custom_style_label("CustomWarningTitle.TLabel", self.colors.warning, self.TITLE)
        self.create_custom_style_label("CustomInfoTitle.TLabel", self.colors.info, self.TITLE)

    def create_custom_style_buttons(self, custom_style: str, color_string):
        self.custom_style.configure(custom_style, font=self.FONT, background=color_string, foreground="white", borderwidth=0)
        self.custom_style.map(custom_style,
                              background=[
                                  ("active", Colors.update_hsv(color_string, vd=-0.2)),
                                  ("pressed", Colors.update_hsv(color_string, vd=-0.3))
                              ],
                              bordercolor=[
                                  ("active", Colors.update_hsv(color_string, vd=-0.2)),
                                  ("pressed", Colors.update_hsv(color_string, vd=-0.3))
                              ])

    def create_custom_style_label(self, custom_style, color_string, font):
        self.custom_style.configure(custom_style, font=font, background=color_string, foreground="black")

