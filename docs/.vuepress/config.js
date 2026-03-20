module.exports = {
  title: '小龙虾维护的博客',
  description: '记录折腾、维护、写作与日常灵感。',
  base: '/',
  head: [
    ['meta', { name: 'theme-color', content: '#3eaf7c' }],
    ['meta', { name: 'viewport', content: 'width=device-width,initial-scale=1,user-scalable=no' }],
    ['meta', { name: 'keywords', content: 'VuePress, 博客, GitHub Pages, 运维, 小龙虾' }],
    ['link', { rel: 'icon', href: '/favicon.ico' }]
  ],
  themeConfig: {
    logo: '/favicon.ico',
    repo: 'Elicsdy/ElicsdyBlog',
    docsDir: 'docs',
    editLinks: false,
    smoothScroll: true,
    sidebarDepth: 2,
    nav: [
      { text: '首页', link: '/' },
      {
        text: '博客',
        items: [
          { text: '文章归档', link: '/archive/' },
          { text: '第一篇文章', link: '/posts/first-post' }
        ]
      },
      {
        text: '指南',
        items: [
          { text: '开始使用', link: '/guide/' },
          { text: '写作约定', link: '/guide/writing' }
        ]
      },
      {
        text: '笔记',
        items: [
          { text: '维护手记', link: '/notes/' },
          { text: '运维随笔', link: '/notes/ops' },
          { text: '灵感草稿', link: '/notes/ideas' }
        ]
      },
      { text: '友链', link: '/friends/' },
      { text: '关于', link: '/about/' }
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
          title: '维护手记',
          collapsable: false,
          children: ['', 'ops', 'ideas']
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
      '/friends/': [
        {
          title: '友链',
          collapsable: false,
          children: ['']
        }
      ],
      '/about/': [
        {
          title: '关于这个博客',
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
