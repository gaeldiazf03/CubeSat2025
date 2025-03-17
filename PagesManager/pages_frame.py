import ttkbootstrap as ttk
from Pages import HomePage, GraphsPage, SerialPage, ExcelPage


class ShowFrame(ttk.Frame):
    def __init__(self, master, sub_color: str):
        super().__init__(master, style=sub_color)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.sub_color = sub_color

        self.frames = {}    # Almacena frames

        for PageClass in (HomePage, SerialPage, GraphsPage, ExcelPage):
            page_name = PageClass.__name__
            frame = PageClass(self, sub_color=self.sub_color)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_page("HomePage")

    def show_page(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == '__main__':
    app = ttk.Window(themename="journal")
    app.geometry("800x500")
    pf = ShowFrame(master=app, sub_color="primary")
    pf.pack(side="top", anchor="e")
    app.mainloop()
