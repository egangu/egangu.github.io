---
permalink: /cv/
title: "Curriculum Vitae"
excerpt: "Yanggan Gu's curriculum vitae"
author_profile: false
---

<div class="cv-page">
  <div class="cv-page__header">
    <div>
      <h1>Curriculum Vitae</h1>
      <p>English and Chinese versions are available below.</p>
    </div>
  </div>

  <section class="cv-page__version" aria-labelledby="cv-english">
    <div class="cv-page__header">
      <div><h2 id="cv-english">English Version</h2></div>
      <div class="cv-page__actions">
        <a class="btn btn--info" href="{{ '/files/cv.pdf' | relative_url }}" download="Yanggan_Gu_CV_EN.pdf">
          <i class="fas fa-fw fa-download" aria-hidden="true"></i> Download English PDF
        </a>
        <a class="btn btn--inverse" href="{{ '/files/cv.pdf' | relative_url }}" target="_blank" rel="noopener">
          <i class="fas fa-fw fa-external-link-alt" aria-hidden="true"></i> Open English PDF
        </a>
      </div>
    </div>

    <iframe
      class="cv-page__preview"
      src="{{ '/files/cv.pdf' | relative_url }}#view=FitH"
      title="Yanggan Gu's English curriculum vitae in PDF format"
      loading="lazy">
    </iframe>

    <p class="cv-page__fallback">
      PDF preview is unavailable on smaller screens. Please
      <a href="{{ '/files/cv.pdf' | relative_url }}">open or download the English PDF</a>.
    </p>
  </section>

  <section class="cv-page__version" aria-labelledby="cv-chinese">
    <div class="cv-page__header">
      <div><h2 id="cv-chinese">中文版</h2></div>
      <div class="cv-page__actions">
        <a class="btn btn--info" href="{{ '/files/cv-zh.pdf' | relative_url }}" download="Yanggan_Gu_CV_ZH.pdf">
          <i class="fas fa-fw fa-download" aria-hidden="true"></i> 下载中文 PDF
        </a>
        <a class="btn btn--inverse" href="{{ '/files/cv-zh.pdf' | relative_url }}" target="_blank" rel="noopener">
          <i class="fas fa-fw fa-external-link-alt" aria-hidden="true"></i> 打开中文 PDF
        </a>
      </div>
    </div>

    <iframe
      class="cv-page__preview"
      src="{{ '/files/cv-zh.pdf' | relative_url }}#view=FitH"
      title="辜仰淦的中文简历 PDF"
      loading="lazy">
    </iframe>

    <p class="cv-page__fallback">
      小屏幕上无法预览 PDF，请<a href="{{ '/files/cv-zh.pdf' | relative_url }}">打开或下载中文 PDF</a>。
    </p>
  </section>
</div>
