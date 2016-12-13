#!/usr/bin/env python

import Tkinter as tk
import Database as DB
import Widgets as wd
import tkMessageBox

class EditVisit:
    'App for Editing a student visit in the database'
    #################   CONSTRUCTOR   #################
    def __init__(self, db, top_lvl, idInput = "", visit_dateInput = "", visit_startInput = ""):
        '''
        Initialize a gui for the insertion of students infomation'
        INPUT:
            - db: the databse
            - top_lvl: the top level window
            - idInput: the student ID
            - visit_dateInput: the date of the visit
            - visit_startInput: the start time of the visit
        '''
        #create a root container
        self.root = tk.Toplevel(top_lvl)
        self.root.title("Edit Visit")

        #Fletching data from the given infomation
        try:
            keys = [idInput, visit_dateInput, visit_startInput]
            data = db.findVisit(keys)[0]
            stuName = ' '.join(db.findStudent(idInput)[0][1:3])
        except IndexError:
            data = ["N/A" for i in range(1, 10)]
            stuName = "N/A"


        #upper parts : display crucial infomation

        #Identity display, uneditable
        ID = wd.LabelWidget(self.root, 0, 0, data[0])
        ID.config(width = 45)
        name = wd.LabelWidget(self.root, 1, 0, stuName)
        name.config(width = 45)

        #Labels: to the left of the window
        dateL = wd.LabelWidget(self.root, 0, 1, "Visit Date")
        startL = wd.LabelWidget(self.root, 0, 2, "Visit Start")
        showL = wd.LabelWidget(self.root, 0, 3, "Show")
        topicL = wd.LabelWidget(self.root, 0, 4, "Topic")

        #Entries: to the right of the window
        dateE = wd.EntryWidget(self.root, 1, 1, data[1])
        startE = wd.EntryWidget(self.root, 1, 2, data[2])

        #check button for the show
        showVar = tk.StringVar()
        showE = tk.Checkbutton(self.root, variable=showVar, onvalue="yes", offvalue = "no")
        if data[3] == "yes":
            showE.select()
        else:
            showE.deselect() #set the check button to offvalue
        showE.grid(column = 1, row=3)

        topicE = wd.EntryWidget(self.root, 1, 4, data[4])
        topicE.config(width = 50)


        #time stamp for the new notes Student Comments
        timeStamp = db.getTimeStamp()

        #lower part, display long text
        #Visit NOTE
        noteL = wd.LabelWidget(self.root, 0, 5, "Visit Note")
        noteL.grid(columnspan=2)
        noteE = wd.TextWidget(self.root, 0, 6, 150, 5, data[5])
        noteE.grid(columnspan = 2)
        noteE.append(timeStamp + " -- ")
        oldNote = noteE.getVal() #store the old note for comparision later

        #Student Comments
        newComments = wd.LabelWidget(self.root, 0, 7, "Student comments")
        newComments.config(width = 50)
        newComments.grid(columnspan = 2)
        comments = wd.TextWidget(self.root, 0, 8, 150, 5, data[6])
        comments.grid(columnspan = 2)
        comments.append(timeStamp + " -- ")
        oldComments = comments.getVal() #store the comment note for comparision later

        #observations
        newObservations = wd.LabelWidget(self.root, 0, 9, "Observations")
        newObservations.config(width = 50)
        newObservations.grid(columnspan = 2)
        observations = wd.TextWidget(self.root, 0, 10, 150, 5, data[7])
        observations.grid(columnspan = 2)
        observations.append(timeStamp + " -- ")
        oldObservations = observations.getVal() #store the old note for comparision later

        #recommendations
        newRecommendations = wd.LabelWidget(self.root, 0, 11, "Recommendations")
        newRecommendations.config(width = 50)
        newRecommendations.grid(columnspan = 2)
        recommendations = wd.TextWidget(self.root, 0, 12, 150, 5, data[8])
        recommendations.grid(columnspan = 2)
        recommendations.append(timeStamp + " -- ")
        oldRecommendations = observations.getVal() #store the old note for comparision later

        #Log display to the gui
        log = wd.LabelWidget(self.root, 0, 14, "Status", 30)
        log.config(width = 100)
        #having the log display to span 2 columns
        log.grid(columnspan = 2)


        def update():
            'Method to call for the Update button'
            try:
                #interaction witht the Database object

                #checking if there is any changes had been made?
                dt = dateE.getVal()
                sta = startE.getVal()

                nt = False if oldNote == noteE.getVal() else noteE.getVal()
                comm = False if oldComments == comments.getVal() else comments.getVal()
                obs = False if oldObservations == observations.getVal() else observations.getVal()
                rec = False if oldRecommendations == observations.getVal() else recommendations.getVal()

                db.updateVisit(keys, dt, sta, showVar.get(), topicE.getVal(), nt, comm, obs, rec)

                log.set("Update Success")
            except Exception, value:
                #If insertion fail, report to the Log display
                log.set(value)

        def delete():
            'Method to delete a visit'
            try:
                if tkMessageBox.askyesno("Warning", "Delete This Visit"):
                    db.delVisit(keys[0], keys[1], keys[2])
                    log.set("Delete Success")
                    #wiping out displayed data
                    self.root.destroy()
                else:
                    log.set("Delete Canceled")
            except Exception, value:
                log.set(value)

        #A Delete button
        submit = tk.Button(self.root, text="Delete visit", command = delete)
        submit.grid(column = 0, row=13)

        #A Submit button
        submit = tk.Button(self.root, text="Update", command = update)
        submit.grid(column = 1, row=13)

        self.root.grab_set()

        #make the window appears
        # self.root.mainloop()



if __name__ == "__main__":
    #connecting with the database
    db = DB.Database('database/cup.db')
    new = EditVisit(db, "hawkeye20", "2015-04-22", "14:22")
