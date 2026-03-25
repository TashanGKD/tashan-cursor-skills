---
name: article-image-styles
description: 管理他山公众号的配图风格库，提供风格模板调用和新风格沉淀。触发词：调用风格库/用XX风格/存入风格库/更新风格模板/风格库有哪些风格。
---

# 配图风格库管理（article-image-styles）

> 定位：wechat-article-writer 和 article-image-angles 的底层支撑。
> 核心价值：把「每次从零写提示词」变成「从经过验证的风格模板库调用」，保证风格一致性。

---

## 风格库文件位置

路径：`_内部总控/产品定义/配图风格库.md`（若不存在则初始化）

---

## 激活后立即执行

### 查询模式（触发词含「有哪些风格」「调用风格」「风格库」）

Step 1  读取风格库文件：`_内部总控/产品定义/配图风格库.md`
Step 2  若文件不存在，执行初始化流程（见下方「初始风格库」章节），写入文件后继续
Step 3  输出所有可用风格的名称、适用场景和关键词摘要
Step 4  用户选择后，返回完整提示词模板（供 article-image-angles 或 wechat-article-writer 使用）

### 新增/更新模式（触发词含「存入风格库」「更新风格」「新增风格」）

Step 1  获取用户提供的风格名称、适用场景、提示词
Step 2  读取现有风格库，检查是否存在同名风格
Step 3  若已有同名风格，询问用户：覆盖 / 新增版本 / 取消
Step 4  按选择追加写入风格库文件（不覆盖已有内容，版本追加）
Step 5  确认写入成功，告知用户新风格已入库

---

## 风格库条目格式

```
## [风格名称]

**适用场景**：[什么类型的文章适合用这种风格]
**关键词**：[风格标签，如：极简/商务/温暖/科技感]
**基础提示词模板**：
[提示词内容，含占位符如 {{主题}}、{{色调}}]

**使用案例**：[过去用这个风格生成的文章配图列表，初始为空]
**版本**：v1.0 | [日期]
```

---

## 初始风格库（首次运行时初始化写入风格库文件）

### 极简线条风

**适用场景**：抽象概念、框架类、方法论类文章
**关键词**：极简、线条、几何、思考感、留白
**基础提示词模板**：
minimalist line art, {{主题}} concept visualization, clean geometric shapes, black and white with subtle {{色调}} accent, white background, editorial style, no text, high contrast, vector aesthetic

**使用案例**：（待补充）
**版本**：v1.0 | 2026-03-19

---

### 温暖场景风

**适用场景**：人文、情感、故事类、人物成长类文章
**关键词**：温暖、柔和、生活感、人文、情绪
**基础提示词模板**：
warm lifestyle photography style illustration, {{主题}} scene, soft natural light, earthy tones with warm {{色调}}, cozy atmosphere, human element, story-telling composition, gentle bokeh, no text

**使用案例**：（待补充）
**版本**：v1.0 | 2026-03-19

---

### 科技蓝绿风

**适用场景**：AI、产品、数字化、科技趋势类文章（与他山品牌色呼应）
**关键词**：科技感、蓝绿、数字、未来感、信息可视化
**基础提示词模板**：
futuristic tech visualization, {{主题}} concept, deep navy blue and teal gradient, glowing particle network, data flow aesthetic, clean digital interface elements, no text, cinematic lighting, 16:9 composition

**使用案例**：（待补充）
**版本**：v1.0 | 2026-03-19

---

## 与其他 Skill 的关系

| Skill | 关系 |
|---|---|
| `wechat-article-writer` | 在配图生成步骤调用本 Skill 的风格库，而不是从零写提示词 |
| `article-image-angles` | 确定配图角度后，调用本 Skill 获取对应风格的提示词模板 |
| `article-proofreading` | 无直接关系 |

---

## 变更记录

### v1.0 — 2026-03-19 — 初始创建

**根因**：wechat-article-writer 每次配图从零写提示词，风格不一致，已验证的好风格无法复用。缺失 Skill 信号（信号 E），本次新建填补该空白。

**经验核心**：建立风格库文件作为底层资产，查询模式和新增模式分离，所有配图生成类 Skill 统一调用风格库。

**修改内容**：
- 新建：article-image-styles v1.0，含三种初始风格（极简线条/温暖场景/科技蓝绿）

**验证结果**：
- 正向验证：下次写文章配图时，wechat-article-writer 应调用本 Skill 而非从零写提示词 → 待验证
- 负向验证：顺利执行已有配图流程时不额外触发本 Skill → 待验证

**验证状态**：🔵 待验证
