# Codex Skills 仓库说明

这个仓库用于集中存放与维护 Codex Skills。每个 skill 都是一个可复用的“任务能力包”，包含触发条件、工作流程、参考资料和可执行脚本。

当前仓库包含 **41** 个 skills（包含 `.system` 系统技能 2 个）。

## 1. 仓库目标

- 统一管理技能定义，避免每个项目重复搭建流程。
- 通过标准化 `SKILL.md` 约束触发条件、执行步骤和质量门槛。
- 支持“按任务场景”快速选择技能，提升交付一致性。
- 让技能具备可迁移性：不同仓库、不同 agent 都能复用。

## 2. 目录结构

```text
skills/
  .system/                # 系统级技能（创建/安装 skill）
  <skill-name>/
    SKILL.md              # 技能说明（必须）
    agents/openai.yaml    # UI/元信息（常见）
    scripts/              # 可执行脚本（可选）
    references/           # 参考文档（可选）
    assets/               # 素材文件（可选）
```

## 3. 如何使用本仓库

### 3.1 选择 skill 的原则

1. 优先选择“最小可覆盖需求”的技能集合。
2. 当多个 skill 同时适配时，按顺序执行：
   - 先“信息获取/研究”
   - 再“设计/实现”
   - 最后“验证/发布”
3. 避免同类 skill 重复叠加（例如多个研究 skill 同时深挖同一问题）。

### 3.2 触发方式

- 用户显式提到 skill 名（例如 `$openai-docs`）。
- 用户需求与 skill 描述高度匹配（隐式触发）。

### 3.3 建议的工作流模板

1. 明确任务目标与交付物。
2. 选定 1-3 个最相关 skill。
3. 先读 `SKILL.md` 再执行。
4. 仅按需加载 `references/`，避免上下文膨胀。
5. 若 skill 包含 `scripts/`，优先复用脚本而非临时手写。

## 4. 场景化选型速查

### 4.1 软件工程与质量

- 架构/API：`backend-patterns`、`api-design`
- 代码规范：`coding-standards`
- 测试与验证：`tdd-workflow`、`e2e-testing`、`verification-loop`、`eval-harness`
- 安全：`security-review`

### 4.2 前端与设计实现

- 设计到代码：`figma`、`figma-implement-design`
- 前端实现优化：`frontend-patterns`
- 浏览器自动化：`playwright`
- Web 游戏迭代：`develop-web-game`
- 幻灯片：`frontend-slides`

### 4.3 研究与文档

- 通用深度研究：`deep-research`、`market-research`
- 论文拆解：`paper-deep-review`
- 长文写作：`article-writing`
- OpenAI 官方文档查询：`openai-docs`

### 4.4 协作、流程与发布

- PR 评论处理：`gh-address-comments`
- CI 故障处理：`gh-fix-ci`
- 一键提交推 PR：`yeet`
- 任务管理：`linear`
- 长周期自主开发：`codex-longrun-dev`
- 多 agent 并行：`dmux-workflows`
- 上下文启动与滚动管理：`repo-codex-bootstrap`、`strategic-compact`

### 4.5 内容、媒体与增长

- 内容系统：`content-engine`
- 多平台分发：`crosspost`
- 视频编辑：`video-editing`
- AI 多媒体生成：`fal-ai-media`
- X/Twitter API：`x-api`

### 4.6 文档格式处理

- DOCX：`doc`
- PDF：`pdf`
- 屏幕截图：`screenshot`

### 4.7 系统技能

- 创建/更新 skill：`skill-creator`
- 安装 skill：`skill-installer`

## 5. 全量 Skill 详细说明（41 个）

> 说明格式：
> - **用途**：这个 skill 解决什么问题。
> - **使用时机**：什么输入/任务最适合触发。
> - **建议**：实战中推荐的用法、组合和注意点。

### 5.1 系统技能（.system）

#### `skill-creator`
- 用途：创建新 skill 或更新现有 skill，规范化技能结构与说明。
- 使用时机：你要沉淀一类可复用流程，或重构一个过于松散的技能。
- 建议：先用真实任务样例反推能力边界，再最小化 `SKILL.md`，复杂细节放 `references/`。

#### `skill-installer`
- 用途：从 curated 列表或 GitHub 仓库安装 skills 到 `$CODEX_HOME/skills`。
- 使用时机：需要快速拉取新技能、同步团队技能库、跨机器恢复技能环境。
- 建议：安装后立刻检查目录结构与依赖脚本可执行性，并做一次最小烟雾测试。

### 5.2 工程架构与编码规范

