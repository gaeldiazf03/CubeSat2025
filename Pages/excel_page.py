import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from Settings import var as variables_excel


class ExcelPage(ttk.Frame):
    def __init__(self, master, sub_color):
        super().__init__(master)

        self.lbl_title = ttk.Label(self, text="Excel Table Page", font="Consolas 20 bold")
        self.lbl_title.pack(side="top", fill="x")

        excel_frame = Tableview(
            self,
            coldata=variables_excel,
            paginated=True,
            searchable=False,
            bootstyle=DANGER
        )
        excel_frame.pack(fill=BOTH, expand=True)

if __name__ == "__main__":
    app = ttk.Window()

    # pyrefly: ignore  # missing-argument
    serial_page = ExcelPage(app)
    serial_page.pack()

    app.mainloop()
