# 将 Typst CV 发布到 GitHub Pages / Jekyll：方案调研

> 调研日期：2026-08-11。资料只采用项目官方文档、GitHub 官方文档和公开仓库的源码；链接均直接指向原始资料或具体实现文件。

## 结论

推荐采用 **“独立的 `/cv/` HTML 页面 + `/files/cv.pdf` 直接下载 + 宽屏原生 `iframe` 预览 + GitHub Actions 自动编译”**。

这把 PDF 保持为招聘方可下载、可打印的权威版本，同时让主页访客无需离站即可阅读。`iframe` 只是渐进增强：页面必须始终有“打开 PDF / 下载 PDF”链接，移动端可以只显示这个链接。对于一份通常只有 1--3 页的 CV，不建议一开始引入 PDF.js。

本仓库已经在 [`_config.yml`](../_config.yml) 的 `include` 中列入了 `files`，因此最终生成的 `files/cv.pdf` 会随 Jekyll 站点发布；可用 `{{ '/files/cv.pdf' | relative_url }}` 生成同时兼容用户页和项目页的 URL。

Typst 官方说明 `compile` 与 `watch` 在不指定格式时会生成 PDF，PDF 也是默认导出格式；PDF 还支持文本/结构提取和 Tagged PDF（默认写入），很适合作为 CV 的可下载交付物。[Typst：PDF 导出](https://typst.app/docs/reference/pdf/)

## 四种方式的比较

| 方式 | 适用场景 | 优点 | 代价/限制 | 建议 |
| --- | --- | --- | --- | --- |
| 直接链接下载 PDF | 所有 CV 都应具备 | 最简单、URL 稳定、打印/投递自然 | 无站内阅读体验 | **必选** |
| 原生 `iframe` / `embed` / `object` | 想在 `/cv/` 站内预览 | 几行 HTML、零额外 JS；浏览器 PDF 阅读器负责缩放/搜索 | 外观与能力取决于访问者浏览器；必须有降级链接 | **推荐的预览层**，优先 `iframe` |
| PDF.js | 需要统一的工具栏、页码、缩略图、搜索或希望不依赖浏览器原生预览 | 完全由站点控制的 HTML5 PDF viewer | 要发布 viewer、worker、字体/资源，并跟进安全与版本更新；站点体积、维护复杂度更高 | 仅有明确高级需求时使用 |
| CI 自动编译并部署 | Typst 源码会持续更新 | 源码、PDF、网页同次提交保持同步；避免手工漏传 PDF | 要将 Pages 发布源切到 GitHub Actions，并在工作流中构建 Jekyll | **推荐** |

`<object>` 能提供其内部 fallback 内容，`<embed>` 的 fallback/可访问性较弱；对本站而言，用 `iframe` 加同页下载链接更直接。下面是可放入 Jekyll 页面（例如 `_pages/cv.md`）的最小结构：

```html
<p>
  <a href="{{ '/files/cv.pdf' | relative_url }}" download>下载 CV（PDF）</a>
  ·
  <a href="{{ '/files/cv.pdf' | relative_url }}" target="_blank" rel="noopener">在新标签页打开</a>
</p>

<iframe
  src="{{ '/files/cv.pdf' | relative_url }}"
  title="Yanggan Gu 的 CV（PDF）"
  width="100%"
  height="900">
  <p>浏览器无法内嵌预览；请<a href="{{ '/files/cv.pdf' | relative_url }}">下载 CV PDF</a>。</p>
</iframe>
```

应以 CSS 媒体查询在窄屏隐藏或缩短 iframe，但不要隐藏上述两个链接。不要把仅供工作流下载的 Actions artifact 当作公开 CV URL：它适合在工作流内传递构建结果，而非稳定的对外文件地址。[GitHub Actions：artifact 用途](https://docs.github.com/en/actions/tutorials/store-and-share-data)

## CI 自动编译与 Pages 部署

Typst 的 CLI 用法是 `typst compile source.typ output.pdf`；需要自带字体时可传 `--font-path`。[Typst 编译器 README：Usage](https://github.com/typst/typst#usage)

目前可用的 Typst 安装 action 是社区维护的 [`typst-community/setup-typst`](https://github.com/typst-community/setup-typst)，不是 `typst-community/typst-action`（后者目前不存在）。它的 [`action.yml`](https://github.com/typst-community/setup-typst/blob/main/action.yml) 定义了 `typst-version`、包缓存等输入，README 给出 `setup-typst` 后直接运行 `typst compile` 的示例。[setup-typst README](https://github.com/typst-community/setup-typst#basic-usage)

对这个 Jekyll 仓库，合理的工作流顺序是：

```text
cv/*.typ、字体、工作流或主分支变更
  → setup-typst（固定 Typst 版本）
  → typst compile cv/main.typ files/cv.pdf
  → bundle exec jekyll build --destination _site
  → upload-pages-artifact (_site)
  → deploy-pages
```

不要只上传 `files/cv.pdf`：这样会丢失 Jekyll 生成的主页。应上传完整 `_site`，让 PDF 与主页成为同一个 Pages artifact。字体若未被 Typst 模板嵌入或 runner 没有安装，应提交到仓库并用 `--font-path` 指定，确保本地和 CI 输出一致。

GitHub Pages 官方文档要求/建议的自定义工作流链路是 `configure-pages`、构建静态文件、`upload-pages-artifact`，随后在依赖 build 的 deploy job 中使用 `deploy-pages`；部署 job 至少需要 `pages: write` 和 `id-token: write` 权限，并建立环境（通常为 `github-pages`）。[GitHub Pages：使用自定义工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

可作为后续实施的骨架（具体 Typst 入口路径待 CV 仓库确定）：

```yaml
name: Build and deploy site
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: typst-community/setup-typst@v5
        with:
          typst-version: 0.14.2 # 实施时固定到 CV 已验证的版本
      - run: typst compile --font-path cv/fonts cv/main.typ files/cv.pdf
      - run: bundle install && bundle exec jekyll build --destination _site
      - uses: actions/upload-pages-artifact@v4
        with:
          path: _site
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

采用该工作流前，需要在仓库 Pages 设置中把发布源改为 **GitHub Actions**。[GitHub Pages：配置 publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## PDF.js 何时值得引入

[Mozilla PDF.js](https://github.com/mozilla/pdf.js) 是基于 HTML5 的 PDF viewer。其源码中的 [`web/viewer.html`](https://github.com/mozilla/pdf.js/blob/master/web/viewer.html) 是 viewer 壳，[`web/app.js`](https://github.com/mozilla/pdf.js/blob/master/web/app.js#L887-L898) 会读取 `?file=` 查询参数加载 PDF。把官方构建产物作为站点静态资源后，可用类似下面的地址：

```html
<iframe
  src="{{ '/pdfjs/web/viewer.html?file=../../files/cv.pdf' | relative_url }}"
  title="CV PDF 阅读器">
</iframe>
```

实际部署必须核对 `viewer.html` 到 `cv.pdf` 的相对路径，并让 PDF 与 viewer 保持同源；不可只复制一个 `viewer.html`。PDF.js 官方 README 说明生产构建会产生 viewer 依赖的 `pdf.js` 与 `pdf.worker.js`，二者都需要发布。[PDF.js：Building PDF.js](https://github.com/mozilla/pdf.js#building-pdfjs)

因此只有在“各浏览器一致预览”或完整 viewer 功能是产品需求时，才选 PDF.js；CV 页面通常没有这个必要。

## 可直接借鉴的开源实现

1. **最贴近目标：Typst CV + 原生预览 + 下载 + Pages CI** — [kheison/Free-CV-Maker-Template 的 `build-cv.yml`](https://github.com/kheison/Free-CV-Maker-Template/blob/main/.github/workflows/build-cv.yml)。同一 workflow 中用 `setup-typst` 编译 `cv.typ → CV.pdf`，复制 PDF 到 Pages 产物，生成含 `<iframe src="CV.pdf">` 与 `download` 链接的 `index.html`，最后用 `upload-pages-artifact` / `deploy-pages` 部署。这是四个方案在一个小仓库中的完整串联参考。
2. **Typst CV + 两阶段 Pages artifact/deploy** — [HyperSoWeak/cv 的 `deploy-resume.yml`](https://github.com/HyperSoWeak/cv/blob/main/.github/workflows/deploy-resume.yml)。build job 安装 Typst、编译 `resume.typ → resume.pdf`、复制到 `dist` 并上传；deploy job 依赖 build。这特别适合把本仓库原来的 Jekyll build 插在“编译”与“上传”之间。
3. **独立 HTML 页面与可访问 fallback 的实际样式** — [kheison workflow 内的生成 HTML](https://github.com/kheison/Free-CV-Maker-Template/blob/main/.github/workflows/build-cv.yml#L48-L117)。其中 iframe 有 `title`，并且同屏有 PDF 下载按钮；可直接把结构迁移到 `_pages/cv.md`，样式改为本站 SCSS。
4. **不使用 PDF 预览、改用 Typst 生成 SVG** — [gotenksIN/resume 的 `index.html`](https://github.com/gotenksIN/resume/blob/main/index.html#L104-L121) 与 [Pages workflow](https://github.com/gotenksIN/resume/blob/main/.github/workflows/deploy.yml)。该实现保留 PDF 下载，但以 `<object data="resume.svg">` 进行站内展示。这是想要更可控、可响应式的视觉预览时的另一条路，但需额外把 Typst 输出 SVG，并不等同于 PDF reader。
5. **可复用的多文档 Typst Pages 工作流** — [luiswirth/typst-deploy 的源码 workflow](https://github.com/luiswirth/typst-deploy/blob/main/.github/workflows/typst-deploy.yml)。它接收多个 `.typ` 输入、逐个编译为 `public/*.pdf`，再生成 PDF 列表/重定向页并部署。适合以后把“CV、research statement、teaching statement”一起发布。

## 推荐的实施顺序

1. 先将经本地检查的 `cv.pdf` 放到 `files/cv.pdf`，在 About 页加“CV（PDF）”链接；这是立即可用且风险最低的发布路径。
2. 新增 `/cv/` 页面，加入上述 `iframe` 和显式下载/新窗口链接，并在手机端确认链接可用。
3. CV Typst 源码确定位置后，再切换到自定义 Pages Action：每次合并 main 自动重新生成 `files/cv.pdf` 和 Jekyll `_site`。
4. 只有真的需要统一 viewer 功能时，才引入、固定版本并定期更新 PDF.js。
