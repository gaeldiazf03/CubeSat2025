import tkinter as tk
from tkinter import scrolledtext
from ToolsGUI import ArduinoConnection, get_ports


class SerialMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor Serial Arduino")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.text_area.grid(column=0, row=0, padx=10, pady=10)

        self.conn = ArduinoConnection()
        self.ports = get_ports()
        if self.ports:
            self.conn.connect('COM4', 115200, 1)
            self.conn.start_reading()

        self.update_text_area()

    def update_text_area(self):
        if self.conn.check_connection():
            data = self.conn.get_reading()
            if data:
                self.text_area.insert(tk.END, data + "\n")
                self.text_area.yview(tk.END)
                print(data)
        self.root.after(100, self.update_text_area)  # Actualizar cada 100 ms


if __name__ == '__main__':
    root = tk.Tk()
    app = SerialMonitorApp(root)
    root.mainloop()
