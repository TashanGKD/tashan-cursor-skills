---
name: frontend-brand
description: 他山前端品牌设计系统完整参考手册。包含技术框架选型、设计令牌（颜色/字体/圆角/阴影）、组件规范代码模板、响应式/无障碍约定。被 role-前端开发 和 role-UI设计师 主动调用；与 frontend-brand-guard.mdc（约束层）配套使用。
---

# 他山前端品牌设计系统（frontend-brand）

关系类型：validates `frontend-brand-guard.mdc` / extends `role-前端开发` / extends `role-UI设计师`

> **本 Skill 是可复用知识层**，回答「怎么写才对」。
> 配套 Rule `frontend-brand-guard.mdc` 是约束层，回答「哪些绝对不能写」。
> 两者共同构成他山前端品牌安全闭环。

---

## 激活后立即执行

```
Step 1  明确当前场景（产品内页 or 官网/主页）
         → 不确定时默认：产品内页（黑白极简）

Step 2  定位具体需求（组件类型 / 页面类型 / 样式修改）
         → 查阅本 Skill 对应章节，直接使用规范类名和代码模板

Step 3  输出代码 / 设计方案
         → 输出前对照「禁止清单」自检

Step 4  遇到本 Skill 未覆盖的细节时
         → Read: 项目群/Tashan-TopicLab/docs/design/frontend-design-guide.md（权威全文）
```

---

## 一、技术框架

| 技术 | 版本 | 用途 | 备注 |
|------|------|------|------|
| React | 18.x | UI 框架 | |
| TypeScript | 5.x | 类型系统 | 严格模式 |
| Vite | 5.x | 构建工具 | |
| Tailwind CSS | 3.x | 样式系统 | utility-first，不用 CSS-in-JS |
| react-router-dom | 6.x | 路由 | |
| react-markdown + remark-gfm | latest | Markdown 渲染 | |
| KaTeX + remark-math + rehype-katex | latest | 数学公式 | |
| Vitest + @testing-library/react | latest | 测试 | |

**样式方案原则**：Tailwind utility → `@layer components` 共享类 → `@layer utilities` 动画/工具类。禁止 styled-components / emotion / CSS Modules（除非极特殊场景且须审批）。

**文件结构约定**：

```
frontend/src/
├── api/           # API 客户端（axios 封装）
├── components/    # 可复用组件
├── hooks/         # 自定义 hooks
├── modules/       # 功能模块（如 profile-helper）
├── pages/         # 页面组件
├── utils/         # 工具函数
├── App.tsx
├── main.tsx
└── index.css      # 全局样式、@layer、CSS 变量
```

---

## 二、设计令牌（Design Tokens）

### 2.1 字体

