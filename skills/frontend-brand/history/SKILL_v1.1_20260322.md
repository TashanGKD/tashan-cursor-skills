---
name: frontend-brand
description: 他山前端品牌设计系统完整参考手册。包含技术框架选型、设计令牌（颜色/字体/圆角/阴影）、组件规范代码模板、响应式/无障碍约定。被 role-前端开发 和 role-UI设计师 主动调用；与 frontend-brand-guard.mdc（约束层）配套使用。
---

# 他山前端品牌设计系统（frontend-brand）

关系类型：validates `frontend-brand-guard.mdc` / extends `role-前端开发` / extends `role-UI设计师`

> **本 Skill 是可复用知识层**，回答「怎么写才对」。
> 配套 Rule `frontend-brand-guard.mdc` 是约束层，回答「哪些绝对不能写」。
> **真相来源**：所有代码以 `frontend/src/index.css` 和 `frontend/tailwind.config.js` 为准。

---

## 激活后立即执行

```
Step 1  明确当前场景（产品内页 or 官网/主页）
         → 不确定时默认：产品内页（黑白极简）

Step 2  定位具体需求（组件类型 / 页面类型 / 样式修改）
         → 查阅本 Skill 对应章节，直接使用规范类名和代码模板

Step 3  输出代码 / 设计方案
         → 输出前对照第十章「禁止清单」自检

Step 4  遇到本 Skill 未覆盖的细节时，按优先级查阅：
         1. frontend/src/index.css（CSS 变量/动画定义的唯一真相）
         2. frontend/tailwind.config.js（Tailwind 映射的唯一真相）
         3. 项目群/Tashan-TopicLab/docs/design/frontend-design-guide.md（语义说明）
```

---

## ⚠️ 已知文档内部不一致（必须知晓）

`shape-system.md` 表格中写 `rounded-lg` = Default = 12px，但实际代码 `tailwind.config.js` 将 `rounded-lg` 映射到 `var(--radius-lg)` = **16px**，`frontend-design-guide.md` 中卡片/按钮/模态框也均使用 `rounded-lg`。**以代码为准：`rounded-lg` = 16px**，是标准通用圆角。

---

## 一、技术框架

| 技术 | 版本 | 用途 |
|------|------|------|
| React | 18.x | UI 框架 |
| TypeScript | 5.x | 类型系统 |
| Vite | 5.x | 构建工具 |
| Tailwind CSS | 3.x | 样式（utility-first，不用 CSS-in-JS） |
| react-router-dom | 6.x | 路由 |
| react-markdown + remark-gfm | latest | Markdown 渲染 |
| KaTeX + remark-math + rehype-katex | latest | 数学公式 |
| Vitest + @testing-library/react | latest | 测试 |

**样式分层**：Tailwind utility → `@layer components` → `@layer utilities`（动画/工具）→ `@layer base`（html/body）

**文件结构**（实际项目）：

```
frontend/src/
├── api/           # axios 封装
├── components/    # 可复用组件
├── hooks/         # 自定义 hooks
├── modules/       # 功能模块
├── pages/         # 页面组件
├── utils/         # 工具函数
├── App.tsx
├── main.tsx
└── index.css      # CSS 变量 / @layer base / 动画 / markdown 样式
```

---

## 二、设计令牌（完整以代码为准）

### 2.1 字体

```javascript
// tailwind.config.js
fontFamily: {
  serif: ['Noto Serif SC', 'STSong', 'SimSun', 'serif'],
  sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
}
```

```html
<!-- index.html — 字体加载 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
```

**规则**：
- 所有用户可见文字 → `font-serif`（Noto Serif SC）
- 技术标识/代码片段 → `font-mono`
- 禁止：Inter、Roboto、Arial 作主字体

### 2.2 排版比例（来自 frontend-design-guide.md）

| 用途 | Tailwind 类 |
|------|-------------|
| 页面标题 | `text-xl sm:text-2xl font-serif font-bold text-black` |
| 章节标题 | `text-lg font-serif font-semibold text-black` |
| 卡片标题 | `text-base font-serif font-semibold text-black` |
| 正文 | `text-sm font-serif text-black` 或 `text-gray-600` |
| 次要信息 | `text-xs text-gray-500` |
| 技术ID | `text-[10px] text-gray-400 font-mono` |

