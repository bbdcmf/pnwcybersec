# Searches binaries_dir for any zip files. If any are found, it attempts to extract those zip files to extract_dir. From there, it then searches extract_dir for any windows executables. If any are found, it then takes the hash of that executable file, renames the file to it's hash and then copies the file to exe_dir

import pyzipper, os, shutil, hashlib

rootdir = '/run/media/bbdcmf/T7/theZoo/'
binaries_dir = rootdir+'Binaries/'
extract_dir = rootdir+'Extracted/'
exe_dir = rootdir+'exes/'
passwd = 'infected'
            
def unZip():
    dirs = os.listdir(binaries_dir)
    for directory in dirs:
        items = os.listdir(binaries_dir+directory)
        for item in items:
            # If the item is a .zip file
            if(item.endswith('.zip')):
                try:
                    # Attempt to extract the zip file
                    with pyzipper.AESZipFile(binaries_dir+directory+'/'+item, 'r') as zip_file:
                        zip_file.pwd = passwd.encode()
                        zipOutputPath = extract_dir+directory+'/'
                        # Create a new directory and extract the zip file there
                        if(not os.path.isdir(zipOutputPath)):
                            os.mkdir(zipOutputPath)
                        zip_file.extractall(zipOutputPath)
                # Print any errors
                except Exception as e:
                    print(e)
                    print(binaries_dir+directory+'/'+item)
                    pass

def copyExe(item):
    try:
        with open(item, 'rb') as exe:
            if(exe.read(2) == b'MZ'):
                file_hash = hashlib.sha256(exe.read()).hexdigest()
                shutil.copyfile(item, exe_dir+file_hash)
    except Exception as e:
        print(e)
        print(item)
        pass

def getExes():
    dirs = os.listdir(extract_dir)
    for directory in dirs:
        items = os.listdir(extract_dir+directory)
        for item in items:
            filePath = extract_dir+directory+'/'+item
            # If the item is a file
            if(os.path.isfile(filePath)):
                # If file is a windows executable: get the file hash, rename the file to it's hash, and copy the file
                copyExe(filePath)
            # If the item is a directory
            elif(os.path.isdir(filePath)):
                innerfiles = os.listdir(filePath+'/')
                for innerfile in innerfiles:
                    innerFilePath = filePath+'/'+innerfile
                    # If the item within the director is a file
                    if(os.path.isfile(innerFilePath)):
                        # If file is a windows executable: get the file hash, rename the file to it's hash, and copy the file
                        copyExe(innerFilePath)
                        
def main():
    unZip()
    getExes()
    
if(__name__ == "__main__"):
    main()
