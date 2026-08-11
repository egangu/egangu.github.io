#show heading: set text(font: "Linux Biolinum")

#show link: underline

// Uncomment the following lines to adjust the size of text.
// The recommended resume text size is from 10pt to 12pt.
// #set text(
//   size: 12pt,
// )

// Feel free to change the margin below to best fit your own CV.
#set page(
  margin: (x: 0.9cm, y: 1.3cm),
)

#set par(justify: true)

#let chiline() = { v(-3pt); line(length: 100%); v(-5pt) }

= Yanggan Gu //(辜仰淦 in Mandarin)

yanggangu\@outlook.com |
#link("https://scholar.google.com/citations?user=cY4ofhcAAAAJ&hl=en&authuser=1")[Google Scholar] | #link("https://egangu.github.io/")[Homepage] |
#link("https://github.com/EganGu")[Github] |

== Education
#chiline()

#link("https://eng.suda.edu.cn/")[*Soochow University*] [_Project 211_], Suzhou, China. #h(1fr) 2022/09 - 2025/06  \
_M.S._ in Computer Science and Technology. #h(1fr) GPA 3.7 (Top-5%) \
// Mathematics for Computer Science (93/100) | Machine Learning (87/100)
// - #lorem(10)

#link("https://english.gdut.edu.cn/")[*Guangdong University of Technology*], Guangzhou, China. #h(1fr) 2018/09 -- 2022/06 \
_B.S._ in Software Engineering. #h(1fr) GPA 4.0 (Top-1%) \
// Advanced Mathematics (98/100) | Discrete Mathematics (96/100) | Linear Algebra (94/100) | Algorithms (94/100)
// - #lorem(10)

== Research Experience
#chiline()

*Model Fusion in LLMs*, _Research Assistant_  #h(1fr) 2025/04 - Now \
#link("https://www.polyu.edu.hk/comp/")[Department of Computing, Hong Kong Polytechnic University]. #h(1fr) Advisor: #link("https://www4.comp.polyu.edu.hk/~hongxyang/")[Prof. Hongxia Yang]\
_Research Topic_: Model Fusion, Alignment of LLMs, Reasoning in LLMs

*Trustworthy LLMs*, _Research Assistant_  #h(1fr) 2024/06 - 2025/03 \
#link("https://www.hkust-gz.edu.cn/academics/hubs-and-thrust-areas/information-hub/artificial-intelligence/")[AI Thrust, The Hong Kong University of Science and Technology (Guangzhou)]. #h(1fr) Advisor: #link("https://scholar.google.com/citations?user=dbBKbXoAAAAJ&hl=en")[Prof. Xuming Hu]\
_Research Topic_: Alignment of LLMs, Factual Reasoning in LLMs, Knowledge Distillation

*Syntactic Parsing*, _Master's Researcher_ #h(1fr) 2022/09 - 2025/06 \
#link("https://scst.suda.edu.cn")[School of Computer Science and Technology, Soochow University]. #h(1fr) Advisor: #link("https://scholar.google.com/citations?user=faXAgZQAAAAJ&hl=en")[Prof. Zhenghua Li]\
_Research Topic_: Linguistic Structure Prediction, Text2SQL (maintaining #link("https://github.com/SUDA-LA/SeSQL")[SeSQL] dataset)

== Main Publications
#chiline()

#link("https://arxiv.org/pdf/2505.13878")[*InfiFPO: Implicit Model Fusion via Preference Optimization in Large Language Models*] #link("https://huggingface.co/collections/InfiX-ai/infifpo-6895615b347999b0b2fd6842")[[Code]], _First Author_. \
*Keywords*: Alignment, Model Fusion, LLMs. #h(1fr) *NeurIPS* 2025 Spotlight (CCF-A) \
*Intro*: This paper introduces InfiFPO, a novel preference optimization method for implicit model fusion of LLMs. Unlike prior fusion approaches that mostly rely on supervised fine-tuning or discard probability information during preference alignment, InfiFPO synthesizes multi-source probabilities at the sequence level to replace the reference model in Direct Preference Optimization. Experiments across 11 benchmarks show that InfiFPO consistently surpasses existing model fusion and preference optimization techniques, boosting the Phi-4 model's average performance from 79.95 to 83.33, with notable improvements in mathematics, coding, and reasoning tasks.

