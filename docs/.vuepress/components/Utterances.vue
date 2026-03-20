<template>
  <div class="utterances-wrapper">
    <div ref="comments"></div>
  </div>
</template>

<script>
export default {
  name: 'Utterances',
  props: {
    repo: {
      type: String,
      required: true
    },
    issueTerm: {
      type: String,
      default: 'pathname'
    },
    label: {
      type: String,
      default: 'comment'
    },
    theme: {
      type: String,
      default: 'github-light'
    }
  },
  mounted() {
    this.renderComments()
  },
  watch: {
    '$route.path'() {
      this.renderComments()
    }
  },
  methods: {
    renderComments() {
      const container = this.$refs.comments
      if (!container) return
      container.innerHTML = ''
      const script = document.createElement('script')
      script.src = 'https://utteranc.es/client.js'
      script.async = true
      script.setAttribute('repo', this.repo)
      script.setAttribute('issue-term', this.issueTerm)
      script.setAttribute('label', this.label)
      script.setAttribute('theme', this.theme)
      script.setAttribute('crossorigin', 'anonymous')
      container.appendChild(script)
    }
  }
}
</script>
