from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import time

SFID = "0B6OVPYHQgk9NYW43bzhQMmE1cUU"
TechID = "16grOWcXkxrjt1JundUKUQoGlPZigPBsOzExyKozcpD8"

def Connect():
    print("Authenticating")
    gauth = GoogleAuth()

    try:
        gauth.LoadCredentialsFile("./mycreds.txt")
    except:
        gauth.LoadCredentialsFile("home/pi/Mx/MxPiDrive/mycreds.txt")
        
    if( gauth.credentials is None):
        gauth.LocalWebserverAuth()
    elif( gauth.access_token_expired):
        gauth.Refresh()
    else:
        gauth.Authorize()
        
    try:
        gauth.LoadCredentialsFile("./mycreds.txt")
    except:
        gauth.LoadCredentialsFile("home/pi/Mx/MxPiDrive/mycreds.txt")
        
    print("Done Authenticating")

    drive = GoogleDrive(gauth)
    return drive
def CopyTechnicalReport(drive,parent,name = "Technical Report"):
    drive.auth.service.files().copy(fileId = TechID, body={"parents":[{"kind": "drive#fileLink",
                                                                   "id": parent}], 'title': name}).execute()
def GetFiles(drive,ParentId = None):
    if(not ParentId):
        ParentId = SFID
    file_list = drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()

    ViewTime = None
    name = None
    for file1 in file_list:
        if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
            if(ViewTime == None):
                ViewTime = file1['lastViewedByMeDate']
                name = file1['title']
            else:
                if(ViewTime < file1['lastViewedByMeDate']):
                    ViewTime = file1['lastViewedByMeDate']
                    name = file1['title']
                    
    for file1 in file_list:
        if(file1['title'] == name):
            name = file1['alternateLink']
    #Files[file1["title"]] = file1["alternateLink"]
                    
    return name
def GetFolders(drive,ParentId = None):
    if(not ParentId):
        ParentId = SFID
    file_list = drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()
    Folders = {}
    for file1 in file_list:
        #print(file1['alternateLink'])
        if(file1['mimeType'] == "application/vnd.google-apps.folder"):
            Folders[file1["title"]] = file1["id"]
    return Folders
def UploadFile(drive,ParentId,FilePath,FileName):

    file2Upload = drive.CreateFile({"parents":[{"id" : ParentId}]})
    file2Upload.SetContentFile(FilePath)
    file2Upload["title"] = FileName
    file2Upload.Upload()
def GetTeacherID(drive,dayId,Name):
    file_list = drive.ListFile({"q":"'"+dayId+"' in parents and trashed = false"}).GetList()
    for file1 in file_list:
        if(Name == file1['title']):
            return {file1['title'] : file1['id']}
            
def GetClassFolderID(drive,SchoolId,Day):
    file_list = drive.ListFile({"q":"'"+SchoolId+"' in parents and trashed = false"}).GetList()
    for file1 in file_list:
        if(Day in file1['title']):
            return {file1['title'] : file1['id']}
            
def GetSchoolFolderIDs(drive):
    file_list = drive.ListFile({"q":"'"+SFID+"' in parents and trashed = false"}).GetList()
    SchoolIds = {}
    for file1 in file_list:
        if(not "Technical" in file1['title']):
            SchoolIds[file1['title'].strip()] = file1['id']
    return SchoolIds
def CreateFolder(drive,FolderName,ParentId):
    newFolder = drive.CreateFile({"title":FolderName,
                                  "mimeType": "application/vnd.google-apps.folder",
                                  "parents" : [{"id" : ParentId}]})
    newFolder.Upload()
    return newFolder['id']

##DRIVE = Connect()
##Ids = GetSchoolFolderIDs(DRIVE)
##cD = time.strftime("%A")
##DayId = GetClassFolderID(DRIVE,Ids['Ponderosa'],cD)
##p = "C:\\Users\\Fernando\\Desktop\\Anaheim GoogleDrive\\test.txt"
##ClassId = GetTeacherID(DRIVE,DayId[cD],"Vasquez")
##Upload(DRIVE,ClassId["Vasquez"],"Code",p,"test")
