#set text(font: "Linux Biolinum", lang: "zh", size: 10.5pt)
#show heading: set text(font: "Linux Biolinum")
#show link: underline

#set page(
  margin: (x: 0.9cm, y: 1.1cm),
)

#set par(justify: true)

#let chiline() = { v(-3pt); line(length: 100%); v(-5pt) }

= 辜仰淦（Yanggan Gu）

yanggangu\@outlook.com |
#link("https://scholar.google.com/citations?user=cY4ofhcAAAAJ&hl=en")[Google Scholar] | #link("https://egangu.github.io/")[个人主页] |
#link("https://github.com/EganGu")[GitHub]

== 教育经历
#chiline()

#link("https://www.polyu.edu.hk/")[*香港理工大学*]，中国香港。 #h(1fr) 2026/01 - 至今 \
_计算学博士生（Ph.D. student in Computing）。_ #h(1fr) 导师：#link("https://www4.comp.polyu.edu.hk/~hongxyang/")[杨红霞教授] \

#link("https://eng.suda.edu.cn/")[*苏州大学*] [_211 工程_]，苏州，中国。 #h(1fr) 2022/09 - 2025/06 \
_计算机科学与技术硕士。_ #h(1fr) GPA 3.7（前 5%） \

#link("https://english.gdut.edu.cn/")[*广东工业大学*]，广州，中国。 #h(1fr) 2018/09 - 2022/06 \
_软件工程学士。_ #h(1fr) GPA 4.0（前 1%） \

== 研究经历
#chiline()

*Model Fusion in LLMs*，_研究人员_ #h(1fr) 2025/04 - 至今 \
#link("https://www.polyu.edu.hk/comp/")[香港理工大学计算学系]。 #h(1fr) 导师：#link("https://www4.comp.polyu.edu.hk/~hongxyang/")[杨红霞教授] \
_研究方向_：Model Fusion、LLM Alignment、LLM Reasoning

*Trustworthy LLMs*，_研究助理_ #h(1fr) 2024/06 - 2025/03 \
#link("https://www.hkust-gz.edu.cn/academics/hubs-and-thrust-areas/information-hub/artificial-intelligence/")[香港科技大学（广州）人工智能学域]。 #h(1fr) 导师：#link("https://scholar.google.com/citations?user=dbBKbXoAAAAJ&hl=en")[胡旭明教授] \
_研究方向_：LLM Alignment、Factual Reasoning in LLMs、Knowledge Distillation

*Syntactic Parsing*，_硕士研究生_ #h(1fr) 2022/09 - 2025/06 \
#link("https://scst.suda.edu.cn")[苏州大学计算机科学与技术学院]。 #h(1fr) 导师：#link("https://scholar.google.com/citations?user=faXAgZQAAAAJ&hl=en")[李正华教授] \
_研究方向_：Linguistic Structure Prediction、Text2SQL（维护 #link("https://github.com/SUDA-LA/SeSQL")[SeSQL] 数据集）

== 代表性论文
#chiline()

#link("https://arxiv.org/abs/2509.24244")[*Model Merging Scaling Laws in Large Language Models*] #link("https://github.com/InfiXAI/Merging-Scaling-Law")[[Code]] \
_共同第一作者_ #h(1fr) *ICML* 2026（CCF-A） \
建立 Model Merging Scaling Laws，预测不同 model sizes、expert counts 和 data regimes 下的 model-merging performance。

#link("https://www.preprints.org/frontend/manuscript/412c5de33e20b4c7364a754d6fcab767/download_pub")[*From Parameters to Behaviors: A Survey of Model Fusion for Large Language Models*] \
_共同第一作者_ #h(1fr) *EMNLP* 2026 Findings（CCF-B） \
构建涵盖 parameter-level、prediction-level 与 behavior-level methods 的统一 Model Fusion taxonomy。

#link("https://arxiv.org/pdf/2505.13878")[*InfiFPO: Implicit Model Fusion via Preference Optimization in Large Language Models*] #link("https://github.com/InfiXAI/InfiFPO")[[Code]] \
_第一作者_ #h(1fr) *NeurIPS* 2025 Spotlight（CCF-A） \
提出基于 Preference Optimization 的 sequence-level probability fusion，并在 11 个 benchmarks 上进行验证。

#link("https://arxiv.org/abs/2502.14272")[*Capturing Nuanced Preferences: Preference-Aligned Distillation for Small Language Models*] #link("https://github.com/EganGu/PAD")[[Code]] \
_第一作者_ #h(1fr) *ACL* 2025 Findings（CCF-A） \
将完整的 preference distributions 蒸馏至 small language models，实现更精细的 preference alignment。

#link("https://arxiv.org/abs/2408.12188")[*Reasoning Factual Knowledge in Structured Data with Large Language Models*] #link("https://github.com/EganGu/StructFact")[[Code]] \
_共同第一作者_ #h(1fr) *ACL* 2025 Findings（CCF-A） \
提出 StructFact：包含 13,407 个 queries，用于评测 heterogeneous structured knowledge 上的 reasoning。

== 荣誉与奖励
#chiline()

- *CCL-2023 Chinese AMR Parsing Evaluation Task 第一名。* #link("https://aclanthology.org/2023.ccl-3.5/")[[报告]] #h(1fr) 2023/08 \
- *广东工业大学十大创新人物。* #link("https://www.sohu.com/a/507610953_121124288")[[搜狐新闻]] #h(1fr) 2021/12 \
- *国家励志奖学金。* #link("https://drive.google.com/file/d/1FIV03Zrx7rMji_6WPKmpcm3MVlIy4eE1/view?usp=sharing")[[证明]] #h(1fr) 2021/11 \

== 学术服务
#chiline()

- *审稿人*：ICML、ICLR、NeurIPS、ARR 和 TMLR。
