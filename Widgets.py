import Tkinter as tk
import ttk

'Simple widget implementation for the input and display of infomation'

#selectable grid for the label
class LabelWidget(tk.Entry):
    'Widgets for the Label. Text is not editable'
    '''NOTE: the tk.Entry only have 1 line'''
    def __init__(self, master, x, y, text, w = 8):
        'Inputs: master, x and y grid position, text to display, width'
        #The text extry is a StringVar object
        self.text = tk.StringVar()
        #set the text to display
        self.text.set(text)
        #contrusct the Entry object
        tk.Entry.__init__(self, master=master)
        self.config(textvariable=self.text, width=w,
                    relief="ridge",
                    fg="#000000fff",
                    justify='center',
                    state="readonly") #state = read only
        #set the grid position of the entry
        self.grid(column=x, row=y)

        #enable select_all
        self.bind("<Command-Key-a>", self.select_all)
        self.bind("<Command-Key-A>", self.select_all) # just in case caps lock is on

    def select_all(self, event):
        'Method to select all the text inside the Entry object'
        self.select_range(0, tk.END)
        self.icursor(tk.END) #bring the crusor to the end
        self.xview(tk.END) #bring the view to the end

    def set(self, ms):
        'Method to set the text to display. Input ms as the message.'
        self.text.set(ms)


#entry grid for something
class EntryWidget(tk.Entry):
    'One-line text entry widgets'
    def __init__(self, master, x, y, text=""):
        tk.Entry.__init__(self, master=master)
        self.value = tk.StringVar()
        self.value.set(text)
        self.config(textvariable=self.value, width=15,
                    relief="ridge",
                    bg="#ddddddddd", fg="#000000000",
                    justify='center')
        self.grid(column=x, row=y)

        #enable select_all
        self.bind("<Command-Key-a>", self.select_all)
        self.bind("<Command-Key-A>", self.select_all) # just in case caps lock is on

    def getVal(self):
        'Method to get the value of the entry'
        return self.value.get()

    def select_all(self, event):
        self.select_range(0, tk.END)
        self.icursor(tk.END) #bring the crusor to the end
        self.xview(tk.END) #bring the view to the end

class TextWidget(tk.Text):
    'Multi-line text entry'
    def __init__(self, master, x, y, w, h,text = "", sbx_pos = 2):
        'x and y are the grid position. w and h are the width and height of the text box'
        tk.Text.__init__(self, master=master, width = w, height = h)
        #insert the default value. 1.0 is the first position
        self.insert(1.0, text)
        self.grid(column = x, row = y)

        #scroll bars that are next to and under the text box
        sb = tk.Scrollbar(master=master, command=self.yview)
        self.configure(yscrollcommand=sb.set)#fix Scrollbar
        sb.grid(column = x+sbx_pos, row = y, sticky='nswe')

        #enable select_all
        self.bind("<Command-Key-a>", self.select_all)
        self.bind("<Command-Key-A>", self.select_all) # just in case caps lock is on

    def getVal(self):
        'Get the value of the text'
        return self.get(1.0, tk.END) #1.0 first line, first character

    def append(self, text):
        self.insert(tk.END, text)

    def select_all(self, event):
        #select all the text
        self.tag_add(tk.SEL, "1.0", tk.END) #tag SEL as the staring 1.0 and the END
        #move the crusor to the begining
        self.mark_set(tk.INSERT, tk.END)
        self.see(tk.INSERT)

if __name__ == '__main__':
    frame = tk.Tk()
    frame.grid()
    a = LabelWidget(frame, 0, 0, "test")
    a = EntryWidget(frame, 0, 1, "default value")

    text = TextWidget(frame, 1, 1, 10, 10, "testing")
    print text.getVal()

    def prt():
        print text.getVal()

    b = tk.Button(frame, text="print", command = prt)

    b.grid(column = 1, row=2)
    frame.mainloop()
