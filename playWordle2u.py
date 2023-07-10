import random
import time
import selector
import cvzone
import pyautogui as pg
import numpy as np
import cv2
import json
from difflib import get_close_matches
from tkinter import *
import os
from tkinter import messagebox
class Game:
    def __init__(self):
        self.data = [*open("dict.txt").read().split("\n")]
        self.wd=[]
        self.suggest = ['jumpy', 'gowns', 'black', 'their']
        random.shuffle(self.suggest)
        print(self.suggest)


    def suggestions(self):
        return filter(lambda x: len(x) == 5 and "-" not in x, self.data)

    def check(self,wr):
        for x, i in enumerate(wr):
            for j in wr[x + 1:]:
                if i == j:
                    return False
        return True

    def checker(self, wr, word, exc):
        for x, i in enumerate(list(word)):
            if i.isupper():
                if i.lower() not in wr:
                    return False
                elif (i.lower() == wr[x-5]):
                    return False
            elif (i != "*"):
                if (i != wr[x]):
                    return False
        for i in wr:
            if i in exc:
                wd = word.lower()
                if i in wd:
                    if wd.count(i) == wr.count(i):
                        return True
                return False
        return True

    def checkerel(self, wr, word):
        for x, i in enumerate(word):
            if i.isupper():
                if i.lower() not in wr:
                    return False
            elif i != "*":
                print(self.exc)
                if i in self.exc:
                    return False
                if i not in wr or i == wr[x]:
                    return False
        return True

    def suggestions2(self, lsto):
        return filter(self.check, lsto)

    def suggestw(self, word, lsto, exc):
        return filter(lambda x: self.checker(x, word, list(exc)), lsto)

    def suggestrel(self, word, lsto):
        return filter(lambda x: self.checkerel(x, word), lsto)

    def translate(self, w):
        # converts to lower case
        w = w.lower()

        if w in self.data:
            return w
        # for getting close matches of word
        elif len(self.get_close_matches(w, self.data.keys())) > 0:
            alph = self.get_close_matches(w, self.data.keys())[0]
            if (len(alph) == 5):
                print(f' do u mean {alph}')
            # yn = yn.lower()
            # if yn == "y":
            #     return data[get_close_matches(w, data.keys())[0]]
            # elif yn == "n":
            #     return "The word doesn't exist. Please double check it."
            # else:
            #     return "We didn't understand your entry."
        else:
            return "The word doesn't exist. Please double check it."

    allposible = []

    def toString(self, List):
        wd = ''.join(List)
        return wd

    def getWord(self,word='',exc='',n=8):

        sug=[]
        if self.wd:
            sug = self.wd
        else:
            sug = self.data

        if n < 4 and len(word)-word.count("*") != 5:
            return self.suggest[n]
        else:
            self.wd=list(self.suggestw(word, sug, exc))
            if len(self.wd) == 0:
                print("Word do not exists in our dictionary")
                exit()
            rnm=random.randint(0, len(self.wd)-1)
            print(self.wd,rnm)
            return self.wd[rnm]


    def play(self):
        screenshot = pg.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        board=""
        folder_path = "./boardun"
        num_files = len(os.listdir(folder_path))
        for regi in range(1, num_files+1):
            board = pg.locateOnScreen(f'./boardun/wt{regi}.png')
            if board:
                break
        exe = ''
        word = ['', '', '', '', '', '*', '*', '*', '*', '*']
        roi = ""
        if not board:
            print("please choose the correct region")
            b_inf = list(map(int, selector.getSelection()))
            print(b_inf)
            if (b_inf[3]-b_inf[1])<100 or (b_inf[2]-b_inf[0])<120:
                menu()
            sc = pg.screenshot()
            roi = sc.crop(b_inf)
            roi.save(f"./boardun/wt{num_files + 1}.png")
            board = Obj(b_inf)

        prev = ""
        if board:
            cntgc=0
            errv = 4
            errw = 1
            bh = board.height
            bw = board.width
            bl = board.left
            bt = board.top
            blkh = (bh - errv) // 6
            blkw = (bw - errw) // 5
            cv2.rectangle(
                screenshot,
                (bl, bt),
                (bl + bw, bt + bh),
                (255, 255, 0),
                3)
            i = 0
            while i < 6:
                for ind in range(5):
                    if i == 0:
                        pg.click(bl, bt)
                    elif ind == 5:
                        break
                    print(ind)
                    cv2.rectangle(
                        screenshot,
                        (bl + blkw * ind, bt + blkh * i),
                        (bl + blkw * ind + blkw, bt + blkh * i + blkh),
                        (255, 0, 255),3)

                wrd = self.getWord(''.join(word), exe,i)
                if wrd == prev:
                    if roi != "": os.remove(f"./boardun/wt{num_files + 1}.png")
                    error()
                print(wrd, exe, word)
                # print("->",gm.getWord())
                pg.typewrite(wrd + "\n")
                # cv2.imshow("scrn",screenshot)
                # #smelt
                # cv2.waitKey(0)
                time.sleep(2)
                screenshot = pg.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                cntg = 0
                for wind in range(5):
                    xcor=bt + blkh * i + 8+i*2
                    ycor=bl + blkw * wind + blkw // 2
                    b, g, r = screenshot[xcor, ycor]
                    k=2
                    while [int(b), int(g), int(r)] == [255, 255, 255] or [int(b), int(g), int(r)] == [233, 225, 222]:
                        xcor = bt + blkh * i + 8 + i * 2+k
                        ycor = bl + blkw * wind + blkw // 2
                        b, g, r = screenshot[xcor, ycor]
                        k+=2
                    # print(xcor,ycor)
                    cv2.circle(screenshot, (ycor,xcor), 5, (0, 0, 255), -1)

                    print("**",r,g,b)
                    if [int(b), int(g), int(r)] == [55, 194, 243]:
                        word[wind+5] = wrd[wind].upper()
                    elif [int(b), int(g), int(r)] == [81, 184, 121]:
                        for upi, upx in enumerate(word[5:]):
                            if upx.lower() == wrd[wind].lower():
                                word[5+upi] = "*"
                        word[wind] = wrd[wind].lower()
                        cntg += 1
                    elif [int(b), int(g), int(r)] == [196, 174, 164]:
                        if(word[wind] == ''):
                            word[wind] = '*'
                        exe += wrd[wind].lower()
                    elif [int(b), int(g), int(r)] == [255, 252, 251]:
                        pg.typewrite(["backspace"] * 5)
                        i -= 1
                        print("-----------------------------")
                        screenshot = pg.screenshot()
                        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                        break
                    else:
                        print("xxxxxx ",[int(b), int(g), int(r)]," xxxxxxxxxx")
                        cv2.imshow("scrn", screenshot)
                        cv2.waitKey(0)
                        return 0
                    print("&*", word, exe, i)

                # cv2.imshow("scrn", screenshot)
                # cv2.waitKey(0)

                if cntg >= 5:
                    return 1
                i += 1

