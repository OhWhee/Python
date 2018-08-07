import os

class File:
    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.start = 0
        
    def write(self, text):
        self.file_object.write(text)
        self.file_object.close()
    
    def __add__(self, second):
        with open(self.path + os.path.splitext(self.name)[0] + os.path.splitext(second.name)[0]+".txt", "w") as obj_f:
            with open(self.path+self.name, "r") as f:
                for lines in f:
                    obj_f.writelines(lines)
        with open(self.path + os.path.splitext(self.name)[0] + os.path.splitext(second.name)[0]+".txt", "a") as obj_f:
            with open(second.path+second.name, "r") as f_second:
                for lines in f_second:
                    obj_f.writelines(lines)
        new_obj = File(self.path, name=os.path.splitext(self.name)[0] + os.path.splitext(second.name)[0]+".txt")
        return new_obj
    
    def __iter__(self):
        return self
    
    def __next__(self):

        with open(self.path + os.path.splitext(self.name)[0] + ".txt", "r") as lines:
            lines.seek(self.start)
            text_line = lines.readline()
            if not text_line:
                self.start = 0
                raise StopIteration
            
            self.start = lines.tell()
            return text_line


    def __str__(self):
        return str(self.path + self.name)
