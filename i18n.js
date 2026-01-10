// 多语言支持系统
class I18n {
  constructor() {
    this.currentLang = this.detectLanguage();
    this.translations = window.translations || {};
    this.init();
  }
  
  // 检测用户语言偏好
  detectLanguage() {
    // 1. 检查localStorage中保存的语言
    const savedLang = localStorage.getItem('preferred-language');
    if (savedLang && this.isValidLanguage(savedLang)) {
      return savedLang;
    }
    
    // 2. 检查浏览器语言
    const browserLang = navigator.language || navigator.userLanguage;
    if (browserLang.startsWith('zh')) {
      return 'zh-TW'; // 默认使用繁体中文
    } else if (browserLang.startsWith('en')) {
      return 'en';
    } else if (browserLang.startsWith('es')) {
      return 'es';
    }
    
    // 3. 默认语言
    return 'es';
  }
  
  // 验证语言代码是否有效
  isValidLanguage(lang) {
    return ['es', 'en', 'zh-TW'].includes(lang);
  }
  
  // 初始化
  init() {
    this.createLanguageSwitcher();
    this.translatePage();
    this.bindEvents();
  }
  
  // 创建语言切换器
  createLanguageSwitcher() {
    let headerControls = document.querySelector('.header-controls');
    if (!headerControls) {
      // 如果不存在，创建header-controls容器
      const header = document.querySelector('header');
      if (!header) return;
      headerControls = document.createElement('div');
      headerControls.className = 'header-controls';
      header.appendChild(headerControls);
    }
    
    const langSwitcher = document.createElement('div');
    langSwitcher.className = 'language-switcher';
    langSwitcher.innerHTML = `
      <button class="lang-btn ${this.currentLang === 'es' ? 'active' : ''}" data-lang="es">ES</button>
      <button class="lang-btn ${this.currentLang === 'en' ? 'active' : ''}" data-lang="en">EN</button>
      <button class="lang-btn ${this.currentLang === 'zh-TW' ? 'active' : ''}" data-lang="zh-TW">中文</button>
    `;
    
    headerControls.insertBefore(langSwitcher, headerControls.firstChild);
  }
  
  // 绑定事件
  bindEvents() {
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('lang-btn')) {
        const lang = e.target.getAttribute('data-lang');
        this.setLanguage(lang);
      }
    });
  }
  
  // 设置语言
  setLanguage(lang) {
    if (!this.isValidLanguage(lang)) return;
    
    this.currentLang = lang;
    localStorage.setItem('preferred-language', lang);
    
    // 更新按钮状态
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
    });
    
    // 翻译页面
    this.translatePage();
    
    // 更新HTML lang属性
    document.documentElement.lang = lang;
  }
  
  // 获取翻译文本
  getText(key) {
    return this.translations[this.currentLang]?.[key] || key;
  }
  
  // 翻译页面
  translatePage() {
    // 翻译带有data-i18n属性的元素
    document.querySelectorAll('[data-i18n]').forEach(element => {
      const key = element.getAttribute('data-i18n');
      const text = this.getText(key);
      
      if (element.tagName === 'INPUT' && element.type === 'text') {
        element.placeholder = text;
      } else {
        element.textContent = text;
      }
    });
    
    // 翻译带有data-i18n-html属性的元素（包含HTML内容）
    document.querySelectorAll('[data-i18n-html]').forEach(element => {
      const key = element.getAttribute('data-i18n-html');
      const text = this.getText(key);
      element.innerHTML = text;
    });
    
    // 翻译带有data-i18n-title属性的元素
    document.querySelectorAll('[data-i18n-title]').forEach(element => {
      const key = element.getAttribute('data-i18n-title');
      const text = this.getText(key);
      element.title = text;
    });
    
    // 特殊处理：技术栈标签
    document.querySelectorAll('[data-tech-area]').forEach(element => {
      const techText = element.getAttribute('data-tech-area');
      element.innerHTML = `<strong>${this.getText('tech_areas')}</strong> ${techText}`;
    });
    
    // 特殊处理：版权年份
    this.updateCopyright();
  }
  
  // 更新版权信息
  updateCopyright() {
    const footerElement = document.querySelector('footer');
    if (footerElement) {
      const currentYear = new Date().getFullYear();
      const rightsText = this.getText('all_rights');
      footerElement.innerHTML = `&copy; ${currentYear} Cicidas. ${rightsText}`;
    }
  }
}

// 主题切换功能
function initThemeToggle() {
  const btn = document.getElementById('theme-toggle');
  if (!btn) return;
  
  btn.onclick = function() {
    document.body.classList.toggle('dark-theme');
    if(document.body.classList.contains('dark-theme')){
      localStorage.setItem('theme', 'dark');
      btn.textContent = '🌞';
    } else {
      localStorage.setItem('theme', 'light');
      btn.textContent = '🌚';
    }
  };
  
  // 页面加载时自动应用主题
  if(localStorage.getItem('theme') === 'dark'){
    document.body.classList.add('dark-theme');
    btn.textContent = '🌞';
  } else {
    btn.textContent = '🌚';
  }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 等待translations.js加载完成
  if (typeof translations !== 'undefined') {
    window.i18n = new I18n();
  } else {
    console.error('Translations not loaded');
  }
  
  initThemeToggle();
});