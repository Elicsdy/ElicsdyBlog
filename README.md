# ElicsdyBlog

一个基于 **VuePress 1.x** 的个人博客仓库，内容以中文为主，兼顾手写笔记与自动生成栏目。

目前仓库里既有静态页面内容，也有几条自动化流水线，会定时生成：

- 每日热点新闻
- GitHub 热门项目
- AI / 开发资讯精选
- 每周技术周报

部署目标是 **GitHub Pages**。

## 技术栈

- Node.js + npm
- VuePress 1.x
- Python 3（用于内容生成脚本）
- GitHub Actions（用于定时更新与部署）

## 本地开发

安装依赖：

```bash
npm ci
```

启动本地开发：

```bash
npm run dev
```

构建静态站点：

```bash
npm run build
```

构建产物会输出到：

```text
docs/.vuepress/dist
```

## 目录结构

```text
.
├── docs/                   # 博客正文与页面
│   ├── .vuepress/          # VuePress 配置
│   ├── news/               # 每日热点新闻
│   ├── github-hot/         # GitHub 热门项目
│   ├── ai-digest/          # AI / 开发资讯精选
│   ├── weekly/             # 每周技术周报
│   └── notes/              # 运维/交接/手写笔记
├── scripts/                # 自动生成脚本
└── .github/workflows/      # GitHub Actions 工作流
```

## 自动化说明

当前仓库内主要自动化包括：

- `update-daily-hot-news.yml`
- `update-github-hot.yml`
- `update-ai-dev-digest.yml`
- `update-weekly-tech-digest.yml`
- `deploy-pages.yml`

其中内容更新工作流会提交生成结果到 `main`，随后由 Pages 工作流完成构建与部署。

## 当前维护建议

这个仓库现在是 **能正常构建、能持续生成内容、能部署** 的状态，但要注意两点：

1. **VuePress 1.x / Vue 2 已偏旧**  
   短期继续维护没问题，但中长期建议规划迁移到 VuePress 2 或其他更现代的静态站点方案。

2. **依赖审计里的风险大多来自构建链**  
   站点本身是静态产物，运行面风险不高；不过开发依赖比较老，后续升级时需要整体评估，而不是零碎地逐个 bump。

## 维护原则

- 小步修改，先保证站点可构建
- 自动生成内容的格式尽量稳定，避免频繁改版
- 先让系统稳定，再让它优雅
