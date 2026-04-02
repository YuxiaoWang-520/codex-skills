<div align="right">

[![Language: English](https://img.shields.io/badge/Language-English-0A66C2)](./README_EN.md)
[![语言: 简体中文](https://img.shields.io/badge/语言-简体中文-2EA44F)](./README.md)

</div>

# Harness Craft

驾驭 AI 编码 Agent 的工艺库。Skills（按需调用的操作手册）+ Rules（始终生效的行为准则）= 更强、更可控的 AI 工程伙伴。

## Overview

- 仓库目标：沉淀高复用的 skills 与 rules，降低重复上下文沟通成本，让 AI agent 开箱即用地遵循工程最佳实践。
- 当前规模：**41** 个 skills + **15** 条 rules（通用 10 条 + Python 5 条）。
- 适用对象：AI 应用开发者、自动化工程师、研究/内容团队、开源维护者。

## Skills vs Rules

| | Skills | Rules |
|--|--------|-------|
| **类比** | 操作手册 | 宪法 |
| **加载方式** | 按需显式调用（`/skill-name`） | 每次会话自动注入 |
| **占用 context** | 调用时才加载全文 | 始终占用（但每条很短） |
| **适合放什么** | 长篇工作流程（TDD、E2E、深度研究…） | 短小的全局约束（编码风格、安全检查、Git 规范…） |
| **生效方式** | 用户触发后执行 | 每轮交互自动遵守 |

**一句话**：Rules 是 agent 的本能反射，Skills 是 agent 的后天技能。

## Repository Structure

```text
skills/
  .system/
    skill-creator/
    skill-installer/
  <skill-name>/
    SKILL.md              # 必需：触发条件与执行流程
    agents/openai.yaml    # 可选：界面与元信息
    scripts/              # 可选：可执行脚本
    references/           # 可选：按需加载资料
    assets/               # 可选：模板/素材

rules/
  common/                 # 语言无关的通用规则（始终生效）
    coding-style.md         # 不可变数据、文件组织、函数 <50 行
    security.md             # commit 前安全检查清单
    testing.md              # TDD 流程、覆盖率 ≥80%
    git-workflow.md         # commit 格式、PR 规范
    code-review.md          # 审查标准、严重级别、阻止合并条件
    development-workflow.md # 完整开发流程：搜索→规划→TDD→审查→提交
    patterns.md             # 设计模式、骨架项目复用
    performance.md          # 模型选择、context 管理、扩展思考
    agents.md               # 子 agent 自动调度策略
    hooks.md                # Hook 系统与 TodoWrite 实践
  python/                 # Python 专用规则（仅 .py/.pyi 文件生效）
    coding-style.md         # PEP 8、type annotations、frozen dataclass
    patterns.md             # Protocol、dataclass DTO、context manager
    security.md             # 环境变量管理、bandit 扫描
    testing.md              # pytest、coverage、mark 分类
    hooks.md                # Python 项目 hook 集成
```

## How To Use

### Skills

1. 明确任务目标与交付物（代码、文档、报告、PR、发布等）。
2. 选择最小可覆盖的 1-3 个 skills，避免同类技能重复叠加。
3. 先读 `SKILL.md` 再执行；仅按需读取 `references/`。
4. 有 `scripts/` 时优先复用脚本，减少一次性手写逻辑。
5. 完成后做验证与回顾：输出、日志、测试、风险点、下一步。

### Rules

Rules 安装后**无需任何操作**，每次会话自动生效：

```bash
# 安装到用户级（所有项目生效）
mkdir -p ~/.claude/rules
cp -r rules/common ~/.claude/rules/
cp -r rules/python ~/.claude/rules/   # 按需选择语言

# 或安装到项目级（仅当前项目生效）
mkdir -p .claude/rules
cp -r rules/common .claude/rules/
```

安装后 AI agent 会自动：
- 用 `feat:/fix:/refactor:` 格式写 commit message
- 提交前检查硬编码密钥、SQL 注入、XSS 等安全问题
- 遵循不可变数据模式、函数 <50 行等编码规范
- Python 文件自动加 type annotations、用 frozen dataclass
- 写完代码后主动触发 code review

## Skill Trigger Rules

- 显式触发：用户在需求中直接提到 skill 名称（例如 `$openai-docs`）。
- 语义触发：用户需求与 skill `description` 高度匹配。
- 多 skill 组合：优先「研究/输入」→「实现/产出」→「验证/交付」。

## Recommended Workflow

1. 上下文准备：`repo-codex-bootstrap` + `strategic-compact`
2. 架构与实现：`api-design` / `backend-patterns` / `frontend-patterns`
3. 质量保障：`tdd-workflow` + `e2e-testing` + `verification-loop`
4. 发布协作：`gh-address-comments` / `gh-fix-ci` / `yeet`

## Star Rating（技能优先级）

- `⭐⭐ Core`：跨项目高复用、建议优先掌握（默认工作流核心）。
- `⭐ Common`：高频实战技能，覆盖大部分工程与协作场景。
- 无星标：按特定任务场景使用的专业技能。

### Starred Skills Quick Picks

- `⭐⭐ repo-codex-bootstrap`：会话记忆与仓库上下文管理基座。
- `⭐⭐ codex-longrun-dev`：长周期、多阶段任务的稳定推进框架。
- `⭐ backend-patterns`, `⭐ frontend-patterns`, `⭐ coding-standards`, `⭐ security-review`
- `⭐ api-design`, `⭐ tdd-workflow`, `⭐ verification-loop`, `⭐ playwright`
- `⭐ deep-research`, `⭐ openai-docs`, `⭐ article-writing`
- `⭐ gh-address-comments`, `⭐ gh-fix-ci`

## Rules Reference

> Rules 安装后自动生效，无需手动调用。以下是每条 rule 的作用。

### Common Rules（通用，所有语言生效）

| Rule | 自动做什么 |
|------|-----------|
| `coding-style` | 强制不可变数据模式；函数 <50 行、文件 <800 行、嵌套 <4 层 |
| `security` | 每次 commit 前检查：无硬编码密钥、SQL 参数化、XSS/CSRF 防护 |
| `testing` | 强制 TDD（先写测试再写代码）；覆盖率 ≥80% |
| `git-workflow` | commit 格式 `<type>: <description>`；PR 分析完整 commit 历史 |
| `code-review` | 写完代码自动审查；CRITICAL 问题阻止合并；安全敏感代码强制安全审查 |
| `development-workflow` | 开发流程：先搜索现有方案→规划→TDD→Review→Commit |
| `patterns` | 新功能先搜索成熟骨架项目；推荐 Repository Pattern |
| `performance` | 模型选择建议（Haiku 省钱/Sonnet 日常/Opus 架构）；context 管理策略 |
| `agents` | 自动调度子 agent：复杂功能→planner，写完代码→code-reviewer |
| `hooks` | TodoWrite 最佳实践、权限控制指南 |

### Python Rules（仅 `.py`/`.pyi` 文件生效）

| Rule | 自动做什么 |
|------|-----------|
| `coding-style` | PEP 8；所有函数必须写 type annotations；用 `frozen=True` dataclass |
| `patterns` | Protocol 鸭子类型、dataclass DTO、context manager、generator |
| `security` | `os.environ["KEY"]` 严格取值；bandit 静态扫描 |
| `testing` | pytest + `--cov`；`pytest.mark.unit/integration` 分类 |
| `hooks` | Python 项目 hook 集成指南 |

## Full Skill Reference

> 字段说明：
> - 用途：解决什么问题
> - 使用时机：何时触发最有效
> - 使用建议：落地时的实践建议

### 1) System Skills

| Skill | 用途 | 使用时机 | 使用建议 |
|---|---|---|---|
| `skill-creator` | 创建/更新 skill，规范化技能结构 | 要沉淀新能力或重构旧技能时 | 用真实样例反推边界，保持 `SKILL.md` 精简 |
| `skill-installer` | 安装 curated/GitHub skills 到 `$CODEX_HOME/skills` | 新环境搭建、团队同步、迁移恢复 | 安装后立即做最小烟雾测试 |

### 2) Engineering & Quality

| Skill | 用途 | 使用时机 | 使用建议 |
|---|---|---|---|
| `⭐ api-design` | 生产级 REST API 设计 | 新建/重构接口，对外开放 API | 先定资源与错误模型，再做分页过滤 |
| `⭐ backend-patterns` | Node/Express/Next.js 后端架构与优化 | 后端模块重构、性能瓶颈治理 | 与 `security-review` 联合，在设计阶段介入 |
| `⭐ frontend-patterns` | React/Next.js 架构与性能实践 | 页面复杂度上升、状态管理混乱 | 先做状态分层与渲染边界，再做优化 |
| `⭐ coding-standards` | TS/JS/React/Node 编码规范 | 团队风格不一致、评审成本高 | 绑定 lint/test 门禁，防止"规范落空" |
| `⭐ security-review` | 安全审查清单（鉴权/输入/密钥/支付） | 涉及敏感数据或高风险接口时 | 先做威胁建模，再做实现与验证 |
| `⭐ tdd-workflow` | 测试驱动开发流程 | 新功能、修复缺陷、重构高风险模块 | 先写失败测试，再写实现 |
| `e2e-testing` | Playwright 端到端测试体系 | 核心用户路径需要回归保障 | 优先覆盖高价值路径，减少脆弱断言 |
| `⭐ verification-loop` | 会话级综合验证机制 | 多模块改动、需要可审计交付 | 形成"静态检查→测试→手测"闭环 |
| `eval-harness` | EDD 评估框架 | 需要量化 agent/model 效果 | 先固化指标和样本，再做策略对比 |
| `⭐⭐ codex-longrun-dev` | 长周期自主开发协作框架 | 任务跨度数小时/数天 | 一次一个 feature，确保每轮可验证 |
| `dmux-workflows` | dmux/tmux 多 agent 编排 | 可并行拆解的复杂任务 | 预先划分无重叠职责边界 |
| `⭐⭐ repo-codex-bootstrap` | 仓库级 `codex/` 文档初始化与维护 | 新仓库或跨会话上下文易丢失 | 每会话先读 `memory.md`/`prompt.md`，每轮滚动更新 |
| `strategic-compact` | 关键阶段手动上下文压缩 | 长任务上下文接近上限时 | 按里程碑压缩，不按固定轮次机械压缩 |

### 3) Frontend, Design & Automation

| Skill | 用途 | 使用时机 | 使用建议 |
|---|---|---|---|
| `figma` | 通过 Figma MCP 拉取设计上下文与资产 | 有 Figma URL/节点或 MCP 连接问题 | 先拉 token/变量再编码，避免视觉猜测 |
| `figma-implement-design` | Figma 1:1 高保真实现 | 明确要求"与设计稿一致" | 先对齐项目设计系统与 token 映射 |
| `⭐ playwright` | 终端自动化真实浏览器 | UI 流程复现、抓取、截图、调试 | 脚本化关键路径并显式等待 |
| `develop-web-game` | Web 游戏迭代与验证闭环 | HTML/JS 游戏小步快跑开发 | 每次只改一个机制并即时回归 |
| `frontend-slides` | HTML 幻灯片制作或 PPT 转 Web | 路演、演讲、培训课件 | 先定叙事节奏和视觉母版 |
| `screenshot` | 系统级截图能力 | 需要窗口/区域/全屏截图 | 先确认目标窗口与分辨率 |

### 4) Research, Docs & Knowledge

| Skill | 用途 | 使用时机 | 使用建议 |
|---|---|---|---|
| `⭐ deep-research` | 多源深度研究并提供引用 | 需要证据链与可追溯结论 | 先收敛问题，再扩展来源 |
| `market-research` | 市场/竞品/尽调研究 | 商业决策、市场进入、融资准备 | 结论绑定决策动作，避免信息堆砌 |
| `paper-deep-review` | 论文深读与结构化拆解 | 需要快速理解方法与实验 | 先看问题定义与贡献，再看实验边界 |
| `⭐ openai-docs` | OpenAI 官方文档检索与引用 | 涉及 OpenAI API 能力或限制 | 优先官方来源，标注查询日期 |
| `exa-search` | Exa 神经搜索（网页/代码/公司） | 需要快速定位高相关资料 | 把检索结果做二次验证再下结论 |
| `⭐ article-writing` | 高质量长文写作与风格对齐 | 文章、教程、Newsletter、指南 | 先确定受众与样例文风再写作 |
| `doc` | `.docx` 创建/编辑与排版校验 | Word 文档交付且版式重要 | 结构化生成后做渲染复核 |
| `pdf` | PDF 解析、生成与审阅 | 报告/论文/票据类 PDF 工作流 | 文本抽取与版式校验分开处理 |

### 5) GitHub, Project Ops & Delivery

| Skill | 用途 | 使用时机 | 使用建议 |
|---|---|---|---|
| `⭐ gh-address-comments` | 处理 PR review/issue 评论 | PR 收到反馈需要逐条闭环 | 先分级评论，再按优先级处理 |
| `⭐ gh-fix-ci` | 排查并修复 GitHub Actions 失败 | PR checks 失败或不稳定 | 先最小复现，再实施修复 |
| `yeet` | 一键 stage/commit/push/开 PR | 用户明确要求一条龙发布 | 仅在显式授权下使用 |
| `linear` | Linear 任务与项目流管理 | 需要跟踪任务状态和协作 | issue 必须写清验收标准 |

### 6) Content, Media & Growth

| Skill | 用途 | 使用时机 | 使用建议 |
|---|---|---|---|
| `content-engine` | 多平台原生内容系统建设 | 从单一素材扩展内容矩阵 | 先定义内容支柱再多平台改写 |
| `crosspost` | 跨平台差异化分发 | 同主题需发 X/LinkedIn/Threads 等 | 保持核心观点一致，平台表达重写 |
| `video-editing` | AI 辅助视频编辑全流程 | vlog、产品短视频、批量剪辑 | 先锁主线叙事，再加特效 |
| `fal-ai-media` | fal.ai 图像/视频/音频生成 | 需要快速生成 AI 媒体资产 | 先小样本试参，再批量生成 |
| `x-api` | X/Twitter API 集成 | 自动发帖、检索、分析 | 严格处理 OAuth 与速率限制 |

### 7) Business & Fundraising

| Skill | 用途 | 使用时机 | 使用建议 |
|---|---|---|---|
| `investor-materials` | 融资材料创建与维护 | BP/one-pager/memo/财务模型准备 | 所有材料共用同一数据口径 |
| `investor-outreach` | 投资人外联文案 | 冷启动、引荐、跟进、进展更新 | 按投资人画像做个性化首段 |

### 8) Platform Integrations

| Skill | 用途 | 使用时机 | 使用建议 |
|---|---|---|---|
| `claude-api` | Anthropic Claude API 工程化集成 | 构建 Claude 驱动应用 | 先定义调用模式，再封装工具链 |

## Inventory

**Skills (A-Z):** `api-design`, `article-writing`, `backend-patterns`, `claude-api`, `codex-longrun-dev`, `coding-standards`, `content-engine`, `crosspost`, `deep-research`, `develop-web-game`, `dmux-workflows`, `doc`, `e2e-testing`, `eval-harness`, `exa-search`, `fal-ai-media`, `figma`, `figma-implement-design`, `frontend-patterns`, `frontend-slides`, `gh-address-comments`, `gh-fix-ci`, `investor-materials`, `investor-outreach`, `linear`, `market-research`, `openai-docs`, `paper-deep-review`, `pdf`, `playwright`, `repo-codex-bootstrap`, `screenshot`, `security-review`, `skill-creator`, `skill-installer`, `strategic-compact`, `tdd-workflow`, `verification-loop`, `video-editing`, `x-api`, `yeet`.

**Rules:** `common/coding-style`, `common/security`, `common/testing`, `common/git-workflow`, `common/code-review`, `common/development-workflow`, `common/patterns`, `common/performance`, `common/agents`, `common/hooks`, `python/coding-style`, `python/patterns`, `python/security`, `python/testing`, `python/hooks`.

## Maintenance Guidelines

- 每个 skill 目录必须包含 `SKILL.md`。
- `name` 与目录名保持一致，`description` 写清触发条件。
- Rules 保持短小（每条 10-50 行），长流程请放到 skills 中。
- 脚本涉及执行权限时，保持可执行位正确。
- 外部依赖变更（API、平台策略、CLI 行为）后及时更新 skill/rule。
- 重要改动应通过 PR 描述记录变更原因与影响范围。

## Contributing

欢迎提交 Issue 和 PR 来补充新技能/规则、修正流程或改进文档。建议在提交前确保：

1. 技能触发条件清晰且可复用。
2. `SKILL.md` 与脚本/参考资料一致。
3. Rules 遵循"短小 + 全局约束"原则，不放具体工作流。
4. 说明中包含边界条件与失败回退策略。