class Obj:
    def __init__(self,b_inf):
        self.top=b_inf[1]
        self.left=b_inf[0]
        self.width=b_inf[2]-b_inf[0]
        self.height=b_inf[3]-b_inf[1]
    
class Blockc:
    def findColor(self,img,y,x):
        b,g,r = img[y,x]
        return [int(b),int(g),int(r)]
    def isGreen(self,img,y_,x_):
        if [78,141,83]==self.findColor(self,img,y_,x_):
            return True
        return False
    def isYellow(self,img,y_,x_):
        if [59,159,181]==self.findColor(self,img,y_,x_):
            return True
        return False
    def isgrey(self,img,y_,x_):
        if [60,58,58]==self.findColor(self,img,y_,x_):
            return True
        return False

#rgb(83,141,78)gr
#rgb(181,159,59)yel
#rgb(58,58,60)gry


def startGame(ref):
    ref.destroy()
    gm = Game()
    gm.play()

def error():
    mn = Tk()
    messagebox.showerror("Error", "We faced issue in detecting grid region selected by you! Please try to select exact grid next time.")
    exit()
    mn.mainloop()

def menu():
    mn = Tk()
    mn.geometry('%dx%d+%d+%d' % (300, 50, mn.winfo_screenwidth() // 2, mn.winfo_screenheight() // 2))

    button = Button(mn, text='Solve', command=lambda: startGame(mn))
    button.pack(side=TOP, pady=5)
    mn.mainloop()


if __name__ == '__main__':
    menu()

#print(blk.findColor(screenshot, bt+blkh*1+5, bl+blkw*1+5))

# ['least', 'tales', 'steal', 'slate', 'stale', 'teals', 'tesla', 'taels', 'stela']
# ['spare', 'spear', 'pears', 'reaps', 'pares', 'rapes', 'parse', 'apers']



