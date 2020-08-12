# Backups
A simple command-line backups app

## What it does

It takes a list of specified folders and Zip's them. It then creates a backup folder, called by default "D6-Backup" and moves the Zipped folders to that main backup folder. It then proceeds to Zip the main backup folder, for easy transport. This is the final backup. If you have a path specified in backup_data/move_to.txt, the program will ask if you want to move the final, zipped backup file to that location. This is typically for sending the final backup file to a USB stick. If move_to is set, it will move the file there and rename it to the following format: YYYY-MM-DD-backupFolderName.zip, allowing you to easily compare from past backups.

### Running the app:

1. Download as ZIP and move to a folder of your choice.
2. Navigate to /your/specified/path/backups/ in Terminal
3. Run with *python3 backups.py*

### Setting up your folders

**Setting folders to backup**

In backup_data/folders.txt put an absolute path to a folder you want to backup. For example, if you're on Linux and you want to backup your Documents folder, put "/home/yourusername/Documents/" on a line in that file. Each line contains one absolute path; and you can add as many folders as you like.

**Setting the optional moveTo location**

The moveTo location is an optional path to a folder where you want to store the final backup. This is typically used to put the path of a USB stick in the backup_data/move_to.txt file. The program will ask if you want to move the final backup to this location.

If moveTo is not set (when the move_to.txt file is empty), the final backup will be placed in your home folder.


## Modifying backups.py

Every method is documented and separated following, as close as possible, to the Single Responsibility Principle (SRP [Wikipedia](https://en.wikipedia.org/wiki/Single-responsibility_principle)) to allow you to easily modify the script.
