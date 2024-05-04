# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 00:47:24 2024

@author: someone
"""

from PIL import Image, ImageGrab
import tkinter as tk
import time
from pynput.mouse import Controller, Button

def add_xy(xy,template_xy):
    new_x = xy[0]+template_xy[0]
    new_y = xy[1]+template_xy[1]
    new_xy = (new_x,new_y)
    return new_xy

def compare_RGB(RGB1,RGB2):
    loss = 0
    loss += abs(RGB1[0] - RGB2[0])
    loss += abs(RGB1[1] - RGB2[1])
    loss += abs(RGB1[2] - RGB2[2])
    return loss

def GetCells():
    Cells = {}
    for y in range(16):
        for x in range(30):
            Cell = (x,y)
            Cells[Cell] = 0
    return Cells


def Detect():

    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
    
    screenshot = screenshot.convert("RGB")
    print("Screenshot taken, analysing image...")

    
    template = Image.open("template.png").convert("RGB")
    template_xys = [(0,0),(250,0),(500,0),(0,250),(755,0),(755,250),(0,509),(250,509),(500,509),(755,509)]
        
    anchor = ()
    target_loss = 50
    length = len(template_xys)


    for y in range(300, 1080-509, 1):
        for x in range(100, 1920-755, 1):
            xy = (x,y)
            loss = 0
            i = 0
            criterion = True
            
            while criterion:
                template_xy = template_xys[i]
                r, g, b = template.getpixel(template_xy)
                RGB1 = (r,g,b)
                
                screenshot_xy = add_xy(xy,template_xy)       
                r2, g2, b2 = screenshot.getpixel(screenshot_xy)
                RGB2 = (r2,g2,b2)
                
                loss += compare_RGB(RGB1,RGB2)
                i += 1
                criterion = loss < target_loss and i < length

            if loss < target_loss:
                anchor = (x,y)
                
    
    if anchor == ():
        print("Could not detect anchor!")
        label_message.config(text="Could not detect anchor!")
    else:
        print("Anchor detected: " + str(anchor))
        anchor_x = anchor[0]
        anchor_y = anchor[1]
        
        flag = Image.open("flag.png").convert("RGB")
        mine = Image.open("mine.png").convert("RGB")
        mine2 = Image.open("mine2.png").convert("RGB")
        
        flag_xys = []
        for y in range(0,24,2):
            for x in range(0,24,2):
                flag_xys.append((x,y))


        target_loss = 200    
        detected_mines = 0

        board = GetCells()

        for y in range(anchor_y+81,anchor_y+464,24):
            for x in range(anchor_x+18,anchor_x+737,24):
                
                xy = (x,y)
                loss = 0
                
                for i in range(144): #Flag
                    flag_xy = flag_xys[i]            
                    r, g, b = flag.getpixel(flag_xy)
                    RGB1 = (r,g,b)
                    
                    screenshot_xy = add_xy(xy,flag_xy)       
                    r2, g2, b2 = screenshot.getpixel(screenshot_xy)
                    RGB2 = (r2,g2,b2)
                    
                    loss += compare_RGB(RGB1,RGB2)          
                
                if loss < target_loss:    
                    
                    Cell_x = (x - anchor_x - 18) // 24
                    Cell_y = (y - anchor_y - 81) // 24
                    Cell = (Cell_x,Cell_y)
                    board[Cell] = 1
                    detected_mines += 1
                   
                loss = 0
                for i in range(144): #Mine
                    mine_xy = flag_xys[i]            
                    r, g, b = mine.getpixel(mine_xy)
                    RGB1 = (r,g,b)
                    
                    screenshot_xy = add_xy(xy,mine_xy)       
                    r2, g2, b2 = screenshot.getpixel(screenshot_xy)
                    RGB2 = (r2,g2,b2)
                    
                    loss += compare_RGB(RGB1,RGB2)          
                
                if loss < target_loss:    
                    
                    Cell_x = (x - anchor_x - 18) // 24
                    Cell_y = (y - anchor_y - 81) // 24
                    Cell = (Cell_x,Cell_y)
                    board[Cell] = 1
                    detected_mines += 1

                loss = 0
                for i in range(144): #Mine2
                    mine2_xy = flag_xys[i]            
                    r, g, b = mine2.getpixel(mine2_xy)
                    RGB1 = (r,g,b)
                    
                    screenshot_xy = add_xy(xy,mine2_xy)       
                    r2, g2, b2 = screenshot.getpixel(screenshot_xy)
                    RGB2 = (r2,g2,b2)
                    
                    loss += compare_RGB(RGB1,RGB2)          
                
                if loss < target_loss:    
                    
                    Cell_x = (x - anchor_x - 18) // 24
                    Cell_y = (y - anchor_y - 81) // 24
                    Cell = (Cell_x,Cell_y)
                    board[Cell] = 1
                    detected_mines += 1

            
        print("Mines Detected: " + str(detected_mines))
        label_message.config(text="Mines Detected: " + str(detected_mines))
        
        file = open("board.txt","w")
        for y in range(16):
            if y > 0:
                file.writelines("\n")
            for x in range(30):
                Cell = (x,y)
                if board[Cell] == 1:
                    file.writelines("*")
                else:
                    file.writelines("-")
        file.close()
		
        print("Saved board as board.txt")
        label_message.config(text="Saved board as board.txt")
		



def AutoClick():
    mouse = Controller()

    print("Ready")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)

    file = open("board.txt","r")

    for y in range(16):
        line = file.readline()[0:30]
        print(line)
        for x in range(30):
            if x > 0:
                mouse.move(24,0)
            time.sleep(0.01)
            if line[x] == "*":
                mouse.click(Button.right,1)
                
        mouse.move(-696,24)
        time.sleep(0.01)

    label_message.config(text="Done")

root = tk.Tk()
root.geometry("300x150")
root.config(bg="#000000")

label_Title = tk.Label(root,text="Convenient MBF maker",fg="#FFFFFF", bg="#000000",font=("Verdana",15))
label_Title.place(relx=0.5,rely=0.25,anchor="center")

label_message = tk.Label(root,text="",fg="#FFFFFF", bg="#000000",font=("Verdana",10))
label_message.place(relx=0.5,rely=0.85,anchor="center")

button_Detect = tk.Button(root,width=8, text="Detect", command=Detect)
button_Detect.place(relx=0.2, rely=0.6, anchor="center")

button_Autoclick = tk.Button(root,width=8, text="Autoclick", command=AutoClick)
button_Autoclick.place(relx=0.5, rely=0.6, anchor="center")

root.attributes('-topmost', 'true')
root.mainloop()
