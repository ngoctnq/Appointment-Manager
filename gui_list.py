import Tkinter as tk
import ttk
import Database as DB
import Widgets as wd
import EditVisit as ev
import gui_student as gs

class GuiList:
    #################   CONSTRUCTOR   #################
    def __init__(self, top_lvl):
        '''
        Method to create a window that contains a list for serach result display
        Input:
            top_lvl: the top level window
        '''
        #create container
        self.root = tk.Toplevel(top_lvl)
        self.top_lvl = top_lvl
        self.root.title("Search results")

        ##set weight to the grid so that it can take up more space
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)

    def draw_table(self, db, data):
        '''
            Method to draw a table with data. The typer
            Input:
                - db: the database
                - data : contain the infomation of the data that we need
        '''
        list_columns = [a[0] for a in data.description]

        ###  TREEVIEW INITIALIZATION AND CONFIGURATIONS  ###
        #create a tree view
        self.tree = ttk.Treeview(self.root, selectmode='extended')

        #Scrollbars
        self.ysb = ttk.Scrollbar(self.root, orient='vertical', command=self.tree.yview)
        self.xsb = ttk.Scrollbar(self.root, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)

        #make the table appears in grid
        self.tree.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W,columnspan=8)
        self.ysb.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.xsb.grid(row=1, column=0, sticky=tk.E + tk.W)
        self.tree.selectmode = "browse"

        def onDoubleClick(event):
            item = self.tree.identify('item', event.x, event.y)
            col_no = self.tree.identify_column(event.x)
            if len(list_columns) == 8: # full tree
                values = self.tree.item(item, "values")
                if col_no in ['#2', '#3']:
                    name = values[1] + ' ' + values[2]
                    id_field = values[0]
                    self.root.destroy()
                    gs.StudentList(db, self.top_lvl, [id_field, name, db.getStudentComment(id_field)], db.findVisit_student(id_field))
                else:
                    id_field = values[0]
                    date_field = values[4]
                    time_field = values[5]
                    # print id_field, date_field, time_field
                    self.root.destroy()
                    ev.EditVisit(db, self.top_lvl, id_field, date_field, time_field)
            elif len(list_columns) == 5: # name_only
                values = self.tree.item(item, "values")
                id_field = values[0]
                name = values[1] + ' ' + values[2]
                self.root.destroy()
                gs.StudentList(db, self.top_lvl, [id_field, name, db.getStudentComment(id_field)], db.findVisit_student(id_field))

        self.tree.bind("<Double-1>", onDoubleClick)

        ###  DATA  ###

        #index the column
        self.tree["columns"] = list_columns

        ## column name ##
        #columb attributes
        for i in list_columns:
            self.tree.column(i, minwidth=20)
            self.tree.heading(i, text=i)

        ##Actual data
        data = data.fetchall()
        index = 1

        for row in data:
            self.tree.insert('', 'end', text=str(index), values=(row))
            index+=1

        self.root.grab_set()

        #make the window appears
        # self.root.mainloop()

if __name__ == "__main__":
    gui = GuiList()

    #connecting with the database
    db = DB.Database('database/cup.db')

    gui.draw_table(db, 'visits')
