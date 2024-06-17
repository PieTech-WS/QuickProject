from Includes.org.cora.CoraOS.Essentials.data.json.DataStorage import DStorage
from Includes.org.cora.CoraOS.Essentials.fs.Type.basictype import Folder, FolderNotFound, TypeERROR
import os
CurrentWorkDir = os.getcwd()
print(CurrentWorkDir)
try:
    Folder(".quickproject")
except FolderNotFound or TypeERROR:
    