行高与截断：正文 `leading-relaxed`，单行 `truncate`，多行 `line-clamp-2`

### 2.3 CSS 变量（`src/index.css` — 唯一真相）

```css
:root {
  /* 主题色 (Brand) */
  --brand-primary: #3B82F6;
  --brand-dark:    #1E40AF;
  --brand-light:   #DBEAFE;

  /* 强调色 (Accent) */
  --accent-primary: #0EA5E9;
  --accent-success: #10B981;
  --accent-warning: #F59E0B;
  --accent-error:   #EF4444;
  --accent-info:    #3B82F6;

  /* 底色 (Background) */
  --bg-page:      #F8FAFC;
  --bg-container: #FFFFFF;
  --bg-secondary: #F1F5F9;
  --bg-tertiary:  #F8FAFC;
  --bg-hover:     #F1F5F9;
  --bg-selected:  #E0F2FE;
  --bg-disabled:  #E2E8F0;
  --bg-footer:    #0E2E4F;

  /* 文字色 (Text) */
  --text-primary:   #1E293B;   /* ← 注意：不是 #0F172A */
  --text-secondary: #475569;
  --text-tertiary:  #94A3B8;
  --text-disabled:  #CBD5E1;
  --text-inverse:   #FFFFFF;

  /* 边框色 (Border) */
  --border-default: #E2E8F0;
  --border-hover:   #CBD5E1;
  --border-focus:   #3B82F6;
  --border-active:  #0EA5E9;

  /* 阴影 (Shadow) */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.06);
  --shadow-xl: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);

  /* 圆角 (Radius) — 精简三级 */
  --radius-sm:   12px;     /* 已废弃，映射到 --radius-md */
  --radius-md:   12px;     /* 12px — 理论默认（实际 rounded-lg = 16px，见顶部说明） */
  --radius-lg:   16px;     /* 16px — 弹窗/下拉/标准通用 */
  --radius-xl:   16px;     /* 已废弃，映射到 --radius-lg */
  --radius-2xl:  16px;     /* 已废弃，映射到 --radius-lg */
  --radius-full: 9999px;   /* 完全圆形 */

  /* 过渡 (Transition) */
  --transition-fast:   150ms ease;
  --transition-normal: 200ms ease;
  --transition-slow:   300ms ease;

  /* 兼容旧变量（迁移期间保留，勿在新代码中直接使用） */
  --color-primary:    var(--brand-primary);
  --color-secondary:  var(--accent-primary);
  --color-dark:       var(--text-primary);
  --color-darker:     var(--brand-dark);
  --color-gray:       var(--text-secondary);
  --color-gray-light: var(--border-default);
  --color-gray-dark:  var(--text-tertiary);
  --gradient-dark:    var(--bg-footer);
}
```

### 2.4 Tailwind Config（`tailwind.config.js` — 唯一真相）

```javascript
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        serif: ['Noto Serif SC', 'STSong', 'SimSun', 'serif'],
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      colors: {
        brand:   { primary: 'var(--brand-primary)', dark: 'var(--brand-dark)', light: 'var(--brand-light)' },
        accent:  { primary: 'var(--accent-primary)', success: 'var(--accent-success)',
                   warning: 'var(--accent-warning)', error: 'var(--accent-error)', info: 'var(--accent-info)' },
        surface: { page: 'var(--bg-page)', container: 'var(--bg-container)', secondary: 'var(--bg-secondary)',
                   hover: 'var(--bg-hover)', selected: 'var(--bg-selected)', disabled: 'var(--bg-disabled)' },
        content: { primary: 'var(--text-primary)', secondary: 'var(--text-secondary)',
                   tertiary: 'var(--text-tertiary)', disabled: 'var(--text-disabled)', inverse: 'var(--text-inverse)' },
        line:    { default: 'var(--border-default)', hover: 'var(--border-hover)',
                   focus: 'var(--border-focus)', active: 'var(--border-active)' },
        black: '#000000',
        white: '#FFFFFF',
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
      },
      borderRadius: {
        sm:   'var(--radius-sm)',    // 12px (deprecated)
        md:   'var(--radius-md)',    // 12px
        lg:   'var(--radius-lg)',    // 16px ← 标准通用圆角
        xl:   'var(--radius-xl)',    // 16px (deprecated)
        '2xl':'var(--radius-2xl)',   // 16px (deprecated)
        full: 'var(--radius-full)',  // 9999px
      },
      boxShadow: {
        sm: 'var(--shadow-sm)', md: 'var(--shadow-md)',
        lg: 'var(--shadow-lg)', xl: 'var(--shadow-xl)',
      },
      transitionDuration: {
        fast: '150ms', normal: '200ms', slow: '300ms',
      },
    },
  },
  plugins: [],
}
```

