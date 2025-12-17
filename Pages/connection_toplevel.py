import ttkbootstrap as ttk
from Settings import icon
from ToolsGUI import get_ports, ArduinoConnection
from ToolsGUI.MessagesGUI import show_message
from Plantillas import TopLevelFrame


class Com(TopLevelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self._message = 0

        self.iconphoto(False, ttk.PhotoImage(file=icon))
        self.geometry('450x130')
        self.title('Puertos COM')

        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        for i in range(2):
            self.grid_rowconfigure(i, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Menubutton para seleccionar puertos
        self.menu = None
        self.mb = ttk.Menubutton(self, text='Seleccionar puerto', width=47)
        self.mb.configure(state='disabled', text='Escaneando puertos...')
        self.mb.grid(row=0, column=0, columnspan=3)

        self.port_var = ttk.StringVar()
        self.port_var.set('')

        # Botones
        self.disconnect_button = ttk.Button(self, text="Desconectar", command=self.disconnect_port, width=12, style="CustomWarning.TButton")
        self.connect_button = ttk.Button(self, text="Conectar", command=self.connect_port, width=12, style="CustomSuccess.TButton")
        self.close_button = ttk.Button(self, text="Cerrar", command=self.destroy, width=12, style="CustomDanger.TButton")

        self.disconnect_button.grid(row=1, column=0)
        self.connect_button.grid(row=1, column=1)
        self.close_button.grid(row=1, column=2)

        self.last_ports = []
        self.update_ports()

        self._start_auto_update()
        self.port_update_id = None

    def _start_auto_update(self):
        """Maneja cíclicamente el auto update para actualizar los puertos"""
        self.update_ports()
        # pyrefly: ignore  # bad-assignment, bad-argument-type
        self.port_update_id = self.after(3000, self._start_auto_update)

    def update_ports(self):
        """Versión con manejo robusto de estados iniciales"""
        current_ports = get_ports()

        if current_ports != self.last_ports:
            self.last_ports = current_ports

            if self.menu:
                self.menu.destroy()
            # pyrefly: ignore  # bad-assignment
            self.menu = ttk.Menu(self.mb)

            if not current_ports:
                self.mb.configure(state='disabled', text='No hay puertos disponibles')
                self.port_var.set('')
            else:
                self.mb.configure(state='normal', text='Seleccionar puerto' if not self.port_var.get() else f"Puerto: {self.port_var.get()}")
                for port in current_ports:
                    # pyrefly: ignore  # missing-attribute
                    self.menu.add_radiobutton(label=port, variable=self.port_var, command=lambda p=port: self.port_selected(p))
            self.mb['menu'] = self.menu

    def on_close(self):
        if self.port_update_id:
            self.after_cancel(self.port_update_id)  # Cancelamos usando el ID
        self.parent.com_window = None
        self.destroy()

    def port_selected(self, port):
        """Actualiza el texto del Menubutton cuando se selecciona un puerto"""
        self.mb['text'] = f"Puerto: {port}"
        self.port_var.set(port)
        print(f"Puerto seleccionado: {port}")

    def connect_port(self):
        """Intenta conectar con el puerto seleccionado"""
        port = self.port_var.get()
        if port:
            try:
                arduino = ArduinoConnection()
                if arduino.check_connection():
                    self._message = 0b00000010  # MSG_ALREADY_CONNECTED
                    show_message(self, self._message)
                    return

                arduino.connect(port, 115200)
                arduino.start_reading()
                self._message = 0b00000001  # MSG_CONNECTED
            except Exception as e:
                print(f"Error al conectar: {e}")
                self._message = 0b00000100  # MSG_CONNECTION_ERROR
        else:
            self._message = 0b00001000  # MSG_NO_PORT_SELECTED
        show_message(self, self._message)

    def disconnect_port(self):
        """Desconecta el puerto serie"""
        try:
            arduino = ArduinoConnection()
            if arduino.check_connection():
                arduino.disconnect()
                self._message = 0b00010000  # MSG_DISCONNECTED
            else:
                self._message = 0b00100000  # MSG_NO_ACTIVE_CONN
        except Exception as e:
            print(f"Error al desconectar: {e}")
            self._message = 0b01000000  # MSG_DISCONNECT_ERROR
        show_message(self, self._message)
