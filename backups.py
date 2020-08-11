import shutil
import os
import re
import sys
import datetime


# Errors
class NoBackupLocationsSpecified(Exception):
    pass



class Backup:
    '''
    @attrs:
        (list) zippedFiles:
            Automatically set; the list of folders that were zipped in self.zipLocations()
    '''
    def __init__(self):
        self.zippedFiles = []

    @property
    def homeFolder(self):
        '''Get the user's home folder from the first line of the folder.txt file.'''
        content = self.openBackupLocationsFile()
        matched = re.split("/[A-Z]*[a-z]*/$", content[0])
        return matched[0] + "/"

    @property
    def backupLocations(self):
        '''A list of the lines in backup_data/folders.txt.'''
        content = self.openBackupLocationsFile()
        
        return [location.replace("\n", "") for location in content if location != ""]
    
    @property
    def moveToLocation(self):
        '''The path in backup_data/move_to.txt'''
        with open("backup_data/move_to.txt") as moveToLocationFile:
            content = moveToLocationFile.read()
        
        return content.strip()
    
    @property
    def date(self):
        '''The current date; used in self.moveZippedBackupFolder() if self.moveToLocation is not empty'''
        x = datetime.datetime.now()
        x = str(x).split(" ")
        return x[0]
    
    def openBackupLocationsFile(self):
        '''Used in various properties to get the listed folders to backup.'''
        with open("backup_data/folders.txt") as locationsFile:
            if locationsFile.read() == "":
                content = ""
            else:
                content = locationsFile.readlines()
        
        if content == "":
            raise NoBackupLocationsSpecified("\n\nPlease specifiy folders in backup_data/folders.txt to backup. For more information, read the README.\n\n")

        return content

    def zipLocations(self):
        '''Zip all the folders specified in backup_data/folders.txt.'''
        for location in self.backupLocations:
            outputName = re.findall("/[A-Z]*[a-z]*/$", location)
            print("Zipping {}...".format(location))
            shutil.make_archive(self.homeFolder + outputName[0].replace("/", ""), 'zip', location)
            print("Zipped {}.".format(location))

            zippedName = outputName[0].replace("/", "")
            zippedName += ".zip"
            self.zippedFiles.append(zippedName)

        
    def createBackupFolder(self):
        '''Create a folder named "D6-Backup" in the user's home folder.'''
        try:
            os.mkdir(self.homeFolder + "D6-Backup")
        except FileExistsError:
            print("The 'D6-Backup' folder exists. Please delete it and re-run the program.")
            sys.exit()
    
    def moveLocationsToBackupFolder(self):
        '''Move all the zipped folders to D6-Backup, the main backup folder.'''
        for zippedFile in self.zippedFiles:
            print("Moving {}...".format(zippedFile))
            shutil.move(self.homeFolder + zippedFile, self.homeFolder + "D6-Backup/")
            print("Moved {} to {}...".format(zippedFile, self.homeFolder + "D6-Backup/"))
        
    def zipBackupFolder(self):
        '''Zip the D6-Backup folder for easy transport.'''
        print("Zipping D6-Backup...")
        shutil.make_archive(self.homeFolder + "D6-Backup/", "zip", self.homeFolder + "D6-Backup/")
        print("Zipped D6-Backup.")
    
    def removeUnzippedBackupFolder(self):
        '''When zipping a folder, the original folder stays, so we remove D6-Backup after it has been zipped.'''
        print("Removing unzipped backup folder...")
        shutil.rmtree(self.homeFolder + "D6-Backup/")
        print("Removed unzipped backup folder.")
    
    def moveZippedBackupFolder(self):
        '''If self.moveToLocation is not empty, move the folder to the specified location.'''
        if self.moveToLocation == "":
            confirm = "n"
        else:
            confirm = input("Would you like to move this Backup to '{}'? (y/n) ".format(self.moveToLocation))
        

        if confirm == "y":
            shutil.move(self.homeFolder + "D6-Backup.zip", self.moveToLocation)
            os.rename(self.moveToLocation + "D6-Backup.zip", self.moveToLocation + self.date + "-D6-Backup.zip")
        
        print("\n\nBackup Completed!\n\n")

    def __call__(self):
        '''Run all methods'''
        self.zipLocations()
        self.createBackupFolder()
        self.moveLocationsToBackupFolder()
        self.zipBackupFolder()
        self.removeUnzippedBackupFolder()
        self.moveZippedBackupFolder()
    


if __name__ == '__main__':
    bk = Backup()
    bk()