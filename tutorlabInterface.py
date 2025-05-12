import psycopg2
from tabulate import tabulate
#all the functions are defined first and then the code for decisions is at the bottom
'''
I used videos from microsoft copilot to learn how to use psycopg2. My code is completely different from what they do. Only syntax is similar, my programming is different.
https://www.youtube.com/watch?v=2PDkXviEMD0
'''
# Create a dictionary to hold your credentials for connecting to the PostgreSQL database
# Replace with your actual database credentials
credentials = {
    "dbname": "Tutorlab",
    "user": "postgres", # Default user name is postgres
    "password": "p558h@LG0h",
    "host": "localhost",  # Change if using a remote server
    "port": "5432"  # Default PostgreSQL port
}

# Define a function to establish connection to the PostgreSQL database 
def connect_db():
    # Managing exception in case of failed connection
    try:
        connection = psycopg2.connect(**credentials) # Unpacking the credentials dictionary
        print("Connected to the database successfully!")
        return connection
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

def get_valid_integer(prompt, min_value, max_value):#user input validation so that they don't end up inputting text or number causing the program to crash
    while True:#I got this code from microsoft copilot. I asked it to fix my code.
        try:#the ai fixed the limit for what number can be inputted using the user input greater and or equal to min value and less than or equal to max value
            user_input = int(input(prompt))#it also added the try except statements to catch text input. That is all it added
            if min_value <= user_input <= max_value:
                return user_input
            else:
                print(f"Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def newStudent():#add a new student to the database
    while True:
        confirmAccident=input("If you accidentally selected then press y else press any key: ")
        if confirmAccident=="y":
            break
        con=connect_db()
        cur=con.cursor()
        studentEmailID=input("Write your student email id and then press enter: ")
        fullName=input("Write your full name and then press enter: ")
        isAthlete=input("Are you an athlete? If yes then type the letter y and then press enter, else enter anything and then press enter: ")
        '''the studentEmailID, fullName, and isAthlete is asked because that is the information that is stored for students that go to tutoring
        then the input for isAthlete is put through a if statement to determine if what was inputted said the sutdent was an athlete or not
        '''
        if isAthlete=="y":
            isAthlete=True
        else:
            isAthlete=False
        cur.execute("""INSERT INTO student (student_email_id,full_name,athlete) VALUES (%s,%s,%s);""",(studentEmailID,fullName,isAthlete))
        con.commit()#once the information for isAthlete is confirmed it is overwritten with a boolean value and then executed
        cur.close()
        con.close()
        print("You have been successfully added to the database!")#this code successfully works! emily madison was successfully added as a test
        continu=str(input("Press any key to continue.: "))
        break

def newTutor():#add a new tutor to the database
    while True:
        confirmAccident=input("If you accidentally selected press y else press any key: ")
        if confirmAccident=="y":
            break
        con=connect_db()
        cur=con.cursor()#the email, full name, and phone number is asked for as that is what is stored
        tutorEmailID=input("Write your student email id and then press enter: ")
        fullName=input("Write your full name and then press enter: ")
        phoneNumTemp=str(input("Type your phone number and then press enter: "))
        phoneNum=""
        unwantedInPhonNum=["-","(",")"," "]
        for char in phoneNumTemp:#the dashes in phone numbers is removed because people might type their phone number in with dashes
            if char not in unwantedInPhonNum:
                phoneNum+=char
        cur.execute("""INSERT INTO tutor (tutor_email_id,full_name,phone_number) VALUES (%s,%s,%s);""",(tutorEmailID,fullName,phoneNum))
        con.commit()# once the phone number has been properly processed the email id, name, and phone number is inserted into the table
        cur.close()
        con.close()
        print("You have been successfully added to the database!")#This code works successfully! Henry Emily was addedd succesfully as a test
        continu=str(input("Press any key to continue.: "))
        break

def tutorAttend():#function for tutors to add information that they were present for the session
    while True:
        confirmAccident=input("If you accidentally selected then press y else press any key: ")
        if confirmAccident=="y":
            break
        print("Do you want to see records of tutor attendance, clock in as a tutor, or clock out as a tutor?")
        print("If you want to see records press 0 and then press enter, if you want to clock in press 1 and then press enter, if you want to clock out then press 2.")
        userChoice=get_valid_integer("Enter the number for what you choose: ", 0, 2)
        if userChoice ==0:#test this make sure not to erase other previous record departure times because of same email id
            confirmAccident=input("If you accidentally selected then press y else press any key: ")
            if confirmAccident=="y":
                break
            con=connect_db()
            cur=con.cursor()
            cur.execute("SELECT * FROM tutor_attendance;")
            rows=cur.fetchall()
            head=["Date","Time Of Arrival","Time Of Departure","Tutor Email ID"]
            print(tabulate(rows,headers=head,tablefmt="fancy_grid"))
            con.commit()
            cur.close()
            con.close()
            continu=str(input("Press any key to continue.: "))
        elif userChoice==1:
            confirmAccident=input("If you accidentally selected then press y else press any key: ")
            if confirmAccident=="y":
                break
            con=connect_db()
            cur=con.cursor()
            userID=str(input("What is your email id?: "))# once i get the user id i put it in a tuple format and have it inserted in the query as tuple
            cur.execute("INSERT INTO tutor_attendance (date,arrival,tutor_email_id) VALUES (CURRENT_DATE, CURRENT_TIME,%s);", (userID,))#i used ms copilot to learn how to get the current date and current time and know how to use tuple for user input
            con.commit()#i had to get help from ai to understand how to use tuples when inserting, thats why the userid has a comma withou it it, without the comma it won't work.
            cur.close()
            con.close()
            continu=str(input("Press any key to continue.: "))
        elif userChoice==2:
            confirmAccident=input("If you accidentally selected then press y else press any key: ")
            if confirmAccident=="y":
                break
            con=connect_db()
            cur=con.cursor()
            userID=str(input("What is your email id?: "))
            cur.execute("UPDATE tutor_attendance SET departure = CURRENT_TIME WHERE tutor_email_id = %s AND date=CURRENT_DATE;", (userID,))#i used ms copilot to learn how to get the current date and current time and know how to use tuple for user input
            con.commit()
            cur.close()
            con.close()#all of it works succesfully, I added very new record date April 21 2025
            continu=str(input("Press any key to continue.: "))
        break

def sessionAttend():#function for the student to say which tutor helped them
    while True:
        confirmAccident=input("If you accidentally selected then press y else press any key: ")
        if confirmAccident=="y":
            break
        userChoice=get_valid_integer("1. If you want to sign in to math tutoring.\n2. If you want to sign out of math tutoring.\n",1,2)
        if userChoice==1:
            confirmAccident=input("If you accidentally selected then press y else press any key: ")
            if confirmAccident=="y":
                break
            con=connect_db()
            cur=con.cursor()
            studentEmailID=str(input("What is your email ID?: "))
            classID=str(input("What is the ID of the class you are coming here for help for?: "))
            cur.execute("SELECT * FROM classes WHERE class_id=%s",(classID,))
            rows=cur.fetchall()
            if rows == []:
                classes(classID)
            cur.execute("SELECT * FROM enrollment WHERE class_id=%s AND student_email_id=%s",(classID,studentEmailID))
            rows=cur.fetchall()
            if rows == []:
                enroll(classID,studentEmailID)
            tutorEmailID=str(input("What is the email ID of the tutor who is helping you?: "))
            cur.execute("INSERT INTO session_attendance (date,student_email_id,arrival,class_id,tutor_email_id) VALUES (CURRENT_DATE,%s,CURRENT_TIME,%s,%s)",(studentEmailID,classID,tutorEmailID))#i used ms copilot to leanr how to get the current date and current time
            con.commit()
            cur.close()
            con.close()
            continu=str(input("Press any key to continue.: "))
        elif userChoice==2:
            confirmAccident=input("If you accidentally selected then press y else press any key: ")
            if confirmAccident=="y":
                break
            con=connect_db()
            cur=con.cursor()
            studentEmailID=str(input("What is your email ID?: "))
            cur.execute("UPDATE session_attendance SET departure = CURRENT_TIME WHERE student_email_id = %s AND departure IS NULL;", (studentEmailID,))#i used ms copilot to learn how to get the current date and current time and know how to use tuple for user input
            con.commit()
            cur.close()
            con.close()
            continu=str(input("Press any key to continue.: "))
        break


def enroll(a,b):#function for student to add which class they are enrolled in
    con=connect_db()
    cur=con.cursor()
    classID=a
    sectionNum=int(input("What is the section number?: "))
    semester=str(input("Which semester are you taking this class?: "))
    emailID=b
    professorName=str(input("What is the full name of the professor?: "))

    cur.execute("INSERT INTO enrollment (class_id,section,semester,student_email_id,professor) VALUES (%s,%s,%s,%s,%s)",(classID,sectionNum,semester,emailID,professorName))
    con.commit()
    cur.close()
    con.close()#works successfully! I added em815 with azarion

def classes(a):#function for student to add which class specifically they are in, after all each class has sections and differ by years
    con=connect_db()
    cur=con.cursor()
    classID=a
    className=str(input("What is the name of the class?: "))
    cur.execute("INSERT INTO classes (class_id,class_name) VALUES (%s,%s);",(classID,className))
    con.commit()
    cur.close()
    con.close()#works successfully, I added abstract algebra as an example
      

def admin():
    while True:
        confirmAccident=input("If you accidentally selected then press y else press any key: ")
        if confirmAccident=="y":
            break
        userInput=get_valid_integer("1. How many students go to tutoring for a specific day on each day that they do go to tutoring for a class.\n2. How many students go to tutoring for each of the classes a professor teaches.\n3. See all students.\n4. See all tutors.\n5. Alter a student record or tutor record.\n6. To see the full information of every class students have gone to tutoring for help for and which students went for help for which class.\n",1,6)
        if userInput==1:
            confirmAccident=input("If you accidentally selected then press y else press any key: ")
            if confirmAccident=="y":
                break
            con=connect_db()
            cur=con.cursor()
            idOfClass=str(input("What is the class id?: "))
            #SELECT date, COUNT(DISTINCT student_email_id) FROM session_attendance WHERE class_id = 'MATH-221' GROUP BY date;
            stringToExec="SELECT date, COUNT(DISTINCT student_email_id) FROM session_attendance WHERE class_id ILIKE '"+idOfClass+ "' GROUP BY date;"
            cur.execute(stringToExec)
            rows=cur.fetchall()
            head=["Date","Number Of Students"]
            print(tabulate(rows,headers=head,tablefmt="fancy_grid"))
            con.commit()
            cur.close()
            con.close()
            continu=str(input("Press any key to continue.: "))
        elif userInput==6:
            confirmAccident=input("If you accidentally selected then press y else press any key: ")
            if confirmAccident=="y":
                break
            con=connect_db()
            cur=con.cursor()
            cur.execute("SELECT * FROM enrollment JOIN classes ON classes.class_id = enrollment.class_id;")
            rows=cur.fetchall()
            head=["Class ID","Section","Semester","Student Email ID","Professor","Class ID","Class Name"]
            print(tabulate(rows,headers=head,tablefmt="fancy_grid"))
            con.commit()
            cur.close()
            con.close()
        elif userInput==2:
            confirmAccident=input("If you accidentally selected then press y else press any key: ")
            if confirmAccident=="y":
                break
            con=connect_db()
            cur=con.cursor()
            #SELECT COUNT(DISTINCT student_email_id), class_id,MIN(date) FROM session_attendance WHERE class_id IN (SELECT class_id FROM enrollment WHERE professor = 'Professor Olivia Davis') AND (date<'2024-12-30' AND date>'2024-08-01') GROUP BY class_id;
            nameOfProf=str(input("What is the name of the professor?: "))
            isSemFall=str(input("Is the semester you are looking for the fall or spring semester? If it is the Fall type f. If not type anything.: "))
            whatYear=str(input("What year is the semester you want to get data from? Type the year as a number: "))
            execString="SELECT COUNT(DISTINCT student_email_id), class_id,MIN(date) FROM session_attendance WHERE class_id IN (SELECT class_id FROM enrollment WHERE professor ILIKE '"+ "%"+ nameOfProf +"') AND (date<'"
            if isSemFall=="f":
                execString=execString+whatYear+"-12-30' AND date>'"+whatYear+"-08-01') GROUP BY class_id;"
            else:
                execString=execString+whatYear+"-05-30' AND date>'"+whatYear+"-01-01') GROUP BY class_id;"
            cur.execute(execString)
            rows=cur.fetchall()
            newTable=[[row[i] for i in range(len(row)) if i != 2] for row in rows]#I had to get help from microsoft copilot because I want the new table to not have the useless column. It taught me how to concatenate a list in python
            head=["Number Of Students","Class ID"]#I am concatenating a list within a list as a mentioned above, it is quite difficult to write this so I had to get help.
            print(tabulate(newTable,headers=head,tablefmt="fancy_grid"))
            con.commit()
            cur.close()
            con.close()
            continu=str(input("Press any key to continue.: "))
        elif userInput==3:
            confirmAccident=input("If you accidentally selected then press y else press any key: ")
            if confirmAccident=="y":
                break
            con=connect_db()
            cur=con.cursor()
            cur.execute("SELECT * FROM student;")
            rows=cur.fetchall()
            head=["Email ID","Full Name","Athlete"]
            print(tabulate(rows,headers=head,tablefmt="fancy_grid"))
            con.commit()
            cur.close()
            con.close()
            continu=str(input("Press any key to continue.: "))
        elif userInput==4:
            confirmAccident=input("If you accidentally selected then press y else press any key: ")
            if confirmAccident=="y":
                break
            con=connect_db()
            cur=con.cursor()
            cur.execute("SELECT * FROM tutor;")
            rows=cur.fetchall()
            head=["Email ID","Full Name","Phone Number"]
            print(tabulate(rows,headers=head,tablefmt="fancy_grid"))
            con.commit()
            cur.close()
            con.close()
            continu=str(input("Press any key to continue.: "))
        elif userInput==5:
            studentOrTutor=str(input("If you want to alter student record type s else if you want to alter tutor record type any key.: "))
            if studentOrTutor=="s":
                studentEmailID=input("What is the student's Email ID?: ")
                con=connect_db()
                cur=con.cursor()
                cur.execute("SELECT * FROM student WHERE student_email_id = %s",(studentEmailID,))
                rows=cur.fetchall()
                if rows == []:
                    print("Unfortunately no student was found with that email ID.")
                    useless=input("Press any key to continue.")
                else:
                    head=["Email ID","Full Name","Athlete"]
                    print(tabulate(rows,headers=head,tablefmt="fancy_grid"))
                    tooLate=False
                    cur.execute("SELECT * FROM session_attendance WHERE student_email_id = %s",(studentEmailID,))
                    rows=cur.fetchall()
                    if rows == []:
                        cur.execute("SELECT * FROM enrollment WHERE student_email_id = %s",(studentEmailID,))
                        rows=cur.fetchall()
                        if rows != []:
                            tooLate=True
                    else:
                        tooLate=True
                    if tooLate==False:
                        choice=get_valid_integer("1. Change name.\n2. Change athlete status.\n3. Change ID.\n4. Change all three.",1,4)
                        if choice==1:
                            newName=str(input("Enter the new full name of the student: "))
                            cur.execute("UPDATE student SET full_name=%s WHERE student_email_id = %s",(newName,studentEmailID))
                            con.commit()
                            cur.close()
                            con.close()
                            ueless=input("Type any key to continue: ")
                        elif choice==2:
                            Athlete=str(input("If the student is now an athlete enter y, if they are no longer an athlete enter any key: "))
                            if Athlete=="y":
                                cur.execute("UPDATE student SET athlete=True WHERE student_email_id = %s",(studentEmailID,))
                            else:
                                cur.execute("UPDATE student SET athlete=False WHERE student_email_id = %s",(studentEmailID,))
                            con.commit()
                            cur.close()
                            con.close()
                            ueless=input("Type any key to continue: ")
                        elif choice==3:
                            newID=str(input("Enter the new Email ID of the student: "))
                            cur.execute("UPDATE student SET student_email_id=%s WHERE student_email_id = %s",(newID,studentEmailID))
                            con.commit()
                            cur.close()
                            con.close()
                            ueless=input("Type any key to continue: ")
                        elif choice==4:
                            newName=str(input("Enter the new full name of the student: "))
                            Athlete=str(input("If the student is now an athlete enter y, if they are no longer an athlete enter any key: "))
                            newID=str(input("Enter the new Email ID of the student: "))
                            cur.execute("UPDATE student SET student_email_id=%s WHERE student_email_id = %s",(newID,studentEmailID))
                            cur.execute("UPDATE student SET full_name=%s WHERE student_email_id = %s",(newName,newID))
                            if Athlete=="y":
                                cur.execute("UPDATE student SET athlete=True WHERE student_email_id = %s",(newID,))
                            else:
                                cur.execute("UPDATE student SET athlete=False WHERE student_email_id = %s",(newID,))
                            con.commit()
                            cur.close()
                            con.close()
                            ueless=input("Type any key to continue: ")
                    else:
                        choice=get_valid_integer("1. Change name.\n2. Change athlete status.\n3. Change all two.",1,3)
                        if choice==1:
                            newName=str(input("Enter the new full name of the student: "))
                            cur.execute("UPDATE student SET full_name=%s WHERE student_email_id = %s",(newName,studentEmailID))
                            con.commit()
                            cur.close()
                            con.close()
                            ueless=input("Type any key to continue: ")
                        elif choice==2:
                            Athlete=str(input("If the student is now an athlete enter y, if they are no longer an athlete enter any key: "))
                            if Athlete=="y":
                                cur.execute("UPDATE student SET athlete=True WHERE student_email_id = %s",(studentEmailID,))
                            else:
                                cur.execute("UPDATE student SET athlete=False WHERE student_email_id = %s",(studentEmailID,))
                            con.commit()
                            cur.close()
                            con.close()
                            ueless=input("Type any key to continue: ")
                        elif choice==3:
                            newName=str(input("Enter the new full name of the student: "))
                            Athlete=str(input("If the student is now an athlete enter y, if they are no longer an athlete enter any key: "))
                            cur.execute("UPDATE student SET full_name=%s WHERE student_email_id = %s",(newName,studentEmailID))
                            if Athlete=="y":
                                cur.execute("UPDATE student SET athlete=True WHERE student_email_id = %s",(studentEmailID,))
                            else:
                                cur.execute("UPDATE student SET athlete=False WHERE student_email_id = %s",(studentEmailID,))
                            con.commit()
                            cur.close()
                            con.close()
                            ueless=input("Type any key to continue: ")
            else:
                tutorEmailID=input("What is the tutor's Email ID?: ")
                con=connect_db()
                cur=con.cursor()
                cur.execute("SELECT * FROM tutor WHERE tutor_email_id = %s",(tutorEmailID,))
                rows=cur.fetchall()
                if rows == []:
                    print("Unfortunately no tutor was found with that email ID.")
                    useless=input("Press any key to continue.")
                else:
                    head=["Email ID","Full Name","Phone Numbers"]
                    print(tabulate(rows,headers=head,tablefmt="fancy_grid"))
                    tooLate=False
                    cur.execute("SELECT * FROM tutor_attendance WHERE tutor_email_id = %s",(tutorEmailID,))
                    rows=cur.fetchall()
                    if rows == []:
                        cur.execute("SELECT * FROM session_attendance WHERE tutor_email_id = %s",(tutorEmailID,))
                        rows=cur.fetchall()
                        if rows != []:
                            tooLate=True
                    else:
                        tooLate=True
                    if tooLate==False:
                        choice=get_valid_integer("1. Change name.\n2. Change phone number.\n3. Change ID.\n4. Change all three.",1,4)
                        if choice==1:
                            newName=str(input("Enter the new full name of the tutor: "))
                            cur.execute("UPDATE tutor SET full_name=%s WHERE tutor_email_id = %s",(newName,tutorEmailID))
                            con.commit()
                            cur.close()
                            con.close()
                            ueless=input("Type any key to continue: ")
                        elif choice==2:
                            #change!
                            '''HERE HERE HERE'''
                            phoneNumTemp=str(input("Type your phone number and then press enter: "))
                            phoneNum=""
                            unwantedInPhonNum=["-","(",")"," "]
                            for char in phoneNumTemp:#the dashes in phone numbers is removed because people might type their phone number in with dashes
                                if char not in unwantedInPhonNum:
                                    phoneNum+=char
                            cur.execute("UPDATE tutor SET phone_number = %s WHERE tutor_email_id=%s",(phoneNum,tutorEmailID))
                            con.commit()
                            cur.close()
                            con.close()
                            ueless=input("Type any key to continue: ")
                        elif choice==3:
                            newID=str(input("Enter the new Email ID of the tutor: "))
                            cur.execute("UPDATE tutor SET tutor_email_id=%s WHERE tutor_email_id = %s",(newID,tutorEmailID))
                            con.commit()
                            cur.close()
                            con.close()
                            ueless=input("Type any key to continue: ")
                        elif choice==4:
                            newName=str(input("Enter the new full name of the tutor: "))
                            phoneNumTemp=str(input("Type your phone number and then press enter: "))
                            newID=str(input("Enter the new Email ID of the tutor: "))
                            cur.execute("UPDATE tutor SET tutor_email_id=%s WHERE tutor_email_id = %s",(newID,tutorEmailID))
                            cur.execute("UPDATE tutor SET full_name=%s WHERE tutor_email_id = %s",(newName,newID))
                            phoneNum=""
                            unwantedInPhonNum=["-","(",")"," "]
                            for char in phoneNumTemp:#the dashes in phone numbers is removed because people might type their phone number in with dashes
                                if char not in unwantedInPhonNum:
                                    phoneNum+=char
                            cur.execute("UPDATE tutor SET phone_number = %s WHERE tutor_email_id=%s",(phoneNum,newID))
                            con.commit()
                            cur.close()
                            con.close()
                            ueless=input("Type any key to continue: ")
                    else:
                        choice=get_valid_integer("1. Change name.\n2. Change phone number.\n3. Change all two.",1,4)
                        if choice==1:
                            newName=str(input("Enter the new full name of the tutor: "))
                            cur.execute("UPDATE tutor SET full_name=%s WHERE tutor_email_id = %s",(newName,tutorEmailID))
                            con.commit()
                            cur.close()
                            con.close()
                            ueless=input("Type any key to continue: ")
                        elif choice==2:
                            #change!
                            '''HERE HERE HERE'''
                            phoneNumTemp=str(input("Type your phone number and then press enter: "))
                            phoneNum=""
                            unwantedInPhonNum=["-","(",")"," "]
                            for char in phoneNumTemp:#the dashes in phone numbers is removed because people might type their phone number in with dashes
                                if char not in unwantedInPhonNum:
                                    phoneNum+=char
                            cur.execute("UPDATE tutor SET phone_number = %s WHERE tutor_email_id=%s",(phoneNum,tutorEmailID))
                            con.commit()
                            cur.close()
                            con.close()
                            ueless=input("Type any key to continue: ")
                        elif choice==3:
                            newName=str(input("Enter the new full name of the tutor: "))
                            phoneNumTemp=str(input("Type your phone number and then press enter: "))
                            cur.execute("UPDATE tutor SET full_name=%s WHERE tutor_email_id = %s",(newName,tutorEmailID))
                            phoneNum=""
                            unwantedInPhonNum=["-","(",")"," "]
                            for char in phoneNumTemp:#the dashes in phone numbers is removed because people might type their phone number in with dashes
                                if char not in unwantedInPhonNum:
                                    phoneNum+=char
                            cur.execute("UPDATE tutor SET phone_number = %s WHERE tutor_email_id=%s",(phoneNum,tutorEmailID))
                            con.commit()
                            cur.close()
                            con.close()
                            ueless=input("Type any key to continue: ")
        break

while True:
    selectRole=str(input("Enter s if you are a student, t if you are a tutor, and a if you are an admin. If you want to exit enter q.: "))
    if selectRole=="s":
        confirmAccident=input("If you accidentally selected then press y else press any key: ")
        if confirmAccident=="y":
            break
        print("If this is you first time using math tutoring services sign up by entering 1.")
        print("If you want to sign in or sign out to math tutoring enter 2.")
        studentChoice=get_valid_integer("Enter you choice: ",1,2)
        if studentChoice==1:
            newStudent()
        elif studentChoice==2:
            sessionAttend()
    elif selectRole=="t":
        confirmAccident=input("If you accidentally selected then press y else press any key: ")
        if confirmAccident=="y":
            break
        print("If you are a new tutor sign up by entering 1.")
        print("If you want to clock in or clock out of your job enter 2.")
        tutorChoice=get_valid_integer("Enter your choice: ",1,2)
        if tutorChoice==1:
            newTutor()
        elif tutorChoice==2:
            tutorAttend()
    elif selectRole=="a":
        confirmAccident=input("If you accidentally selected then press y else press any key: ")
        if confirmAccident=="y":
            break
        admin()
    elif selectRole=="q":
        print("Exiting program.")
        break
