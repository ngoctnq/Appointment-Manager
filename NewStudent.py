import Tkinter as tk
import Database as DB
import Widgets as wd
import gui_student as gs

class NewStudent:
    'App for creating a new student in the database'
    #################   CONSTRUCTOR   #################
    def __init__(self, top_lvl, db):
        '''
        Initialize a gui for the insertion of students infomation'
        INPUT:
            - top_lvl the top_lvl window
            -db - the databse
        '''
        #create a root container
        self.root = tk.Toplevel(top_lvl)
        self.root.title("New Student")
        self.top_lvl = top_lvl
        #Labels: to the left of the window
        idL = wd.LabelWidget(self.root, 0, 0, "ID")
        firstL = wd.LabelWidget(self.root, 0, 1, "First")
        lastL = wd.LabelWidget(self.root, 0, 2, "Last")
        yearL = wd.LabelWidget(self.root, 0, 3, "Year")

        #Entries: to the right of the window
        idE = wd.EntryWidget(self.root, 1, 0, "")
        firstE = wd.EntryWidget(self.root, 1, 1, "")
        lastE = wd.EntryWidget(self.root, 1, 2, "")
        yearE = wd.EntryWidget(self.root, 1, 3, "")

        yearL = wd.LabelWidget(self.root, 0, 4, "note")
        yearL.grid(columnspan=2)
        noteE = wd.TextWidget(self.root, 0, 5, 50, 10, "")
        noteE.grid(columnspan = 2)
        timeStamp = db.getTimeStamp()
        noteE.append(timeStamp + " -- ")
        oldNote = noteE.getVal() #store the old note for comparision later

        #Log display to the gui
        log = wd.LabelWidget(self.root, 0, 7, "Status", 30)
        #having the log display to span 2 columns
        log.grid(columnspan = 2)

        def ins():
            'method to call for the Submit button'
            try:
                #checking if the user had inserted any special note for each students
                note = "" if oldNote == noteE.getVal() else noteE.getVal()
                #interaction witht the Database object
                db.insStudent(idE.getVal(), firstE.getVal(), lastE.getVal(), int(yearE.getVal()), note)

                #report that the insertion is success
                log.set("Success")
                name = firstE.getVal() + ' ' + lastE.getVal()
                id_field = idE.getVal()
                self.root.destroy()
                gs.StudentList(db, self.top_lvl, [id_field, name, db.getStudentComment(id_field)], db.findVisit_student(id_field))
            except Exception, value:
                #If insertion fail, report to the Log display
                log.set(value)

        #A Submit button
        submit = tk.Button(self.root, text="Submit", command = ins)
        submit.grid(column = 0, row=6, columnspan = 2)

        self.root.grab_set()

        #make the window appears
        # self.root.mainloop()



if __name__ == "__main__":
    #connecting with the database
    db = DB.Database('database/cup.db')
    new = NewStudent(db)
