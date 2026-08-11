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
      <p>View the latest version below or download a copy for offline reading.</p>
    </div>
    <div class="cv-page__actions">
      <a class="btn btn--info" href="{{ '/files/cv.pdf' | relative_url }}" download="Yanggan_Gu_CV.pdf">
        <i class="fas fa-fw fa-download" aria-hidden="true"></i> Download PDF
      </a>
      <a class="btn btn--inverse" href="{{ '/files/cv.pdf' | relative_url }}" target="_blank" rel="noopener">
        <i class="fas fa-fw fa-external-link-alt" aria-hidden="true"></i> Open in new tab
      </a>
    </div>
  </div>

  <iframe
    class="cv-page__preview"
    src="{{ '/files/cv.pdf' | relative_url }}#view=FitH"
    title="Yanggan Gu's curriculum vitae in PDF format"
    loading="lazy">
  </iframe>

  <p class="cv-page__fallback">
    PDF preview is unavailable on smaller screens. Please
    <a href="{{ '/files/cv.pdf' | relative_url }}">open or download the PDF</a>.
  </p>
</div>
