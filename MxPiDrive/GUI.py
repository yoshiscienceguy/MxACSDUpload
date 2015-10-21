import Tkinter as tk
import tkFileDialog
import gdrive
import time
import urllib2
import webbrowser


UNITS = [
    ("Unit 1: Hardware Terminology", "Hardware Terminology"),
    ("Unit 2: Blink Blink", "Blink Blink"),
    ("Unit 3: Google Drive", "Google Drive"),
    ("Unit 4: Ho Ho Holiday Lights", "Ho Ho Holiday Lights"),
    ("Unit 5: Rock Paper Scissors", "Rock Paper Scissors"),
    ("Unit 6: Dice Game", "Dice Game"),
    ("Unit 7: Simon Says", "Simon Says"),
    ("Unit 8: Home Alarm System", "Home Alarm System"),]


try:
    response = urllib2.urlopen("http://www.google.com",timeout=1)
except:
    print("You Don't Have an Active Internet Connection")
    print("Please ask a Mentor for HELP")
    quit()
class Menu():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Google Drive Upload")
        self.master = tk.Frame(self.root,width= 300)
        self.menu = tk.Frame(self.root,width= 300)
        self.buttons = tk.Frame (self.root,width= 300)
        self.master.pack()
        #tk.mainloop()
        
    def drawDropDown(self,frame,functionName,listDisplay,Default = False):
        AssociatedVariable = tk.StringVar(frame)
        AssociatedVariable.trace("w",eval(functionName))
        DropDown = apply(tk.OptionMenu,(frame,AssociatedVariable)+tuple(listDisplay))
        if(Default):
            AssociatedVariable.set(listDisplay[0])
        DropDown.pack(pady=(10,0))

        return DropDown , AssociatedVariable
        
        
    def drawButton(self,frame,toSay,functionName):
        submit = tk.Button(frame, text = toSay,command = eval(functionName))

        return submit
    
    def drawRadioButtons(self,frame):
        v = tk.StringVar()

        Buttons = []
        for texts, unit in UNITS:
            rb = tk.Radiobutton(frame, text = texts, variable = v, value = unit)
            rb.pack(anchor = tk.W)
            rb.deselect()
            Buttons.append(rb)
        v.set("Hardware Terminology")
        return v, Buttons
    def drawMenu(self,frame,listDisplay,NewOption = False):

        scrollbar = tk.Scrollbar(frame,orient = tk.VERTICAL)
        listbox = tk.Listbox(frame,yscrollcommand = scrollbar.set,width = 50)
        scrollbar.config(command = listbox.yview)

        if(NewOption):
            listbox.insert(tk.END,"(create New)")
        for item in listDisplay:
            listbox.insert(tk.END,item)

        return listbox,scrollbar
    def drawMessage(self,frame,toSay):
        var = tk.StringVar()
        textbox = tk.Label(frame,textvariable = var)
        var.set(toSay)
        textbox.pack(pady = 10)
        return var
    def drawTextBox (self,frame):
        userinput = tk.StringVar()
        entry = tk.Entry(frame,textvariable = userinput,width = 50,justify =tk.CENTER)
        entry.pack(pady = 10)
        return entry , userinput
    def UpdateList(self,obj,var,lis):
        obj["menu"].delete(0,"end")
        TeachersVar.set (lis[0])
        for things in lis:
            obj["menu"].add_command(label = things,command = tk._setit(var,things))
    def UpdateMenu(self,obj,newlist,makeNew = False):
    
        obj.delete(0,tk.END)
        if(makeNew):
            obj.insert(tk.END,"(Create New Team)")
        for thing in newlist:
            obj.insert(tk.END,thing)
    def packMenu(self,listbox,scrollbar):
        
        listbox.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
