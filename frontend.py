import tkinter as tk
import backend
import sys
import requests
from bs4 import BeautifulSoup
from pytube import YouTube
import os
import subprocess


class Front(object):
    def __init__(self, w):
        # Connect with BackEnd
        self.bk = backend.Back()

        # Link window and add main characteristics
        self.w = w
        self.w.title("Movie Database App")
        self.w.geometry("825x510")
        self.font = ("Arial", 14)
        self.small_font = ("Arial", 10)

        self.last_selected = 0

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
        self.display = tk.Listbox(master=self.w, height=18, width=55, font=self.small_font)
        self.display.grid(row=2, column=0, rowspan=15, columnspan=2, padx=(25, 20), pady=50)
        self.display.bind("<<ListboxSelect>>", self.select_row)
        # Add a Scrollbar
        self.scroll = tk.Scrollbar(master=self.w)
        self.scroll.grid(row=2, column=1, sticky="nse", rowspan=15, padx=(25, 20), pady=50)
        # Link Scrollbar to Main Display
        self.scroll.config(command=self.display.yview)

        # Create Buttons
        self.show = tk.Button(master=self.w, font=self.font, text="Show All", width=10, command=self.show_all_databases)
        self.show.grid(row=2, column=3, pady=(50, 0))

        self.add = tk.Button(master=self.w, font=self.font, text="Add", width=10, command=self.add_entry)
        self.add.grid(row=3, column=3)

        self.delete = tk.Button(master=self.w, font=self.font, text="Delete", width=10, command=self.delete_entry)
        self.delete.grid(row=4, column=3)

        self.update = tk.Button(master=self.w, font=self.font, text="Update", width=10, command=self.update_entry)
        self.update.grid(row=5, column=3)

        self.search = tk.Button(master=self.w, font=self.font, text="Search", width=10, command=self.search_entry)
        self.search.grid(row=6, column=3)

        self.play = tk.Button(master=self.w, font=self.font, text="Trailer", width=10, command=self.play_trailer)
        self.play.grid(row=7, column=3)

        self.exit = tk.Button(master=self.w, font=self.font, text="Exit", width=10, command=sys.exit)
        self.exit.grid(row=8, column=3)

        # Display DB
        self.show_all_databases()

    def select_row(self, event=None):
        rows = self.display.curselection()  # print(rows)
        try:
            line = self.display.get(rows[0])
        except:
            return ()
        # Display selected entry in textEdit boxes above for editing
        self.title_text.set(line[1])
        self.year_text.set(line[2])
        self.director_text.set(line[3])
        self.lead_text.set(line[4])

        self.last_selected = line[0]

        return line

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
        line = self.select_row()
        # call the BackEnd method to delete
        try:
            self.bk.del_from_db(line[0])
        except:
            pass
        self.show_all_databases()

    def update_entry(self):
        # Get Input Data
        title = self.title.get()
        year = int(self.year.get())
        director = self.director.get()
        lead = self.lead.get()
        # Call BackEnd to Update the Database
        self.bk.update_db(title, year, director, lead, self.last_selected)

        self.show_all_databases()

    def search_entry(self):
        # Get Input Data
        title = self.title.get()
        year = self.year.get()
        director = self.director.get()
        lead = self.lead.get()

        rows = self.bk.search_db(title, year, director, lead)
        self.display.delete(0, tk.END)
        for row in rows:
            # print database entries in listbox
            self.display.insert(tk.END, row)

    def show_all_databases(self):
        rows = self.bk.get_all()
        self.display.delete(0, tk.END)
        for row in rows:
            # print database entries in listbox
            self.display.insert(tk.END, row)

    def play_trailer(self):
        # Query: title + year + "trailer"
        title = self.title.get()
        year = self.year.get()
        query = "{} {} trailer".format(title, year)

        page = requests.get("http://google.com/search?hl=en&q={}".format(query))

        soup = BeautifulSoup(page.content, features="html.parser")
        # Get links from page content
        links = soup.find_all("a")

        for link in links:
            link_parsed = link.get("href")

            if "youtube" in link_parsed:
                # print("Final link is", link_parsed)
                break

        # Clean Final Link to Match Expectations
        final_link = link_parsed.replace("/url?q=", "")
        sa_pos = final_link.find("&sa")
        final_link = final_link[0:sa_pos]
        final_link = final_link.replace("%3Fv%3D", "?v=")

        yt = YouTube(final_link)
        filename = title.lower().replace(" ", "_")
        stream = yt.streams.get_highest_resolution()
        stream.download("", filename)

        if tk.sys.platform == "win32":
            # Windows User
            os.startfile("{}.mp4".format(filename))
        else:
            # MacOS User
            subprocess.call(["open", "{}.mp4".format(filename)])


window = tk.Tk()
movie_app = Front(window)
window.mainloop()
