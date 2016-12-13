#!/usr/bin/env python
import sqlite3
import logging
import time, datetime #this is for creating a new time stamp
from copy import deepcopy #for the duplication of tuples

class Database(object):
    '''
    DATABASE library for the interaction with the database

    class database
    - used for setting up connection with the database
    - used for fletching, adding and updating data
    '''
    #################   CONSTRUCTOR   #################
    #the input is a database
    def __init__(self, db):
        '''
        CONSTRUCTOR
        input:
        - db: location of the .db file

        fields:
        - con : the connection to the database
        - cur : crusor object
        - relation : a list of relations of the database
        - meta : containing the metadata of each relation schema
        '''
        ### CONNECT TO DB ####
        self.con = sqlite3.connect(db)
        #crusor object allow people to execute commands
        self.cur = self.con.cursor()

        ### DATABASE ATTRIBUTE METADATA ####
        #Name of the relations
        self.relations = ['students', 'visits', 'comments']
        #Meta data of each relations
        self.meta = {'students': self.cur.execute('PRAGMA table_info("students")').fetchall(),\
                    'visits': self.cur.execute('PRAGMA table_info("visits")').fetchall(),\
                    'comments': self.cur.execute('PRAGMA table_info("comments")').fetchall(),}

    #################   DATABASE HANDLING   #################
    #method to close the connection with database
    def close(self):
        '''
        Method to safely close the connection with database.
        '''
        self.con.close()

    #fletch all data from table r
    def fetchData(self, r):
        '''
        Method to fetch data from relation r
        input
        - r: name of the relation (i.e. students, visits)
        output:
        - output tuples that contains data
        '''
        if r in self.relations: #checking if the input is a valid table
            return self.cur.execute('select * from {}'.format(r)).fetchall()
        else:
            #no relation is found. Return nothing
            pass


    ###############   GENERAL QUERY   ##############
    # search
    def search_general(self, name, topic, dd, mm, yy, no_show):
        '''
        Generic search function for a student
        inputs
        - name: name of the student
        - topic: topic of the visit
        - dd: date
        - nn: month
        - yy: year
        - no_show: 'yes' or 'no', indicating if the student show up or not
        '''

        name = '%'+name+'%'
        topic = '%'+topic+'%'

        #execute to update data
        try:
            if (topic + dd + mm + yy + no_show) == '%%maybe':
                return self.cur.execute("select * from students where (first || \" \" || last) like ?", [name])
            else:
                if topic == '%*%':
                    topic = '%%'
                query = 'select '\
                    +'students.ID, first, last, year, visit_date, visit_start, show, topic '\
                    +'from students, visits where students.ID = visits.ID and '\
                    +"(first || \" \" || last) like ? and "\
                    +'(topic like ?)'
                i_list = [name, topic]

                if no_show != 'maybe':
                    no_show = 'yes' if no_show == 'no' else 'no'
                    query += " and show = ?"
                    i_list.append(no_show)

                if yy == '':
                    return self.cur.execute(query, i_list)
                else:
                    query += " and strftime('%Y',visit_date) = ?"
                    i_list.append(yy)
                    if mm == '':
                        return self.cur.execute(query, i_list)
                    else:
                        query += " and strftime('%m',visit_date) = ?"
                        i_list.append(mm)
                        if dd == '':
                            return self.cur.execute(query, i_list)
                        else:
                            query += " and strftime('%d',visit_date) = ?"
                            i_list.append(dd)
                            return self.cur.execute(query, i_list)

            # test line
            # ret = self.cur.execute('select * from students')
        except sqlite3.IntegrityError, value:
            #print out the value
            logging.warning(value)
            '''
                There are two types of IntegrityError
                    UNIQUE : duplication of primary key
                    NOT NULL: when input a None into the input of a none null attribute
            '''
            #Unsuccessful update, rollback to earlier commit
            self.con.rollback()
            #raise exception for the GUI
            raise Exception(value)

    #################   STUDENTS   #################
    #Insertion
    def insStudent(self, ID, first, last, year, note):
        '''
        Insert a new student.
        inputs
        - ID, first, last, year
        '''

        #data holder
        data = [ID, first, last, year, note]

        #execute to update data
        try:
            #proccess data and insert new data into the database
            self.cur.execute('insert into students values(?,?,?,?,?)', data)
            #commit the new name to the database
            self.con.commit()
        except sqlite3.IntegrityError, value:
            #print out the value
            logging.warning(value)
            '''
                There are two types of IntegrityError
                    UNIQUE : duplication of primary key
                    NOT NULL: when input a None into the input of a none null attribute
            '''
            #Unsuccessful update, rollback to earlier commit
            self.con.rollback()
            #raise exception for the GUI
            raise Exception(value)

    #Find visit
    def findStudent(self, ID):
        '''
        Find a student using ID
        input:
        - ID: the unique ID that each student has
        output:
        - tuple that contain the infomation about the student
            ((ID, first, last, year, note))
        '''
        try:
            return self.cur.execute('select * from students where (ID = ?)', [ID]).fetchall()
        except sqlite3.IntegrityError, value:
            logging.warning(value)
            #raise exception for the GUI
            raise Exception(value)

    #Find All IDs
    def idList(self):
        '''
        Method to find all the IDs of the students in the database
        output:
        - tuple that contain all the IDs
            (id1, id2, id3, ...)
        '''
        try:
            return self.cur.execute('select ID from students').fetchall()[0]
        except sqlite3.IntegrityError, value:
            logging.warning(value)
            #raise exception for the GUI
            raise Exception(value)

    #Update
    def updateStudent(self, ID, note):
        '''
        Method to update student data
        inputs:
        - ID: unique ID of each student
        - note: the updated note for each student
        '''
        data = [note, ID]
        try:
            self.cur.execute('update students set note = ? where (ID = ?)', data)
            self.con.commit()
        except sqlite3.IntegrityError, value:
            logging.warning(value)
            self.con.rollback()
            #raise exception for the GUI
            raise Exception(value)

    #Deletion
    def delStudent(self, ID):
        '''
        Method to delete a student
        input: ID
        '''
        data = [ID]
        try:
            self.cur.execute('delete from students where ID = ?', data)
            self.con.commit()
        except sqlite3.IntegrityError, value:
            logging.warning(value)
            #Unsuccessful update, rollback to earlier commit
            self.con.rollback()
            #raise exception for the GUI
            raise Exception(value)

    #################   VISITS   #################

    #Insertion
    def insVisit(self, ID, visit_date, visit_start, show, topic, note, comments, observations, recommendations):
        '''
        Method to insert a new visit
        input:
        - ID
        - visit_date: YYYY-MM-DD
        - visit_start: HH:MM
        - show: yes/no
        - topic, note, comments, observations, recommendations: strings
        '''
        #data holder
        data = [ID, visit_date, visit_start, show, topic, note, comments, observations, recommendations]
        #execute to update data
        try:
            self.cur.execute('insert into visits values(?,?,?,?,?,?,?,?,?)', data)
            self.con.commit()
        except sqlite3.IntegrityError, value:
            logging.warning(value)
            self.con.rollback()
            #raise exception for the GUI
            raise Exception(value)

    #Find visit
    def findVisit(self, keys):
        '''
        Method to find a visit
        inputs
        - key is a tuple that contains ID, visit_date, visit_date
        output:
        - a tuple that contain infomation for visits:
          (ID, visit_date, visit_start, show, topic, note, comments, observations, recommendations)
        '''
        #data holder
        data = keys
        #execute to update data
        try:
            return self.cur.execute('select * from visits where (ID = ?) and (visit_date = ?) and (visit_start = ?)', data).fetchall()
        except sqlite3.IntegrityError, value:
            logging.warning(value)
            #raise exception for the GUI
            raise Exception(value)

    def findVisit_student(self, id_no):
        '''
        Method to find all the visit from a student
        input:
        - input the student's ID
        output:
        - output a tuple that contain all the visit_date and visit_start of the student with the given ID
        '''
        #execute to update data
        try:
            return self.cur.execute('select visit_date, visit_start, topic from visits where (ID = ?)', [id_no])
        except sqlite3.IntegrityError, value:
            logging.warning(value)
            #raise exception for the GUI
            raise Exception(value)

    #update visit
    def updateVisit(self, keys, visit_date, visit_start, show, topic, note, comments, observations, recommendations):
        '''
        Method to update the visit tuple
        input:
        - key: it contains the original keys (ID, visit_date, visit_start)
        - visit_date, visit_start: two values might be different from the original.
        - show, topic, note, comments, observations, recommendations: string
        '''
        #data holder

        data = [show, topic, note, comments, observations, recommendations]
        dataCol = ["show", "topic", "note", "comments", "observations", "recommendations"]

        def updateTuple(attribute, data):
            query = 'update visits set {att} = "{d}" where (ID = "{ide}") and (visit_date = "{v_d}") and (visit_start ="{v_s}")'.format(att = attribute, d = data, ide = keys[0], v_d = keys[1], v_s = keys[2])
            #print query
            self.cur.execute(query)
        #execute to update data
        try:
            #Consider "visit_date" and "visit_start" because they are in primary key
            updateTuple("visit_date", visit_date)
            keys[1]= visit_date

            updateTuple("visit_start", visit_start)
            keys[2]= visit_start

            #Modify data
            for i in range(len(data)):
                if data[i]:
                    updateTuple(dataCol[i], data[i])

            #commit to the database
            self.con.commit()
        except sqlite3.IntegrityError, value:
            logging.warning(value)
            #raise exception for the GUI
            raise Exception(value)
            self.con.rollback()
    #Deletion
    def delVisit(self, ID, visit_date, visit_start):
        '''
        Method to delete a visit tuple
        inputs:
        - id: student's ID
        - visit_date: YYYY-MM-DD
        - visit_start: HH:MM
        '''
        data = [ID, visit_date, visit_start]
        try:
            self.cur.execute('delete from visits where (ID = ?) and (visit_date = ?) and (visit_start = ?)', data)
            self.con.commit()
        except sqlite3.IntegrityError, value:
            logging.warning(value)
            self.con.rollback()
            #raise exception for the GUI
            raise Exception(value)

    #Time Stamp
    def getTimeStamp(self):
        '''
            Method to generate a timeStamp
            output: YYYY-MM-DD:HH:MM:SS
        '''
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def getStudentComment(self, id_no):
        '''
            Method to get the student comments
            output: String
        '''
        student = self.findStudent(id_no)[0]
        # print student
        return student[4]

#Only execute the main menthod if the file is run directly
if __name__ == '__main__':
    db = Database('database/cup.db')
    # db.insStudent('nntran17', 'Ngoc', 'Tran', 2017, '')
    # db.delStudent('tanguyen17')
    # db.insVisit('tanguyen17', '2016-11-13', '09:00', 1, 'Time Management', 'Nothing special')
    # db.delVisit('tanguyen17', '2016-11-13', '09:00')
    # db.insComment('tanguyen17', '2016-11-13', '09:00', '2016-11-13', '10:00', 'Good', 'ok', 'Nothing special')
    # db.delComment('tanguyen17', '2016-11-13', '09:00', '2016-11-13', '10:00')
    # print db.findVisit("tanguyen17", "2016-9-20", "10:29")

    # print db.getTimeStamp()
    # for i in db.cur:
    #     print i

    query = 'select '\
        +'students.ID, first, last, year, visit_date, show, topic '\
        +'from students, visits where students.ID = visits.ID' #\
        # +"where ((first || \" \" || last) like ?) and"\
        # +'(topic like ?)', [name, topic])

    print query

    db.cur.execute(query)
    ############################################################
    db.close()
