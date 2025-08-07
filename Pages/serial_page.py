import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from Plantillas import BaseFrame


class SerialPage(BaseFrame):
    def __init__(self, master, sub_color):
        super().__init__(master)
        self.sub_color = sub_color

        self.lbl_title = ttk.Label(self, text="Serial Page", font=self.TITLE, bootstyle="inverse-"+self.sub_color)
        self.lbl_title.grid(column=0, row=0, sticky="ew")

        self.serial_lblframe = ttk.Labelframe(self, text='Serial', bootstyle="info", labelanchor="nw")
        self.serial_lblframe.grid(column=0, row=1, columnspan=3, sticky="nsew", padx=10, pady=10)

        self.str_serial = ScrolledText(self.serial_lblframe, wrap=WORD, font=self.FONT, autohide=True, hbar=True)
        self.str_serial.text["state"] = "disabled"
        self.str_serial.pack(fill=BOTH, expand=True, padx=15, pady=5)


if __name__ == "__main__":
    app = ttk.Window()

    serial_page = SerialPage(app, "light")
    serial_page.pack()

    app.mainloop()
