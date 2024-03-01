import os
import sys
sys.path.append('/usr/people/hidaka/.local/lib/python3.9/site-packages')
sys.path.append('/usr/lib/python3.9/site-packages')
sys.path.append('/usr/lib64/python3.9/site-packages')
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

class GoogleDriveFacade:
    
    def __init__(self, setting_path: str='/usr/people/hidaka/settings.yaml'):
        gauth = GoogleAuth(setting_path)
        gauth.LocalWebserverAuth()

        self.drive = GoogleDrive(gauth)

    def create_folder(self, folder_name):
        ret = self.check_files(folder_name)
        if ret:
            folder = ret
            print(f"{folder['title']}: exists")
        else:   
            folder = self.drive.CreateFile(
                {
                    'title': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
            )
            folder.Upload()

        return folder

    def check_files(self, folder_name,):
        query = f'title = "{os.path.basename(folder_name)}"'

        list = self.drive.ListFile({'q': query}).GetList()
        if len(list)> 0:
            return list[0]
        return False

    def upload(self, 
               local_file_path: str,
               save_folder_name: str = 'sample'
        ):
        
        if save_folder_name:
            folder = self.create_folder(save_folder_name)
        
        file = self.drive.CreateFile(
            {
                'title':os.path.basename(local_file_path),
                'parents': [
                    {'id': folder["id"]}
                ]
            }
        )
        file.SetContentFile(local_file_path)
        file.Upload()
        
        drive_url = f"https://drive.google.com/uc?id={str( file['id'] )}" 
        return drive_url
    
def upload(local_file_path,save_folder_name=''):
    g = GoogleDriveFacade()
    g.upload(
        local_file_path,
        save_folder_name
    )
