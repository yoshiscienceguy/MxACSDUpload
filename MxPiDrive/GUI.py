import Tkinter as tk
import tkFileDialog
import gdrive
import time, platform, os, urllib2, webbrowser

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
            AssociatedVariable.set("Choose")

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
           # print("Radio Buttons don't Exist")
            pass
        ChooseDownloadCode.pack_forget()
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
        #gdrive.CopyTechnicalReport(drive,DocId)
        self.TeamFolder = gdrive.GetFolders (drive,self.TeacherIds[self.teacher])
        Teams = GetList(self.TeamFolder)

        m.UpdateMenu(GroupNames,Teams,True)
    def CreateAlert(self,message):
        self.slave = slave = tk.Tk()
        newFrame = tk.Frame(self.slave, width = 200)
        self.slave.title("Alert")
        T = tk.Label(self.slave,text = message)
        T.pack(padx = (10,10),pady = (10,10))


        self.Createbutton = m.drawButton(newFrame,"Ok",'h.destroy')
        self.Createbutton.pack(pady = (0,10))
        newFrame.pack()
    def destroy(self):
        self.slave.destroy()
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
                os = platform.platform().split('-')[0]
                if(os == "Windows"):
                   TechnicalReport.pack() 

                ChooseUploadFolder.pack()
                ChooseDownloadCode.pack()

                self.Unit, self.UnitChoices = m.drawRadioButtons(m.menu);

                m.buttons.pack(pady = 10)
                currentTeamID = self.TeamIds[currentselection]
                self.TeamFolder = gdrive.GetFolders (drive,currentTeamID)
                InnerFolders = GetList(self.TeamFolder)

                
        except:
            self.CreateAlert("Please Choose a Team")
            
    def TechnicalReport(self,silent = False):
        
        ProjectName = self.Unit.get() + " Technical Report"


        gdrive.CopyTechnicalReport (drive,self.TeamFolder["Documents"],ProjectName)
        url = gdrive.GetFileURL(drive,ProjectName,self.TeamFolder["Documents"])
        if(not silent):
            webbrowser.open(url,new = 2)
    def UploadButton(self):
        try:

            #Folder2Upload = self.TeamFolder[Folders[int(GroupFolders.curselection()[0])]]
            Folder2Upload = self.TeamFolder['Code']
            try:
                options = {}
                options['defaultextension'] = '.py'
                options['filetypes'] = [('Python Files', '.py'),('All Files', '.*')]
                osType = platform.platform().split("-")[0]
                if(osType!= "Windows"):
                    options['initialdir'] = '/home/pi/Desktop'
                else:
                    options['initialdir'] = os.path.expanduser("~")+"\\Desktop\\"
                
                

                options['parent'] = m.buttons
                options['title'] = 'Select file to Upload'
                
                path = tkFileDialog.askopenfilename(**options)

                
                parts = path.split("/")
                FileName = parts[-1].split(".")[0]

                if(gdrive.GetFileID(drive,FileName + ".py",Folder2Upload) == None):
                    FileName +=  " (" + self.Unit.get() + ").py"
                else:
                    FileName += ".py"


                #path = "C:\Users\Fernando\Desktop\Anaheim GoogleDrive\test.txt"
                gdrive.UploadFile (drive,Folder2Upload,path,FileName)
                print('Upload \"'+ FileName+'\" Successful')
                self.CreateAlert('Upload \"'+ FileName+'\" Successful')
                os.remove(path)
                self.TechnicalReport(True)
            except:
                self.CreateAlert("No File Selected")
                
        except:
            self.CreateAlert("Please Select a Folder")


    def DownloadButton(self):
        Folder2Download = self.TeamFolder['Code']
        path = '/home/pi'
        Files = gdrive.GetFiles(drive,Folder2Download)
        FileID = None
        FileName = None
        for file1 in Files:
            if(self.Unit.get() in file1):
                FileName =file1
                FileID = Files[file1]
                break
        if(FileID and FileName):
            gdrive.DownloadFile(drive,FileID,FileName)
            osType = platform.platform().split("-")[0]
            if(osType!= "Windows"):
                DesktopPath= "/home/pi/Desktop/"
            else:
                DesktopPath = os.path.expanduser("~")+"\Desktop\\"

            try:
                os.rename(FileName,DesktopPath+FileName)
            except:
                os.remove(DesktopPath+FileName)
                os.rename(FileName,DesktopPath+FileName)
            print('Download \"'+ FileName+'\" Successful')
            self.CreateAlert("File Downloaded! Look for it on Desktop")
                
        else:
            self.CreateAlert("File Does not Exist")

        
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
ChooseDownloadCode = m.drawButton(m.buttons,"Download Code", "h.DownloadButton")

m.menu.pack()
m.buttons.pack ()
tk.mainloop()