---

## 三、配色场景

| 场景 | 使用时机 | 核心色调 |
|------|----------|---------|
| **产品内页（默认）** | 话题列表/详情/配置/库 | 黑+白+灰，`black`/`white`/`gray-*` |
| **官网/主页** | Landing page / 营销页 | 蓝绿渐变 `#5B9BD5` + `#9FD4C4` |

**不确定时，始终用产品内页风格。**

### 产品内页速查

```
主色/CTA：       #000000 (black)
页面背景：        #FFFFFF (white)
卡片边框：        gray-200
次边框：          gray-100
悬停边框：        gray-300 / black（激活）
主文字：          text-black
描述文字：        text-gray-600 / text-gray-700
次要文字：        text-gray-500
技术标识：        text-gray-400 font-mono
禁用：            text-gray-400 opacity-50
选中背景：        bg-gray-100
悬停背景：        bg-gray-50
文字选中：        ::selection { bg-black text-white }
```

### 官网/主页速查

```css
--color-primary:   #5B9BD5;   /* 淡蓝 */
--color-secondary: #9FD4C4;   /* 淡绿 */
--color-dark:      #0E2E4F;   /* 深海蓝（footer/heading） */
--gradient-primary: linear-gradient(135deg, #5B9BD5 0%, #9FD4C4 100%);
--gradient-secondary: linear-gradient(135deg, #6BC5D6 0%, #B5E5C8 100%);
--gradient-dark: linear-gradient(135deg, #0E2E4F 0%, #0A1F35 100%);
/* 渐变标题文字 */
.gradient-text {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### 语义状态色

| 状态 | 类 |
|------|-----|
| Default | `border-gray-200 text-gray-600` |
| Active/Selected | `border-black text-black` 或 `bg-gray-100` |
| Disabled | `text-gray-400 opacity-50` |
| Open | `bg-green-50 text-green-700` |
| Running | `bg-blue-50 text-blue-600` |
| Completed | `bg-gray-100 text-gray-600` |

> 语义色统一封装在 `.status-badge*` CSS 类（见第九章），不允许各处临时映射。

---

## 四、圆角系统（代码实际值）

| Tailwind 类 | CSS 变量 | 实际值 | 使用场景 |
|------------|----------|--------|---------|
| `rounded-lg` | `var(--radius-lg)` | **16px** | 卡片/按钮/输入框/模态框（指南统一用此类） |
| `rounded-xl` | `var(--radius-xl)` | 16px | 已废弃，等同 `rounded-lg` |
| `rounded-full` | `var(--radius-full)` | 9999px | 头像/Chip/徽章 |
| `rounded-md` | `var(--radius-md)` | 12px | 理论默认，当前实际用 `rounded-lg` |

**禁止**：自定义值 `rounded-[XXpx]`

---

## 五、组件代码模板（来自 frontend-design-guide.md）

### 5.1 按钮

```tsx
// 主按钮
<button className="bg-black text-white px-4 py-1.5 rounded-lg text-sm font-serif font-medium hover:bg-gray-900 transition-colors disabled:opacity-50">
  操作
</button>

// 次按钮
<button className="border border-gray-200 bg-white text-black px-4 py-1.5 rounded-lg text-sm font-serif font-medium hover:border-black transition-colors disabled:opacity-50">
  次要操作
</button>

// 文字按钮
<button className="text-sm text-gray-500 hover:text-black transition-colors">返回</button>

// 图标按钮
<button className="p-2 rounded-lg text-gray-600 hover:text-black hover:bg-gray-100 transition-colors" aria-label="打开菜单">
  <Icon />
</button>

