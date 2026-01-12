import getpass
username = getpass.getuser()
SOURCE_DIR = r"C:\\Users\\{}\\Pictures\\Screenshots".format(username) # 系统默认截图保存路径
PS_PATH_NEW = r"C:\\Program Files\\PowerShell\\7\\pwsh.exe" # 新版PowerShell默认路径
PS_PATH_OLD = r"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" # 旧版PowerShell默认路径