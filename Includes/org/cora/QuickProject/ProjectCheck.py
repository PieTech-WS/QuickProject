from Includes.org.cora.CoraOS.Essentials.fs.Type.basictype import Folder, FolderNotFound, TypeERROR
from Includes.org.cora.CoraOS.Essentials.data.json.DataStorage import DStorage
import sys
from ..CoraOS.Essentials.i18n.LangPackContent import LangPackContent
from . import VersionLevel
def check(LogUtil):
    LangPackObj = LangPackContent()
    try:
        projectFolder = Folder(".quickproject")
    except FolderNotFound or TypeERROR:
        LogUtil.error(LangPackObj.Content("QuickProject.LangPack.NotAProject"))
    settings = projectFolder.checkFile("settings.json")
    if settings == None:
        LogUtil.error(LangPackObj.Content("QuickProject.LangPack.NotAnAvailableProject"))
        sys.exit()
    else:
        Settings = DStorage(settings.Path, False)
        try:
            projVer = Settings.Value("QuickProject.VersionLevel")
            Settings.close()
        except KeyError:
            LogUtil.error(LangPackObj.Content("QuickProject.LangPack.BrokenSettingsFile"))
        del Settings
        if projVer not in VersionLevel.SupportLevel:
            LogUtil.error(LangPackObj.Content("QuickProject.LangPack.UnsupportedProjectVersion"))

