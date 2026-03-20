# GitHub Pages 部署笔记（2026-03-20）

<p class="post-meta">记录时间：2026-03-20</p>

这篇笔记记录今天把博客从空仓库拉到可访问状态的全过程，方便以后照着再来一次，也方便回头排错。

## 今天做了什么

### 1. 准备 Git 和 GitHub 连接

先在本机确认了 git 可用，然后配置了：

- `user.name = Elicsdy`
- `user.email = 2903204554@qq.com`

接着生成 GitHub 专用 SSH key，加入 GitHub 账号，确保仓库可以正常 push。

## 2. 初始化博客仓库

仓库名：`ElicsdyBlog`

博客技术栈选择：

- **VuePress 1.x**
- 默认主题
- 保留顶部导航和左侧侧边栏
- 首页继续使用 Markdown

## 3. 首次部署 GitHub Pages

一开始先把代码推上仓库，再配置 GitHub Actions 部署 Pages。

这里遇到的关键问题是：

- **构建成功**
- **部署失败**

报错核心是：

> Failed to create deployment (404)

最后确认原因不是 VuePress 构建有问题，而是：

- **GitHub Pages 还没在仓库设置里启用好**

修复方式：

1. 打开 `Settings -> Pages`
2. 把 `Build and deployment` 的来源改成 **GitHub Actions**
3. 重新触发工作流

这一步做完之后，Pages 部署就成功了。

## 4. 绑定自定义域名

域名：`Elicsdy.hlaq.top`

处理方式：

- 仓库里加入 `CNAME`
- DNS 配置 `CNAME -> Elicsdy.github.io`

刚配完时自定义域名还是 404，但默认 Pages 地址已经可以访问。等 GitHub Pages 接管域名和证书完成后，自定义域名就恢复成正常访问。

## 5. 评论系统

评论系统最终接的是：

- **Utterances**

它依赖：

- 仓库启用 Issues
- GitHub 账号安装 Utterances App

安装完后，评论区就能正常显示。

## 6. 之后又补了什么

今天后续又补了几块：

- 首页重新收了一版结构
- 新增新闻推送板块
- 配置每天 00:00 自动生成热点新闻
- 把新闻口径改成了 **国内 10 条 + 国际 10 条**

## 这次部署里最重要的经验

### Pages 失败，先看是不是没启用好

如果 GitHub Actions 的 build 成功、deploy 失败，先别急着怀疑代码，先看仓库 Pages 设置是不是已经正确启用。

### 先打通链路，再优化样式

最重要的是先做到：

- 仓库能 push
- Pages 能跑
- 域名能开
- 评论能显示

这些都通了，博客才算真的“活了”。

### 自动化适合早点接

像新闻推送这种规律性内容，越早脚本化越省事。后面只需要调规则，不需要每天手工重复。

## 当前状态

截至这篇笔记写下时，博客已经具备：

- GitHub Pages 正常访问
- 自定义域名正常访问
- 评论区正常显示
- 新闻板块自动更新

这就够作为一个长期维护的起点了。
