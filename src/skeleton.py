#!/usr/bin/python
# coding: utf-8
'''
Name: skeleton.py
Author: Stevan Gostojić
Date: 16. 04. 2012.
Description: Text editor skeleton.
Note: The program has to be run from the command prompt
'''

# pydevd modul se mora uvesti da bi se program debagovao udaljenim debagerom
#import pydevd; pydevd.settrace()
import curses
import string
import dlist

class Editor:

    def __init__(self):

        self.text = dlist.DoubleList()
        self.text.append(" ")    
        
        
        # Tekuca pozicija kursora
        self.y = 0
        self.x = 0
        self.i=1
        # Pozicija gornjeg levog ugla ekrana
        self.line = 0
        self.column = 0
    
        # Broj linija teksta
        self.lines = 1
        # Duzina najduze linije u tekstu
        self.columns = 1
        
        self.insert_mode = False
        self.select_mode = False
        
        # Inicijalizacija curses biblioteke
        self.stdscr = curses.initscr()
        curses.nonl() 
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        
        # Visina i sirina ekrana   
        self.height, self.width = self.stdscr.getmaxyx()
        # Uzeti u obzir meni i statusnu liniju
        self.height -= 2


        
    def __del__(self):
        curses.nocbreak(); self.stdscr.keypad(0); curses.echo()
        curses.endwin()
        
    def draw(self):    
        # Cisti ekran
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "| F1 - Help | F2 - New | F3 - Load | F4 - Save |")
        
        i=1
        for s in self.text.values()[self.line : self.line + self.height]:
            self.stdscr.addstr(i,0,s[self.column : self.column + self.width -1])
            i+=1
        
        self.stdscr.addstr(self.height + 1, 0, "Ln: " + str(self.line + self.y + 1) + "\tCol: " + str(self.column + self.x + 1) + "\tFile: " + "test.txt" +"\tLs:" +str(self.lines))
        
        # Pomera kurson na tekuce koordinate
        self.stdscr.move(self.y + 1, self.x)
        
        self.columns = len(max(self.text.values(), key=len)) - self.width
        
        
        # Osvezava ekran
        self.stdscr.refresh()
        
        
        
    def left(self):
        if self.x > 0:
            self.x -= 1
        elif self.column > 0:
            self.column -= 1
        elif self.y > 0 and len(self.text.index(self.line + self.y-1)) < self.width - 1: 
            self.y -= 1
            if len(self.text.index(self.line + self.y)) - 1 > 0:
                self.x = len(self.text.index(self.line + self.y)) 
            else:
                self.x = 0
        elif self.y > 0:
                self.column = len(self.text.index(self.line + self.y-1)) - self.width+1
                self.x = self.width -1
                self.y -= 1
        elif self.line > 0:
            self.line -= 1
            if len(self.text.index(self.line + self.y)) - 1 > 0:
                self.x = len(self.text.index(self.line + self.y)) 
            else:
                self.x = 0
    
    
    
    def right(self):
        if self.x < len(self.text.index(self.line+self.y)) and self.x < self.width -1 :
                    self.x += 1
        elif len(self.text.index(self.line+self.y)) > self.width - 1 and self.column < len(self.text.index(self.line+self.y))-self.width+1:
                self.column+=1
        elif self.lines < self.height:
            if self.line +self.y < self.lines - 1:
                self.y += 1
                self.x = 0
                self.column = 0
        elif self.y < self.height - 1:
            self.y+=1
            self.x = 0
            self.column = 0
        elif self.line < self.lines - self.height-1:
            self.line += 1
            self.x = 0
            self.column = 0
                
    
    
    def up(self):
        if self.lines < self.height:
            if self.line + self.y > 0:
                self.y -= 1
        else:
            if self.y > 0:
                self.y -= 1
            elif self.line > 0:
                self.line -= 1
        if self.x > len(self.text.index(self.line + self.y)):
                self.x = len(self.text.index(self.line + self.y)) - self.column
#        else:
#                self.x = 0  
    
    def down(self):
        
        if self.lines < self.height:
            if self.line +self.y < self.lines - 1:
                self.y += 1
        else:
            if self.y < self.height - 1:
                self.y += 1
            elif self.line < self.lines - self.height:
                self.line += 1
                    
        if self.x > len(self.text.index(self.line + self.y)):
                self.x = len(self.text.index(self.line + self.y))-self.column
        # Postavlja kurson na kraj linije ukoliko je ona kraca od tekuce linije
#        if len(self.text.index(self.line + self.y)) - 1 > 0:
#                self.x = len(self.text.index(self.line + self.y))- 1
#        else:
#                self.x = 0
            
    
    
    def home(self):
        
        self.x = 0
        self.column = 0
        
    
    
    def end(self):
        if len(self.text.index(self.line + self.y)) > self. width:
            self.column = len(self.text.index(self.line + self.y)) - self.width+1
            self.x = self.width-1
        else:
            self.x = len(self.text.index(self.line + self.y))
        
    
    def page_up(self):
        
        if self.line > self.height - 1:
            self.line -= self.height
        elif self.line > 0:
            self.line = 0
        elif self.y > 0:
            self.y = 0
        
