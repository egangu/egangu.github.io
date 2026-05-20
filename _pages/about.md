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

<span class="anchor" id="about-me"></span>

Hi, my name is Yanggan Gu (辜仰淦). I am currently a PhD student at [Hong Kong Polytechnic University (PolyU)](https://www.polyu.edu.hk/), advised by [Prof. Hongxia Yang](https://www4.comp.polyu.edu.hk/~hongxyang/). Before this, I received my Master's degree from Soochow University in 2025, advised by [Prof. Zhenghua Li](https://web.suda.edu.cn/zhli13/).

My research trajectory began with syntactic and semantic parsing and has now shifted to Large Language Models (LLMs). My current research focuses on **model merging and fusion**, **scaling laws**, and **human-aligned, trustworthy AI**.

# 🔥 News {#news}

- *2026.05*: &nbsp;🎉🎉 Model Merging Scaling Laws in Large Language Models has been accepted to ICML 2026!
- *2025.09*: &nbsp;🎉🎉 Two papers have been accepted to NeurIPS 2025!
- *2025.02*: &nbsp;🎉🎉 Two papers have been accepted to ACL 2025 Findings!

# 📝 Publications {#publications}

### 2026

- 📄 [C8] Yuanyi Wang, <strong class="author-highlight">Yanggan Gu (Co-1st)</strong>, Yiming Zhang, Qi Zhou, Zhaoyi Yan, Congkai Xie, Xinyao Wang, Jianbo Yuan, Hongxia Yang. Model Merging Scaling Laws in Large Language Models. In <strong>ICML 2026</strong>. 🔗[[Paper]](https://arxiv.org/abs/2509.24244) [[Project]](https://infix-ai.com/research/ScalingLaws) [[Code]](https://github.com/InfiXAI/Merging-Scaling-Law)

- 📄 [J2] Qi Zhou, Yiming Zhang, <strong class="author-highlight">Yanggan Gu</strong>, Yuanyi Wang, Zhaoyi Yan, Zhen Li, Chi Yung Chung, Hongxia Yang. Model Fusion for Scalable and Sustainable Artificial Intelligence: A Review and Outlook. In <strong>Journal of Modern Power Systems and Clean Energy</strong>, 2026. 🔗[[Paper]](https://doi.org/10.35833/MPCE.2025.000973)

- 📄 [Pre1] Yuanyi Wang, <strong class="author-highlight">Yanggan Gu</strong>, Zihao Wang, Kunxi Li, Yifan Yang, Zhaoyi Yan, Congkai Xie, Jianmin Wu, Hongxia Yang. MergePipe: A Budget-Aware Parameter Management System for Scalable LLM Merging. In arXiv 2026. 🔗[[Paper]](https://arxiv.org/abs/2602.13273) [[Code]](https://github.com/wyy-code/mergepipe)

- 📄 [Pre2] Yuanyi Wang, Yifan Yang, Su Lu, <strong class="author-highlight">Yanggan Gu</strong>, Pengkai Wang, Wenjun Wang, Zhaoyi Yan, Congkai Xie, Jianmin Wu, Jialun Cao, Shing-Chi Cheung, Hongxia Yang. Geometry Conflict: Explaining and Controlling Forgetting in LLM Continual Post-Training. In arXiv 2026. 🔗[[Paper]](https://arxiv.org/abs/2605.09608) [[Code]](https://github.com/wyy-code/GCWM)

- 📄 [Pre3] <strong class="author-highlight">Yanggan Gu</strong>, Shuo Cai, Zihao Wang, Wenjun Wang, Yuanyi Wang, Pengkai Wang, Sirui Huang, Su Lu, Jianmin Wu, Hongxia Yang. FeatCal: Feature Calibration for Post-Merging Models. In arXiv 2026. 🔗[[Paper]](https://arxiv.org/abs/2605.13030) [[Code]](https://github.com/egangu/featcal)

- 📄 [Pre4] Wenjun Wang, <strong class="author-highlight">Yanggan Gu (Co-1st)</strong>, Shuo Cai, Yuanyi Wang, Pengkai Wang, Jianmin Wu, Hongxia Yang. E-PMQ: Expert-Guided Post-Merge Quantization with Merged-Weight Anchoring. In arXiv 2026. 🔗[[Paper]](https://arxiv.org/abs/2605.16882) [[Code]](https://github.com/wwjzhy/E-PMQ)

### 2025

- 📄 [C6] <strong class="author-highlight">Yanggan Gu</strong>, Yuanyi Wang, Zhaoyi Yan, Yiming Zhang, Qi Zhou, Fei Wu, Hongxia Yang. InfiFPO: Implicit Model Fusion via Preference Optimization in Large Language Models. In <strong>NeurIPS 2025</strong> <span class="pub-badge">Spotlight</span>. 🔗[[Paper]](https://arxiv.org/pdf/2505.13878) [[Code]](https://github.com/InfiXAI/InfiFPO) [[Model]](https://huggingface.co/InfiX-ai/InfiFPO-14B)

- 📄 [C7] Yuanyi Wang, Zhaoyi Yan, Yiming Zhang, Qi Zhou, <strong class="author-highlight">Yanggan Gu</strong>, Fei Wu, Hongxia Yang. InfiGFusion: Graph-on-Logits Distillation via Efficient Gromov-Wasserstein for Model Fusion. In <strong>NeurIPS 2025</strong>. 🔗[[Paper]](https://arxiv.org/pdf/2505.13893) [[Project]](https://infix-ai.com/research/infigfusion/) [[Code]](https://github.com/InfiXAI/InfiGFusion) [[Model]](https://huggingface.co/InfiX-ai/InfiGFusion-14B)

- 📄 [J1] Qi Zhou, Yiming Zhang, <strong class="author-highlight">Yanggan Gu</strong>, Yuanyi Wang, Zhijie Sang, Zhaoyi Yan, Zhen Li, Shengyu Zhang, Fei Wu, Hongxia Yang. Democratizing AI Through Model Fusion: A Comprehensive Review and Future Directions. In <strong>Nexus</strong>. 🔗[[Paper]](https://www.cell.com/nexus/pdf/S2950-1601(25)00049-X.pdf)

- 📄 [C5] Yunkai Dang, Mengxi Gao, Yibo Yan, Xin Zou, <strong class="author-highlight">Yanggan Gu</strong>, Aiwei Liu, Xuming Hu. Exploring Response Uncertainty in MLLMs: An Empirical Evaluation under Misleading Scenarios. In <strong>EMNLP 2025 Main</strong>. 🔗[[Paper]](https://arxiv.org/pdf/2411.02708)

- 📄 [C2] <strong class="author-highlight">Yanggan Gu</strong>, Junzhuo Li, Sirui Huang, Xin Zou, Zhenghua Li, Xuming Hu. Capturing Nuanced Preferences: Preference-Aligned Distillation for Small Language Models. In <strong>ACL 2025 Findings</strong>. 🔗[[Paper]](https://aclanthology.org/2025.findings-acl.822.pdf)

- 📄 [C3] Sirui Huang, <strong class="author-highlight">Yanggan Gu (Co-1st)</strong>, Zhonghao Li, Xuming Hu, Li Qing, Guandong Xu. StructFact: Reasoning Factual Knowledge from Structured Data with Large Language Models. In <strong>ACL 2025 Findings</strong>. 🔗[[Paper]](https://aclanthology.org/2025.findings-acl.391.pdf)

- 📄 [C4] Sirui Huang, Hanqian Li, <strong class="author-highlight">Yanggan Gu</strong>, Xuming Hu, Qing Li, Guandong Xu. HyperG: Hypergraph-Enhanced LLMs for Structured Knowledge. In <strong>SIGIR 2025</strong>. 🔗[[Paper]](https://dl.acm.org/doi/pdf/10.1145/3726302.3730002)

### 2024

- 📄 [C1] <strong class="author-highlight">Yanggan Gu</strong>, Yang Hou, Zhefeng Wang, Xinyu Duan, Zhenghua Li. High-Order Joint Constituency and Dependency Parsing. In <strong>COLING 2024</strong>. 🔗[[Paper]](https://aclanthology.org/2024.lrec-main.713.pdf)

# 🎖 Honors and Awards {#honors-and-awards}

- 2023.08: 1st place in the CCL-2023 Chinese AMR Parsing Evaluation Task. [Report](https://aclanthology.org/2023.ccl-3.5/)
- 2021.12: Top 10 Innovative Figures of Guangdong University of Technology. [Sohu News](https://www.sohu.com/a/507610953_121124288)
- 2021.11: National Encouragement Scholarship. [Link](https://edu.gd.gov.cn/zwgknew/gsgg/content/post_3678694.html)
- 2021.11: 1st Prize at the 9th "China Software Cup" College Student Design Competition. [Link](https://www.cnsoftbei.com/content-1-565-1.html)

# 🪴 Service {#service}

- Reviewer: ICML 2026, ICLR 2026, NeurIPS 2026.

# 🎓 Education {#education}

- 2025.09 - Present, PhD student at [Hong Kong Polytechnic University (PolyU)](https://www.polyu.edu.hk/), advised by [Prof. Hongxia Yang](https://www4.comp.polyu.edu.hk/~hongxyang/).
- 2022.09 - 2025.06, Graduate student at NLP Lab, Soochow University, advised by [Prof. Zhenghua Li](https://web.suda.edu.cn/zhli13/).
- 2018.09 - 2022.06, Undergraduate student at School of Computer Science, Guangdong University of Technology, advised by [Prof. Guangqiang Xie](https://yzw.gdut.edu.cn/info/1120/1879.htm).

# 💻 Internships {#internships}

- 2025.06 - 2025.12, [InfiX-ai](https://huggingface.co/InfiX-ai), Shenzhen, China.
