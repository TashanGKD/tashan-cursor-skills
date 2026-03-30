"""
README 配图生成脚本
使用 qwen-image-2.0-pro 生成 tashan-cursor-skills README 所需的所有架构图
"""
import os
import time
import requests

API_KEY = "sk-68b70d6863b94c299ecd27e9d49b41ba"
ENDPOINT = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
OUT_DIR = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT_DIR, exist_ok=True)

STYLE = (
    "简洁专业的技术架构信息图，白色背景。"
    "主色调：深蓝色 #1a3a6e 和亮蓝色 #3b82f6；"
    "辅色：绿色 #10b981（成功/输出）、橙色 #f59e0b（信号/警告）、紫色 #7c3aed（认知层）；"
    "圆角矩形节点，箭头清晰带方向，字体清晰，所有标注均为中文，"
    "整体简约专业，排版工整，适合技术文档和 GitHub README。"
)

IMAGES = [
    {
        "name": "harness-architecture",
        "prompt": (
            STYLE +
            "【图名：Agent Harness 架构全景图】"
            "画一张三层架构全景图，展示 Agent Harness 的完整结构。"
            "最上层（紫色区域）标注「记忆层 Memory Layer」，包含四个子模块："
            "「L1 系统性文档」「L1.5 底层原则库」「L2 认知碎片」「L3 原始记录」，"
            "旁边注明「存储为什么」。"
            "中间层（绿色区域）标注「工作层 Work Layer」，包含四个子模块："
            "「产品文档」「代码实现」「测试/部署」「决策追踪台」，"
            "旁边注明「产出价值」。"
            "最下层（蓝色区域）标注「执行层 Execution Layer」，包含三个子模块："
            "「Rules 32条约束」「Skills 95个流程」「SubAgents 18个验证者」，"
            "旁边注明「知道怎么做」。"
            "三层之间有双向箭头连接，标注「六条通路形成自我进化飞轮」。"
            "图右侧有一个小标注框：「每次任务 → 信号 → 三层同步更新 → Harness 复利增长」。"
            "图标题在顶部：「三大闭环 · Self-Evolving Agent Harness」"
        ),
    },
    {
        "name": "three-loop-pathways",
        "prompt": (
            STYLE +
            "【图名：三大闭环与六条通路】"
            "画一张三个嵌套循环（三个大矩形框从上到下排列）的架构图。"
            "第一个矩形框（最上方，紫色边框）：「Loop 2 记忆层」"
            "内容：L1文档 | L1.5原则库 | L2碎片 | L3记录"
            "第二个矩形框（中间，绿色边框）：「Loop 3 工作层」"
            "内容：产品文档 | 代码 | 测试 | 追踪台"
            "第三个矩形框（最下方，蓝色/橙色边框）：「Loop 1 执行层」"
            "内容：Rules（始终在场）| Skills（按需加载）| SubAgents（独立视角）"
            "三个矩形之间用六条带标注的箭头连接，左侧向下三条："
            "A（认知激活工作）、C（Skill支撑执行）左侧向下，"
            "E（认知驱动Skill更新）穿越中间向下。"
            "右侧向上三条：B（工作产生洞见）、D（工作暴露缺口）向上，F（失败触发反思）向上。"
            "箭头均带颜色和简短标注。"
            "图底部有一行小字：「六条通路 = 自我进化飞轮，用得越多 Harness 越强」"
        ),
    },
    {
        "name": "signal-flywheel",
        "prompt": (
            STYLE +
            "【图名：D5信号路由飞轮】"
            "画一张中心辐射型信息图（飞轮/蜘蛛网式布局）。"
            "中心圆形节点标注：「任务执行完成\nD5信号感知」（深蓝色背景白字）。"
            "从中心向外辐射出5条路径，每条路径末端是一个矩形节点："
            "路径1（橙色）→「A信号 踩坑」→ 「立即追加到\nSkill步骤警告」"
            "路径2（紫色）→「B信号 意外行为」→ 「PENDING-SKILLS\n等待体系健检」"
            "路径3（绿色）→「D信号 洞见」→ 「L2碎片 → L1整合\n→ Skill D0-B更新」"
            "路径4（蓝色）→「E信号 流程缺口」→ 「skill-designer\n建新Skill」"
            "路径5（红色）→「G信号 结构根因」→ 「人工确认\n→ 规范更新」"
            "每条路径末端节点下方有小字注明效果。"
            "图外圈有一个循环箭头标注：「飞轮效应：每次任务 → 至少一条改进 → Harness 复利增长」"
        ),
    },
    {
        "name": "scenario1-new-feature",
        "prompt": (
            STYLE +
            "【图名：场景一 · 新功能开发完整闭环】"
            "画一张从左到右的水平流程图，展示新功能开发的完整闭环。"
            "分三个区域：顶部区域、主流程区域、底部信号区域。"
            ""
            "【顶部区域，紫色背景小框】：「通路A：认知根激活」"
            "内容：「role-产品经理 读取 L1认知文档 → 确认认知根 → 带着原则执行」"
            ""
            "【主流程区域，水平从左到右】："
            "①「产品定义\nrole-PM」→ 菱形「关卡A\nuser-simulator\n用户视角」→"
            "②「技术架构\nrole-架构师」→ 菱形「关卡B\narch-destroyer\n破坏者视角」→"
            "③「并行开发\n前端+后端+AI」→ 菱形「关卡C\nverifier\n独立验证」→"
            "④「上线\nDevOps」"
            "关卡菱形用橙色，正常节点用蓝色圆角矩形。"
            "每个关卡下方标注：PASS继续 / FAIL返回修改"
            ""
            "【底部信号区域，三个分支向下】："
            "从④上线节点向下引出三条分支："
            "「A信号」→「追加 Skill 踩坑警告」"
            "「D信号」→「L2碎片 → L1整合 → Skill更新」"
            "「E信号」→「PENDING-SKILLS → 建新Skill」"
            "底部有循环箭头，从信号区域回到①，标注「下次执行读到更新后的Skill」"
        ),
    },
    {
        "name": "scenario2-bug-fix",
        "prompt": (
            STYLE +
            "【图名：场景二 · Bug修复TDD完整闭环】"
            "画一张垂直向下的流程图，展示 Bug 修复的完整循环。"
            ""
            "【顶部入口】：椭圆「发现问题」"
            "↓"
            "【分类节点】：矩形「issue-tracker 分类」"
            "→ 左分支：「产品设计问题 → 产品追踪台」（橙色）"
            "→ 右分支（主流程）：「技术实现问题 → 技术追踪台」（蓝色）"
            "↓（右分支继续向下）"
            "【协调者节点】：矩形「bug-fix-loop-coordinator\n读追踪台 按P0→P1→P2顺序」"
            "↓"
            "【循环框（虚线边框，标注 循环×N）】内部包含："
            "「fixer 子智能体」→「① 复现Bug（写失败测试）」→「② 修复代码（让测试通过）」→「③ CI验证」→「④ 更新追踪台」"
            "循环框右侧有判断：「P0/P1是否清零？」→ 否 → 继续循环"
            "↓（P0/P1清零）"
            "【验证节点】：矩形「verifier 子智能体\n独立回归验证」（绿色）"
            "↓"
            "【完成节点】：椭圆「可上线」（绿色）"
            ""
            "右侧竖排列出三个信号输出："
            "「G信号 → 规范更新 → 下次架构避免」"
        ),
    },
    {
        "name": "scenario3-cognitive",
        "prompt": (
            STYLE +
            "【图名：场景三 · 认知洞见积累完整闭环】"
            "画一张从上到下的瀑布式流程图，展示一个认知洞见如何从原始想法变成体系能力。"
            ""
            "【第一层，橙色】：「原始洞见 / 日常想法」"
            "例：「发现AI长对话超过20轮会忘记早期约定」"
            "↓ cognitive-capture-fragment"
            "【第二层，蓝色】：「L2 认知碎片」"
            "内容：title / domain / insight / evidence / generalizability 五个字段"
            "↓ cognitive-integrate-fragments（积累多条后）"
            "【第三层，蓝色深色】：「L1 系统性文档」"
            "内容：「上下文工程与智能体能力参考手册」精准追加"
            "↓ cognitive-extract-principle（发现跨领域规律）"
            "【第四层，紫色】：「L1.5 底层原则库」"
            "内容：P_new「AI长对话的上下文稳定性原则：关键约定必须周期性重注入」"
            "↓ [通路E] rg搜索依赖此文档的Skill"
            "【第五层，绿色】：「Skill D0-B 更新」"
            "内容：role-AI工程师 下次激活时自动读到这条原则"
            "↓ [通路A] 下次任务"
            "【第六层，绿色浅色】：「更好的AI工程执行」"
            "内容：「确认是否已设计约定重注入机制」→ Prompt设计更完整"
            ""
            "图右侧有一个大循环箭头从第六层回到第一层，标注：「越用越聪明的飞轮」"
        ),
    },
    {
        "name": "skill-self-loop",
        "prompt": (
            STYLE +
            "【图名：Skill体系自循环进化图】"
            "画一张展示 Skill 体系如何自我进化的循环图。"
            "整体是一个大圆形循环，包含以下节点，按顺时针排列："
            ""
            "①「实际任务执行」（蓝色，12点位置）"
            "→ 顺时针 →"
            "②「D5信号感知\nA/B/D/E/G 五类」（橙色，2点位置）"
            "→ 顺时针 →"
            "③「信号路由处理\n踩坑/洞见/缺口/根因」（黄色，4点位置）"
            "→ 顺时针 →"
            "④「Skill/Rule 更新\nskill-updater 三问协议」（绿色，6点位置）"
            "→ 顺时针 →"
            "⑤「体系健检\nskill-system-health-check」（蓝绿色，8点位置）"
            "→ 顺时针 →"
            "⑥「更好的下次执行\n读到更新后的Skill」（蓝色，10点位置）"
            "→ 顺时针回到① →"
            ""
            "圆圈外部有三个分支触发路径（用虚线箭头指向外部）："
            "从②分出：「D信号 → L2碎片 → L1整合（通路B）」"
            "从④分出：「project-retrospective 批量沉淀」"
            "从③分出：「G信号 → 人工决策」（红色虚线）"
            ""
            "圆圈中心标注：「飞轮效应\n用得越多\n体系越强」"
        ),
    },
]


