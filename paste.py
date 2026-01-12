import subprocess
import os
from config import PS_PATH_NEW, PS_PATH_OLD

def run_powershell_copy_script():
    """
    直接指定PowerShell绝对路径
    """
    # 1. 使用脚本相对路径
    ps1_abs_path = os.path.join(os.path.dirname(__file__), "CopyFileToClipboard.ps1")

    # 2. 校验PS1脚本是否存在
    if not os.path.exists(ps1_abs_path):
        print(f"错误：PS1脚本不存在 → {ps1_abs_path}")
        print(f"请检查：是否将 CopyFileToClipboard.ps1 放在 {os.path.dirname(__file__)} 目录下")
        return False
    
    # 3. 直接指定PowerShell绝对路径
    ps_paths = [
        PS_PATH_NEW,
        PS_PATH_OLD
    ]
    ps_exe = None
    for path in ps_paths:
        if os.path.exists(path):
            ps_exe = path
            break
    
    if not ps_exe:
        print("错误：未找到PowerShell可执行文件！")
        print("请检查以下路径是否存在：")
        for path in ps_paths:
            print(f"   - {path}")
        return False
    
    try:
        # 4. 构造调用指令
        cmd = [
            ps_exe,  # 直接用PowerShell绝对路径
            "-ExecutionPolicy", "Bypass",
            "-NoProfile",
            "-File", ps1_abs_path
        ]
        
        # 5. 打印执行指令（便于排查）
        print(f"执行指令：{' '.join(cmd)}")
        
        # 6. 执行指令
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            shell=False
        )
        
        # 7. 处理结果
        if result.returncode == 0:
            print("Python调用PS1脚本成功！")
            print("PS1脚本输出：")
            print(result.stdout)
            return True
        else:
            print(f"Python调用PS1脚本失败！")
            print(f"错误输出：{result.stderr}")
            return False
            
    except Exception as e:
        print(f"调用过程异常：{str(e)}")
        return False
    