```javascript
// tailwind.config.js — fontFamily
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

**使用规则**：
- 所有用户可见文字 → `font-serif`（Noto Serif SC）
- 技术标识/代码片段 → `font-mono`
- 禁止：Inter、Roboto、Arial 作主字体

### 2.2 排版比例

| 用途 | Tailwind 类 |
|------|-------------|
| 页面标题 | `text-xl sm:text-2xl font-serif font-bold text-black` |
| 章节标题 | `text-lg font-serif font-semibold text-black` |
| 卡片标题 | `text-base font-serif font-semibold text-black` |
| 正文 | `text-sm font-serif text-black` 或 `text-gray-600` |
| 次要信息 | `text-xs text-gray-500` |
| 技术ID | `text-[10px] text-gray-400 font-mono` |

### 2.3 CSS 变量（`src/index.css :root`）

```css
:root {
  /* 品牌色 */
  --brand-primary: #3B82F6;
  --brand-dark: #1E40AF;
  --brand-light: #DBEAFE;

  /* 强调色 */
  --accent-primary: #0EA5E9;
  --accent-success: #10B981;
  --accent-warning: #F59E0B;
  --accent-error: #EF4444;
  --accent-info: #3B82F6;

  /* 背景色 */
  --bg-page: #F8FAFC;
  --bg-container: #FFFFFF;
  --bg-secondary: #F1F5F9;
  --bg-hover: #F1F5F9;
  --bg-selected: #E0F2FE;
  --bg-disabled: #E2E8F0;
  --bg-footer: #0E2E4F;

  /* 文字色 */
  --text-primary: #0F172A;
  --text-secondary: #475569;
  --text-tertiary: #94A3B8;
  --text-disabled: #CBD5E1;
  --text-inverse: #FFFFFF;

  /* 边框色 */
  --border-default: #E2E8F0;
  --border-hover: #CBD5E1;
  --border-focus: #3B82F6;
  --border-active: #0EA5E9;

  /* 阴影 */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.06);
  --shadow-xl: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);

  /* 圆角（三级简化体系） */
  --radius-md: 12px;   /* 默认：卡片/按钮/输入框（70%） */
  --radius-lg: 16px;   /* 大圆角：模态框/下拉框（20%） */
  --radius-full: 9999px; /* 全圆：头像/chip/徽章（10%） */

  /* 过渡 */
  --transition-fast: 150ms ease;
  --transition-normal: 200ms ease;
  --transition-slow: 300ms ease;
}
```

### 2.4 Tailwind Config 完整配置

```javascript
// tailwind.config.js
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        serif: ['Noto Serif SC', 'STSong', 'SimSun', 'serif'],
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
      },
      colors: {
        brand: {
          primary: 'var(--brand-primary)',
          dark: 'var(--brand-dark)',
          light: 'var(--brand-light)',
        },
        accent: {
          primary: 'var(--accent-primary)',
          success: 'var(--accent-success)',
          warning: 'var(--accent-warning)',
          error: 'var(--accent-error)',
        },
        surface: {
          page: 'var(--bg-page)',
          container: 'var(--bg-container)',
          secondary: 'var(--bg-secondary)',
          hover: 'var(--bg-hover)',
          selected: 'var(--bg-selected)',
        },
        content: {
          primary: 'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          tertiary: 'var(--text-tertiary)',
          inverse: 'var(--text-inverse)',
        },
        line: {
          default: 'var(--border-default)',
          hover: 'var(--border-hover)',
          focus: 'var(--border-focus)',
          active: 'var(--border-active)',
        },
        black: '#000000',
        white: '#FFFFFF',
      },
      borderRadius: {
        sm: 'var(--radius-md)',   // deprecated → maps to md
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
        xl: 'var(--radius-lg)',   // deprecated → maps to lg
        full: 'var(--radius-full)',
      },
      boxShadow: {
        sm: 'var(--shadow-sm)',
        md: 'var(--shadow-md)',
        lg: 'var(--shadow-lg)',
        xl: 'var(--shadow-xl)',
      },
    },
  },
  plugins: [],
}
```

---

## 三、配色场景选择

**两种场景，明确区分**：

| 场景 | 使用时机 | 核心色调 |
|------|----------|---------|
| **产品内页（默认）** | 话题列表/详情/配置/库页面 | 黑+白+灰系，`black`/`white`/`gray-*` |
| **官网/主页** | Landing page、营销页面 | 蓝绿渐变，`#5B9BD5` + `#9FD4C4` |

**不确定时，始终使用产品内页风格。**

### 产品内页配色速查

```
主色/CTA按钮：    #000000 (black)
页面背景：        #FFFFFF (white)
卡片边框：        gray-200 (#E2E8F0)
悬停边框：        gray-300
选中/焦点边框：   black
主文字：          text-black
描述文字：        text-gray-600 / text-gray-700
次要文字：        text-gray-500
技术标识：        text-gray-400 font-mono
禁用态：          text-gray-400 opacity-50
选中背景：        bg-gray-100
悬停背景：        bg-gray-50
```

### 官网/主页配色速查