#### `api-design`
- 用途：设计生产级 REST API（资源命名、状态码、分页、过滤、错误模型、版本化、限流）。
- 使用时机：新建 API、重构旧接口、准备对外开放接口时。
- 建议：先定资源模型和错误语义，再补分页/过滤；避免先写路由再补语义导致返工。

#### `backend-patterns`
- 用途：Node.js/Express/Next.js API 后端架构、性能与数据库优化实践。
- 使用时机：后端新模块落地、接口吞吐瓶颈、服务拆分或重构。
- 建议：与 `security-review` 联合使用，先做边界与数据流设计，再做性能调优。

#### `frontend-patterns`
- 用途：React/Next.js 前端架构、状态管理、性能优化、UI 实践。
- 使用时机：页面结构变复杂、状态混乱、交互性能下降时。
- 建议：先做状态分层与渲染边界设计，再上性能优化，避免“盲目 memo 化”。

#### `coding-standards`
- 用途：TypeScript/JavaScript/React/Node.js 通用编码规范与最佳实践。
- 使用时机：团队代码风格不统一、重构质量下滑、评审成本过高时。
- 建议：和 lint/format/test 门禁绑定，规范才能真正稳定执行。

#### `security-review`
- 用途：认证、输入处理、密钥、支付与敏感接口的安全检查清单。
- 使用时机：涉及用户数据、鉴权、支付、外部输入落库等高风险改动。
- 建议：在方案设计阶段就触发，不要等到“开发完成后再补安全”。

### 5.3 测试、验证与评估

#### `tdd-workflow`
- 用途：基于测试驱动开发推进新功能、修 bug、重构，强调覆盖率与回归保护。
- 使用时机：需求变更频繁、回归风险高、历史缺陷密集模块。
- 建议：先写失败测试再编码；把关键边界条件放进测试，而不是注释里。

#### `e2e-testing`
- 用途：Playwright E2E 体系化实践（POM、配置、CI 集成、抗脆弱策略）。
- 使用时机：核心用户路径需要端到端保障，或回归主要发生在页面交互层。
- 建议：优先覆盖“高业务价值路径”，不要先追求大量低价值 UI 用例。

#### `verification-loop`
- 用途：会话级综合验证流程，确保改动可运行、可解释、可复现。
- 使用时机：任务跨多个模块，且需要在交付前形成可审计验证链路。
- 建议：把验证拆成“静态检查 + 单测 + 集成验证 + 关键手测”四段。

#### `eval-harness`
- 用途：采用 EDD（eval-driven development）理念做正式评估框架。
- 使用时机：需要量化模型/Agent 任务表现、对比策略优劣时。
- 建议：先定义稳定的评估指标与数据集，再比较实现方案，避免“指标漂移”。

### 5.4 研究、分析与知识整理

#### `deep-research`
- 用途：多源检索与综合（firecrawl + exa），产出带引用的研究报告。
- 使用时机：需要证据链、交叉验证、可追溯来源的深入调研。
- 建议：先收敛研究问题，再扩展来源；避免主题过宽导致报告失焦。

#### `market-research`
- 用途：市场调研、竞品分析、投资尽调、行业扫描。
- 使用时机：要做市场进入判断、竞品定位、融资材料支撑时。
- 建议：结论必须绑定决策场景（Go/No-go、定价、优先级），避免纯信息堆砌。

#### `paper-deep-review`
- 用途：深度拆解论文方法、实验、对比基线、优缺点与创新性。
- 使用时机：需要快速且严谨地理解论文并转化为工程行动项。
- 建议：先抽取问题定义与贡献，再拆实验设置；重点看可复现与外推边界。

#### `openai-docs`
- 用途：针对 OpenAI 产品/API 的官方文档查询与引用（强调最新与官方）。
- 使用时机：涉及 OpenAI 接口能力、限制、SDK 用法、版本变动时。
- 建议：优先官方文档与官方域名；记录查询日期，避免引用过期结论。

#### `exa-search`
- 用途：通过 Exa MCP 做网络、代码、公司、人物等神经搜索。
- 使用时机：需要快速定位高相关外部资料、样例代码或背景信息时。
- 建议：与 `deep-research` 搭配，把 Exa 结果作为候选来源再做二次验证。

### 5.5 文档与写作产出

#### `article-writing`
- 用途：输出高质量长文（文章、教程、Newsletter、指南）并保持稳定文风。
- 使用时机：用户需要超过一段的系统性内容，且强调风格一致与可信度。
- 建议：先给样例语料做“风格拟合”，再写正文；每段先给证据后给观点。

#### `doc`
- 用途：读取、创建、编辑 `.docx`，并关注版式和渲染一致性。
- 使用时机：需要交付 Word 文档，尤其在模板、排版、导出质量重要时。
- 建议：优先 `python-docx` 结构化生成，最终用渲染脚本做视觉复核。

