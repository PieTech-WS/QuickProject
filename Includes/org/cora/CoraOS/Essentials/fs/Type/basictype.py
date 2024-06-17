import io
import mimetypes
import os
import time


class FileOps:
    def __init__(self, abspath: str, mode: str, encoding: str = "utf-8"):
        self.abspath = abspath
        self.mode = mode
        self.encoding = encoding

    def Write(self, content):
        """
        Supported Modes:
        w
        w+
        r+
        a
        a+
        """
        with open(self.abspath, self.mode, encoding=self.encoding) as a:
            a.write(content)

    def bWrite(self, content):
        with open(self.abspath, self.mode) as a:
            a.write(content)

    def Read(self):
        """
        Supported Modes:
        r
        r+
        w+
        a+
        :return FileContent
        """
        with open(self.abspath, self.mode, encoding=self.encoding) as a:
            content: bytes = a.read()
        return content

    def bRead(self):
        """
        Supported Modes:
        r
        r+
        w+
        a+
        :return FileContent
        """
        with open(self.abspath, self.mode) as a:
            content: bytes = a.read()
        return content


# coraos.fs.type.File
def CreateFile(path: str):
    try:
        return File(path)
    except FileNotFound:
        with open(path, "w") as a:
            a.write("")
        return File(path)
    except TypeERROR:
        raise TypeERROR("There is already a folder with the same name.")


class FileIO_NOT_FOUND(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class FileIO_MODE_ERROR(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class File_SecureMove_Check_ERROR(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class File:
    """
    File type
    Basic type of file.
    """

    def __init__(self, path: str):
        if os.path.exists(path):
            if not os.path.isfile(path):
                raise TypeERROR("{} is not a file.".format(path))
            else:
                pass
        else:
            raise FileNotFound("File {} can't be found.".format(path))
        self.Content = None
        self.FileIO = None
        self.FileIO_info = None
        self.Path = os.path.abspath(path)
        self.Parent = os.path.dirname(self.Path)
        self.Name = os.path.basename(self.Path)
        self.Type = mimetypes.guess_type(self.Path)[0]
        stats = os.stat(self.Path)
        self.Size = stats.st_size
        self.CreatedTime = time.localtime(stats.st_mtime)

    def Open(self, mode: str = "r+", encoding: str = "utf-8"):
        self.FileIO = FileOps(self.Path, mode, encoding)
        self.FileIO_info = {"Mode": mode, "Encoding": encoding}

    def LoadContent(self):
        self.Content = self.FileIO.Read()

    def Write(self, content):
        self.FileIO.Write(content)

    def Move(self, pathTo: str, overwrite: bool = False, returnFile: bool = False, verify: bool = True):
        """
        coraos.fs.type.file.File.Move
        Move target file to target path.
        """
        if self.FileIO is None:
            raise FileIO_NOT_FOUND("FileIO is not open. Please use 'File.Open' to open a FileIO")
        try:
            self.LoadContent()
        except io.UnsupportedOperation:
            raise FileIO_MODE_ERROR("FileIO Mode is error. This operation requires w+ or r+ mode, but FileIO is "
                                    "currentlyin {}.".format(self.FileIO_info["Mode"]))
        targetPath = Folder(pathTo)
        # check files
        result = targetPath.checkFile(self.Name)
        if result is not None:
            if overwrite:
                targetFile = result
            else:
                raise File_SecureMove_Check_ERROR("There is already a file with the same name in the target "
                                                  "directory, but overwrite is set to False")
        else:
            targetFile = targetPath.newFile(self.Name)
        targetFile.Open()
        targetFile.Write(self.Content)
        if returnFile:
            return targetFile

    def sMove(self, pathTo: str, overwrite: bool = False, returnFile: bool = False, verify: bool = True):
        """
        coraos.fs.type.file.File.sMove
        Move target file to target path in binary.
        Using independent FileOps.
        """
        FileOps_ = FileOps(self.Path, "rb")
        Content = FileOps_.bRead()
        targetPath = Folder(pathTo)
        # check files
        result = targetPath.checkFile(self.Name)
        if result is not None:
            if overwrite:
                targetFile = result
            else:
                raise File_SecureMove_Check_ERROR("There is already a file with the same name in the target "
                                                  "directory, but overwrite is set to False")
        else:
            targetFile = targetPath.newFile(self.Name)
        FileOps__ = FileOps(targetFile.Path, "rb+")
        FileOps__.bWrite(Content)
        Content_: bytes = FileOps__.bRead()
        Content: bytes = FileOps_.bRead()
        import hashlib
        hash = hashlib.md5()
        hash.update(Content)
        hash_ = hash.hexdigest()
        hash2 = hashlib.md5()
        hash2.update(Content_)
        hash__ = hash2.hexdigest()
        if hash__ != hash_:
            raise Move_VerifyERROR("Cannot verify moved file.Try again.")
        if returnFile:
            return targetFile


class Move_VerifyERROR(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class TypeERROR(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class FileNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


# coraos.fs.type.Folder
def CreateFolder(path: str):
    try:
        Folder(path)
    except FolderNotFound:
        os.mkdir(path)
    except TypeERROR:
        raise TypeERROR("There is already a file with the same name")


class Folder:
    def __init__(self, path: str):
        if os.path.exists(path):
            if not os.path.isdir(path):
                raise TypeERROR("{} is not a folder.".format(path))
        else:
            raise FolderNotFound("Folder {} can't be found.".format(path))
        self.Path = os.path.abspath(path)

    def is_empty(self):
        if len(os.listdir(self.Path)) == 0:
            return True

    def searchFile(self, keyword: str, childfolder: bool = False):
        """
        Search in childfolder is not available.
        """
        files = os.listdir(self.Path)
        result = {}
        for i in files:
            if keyword in i:
                path = "{}/{}".format(self.Path, i)
                try:
                    result[i] = Folder(path)
                except TypeERROR:
                    result[i] = File(path)
        return result

    def checkFile(self, name: str):
        result: dict = self.searchFile(name)
        for i in result.keys():
            if i == name:
                return File("{}/{}".format(self.Path, name))
        return None

    def newFile(self, name: str):
        return CreateFile("{}/{}".format(self.Path, name))

    def newChildFolder(self, name):
        try:
            Folder("{}/{}".format(self.Path, name))
        except FolderNotFound:
            os.mkdir("{}/{}".format(self.Path, name))


class FolderNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
