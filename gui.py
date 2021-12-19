import time
import requests as rq
from bs4 import BeautifulSoup as bs
from tkinter import *
from bengal_book import BengaliBook


class Gui:
    def __init__(self):
        self.one_lib_home = "https://1lib.in"
        self.pdfdrive_home = "https://www.pdfdrive.com"
        self.int_arch_home = "https://archive.org"
        self.libFound = False
        self.int_arch_Found = False
        self.pdfdriveFound = False
        self.google_found = False
        self.root = Tk()
        self.root.title("Bigreads Book downloder")
        self.found = Label(self.root, text="")
        self.root.geometry("450x200")
        self.output = Text(self.root, height=2, width=50)
        self.btnClick = False

        self.root.minsize(450, 200)
        self.root.maxsize(450, 200)
        self.root.resizable(width=False, height=False)

    try:
        def check_one_lib(self, book_name):
            space_removed = book_name.replace(" ", "%20")
            one_lib_search_url = "https://1lib.in/s/"
            url = one_lib_search_url + space_removed
            page = rq.get(url)
            soup = bs(page.content, 'html.parser')
            names = soup.select(".bookRow h3 a")
            if len(names) > 0:
                for name in names:
                    if book_name.casefold() in name.text.casefold():
                        self.libFound = True
                        return self.one_lib_home + name.get("href")
            else:
                self.libFound = False
                return self.libFound

        def check_pdfdrive(self, book_name):
            space_removed = book_name.replace(" ", "%20")
            one_lib_search_url = "https://www.pdfdrive.com/search?q="
            url = one_lib_search_url + space_removed
            page = rq.get(url)
            soup = bs(page.content, 'html.parser')
            names = soup.select(".file-right a")
            if len(names) > 0:
                for name in names:
                    if book_name.casefold() in name.text.casefold():
                        self.pdfdriveFound = True
                        return self.pdfdrive_home + name.get("href")
            else:
                self.pdfdriveFound = False
                return self.pdfdriveFound

        def check_int_arch(self, book_name):
            space_removed = book_name.replace(" ", "+")
            if "'" in space_removed:
                space_removed = space_removed.replace("'", "%27")

            one_lib_search_url = "https://archive.org/details/internetarchivebooks?query="
            url = one_lib_search_url + space_removed
            page = rq.get(url)
            soup = bs(page.content, 'html.parser')
            book_names = soup.select(".C234 div .ttl")
            book_links = soup.select(".C234 div a")
            if len(book_names) > 0 and len(book_links) > 0:
                for i in range(len(book_names)):
                    if book_name.casefold() in book_names[i].text.casefold():
                        self.int_arch_Found = True
                        return self.int_arch_home + book_links[i].get("href")
            else:
                self.int_arch_Found = False
                return self.int_arch_Found

        def google_Found(self, book_name):
            space_removed = book_name.replace(" ", "+")
            if "'" in space_removed:
                space_removed = space_removed.replace("'", "%27")
            google_search_url = "https://www.google.com/search?q={quer}+filetype%3Apdf".format(quer=space_removed)
            return google_search_url
    except ConnectionError as e:
        print("Connet to net")

    def buffer(self):
        if self.btnClick:
            self.found.configure(text="Connect to internet")
            self.found.pack()
            return

    def if_found(self, text, link):
        self.found.configure(text=text)
        self.found.pack()
        self.output.delete("1.0", "end-1c")
        self.output.insert(END, link)
        self.output.pack()

    def find(self):
        txt = self.inp.get("1.0", "end-1c")
        if len(txt) > 0:
            self.btnClick = True
            self.buffer()
            onelib = self.check_one_lib(txt)
            if onelib:
                text = txt.capitalize() + " Book Found!"

                self.if_found(text, onelib)
            else:
                pdfdrive = self.check_pdfdrive(txt)
                if pdfdrive:
                    text = txt.capitalize() + " Book Found!"
                    self.if_found(text, pdfdrive)

                else:
                    int_arch = self.check_int_arch(txt)
                    if int_arch:
                        text = txt.capitalize() + " Book Found!"
                        self.if_found(text, int_arch)

                    else:
                        bengal_book = BengaliBook()
                        link = bengal_book.find_book(txt)
                        if link:
                            text = txt.capitalize() + " Book Found!"
                            self.if_found(text, link)

                        else:
                            google = self.google_Found(txt)
                            text = "Google link!"
                            self.if_found(text, google)

        else:
            self.found.configure(text="Enter a valid book name")
            self.found.pack()

    def start(self):
        self.label = Label(self.root, text="Enter the name of the Book ")
        self.inp = Text(self.root, height=2, width=30)
        self.btn = Button(self.root, text="Find the book", command=self.find)
        self.space_label = Label(self.root, text="  ")

        self.space_label.pack()
        self.label.pack()
        self.inp.pack()
        self.btn.pack()
        self.root.mainloop()


ob = Gui()
ob.start()