// 圆形操作按钮（+/×）
<button className="w-7 h-7 rounded-full flex items-center justify-center bg-black text-white hover:bg-gray-800 transition-colors" aria-label="添加">+</button>
```

### 5.2 卡片

```tsx
// 标准内容卡片（可点击，含响应式宽度）
<div className="flex flex-col gap-1 px-4 py-3 rounded-lg border border-gray-200 bg-white hover:border-gray-300 hover:bg-gray-50 transition-colors w-full min-w-0 sm:min-w-[200px] sm:max-w-[280px] sm:w-auto text-left cursor-pointer">
  <span className="text-base font-serif font-semibold text-black truncate">标题</span>
  <span className="text-sm font-serif text-gray-600 line-clamp-2">描述</span>
  <span className="text-xs text-gray-500">元数据</span>
</div>

// 话题列表项
<div className="border border-gray-200 rounded-lg p-4 sm:p-6 hover:border-black transition-colors active:bg-gray-50 cursor-pointer">
  {/* 内容 */}
</div>

// 选中态卡片（select 模式）
<div className={`rounded-lg border px-4 py-3 transition-colors cursor-pointer ${
  isSelected
    ? 'border-gray-400 bg-gray-100'
    : 'border-gray-200 bg-white hover:border-gray-300 hover:bg-gray-50'
}`}>
  {/* 选中时按钮: bg-gray-400 text-white / 未选中: bg-black text-white */}
</div>
```

### 5.3 输入控件

```tsx
<input
  className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm font-serif focus:border-black focus:outline-none transition-colors"
  placeholder="输入内容"
/>
<textarea
  className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm font-serif focus:border-black focus:outline-none transition-colors resize-none"
  rows={4}
/>
<label className="block text-sm font-serif font-medium text-black mb-2">字段名</label>
```

### 5.4 导航（TopNav）

```tsx
<nav className="h-14 bg-white border-b border-gray-200 flex items-center px-4 sm:px-6 justify-between">
  <span className="text-base font-serif font-bold text-black">他山</span>
  <div className="hidden md:flex items-center gap-6">
    <a className="text-sm font-serif text-black font-medium">激活页</a>
    <a className="text-sm font-serif text-gray-500 hover:text-black transition-colors">其他</a>
  </div>
  <button className="bg-black text-white px-4 py-1.5 rounded-lg text-sm font-serif font-medium hover:bg-gray-900">登录</button>
  <button className="md:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100" aria-label="打开菜单">☰</button>
</nav>
```

### 5.5 模态框

```tsx
<div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
  {/* 文档说 rounded-lg，与卡片一致 */}
  <div className="bg-white rounded-lg shadow-xl border border-gray-200 max-w-2xl w-full max-h-[85vh] flex flex-col">
    <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
      <h2 className="text-lg font-serif font-semibold text-black">标题</h2>
      <button className="text-gray-500 hover:text-black text-2xl" aria-label="关闭">×</button>
    </div>
    <div className="flex-1 overflow-auto px-6 py-4">{/* 内容 */}</div>
    <div className="px-6 py-4 border-t border-gray-200 flex justify-end gap-3">
      <button className="text-sm text-gray-500 hover:text-black">取消</button>
      <button className="bg-black text-white px-4 py-1.5 rounded-lg text-sm font-serif font-medium hover:bg-gray-900">确认</button>
    </div>
  </div>
</div>
```

### 5.6 Tab 面板

```tsx
<div className="flex gap-1 border-b border-gray-200 -mb-px overflow-x-auto scrollbar-hide">
  {tabs.map(tab => (
    <button key={tab.id}
      className={`px-4 py-2 text-sm font-serif whitespace-nowrap border-b-2 transition-colors ${
        activeTab === tab.id ? 'text-black font-medium border-black' : 'text-gray-500 hover:text-gray-700 border-transparent'
      }`}
      onClick={() => setActiveTab(tab.id)}>{tab.label}</button>
  ))}
</div>
{/* 内容带方向动画 */}
<div className={dir === 'right' ? 'animate-slide-in-right' : 'animate-slide-in-left'}>
  {/* 内容 */}
</div>
```

### 5.7 Chip（标签/过滤器）

```tsx
{/* 移动端 pill，桌面端 card */}
<div className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs bg-gray-100 border border-gray-200 sm:rounded-lg sm:px-3 sm:py-2 sm:min-w-[180px] sm:max-w-[280px] sm:bg-white sm:hover:border-gray-400 sm:hover:bg-gray-50 transition-colors">
  <span className="font-serif text-black truncate max-w-[120px] sm:max-w-[220px]">标签文字</span>
  <button className="w-5 h-5 sm:w-7 sm:h-7 rounded-full flex items-center justify-center text-gray-400 hover:text-black hover:bg-gray-200 transition-colors flex-shrink-0" aria-label="移除">×</button>
