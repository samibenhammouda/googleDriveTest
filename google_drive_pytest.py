import os 
import sys
import hashlib
import filecmp
import pytest
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from time import sleep


gauth = GoogleAuth()
drive = GoogleDrive(gauth)

folder_id = '1u3GTBlyuvSPU2cPOdghEqdmZP5BEnYxb'
directory = "C:/Users/sami/Desktop/Acronis/google_drive_test/data"

def upload_file():
    """
     Upload file to google drive
    """
    for f in os.listdir(directory):
        filename = os.path.join(directory,f)
        gfile = drive.CreateFile({'parents' : [{'id': folder_id}], 'title': f})
        gfile.SetContentFile(filename)
        print('==> File uploaded !')
        gfile.Upload()
        
def download_file():
    """
    Download file from google drive (file will be downloaded under 'C:/Users/sami/Desktop/Acronis/google_drive_test/' )
    """
    file_list = drive.ListFile({'q' : f"'{folder_id}' in parents and trashed=false"}).GetList()
    for index, file in enumerate(file_list):
        print(index+1, ' ==> File downloaded: ', file['title'])
        file.GetContentFile(file['title'])

def hashfile(g_file):
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()
  
    with open(g_file, 'rb') as f:   
        while True:          
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data) 
    # Convertion to hexadecimal format 
    return sha256.hexdigest()

def test_google_drive():
    print("\n##### Upload file to google drive...")
    upload_file()
    sleep(2)
    print("##### Download file from google drive...")
    download_file()
    sleep(2)
    print("##### Check whether the original and downloaded files are identical")    
    original_file = 'C:/Users/sami/Desktop/Acronis/google_drive_test/data/hello.txt'
    downloaded_file = 'C:/Users/sami/Desktop/Acronis/google_drive_test/hello.txt'
    assert filecmp.cmp(original_file, downloaded_file), pytest.fail("==> Original and downloaded files are not identical")
    print("==> Original and downloaded files are identical")
    

    # Or by using hashing (Secure hash algorithm 256)
    """
    original_file_hash = hashfile('C:/Users/sami/Desktop/Acronis/google_drive_test/data/hello.txt')
    downloaded_file_hash = hashfile('C:/Users/sami/Desktop/Acronis/google_drive_test/hello.txt')
    
    # check whether the two hashes match or not
    if original_file_hash != downloaded_file_hash:
        error_msg = "==> Files are different!"
        print(error_msg)
        print(f"Hash of original file: {original_file_hash}")
        print(f"Hash of downloaded file: {downloaded_file_hash}")
        pytest.fail(error_msg)        
    print("==> Original and downloaded files are same")
    print(f"Hash: {original_file_hash}")
    """