---
name: ai-image-generator
description: AI配图能力层 Skill。任何需要生成信息图的任务都调用此 Skill，而不是自行调用 API。包含：模型选择、API调用、多视角草图流程、风格库引用、配图索引联动。触发词：「需要绘图」「生成配图」「画一张图」「制作信息图」「根据这段文字画图」「图片提示词」。
---

# AI配图能力 Skill

> 这是一个**能力层 Skill**，被其他 Skill 调用，不直接面向用户任务。
> 任何需要生成图片的 Skill 都应该引用本 Skill，而不是自行嵌入 API 细节。

---

## 模型与 API

| 优先级 | 模型 | 适用场景 | API Key |
|---|---|---|---|
| **首选** | `qwen-image-2.0-pro` | 含中文文字的信息图、结构图 | `sk-68b70d6863b94c299ecd27e9d49b41ba` |
| **次选** | `wan2.6-t2i` | 纯视觉风格图（无需复杂中文文字排版）| 同上（dashscope）|
| 备用 | `gpt-image-1`（DMXAPI）| 英文为主的极简图 | `sk-wzI4JscScaJ1pxVKRQ4qxmJcpH1OIgsqshlP55Tq6NtZ3H5p` |

**选择原则**：信息图/结构图/有中文标注 → 用 `qwen-image-2.0-pro`；纯视觉风格图 → 用 `wan2.6-t2i`。

**`wan2.6-t2i` API 调用**（endpoint 不同）：
```python
url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis'
body = {'model': 'wan2.6-t2i', 'input': {'prompt': 'PROMPT'}, 'parameters': {'size': '1024*1024', 'n': 1}}
```

⚠️ **已知问题**：DMXAPI 上的 DALL-E 3 有较高概率网络超时（实测超时案例：2026-03-20 向日葵调研任务）。遇到超时时直接切换 qwen-image-2.0-pro，不要反复重试 DALL-E 3。

### qwen-image-2.0-pro API 调用

```python
import requests, base64

API_KEY = 'sk-68b70d6863b94c299ecd27e9d49b41ba'
ENDPOINT = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation'

headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
payload = {
    "model": "qwen-image-2.0-pro",
    "input": {"messages": [{"role": "user", "content": [{"text": "你的提示词"}]}]},
    "parameters": {
        "n": 1,
        "watermark": False,
        "prompt_extend": True,
        "size": "1024*1024"   # 标准图；小图同尺寸，HTML 中用 max-width: 65% 控制
    }
}

resp = requests.post(ENDPOINT, headers=headers, json=payload, timeout=120)
img_url = resp.json()['output']['choices'][0]['message']['content'][0]['image']

# 下载并保存（URL 24 小时有效，立即保存）
ir = requests.get(img_url, timeout=60)
with open('output.png', 'wb') as f:
    f.write(ir.content)
```

⚠️ **限速处理**：遇到 429 时等待 30 秒后重试，最多重试 3 次。

---

## 风格库

风格库文件：`_内部总控/产品定义/图片风格库.md`（10种风格，当前文章使用 **S03**）

**S03 标准提示词前缀**（适合大多数中文信息图）：
```
简洁专业的信息图，适合微信文章，白色背景。[内容描述]
深蓝色#1a2f5e和橙色#e8622c为主色，圆角矩形，清晰中文标注，整体简洁商务风格。
```

---

## 绘图流程（每张图必须走完）

### Step 1：分析段落逻辑

在开始绘图之前，必须先回答：
1. 这张图对应手稿哪个段落？（定位行号/小节）
2. 这段文字背后想传达的**核心图像**是什么？（一句话）
3. 这张图如果画成功，读者读完会在脑子里形成什么**空间/结构印象**？
4. 图不只是文字映射——它应该补充文字没说完的部分，或把文字的逻辑结构可视化

### Step 2：从多个视角设计草图

对每张图，至少从 **2 个独立逻辑视角**各写一条提示词：
- 视角A：[逻辑A]，提示词：`...`
- 视角B：[逻辑B]，提示词：`...`

⛔ **禁止**：只写一条提示词直接生成，跳过视角分析

### Step 3：调用 API 生成

按上方 API 调用格式，对每个视角各生成一张图。

### Step 4：更新配图索引

生成完毕后，必须在对应文章的 `配图索引_[文章名].md` 中追加/更新条目：
```
| 图片文件名 | 对应段落 | 段落核心主旨 | 提示词摘要 | 状态 |
```

如果文章还没有配图索引，立即创建（模板：`.cursor/skills/wechat-article-writer/templates/配图索引模板.md`）。

### Step 5：嵌入到 HTML

- **大图**（核心结构图）：`max-width: 100%`
- **小图**（辅助说明图、循环图、对比图）：`max-width: 65%`

```html
<!-- 大图 -->
<p style="text-align:center; margin: 24px 0;">
  <img src="data:image/png;base64,{BASE64}" alt="描述" style="max-width:100%; border-radius:8px;">
</p>

<!-- 小图 -->
<p style="text-align:center; margin: 8px 0 24px;">
  <img src="data:image/png;base64,{BASE64}" alt="描述" style="max-width:65%; border-radius:8px;">
</p>
```

---

## 图片大小原则

| 图类型 | 用途 | HTML 宽度 |
|---|---|---|
| 大图 | 核心结构图（坐标系、架构图、飞轮图）| 100% |
| 小图 | 辅助说明（循环图、对比图、路径图）| 65% |

---

## 图的质量原则

1. **不是文字映射**：图应该传达文字没法直接说的**空间/结构关系**
2. **完整的故事**：读图应有额外收获，不是重读文字
3. **可视化目的是传达图像**：读完图，读者脑中应形成一个清晰的形象
4. **提示词足够清晰**：描述节点数量、颜色、连接关系、箭头方向、副文字内容

---

## 与其他 Skill 的关系

| 调用方 | 调用方式 |
|---|---|
| `wechat-article-writer` | Step 4（配图生成）引用本 Skill |
| `role-UI设计师` | 需要可视化时引用本 Skill |
| `role-产品经理` | 需要配图说明产品结构时引用本 Skill |
| 其他需要绘图的 Skill | 同上 |

---

## 变更记录

### v1.0 — 2026-03-20 — 初始创建（从 wechat-article-writer 提取）

**根因**：绘图 API 细节和多视角草图流程只存在于 wechat-article-writer，其他 Skill 无法复用。根本原因是 Skill 体系缺少「能力层」，导致执行细节散落在流程层 Skill 里。

**修改内容**：
- 新建：ai-image-generator Skill（能力层）
- 从 wechat-article-writer Step 4 提取：API 配置、多视角流程、风格库引用
- wechat-article-writer Step 4 改为引用本 Skill

**验证状态**：🔵 待验证
