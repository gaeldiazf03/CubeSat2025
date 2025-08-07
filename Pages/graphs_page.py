import ttkbootstrap as ttk


class GraphsPage(ttk.Frame):
    def __init__(self, master, sub_color, **kwargs):
        super().__init__(master, **kwargs)

        self.lbl_title = ttk.Label(self, text="Graphs page", font="Consolas 20 bold")
        self.lbl_title.grid(column=0, row=0, columnspan=2)


if __name__ == '__main__':
    app = ttk.Window(themename="journal")

    gp = GraphsPage(master=app)
    gp.pack()

    app.mainloop()
