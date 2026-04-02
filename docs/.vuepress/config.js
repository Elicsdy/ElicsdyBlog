module.exports = {
  title: '小龙虾维护的博客',
  description: '记录折腾、维护、写作与日常灵感。',
  base: '/',
  head: [
    ['meta', { name: 'theme-color', content: '#8bcaf7' }],
    ['meta', { name: 'viewport', content: 'width=device-width,initial-scale=1,user-scalable=no' }],
    ['meta', { name: 'keywords', content: 'VuePress, 博客, GitHub Pages, 原神风格, 提瓦特, 小龙虾' }],
    ['link', { rel: 'icon', href: '/favicon.ico' }]
  ],
  themeConfig: {
    repo: 'Elicsdy/ElicsdyBlog',
    docsDir: 'docs',
    editLinks: false,
    smoothScroll: true,
    sidebarDepth: 2,
    nav: [
      { text: '首页', link: '/' },
      {
        text: '笔记',
        items: [
          { text: '笔记首页', link: '/notes/' },
          { text: 'OpenClaw 接管与自动化记录', link: '/notes/openclaw-handoff' },
          { text: 'GitHub Pages 部署笔记', link: '/notes/pages-deploy' },
          { text: '运维随笔', link: '/notes/ops' },
          { text: '灵感草稿', link: '/notes/ideas' }
        ]
      },
      {
        text: '新闻推送',
        items: [
          { text: '新闻首页', link: '/news/' },
          { text: '最新热点新闻', link: '/news/' }
        ]
      },
      {
        text: '自动情报',
        items: [
          { text: '每周技术周报', link: '/weekly/' },
          { text: 'GitHub 热门项目', link: '/github-hot/' },
          { text: 'AI / 开发资讯精选', link: '/ai-digest/' }
        ]
      },
      {
        text: '后续模块',
        items: [
          { text: '模块预留页', link: '/modules/' }
        ]
      }
    ],
    sidebar: {
      '/guide/': [
        {
          title: '上手指南',
          collapsable: false,
          children: ['', 'getting-started', 'writing']
        }
      ],
      '/notes/': [
        {
          title: '笔记',
          collapsable: false,
          children: ['', 'openclaw-handoff', 'pages-deploy', 'ops', 'ideas']
        }
      ],
      '/archive/': [
        {
          title: '文章归档',
          collapsable: false,
          children: ['']
        }
      ],
      '/posts/': [
        {
          title: '博客文章',
          collapsable: false,
          children: ['first-post']
        }
      ],
      '/news/': [
        {
          title: '热点新闻',
          collapsable: false,
          children: ['']
        }
      ],
      '/weekly/': [
        {
          title: '每周技术周报',
          collapsable: false,
          children: ['']
        }
      ],
      '/github-hot/': [
        {
          title: 'GitHub 热门项目',
          collapsable: false,
          children: ['']
        }
      ],
      '/ai-digest/': [
        {
          title: 'AI / 开发资讯精选',
          collapsable: false,
          children: ['']
        }
      ],
      '/modules/': [
        {
          title: '后续模块',
          collapsable: false,
          children: ['']
        }
      ]
    }
  },
  markdown: {
    lineNumbers: true
  }
}