#### `pdf`
- 用途：PDF 读取/生成/审阅，强调渲染和布局正确性。
- 使用时机：处理报告、票据、合同、论文 PDF 的抽取或生成。
- 建议：文本抽取和版面检查要分开做，生成后始终进行页面级截图校验。

### 5.6 前端、设计与交互实现

#### `figma`
- 用途：通过 Figma MCP 拉取设计上下文、变量、截图与资产，辅助设计到代码。
- 使用时机：用户给出 Figma 链接/节点，或需要排查 Figma MCP 连接问题。
- 建议：先拿到节点上下文和设计 token，再编码，避免“凭视觉猜测”。

#### `figma-implement-design`
- 用途：将 Figma 节点高保真（1:1）转为生产代码。
- 使用时机：明确要求“与 Figma 一致”的组件/页面实现。
- 建议：先确认项目现有设计系统约束，再映射 Figma 变量到工程 token。

#### `frontend-slides`
- 用途：构建高视觉质量 HTML 演示稿或将 PPT/PPTX 转 Web。
- 使用时机：演讲、路演、发布会、培训课件的网页化演示需求。
- 建议：先确定叙事节奏和视觉母版，再逐页动画；避免每页风格割裂。

#### `playwright`
- 用途：在终端自动化真实浏览器（导航、表单、截图、抓取、调试 UI 流程）。
- 使用时机：需要复现前端问题、采集页面信息、走完整交互路径。
- 建议：优先可重放脚本；将关键步骤显式等待，降低偶发失败率。

#### `develop-web-game`
- 用途：Web 游戏小步迭代 + Playwright 验证闭环。
- 使用时机：HTML/JS 游戏开发中，需要“改一点、测一点、看截图/日志”。
- 建议：每次只改一个机制并立即回归，避免多变量同时变化难以定位问题。

#### `screenshot`
- 用途：系统级截图（全屏、窗口、区域）。
- 使用时机：工具链截图能力不足，或用户明确要求 OS 级截图时。
- 建议：先确认目标显示器/窗口，再截图；必要时附带分辨率与时间戳。

### 5.7 协作流程、GitHub 与项目运营

#### `gh-address-comments`
- 用途：用 `gh` 处理当前分支 PR 的 review/issue 评论。
- 使用时机：PR 收到批注，需要按评论逐条修复并回传状态。
- 建议：先分组“必须修复/可讨论/已解决”，再按优先级提交。

#### `gh-fix-ci`
- 用途：定位并修复 GitHub Actions 失败检查。
- 使用时机：PR checks 红灯，需要查看日志、归因、提出修复方案。
- 建议：先拿最小复现，再修；遵守“先确认后实施”的流程控制变更风险。

#### `yeet`
- 用途：在用户明确要求时执行“stage + commit + push + 开 PR”一条龙。
- 使用时机：用户明确说要一次性完成发布链路。
- 建议：只在显式授权时使用；提交前确认 diff 干净且 commit 信息可审计。

#### `linear`
- 用途：管理 Linear 中的 issue、项目和团队流程。
- 使用时机：任务拆解、状态同步、跨人协作追踪。
- 建议：issue 描述要包含验收标准，避免只有标题没有可执行定义。

#### `dmux-workflows`
- 用途：通过 dmux/tmux 编排多 agent 并行工作。
- 使用时机：任务可拆并行、需要跨工具协作（Codex/Claude/OpenCode）时。
- 建议：先划分不重叠责任边界，再并发；定时做结果汇总与冲突消解。

#### `codex-longrun-dev`
- 用途：支持长周期自主开发（跨上下文窗口、低人工确认、阶段性稳定交付）。
- 使用时机：持续数小时/数天的大型迭代任务。
- 建议：坚持“一次一个 feature + 每会话可验证 + 干净提交”的节奏。

#### `repo-codex-bootstrap`
- 用途：初始化并维护仓库级 `codex/` 记忆与计划文档。
- 使用时机：新仓库启动、上下文容易丢失、需要跨会话持续追踪时。
- 建议：每次会话先读 `memory.md` 和 `prompt.md`，每轮交互滚动更新两者。

#### `strategic-compact`
- 用途：在关键阶段做手动上下文压缩，保持长期任务上下文稳定。
- 使用时机：任务跨度大、会话切换频繁、上下文接近容量上限时。
- 建议：按“里程碑”压缩，而非按固定字数/固定轮次机械压缩。

### 5.8 内容增长、媒体与渠道分发

#### `content-engine`
- 用途：构建多平台原生内容系统（X/LinkedIn/TikTok/YouTube/Newsletter）。
- 使用时机：需要从单一素材扩展到多渠道内容矩阵。
- 建议：先定义内容支柱与受众，再做平台改写，避免“同文硬发”。

