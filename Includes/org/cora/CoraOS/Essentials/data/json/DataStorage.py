import json


class DStorage:
    def __init__(self, file: str, autoSave: bool):
        self.datafile = open(file, "w+", encoding="utf-8")
        self.content: dict = json.load(self.datafile)
        self.autoSave = autoSave
        
    def autoSaving(self):
        if self.autoSave:
            self.save()
            
    def close(self):
        self.datafile.close()
    
    def save(self):
        json.dump(self.content, self.datafile, indent=4)
        
    def Value(self, key: str):
        return self.content[key]
    
    def chValue(self, key: str, content):
        self.content[key] = content
        self.autoSaving()
        
    def newKey(self, name):
        self.content[name] = {}
    
    def reKey(self, key: str, new_key: str):
        self.content[new_key] = self.content[key]
        self.content.pop(key)
        self.autoSaving()
    
    
    