import ttkbootstrap as ttk
from PIL import Image, ImageTk
from Settings import logo
from Plantillas import BaseFrame


class HomePage(BaseFrame):
    def __init__(self, master, sub_color, **kwargs):
        super().__init__(master, button_color='primary', **kwargs)

        self.sub_color = sub_color

        for i in range(3):
            self.columnconfigure(i, weight=1)
        for i in range(5):
            self.rowconfigure(i, weight=1)

        # pyrefly: ignore  # bad-argument-type, unexpected-keyword
        self.lbl_titulo = ttk.Label(self, text='Delphinus Cubesat', font=self.TITLE, bootstyle="inverse-"+self.sub_color)
        self.lbl_titulo.grid(column=0, row=0, columnspan=3)

        self.iconoCansat = Image.open(logo)
        self.cansatResize = self.iconoCansat.resize((350, 350))
        self.cansatReady = ImageTk.PhotoImage(image=self.cansatResize, master=self)

        # pyrefly: ignore  # unexpected-keyword
        self.cansatLabel = ttk.Label(self, image=self.cansatReady, bootstyle='inverse-'+self.sub_color)
        self.cansatLabel.grid(column=1, row=1, rowspan=3)

        self.btn_connection = ttk.Button(self, text='Configurar serial', width=15, style="Custom.TButton")
        self.btn_connection.grid(column=0, row=4)

        self.btn_colors = ttk.Button(self, text='Themes', width=15, style="Custom.TButton")
        self.btn_colors.grid(column=1, row=4)

        self.btn_about = ttk.Button(self, text='About', width=15, style="Custom.TButton")
        self.btn_about.grid(column=2, row=4)


if __name__ == '__main__':
    root = ttk.Window(themename="united")
    home = HomePage(master=root, sub_color="secondary")
    home.pack(fill="both", expand=True)
    root.mainloop()
