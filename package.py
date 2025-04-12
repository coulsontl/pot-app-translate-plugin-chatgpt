import json
import zipfile
import os
import sys
import tempfile
import shutil

def create_potext_package(model_type='chatgpt'):
    if model_type not in ['chatgpt', 'grok']:
        print(f"错误: 不支持的模型类型 {model_type}，只支持 'chatgpt' 或 'grok'")
        return False
    
    # 根据模型类型选择配置文件
    info_file = f'info.{model_type}.json'
    model_specific_js = f'main.{model_type}.js'
    
    # 确保核心文件存在
    core_js = 'main.js'
    if not os.path.exists(core_js):
        print(f"错误: 核心JavaScript文件 {core_js} 不存在!")
        return False
    
    # 确保模型特定文件存在
    if not os.path.exists(model_specific_js):
        print(f"错误: 模型特定JavaScript文件 {model_specific_js} 不存在!")
        return False
    
    # 读取info.json文件
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            info = json.load(f)
    except FileNotFoundError:
        print(f"错误: 配置文件 {info_file} 不存在!")
        return False
    
    # 提取id和icon
    plugin_id = info['id']
    icon_file = info['icon']
    
    # 输出信息
    print(f"正在打包插件: {plugin_id}")
    print(f"使用图标: {icon_file}")
    print(f"使用配置文件: {info_file}")
    print(f"使用模型特定文件: {model_specific_js}")
    print(f"使用核心文件: {core_js}")
    
    # 创建.potext文件（实际上是一个zip文件）
    output_filename = f"{plugin_id}.potext"
    
    # 检查输出文件是否已存在
    if os.path.exists(output_filename):
        print(f"警告: 文件 {output_filename} 已存在，将被覆盖")
    
    # 检查要打包的文件是否存在
    if not os.path.exists(icon_file):
        print(f"错误: 图标文件 {icon_file} 不存在!")
        return False
    
    # 创建临时目录用于处理文件
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"创建临时目录: {temp_dir}")
        
        # 合并JavaScript文件
        temp_js_file = os.path.join(temp_dir, 'main.js')
        with open(temp_js_file, 'w', encoding='utf-8') as outfile:
            # 首先写入核心文件
            with open(core_js, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write('\n\n')
            
            # 然后写入模型特定文件
            with open(model_specific_js, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
        
        print(f"合并JavaScript文件: {core_js} + {model_specific_js} -> {temp_js_file}")
        
        # 创建zip文件 (使用'w'模式会自动覆盖已存在的文件)
        with zipfile.ZipFile(output_filename, 'w') as zipf:
            # 将配置文件写入为 info.json
            zipf.write(info_file, 'info.json')
            print(f"- 添加文件: {info_file} -> info.json")
            
            # 将合并后的JS文件写入为 main.js
            zipf.write(temp_js_file, 'main.js')
            print(f"- 添加文件: {temp_js_file} -> main.js")
            
            # 添加图标文件
            zipf.write(icon_file)
            print(f"- 添加文件: {icon_file}")
    
    print(f"打包完成: {output_filename}")
    return True

def package_all():
    """打包所有支持的模型类型"""
    supported_models = ['chatgpt', 'grok']
    success_count = 0
    
    print(f"将打包以下插件: {', '.join(supported_models)}")
    
    for model in supported_models:
        print(f"\n===== 开始打包 {model} 插件 =====")
        if create_potext_package(model):
            success_count += 1
    
    print(f"\n===== 打包总结 =====")
    print(f"共打包了 {success_count}/{len(supported_models)} 个插件")
    
    if success_count == len(supported_models):
        print("所有插件打包成功!")
        return True
    else:
        print("部分插件打包失败，请检查错误信息")
        return False

if __name__ == "__main__":
    try:
        # 如果有命令行参数，使用参数指定的模型类型
        if len(sys.argv) > 1:
            model_type = sys.argv[1].lower()
            create_potext_package(model_type)
        else:
            # 没有参数时打包所有插件
            package_all()
    except KeyboardInterrupt:
        print("\n打包过程被用户中断")
    except Exception as e:
        print(f"\n打包过程出错: {e}") 