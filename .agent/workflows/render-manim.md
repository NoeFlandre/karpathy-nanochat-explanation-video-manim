---
description: Render NanoChat Manim video scenes
---

This workflow renders the NanoChat educational video scenes. The scenes can be rendered individually or as a complete video.

## Quick Start

### 1. Render Individual Scene (Low Quality Preview)
// turbo
```bash
cd scenes && uv run manim -ql scene_01_intro.py IntroScene
```

### 2. Render Scene in High Quality
```bash
cd scenes && uv run manim -qh scene_01_intro.py IntroScene
```

### 3. Render All Scenes (Low Quality)
```bash
cd scenes
for i in {01..10}; do 
  uv run manim -ql scene_${i}_*.py 
done
```

## Available Scenes

| Scene | File | Class | Description |
|-------|------|-------|-------------|
| 1 | `scene_01_intro.py` | `IntroScene` | Introduction to nanochat |
| 2 | `scene_02_architecture.py` | `ArchitectureScene` | Architecture overview |
| 3 | `scene_03_tokenizer.py` | `TokenizerScene` | BPE tokenizer deep dive |
| 4 | `scene_04_transformer.py` | `TransformerScene` | Transformer architecture |
| 5 | `scene_05_base_training.py` | `BaseTrainingScene` | Base training with Muon |
| 6 | `scene_06_midtraining.py` | `MidtrainingScene` | Midtraining and tool use |
| 7 | `scene_07_sft.py` | `SFTScene` | Supervised fine-tuning |
| 8 | `scene_08_rl.py` | `RLScene` | Reinforcement learning |
| 9 | `scene_09_inference.py` | `InferenceScene` | Inference engine |
| 10 | `scene_10_conclusion.py` | `ConclusionScene` | Conclusion and benchmarks |

## Quality Options

- `-ql` / `--quality l` - Low quality (480p15), fast preview
- `-qm` / `--quality m` - Medium quality (720p30)
- `-qh` / `--quality h` - High quality (1080p60)
- `-qk` / `--quality k` - 4K quality (4K60)

## Output Location

Videos are saved to `media/videos/<scene_file>/<quality>/`

## Tips

- Use low quality for iterating on animations
- Each scene takes ~1-3 minutes to render in low quality
- High quality rendering takes significantly longer
- Add `-p` to automatically preview after rendering
