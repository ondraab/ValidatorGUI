import Tkinter as tk
import ttk

class ToggledFrame(tk.Frame):

    def __init__(self, parent, text = "", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.title_frame =