from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import platform

SFID = "0B6OVPYHQgk9NYW43bzhQMmE1cUU"
TechID = "16grOWcXkxrjt1JundUKUQoGlPZigPBsOzExyKozcpD8"

def Connect():
    print("Authenticating")
    gauth = GoogleAuth()

    os = platform.platform().split('-')[0]
    print(os)
    if(os != "Windows"):
        gauth.LoadCredentialsFile("./Mx/MxPiDrive/mycreds.txt")
    else:
        gauth.LoadCredentialsFile("./mycreds.txt")
        
    if( gauth.credentials is None):
        gauth.LocalWebserverAuth()
    elif( gauth.access_token_expired):
        gauth.Refresh()
    else:
        gauth.Authorize()
           

    if(os != "Windows"):
        gauth.LoadCredentialsFile("./Mx/MxPiDrive/mycreds.txt")
    else:
        gauth.LoadCredentialsFile("./mycreds.txt")
        
    print("Done Authenticating")

    drive = GoogleDrive(gauth)
    return drive
def CopyTechnicalReport(drive,parent,name = "Technical Report"):
    file_list = drive.ListFile({"q":"'"+parent+"' in parents and trashed = false"}).GetList()
    found = False
    for file1 in file_list:
        if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
            if(file1['title'] == name):
                found = True
                    
    if(not found):
        drive.auth.service.files().copy(fileId = TechID, body={"parents":[{"kind": "drive#fileLink",
                                                                   "id": parent}], 'title': name}).execute()
   
def GetFileURL(drive,ProjectName,ParentId = None):
    if(not ParentId):
        ParentId = SFID
    file_list = drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()


    for file1 in file_list:
        if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
            if(file1['title'] == ProjectName):
                return file1['alternateLink']
def GetFileID(drive,FileName,ParentId = None):
    if(not ParentId):
        ParentId = SFID
    file_list = drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()


    for file1 in file_list:
        if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
            if(file1['title'] == FileName):
                return file1['id']
    return None
def GetFiles(drive,ParentId = None):
    if(not ParentId):
        ParentId = SFID
    file_list = drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()
    Files = {}
    for file1 in file_list:
        #print(file1['alternateLink'])
        if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
            Files[file1["title"]] = file1["id"]
    return Files   
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
def DownloadFile(drive,FileId,FileName):
    file1 = drive.CreateFile({'id':FileId})
    file1.GetContentFile(FileName)
def UploadFile(drive,ParentId,FilePath,FileName):
    Id = GetFileID(drive,FileName,ParentId)
    if(Id ==None):
        file2Upload = drive.CreateFile({"parents":[{"id" : ParentId}]})
    else:
        file2Upload = drive.CreateFile({'id':Id})
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
