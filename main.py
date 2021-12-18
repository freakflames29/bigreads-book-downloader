import requests as rq
from bs4 import BeautifulSoup as bs


class Book:
    def __init__(self):
        self.one_lib_home = "https://1lib.in"
        self.pdfdrive_home = "https://www.pdfdrive.com"
        self.int_arch_home = "https://archive.org"
        self.libFound = False
        self.int_arch_Found = False
        self.pdfdriveFound = False
        self.google_found = False

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
        page = rq.  get(url)
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


ob = Book()
print("Welcome to bigreads book downloader")
print("Enter the name of the book you want to download >",end=" ")
book_name = input()
one_lib=ob.check_one_lib(book_name)
if one_lib:
    print("Book found!")
    print("Link:- ",one_lib)
else:
    print("Book not found!")
    print("Checking another site!")
    pdfdrive=ob.check_pdfdrive(book_name)
    if pdfdrive:
        print("Book found!")
        print("Link:- ",pdfdrive)
    else:
        print("Not found!")
        print("Checking another site!")
        int_arch=ob.check_int_arch(book_name)
        if int_arch:
            print("Book found!")
            print("Link:- ",int_arch)
        else:
            print("Not found!")
            print("Checking google!")
            google_url=ob.google_Found(book_name)
            print(google_url)
