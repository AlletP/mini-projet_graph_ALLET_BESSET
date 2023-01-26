import bz2,shutil
import os



for file in os.listdir():
    if file != os.path.basename(__file__):
        with bz2.BZ2File(file) as source, open(file[:-4],"wb") as dest: shutil.copyfileobj(source,dest) # don't forgot to move files to the good repertory
