import os

def find_database(dbname):
    cwd = os.getcwd()
    while True:
        dbpath = os.path.join(cwd,dbname)
        if os.path.isfile(dbpath):
            return dbpath

        nwd = os.path.dirname(cwd)
        
        if (nwd == cwd or not os.path.isdir(nwd)):
                return None

        cwd = nwd


database = find_database('taqi.db')
wiki_root = os.path.dirname(database)

print wiki_root

                       
