# 新手 GitHub Pages 部署教程
> 专为 Git 小白设计的最简化教程

## 🎯 目标：10分钟内把网站上线

### 方案A：GitHub 网页版（最简单）

#### 步骤1：创建仓库（2分钟）
1. 打开 [GitHub.com](https://github.com)，登录账号
2. 点击右上角绿色按钮 **"New"**
3. 填写仓库名：`my-website`
4. 选择 **"Public"**
5. 勾选 **"Add a README file"**
6. 点击 **"Create repository"**

#### 步骤2：上传网站文件（3分钟）
1. 在刚创建的仓库页面，点击 **"uploading an existing file"**
2. 拖拽你的所有网站文件到页面（或点击选择文件）
3. 在下方输入提交信息：`上传我的网站`
4. 点击绿色按钮 **"Commit changes"**

#### 步骤3：开启 GitHub Pages（2分钟）
1. 在仓库页面点击 **"Settings"** 标签
2. 滚动到左侧菜单，点击 **"Pages"**
3. 在 "Source" 选择 **"Deploy from a branch"**
4. Branch 选择 **"main"**，文件夹选择 **"/ (root)"**
5. 点击 **"Save"**

#### 步骤4：访问你的网站（3分钟）
- 等待1-2分钟，刷新 Pages 页面
- 会显示：`Your site is published at https://你的用户名.github.io/my-website`
- 点击链接就能看到你的网站！

---

### 方案B：使用 GitHub Desktop（图形界面）

#### 下载安装
1. 访问 [desktop.github.com](https://desktop.github.com)
2. 下载并安装 GitHub Desktop
3. 使用 GitHub 账号登录

#### 操作步骤
1. **Clone repository**: 选择你在 GitHub 创建的仓库
2. **添加文件**: 把网站文件复制到本地仓库文件夹
3. **Commit**: 在 GitHub Desktop 中写提交信息，点击 "Commit to main"
4. **Push**: 点击 "Push origin"

---

### 方案C：一键脚本（适合反复更新）

#### Windows 用户
创建 `一键部署.bat` 文件：
```batch
@echo off
echo 🚀 正在部署网站...

REM 添加所有文件
git add .

REM 提交更改
set /p message="请输入更新说明（直接回车使用默认）: "
if "%message%"=="" set message=更新网站 %date% %time%
git commit -m "%message%"

REM 推送到GitHub
git push origin main

echo ✅ 部署完成！请等待1-2分钟然后访问网站
pause
```

#### Mac 用户
创建 `一键部署.command` 文件：
```bash
#!/bin/bash
cd "$(dirname "$0")"

echo "🚀 正在部署网站..."

git add .

read -p "请输入更新说明（直接回车使用默认）: " message
if [ -z "$message" ]; then
    message="更新网站 $(date)"
fi

git commit -m "$message"
git push origin main

echo "✅ 部署完成！请等待1-2分钟然后访问网站"
```

---

## 🆘 遇到问题时的自救方法

### 常见错误及解决方案

#### 错误1：`git push` 要求输入用户名密码
**解决**：
1. 在 GitHub 设置中生成 Personal Access Token
2. 用户名输入 GitHub 用户名
3. 密码输入生成的 token（不是GitHub密码）

#### 错误2：文件没有更新
**解决**：
1. 等待5分钟（GitHub有时会延迟）
2. 按 Ctrl+F5 强制刷新浏览器
3. 检查是否真的推送成功

#### 错误3：网站显示404
**解决**：
1. 确保有 `index.html` 文件
2. 文件名不要包含中文或特殊字符
3. 检查 Settings → Pages 是否正确配置

---

## 🎓 学习进阶路线

### 第一周：基础操作
- [ ] 学会用 GitHub 网页上传文件
- [ ] 学会开启 GitHub Pages
- [ ] 学会修改文件并重新上传

### 第二周：命令行入门
- [ ] 安装 Git
- [ ] 学会 `git clone`
- [ ] 学会 `git add . && git commit -m "消息" && git push`

### 第三周：进阶操作
- [ ] 学会查看 `git status`
- [ ] 学会解决简单冲突
- [ ] 学会使用分支

---

## 📞 求助指南

### 什么时候可以自己解决
- 网站不更新 → 等5分钟，刷新浏览器
- 上传文件失败 → 检查文件大小（GitHub限制100MB）
- 404错误 → 检查文件名是否正确

### 什么时候需要求助
- 出现红色错误信息
- 第一次设置遇到问题
- 需要高级功能（自定义域名等）

### 高效求助的方式
1. **截图错误信息**：把完整的错误截图发给我
2. **说明操作步骤**：告诉我你做了什么
3. **提供仓库链接**：让我能直接看到问题

---

## 💪 信心建设

### 好消息
- **GitHub Desktop** 图形界面很友好
- **网页版操作** 直观易懂
- **一键脚本** 减少重复操作
- **我随时在线** 帮你解决问题

### 现实预期
- **前3次部署** 可能需要求助
- **第4-10次** 基本能独立操作
- **10次之后** 就是肌肉记忆了

### 学习时间
- **网页版** → 30分钟上手
- **GitHub Desktop** → 1小时上手  
- **命令行** → 1周基本熟练

---

## 🚀 立即开始

**我的建议：先用方案A（网页版）试一次，成功后再考虑其他方案。**

记住：**每个程序员都是从不会Git开始的**，你只需要迈出第一步！

有任何问题随时问我，我会一步步指导你！ 😊