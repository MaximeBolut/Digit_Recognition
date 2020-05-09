
from keras.models import load_model
import tkinter as tk
from tkinter import *
import os
import cv2
import win32gui
from PIL import ImageGrab, Image
import numpy as np

import matplotlib.pyplot as plt

model = load_model('mnist.h5')


def preprocessing_image():
    """function to preprocess the image to"""
    image = cv2.imread('test.jpg')
    #print(type(image))
    grey = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    #ret is the threshold value, here 75. 
    ret, thresh = cv2.threshold(grey.copy(), 75, 255, cv2.THRESH_BINARY_INV)
   
    #cv2.imshow('binarized image', thresh)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #print(type(contours[0]))
    #print(len(contours[0]))
    cv2.drawContours(image, contours, -1, (0, 0, 255), 3) 
    #cv2.imshow('Contours', image) 
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)        
        # Creating a rectangle around the digit in the original image (for displaying the digits fetched via contours)
        cv2.rectangle(image, (x,y), (x+w, y+h), color=(0, 255, 0), thickness=2)
        # Cropping out the digit from the image corresponding to the current contours in the for loop
        digit = thresh[y:y+h, x:x+w]        
        # Resizing that digit to (18, 18)
        resized_digit = cv2.resize(digit, (18,18))        
        # Padding the digit with 5 pixels of black color (zeros) in each side to finally produce the image of (28, 28)
        padded_digit = np.pad(resized_digit, ((5,5),(5,5)), "constant", constant_values=0)        
        # Adding the preprocessed digit to the list of preprocessed digits
        preprocessed_digit = (padded_digit)
    return preprocessed_digit




def predict_digit(img):
    #resize image to 28x28 pixels
    img.save('test.jpg')

    preprocessed_image = preprocessing_image()
    # print(type(preprocessed_image))
    # print(preprocessed_image.shape)
    img = preprocessed_image.reshape(1, 28, 28, 1)
    img = img/255.0


    img = img.reshape(1,28,28,1)

    #predicting the class
    res = model.predict([img])[0]
    return np.argmax(res), max(res)

'''
root=Tk()
root.title("Image 2 Text (by Maxime B)")
#root.iconbitmap('logo.ico')
root.geometry("480x1080")
root.config(background='#2E4053')


masterframe=Frame(root,background='#2E4053', bd=2) 
#masterframe.grid(row=0, columnspan=3)



root.mainloop()
'''

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.title("Digit recognition")
        #self.iconbitmap('logo.ico')
        self.config(background='#2E4053')

        # Creating elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg = "white", cursor="cross")
        self.canvas2 = tk.Canvas(self, width=300, height=300, bg = "white", cursor="cross")

        self.label = tk.Label(self, text="Thinking..", font=("Helvetica", 48))

        self.classify_btn = tk.Button(self, text = "Recognise", command = self.classify_handwriting) 

        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)


        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.canvas2.grid(row=0, column=1, pady=2, sticky=W, )
        self.label.grid(row=1, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=2, column=1, pady=2, padx=2)
        self.button_clear.grid(row=2, column=0, pady=2)
        #self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)
        self.canvas2.bind("<B1-Motion>", self.draw_lines2)

    def clear_all(self):
        self.canvas.delete("all")
        self.canvas2.delete("all")
        self.label['text'] = " ? + ? = ?"


    def classify_handwriting(self):
        
        #HWND = self.canvas.winfo_id() # get the handle of the canvas
        #rect = win32gui.GetWindowRect(HWND) # get the coordinate of the canvas
        rect=(30, 70, 700, 800) #(x, y, w, h) top left corner (0,0)
        im = ImageGrab.grab(rect)
        digit, acc = predict_digit(im)


        rect2=(30, 70, 1400, 800) #(x, y, w, h) top left corner (0,0)
        im2 = ImageGrab.grab(rect2)
        digit2, acc2= predict_digit(im2)     
        if (digit + digit2) != 0:
        	self.label.configure(text= str(digit)+ ' + ' + str(digit2) + ' = ' + str(digit+ digit2))
        else:
        	self.label.configure(text="la tete a toto")



    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=10
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')

    def draw_lines2(self, event):
        self.x = event.x
        self.y = event.y
        r=10
        self.canvas2.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')
       



def getter(widget):
    x=root.winfo_rootx()+widget.winfo_x()
    y=root.winfo_rooty()+widget.winfo_y()
    x1=x+widget.winfo_width()
    y1=y+widget.winfo_height()
    ImageGrab.grab().crop((x,y,x1,y1))

app = App()
mainloop()