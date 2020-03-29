import tkinter as tk
import backend
import sys


class Front(object):
    def __init__(self, w):
        # Connect with BackEnd
        self.bk = backend.Back()

        # Link window and add main characteristics
        self.w = w
        self.w.title("Movie Database App")
        self.w.geometry("825x375")
        self.font = ("Arial", 14)
        self.small_font = ("Arial", 10)

        # Create Input Boxes
        self.title_lb = tk.Label(master=self.w, text="Title", width=12, font=self.font, anchor="w")
        self.title_lb.grid(row=0, column=0, padx=(20, 0), pady=(30, 30))
        self.title_text = tk.StringVar()
        self.title = tk.Entry(master=self.w, font=self.font, textvariable=self.title_text)
        self.title.grid(row=0, column=1, padx=20, pady=(30, 30))

        self.year_lb = tk.Label(master=self.w, text="Year", width=12, font=self.font, anchor="w")
        self.year_lb.grid(row=0, column=2, pady=(30, 30))
        self.year_text = tk.StringVar()
        self.year = tk.Entry(master=self.w, font=self.font, textvariable=self.year_text)
        self.year.grid(row=0, column=3, pady=(30, 30))

        self.director_lb = tk.Label(master=self.w, text="Director", width=12, font=self.font, anchor="w")
        self.director_lb.grid(row=1, column=0, padx=(20, 0))
        self.director_text = tk.StringVar()
        self.director = tk.Entry(master=self.w, font=self.font, textvariable=self.director_text)
        self.director.grid(row=1, column=1, padx=20)

        self.lead_lb = tk.Label(master=self.w, text="Actor/Actress", width=12, font=self.font, anchor="w")
        self.lead_lb.grid(row=1, column=2)
        self.lead_text = tk.StringVar()
        self.lead = tk.Entry(master=self.w, font=self.font, textvariable=self.lead_text)
        self.lead.grid(row=1, column=3)

        # Create Main Display
        self.display = tk.Listbox(master=self.w, height=10, width=55, font=self.small_font)
        self.display.grid(row=2, column=0, rowspan=10, columnspan=2, padx=(25, 20), pady=50)
        self.display.bind("<<ListboxSelect>>", self.select_row)
        # Add a Scrollbar
        self.scroll = tk.Scrollbar(master=self.w)
        self.scroll.grid(row=2, column=1, sticky="nse", rowspan=10, padx=(25, 20), pady=50)
        # Link Scrollbar to Main Display
        self.scroll.config(command=self.display.yview)

        # Create Buttons
        self.add = tk.Button(master=self.w, font=self.font, text="Add", width=10, command=self.add_entry)
        self.add.grid(row=2, column=3, pady=(50, 0))

        self.delete = tk.Button(master=self.w, font=self.font, text="Delete", width=10, command=self.delete_entry)
        self.delete.grid(row=3, column=3)

        self.exit = tk.Button(master=self.w, font=self.font, text="Exit", width=10, command=sys.exit)
        self.exit.grid(row=7, column=3)

    def select_row(self, event=None):
        pass

    def add_entry(self):
        # Get Input Data
        title = self.title.get()
        year = int(self.year.get())
        director = self.director.get()
        lead = self.lead.get()

        # Pass data to BackEnd
        self.bk.add_to_db(title, year, director, lead)
        self.show_all_databases()

    def delete_entry(self):
        pass

    def show_all_databases(self):
        rows = self.bk.get_all()
        for row in rows:
            # print database entries in listbox
            self.display.insert(tk.END, row)


window = tk.Tk()
movie_app = Front(window)
window.mainloop()
