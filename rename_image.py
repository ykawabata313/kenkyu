import glob
import os

path = "image/origin/true/*.jpeg"
i = 1

flist = glob.glob(path)
print(flist)

for file in flist:
    os.rename(file, "image/origin/true/t_{}.jpg".format(i))
    i += 1

lists = glob.glob(path)
print(lists)