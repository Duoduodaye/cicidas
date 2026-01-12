# 🤖 AI News Hub - Cicadas

## 概述
为Cicadas个人网站增强的AI新闻中心，提供最新的人工智能新闻、趋势分析和自动更新功能。

## 新增文件

### 1. `ai-news-enhanced.html`
- **现代化的AI新闻页面**
- 保持与原有Cicadas风格的兼容性
- 集成搜索、分类、实时更新功能
- 响应式设计，支持移动端

### 2. `scripts/daily_ai_news.py`
- **自动新闻获取脚本**
- 生成每日AI新闻摘要
- 输出HTML和JSON格式
- 可设置定时任务自动运行

## 功能特色

### 🎨 视觉设计
- **渐变背景**: 现代感十足的视觉效果
- **卡片布局**: 清晰的信息层次
- **动画效果**: 悬停动画和加载动画
- **响应式**: 完美适配手机、平板、电脑

### 🔍 智能搜索
- **实时搜索**: 输入即搜索，无需点击
- **分类过滤**: 研究、产业、工具、伦理、初创公司
- **标签搜索**: 点击热门标签快速搜索
- **多维度匹配**: 标题、摘要、标签全文搜索

### 📊 数据展示
- **精选新闻**: 重要新闻高亮显示
- **实时统计**: 文章总数、分类统计
- **发布时间**: 清晰的时间戳显示
- **阅读时长**: 预估阅读时间

### 🌐 多语言支持
- **西语 (ES)**: 默认语言
- **英语 (EN)**: 完整翻译
- **中文 (中文)**: 繁体中文支持

## 使用说明

### 立即使用
1. 打开 `ai-news-enhanced.html` 查看效果
2. 使用搜索框查找特定新闻
3. 点击分类按钮过滤内容
4. 点击热门标签快速搜索

### 集成到主网站
1. 在 `index.html` 中更新AI News链接：
```html
<a href="ai-news-enhanced.html" class="project-link">
  <span data-i18n="project4_link">Consulte los detalles</span> &rarr;
</a>
```

### 自动更新新闻
1. 运行新闻脚本：
```bash
cd scripts
python daily_ai_news.py
```

2. 设置每日定时任务（可选）：
```bash
# 编辑 crontab
crontab -e

# 添加每日早上8点运行
0 8 * * * cd /path/to/cicadas/scripts && python daily_ai_news.py
```

## 技术实现

### HTML/CSS/JavaScript
- **原生技术**: 无需额外依赖
- **ES6语法**: 现代JavaScript特性
- **CSS Grid/Flexbox**: 现代布局技术
- **CSS变量**: 主题系统支持

### Python脚本
- **轻量级**: 仅使用标准库
- **可扩展**: 易于添加真实数据源
- **多格式输出**: HTML片段 + JSON数据

## 文件结构
```
cicadas/
├── ai-news-enhanced.html      # 增强版AI新闻页面
├── scripts/
│   └── daily_ai_news.py       # 新闻获取脚本
├── styles.css                 # 原有样式（复用）
├── translations.js             # 原有翻译（复用）
├── i18n.js                    # 原有国际化（复用）
└── AI-NEWS-README.md          # 本说明文件
```

## 开发路线图

### 即将推出
- [ ] 真实新闻API集成
- [ ] 用户收藏功能
- [ ] 社交分享按钮
- [ ] 评论系统

### 长期规划
- [ ] PWA支持（离线阅读）
- [ ] AI推荐算法
- [ ] 个性化定制
- [ ] 多媒体内容支持

## 部署说明

### GitHub Pages
1. 提交所有文件到仓库
2. 在GitHub仓库设置中启用Pages
3. 选择主分支作为源
4. 访问 `https://duoduodaye.github.io/cicadas/ai-news-enhanced.html`

### 自定义域名
如果你有自定义域名，在仓库根目录添加 `CNAME` 文件：
```
your-domain.com
```

## 技术支持

### 常见问题
1. **新闻不显示**: 检查JavaScript控制台错误
2. **搜索不工作**: 确保输入框事件正常绑定
3. **样式错误**: 检查CSS文件路径

### 自定义修改
- **颜色主题**: 修改CSS变量
- **布局调整**: 调整Grid/Flexbox属性
- **内容数据**: 修改mockNews数组

## 贡献指南

欢迎提交改进建议和Bug报告！

### 开发环境
1. 克隆仓库
2. 使用Live Server预览
3. 提交Pull Request

---

## 联系信息
- **Email**: contacto@cicidas.org
- **GitHub**: github.com/duoduodaye
- **网站**: cicidas.org

---

*最后更新: 2025-01-12*
*版本: 1.0.0*