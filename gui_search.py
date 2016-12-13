import Tkinter as tk
import Database as DB
import Widgets as wd
import gui_list as gl
import NewStudent as ns

class gui_search:
    'App for creating searching window'
    #################   CONSTRUCTOR   #################
    def __init__(self, db):
        '''
        Initialize a gui for the insertion of students infomation'
        INPUT: db - the databse
        '''
        #create a root container
        self.root = tk.Tk()
        self.root.title("CSC-271 Database Concept App")

        #Labels: to the left of the window
        search_label = wd.LabelWidget(self.root, 0, 0, "Search Past Records or Add New")
        search_label.grid(columnspan=4)
        search_label.config(width=30)

        #Entries: to the right of the window
        name_label = wd.LabelWidget(self.root, 0, 1, "Name")
        name_bar = wd.EntryWidget(self.root, 1, 1, "")
        name_bar.grid(columnspan=3)
        name_bar.config(width=20)

        #Topic
        topic_label = wd.LabelWidget(self.root, 0, 2, "Topic")
        topic_bar = wd.EntryWidget(self.root, 1, 2, "")
        topic_bar.grid(columnspan=3)
        topic_bar.config(width=20)

        #Date
        date_label = wd.LabelWidget(self.root, 0, 3, "Date (YMD)")
        mm_bar = wd.EntryWidget(self.root, 2, 3, "")
        dd_bar = wd.EntryWidget(self.root, 3, 3, "")
        yy_bar = wd.EntryWidget(self.root, 1, 3, "")
        # dd_bar.grid(columnspan=1)
        # mm_bar.grid(columnspan=1)
        # yy_bard.grid(columnspan=1)
        mm_bar.config(width=4)
        dd_bar.config(width=4)
        yy_bar.config(width=7)

        show_var = tk.StringVar()
        show_checkbox = tk.Checkbutton(self.root, variable=show_var, \
            onvalue="yes", offvalue = "no", text="No show")
        show_checkbox.deselect() #set the check button to offvalue
        show_checkbox.grid(column = 2, row=4)
        show_checkbox.grid(columnspan=2)
        # no_show_label = wd.LabelWidget(self.root, 0, 4, "No show")
        # no_show_label.grid(columnspan=3)
        show_checkbox.config(state = tk.DISABLED)


        showpref_var = tk.StringVar()
        def prefchange():
            if showpref_var.get() == 'yes':
                show_checkbox.config(state = tk.ACTIVE)
            else:
                show_checkbox.config(state = tk.DISABLED)

        #check button for the show preference
        showpref_checkbox = tk.Checkbutton(self.root, variable=showpref_var, \
            onvalue="yes", offvalue = "no", text="Show preference", command=prefchange)
        showpref_checkbox.deselect() #set the check button to offvalue
        showpref_checkbox.grid(column = 0, row=4)
        showpref_checkbox.grid(columnspan=2)

        #Log display to the gui
        log = wd.LabelWidget(self.root, 0, 6, "Status")
        log.config(width = 30)
        #having the log display to span 2 columns
        log.grid(columnspan = 4)

        ## todo: reimplement
        def search_fn():
            'method to call for the search button'
            name_text = name_bar.getVal()
            topic_text = topic_bar.getVal()
            dd_text = dd_bar.getVal()
            mm_text = mm_bar.getVal()
            yy_text = yy_bar.getVal()
            if showpref_var.get() == 'yes':
                noshow_val = show_var.get()
            else:
                noshow_val = 'maybe'
            try:
                if (yy_text == '' and (mm_text + dd_text) != '') or \
                    (mm_text == '' and dd_text != ''):
                    raise ValueError('not a valid date!')
                #interaction with the Database object
                gl.GuiList(self.root).draw_table(db, \
                    db.search_general(name_text, topic_text, dd_text,\
                    mm_text, yy_text, noshow_val))
                #report that the insertion is success
                log.set("Success")
            except Exception as err:
                #If insertion fail, report to the Log display
                print 'ERROR!', err
                # raise err
                log.set(str(err))

        def add_fn():
            'method to call for the add button'
            ns.NewStudent(self.root, db)

        #A Submit button
        search_button = tk.Button(self.root, text="Search", command = search_fn)
        search_button.grid(column = 0, row=5, columnspan=2)

        add_button = tk.Button(self.root, text="Add Student", command = add_fn)
        add_button.grid(column = 2, row=5, columnspan=2)

        self.root.grab_set()

        #make the window appears
        self.root.mainloop()



if __name__ == "__main__":
    #connecting with the database
    db = DB.Database('database/cup.db')
    new = gui_search(db)
