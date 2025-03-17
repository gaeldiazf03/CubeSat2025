import ttkbootstrap as ttk


class Com(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.iconphoto(False, ttk.PhotoImage(file='D:\\PycharmProjects\\RoverGUI\\PagesManager\\img\\Delfin16.png'))
        self.geometry('500x500')
        self.title('Comunicación a Arduino')
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        ttk.Label(self, text="Connection Window").pack()

        ttk.Button(self, text="Quit", command=self.destroy).pack()
        ttk.Button(self, text="Ok", command=lambda: print("Ok")).pack()

        self.place_window_center()
        parent.com_window = self

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

        ttk.Button(self, text="Open", command=self.open_com).pack()

    def open_com(self):
        if self.com_window is None or not self.com_window.winfo_exists():
            self.com_window = Com(self)


if __name__ == '__main__':
    app = App()
    app.mainloop()
