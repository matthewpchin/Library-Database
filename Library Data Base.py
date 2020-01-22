from easygui import *
import sys
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="xxxxx",
  passwd="xxxxx",
  database="library"
)
mycursor = mydb.cursor()
def Startmenu (): #Startmenu
 UsernameTaken = 0#for a later function
 LoginMessage = indexbox(msg='Welcome to the Library database', title='Library Database', choices=(['Login', 'Create Login', 'Change Password','Exit']), image=None)
 if LoginMessage == 0: #if user chooses Login
   while True:
     fieldNames = ["Username", "Password"]
     fieldValues = []
     fieldValues = multpasswordbox("Enter login information","Library Login",fieldNames )
     while 1: #checks if all of the fields are filled in
         if fieldValues == None: break
         errmsg = ""
         for i in range(len(fieldNames)):
             if fieldValues[i].strip() == "":
                 errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
         if errmsg == "": break # no problems found
         fieldValues = multpasswordbox(errmsg,"Login Menu", fieldNames, fieldValues) #If problems are found
     if fieldValues == None: #If user cancels
         return 1 #returns to start menu
     sql = "SELECT * FROM users WHERE username = %s AND password = %s"
     val = (fieldValues[0],fieldValues[1])
     mycursor.execute(sql, val)
     myresult = mycursor.fetchall()
     if tuple(fieldValues) in myresult: #reads sql search and if user info matches
         global currentUser #For later Function
         currentUser = fieldValues[0]#holds the current user
         print(currentUser)
         break #This will jump to the Library database
     elif tuple(fieldValues) not in myresult and fieldValues != None: #if user info doesn't match
         msgbox("Invalid User Information")
         continue
     elif fieldValues == None:
         return 1 #returns to start menu
 elif LoginMessage == 1: #if user chooses creat a user
   while True:
     msg = "Enter your User Information"
     title = "Create a User"
     fieldNames = ["First name","Last Name","Username","Password"]
     fieldValues = []  # we start with blanks for the values
     fieldValues = multpasswordbox(msg,title, fieldNames)
     while 1: #checks if all of the fields are filled in
         if fieldValues == None: break
         errmsg = ""
         for i in range(len(fieldNames)):
             if fieldValues[i].strip() == "":
                 errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
         if errmsg == "": break # no problems found
         fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues) #If problems found
     if fieldValues == None:
         return 1 #returns to start menu
     print(fieldValues)
     sql = "SELECT * FROM users WHERE username = %s AND password = %s"
     val = (fieldValues[2],fieldValues[3])
     mycursor.execute(sql, val)
     myresult = mycursor.fetchall()
     for i in range (0, len(myresult)):#checks username to database
         if fieldValues[2] == myresult[i][0]: #if Username taken
             msgbox("Username Already Taken")
             UsernameTaken = 1 #Sets UserTaken to 1
             continue #this will break out of the For loop function
         elif fieldValues[2] != myresult[i][0]:
             continue
     if UsernameTaken == 1:#If the function = 1 this will loop the outer function
        UsernameTaken = 0 #Resets UserTaken to 0
        continue
     passwordCheck = multpasswordbox("Confirm your Password","Password Confirmation",["Confirm your Password"])
     if passwordCheck== None: #cancel button
         return 1 #returns to start menu
     elif fieldValues[3] == passwordCheck[0]: #If password matches
         sql = "INSERT INTO users (username,password) VALUES (%s,%s)"
         val = (fieldValues[2],fieldValues[3])
         mycursor.execute(sql, val)
         mydb.commit()
         msgbox("Account Created Successfully")
         ynbox("Would You Like to Return to the Login Menu?")
         if 1:
            return 1 #returns to start menu
         else:
            sys.exit(0) #exits
     elif fieldValues[3] != passwordCheck[0]:
         msgbox("Passwords Do not Match \n Please Try Again")
         continue #Loops back to Create Login page
 elif LoginMessage == 2: #If user chooses change password
   while True:
     msg = "Enter your User Information"
     title = "Change your Password"
     fieldNames = ["Username", "Password"]
     fieldValues = []
     fieldValues = multpasswordbox(msg,title,fieldNames)
     while 1: #checks if all of the fields are filled in
         if fieldValues == None: break
         errmsg = ""
         for i in range(len(fieldNames)):
             if fieldValues[i].strip() == "":
                 errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
         if errmsg == "": break # no problems found
         fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues) #If problems found
     if fieldValues == None:
         return 1 #returns to start menu
     print(fieldValues)
     sql = "SELECT * FROM users WHERE username = %s AND password = %s"
     val = (fieldValues[0],fieldValues[1])
     mycursor.execute(sql, val)
     myresult = mycursor.fetchall()
     if tuple(fieldValues) in myresult: #reads the nested list and if the user info matches
         confirmedPassword = passwordbox("Please Confirm your password","Confirm your Password") #confirm Password
         if confirmedPassword == fieldValues[1]:
             newPassword = passwordbox("Please Enter your New Password", "Enter your New Password") #Enter New Password
             if newPassword == None:
                 return 1 #returns to start menu
             checkNewPassword = passwordbox("Please Re-enter your New Password", "Re-enter your New Password") #confirm new password
             if checkNewPassword == None:
                 return 1 #returns to start menu
             elif checkNewPassword != newPassword:
                 msgbox("New Passwords do not Match")
                 continue
             sql = "UPDATE users SET password = %s WHERE password = %s AND username = %s"
             val = (newPassword,fieldValues[1],fieldValues[0])
             mycursor.execute(sql, val)
             mydb.commit()
             msgbox("Password Successfully Changed")
             yn = ynbox("Would You Like to Return to the Main Menu?")
             if yn == True:
                 return 1 #returns to start menu
             else:
                 sys.exit(0) #Exits
         elif confirmedPassword == None:
                 return 1 #returns to start menu
         elif confirmedPassword != fieldValues[1]:
                 msgbox("Passwords do not Match")
                 continue
         elif fieldValues == None:
             continue
     else:
        msgbox("Invalid Username or Password")
        continue
 else:
   sys.exit(0) #exits