#### `crosspost`
- 用途：跨平台分发改写（X/LinkedIn/Threads/Bluesky），强调差异化表达。
- 使用时机：同一主题要多平台发布，但不能原文复制。
- 建议：保留核心观点一致，语气/长度/结构按平台重写。

#### `video-editing`
- 用途：AI 辅助视频编辑全流程（剪辑、结构、配音、增强、发布前打磨）。
- 使用时机：vlog、产品视频、短内容批量生产。
- 建议：先锁定叙事主线再做特效；优先节奏与可看性而非特效堆叠。

#### `fal-ai-media`
- 用途：通过 fal.ai MCP 统一生成图像、视频、音频。
- 使用时机：需要快速产出 AI 媒体资产并在工作流中复用。
- 建议：先小样本探索提示词，再批量生成；记录模型参数确保可复现。

#### `x-api`
- 用途：X/Twitter API 集成（发帖、线程、检索、分析）。
- 使用时机：需要程序化运营 X 渠道或自动化数据采集。
- 建议：严格处理 OAuth 与限流；运营类自动化要设置人工复核点。

### 5.9 商业、融资与投资沟通

#### `investor-materials`
- 用途：生成和维护融资材料（BP、one-pager、memo、模型、里程碑计划）。
- 使用时机：准备融资、更新投资人材料、统一口径时。
- 建议：所有数字在不同材料中保持一致，先统一“单一事实来源”。

#### `investor-outreach`
- 用途：撰写投资人触达文案（冷启动邮件、引荐文案、跟进、更新）。
- 使用时机：需要高密度外联且保证个性化与专业度。
- 建议：先细分投资人画像，再个性化首段；控制邮件长度和单次 CTA 数量。

### 5.10 平台与模型集成

#### `claude-api`
- 用途：Anthropic Claude API 的 Python/TypeScript 集成实践（消息、流式、工具调用等）。
- 使用时机：搭建或优化 Claude 驱动应用。
- 建议：先明确模型调用模式（同步/流式/批处理），再做工具链封装。

## 6. 推荐组合（高频）

1. **新功能研发闭环**
   - `repo-codex-bootstrap` + `backend-patterns`/`frontend-patterns` + `tdd-workflow` + `verification-loop`
2. **PR 交付闭环**
   - `gh-address-comments` + `gh-fix-ci` + `yeet`
3. **设计到前端实现**
   - `figma` + `figma-implement-design` + `playwright`
4. **深度研究到内容发布**
   - `deep-research` + `article-writing` + `content-engine` + `crosspost`
5. **融资资料与外联**
   - `market-research` + `investor-materials` + `investor-outreach`

## 7. 使用建议（仓库级）

- 每次新增/修改 skill，优先更新 `SKILL.md` 的触发条件与边界，而不是只改脚本。
- 对“高风险动作”技能（如 `yeet`、`gh-fix-ci`）建议在说明里保留显式确认门槛。
- 优先把可重复步骤脚本化，减少上下文 token 消耗。
- `references/` 只放“按需加载”资料，避免把大量细节塞进 `SKILL.md`。
- 对依赖外部环境的技能（如 `gh-*`、`figma`、`openai-docs`）建议在 skill 内写清前置条件检查。

## 8. 维护清单

- 每个 skill 目录必须至少有 `SKILL.md`。
- `name` 与目录名保持一致，`description` 明确触发时机。
- 脚本可执行权限正确（如需要）。
- 重大改动后补一条变更记录（建议在提交信息或 PR 描述里体现）。
- 定期复核技能是否过时（API 版本、平台策略、工具可用性）。

## 9. 当前技能总览（按字母序）

`api-design`, `article-writing`, `backend-patterns`, `claude-api`, `codex-longrun-dev`, `coding-standards`, `content-engine`, `crosspost`, `deep-research`, `develop-web-game`, `dmux-workflows`, `doc`, `e2e-testing`, `eval-harness`, `exa-search`, `fal-ai-media`, `figma`, `figma-implement-design`, `frontend-patterns`, `frontend-slides`, `gh-address-comments`, `gh-fix-ci`, `investor-materials`, `investor-outreach`, `linear`, `market-research`, `openai-docs`, `paper-deep-review`, `pdf`, `playwright`, `repo-codex-bootstrap`, `screenshot`, `security-review`, `strategic-compact`, `tdd-workflow`, `verification-loop`, `video-editing`, `x-api`, `yeet`, `skill-creator`, `skill-installer`.

---

如果你希望，我可以继续补一个 `README_EN.md`（英文版）以及一个“按角色（工程师/研究员/增长/融资）”的快速入口索引。
