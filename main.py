import ttkbootstrap as ttk
from PagesManager import ShowFrame, MenuFrame
from Settings import config, icon, sub_color


class Cubesat(ttk.Window):
    """
    Aplicación principal del monitor del cubesat
    Aquí casi nada se va a agregar, por eso es que se piensa en esta aplicación
    como algo más modular. Que podemos implementar un nuevo código, insertarlo en cierta sección
    sabiendo que va a fallar allá y no acá. Muy pocas veces he necesitado editar aquí
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.color: str = sub_color

        # Configuración del grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=160)
        self.grid_columnconfigure(1, weight=1)

        # Iconos
        self.icono_16 = ttk.PhotoImage(file=icon, master=self)
        self.iconphoto(False, self.icono_16)

        # FRAME - Contenedor
        self.frame_menu = ShowFrame(self, sub_color="light")
        self.frame_menu.configure(padding=(15, 30, 15, 30))
        self.frame_menu.grid(row=0, column=1, sticky="nsew")

        # FRAME - Pages manager
        self.frame_pages = MenuFrame(self, sub_color=self.color, show_page_callback=self.show_page)
        self.frame_pages.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name):
        self.frame_menu.show_page(page_name)


if __name__ == "__main__":
    ttk.utility.enable_high_dpi_awareness()
    app: Cubesat = Cubesat(**config)
    app.mainloop()