</div>
```

### 5.8 头像（Expert Avatar）

```tsx
{/* w-6 h-6 或 w-7 h-7（指南两种尺寸） */}
<div className="w-6 h-6 rounded-full bg-black text-white flex items-center justify-center font-serif text-xs flex-shrink-0">
  {name.charAt(0).toUpperCase()}
</div>
```

### 5.9 Spinner（加载）

```tsx
{/* 使用 index.css 的 .spinner class */}
<span className="spinner" />
{/* 或直接 animate-spin */}
<div className="inline-block w-4 h-4 border-2 border-gray-200 border-t-black rounded-full animate-spin" />
```

---

## 六、布局与间距

### 容器宽度

```tsx
<div className="max-w-6xl mx-auto px-4 sm:px-6">  {/* 内容库 */}
<div className="max-w-4xl mx-auto px-4 sm:px-6">  {/* 列表页 */}
<div className="max-w-2xl mx-auto px-4 sm:px-6">  {/* 表单/详情 */}
```

### 垂直节奏

```
页面内边距：  py-6 sm:py-8
标题到内容：  mb-6 sm:mb-8（或 mb-8 sm:mb-12）
卡片间距：    gap-4
表单字段间：  gap-6
主内容偏移：  pt-14（TopNav 高度）
```

### 响应式模式

| 场景 | 移动端 | 桌面端 |
|------|--------|--------|
| 内边距 | `px-4 py-6` | `sm:px-6 sm:py-8` |
| 标题 | `text-xl` | `sm:text-2xl` |
| 导航 | 汉堡菜单 | `md:flex` 横向链接 |
| Chip | `rounded-full` 紧凑 | `sm:rounded-lg` 展开 |
| 网格 | 单列 | `sm:grid-cols-2 lg:grid-cols-3` |

---

## 七、`@layer base`（`index.css` 实际定义）

```css
@layer base {
  html {
    font-family: 'Noto Serif SC', STSong, SimSun, serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    -webkit-tap-highlight-color: transparent;
    scroll-behavior: smooth;
    overscroll-behavior: none;
  }
  body {
    font-feature-settings: "kern" 1, "liga" 1;
    padding-left: env(safe-area-inset-left);
    padding-right: env(safe-area-inset-right);
    overflow-x: hidden;
    background-color: var(--bg-page);
    color: var(--text-primary);
    min-height: 100vh;
    overscroll-behavior: none;
  }
  ::selection {
    @apply bg-black text-white;
  }
}
```

---

## 八、动画与工具类（`index.css` 实际定义）

### 动画关键帧（以代码为准，与设计文档有差异）

```css
@layer utilities {
  /* === 动画关键帧 === */
  @keyframes spin {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
  }
  @keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.2; }
  }
  @keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
  }
  @keyframes slideInFromRight {
    from { opacity: 0.6; transform: translateX(12%); }
    to   { opacity: 1;   transform: translateX(0); }
  }
  @keyframes slideInFromLeft {
    from { opacity: 0.6; transform: translateX(-12%); }
    to   { opacity: 1;   transform: translateX(0); }
  }
  @keyframes nudgeRight {
    0%, 100% { transform: translateX(0);   opacity: 0.7; }
    50%      { transform: translateX(4px); opacity: 1; }
  }

  /* === 动画类 === */
  .animate-spin           { animation: spin 0.8s linear infinite; }
  .animate-blink          { animation: blink 1.2s ease-in-out infinite; }
  .animate-fade-in        { animation: fadeIn 0.15s ease-out; }
  .animate-slide-in-right { animation: slideInFromRight 0.2s ease-out; }
  .animate-slide-in-left  { animation: slideInFromLeft  0.2s ease-out; }
  .animate-nudge-right    { animation: nudgeRight 2s ease-in-out infinite; }

  /* === 工具类 === */
  .prose-serif        { font-family: 'Noto Serif SC', STSong, SimSun, serif; }
  .border-thin        { border-width: 0.5px; }
  .safe-area-inset-top { padding-top: env(safe-area-inset-top); }
  .touch-manipulation { touch-action: manipulation; }
  .scroll-contain     { overscroll-behavior: contain; -webkit-overflow-scrolling: touch; }
  .no-bounce          { overscroll-behavior: none; touch-action: pan-y; }
  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
  .scrollbar-hide::-webkit-scrollbar { display: none; }
}
```

**过渡规则**：
- 常规状态变化 → `transition-colors`（优先，避免 transition-all 引起布局抖动）
- 可接受 → `transition-all duration-200`
- Tab 切换 → `animate-slide-in-right` / `animate-slide-in-left`
- 触摸优化 → `touch-manipulation`（消除 300ms 延迟）

---

## 九、预定义 CSS 组件类（`index.css` 实际定义，非 Tailwind 工具类）

```css
/* === Spinner === */
.spinner {
  @apply inline-block w-4 h-4 border-2 border-gray-200 border-t-black rounded-full animate-spin;
}

