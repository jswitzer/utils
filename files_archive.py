import sys
import os
import stat

class DirectoryWalker(object):
    def __init__(self):
        pass
    def init_level(self, level):
        if level in self.level_info:
            return
        self.level_info[level] = {'size':0, 'paths':{}}

    def walk(self, path):
        self.level_info = {}
        def find_readmes(root):
            children = os.listdir(root)
            if "README" in children:
                try:
                    with open(os.path.join(root, "README"), "r") as f:
                        for line in f:
                            if line.startswith('FILES_ARCHIVE_LEVEL'):
                                level = int(line.split()[1].strip())
                                self.init_level(level)
                                self.level_info[level]['paths'].append(root)
                                return True
                except:
                    pass

            for f in children:
                 fpath = os.path.join(root, f)
                 if stat.S_ISDIR(os.stat(fpath).st_mode):
                     find_readmes(fpath)

        find_readmes(path)

    def scan(self, path):
        def size_get_recursive(root):
            total_size = 0
            for root, dirs, files in os.walk(root):
                for f in files:
                    fp = os.path.join(root, f)
                    total_size += os.stat(fp).st_size
            return total_size

        self.walk(path)
        for ln,li in self.level_info.items():
            li['size'] = 0 
            for d in li['paths']:
                li['size'] += size_get_recursive(d)
        
dw = DirectoryWalker()
dw.scan(sys.argv[1])
print dw.level_info
