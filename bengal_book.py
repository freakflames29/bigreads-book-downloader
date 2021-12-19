import requests as rq
from bs4 import BeautifulSoup as bs

class BengaliBook:
    def __int__(self):
        self.book_found = False
    def find_book(self,bookname):
        space_removed=bookname.replace(" ","+")
        url="https://www.banglabook.org/?s="+space_removed
        page=rq.get(url)
        soup=bs(page.content,"html.parser")
        names=soup.select(".post-entry h2 a")
        if len(names)>0:
            for name in names:
                if  bookname.casefold() in name.text.casefold():
                    self.book_found=True
                    return name.get("href")
        else:
            return False

# ob=BengaliBook()
# out=ob.find_book("rabindranath ekhane")
# print(out)