/* === Status Badge === */
.status-badge {
  @apply inline-flex items-center px-2 py-0.5 text-xs border;
}
.status-badge-default { @apply status-badge border-gray-200 text-gray-600; }
.status-badge-active  { @apply status-badge border-black text-black; }

/* === Expert Dot === */
.expert-dot-active { @apply w-2 h-2 rounded-full bg-black animate-blink; }
```

使用示例：
```tsx
<span className="spinner" />
<span className="status-badge-active">进行中</span>
<span className="expert-dot-active" />
```

---

## 十、Markdown 内容渲染（以 `index.css` 实际代码为准）

包裹 `react-markdown` 输出用 `.markdown-content` 类（纯 CSS 选择器，非 `@layer`）：

```css
/* --- 基础 --- */
.markdown-content { @apply leading-relaxed text-black; font-family: 'Noto Serif SC', STSong, SimSun, serif; }

/* --- 标题（通用）--- */
.markdown-content h1, h2, h3, h4, h5, h6 { @apply mt-8 mb-4 font-bold text-black; font-family: 'Noto Serif SC', ...; }
.markdown-content h1 { @apply text-2xl border-b border-black pb-2; }
.markdown-content h2 { @apply text-xl border-b border-gray-200 pb-1; }
.markdown-content h3 { @apply text-lg; }
.markdown-content h4 { @apply text-base; }

/* --- 正文 --- */
.markdown-content p         { @apply mb-4; }
.markdown-content p:last-child { @apply mb-0; }
.markdown-content ul, ol    { @apply mb-4 pl-6; }
.markdown-content li        { @apply mb-2; }
.markdown-content hr        { @apply border-t border-gray-200 my-8; }

/* --- 链接 --- */
.markdown-content a { @apply text-black underline; text-decoration-thickness: 1px; text-underline-offset: 2px; }
.markdown-content a:hover { text-decoration-thickness: 2px; }

/* --- 图片（有完整样式！） --- */
.markdown-content img {
  @apply block h-auto my-4 rounded-xl border border-gray-200 bg-gray-50 shadow-sm mx-auto;
  max-height: min(72vh, 520px);
  width: auto;
  max-width: 100%;
  object-fit: contain;
}

/* --- 代码 --- */
.markdown-content code { @apply bg-gray-100 px-1 py-0.5 text-sm; font-family: 'Courier New', Courier, monospace; }
.markdown-content pre  { @apply bg-gray-900 text-white p-4 mb-4 overflow-x-auto; }
.markdown-content pre code { @apply bg-transparent p-0; }

/* --- 引用 --- */
.markdown-content blockquote { @apply border-l-2 border-black pl-4 my-4 text-gray-600 italic; }

/* --- 表格（注意：border-collapse，非 rounded） --- */
.markdown-content table { @apply w-full border-collapse mb-4 text-sm; }
.markdown-content th, .markdown-content td { @apply border border-gray-200 px-3 py-2 text-left; }
.markdown-content th { @apply bg-gray-50 font-semibold text-black; }
.markdown-content td { @apply text-gray-700; }
```

---

## 十一、无障碍（a11y）约定

```tsx
// 图标按钮必须有 aria-label
<button aria-label="关闭菜单">×</button>

// 可展开元素
<button aria-expanded={isOpen} aria-label="切换菜单">

// 非 button 可点击
<div role="button" tabIndex={0} onKeyDown={e => e.key === 'Enter' && handleClick()} onClick={handleClick}>