#         Postavlja kurson na kraj linije ukoliko je ona kraca od tekuce linije
#        if len(self.text.index(self.line + self.y)) - 1 > 0:
#                self.x = len(self.text.index(self.line + self.y))
#        else:
#                self.x = 0
    
    
    
    def page_down(self):
        if self.lines < self.height:
            self.y=self.lines-1
        elif self.line + self.height < self.lines - self.height:
            self.line += self.height 
        elif self.line + self.height < self.lines -1 :
            self.line += self.lines - (self.line + self.height)
        elif self.y < self.lines-1:
            self.y = self.height - 1
            if self.line+self.height < self.lines:
                self.line+=1
#            
#        if len(self.text.index(self.line + self.y)) - 1 > 0:
#                self.x = len(self.text.index(self.line + self.y))
#        else:
#                self.x = 0
    def enter(self):
        
        prefix = self.text.index(self.line + self.y)[:self.column + self.x]
        suffix = self.text.index(self.line + self.y)[self.column + self.x:]
        self.text.insertIndex(self.line + self.y, prefix)
        self.text.insertIndex(self.line + self.y + 1, suffix)
        self.text.removeIndex(self.line + self.y + 2)
        
        self.lines += 1
    
        if self.y < self.height - 1:
            self.y += 1
        elif self.line < self.lines - 1:
            self.line += 1
        else:
            self.line = self.lines
            
        self. x = 0
        self.column = 0
    
    
    
    def backspace(self):
    
        if self.x>0:
            prefix = self.text.index(self.line + self.y)[:self.column + self.x-1]
            suffix = self.text.index(self.line + self.y)[self.column + self.x:]
            self.text.insertIndex(self.line + self.y, prefix+suffix)
            self.text.removeIndex(self.line + self.y + 1)
            
        elif self.x==0 and self.y>0:
            prefix= self.text.index(self.line + self.y-1)[self.column+self.x:]
            suffix= self.text.index(self.line+self.y)[self.column+self.x:]
            self.text.insertIndex(self.line+self.y-1, prefix+suffix)
            self.text.removeIndex(self.line+self.y)
            self.text.removeIndex(self.line+self.y)
            if len(prefix)>self.width -1:
                self.column += len(prefix) - self.width+2
                self.x= self.width -1
            else:
                self.x=len(prefix)+1
            if self.line+self.height==self.lines and self.line>0:
                self.line-=1
            else:
                self.y-=1
            self.lines -= 1
             
        if self.column > 0:
            self.column-=1
        elif self.x > 0:
            self.x -= 1
        elif self.y > 0:
            self.y-=1
            
    def delete(self):
    
        if  self.x < len(self.text.index(self.line+self.y)) :
            prefix = self.text.index(self.line + self.y)[:self.column + self.x]
            suffix = self.text.index(self.line + self.y)[self.column + self.x+1:]
            self.text.insertIndex(self.line + self.y, prefix+suffix)
            self.text.removeIndex(self.line + self.y + 1)
            
        elif self.x==len(self.text.index(self.line+self.y)) and self.line+self.y < self.lines-1:
            self.lines-=1
            prefix= self.text.index(self.line + self.y)[:self.column+self.x]
            suffix= self.text.index(self.line+self.y+1)[:-1]
            self.text.insertIndex(self.line+self.y, prefix+suffix)
            self.text.removeIndex(self.line+self.y+1)
            self.text.removeIndex(self.line+self.y+1)
            if self.line > 0:
                self.line-=1
                self.y+=1
                    
    
    def printable(self, ch):
        if self.insert_mode:
            prefix = self.text.index(self.line + self.y)[:self.column + self.x]
            if self.column + self.x < len(self.text.index(self.line + self.y)) - 1:
                suffix = self.text.index(self.line + self.y)[self.column + self.x + 1:]
            else:
                suffix = ""
            self.text.insertIndex(self.line + self.y, prefix + chr(ch) + suffix)
            self.text.removeIndex(self.line + self.y + 1)
        else:
            prefix = self.text.index(self.line + self.y)[:self.column + self.x]
            suffix = self.text.index(self.line + self.y)[self.column + self.x:]
            self.text.insertIndex(self.line + self.y, prefix + chr(ch) + suffix)
            self.text.removeIndex(self.line + self.y + 1)
        
        if self.x < self.width - 1:
            self.x += 1
        elif self.column < self.columns - self.width:
            self.column += 1
        else:
            self.column += 1
            self.columns += 1
    
    
    
    def new(self):
        self.text = dlist.DoubleList()
        self.text.append("")        
        
        # Trenutna pozicija kursora
        self.y = 0
        self.x = 0
        
        # Visina i sirina ekrana   
        self.height, self.width = self.stdscr.getmaxyx()
        self.height -= 2
        
        # Pozicija gornjeg levog ugla ekrana
        self.line = 0
        self.column = 0
        self.columns=1
    
        # Broj linija teksta
        self.lines = self.text.size()
        # Duzina najduze linije teksta
        self.columns = len(max(self.text.values(), key=len)) - self.width
    
    
    
    def load(self, filename):
        self.text = dlist.DoubleList()
        self.f= open(filename,'r')
        for line in self.f:
            self.text.append(line[:-1])
        self.f.close()    
        
        self.y = 0
        self.x = 0

        
        self.height, self.width = self.stdscr.getmaxyx()
        self.height -= 2
        
        self.line = 0
        self.column = 0
        
        self.lines = self.text.size()
        self.columns = len(max(self.text.values(), key=len)) - self.width
        
    
    def save(self, filename):
        
        self.stdscr.clear()
        self.stdscr.addstr(10, 20, "File Name:")
        
        curses.echo()
        if self.stdscr.getch()!=27:
            filename = self.stdscr.getstr()
            f = open (filename, 'w')
            for line in self.text.values():
                f.write(line + '\n')
            f.close()
            curses.noecho()
        else:
            pass
        
    def Help(self):
        
        curses.echo()
        while self.stdscr.getch()!=27:
            
            curses.curs_set(0)
            self.stdscr.clear()
            self.stdscr.addstr(1,30,"Text Editor" ,curses.A_BOLD)
            self.stdscr.addstr(1,1,"23.06.2012", curses.A_REVERSE)
            self.stdscr.addstr(1,54," Press ESC to exit Help ")
            self.stdscr.addstr(1,54,"|", curses.A_BLINK)
            self.stdscr.addstr(1,78,"|", curses.A_BLINK)
            self.stdscr.addstr(0,54,"-------------------------",curses.A_BLINK)
            self.stdscr.addstr(2,54,"-------------------------" ,curses.A_BLINK)
            self.stdscr.addstr(5,1,"Authors: Marko Kalinic i Aleksandar Pivin.")
            self.stdscr.addstr(7,1,"Short Description: ")
            self.stdscr.addstr(9,1,"This is program made for creating and/or manipulating text files.")
            self.stdscr.addstr(10,1,"In current versions, only functuons available are: ")
            self.stdscr.addstr(12,2," - New ")
            self.stdscr.addstr(13,2," - Load ")
            self.stdscr.addstr(14,2," - Save ")
            self.stdscr.addstr(16,1,"Keyboard shortcuts can be found at the header of the main program window.")
            self.stdscr.addstr(17,1,"User can move trough the text using arrows, pgup, pgdown, home and end buttons.")
            self.stdscr.addstr(18,1,"To delete text, user can use backspace and delete buttons (default).")
            self.stdscr.addstr(24,0,"Send descriptions of all bugs and glitches to: kalestri@hotmail.com ")
            
            curses.noecho()
        
        
    def loop(self):
        # Pravi prazan dokument
        self.new()   
        
        while True:
            
            assert 0 <= self.y and self.y <= self.height - 1
            assert 0 <= self.x and self.x <= self.width - 1
            assert 0 <= self.line
            assert 0 <= self.column
            
            self.draw()
            
            # Cita taster   
            ch = self.stdscr.getch()
            
            # Escape
            if ch == 27:
                break
            # Left Arrow
            elif ch == curses.KEY_LEFT:
                self.left()
            # Right Arrow
            elif ch == curses.KEY_RIGHT:
                self.right()
            # Up Arrow
            elif ch == curses.KEY_UP:
                self.up()
            # Down Arrow
            elif ch == curses.KEY_DOWN: 
                self.down()
            # Home
            elif ch == curses.KEY_HOME:
                self.home()
            # End
            elif ch == curses.KEY_END:
                self.end()
            # Page Up
            elif ch == curses.KEY_PPAGE:
                self.page_up()
            # Page Down
            elif ch == curses.KEY_NPAGE:
                self.page_down()
            # Enter key
            elif ch == 10 or ch == 13:
                self.enter()
            # Backspace
            elif ch == 8:
                self.backspace()
            # Delete
            elif ch == curses.KEY_DC:
                self.delete()
            # Insert
            elif ch == curses.KEY_IC:
                self.insert_mode = not self.insert_mode
            # F1
            elif ch == curses.KEY_F1:
                self.Help()
            # F2
            elif ch == curses.KEY_F2:
                self.new()
            # F3
            elif ch == curses.KEY_F3:
                self.load("test.txt")
            # F4
            elif ch == curses.KEY_F4:
                self.save("test.txt")
                
            # Undo
            elif ch == curses.KEY_F5:
                self.undo()
            
            # Printable characters		            
            elif chr(ch) in string.printable:
                self.printable(ch)
            
            # Postavlja mod kursora
            if self.insert_mode:
                curses.curs_set(2)
            else:
                curses.curs_set(1)


        
if __name__ == "__main__":
    editor = Editor()
    editor.loop()
