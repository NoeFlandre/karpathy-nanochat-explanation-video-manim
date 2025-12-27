"""
Scene 2: Architecture Overview
High-level view of the nanochat architecture and training pipeline.
"""

from manim import *
try:
    from .common import *
except ImportError:
    from common import *


class ArchitectureScene(Scene):
    """Architecture overview showing the full training pipeline."""
    
    def construct(self):
        configure_scene(self)
        
        # Part 1: File structure
        self.play_file_structure()
        
        # Part 2: Training pipeline deep dive
        self.play_training_pipeline()
        
        # Part 3: Model architecture teaser
        self.play_model_architecture_teaser()
    
    def play_file_structure(self):
        """Show the repository file structure."""
        
        title = Text("Repository Structure", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # File tree representation
        tree_data = [
            ("nanochat/", 0, BLUE_PRIMARY),
            ("  gpt.py", 1, TEXT_WHITE),
            ("  tokenizer.py", 1, TEXT_WHITE),
            ("  engine.py", 1, TEXT_WHITE),
            ("  muon.py", 1, TEXT_WHITE),
            ("  dataloader.py", 1, TEXT_WHITE),
            ("scripts/", 0, PURPLE_PRIMARY),
            ("  base_train.py", 1, TEXT_WHITE),
            ("  chat_sft.py", 1, TEXT_WHITE),
            ("  chat_rl.py", 1, TEXT_WHITE),
            ("rustbpe/", 0, ORANGE_ACCENT),
            ("  lib.rs", 1, TEXT_WHITE),
            ("tasks/", 0, GREEN_ACCENT),
            ("speedrun.sh", 0, PINK_ACCENT),
        ]
        
        tree_group = VGroup()
        
        for text, indent, color in tree_data:
            line = Text(text, font_size=24, color=color)
            if len(tree_group) == 0:
                line.move_to(UP * 2 + LEFT * 4)
            else:
                line.next_to(tree_group[-1], DOWN, buff=0.15, aligned_edge=LEFT)
            tree_group.add(line)
        
        tree_group.move_to(LEFT * 3)
        
        # Description boxes on the right
        descriptions = VGroup()
        
        desc_items = [
            ("Core Model", "GPT architecture with RoPE,\nGQA, and ReLU² MLP", BLUE_PRIMARY),
            ("Optimizers", "Muon (Newton-Schulz)\n+ AdamW", PURPLE_PRIMARY),
            ("Tokenizer", "Rust BPE for speed,\ntiktoken for inference", ORANGE_ACCENT),
            ("Training", "Base → Mid → SFT → RL\nFull pipeline", GREEN_ACCENT),
        ]
        
        for i, (name, desc, color) in enumerate(desc_items):
            box = RoundedRectangle(
                corner_radius=0.1,
                width=3.5,
                height=1.0,
                fill_color=color,
                fill_opacity=0.2,
                stroke_color=color,
                stroke_width=2
            )
            
            name_text = Text(name, font_size=22, color=color, weight=BOLD)
            desc_text = Text(desc, font_size=16, color=TEXT_GRAY)
            
            name_text.move_to(box.get_top() + DOWN * 0.25)
            desc_text.next_to(name_text, DOWN, buff=0.1)
            
            group = VGroup(box, name_text, desc_text)
            group.move_to(RIGHT * 3 + DOWN * (i - 1.5) * 1.3)
            descriptions.add(group)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        # Animate tree line by line
        for line in tree_group[:6]:
            self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.15)
        
        self.play(FadeIn(descriptions[0]), run_time=0.3)
        
        for line in tree_group[6:10]:
            self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.15)
        
        self.play(FadeIn(descriptions[1]), run_time=0.3)
        
        for line in tree_group[10:12]:
            self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.15)
        
        self.play(FadeIn(descriptions[2]), run_time=0.3)
        
        for line in tree_group[12:]:
            self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.15)
        
        self.play(FadeIn(descriptions[3]), run_time=0.3)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(tree_group),
            FadeOut(descriptions),
            run_time=1
        )
    
    def play_training_pipeline(self):
        """Detailed training pipeline visualization."""
        
        title = Text("Training Pipeline", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Create detailed pipeline
        stages = [
            ("Raw Text\n(FineWeb)", TEXT_GRAY, "~50B chars"),
            ("Tokenizer\n(BPE)", BLUE_PRIMARY, "65K vocab"),
            ("Base Model\n(Pretraining)", PURPLE_PRIMARY, "20:1 ratio"),
            ("Midtraining\n(Conversations)", GREEN_ACCENT, "+tool use"),
            ("SFT\n(Supervised)", ORANGE_ACCENT, "~23K rows"),
            ("RL\n(REINFORCE)", RED_ACCENT, "GSM8K"),
        ]
        
        boxes = VGroup()
        info_labels = VGroup()
        arrows = VGroup()
        
        # Two rows layout
        row1_indices = [0, 1, 2]
        row2_indices = [3, 4, 5]
        
        for i, (name, color, info) in enumerate(stages):
            box = RoundedRectangle(
                corner_radius=0.15,
                width=2.5,
                height=1.3,
                fill_color=color,
                fill_opacity=0.25,
                stroke_color=color,
                stroke_width=3
            )
            
            label = Text(name, font_size=22, color=TEXT_WHITE)
            label.move_to(box.get_center())
            
            info_text = Text(info, font_size=16, color=color)
            info_text.next_to(box, DOWN, buff=0.1)
            
            group = VGroup(box, label)
            
            if i in row1_indices:
                group.move_to(UP * 1.2 + RIGHT * (i - 1) * 3)
            else:
                group.move_to(DOWN * 1.5 + RIGHT * (i - 4) * 3)
            
            info_text.next_to(group, DOWN, buff=0.15)
            
            boxes.add(group)
            info_labels.add(info_text)
        
        # Arrows
        for i in range(len(stages) - 1):
            if i == 2:  # Connect row 1 to row 2
                start = boxes[2].get_right() + RIGHT * 0.5
                mid = start + DOWN * 1.3
                end = boxes[3].get_left() + LEFT * 0.5
                
                arrow_path = VGroup(
                    Arrow(boxes[2].get_right(), mid, color=TEXT_DIM, buff=0.1, stroke_width=2),
                    Arrow(mid, boxes[3].get_left(), color=TEXT_DIM, buff=0.1, stroke_width=2)
                )
                arrows.add(arrow_path)
            else:
                if i < 2:
                    arrow = Arrow(boxes[i].get_right(), boxes[i+1].get_left(), 
                                color=TEXT_DIM, buff=0.1, stroke_width=2)
                else:
                    arrow = Arrow(boxes[i].get_right(), boxes[i+1].get_left(), 
                                color=TEXT_DIM, buff=0.1, stroke_width=2)
                arrows.add(arrow)
        
        # Time labels
        time_label = Text("~4 hours on 8×H100 ($100 tier)", font_size=24, color=TEXT_GRAY)
        time_label.to_edge(DOWN, buff=0.8)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        for i, (box, info) in enumerate(zip(boxes, info_labels)):
            anims = [FadeIn(box, scale=0.8), FadeIn(info)]
            if i > 0 and i != 3:
                if i == 3:
                    anims.append(Create(arrows[2]))
                else:
                    anims.append(GrowArrow(arrows[i-1 if i < 3 else i-1]))
            elif i == 3:
                anims.append(Create(arrows[2]))
            self.play(*anims, run_time=0.4)
        
        self.play(FadeIn(time_label), run_time=0.5)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(boxes),
            FadeOut(arrows),
            FadeOut(info_labels),
            FadeOut(time_label),
            run_time=1
        )
    
    def play_model_architecture_teaser(self):
        """Preview of the transformer architecture."""
        
        title = Text("Model Architecture Preview", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Key architecture features
        features = [
            ("Rotary Embeddings", "Relative position encoding via rotation", BLUE_PRIMARY),
            ("QK Normalization", "Stable attention with RMSNorm", PURPLE_PRIMARY),
            ("ReLU² MLP", "Squared ReLU activation", GREEN_ACCENT),
            ("Group Query Attention", "Efficient KV sharing", ORANGE_ACCENT),
            ("Untied Embeddings", "Separate input/output matrices", PINK_ACCENT),
        ]
        
        feature_group = VGroup()
        
        for i, (name, desc, color) in enumerate(features):
            # Icon circle
            icon = Circle(radius=0.3, color=color, fill_opacity=0.3, stroke_width=2)
            
            # Name
            name_text = Text(name, font_size=28, color=color, weight=BOLD)
            name_text.next_to(icon, RIGHT, buff=0.3)
            
            # Description
            desc_text = Text(desc, font_size=20, color=TEXT_GRAY)
            desc_text.next_to(name_text, DOWN, buff=0.1, aligned_edge=LEFT)
            
            row = VGroup(icon, name_text, desc_text)
            row.move_to(DOWN * (i - 2) * 0.9)
            feature_group.add(row)
        
        feature_group.move_to(ORIGIN)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        for feature in feature_group:
            self.play(
                GrowFromCenter(feature[0]),
                FadeIn(feature[1], shift=RIGHT * 0.2),
                FadeIn(feature[2], shift=RIGHT * 0.2),
                run_time=0.4
            )
        
        self.wait(2)
        
        # Teaser text
        teaser = Text("Let's explore each component in detail...", 
                     font_size=32, color=TEXT_GRAY)
        teaser.to_edge(DOWN, buff=0.8)
        
        self.play(FadeIn(teaser, shift=UP * 0.2), run_time=0.5)
        self.wait(1)
        
        # Final transition
        self.play(
            FadeOut(title),
            FadeOut(feature_group),
            FadeOut(teaser),
            run_time=1
        )
