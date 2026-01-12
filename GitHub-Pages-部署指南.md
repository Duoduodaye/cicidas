# GitHub Pages 部署指南

> 从本地网页开发到 GitHub Pages 托管的完整教程

## 目录
- [1. 本地开发准备](#1-本地开发准备)
- [2. GitHub 仓库创建](#2-github-仓库创建)
- [3. 推送代码到 GitHub](#3-推送代码到-github)
- [4. 配置 GitHub Pages](#4-配置-github-pages)
- [5. 自定义域名设置](#5-自定义域名设置)
- [6. 处理重定向问题](#6-处理重定向问题)
- [7. 自动化部署脚本](#7-自动化部署脚本)
- [8. 常见问题解决](#8-常见问题解决)
- [9. 部署状态检查](#9-部署状态检查)
- [10. 完整工作流程](#10-完整工作流程)

---

## 1. 本地开发准备

### 创建项目结构
```bash
# 创建项目文件夹
mkdir my-website
cd my-website

# 初始化git仓库
git init

# 创建基本文件
touch index.html
touch README.md
touch .gitignore
```

### 基本 .gitignore 示例
```gitignore
# 系统文件
.DS_Store
Thumbs.db

# 编辑器文件
.vscode/
.idea/

# 临时文件
*.tmp
*.log

# Node.js (如果使用)
node_modules/
npm-debug.log

# Python (如果使用)
__pycache__/
*.pyc
```

---

## 2. GitHub 仓库创建

### 方法 A：在 GitHub 网站创建
1. 登录 GitHub
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：
   - **Repository name**: `your-project-name`
   - **Description**: 项目描述（可选）
   - **Visibility**: 选择 "Public"（私有仓库需要付费版 GitHub Pages）
   - **⚠️ 重要**: 不要勾选 "Add README"（因为本地已有文件）
4. 点击 "Create repository"

### 方法 B：使用 GitHub CLI
```bash
# 需要先安装 GitHub CLI: https://cli.github.com/
gh repo create your-project-name --public --description "我的网站项目"
```

---

## 3. 推送代码到 GitHub

### 连接本地仓库到 GitHub
```bash
# 添加远程仓库
git remote add origin https://github.com/你的用户名/your-project-name.git

# 检查远程仓库连接
git remote -v
```

### 提交并推送代码
```bash
# 添加所有文件到暂存区
git add .

# 第一次提交
git commit -m "Initial commit: Add website files

🎨 基础网站结构
- index.html 主页内容
- CSS 样式和响应式设计
- JavaScript 功能实现

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# 推送到 GitHub（首次推送需要 -u 参数）
git push -u origin main
```

---

## 4. 配置 GitHub Pages

### 方法 1：通过 GitHub 网站配置
1. 进入你的 GitHub 仓库
2. 点击 **"Settings"** 标签页
3. 在左侧菜单中找到 **"Pages"** 部分
4. 在 "Source" 下拉菜单中选择：
   - **Source**: "Deploy from a branch"
   - **Branch**: "main" 
   - **Folder**: "/ (root)"
5. 点击 **"Save"**
6. 等待 1-2 分钟，页面会显示你的网站 URL

### 方法 2：使用 GitHub CLI
```bash
# 启用 GitHub Pages
gh api repos/:owner/:repo/pages -X POST -F source.branch=main -F source.path=/

# 检查 Pages 状态
gh api repos/:owner/:repo/pages
```

### 默认访问地址
- **格式**: `https://你的用户名.github.io/仓库名`
- **示例**: `https://duoduodaye.github.io/my-website`

---

## 5. 自定义域名设置

### 5.1 添加 CNAME 文件
```bash
# 在项目根目录创建 CNAME 文件
echo "your-domain.com" > CNAME

# 提交并推送
git add CNAME
git commit -m "Add custom domain configuration"
git push
```

### 5.2 DNS 配置
在你的域名提供商（如阿里云、腾讯云等）控制台添加：

#### 根域名配置 (example.com)
```
类型: A
名称: @
值: 185.199.108.153
值: 185.199.109.153
值: 185.199.110.153
值: 185.199.111.153
```

#### 子域名配置 (www.example.com)
```
类型: CNAME
名称: www
值: 你的用户名.github.io
```

### 5.3 GitHub 后台域名验证
1. 在 GitHub 仓库 Settings → Pages
2. 在 "Custom domain" 输入你的域名
3. 勾选 "Enforce HTTPS"（推荐）
4. 等待 DNS 传播（通常 10 分钟到 24 小时）

---

## 6. 处理重定向问题

### 6.1 创建 404 错误页面
创建 `404.html` 文件：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>页面未找到 - 404</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            max-width: 500px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 10px;
        }
        .countdown { font-size: 24px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>😅 页面走丢了</h1>
        <p>抱歉，您访问的页面不存在</p>
        <div class="countdown" id="countdown">3</div>
        <p>秒后自动跳转到首页...</p>
        <a href="/" style="color: #fff; text-decoration: none; 
           background: rgba(255,255,255,0.2); padding: 10px 20px; 
           border-radius: 5px;">立即返回首页</a>
    </div>

    <script>
        let count = 3;
        const countdownEl = document.getElementById('countdown');
        
        const timer = setInterval(() => {
            count--;
            countdownEl.textContent = count;
            
            if (count <= 0) {
                clearInterval(timer);
                window.location.href = '/';
            }
        }, 1000);
    </script>
</body>
</html>
```

### 6.2 页面内重定向方法

#### Meta 标签重定向
```html
<!-- 立即重定向 -->
<meta http-equiv="refresh" content="0; url=/new-page.html">

<!-- 延迟 5 秒重定向 -->
<meta http-equiv="refresh" content="5; url=/new-page.html">
```

#### JavaScript 重定向
```html
<script>
    // 立即重定向
    window.location.href = '/new-page.html';
    
    // 或者使用 replace（不在浏览器历史中留记录）
    window.location.replace('/new-page.html');
    
    // 延迟重定向
    setTimeout(() => {
        window.location.href = '/new-page.html';
    }, 3000);
</script>
```

### 6.3 使用 Jekyll 重定向（高级）
创建 `_config.yml` 文件：
```yaml
# Jekyll 配置
plugins:
  - jekyll-redirect-from

# 全局重定向
redirect_from:
  - /old-path/
  - /another-old-path.html
```

在需要重定向的页面头部添加：
```yaml
---
redirect_from:
  - /old-page/
  - /legacy-url.html
---
```

---

## 7. 自动化部署脚本

### 创建部署脚本 `deploy.sh`
```bash
#!/bin/bash
# GitHub Pages 自动部署脚本
# 使用方法: ./deploy.sh

set -e  # 遇到错误立即停止

echo "🚀 开始部署到 GitHub Pages..."

# 检查是否在正确的目录
if [ ! -f "index.html" ]; then
    echo "❌ 错误: 当前目录没有找到 index.html，请在项目根目录执行此脚本"
    exit 1
fi

# 检查是否有 git 仓库
if [ ! -d ".git" ]; then
    echo "❌ 错误: 当前目录不是 git 仓库，请先运行 git init"
    exit 1
fi

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 检测到文件更改，正在处理..."
    
    # 显示更改的文件
    echo "📋 更改的文件:"
    git status --short
    echo ""
    
    # 添加所有更改
    git add .
    
    # 获取提交信息
    echo "💬 请输入提交信息（回车使用默认信息）:"
    read -r commit_msg
    
    # 如果用户没有输入，使用默认信息
    if [ -z "$commit_msg" ]; then
        commit_msg="Update website content - $(date '+%Y-%m-%d %H:%M')"
    fi
    
    # 提交更改
    git commit -m "$commit_msg

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
    
    echo "✅ 文件已提交"
else
    echo "ℹ️  没有检测到文件更改"
fi

# 推送到 GitHub
echo "📤 推送到 GitHub..."
if git push origin main; then
    echo "✅ 推送成功！"
else
    echo "❌ 推送失败，请检查网络连接和权限"
    exit 1
fi

# 获取仓库信息
REPO_URL=$(git config --get remote.origin.url)
REPO_NAME=$(basename "$REPO_URL" .git)
USERNAME=$(echo "$REPO_URL" | sed 's/.*github.com[/:]\([^/]*\)\/.*/\1/')

echo ""
echo "🎉 部署完成！"
echo "📋 部署信息:"
echo "   • 仓库: $USERNAME/$REPO_NAME"
echo "   • 分支: main"
echo "   • 状态: 正在构建..."
echo ""
echo "🌐 网站地址:"
echo "   • GitHub Pages: https://$USERNAME.github.io/$REPO_NAME"
echo "   • 更新时间: 约 1-2 分钟"
echo ""
echo "🔍 查看构建状态:"
echo "   https://github.com/$USERNAME/$REPO_NAME/actions"
```

### 使脚本可执行并运行
```bash
# 给脚本添加执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

### Windows 用户的 PowerShell 脚本 `deploy.ps1`
```powershell
# PowerShell 部署脚本
Write-Host "🚀 开始部署到 GitHub Pages..." -ForegroundColor Green

# 检查是否有更改
$status = git status --porcelain
if ($status) {
    Write-Host "📝 检测到文件更改，正在处理..." -ForegroundColor Yellow
    
    # 显示更改
    git status --short
    
    # 添加文件
    git add .
    
    # 获取提交信息
    $commitMsg = Read-Host "请输入提交信息（直接回车使用默认）"
    if ([string]::IsNullOrWhiteSpace($commitMsg)) {
        $commitMsg = "Update website content - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    }
    
    # 提交
    git commit -m "$commitMsg`n`n🤖 Generated with Claude Code`n`nCo-Authored-By: Claude <noreply@anthropic.com>"
    Write-Host "✅ 文件已提交" -ForegroundColor Green
} else {
    Write-Host "ℹ️  没有检测到文件更改" -ForegroundColor Blue
}

# 推送
Write-Host "📤 推送到 GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host "🎉 部署完成！网站将在 1-2 分钟内更新" -ForegroundColor Green
```

---

## 8. 常见问题解决

### 问题 1: 页面不更新/缓存问题
**症状**: 推送了新代码但网站显示旧内容

**解决方案**:
```bash
# 方法 1: 强制重新构建
git commit --allow-empty -m "Force rebuild GitHub Pages"
git push

# 方法 2: 清除浏览器缓存
# 在浏览器中按 Ctrl+Shift+R (Windows) 或 Cmd+Shift+R (Mac)

# 方法 3: 检查构建状态
# 访问 https://github.com/用户名/仓库名/actions
```

### 问题 2: CSS/JS 文件 404 错误
**症状**: 样式不加载，JavaScript 不工作

**解决方案**:
```html
<!-- ❌ 错误：绝对路径在 GitHub Pages 子目录中不工作 -->
<link rel="stylesheet" href="/styles.css">
<script src="/script.js"></script>

<!-- ✅ 正确：使用相对路径 -->
<link rel="stylesheet" href="styles.css">
<script src="script.js"></script>

<!-- ✅ 或者使用完整的绝对路径 -->
<link rel="stylesheet" href="/仓库名/styles.css">
<script src="/仓库名/script.js"></script>
```

### 问题 3: 自定义域名不工作
**症状**: 域名访问显示错误或无法访问

**检查清单**:
```bash
# 1. 检查 CNAME 文件内容
cat CNAME
# 应该只包含域名，如: example.com

# 2. 检查 DNS 设置（使用在线工具或命令）
nslookup your-domain.com
dig your-domain.com

# 3. 验证 GitHub Pages 设置
# 访问仓库 Settings → Pages，确保域名配置正确

# 4. 等待 DNS 传播（最长 24 小时）
```

### 问题 4: 构建失败
**症状**: GitHub Actions 显示红色 ❌

**排查步骤**:
1. 访问 `https://github.com/用户名/仓库名/actions`
2. 点击失败的构建查看详细日志
3. 常见原因:
   - 文件名包含特殊字符
   - Jekyll 语法错误
   - 权限问题

**解决方案**:
```bash
# 禁用 Jekyll（如果不需要）
touch .nojekyll
git add .nojekyll
git commit -m "Disable Jekyll processing"
git push
```

### 问题 5: 权限被拒绝
**症状**: `git push` 时提示权限错误

**解决方案**:
```bash
# 1. 检查远程 URL
git remote get-url origin

# 2. 如果使用 HTTPS，切换到 SSH
git remote set-url origin git@github.com:用户名/仓库名.git

# 3. 或者使用个人访问令牌
# 在 GitHub 设置中生成 token，然后:
git remote set-url origin https://token@github.com/用户名/仓库名.git
```

---

## 9. 部署状态检查

### 使用 GitHub CLI 检查
```bash
# 安装 GitHub CLI: https://cli.github.com/

# 查看最近的工作流运行
gh run list

# 查看特定运行的详细信息
gh run view [run-id]

# 查看 Pages 构建状态
gh api repos/:owner/:repo/pages/builds
```

### 使用网页界面检查
1. **Actions 页面**: `https://github.com/用户名/仓库名/actions`
   - 查看构建历史和状态
   - 点击具体构建查看详细日志

2. **Settings > Pages**: 
   - 查看当前 Pages 配置
   - 查看部署状态和错误信息

3. **Insights > Traffic**:
   - 查看网站访问统计

### 命令行检查工具
```bash
# 检查网站状态
curl -I https://你的用户名.github.io/仓库名

# 检查特定页面
curl -I https://你的用户名.github.io/仓库名/about.html

# 检查 DNS（如果使用自定义域名）
nslookup your-domain.com
```

---

## 10. 完整工作流程

### 日常开发流程
```bash
# 1. 本地开发
# 修改 HTML、CSS、JavaScript 文件

# 2. 本地测试
# 在浏览器中打开 index.html 预览

# 3. 提交更改
git add .
git commit -m "描述你的更改"

# 4. 推送到 GitHub
git push origin main

# 5. 等待部署 (1-2 分钟)

# 6. 验证网站
# 访问你的 GitHub Pages 网址确认更新
```

### 使用自动化脚本的流程
```bash
# 开发完成后，直接运行部署脚本
./deploy.sh

# 脚本会自动处理:
# - 检查文件更改
# - 提交代码
# - 推送到 GitHub
# - 显示部署信息
```

### 快速命令参考
```bash
# 快速部署（一行命令）
git add . && git commit -m "Update $(date)" && git push

# 检查部署状态
gh run list --limit 5

# 强制重新构建
git commit --allow-empty -m "Rebuild" && git push

# 查看网站访问日志
gh api repos/:owner/:repo/traffic/views
```

---

## 💡 小贴士

### 最佳实践
1. **定期备份**: 保持本地和 GitHub 同步
2. **语义化提交**: 使用清晰的提交信息
3. **测试优先**: 本地测试后再推送
4. **版本管理**: 使用分支管理不同版本
5. **性能优化**: 压缩图片和资源文件

### 性能优化建议
```html
<!-- 图片优化 -->
<img src="image.jpg" alt="描述" loading="lazy" width="300" height="200">

<!-- CSS 优化 -->
<link rel="preload" href="styles.css" as="style">
<link rel="stylesheet" href="styles.css">

<!-- JavaScript 优化 -->
<script src="script.js" defer></script>
```

### 安全建议
1. **不要提交敏感信息**: API 密钥、密码等
2. **使用 HTTPS**: 启用强制 HTTPS
3. **定期更新**: 保持依赖项最新
4. **访问控制**: 合理设置仓库权限

---

## 📚 相关资源

- [GitHub Pages 官方文档](https://docs.github.com/en/pages)
- [GitHub CLI 文档](https://cli.github.com/manual/)
- [Jekyll 文档](https://jekyllrb.com/docs/) （如果使用 Jekyll）
- [自定义域名设置指南](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

---

*最后更新: 2026年1月*
*作者: Cicadas*
*版本: 1.0*