import os

c=0
def openplay(query,list1):

    for drive in list1:
        for (root, dirs, files) in os.walk(drive, topdown=True):
            print(root)
            print(dirs)
            print(files)
            print('--------------------------------')
            for file in files:
                if query in file.lower():
                    c = 1
                    os.startfile(os.path.join(root, file))
                    del root
                    del dirs
                    del files
                    break
            if c == 1:
                break
        if c == 1:
            break