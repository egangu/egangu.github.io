---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

# 👋 About Me

Hi, my name is Yanggan Gu (辜仰淦). I am currently a PhD student at [Hong Kong Polytechnic University (PolyU)](https://www.polyu.edu.hk/), fortunately advised by [Prof. Hongxia Yang](https://www4.comp.polyu.edu.hk/~hongxyang/). Before this, I received my Master’s degree from Soochow University in 2025, fortunately advised by [Prof. Zhenghua Li](https://web.suda.edu.cn/zhli13/). 

My research trajectory began with syntactic and semantic parsing and has now shifted to Large Language Models (LLMs). I am particularly interested in **model merging and fusion**, as well as **human-aligned, trustworthy AI**.

# 🔬 Research Snapshot

<div class="research-snapshot">
  <div class="research-pill">
    <strong>Model Merging &amp; Fusion</strong>
    <span>Composing, adapting, and reusing LLMs through efficient model composition methods.</span>
  </div>
  <div class="research-pill">
    <strong>Scaling Laws</strong>
    <span>Understanding how model size, expert number, and domain diversity shape merging performance.</span>
  </div>
  <div class="research-pill">
    <strong>Trustworthy AI</strong>
    <span>Preference learning, uncertainty estimation, and structured reasoning for reliable LLMs.</span>
  </div>
</div>

# 🔥 News

- *2026.05*: &nbsp;🎉🎉 Model Merging Scaling Laws in Large Language Models has been accepted to ICML 2026!
- *2025.09*: &nbsp;🎉🎉 Two papers have been accepted to NeurIPS 2025!
- *2025.02*: &nbsp;🎉🎉 Two papers have been accepted to ACL 2025 Findings!

# 🌟 Selected Publications

<div class="selected-publications">
  <article class="selected-publication">
    <div class="selected-publication__venue"><span class="venue-badge venue-icml">ICML 2026</span></div>
    <div class="selected-publication__body">
      <h3><a href="https://arxiv.org/abs/2509.24244">Model Merging Scaling Laws in Large Language Models.</a></h3>
      <p>A scaling-law study that turns model merging into predictable, budget-aware planning.</p>
      <div class="paper-links"><a href="https://arxiv.org/abs/2509.24244">Paper</a><a href="https://infix-ai.com/research/ScalingLaws">Project</a><a href="https://github.com/InfiXAI/Merging-Scaling-Law">Code</a></div>
    </div>
  </article>
  <article class="selected-publication">
    <div class="selected-publication__venue"><span class="venue-badge venue-spotlight">NeurIPS 2025 Spotlight</span></div>
    <div class="selected-publication__body">
      <h3><a href="https://arxiv.org/pdf/2505.13878">InfiFPO: Implicit Model Fusion via Preference Optimization in Large Language Models.</a></h3>
      <p>A preference-optimization framework for fusing source-model behaviors while aligning a pivot model.</p>
      <div class="paper-links"><a href="https://arxiv.org/pdf/2505.13878">Paper</a><a href="https://github.com/InfiXAI/InfiFPO">Code</a><a href="https://huggingface.co/InfiX-ai/InfiFPO-14B">Model</a></div>
    </div>
  </article>
  <article class="selected-publication">
    <div class="selected-publication__venue"><span class="venue-badge venue-neurips">NeurIPS 2025</span></div>
    <div class="selected-publication__body">
      <h3><a href="https://arxiv.org/pdf/2505.13893">InfiGFusion: Graph-on-Logits Distillation via Efficient Gromov-Wasserstein for Model Fusion.</a></h3>
      <p>A structure-aware model-fusion framework using graph-on-logits distillation.</p>
      <div class="paper-links"><a href="https://arxiv.org/pdf/2505.13893">Paper</a><a href="https://infix-ai.com/research/infigfusion/">Project</a><a href="https://github.com/InfiXAI/InfiGFusion">Code</a><a href="https://huggingface.co/InfiX-ai/InfiGFusion-14B">Model</a></div>
    </div>
  </article>
  <article class="selected-publication">
    <div class="selected-publication__venue"><span class="venue-badge venue-acl">ACL 2025 Findings</span></div>
    <div class="selected-publication__body">
      <h3><a href="https://aclanthology.org/2025.findings-acl.822.pdf">Capturing Nuanced Preferences: Preference-Aligned Distillation for Small Language Models.</a></h3>
      <p>A distillation method that transfers nuanced preference distributions from LLMs to smaller models.</p>
      <div class="paper-links"><a href="https://aclanthology.org/2025.findings-acl.822.pdf">Paper</a></div>
    </div>
  </article>
</div>

# 📝 Publications

_* denotes equal contribution._

**Model Merging&Fusion**

- <span class="venue-badge venue-icml">ICML 2026</span> [Model Merging Scaling Laws in Large Language Models.](https://arxiv.org/abs/2509.24244) Yuanyi Wang\*, **Yanggan Gu\***, Yiming Zhang\*, Qi Zhou, Zhaoyi Yan, Congkai Xie, Xinyao Wang, Jianbo Yuan, Hongxia Yang

- <span class="venue-badge venue-spotlight">NeurIPS 2025 Spotlight</span> [InfiFPO: Implicit Model Fusion via Preference Optimization in Large Language Models.](https://arxiv.org/pdf/2505.13878) **Yanggan Gu**, Yuanyi Wang, Zhaoyi Yan, Yiming Zhang, Qi Zhou, Fei Wu, Hongxia Yang

- <span class="venue-badge venue-neurips">NeurIPS 2025</span> [InfiGFusion: Graph-on-Logits Distillation via Efficient Gromov-Wasserstein for Model Fusion.](https://arxiv.org/pdf/2505.13893) Yuanyi Wang, Zhaoyi Yan, Yiming Zhang, Qi Zhou, **Yanggan Gu**, Fei Wu, Hongxia Yang

- <span class="venue-badge">Nexus</span> [Democratizing AI Through Model Fusion: A Comprehensive Review and Future Directions.](https://www.cell.com/nexus/pdf/S2950-1601(25)00049-X.pdf) Qi Zhou, Yiming Zhang, **Yanggan Gu**, Yuanyi Wang, Zhijie Sang, Zhaoyi Yan, Zhen Li, Shengyu Zhang, Fei Wu, Hongxia Yang

**Human-Aligned and Trustworthy AI**

- <span class="venue-badge venue-emnlp">EMNLP 2025 Main</span> [Exploring Response Uncertainty in MLLMs: An Empirical Evaluation under Misleading Scenarios.](https://arxiv.org/pdf/2411.02708) Yunkai Dang, Mengxi Gao, Yibo Yan, Xin Zou, **Yanggan Gu**, Aiwei Liu, Xuming Hu

- <span class="venue-badge venue-acl">ACL 2025 Findings</span> [Capturing Nuanced Preferences: Preference-Aligned Distillation for Small Language Models.](https://aclanthology.org/2025.findings-acl.822.pdf) **Yanggan Gu**, Junzhuo Li, Sirui Huang, Xin Zou, Zhenghua Li, Xuming Hu

- <span class="venue-badge venue-acl">ACL 2025 Findings</span> [StructFact: Reasoning Factual Knowledge from Structured Data with Large Language Models.](https://aclanthology.org/2025.findings-acl.391.pdf) Sirui Huang\*, **Yanggan Gu\***, Zhonghao Li, Xuming Hu, Li Qing, Guandong Xu

- <span class="venue-badge venue-sigir">SIGIR 2025</span> [HyperG: Hypergraph-Enhanced LLMs for Structured Knowledge.](https://dl.acm.org/doi/pdf/10.1145/3726302.3730002) Sirui Huang, Hanqian Li, **Yanggan Gu**, Xuming Hu, Qing Li, Guandong Xu

**Syntactic  Parsing**

- <span class="venue-badge">COLING 2024</span> [High-Order Joint Constituency and Dependency Parsing.](https://aclanthology.org/2024.lrec-main.713.pdf) **Yanggan Gu**, Yang Hou, Zhefeng Wang, Xinyu Duan, Zhenghua Li

# 🎖 Honors and Awards

- *2023.08* 1st place in the CCL-2023 Chinese AMR Parsing Evaluation Task. [Report](https://aclanthology.org/2023.ccl-3.5/). 
- *2021.12* Top 10 Innovative Figures of Guangdong University of Technology. [Sohu News](https://www.sohu.com/a/507610953_121124288)
- *2021.11* National Encouragement Scholarship. [Link](https://edu.gd.gov.cn/zwgknew/gsgg/content/post_3678694.html)
- *2021.11* 1st Prize at the 9th “China Software Cup” College Student Design Competition. [Link](https://www.cnsoftbei.com/content-1-565-1.html)

# 🤝 Service

- Reviewer: ICLR 2026, NeurIPS 2026.

# 📖 Education

- *2022.09 - 2025.06*, Graduate student at NLP Lab, Soochow University, advised by [Prof. Zhenghua Li](https://web.suda.edu.cn/zhli13/). 
- *2018.09 - 2022.06*, Undergraduate student at School of Computer Science, Guangdong University of Technology, advised by [Prof. Guangqiang Xie](https://yzw.gdut.edu.cn/info/1120/1879.htm). 

# 💻 Internships

- *2025.06 - 2025.12*, [InfiX-ai](https://huggingface.co/InfiX-ai), Shenzhen, China.