```css
/* 主题色 */
--color-primary: #5B9BD5;     /* 淡蓝 */
--color-secondary: #9FD4C4;   /* 淡绿 */
--color-dark: #0E2E4F;        /* 深海蓝（footer/heading） */

/* 渐变 */
--gradient-primary: linear-gradient(135deg, #5B9BD5 0%, #9FD4C4 100%);
--gradient-dark: linear-gradient(135deg, #0E2E4F 0%, #0A1F35 100%);

/* 标题渐变文字 */
.gradient-text {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### 语义状态色（需要明确状态区分时）

| 状态 | 类 | 用途 |
|------|-----|------|
| 进行中/Open | `bg-green-50 text-green-700` | 话题状态 |
| 运行中 | `bg-blue-50 text-blue-600` | 讨论进行中 |
| 已完成 | `bg-gray-100 text-gray-600` | 已结束 |
| 警告 | `bg-yellow-50 text-yellow-700` | 提示 |
| 错误 | `bg-red-50 text-red-600` | 错误状态 |

> 语义色统一使用 `StatusBadge` 组件封装，不允许各处自行映射。

---

## 四、圆角系统（三级简化体系）

| 级别 | Tailwind | CSS 变量 | 值 | 场景 | 占比 |
|------|----------|----------|----|------|------|
| **默认** | `rounded-lg` | `--radius-md` | 12px | 卡片/按钮/输入框/所有通用容器 | 70% |
| **大圆角** | `rounded-xl` | `--radius-lg` | 16px | 模态框/下拉框/缩略图 | 20% |
| **全圆** | `rounded-full` | `--radius-full` | 9999px | 头像/Chip/徽章/过滤按钮 | 10% |

**废弃**：`rounded-sm`、`rounded-md`（合并到 lg）、`rounded-2xl`（合并到 xl）
**禁止**：任何自定义值 `rounded-[XXpx]`

---

## 五、组件代码模板

### 5.1 按钮

```tsx
// 主按钮（CTA）
<button className="bg-black text-white px-4 py-1.5 rounded-lg text-sm font-serif font-medium hover:bg-gray-900 transition-colors disabled:opacity-50">
  操作
</button>

// 次按钮
<button className="border border-gray-200 bg-white text-black px-4 py-1.5 rounded-lg text-sm font-serif font-medium hover:border-black transition-colors disabled:opacity-50">
  次要操作
</button>

// 文字按钮（返回/取消）
<button className="text-sm font-serif text-gray-500 hover:text-black transition-colors">
  返回
</button>

// 图标按钮
<button className="p-2 rounded-lg text-gray-600 hover:text-black hover:bg-gray-100 transition-colors" aria-label="打开菜单">
  <Icon />
</button>

// 圆形操作按钮（+ / ×）
<button className="w-7 h-7 rounded-full flex items-center justify-center bg-black text-white hover:bg-gray-800 transition-colors" aria-label="添加">
  +
</button>
```

### 5.2 卡片

```tsx
// 标准内容卡片（可点击）
<div className="flex flex-col gap-1 px-4 py-3 rounded-lg border border-gray-200 bg-white hover:border-gray-300 hover:bg-gray-50 transition-colors cursor-pointer w-full text-left">
  <span className="text-base font-serif font-semibold text-black truncate">标题</span>
  <span className="text-sm font-serif text-gray-600 line-clamp-2">描述内容</span>
  <span className="text-xs text-gray-500">元数据</span>
</div>

// 话题列表项
<div className="border border-gray-200 rounded-lg p-4 sm:p-6 hover:border-black transition-colors active:bg-gray-50 cursor-pointer">
  {/* 内容 */}
</div>

// 选中态卡片
<div className={`rounded-lg border px-4 py-3 transition-colors cursor-pointer ${
  isSelected
    ? 'border-gray-400 bg-gray-100'
    : 'border-gray-200 bg-white hover:border-gray-300 hover:bg-gray-50'
}`}>
  {/* 内容 */}
</div>
```

### 5.3 输入控件

```tsx
// 输入框
<input
  className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm font-serif focus:border-black focus:outline-none transition-colors placeholder:text-gray-400"
  placeholder="输入内容"
/>

// 多行文本
<textarea
  className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm font-serif focus:border-black focus:outline-none transition-colors resize-none"
  rows={4}
