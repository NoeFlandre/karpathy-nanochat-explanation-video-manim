# NanoChat Manim Video

A 3Blue1Brown-style educational video explaining [Karpathy's nanochat](https://github.com/karpathy/nanochat) repository using [Manim](https://www.manim.community/).

## 🎬 Watch the Video

The full rendered video is available at:
```
NanoChat_Full_Video_1080p.mp4
```

**Duration:** ~4.5 minutes | **Resolution:** 1080p60

## 📖 Scenes

| # | Scene | File | Description |
|---|-------|------|-------------|
| 1 | Introduction | `scene_01_intro.py` | nanochat overview, cost tiers |
| 2 | Architecture | `scene_02_architecture.py` | Repository structure, pipeline |
| 3 | Tokenizer | `scene_03_tokenizer.py` | BPE algorithm, Rust performance |
| 4 | Transformer | `scene_04_transformer.py` | RoPE, GQA, ReLU², attention |
| 5 | Base Training | `scene_05_base_training.py` | Muon optimizer, data pipeline |
| 6 | Midtraining | `scene_06_midtraining.py` | Tool use, conversation format |
| 7 | SFT | `scene_07_sft.py` | Task mixture, loss masking |
| 8 | RL | `scene_08_rl.py` | REINFORCE on GSM8K |
| 9 | Inference | `scene_09_inference.py` | KV cache, sampling |
| 10 | Conclusion | `scene_10_conclusion.py` | Benchmarks, takeaways |

## 🚀 Quick Start

```bash
# Install dependencies
uv sync

# Render a single scene (preview)
cd scenes && uv run manim -pql scene_01_intro.py IntroScene

# Render in high quality (1080p60)
cd scenes && uv run manim -qh scene_01_intro.py IntroScene

# Render all scenes
cd scenes
for i in {01..10}; do uv run manim -qh scene_${i}_*.py; done
```

## 📁 Project Structure

```
├── main.py                 # Combined video entry point
├── scenes/
│   ├── common.py          # Shared utilities & colors
│   └── scene_*.py         # Individual scenes
├── NanoChat_Full_Video_1080p.mp4  # Final rendered video
└── nanochat/              # Cloned nanochat repository
```

## 🛠️ Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- [ffmpeg](https://ffmpeg.org/) (for combining videos)

---

## ✨ Vibe Coded

This entire project was **vibe coded** using **Claude Opus 4.5 Thinking** through [Antigravity](https://antigravity.dev) with a single one-shot prompt:

> *"clone this repo : https://github.com/karpathy/nanochat.git Once done analyze it very thoroughly and once u have a good comprehension of it create an entire video breaking down this repo from end to end in great detail. Your video should be of extreme quality, as qualitative as videos made my 3 blue 1 brown youtube channel. You will use manim to create the video. The final of your entire work is a one full video explaining in great detail the entire repo using manim for that. Go off, think hard, be professional and don't stop until u get the video achieved"*

From prompt to final rendered video in one autonomous session. 🚀

## 📄 License

Educational content. nanochat repository © Andrej Karpathy.