// 下拉键盘支持
onKeyDown={(e) => {
  if (e.key === 'ArrowDown') selectNext();
  if (e.key === 'ArrowUp')   selectPrev();
  if (e.key === 'Escape')    close();
}}

// 焦点（不允许无替代的 outline-none）
className="focus:border-black focus:outline-none"  // ✅ 用边框替代
```

---

## 十二、禁止清单（与 frontend-brand-guard.mdc 同步）

```
❌ Inter / Roboto / Arial 作主字体
❌ 大面积渐变背景、紫色配色、通用 AI 风格
❌ 自定义圆角值 rounded-[XXpx]
❌ className 中硬编码颜色值（用 Tailwind 类或 CSS 变量）
❌ 可点击元素无 aria-label
❌ outline-none 无可见焦点替代
❌ Tab 切换和模态框以外的复杂动画
❌ 移动端点击区域 < 44×44px
❌ CSS-in-JS（styled-components / emotion）
❌ 新代码中直接使用旧兼容变量（--color-primary 等）
```

---

## 十三、权威文档路径

```
代码真相（优先）：
/Users/boyuan/aiwork/0310_huaxiang\项目群\Tashan-TopicLab\frontend\
├── src\index.css          ← CSS 变量/动画/@layer base/markdown 样式（唯一真相）
└── tailwind.config.js     ← Tailwind 映射（唯一真相）

设计文档（语义说明，次级）：
/Users/boyuan/aiwork/0310_huaxiang\项目群\Tashan-TopicLab\docs\design\
├── frontend-design-guide.md       ← 完整设计语言（组件类名、布局、响应式）
├── color-system.md                ← 配色变量语义说明
├── shape-system.md                ← 圆角系统说明（⚠️ CSS 变量值与 index.css 不同）
├── tashan-homepage-style-guide.md ← 官网/主页风格
└── style-refactor-checklist.md    ← 重构优先级清单
```

---

## 变更记录

### 2026-03-20 — v1.0 初始创建

见 history/SKILL_v1.0_20260320.md

### 2026-03-20 — v1.0 → v1.1 — 严格对齐 index.css 真相，修复全量偏差

**根因**：用户要求严格验证 SKILL 内容与 TopicLab 实际代码是否完全一致。逐行比对 `index.css`（真相）vs v1.0 发现多处严重偏差。

**错误修复（有误的值）**：
- `--text-primary: #0F172A` → 修正为 `#1E293B`（来自 index.css）
- `fadeIn` keyframe：移除了错误的 `translateY(4px)` transform（index.css 无 transform）
- `blink` keyframe：修正为 `0%,100%{opacity:1} 50%{opacity:0.2} 1.2s ease-in-out`
- `slideInFromRight/Left`：修正为 `translateX(12%/-12%)` + `opacity:0.6`（非 16px + 0）
- Modal 圆角：跟随 guide 用 `rounded-lg`（非 `rounded-xl`）
- Shape 表说明：修正 `rounded-lg` = 16px（非 12px），与 tailwind.config.js 实际映射一致

**缺失内容补充**：
- CSS 变量：补全 `--bg-tertiary`、`--radius-sm/xl/2xl`、旧兼容变量（`--color-*`）
- Tailwind config：补全 `accent.info`、`surface.disabled`、`content.disabled`、`spacing`、`transitionDuration`、`borderRadius '2xl'`
- 动画：补全 `animate-spin`、`animate-nudge-right`
- 工具类：补全 `.prose-serif`、`.border-thin`、`.scroll-contain`、`.no-bounce`
- 预定义 CSS 类：补全 `.spinner`、`.status-badge*`、`.expert-dot-active`
- Markdown：补全 `img` 样式、`h4`、`p:last-child`、`hr`、`text-underline-offset`、正确的 `table` 样式（`border-collapse`，非 `rounded`）
- `@layer base`：补全完整 html/body 属性（`overscroll-behavior`、`background-color`、`color`、`min-height` 等）
- 卡片响应式：补全 `min-w-0 sm:min-w-[200px] sm:max-w-[280px] sm:w-auto`
- Chip 桌面：补全 `sm:min-w-[180px] sm:max-w-[280px]`

**验证结果**：
- 正向验证：所有 CSS 变量值、keyframe 定义、组件类名均可从 index.css 找到对应源码
- 负向验证：无内容被删减，均为补充/修正（只增不减原则满足）

**验证状态**：✅ 已验证（逐行对照 index.css）
