import cv2
import numpy as np
import os

def process_image(input_path):
    # 1. 路径检查
    input_path = os.path.abspath(input_path)
    if not os.path.exists(input_path):
        print(f"错误：输入文件不存在: {input_path}")
        return

    # 2. 构造输出路径（使用脚本所在目录的相对 pimages 文件夹）
    base_dir = os.path.abspath(os.path.dirname(__file__))
    output_dir = os.path.join(base_dir, "pimages")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已创建文件夹: {output_dir}")

    file_name = os.path.basename(input_path)
    name_only = os.path.splitext(file_name)[0]
    output_path = os.path.join(output_dir, f"p{name_only}.png")

    # 3. 读取图片
    img = cv2.imread(input_path)
    if img is None:
        print(f"错误：无法读取图片内容，请检查格式。")
        return

    print(f"已加载图片: {file_name} ({img.shape[1]}x{img.shape[0]})")
    print("操作指南：在弹出的窗口中 [左键点击] 目标颜色。点击后窗口将自动处理。")

    # 4. 核心逻辑：点击即处理
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            target_color = img[y, x].tolist()
            print(f"捕获到颜色 (BGR): {target_color}")
            
            # 执行透明化处理
            b, g, r = cv2.split(img)
            alpha = np.ones(b.shape, dtype=b.dtype) * 255
            
            # 容差设为 15
            lower = np.array([max(0, c - 15) for c in target_color])
            upper = np.array([min(255, c + 15) for c in target_color])
            
            # 建立遮罩
            mask = cv2.inRange(img, lower, upper)
            alpha[mask > 0] = 0
            
            result = cv2.merge((b, g, r, alpha))
            
            # 5. 尝试保存并强制检查结果
            success = cv2.imwrite(output_path, result)
            if success:
                print(f"成功保存到: {output_path}")
            else:
                print(f"保存失败！请检查 {output_dir} 是否有写入权限。")
            
            # 处理完后关闭
            cv2.destroyAllWindows()

    win_name = "Image Picker"
    cv2.namedWindow(win_name)
    cv2.imshow(win_name, img)
    cv2.setMouseCallback(win_name, click_event)

    # 保持窗口开启
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Use a project-relative test image path
    script_dir = os.path.abspath(os.path.dirname(__file__))
    target = os.path.join(script_dir, "images", "test.png")
    process_image(target)