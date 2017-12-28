###   Created by Nick Wallace  ###
###                            ###
###                            ###

import re
from tkinter import *
from tkinter import font
from bs4 import BeautifulSoup
from urllib.request import urlopen
from PIL import ImageTk, Image
from collections import OrderedDict
    
root = Tk()
root.title("MTA Service Status")
root.configure(background = "white")
root.attributes('-fullscreen', True)

root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 1)
root.columnconfigure(2, weight = 1)
root.columnconfigure(3, weight = 1)

header_font = font.Font(family='Heveltica', weight = 'bold', size=13)
main_font = font.Font(family = 'Heveltica', size = 12)

def getData():
    global sort

    url = 'http://web.mta.info/status/serviceStatus.txt'
    xml = urlopen(url).read()
    soup = BeautifulSoup(xml, "xml")
    timestamp = soup.timestamp.text
    subway = soup.subway
    status_dict = {}
    all_lines = subway.findAll('line')
    for line in all_lines:
        line.find('line')
        for info in line: 
            name = line.find('name').text
            status = line.find('status').text
            text = line.find('text').text
            text = text.replace('&lt;','<').replace('&gt;','>').replace('&nbsp;',' ')
            
            if line.find('Date').text == '': 
                datetime = re.sub(':[:]*.{2}[:]* {1}', '', timestamp)
            else:
                datetime = line.find('Date').text.strip(' ') + ' ' + line.find('Time').text.strip(' ')
            status_line = [status, datetime, text]
        status_dict[name] = status_line
    sort = OrderedDict(sorted(status_dict.items()))
    return sort

def firstRun(dict):
    global labels
    labels = {}
    
    header_img = Label(root, text = 'LINE', font = header_font, bg = 'white')
    header_img.grid(columnspan = 2)
    
    header_name = Label(root, text = 'STATUS', anchor = 'center', font = header_font, bg = 'white')
    header_name.grid(row = 0, column = 2)
    
    header_timestamp = Label(root, text = 'TIME', anchor = 'center', font = header_font, bg = 'white')
    header_timestamp.grid(row = 0, column = 3)
    
    rc = 1
    
    for k, v in dict.items():
        img_url = 'img/' + k + '.png'
        img = ImageTk.PhotoImage(Image.open(img_url))

        Grid.rowconfigure(root, rc, weight=1)
        Grid.columnconfigure(root, rc, weight=1)
        
        line_img = Label(root, image = img, bg = 'white')
        line_img.image = img
        line_img.grid(row = rc, columnspan = 2)
        
        #line_name = Label(root, text = k, bg = 'white')
        #line_name.grid(row = rc, column = 1, sticky = W)
        labels[(rc, 1)] = k
        
        line_status = Label(root, text = ' ' + v[0], font = main_font, bg = 'green' if v[0] == 'GOOD SERVICE' else 'yellow' if v[0] == 'PLANNED WORK' else 'red')
        line_status.grid(row = rc, column = 2)
        if v[0] not in ['GOOD SERVICE']: line_status.bind('<Button-1>', addMessage)
        labels[(rc, 2)] = line_status
  
        line_timestamp = Label(root, text = ' ' + v[1], font = main_font, bg = 'white')
        line_timestamp.grid(row = rc, column = 3)
        labels[(rc, 3)] = line_timestamp
        
        rc += 1
    
    blank_line = Label(root, text = '', bg = 'white')
    blank_line.grid(row = rc)

def addMessage(event): 
    global msg_label
    
    grid_info = event.widget.grid_info()
    line = labels[(grid_info['row'],1)]
    
    msg_text = re.sub('<[^>]*>', '', sort[line][2])
    msg_text = re.sub('&[^;]*;', ' ', msg_text)
    msg_text = re.sub('\n+', '\n', msg_text)
    msg_text = re.sub(' +', ' ', msg_text)
    msg_text = re.sub('Show.*?Note:', '', msg_text)
    msg_text = re.sub('Key.*?Note:', '', msg_text)
    msg_text = re.sub(r' [ad].*relay.', '', msg_text)
    
    msg_label = Label(root, text = msg_text, anchor = 'w', justify = 'center', wraplength=480)
    msg_label.grid(row = grid_info['row'] + 1, columnspan = 4)
    msg_label.bind('<Button-1>', removeMessage)
    
def removeMessage(event):
    msg_label.grid_forget()   
        
def refresh(dict):
    rc = 1
    
    for k, v in dict.items():
        labels[(rc,2)].config(text = ' ' + v[0], bg = 'green' if v[0] == 'GOOD SERVICE' else 'yellow' if v[0] == 'PLANNED WORK' else 'red')
        labels[(rc,3)].config(text = ' ' + v[1])
        
        rc += 1
        
def exit():
    root.quit()

firstRun(getData())



refreshButton = Button(root, text = "Refresh", command =lambda: refresh(getData()), height = 1, width = 15).grid(row = 15, column = 0, columnspan = 3) 
exitButton = Button(root, text = "Exit", command = exit, height = 1, width = 15).grid(row = 15, column = 2, columnspan = 3)
blank_line = Label(root, text = '', bg = 'white')
blank_line.grid(row = 16)


mainloop()