def generate_image(name: str, prompt: str) -> str:
    """生成单张图片，返回保存路径"""
    out_path = os.path.join(OUT_DIR, f"{name}.png")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "model": "qwen-image-2.0-pro",
        "input": {
            "messages": [{"role": "user", "content": [{"text": prompt}]}]
        },
        "parameters": {
            "n": 1,
            "watermark": False,
            "prompt_extend": True,
            "size": "1024*1024",
        },
    }

    print(f"\n[生成] {name} ...")
    for attempt in range(3):
        try:
            resp = requests.post(ENDPOINT, headers=headers, json=payload, timeout=120)
            data = resp.json()
            
            if resp.status_code == 429:
                print(f"  限速，等待30秒后重试 (attempt {attempt+1})")
                time.sleep(30)
                continue
            
            if resp.status_code != 200:
                print(f"  错误 {resp.status_code}: {data}")
                return None
            
            img_url = data["output"]["choices"][0]["message"]["content"][0]["image"]
            
            # 下载图片
            ir = requests.get(img_url, timeout=60)
            with open(out_path, "wb") as f:
                f.write(ir.content)
            
            print(f"  ✓ 已保存: {out_path}")
            return out_path
            
        except Exception as e:
            print(f"  异常 (attempt {attempt+1}): {e}")
            if attempt < 2:
                time.sleep(10)
    
    return None


def main():
    print(f"开始生成 {len(IMAGES)} 张架构图...")
    results = {}
    
    for img in IMAGES:
        path = generate_image(img["name"], img["prompt"])
        results[img["name"]] = path
        # 每张图之间等待3秒避免限速
        time.sleep(3)
    
    print("\n===== 生成结果 =====")
    for name, path in results.items():
        status = "✓" if path else "✗"
        print(f"  {status} {name}: {path or '失败'}")
    
    success = sum(1 for p in results.values() if p)
    print(f"\n完成: {success}/{len(IMAGES)} 张成功")


if __name__ == "__main__":
    main()
