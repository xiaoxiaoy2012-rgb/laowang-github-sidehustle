# 老王 GitHub 副业雷达

**从开源项目里找副业方向，再把方向拆成“卖给谁、改什么、怎么收钱、先验证什么”。**

适合想用 AI Coding 做小产品、模板或标准化服务的个人开发者。你不必先读懂几十个英文仓库，也不用把“很多人点星”当成“很多人愿意付钱”。

更多实测、使用技巧与后续案例，微信搜索公众号 **「中年老王学 ai」**。技能免费使用，不需要关注解锁。

## 它给你什么

- 限定范围收集 GitHub 候选，保留查询条件、时间和 README 来源。
- 中文解释项目用途，找具体买家与可改造之处。
- 区分接单收入、可重复销售产品和订阅服务，列出维护成本。
- 给一个小投入的验证动作，说明什么情况下继续、什么情况下停止。
- 保留排除和暂缓理由，没找到合适项目就明确说没有。

它不会承诺收益。**“睡后收入”需要可重复交付的产品、获客和维护**，不能只靠收藏开源项目。

## 安装与使用

源码仓库：[xiaoxiaoy2012-rgb/laowang-github-sidehustle](https://github.com/xiaoxiaoy2012-rgb/laowang-github-sidehustle)。安装包见仓库的 [Releases](https://github.com/xiaoxiaoy2012-rgb/laowang-github-sidehustle/releases)。

### WorkBuddy

使用本项目单独打包的 `laowang-github-sidehustle-workbuddy.zip`。打开「专家·技能·连接器 → 技能 → 添加技能 → 上传技能」导入，再在对话中描述需求。

本地导入与公开市场上架是不同流程。市场发布需通过 WorkBuddy 开放平台，上传、审核状态以后台为准；本仓库不表示已获官方推荐。

### Codex 或其他兼容 SKILL.md 的工具

把 `skills/laowang-github-sidehustle` 文件夹复制到对应工具的技能目录。Codex 常用目录为 `~/.codex/skills/`，然后新建对话调用 `$laowang-github-sidehustle`。其他工具按各自技能安装机制导入；没有逐个客户端实测的兼容性不作保证。

### 第一次这样问

> 用老王 GitHub 副业雷达，帮我找适合个人 AI Coding 的副业项目。我每周能投入 6 小时，先做网页小工具，优先看电商和办公场景。最多给我 3 个，讲清卖给谁、最少改什么、怎么收钱、先怎么验证。没有合适的就直说。

也可以换成：

> 我想做可重复销售的小产品，尽量减少按单定制和售后。帮我看看哪些方向接近这个目标，哪些其实只是换一种方式接外包。

> 只看最近 30 天新建、Python 或 TypeScript 的项目。不要大型推理框架，优先筛有网页演示和清楚运行说明的工具。

> 先收集证据，别出结论。再逐个核对 README、LICENSE、运行条件，最后给我一份中文报告。

## 单独运行数据采集

需要 Python 3.9+ 和能访问 GitHub API 的网络；只用 Python 标准库。

```bash
python3 skills/laowang-github-sidehustle/scripts/scan.py --out ./runs
```

默认从最近 30 天更新的 `saas`、`productivity`、`ecommerce` topic 各取最多 10 个结果，去重后读取 README。自定义查询：

```bash
python3 skills/laowang-github-sidehustle/scripts/scan.py \
  --query 'topic:ecommerce language:TypeScript stars:>=50 archived:false fork:false' \
  --limit 5 --out ./runs
```

脚本只生成 JSON 证据，**需要宿主 AI 继续阅读和判断，才会有副业报告**。它不调用收费模型、不安装候选代码、不自动部署。GitHub 搜索按更新时间排序，不能冒称今日涨星榜或全站扫描。

访问凭证可通过 `GITHUB_TOKEN` 或 `GH_TOKEN` 环境变量提供，不写进命令参数、JSON 或仓库。不要把 Token 发在聊天里。无需为公开仓库采集授予写权限。

返回码 `0` 表示本次采集无错误；`2` 表示采集不完整或没有候选。结果中保留失败项、去重候选数、README 成功数。遇到授权/限流会停止继续请求受影响的阶段。网络失败时检查本机代理与 GitHub 连通性，不要关闭证书验证。

## 更好用的几个技巧

1. **先说你的客源。** “我认识几家电商商家”比“给我找能赚钱的 AI 项目”更有助于筛选。
2. **给投入上限。** 时间、预算、设备会改变推荐；大模型基础设施可能很热门，却不适合业余交付。
3. **先看买家，再看技术。** 把最感兴趣的项目做成输入输出演示，验证需求后再开发完整产品。
4. **要求说出不适合的原因。** 这能帮你少花时间追热点。
5. **追问持续成本。** 每月 API、托管、维护和客服，会影响收入能否沉淀。
6. **先手动跑顺，再定时。** Skill 本身不定时；需要自动日报时，通过使用它的工具设置任务。

## 目录与状态

- `skills/`：通用 Skill 和采集脚本。
- `examples/`：独立实测材料，日期与范围写在报告里。
- `dist/`：本地构建出的通用版、WorkBuddy 版安装包；公开安装包从 Releases 下载。

公众号未定稿文章与原始研究资料只保留在本地，不随公开仓库分发。

当前版本 `0.1.0`。本地检查、API 实测、宿主调用、市场审核分别记录在 [验证状态](STATUS.md)，不混用状态。

## 来源与授权

产品方向参考了用户提供的「夜秣AI搞钱」2026-11-09《用 workbuddy 每天扫描 github 副业项目，总会爆出金色传说！》截图。我们独立编写了本仓库的指令与代码，没有复制原作者的技能源码、素材、截图或实测数据；评分、筛选与报告规则另行设计。参考文章的来源页 URL 尚未取得。

本项目原创代码与文档使用 MIT 许可证。候选项目、依赖、模型、素材仍遵守各自授权。

官方资料：[GitHub 搜索 API](https://docs.github.com/en/rest/search/search)、[WorkBuddy 技能结构](https://open.workbuddy.cn/docs/skill)、[WorkBuddy 技能安装](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)。