#link("https://arxiv.org/abs/2502.14272")[*Capturing Nuanced Preferences: Preference-Aligned Distillation for Small Language Models*] #link("https://github.com/EganGu/PAD")[[Code]], _First Author_. \
*Keywords*: Alignment, Distillation, Trustworthy LLMs. #h(1fr) *ACL* 2025 Findings (CCF-A) \
*Intro*: This paper introduces the Preference-Aligned Distillation (PAD) framework to improve the alignment of small language models (SLMs) with human preferences by modeling the full preference distribution rather than using simple pairwise comparisons. Through experiments across multiple benchmarks, the proposed PAD approach is shown to outperform existing methods, offering more precise preference signals for better response generation in SLMs.

#link("https://arxiv.org/abs/2408.12188")[*Reasoning Factual Knowledge in Structured Data with Large Language Models*] #link("https://github.com/EganGu/StructFact")[[Code]], _Co-first Author_. \
*Keywords*: Trustworthy LLMs, Benchmark, Structured Facts. #h(1fr) *ACL* 2025 Findings (CCF-A) \
*Intro*: This paper develops a benchmark, called _StructFact_, to evaluate the reasoning abilities of large language models (LLMs) over structured factual knowledge, addressing challenges such as heterogeneity, topological interdependencies, and sparsity in structured data. The benchmark consists of 13,407 factual queries across five tasks and examines how LLMs handle fresh, structured data in real-world applications, offering insights into their limitations and potential improvements for knowledge-sensitive tasks.

// #link("https://aclanthology.org/2024.lrec-main.713/")[*High Order Joint Constituency and Dependency Parsing*] #link("https://github.com/EganGu/high-order-joint-parsing")[[Code]], _First Author_. \
// *Keywords*: Constituency/Dependency Parsing, Lexicalized Modeling. #h(1fr) COLING 2024 (CCF-B) \
// *Intro*: This paper proposes an efficient method for joint constituency and dependency parsing by improving upon existing models through a new decoding algorithm, high-order scoring components, and training phase integration of both tasks. The authors demonstrate that their approach, which includes optimizations for speed and model interaction, significantly outperforms prior methods on multiple languages and datasets.

// #link("https://aclanthology.org/2024.lrec-main.713/")[*System Report for CCL23-Eval Task 2: Autoregressive and Non-autoregressive Chinese AMR Semantic Parsing based on Graph Ensembling*], _First Author_. \
// #lorem(5) #h(1fr) CCL 2023 (Evaluations) \

== Honors and Awards
#chiline()

- *1st place in the CCL-2023 Chinese AMR Parsing Evaluation Task.* #link("https://aclanthology.org/2023.ccl-3.5/")[\[Report\]] #h(1fr) 2023/08 \
- *Top 10 Innovative Figures of Guangdong University of Technology.* #link("https://www.sohu.com/a/507610953_121124288")[[Sohu News]]  #h(1fr) 2021/12 \
- *National Encouragement Scholarship.* #link("https://drive.google.com/file/d/1FIV03Zrx7rMji_6WPKmpcm3MVlIy4eE1/view?usp=sharing")[[Link]] #h(1fr) 2021/11 \
// - *1st Prize at the 9th "China Software Cup" College Student Design Competition.* #link("https://www.cnsoftbei.com/content-1-565-1.html")[[Link]] #h(1fr) 2020/10 \

== Language
#chiline()

- *English*: TOEFL 91/120 (Reading 27/30 | Listening 22/30 | Speaking 22/30 | Writing 20/30)
// - *Programming*: Python (\~5 years), #link("https://pytorch.org/")[Pytorch] (\~4 years), #link("https://huggingface.co/docs/transformers/index")[Transformers] (\~ 3 years).
