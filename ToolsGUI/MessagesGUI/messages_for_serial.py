from traceback import format_exc
from Plantillas import TopLevelFrame
import ttkbootstrap as ttk


def _get_last_error():
    return format_exc().splitlines()[-1]


class MessageWindow(TopLevelFrame):
    def __init__(self, parent, message, msg_type):
        super().__init__(parent)
        self.parent = parent
        self.transient(parent)
        self.title("Mensaje del sistema")

        # Mapeo de tipos a estilos
        style_config = {
            "success": {
                "frame_style": "MessageSuccess.TFrame",
                "title": "✓ Éxito",
                "button_style": "CustomSuccess.TButton",
                "label_style": "CustomSuccess.TLabel",
                "title_style": "CustomSuccessTitle.TLabel"
            },
            "danger": {
                "frame_style": "MessageDanger.TFrame",
                "title": "✗ Error",
                "button_style": "CustomDanger.TButton",
                "label_style": "CustomDanger.TLabel",
                "title_style": "CustomDangerTitle.TLabel"
            },
            "warning": {
                "frame_style": "MessageWarning.TFrame",
                "title": "⚠ Advertencia",
                "button_style": "CustomWarning.TButton",
                "label_style": "CustomWarning.TLabel",
                "title_style": "CustomWarningTitle.TLabel"
            },
            "info": {
                "frame_style": "MessageInfo.TFrame",
                "title": "ℹ Información",
                "button_style": "CustomInfo.TButton",
                "label_style": "CustomInfo.TLabel",
                "title_style": "CustomInfoTitle.TLabel"
            }
        }

        config = style_config.get(msg_type, style_config["info"])

        # Frame principal
        main_frame = ttk.Frame(self, padding=15, style=config["frame_style"])
        main_frame.pack(fill="both", expand=True)

        # Contenido
        ttk.Label(main_frame,
                  text=config["title"],
                  style=config["title_style"],
                  foreground="white").pack(pady=(0, 10))

        ttk.Label(main_frame,
                  text=message,
                  wraplength=350,
                  justify="center",
                  style=config["label_style"]).pack(pady=(0, 15))

        # Botón de cierre
        ttk.Button(main_frame,
                   text="Aceptar",
                   command=self.destroy,
                   style=config["button_style"],
                   width=12).pack(pady=5)

        # Configuración final
        self._center_window()
        self.grab_set()

    def _center_window(self):
        """Centra la ventana respecto a su padre"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() - width) // 2
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() - height) // 2
        self.geometry(f"+{x}+{y}")


def _show_message(parent, message):
    messages = {
        0b00000001: ("Conexión establecida correctamente", "success"),
        0b00000010: ("Ya existe una conexión activa", "danger"),
        0b00000100: (f"Error de conexión: {_get_last_error()}", "danger"),
        0b00001000: ("Por favor seleccione un puerto COM primero", "warning"),
        0b00010000: ("Desconectado correctamente", "info"),
        0b00100000: ("No hay conexiones activas para desconectar", "warning"),
        0b01000000: (f"Error al desconectar: {_get_last_error()}", "danger")
    }

    if message:
        for mask, (text, msg_type) in messages.items():
            if message & mask:
                MessageWindow(parent, text, msg_type)
                message &= ~mask  # Limpia el mensaje mostrado
                break

