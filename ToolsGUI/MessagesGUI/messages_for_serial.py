from traceback import format_exc
from Plantillas import TopLevelFrame
import ttkbootstrap as ttk


def _get_last_error():
    return format_exc().splitlines()[-1]


class MessageWindow(TopLevelFrame):
    def __init__(self, parent, message, msg_type):
        super().__init__(parent)
        self.parent = parent
        self.transient(parent)  # Mantiene la relación con la ventana padre
        self.title("Mensaje del sistema")

        # Configura el estilo según el tipo de mensaje
        styles = {
            "success": ("success", "✓ Éxito"),
            "error": ("danger", "✗ Error"),
            "warning": ("warning", "⚠ Advertencia"),
            "info": ("info", "ℹ Información")
        }

        style, title = styles.get(msg_type, ("info", "Mensaje"))

        # Frame principal
        main_frame = ttk.Frame(self, padding=10, style=f"{style}.TFrame")
        main_frame.pack(fill="both", expand=True)

        # Icono y texto
        ttk.Label(main_frame, text=title, style=f"{style}.Inverse.TLabel", font=("Helvetica", 10, "bold")).pack(
            pady=(0, 10))

        ttk.Label(main_frame, text=message, wraplength=300, justify="center").pack(pady=(0, 10))

        # Botón de cierre
        ttk.Button(main_frame, text="Aceptar", command=self.destroy, style=f"{style}.TButton", width=10).pack(pady=5)

        # Configuración de ventana
        self.resizable(False, False)
        self.update_idletasks()
        self.geometry(f"+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")
        self.grab_set()  # Modal
        self.wait_window(self)


def _show_message(parent, message):
    messages = {
        0b00000001: ("Conexión establecida correctamente", "success"),
        0b00000010: ("Ya existe una conexión activa", "warning"),
        0b00000100: (f"Error de conexión: {_get_last_error()}", "error"),
        0b00001000: ("Por favor seleccione un puerto COM primero", "warning"),
        0b00010000: ("Desconectado correctamente", "info"),
        0b00100000: ("No hay conexiones activas para desconectar", "warning"),
        0b01000000: (f"Error al desconectar: {_get_last_error()}", "error")
    }

    if message:
        for mask, (text, msg_type) in messages.items():
            if message & mask:
                MessageWindow(parent, text, msg_type)
                message &= ~mask  # Limpia el mensaje mostrado
                break

