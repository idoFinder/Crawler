import pandas as pd
import os
import bs4 as bs
import urllib.request
from tkinter import *


def valid_url(url):
    try:
        urllib.request.urlopen(url)
        return True
    except(Exception):
        return False


def crawl(url_path, fileName):
    if valid_url(url_path):
        # url = 'https://www.calcudoku.org/sudoku/en/2019-02-15/9/2'
        sauce = urllib.request.urlopen(url_path).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')

        rows = soup.find_all("tr", id=lambda value: value and value.startswith("row"))
        puzzle_size = len(rows)

        # the sudoku matrix
        matrix = [[0 for x in range(puzzle_size)] for y in range(puzzle_size)]

        row_counter = 0
        for row in rows:
            cols = row.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['cell_large'])
            col_counter = 0
            for td in cols:
                if td.find('b') is None:
                    matrix[row_counter][col_counter] = '.'
                else:
                    matrix[row_counter][col_counter] = td.find('b').get_text()
                col_counter = col_counter + 1
            row_counter = row_counter + 1

        puzzle = pd.DataFrame(matrix)
        print(puzzle)

        if fileName:
            base_filename = fileName +'.txt'
        else: base_filename = 'Default.txt'
        with open(os.path.join("c:", base_filename), 'w') as outfile:
                puzzle.to_string(outfile, header=None, index=False)

        return(puzzle)


def crawlPuzzle():
    url_input = E.get()
    fileName = Ename.get()
    if url_input:
        df = crawl(url_input, fileName)
        if df is not None:
            feedback.set('Sudoku has been extracted!')
        else: feedback.set('Something wrong with the url   :(')


myGUI = Tk()
url = StringVar()
fileName = StringVar()
feedback = StringVar()
myGUI.geometry('600x300+300+300')
myGUI.title('The Sudoku Crawler')
Label(myGUI, text='Welcome to Sudoku Crawler', font=("Helvetica", 16)).pack()
Label(myGUI, text='Enter the URL: ').pack()
E = Entry(myGUI, textvariable=url, width=60)
E.pack()
Label(myGUI, text=' ').pack()
Label(myGUI, text='Choose file name: ').pack()
Ename = Entry(myGUI, textvariable=fileName, width=15)
Ename.pack()
Label(myGUI, text=' ').pack()
Button(myGUI, text='Crawl', fg='white', bg='dark green', command=crawlPuzzle, width=15).pack()
feedbackLable = Label(myGUI, textvariable=feedback)
feedbackLable.pack()
Label(myGUI, text='Created by Ido Finder © ').pack(side=BOTTOM)
myGUI.mainloop()










