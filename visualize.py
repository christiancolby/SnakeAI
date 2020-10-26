import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
import snake as s
import time
import collections as col
import copy
import settings

def visualize(snake):
    
    score = 0
    apples=copy.copy(snake.eaten_apple_locations)
    apples.append(copy.copy(snake.current_apple_location))
    apple=apples[0]
    stdscr = curses.initscr()   
    curses.noecho()             
    curses.cbreak()             
    stdscr.nodelay(1)  
    curses.curs_set(0)                          
     
    for i in snake.all_body_locations:
        counter=1
        stdscr.erase()
        for x in range(settings.game_size+1):
            stdscr.addch(x, settings.game_size+1, '|')
            stdscr.addch(settings.game_size+1,x, '-')
        stdscr.addch(settings.game_size+1,settings.game_size+1, '-')
        for j in i:
            stdscr.addch(j[1], j[0], str(counter))
            counter+=1
        while s.contains(apple,i):
            score+=1
            apple=apples[score]
        stdscr.addstr(0, settings.game_size+3, 'Score : ' + str(score) + ' ') 
        stdscr.addch(apple[1],apple[0],'*')
        stdscr.timeout(200)
        _ = stdscr.getch()
    curses.curs_set(1) 
    curses.echo()
    curses.nocbreak()
    curses.endwin()  
                            
