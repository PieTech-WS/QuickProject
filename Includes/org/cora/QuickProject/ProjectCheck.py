from Includes.org.cora.CoraOS.Essentials.fs.Type.basictype import Folder, FolderNotFound, TypeERROR
from Includes.org.cora.CoraOS.Essentials.data.json.DataStorage import DStorage
import sys
from . import VersionLevel
def check(LogUtil):
    try:
        projectFolder = Folder(".quickproject")
    except FolderNotFound or TypeERROR:
        LogUtil.error("QuickProject.LangPack.NotAProject")
    settings = projectFolder.checkFile("settings.json")
    if settings == None:
        LogUtil.error("QuickProject.LangPack.NotAnAvailableProject")
        sys.exit()
    else:
        Settings = DStorage(settings.Path, False)
        try:
            projVer = Settings.Value("QuickProject.VersionLevel")
            Settings.close()
        except KeyError:
            LogUtil.error("QuickProject.LangPack.BrokenSettingsFile")
        del Settings
        if projVer not in VersionLevel.SupportLevel:
            LogUtil.error("QuickProject.LangPack.UnsupportedProjectVersion")

    