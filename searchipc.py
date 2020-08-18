import os
def searching(query,list1):
    searchedlist = []
    searchedlistpath = []
    l=[]
    for drive in list1:
        for (root, dirs, files) in os.walk(drive, topdown=True):
            print(root)
            print(dirs)
            print(files)
            print('--------------------------------')
            for folder in dirs:
                if query in folder.lower():
                    searchedlist.append(folder)
                    searchedlistpath.append(root)
            for file in files:
                if query in file.lower():
                    searchedlist.append(file)
                    searchedlistpath.append(root)
            del root
            del dirs
            del files
    l.append(searchedlist)
    l.append(searchedlistpath)
    return l