def MainMenu(): #Main Menu
    ISBNin = 0
    MainMenuTab = indexbox(currentUser+' Welcome to the Library database','Library Database',(['Make an Entry', 'Find an Entry', 'Delete an Entry','Exit']), image="Library.gif")
    if MainMenuTab == 0: #If User Chooses Create an Entry
        while True:
            fieldNames = ["Title", "Author","ISBN","Type"]
            fieldValues = ["","","xxxxxxxxxxxxx","Book, Magazine, or Movie (This is Case Sensitive)"]
            fieldValues = multenterbox("To Make an Entry, Please Fill in the Corresponding Fields","Library Database",fieldNames,fieldValues)
            while 1: #checks if all of the fields are filled in
               if fieldValues == None: break
               errmsg = ""
               for i in range(len(fieldNames)):
                   if fieldValues[i].strip() == "":
                       errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
               if errmsg == "": break # no problems found
               fieldValues = multenterbox(errmsg,"Library Database",fieldNames,["","","xxxxxxxxxxxxx","Book, Magazine, or Movie (This is Case Sensitive)"])
            if fieldValues == None:
                return 2 #returns to main menu
            print(fieldValues)
            if len(fieldValues[2]) != 13 or fieldValues[2].isdigit() == False: #If the ISBN is inputted wrong
                msgbox("Error, 13 digit number was not inputted and/or letters were inputted.")
                continue
            if fieldValues[3] == "Book" or fieldValues[3] == "Movie" or fieldValues[3] == "Magazine" or fieldValues[3]:
               print("Good") #Checkes if the Type is Ok
            else:
                msgbox("Error, Type must be Book, Movie, or Magazine")
                continue
            sql = "SELECT * FROM library_data WHERE ISBN = %s"
            val = (fieldValues[2],)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            print(myresult)
            if myresult != []:
                 msgbox("Error, ISBN already in Data Base")
                 continue
            sql = "INSERT INTO library_data (title,author,ISBN,type) VALUES (%s,%s,%s,%s)"
            val = (fieldValues)
            mycursor.execute(sql, val)
            mydb.commit()
            msgbox("Entry Created Successfully")
            yn = ynbox("Would You Like to Return to the Main Menu?")
            if yn == True:
                return 2 #returns to main menu
            else:
                sys.exit(0) #exits
    elif MainMenuTab == 1: #If User chooses Search
        while True:
            SearchTab = indexbox('Select a Search Option','Search Library Database',(['By Title', 'By Author', 'By ISBN','By Type','Cancel']))
            if SearchTab == 0: #IF user Searches by Title
                TitleRecord = []
                TitleSearch = multenterbox("Please Input the Title that you are Searching For","Title Search",["Input Title"])
                if TitleSearch == None:
                    continue
                sql = "SELECT * FROM library_data WHERE title = %s"
                val = (TitleSearch)
                mycursor.execute(sql, val)
                TitlesFound = mycursor.fetchall()
                if TitlesFound == []: # if no titles with searched title found
                    msgbox("No Entries were Found with ' "+TitleSearch+" ' as Their Title")
                    continue
                ShownTitles = ""
                for x in range(0,len(TitlesFound)): #converts list of entries with title searched into readable string
                    ShownTitles = ShownTitles + str(TitlesFound[x]).strip('[]')
                    ShownTitles += "\n"
                print(ShownTitles)
                ShownTitles = ShownTitles.replace('\'','')
                msgbox("These Items have been found in the Data Base with the Title ' "+TitleSearch[0]+" ':"+"\n"+ShownTitles,"Library DataBase")
                if ynbox("Would you Like to Return to the Main Menu?"):
                    return 2 #return to main menu
                else:
                    msgbox("Thanks for Using the Library Database "+currentUser+", Come Back Again Soon!")
                    sys.exit(0) #exits
            if SearchTab == 1: # if user selected search by author
                AuthorRecord = []
                AuthorSearch = multenterbox("Please Input the Author that you are Searching For","Author Search",["Input Author"])
                if AuthorSearch == None: continue
                sql = "SELECT * FROM library_data WHERE author = %s"
                val = (AuthorSearch)
                mycursor.execute(sql, val)
                AuthorsFound = mycursor.fetchall()
                if AuthorsFound == []: #If no authors found
                    msgbox("No Entries were Found with the Author' "+AuthorSearch[0]+" '")
                    continue
                ShownAuthors = ""
                for x in range(0,len(AuthorsFound)): #Turns list of Entries with searched author into readable string
                    ShownAuthors = ShownAuthors + str(AuthorsFound[x]).strip('[]')
                    ShownAuthors += "\n"
                print(ShownAuthors)
                ShownTitles = ShownAuthors.replace('\'','')
                msgbox("These Items have been found in the Database with the Author ' "+AuthorSearch[0]+" ':"+"\n"+ShownAuthors,"Library DataBase")
                if ynbox("Would you Like to Return to the Main Menu?"):
                    return 2 #returns to main menu
                else:
                    msgbox("Thanks for Using the Library Database "+currentUser+", Come Back Again Soon!")
                    sys.exit(0)
            elif SearchTab == 2: #If user searches by ISBN
                ISBNSearch = multenterbox("Please Input the ISBN Number that you are Searching For","ISBN Search",["Input ISBN"])
                if ISBNSearch == None: continue
                sql = "SELECT * FROM library_data WHERE ISBN = %s"
                val = (ISBNSearch)
                mycursor.execute(sql, val)
                ISBNFound = mycursor.fetchall()
                if ISBNFound != []:
                    ISBNFound = str(ISBNFound).strip('[]')
                    print(ISBNFound)
                    msgbox("This Item has been found in the Database with ISBN code ' "+ISBNSearch[0]+" ':"+"\n"+ISBNFound,"Library Database")
                    if ynbox("Would you Like to Return to the Main Menu?"):
                        return 2 #returns to main menu
                    else:
                        msgbox("Thanks for Using the Library Database "+currentUser+", Come Back Again Soon!")
                        sys.exit(0)
                msgbox("ISBN with code '"+ISBNSearch[0]+ "' not found in Database") #If ISBN not in Database
                continue
            elif SearchTab == 3: #If user searches by Type
                TypeSearch = choicebox("Please select the Type you would like to Search For","Type Search",["Book","Magazine","Movie"])
                if TypeSearch == None: continue
                sql = "SELECT * FROM library_data WHERE type = %s"
                val = (TypeSearch,)
                mycursor.execute(sql, val)
                TypesFound = mycursor.fetchall()
                if TypesFound == []: #If no entries found with searched Type
                    msgbox("No Entries were Found with the Type' "+TypeSearch+" '")
                    continue
                ShownTypes = ""
                for x in range(0,len(TypesFound)): #converts list of entries into readable string
                    ShownTypes = ShownTypes + str(TypesFound[x]).strip('[]')
                    ShownTypes += "\n"
                    print(ShownTypes)
                    ShownTypes = ShownTypes.replace('\'','')
                msgbox("These Items have been found in the Database with the Type ' "+TypeSearch+" ':"+"\n"+ShownTypes,"Library DataBase")
                if ynbox("Would you Like to Return to the Main Menu?"):
                    return 2 #returns to main menu
                else:
                    msgbox("Thanks for Using the Library Database "+currentUser+", Come Back Again Soon!")
                    sys.exit(0)
            if SearchTab == 4:
                return 2 #returns to main menu
    elif MainMenuTab == 2: #User selects Delete an Entry
        while 1:
            msg = "Enter the Item that you want to Delete"
            title = "Delete from Database"
            fieldNames = ["Title", "Author","ISBN","Type"]
            fieldValues = []
            fieldValues = multenterbox(msg,title,fieldNames,["","","xxxxxxxxxxxxx","Book, Movie, or Magazine"])
            if fieldValues == None: return 2 #returns to main menu
            while 1: #checks if all of the fields are filled in
                if fieldValues == None: break
                errmsg = ""
                for i in range(len(fieldNames)):
                   if fieldValues[i].strip() == "":
                       errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
                if errmsg == "": break # no problems found
                fieldValues = multenterbox(errmsg, title, fieldNames,["","","xxxxxxxxxxxxx","Book, Movie, or Magazine"])
            if fieldValues == None: return 2 #returns to main menu
            print(fieldValues)
            sql = "SELECT * FROM library_data WHERE (title,author,ISBN,type) = (%s,%s,%s,%s)"
            val = (fieldValues)
            mycursor.execute(sql, val)
            DeleteSearch = mycursor.fetchall()
            if DeleteSearch != []:
                sql = "DELETE FROM library_data WHERE (title,author,ISBN,type) = (%s,%s,%s,%s)"
                val = (fieldValues)
                mycursor.execute(sql, val)
                mydb.commit()
                msgbox("Entry Successfully Deleted")
                if ynbox("Would You Like to Return to the Main Menu?"):
                    return 2 #returns to main menu
                else:
                    sys.exit(0) #Exits
            else:
                msgbox("Entry not found in Database")
                return 2 #returns to main menu
    else:
        msgbox("Thanks for Using the Library Database "+currentUser+", Come Back Again Soon!")
        sys.exit(0)

choice = Startmenu()
while choice == 1: #this function is for the startmenu. Stops the def function from creating babies
    choice = Startmenu()

choice2 = MainMenu()
while choice2 == 2: #This function is for the Main Menu. Stops the def function from creating babies
    choice2 = MainMenu()