class Handlers:
    def __init__(self):
        self.school = ""
        self.day = time.strftime("%A")
        self.teacher = ""
        self.dayID = ""
        self.TeacherIds = {}
        self.TeamIds = {}
        self.TeamFolder = {}

    def TeacherHandler(self,p,a,c):

        self.teacher = TeachersVar.get()

        self.TeamIds = gdrive.GetFolders(drive,self.TeacherIds[self.teacher])
        Teams = GetList(self.TeamIds)
        try:
            for radio in self.UnitChoices:
                radio.pack_forget()
        except:
            print("Radio Buttons don't Exist")
            pass
        
        ChooseUploadFolder.pack_forget()
        TechnicalReport.pack_forget()
        m.buttons.pack_forget()
        m.menu.pack()
        #m.packMenu(GroupNames,gns)
        GroupNames.pack()
        DisplayText.set("Please Choose Your Teacher\n"+"_"*30+"\n\nChoose Your Team \nor Create a New One")
        m.UpdateMenu(GroupNames,Teams,True)
        
        chooseGroupButton.pack(pady = 10)
        m.buttons.pack()

    def SchoolHandler(self,p,a,c):
        try:
            self.school = LocationVar.get()

            self.TeacherIds = gdrive.GetFolders(drive,folders[LocationVar.get()])


            
            Teachers = GetList(self.TeacherIds)
     
            m.UpdateList(TeachersObj,TeachersVar,Teachers)
        except:
            print("Starting")
            pass
    def CreateNewFolder(self):
        self.slave = tk.Tk()
        newFrame = tk.Frame(self.slave,width = 200)
        self.slave.title("Enter New Folder Name")
        self.NewNameObject, self.NewNameVariable = m.drawTextBox(newFrame)
        
        self.Createbutton = m.drawButton(newFrame,"Create","h.FolderCreation")
        self.Createbutton.pack(pady = (0,10))
        newFrame.pack()
    def FolderCreation(self):
        newid = gdrive.CreateFolder(drive,self.NewNameObject.get(),self.TeacherIds[self.teacher])
        self.slave.destroy()
        DocId = gdrive.CreateFolder(drive,"Documents",newid)
        CodeId = gdrive.CreateFolder(drive,"Code",newid)
        gdrive.CopyTechnicalReport(drive,DocId)
        self.TeamFolder = gdrive.GetFolders (drive,self.TeacherIds[self.teacher])
        Teams = GetList(self.TeamFolder)

        m.UpdateMenu(GroupNames,Teams,True)
    def ChooseTeam(self):
        try:
            if(int(GroupNames.curselection()[0]) == 0):
                self.CreateNewFolder()
            else:
                self.TeamIds = gdrive.GetFolders(drive,self.TeacherIds[self.teacher])
                Teams = GetList(self.TeamIds)
                currentselection = Teams[int(GroupNames.curselection()[0])-1]
                DisplayText.set("Current Selected Team: "+ currentselection)
                GroupNames.pack_forget ()
                gns.pack_forget()
                chooseGroupButton.pack_forget()
                m.buttons.pack_forget()

                #m.packMenu(GroupFolders,gfs)
                #GroupFolders.pack()
                #m.menu.pack_forget ()
                ChooseUploadFolder.pack()
                TechnicalReport.pack()

                self.Unit, self.UnitChoices = m.drawRadioButtons(m.menu);

                m.buttons.pack(pady = 10)
                currentTeamID = self.TeamIds[currentselection]
                self.TeamFolder = gdrive.GetFolders (drive,currentTeamID)
                InnerFolders = GetList(self.TeamFolder)

                
        except:
           print("Choose a Team")
    def TechnicalReport(self):
        
        ProjectName = self.Unit.get() + " Technical Report"


        gdrive.CopyTechnicalReport (drive,self.TeamFolder["Documents"],ProjectName)
        url = gdrive.GetFiles(drive,self.TeamFolder["Documents"])
        
        webbrowser.open(url,new = 2)
    def UploadButton(self):
        try:

            #Folder2Upload = self.TeamFolder[Folders[int(GroupFolders.curselection()[0])]]
            Folder2Upload = self.TeamFolder['Code']
            try:
                path = tkFileDialog.askopenfilename()
            
                parts = path.split("/")
                FileName = parts[-1].split(".")[0]
                FileName +=  " " + self.Unit.get()
                print(FileName)

                #path = "C:\Users\Fernando\Desktop\Anaheim GoogleDrive\test.txt"
                gdrive.UploadFile (drive,Folder2Upload,path,FileName)
                print('Upload \"'+ FileName+'\" Successful')
                DisplayText.set ('Upload \"'+ FileName+'\" Successful')
            except:
                print("No File Selected")
                
        except:
            print("Please Select a Folder")


        
def GetList(tup,ex = []):
    newlist = tup.keys()
    toreturn = []
    for thing in newlist:
        if(not thing in ex):
            toreturn.append(thing)
    return toreturn
m = Menu()
h = Handlers()
drive = gdrive.Connect()




folders = gdrive.GetFolders(drive)
LocationObj,LocationVar = m.drawDropDown(m.master,"h.SchoolHandler",GetList(folders,["Technical Report Template"]),True)
TeachersObj,TeachersVar = m.drawDropDown(m.master,"h.TeacherHandler",[""])
DisplayText = m.drawMessage(m.master,"Please Choose a School")
GroupNames,gns = m.drawMenu(m.menu,[],True)
chooseGroupButton = m.drawButton(m.buttons,"Choose","h.ChooseTeam")




TechnicalReport = m.drawButton(m.buttons,"Technical Report", "h.TechnicalReport")
ChooseUploadFolder = m.drawButton(m.buttons,"Upload Code","h.UploadButton")

m.menu.pack()
m.buttons.pack ()
tk.mainloop()