/>

// 标签
<label className="block text-sm font-serif font-medium text-black mb-2">
  字段名称
</label>

// 表单组合
<div className="flex flex-col gap-6">
  <div>
    <label className="block text-sm font-serif font-medium text-black mb-2">标题</label>
    <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm font-serif focus:border-black focus:outline-none transition-colors" />
  </div>
</div>
```

### 5.4 导航（TopNav）

```tsx
<nav className="h-14 bg-white border-b border-gray-200 flex items-center px-4 sm:px-6 justify-between">
  {/* Logo */}
  <span className="text-base font-serif font-bold text-black">他山</span>

  {/* 桌面端链接 */}
  <div className="hidden md:flex items-center gap-6">
    <a className="text-sm font-serif text-black font-medium">激活页</a>
    <a className="text-sm font-serif text-gray-500 hover:text-black transition-colors">其他页</a>
  </div>

  {/* CTA */}
  <button className="bg-black text-white px-4 py-1.5 rounded-lg text-sm font-serif font-medium hover:bg-gray-900 transition-colors">
    登录
  </button>

  {/* 移动端汉堡按钮 */}
  <button className="md:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100" aria-label="打开菜单">
    ☰
  </button>
</nav>
```

### 5.5 模态框

```tsx
// 背景遮罩
<div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
  {/* 内容容器 */}
  <div className="bg-white rounded-xl shadow-xl border border-gray-200 max-w-2xl w-full max-h-[85vh] flex flex-col">
    {/* 头部 */}
    <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
      <h2 className="text-lg font-serif font-semibold text-black">标题</h2>
      <button className="text-gray-500 hover:text-black text-2xl transition-colors" aria-label="关闭">×</button>
    </div>
    {/* 内容（可滚动） */}
    <div className="flex-1 overflow-auto px-6 py-4">
      {/* 内容 */}
    </div>
    {/* 底部操作 */}
    <div className="px-6 py-4 border-t border-gray-200 flex justify-end gap-3">
      <button className="text-sm font-serif text-gray-500 hover:text-black">取消</button>
      <button className="bg-black text-white px-4 py-1.5 rounded-lg text-sm font-serif font-medium hover:bg-gray-900">确认</button>
    </div>
  </div>
</div>
```

### 5.6 Tab 面板

```tsx
// Tab 栏
<div className="flex gap-1 border-b border-gray-200 -mb-px overflow-x-auto scrollbar-hide">
  {tabs.map(tab => (
    <button
      key={tab.id}
      className={`px-4 py-2 text-sm font-serif whitespace-nowrap border-b-2 transition-colors ${
        activeTab === tab.id
          ? 'text-black font-medium border-black'
          : 'text-gray-500 hover:text-gray-700 border-transparent'
      }`}
      onClick={() => setActiveTab(tab.id)}
    >
      {tab.label}
    </button>
  ))}
</div>

// Tab 内容（带方向动画）
<div className={activeDirection === 'right' ? 'animate-slide-in-right' : 'animate-slide-in-left'}>
  {/* 内容 */}
</div>
```

### 5.7 Chip（标签/过滤器）

```tsx
// 可移除的 Chip（移动端 pill，桌面端 card）
<div className="inline-flex items-center gap-1.5 rounded-full sm:rounded-lg px-2.5 sm:px-3 py-1 sm:py-2 text-xs sm:text-sm bg-gray-100 sm:bg-white border border-gray-200 sm:hover:border-gray-400 sm:hover:bg-gray-50 transition-colors">
  <span className="font-serif text-black truncate max-w-[120px] sm:max-w-[200px]">标签文字</span>
  <button
    className="w-5 h-5 sm:w-7 sm:h-7 rounded-full flex items-center justify-center text-gray-400 hover:text-black hover:bg-gray-200 transition-colors flex-shrink-0"
    aria-label="移除"
  >
    ×
  </button>
</div>
```

### 5.8 头像（Expert Avatar）

```tsx
// 初始字母头像
<div className="w-6 h-6 rounded-full bg-black text-white flex items-center justify-center font-serif text-xs flex-shrink-0">
  {name.charAt(0).toUpperCase()}
