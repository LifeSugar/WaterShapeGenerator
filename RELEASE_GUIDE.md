# 发布到 Blender Extension 系统

## 快速开始

你的插件现在已经完全准备好接入 Blender Extension 系统！

### 1. 立即发布（推荐）

```bash
# 验证插件结构
python validate_plugin.py

# 创建新版本并发布
python update_version.py 1.0.0
```

### 2. GitHub 设置

确保你的 GitHub 仓库已经设置好：

```bash
# 如果还没有推送到 GitHub
git remote add origin https://github.com/LifeSugar/WaterShapeGenerator.git
git push -u origin main
```

### 3. 自动发布流程

当你运行 `update_version.py` 并推送标签时：
1. GitHub Actions 自动构建插件包
2. 创建 Release 页面
3. 上传可下载的 zip 文件
4. 用户可以从 Release 页面下载安装

## 用户如何安装

### 方式一：直接下载（当前可用）
1. 访问：https://github.com/LifeSugar/WaterShapeGenerator/releases
2. 下载最新的 `watershapegenerator-x.x.x.zip`
3. 在 Blender 中安装：**Edit > Preferences > Add-ons > Install**

### 方式二：Extension 系统（未来可用）
当 Blender Extension 系统支持第三方仓库时：
1. **Edit > Preferences > Get Extensions**
2. 搜索 "水体生成器"
3. 一键安装和更新

## 当前状态

✅ **已完成**：
- Extension 系统配置文件 (`blender_manifest.toml`)
- 自动构建流程 (GitHub Actions)
- 版本管理工具
- 插件验证脚本
- 完整的中文支持

🔄 **即将实现**：
- Blender 官方 Extension 市场支持
- 自动更新检查

## 下一步行动

1. **立即发布**：运行 `python update_version.py 1.0.0`
2. **测试安装**：从 GitHub Release 下载测试
3. **推广使用**：分享 GitHub 链接给用户
4. **等待官方**：关注 Blender Extension 系统的最新进展

## 联系和支持

- **GitHub**: https://github.com/LifeSugar/WaterShapeGenerator
- **Issues**: 在 GitHub 上报告问题和建议
- **更新**: 通过 GitHub Releases 发布更新

你的插件现在完全准备好了！🎉
