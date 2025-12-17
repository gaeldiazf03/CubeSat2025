import ttkbootstrap as ttk
from PIL import Image, ImageTk
from Pages import Com
from Settings import logo
from Plantillas import BaseFrame


class MenuFrame(BaseFrame):
    def __init__(self, master, sub_color, show_page_callback=print, **kwargs):
        super().__init__(master, style=sub_color, **kwargs)
        # pyrefly: ignore  # no-matching-overload
        self.configure(width=200, height=500, bootstyle=sub_color)

        self.show_page_callback = show_page_callback
        self.com_window = None

        self.kotwImage = Image.open(logo)
        self.kotwResize = self.kotwImage.resize((175, 175))
        self.kotwReady = ImageTk.PhotoImage(image=self.kotwResize, master=self)

        # pyrefly: ignore  # unexpected-keyword
        self.kotwLabel = ttk.Label(self, image=self.kotwReady, bootstyle="inverse-"+sub_color)
        self.kotwLabel.place(relx=0.5, y=120, anchor="center")
        self.kotwLabel.bind("<Button-1>", lambda event: self.show_page_callback("HomePage"))

        self.btn_connect = ttk.Button(self, text="Connect", width=10, style="Custom.TButton", command=self.open_com)
        self.btn_connect.place(relx=0.5, rely=0.35, anchor='center')

        self.btn_serial = ttk.Button(self, text="Serial", width=10, style="Custom.TButton", command=lambda: self.show_page_callback("SerialPage"))
        self.btn_serial.place(relx=0.5, rely=0.5, anchor='center')

        self.btn_excel = ttk.Button(self, text="Excel", width=10, style="Custom.TButton", command=lambda: self.show_page_callback("ExcelPage"))
        self.btn_excel.place(relx=0.5, rely=0.65, anchor='center')

        self.btn_graphs = ttk.Button(self, text="Graphs", width=10, style="Custom.TButton", command=lambda: self.show_page_callback("GraphsPage"))
        self.btn_graphs.place(relx=0.5, rely=0.80, anchor='center')

    def open_com(self):
        if self.com_window is None or not self.com_window.winfo_exists():
            # pyrefly: ignore  # bad-assignment
            self.com_window = Com(self)


if __name__ == '__main__':
    app = ttk.Window(themename="united")
    app.geometry("800x500")
    pf = MenuFrame(master=app, sub_color="danger")
    pf.pack(side="bottom", anchor="w", fill="y", expand=True)
    app.mainloop()