</div>

// 大头像
<div className="w-10 h-10 rounded-full bg-black text-white flex items-center justify-center font-serif text-base">
  {name.charAt(0).toUpperCase()}
</div>
```

### 5.9 状态徽章（StatusBadge）

```tsx
const statusConfig = {
  open:      { bg: 'bg-green-50',  text: 'text-green-700',  label: '进行中' },
  running:   { bg: 'bg-blue-50',   text: 'text-blue-600',   label: '运行中' },
  completed: { bg: 'bg-gray-100',  text: 'text-gray-600',   label: '已完成' },
  pending:   { bg: 'bg-yellow-50', text: 'text-yellow-700', label: '待处理' },
  error:     { bg: 'bg-red-50',    text: 'text-red-600',    label: '错误' },
}

// 使用
<span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-serif font-medium ${statusConfig[status].bg} ${statusConfig[status].text}`}>
  {statusConfig[status].label}
</span>
```

---

## 六、布局与间距约定

### 容器宽度

```tsx
// 内容库页面（技能/MCP/专家）
<div className="max-w-6xl mx-auto px-4 sm:px-6">

// 表单/详情页
<div className="max-w-2xl mx-auto px-4 sm:px-6">

// 列表页（话题列表）
<div className="max-w-4xl mx-auto px-4 sm:px-6">
```

### 垂直节奏

```
页面内边距：  py-6 sm:py-8
标题到内容：  mb-6 sm:mb-8
卡片间距：    gap-4
表单字段间：  gap-6
主内容偏移：  pt-14 (TopNav 高度)
```

### Safe Area（移动端）

```css
/* index.css */
body {
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}
/* 底部内容 */
.pb-safe { padding-bottom: env(safe-area-inset-bottom); }
```

### 响应式模式速查

| 场景 | 移动端 | 桌面端 |
|------|--------|--------|
| 内边距 | `px-4 py-6` | `sm:px-6 sm:py-8` |
| 标题 | `text-xl` | `sm:text-2xl` |
| 导航 | 汉堡 + 下拉 | `md:flex` 横向链接 |
| Chip | `rounded-full` 紧凑 | `sm:rounded-lg` 展开 |
| 网格 | 单列 | `sm:grid-cols-2 lg:grid-cols-3` |

---

## 七、动画与过渡

**动画统一定义在 `index.css` 的 `@layer utilities` 中。**

```css
/* index.css */
@layer utilities {
  .animate-blink {
    animation: blink 1s step-end infinite;
  }
  .animate-fade-in {
    animation: fadeIn 0.2s ease-out;
  }
  .animate-slide-in-right {
    animation: slideInRight 0.2s ease-out;
  }
  .animate-slide-in-left {
    animation: slideInLeft 0.2s ease-out;
  }
}

@keyframes blink { 50% { opacity: 0; } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideInRight { from { opacity: 0; transform: translateX(16px); } to { opacity: 1; transform: translateX(0); } }
@keyframes slideInLeft  { from { opacity: 0; transform: translateX(-16px); } to { opacity: 1; transform: translateX(0); } }
```

**过渡规则**：
- 常规状态变化：`transition-colors`（避免 transition-all 引起布局抖动）
- 进入/离开动画：仅 Tab 切换和模态框
- 触摸优化：`touch-manipulation`（消除 300ms 延迟）

---

## 八、Markdown 内容渲染

包裹 `react-markdown` 输出用 `.markdown-content`：

