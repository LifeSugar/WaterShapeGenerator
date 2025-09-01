# Extension 系统集成指南

本插件已经配置好了 Blender Extension 系统支持，可以通过多种方式安装和更新。

## 自动发布流程

### 1. 设置 GitHub 仓库

```bash
# 初始化 Git 仓库（如果还没有）
git init
git add .
git commit -m "初始版本"

# 添加远程仓库
git remote add origin https://github.com/LifeSugar/WaterShapeGenerator.git
git push -u origin main
```

### 2. 发布新版本

使用提供的版本管理脚本：

```bash
# 更新版本号并创建发布
python update_version.py 1.0.1
```

这个脚本会：
- 更新 `blender_manifest.toml` 中的版本号
- 创建 Git 提交
- 创建版本标签
- 推送到 GitHub（可选）

### 3. 自动构建

当推送版本标签时，GitHub Actions 会自动：
- 构建插件包
- 创建 GitHub Release
- 上传可下载的 zip 文件

## 用户安装方式

### 方式一：通过 Blender Extension 系统（推荐）

1. 打开 Blender 4.2+
2. 进入 **Edit > Preferences > Get Extensions**
3. 搜索 "水体生成器" 或 "WaterShapeGenerator"
4. 点击安装

### 方式二：手动安装

1. 访问 GitHub Releases 页面
2. 下载最新的 `watershapegenerator-x.x.x.zip` 文件
3. 在 Blender 中：
   - **Edit > Preferences > Add-ons**
   - 点击 **Install**
   - 选择下载的 zip 文件
   - 启用插件

## 更新检查

用户可以通过以下方式检查和安装更新：

1. **Blender Extension 系统**：
   - **Edit > Preferences > Get Extensions**
   - 在已安装的扩展中查看可用更新

2. **手动检查**：
   - 访问 GitHub Releases 页面
   - 下载并安装新版本

## 开发者发布清单

每次发布新版本时：

1. ✅ 测试所有功能
2. ✅ 更新 CHANGELOG.md
3. ✅ 运行 `python update_version.py x.x.x`
4. ✅ 确认 GitHub Actions 构建成功
5. ✅ 测试从 Release 下载的包
6. ✅ 更新文档（如有需要）

## 文件结构说明

```
WaterShapeGenerator/
├── blender_manifest.toml      # Extension 配置
├── __init__.py                # 插件入口
├── includes/                  # 核心代码
├── assets/                    # 资源文件
├── .github/workflows/         # CI/CD 配置
├── update_version.py          # 版本管理工具
└── README.md                  # 项目说明
```

## 许可证信息

- **许可证**: GPL-3.0-or-later
- **兼容性**: Blender 4.2.0+
- **平台支持**: Windows, macOS, Linux
