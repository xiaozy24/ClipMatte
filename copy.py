import os
import shutil
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from decolor import process_image
from paste import run_powershell_copy_script
from config import SOURCE_DIR

# 配置参数（根据你的实际路径修改）
TARGET_DIR = os.path.join(os.path.dirname(__file__), "images")  # 目标保存目录
TARGET_FILENAME = "test.png"  # 目标文件名

# 确保目标目录存在，如果不存在则创建
if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

class ScreenshotCopyHandler(FileSystemEventHandler):
    """自定义文件监控处理器，处理新截图的复制逻辑"""
    
    def on_created(self, event):
        """当监控目录中有新文件创建时触发"""
        # 排除目录本身的创建事件，只处理文件
        if not event.is_directory:
            source_file = event.src_path
            # 过滤截图文件（通常截图文件是PNG格式，可根据实际情况调整）
            if source_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                # 等待文件完全写入（避免文件还在保存时复制失败）
                time.sleep(0.5)
                # 拼接目标文件完整路径
                target_file = os.path.join(TARGET_DIR, TARGET_FILENAME)
                
                try:
                    # 复制文件并覆盖已有文件
                    shutil.copy2(source_file, target_file)
                    print(f"截图已复制到: {target_file}")
                    print(f"原文件路径: {source_file}")
                    target = os.path.join(TARGET_DIR, TARGET_FILENAME)
                    process_image(target)
                    threading.Thread(target=run_powershell_copy_script, daemon=True).start()
                except Exception as e:
                    print(f"复制失败: {e}")

def main():
    """主函数：启动监控"""
    # 创建事件处理器
    event_handler = ScreenshotCopyHandler()
    # 创建观察者对象
    observer = Observer()
    # 配置观察者：监控源目录的文件创建事件
    observer.schedule(event_handler, SOURCE_DIR, recursive=False)
    
    print(f"开始监控截图目录: {SOURCE_DIR}")
    print(f"新截图将自动复制到: {os.path.join(TARGET_DIR, TARGET_FILENAME)}")
    print("按 Ctrl+C 停止监控")
    
    # 启动观察者
    observer.start()
    
    try:
        # 保持程序运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # 捕获 Ctrl+C，停止监控
        observer.stop()
        print("\n监控已停止")
    
    # 等待观察者线程结束
    observer.join()

if __name__ == "__main__":
    main()