```css
/* index.css */
@layer components {
  .markdown-content h1 { @apply text-2xl font-serif font-bold text-black border-b border-black pb-2 mb-4; }
  .markdown-content h2 { @apply text-xl font-serif font-semibold text-black border-b border-gray-200 pb-1 mb-3; }
  .markdown-content h3 { @apply text-lg font-serif font-semibold text-black mb-2; }
  .markdown-content p  { @apply text-sm font-serif text-gray-700 leading-relaxed mb-4; }
  .markdown-content ul { @apply pl-6 mb-4; }
  .markdown-content ol { @apply pl-6 mb-4 list-decimal; }
  .markdown-content li { @apply text-sm font-serif text-gray-700 mb-2; }
  .markdown-content a  { @apply text-black underline decoration-1 hover:decoration-2; }
  .markdown-content code:not(pre code) { @apply bg-gray-100 px-1 py-0.5 text-sm font-mono rounded; }
  .markdown-content pre { @apply bg-gray-900 text-white p-4 rounded-lg overflow-x-auto mb-4; }
  .markdown-content pre code { @apply bg-transparent text-white text-sm font-mono; }
  .markdown-content blockquote { @apply border-l-2 border-black pl-4 text-gray-600 italic mb-4; }
  .markdown-content table { @apply w-full border border-gray-200 rounded-lg overflow-hidden mb-4; }
  .markdown-content th { @apply bg-gray-50 font-serif font-semibold text-black px-4 py-2 text-left border-b border-gray-200; }
  .markdown-content td { @apply px-4 py-2 text-sm font-serif text-gray-700 border-b border-gray-100; }
}
```

---

## 九、无障碍（a11y）约定

```tsx
// 图标按钮必须有 aria-label
<button aria-label="关闭菜单">×</button>

// 可展开元素必须有 aria-expanded
<button aria-expanded={isOpen} aria-label="切换菜单">

// 非 button 但可点击的 div
<div
  role="button"
  tabIndex={0}
  onKeyDown={e => e.key === 'Enter' && handleClick()}
  onClick={handleClick}
>

// 下拉选择键盘支持
onKeyDown={(e) => {
  if (e.key === 'ArrowDown') selectNext();
  if (e.key === 'ArrowUp')   selectPrev();
  if (e.key === 'Escape')    close();
}}

// 焦点样式（不允许只用 outline-none 无替代）
className="focus:border-black focus:outline-none"  // ✅ 用边框替代 outline
```

---

## 十、禁止清单（与 frontend-brand-guard.mdc 同步）

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
```

---

## 十一、权威文档路径（需精确参数时必读）

```
/Users/boyuan/aiwork/0310_huaxiang\项目群\Tashan-TopicLab\docs\design\
├── frontend-design-guide.md       ← 完整设计语言权威文档
├── color-system.md                ← 配色变量完整列表
├── shape-system.md                ← 圆角系统 + 组件对照清单
├── tashan-homepage-style-guide.md ← 官网/主页风格（蓝绿渐变系）
└── style-refactor-checklist.md    ← 页面/组件重构优先级

前端工程文件：
/Users/boyuan/aiwork/0310_huaxiang\项目群\Tashan-TopicLab\frontend\
├── tailwind.config.js   ← Tailwind 配置（含 CSS 变量映射）
├── src\index.css        ← 全局样式、CSS 变量定义、动画
└── src\components\      ← 现有组件参考实现
```

---

## 变更记录

### 2026-03-20 — 初始创建 v1.0

**根因**：`frontend-brand-guard.mdc`（约束层）创建后，用户指出 Rule 只是约束，所有可复用的设计系统内容应当以 Skill 形式沉淀，供 `role-前端开发`、`role-UI设计师` 主动调用。当前缺少前端品牌 Skill 层，AI 执行前端任务时需分散查阅多个 docs 文件，效率低且一致性无法保证。

**修改内容**：
- 新增：本 Skill 全部内容（首次创建）
- 覆盖范围：技术框架 / 设计令牌（字体/颜色/CSS变量/Tailwind配置）/ 配色场景区分 / 圆角系统 / 11类组件代码模板 / 布局间距 / 动画过渡 / Markdown渲染 / a11y约定 / 禁止清单

**验证结果**：
- 正向验证：触发前端组件编写任务，AI 应直接从本 Skill 获取代码模板，无需逐一查阅 docs（待真实场景验证）
- 负向验证：非前端任务不受影响（待验证）

**验证状态**：🔵 待验证
