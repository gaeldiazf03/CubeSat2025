import ttkbootstrap as ttk
from Settings import icon
from ToolsGUI import get_ports, ArduinoConnection
from Plantillas import TopLevelFrame


class Com(TopLevelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.iconphoto(False, ttk.PhotoImage(file=icon))
        self.geometry('450x130')
        self.title('Puertos COM')
        
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        for i in range(2):
            self.grid_rowconfigure(i, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.menu = None

        # Menubutton para seleccionar puertos
        # self.mb = ttk.Menubutton(self, text='Seleccionar puerto', style='info.Outline.TMenubutton', width=40)
        self.mb = ttk.Menubutton(self, text='Seleccionar puerto', width=47)
        self.mb.grid(row=0, column=0, columnspan=3)
        self.port_var = ttk.StringVar()
        self.menu = None

        # Botones
        self.disconnect_button = ttk.Button(self, text="Desconectar", command=self.disconnect_port, width=12, style="CustomWarning.TButton")
        self.disconnect_button.grid(row=1, column=0)
        self.connect_button = ttk.Button(self, text="Conectar", command=self.connect_port, width=12, style="CustomSuccess.TButton")
        self.connect_button.grid(row=1, column=1)
        self.close_button = ttk.Button(self, text="Cerrar", command=self.destroy, width=12, style="CustomDanger.TButton")
        self.close_button.grid(row=1, column=2)

        self.place_window_center()
        self.update_ports()
        parent.com_window = self

    def update_ports(self):
        """Actualiza la lista de puertos disponibles en el Menubutton"""
        ports = get_ports()
        self.menu = ttk.Menu(self.mb)

        if not ports:
            self.mb.configure(state='disabled', text='No hay puertos disponibles')
        else:
            for port in ports:
                self.menu.add_radiobutton(label=port, variable=self.port_var, command=lambda p=port: self.port_selected(p))
            # Asociar menú con el Menubutton
            self.mb['menu'] = self.menu

        self.after(2000, self.update_ports)

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
                arduino = ArduinoConnection()  # Singleton
                if arduino.check_connection():
                    print("Ya hay una conexión activa.")
                    return

                arduino.connect(port, 115200)  # Puedes ajustar el baudrate
                arduino.start_reading()  # Comienza la lectura en segundo plano
                print(f"Conexión exitosa al puerto {port}")
            except Exception as e:
                print(f"Error al conectar: {e}")
        else:
            print("No hay ningún puerto seleccionado")

    def disconnect_port(self):
        """Desconecta el puerto serie"""
        try:
            arduino = ArduinoConnection()
            if arduino.check_connection():
                arduino.disconnect()
            else:
                print("No hay conexión activa.")
        except Exception as e:
            print(f"Error al desconectar: {e}")

    def on_close(self):
        self.parent.com_window = None
        self.destroy()


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title('Connection Manager')
        self.geometry('500x500')
        self.resizable(False, False)
        self.iconphoto(False, ttk.PhotoImage(file='D:\\PycharmProjects\\RoverGUI\\PagesManager\\img\\Delfin16.png'))

        self.com_window = None

        ttk.Button(self, text="Abrir ventana COM", command=self.open_com).pack(pady=20)

    def open_com(self):
        if self.com_window is None or not self.com_window.winfo_exists():
            self.com_window = Com(self)


if __name__ == '__main__':
    app = App()
    app.mainloop()
