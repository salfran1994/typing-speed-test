from tkinter import *
import time 
import threading
import random

class App(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.start()        
        
    # This function will manage the time and call the function that show the result
    def timer(self):
        for _ in range(60):
            self.my_time -= 1
            self.time_left.config(text=self.my_time)
            time.sleep(1)
        self.show_result()
    
    def getText(self):
        with open("data.txt", "r") as file:
            text = random.choice(file.readlines())
        return text

    def check_paragraph(self, event):
        if self.my_time != 0:
            if self.my_time == 60:
                self.countdown_thread.start()

            for i in range(len(self.contents.get())):
                index = f"1.{i}"
                if self.contents.get()[i] == self.original_paragraph[i]:
                    self.reading_text.tag_remove("bad", index)                
                    self.reading_text.tag_add("good", index) 
                    self.reading_text.tag_config("good", background="yellow", foreground="green")
                else:
                    self.reading_text.tag_remove("good", index)    
                    self.reading_text.tag_add("bad", index) 
                    self.reading_text.tag_config("bad", background="red", foreground="black")
    
    def start(self):
        # Define the variable to manage the time "60 seconds"
        self.my_time = 60
        self.time_left = Label(width=30, font = ('calibre',20,'normal'), text=f"{self.my_time}")
        self.time_left.grid(column=2, row=1, pady=(10,0))

        text_to_read = self.getText()
        self.reading_text = Text(height=20)
        self.reading_text.grid(column=2, row=2, padx=10, pady=10)
        self.reading_text.insert(INSERT, text_to_read)
        self.original_paragraph = self.reading_text.get("1.0", END)

        self.writting_text = Entry(width=30, font = ('calibre',20,'normal'))
        self.writting_text.grid(column=2, row=3, pady=(0,10))
        self.contents = StringVar()
        self.writting_text["textvariable"] = self.contents

        # This line will allow the function timer run as a parallel process
        self.countdown_thread = threading.Thread(target=self.timer)

        # Define a callback for when the user type
        self.writting_text.bind('<KeyRelease>',
                            self.check_paragraph)

    
    def show_result(self):
        wps = self.WPS()
        self.time_left.destroy()
        self.reading_text.destroy()
        self.writting_text.destroy()
        self.message = Label(width=30, font = ('calibre',20,'normal'), text=f"You write {wps} WPS!!!")
        self.message.grid(column=1, row=2, columnspan=3)
        self.button = Button(text="Try again", command=self.start)
        self.button.grid(column=2, row=3)

    def WPS(self):
        written_words = self.contents.get().split(" ")  
        read_wrold = self.original_paragraph.split(" ")
        number_of_words = 0
        for i in range(len(written_words)):
            if written_words[i] == read_wrold[i]:
                number_of_words += 1
        return number_of_words

root = Tk()
myapp = App(root)
myapp.master.title("Type Speed test")
myapp.master.maxsize(800,800)
myapp.mainloop()