"""
Scene 5: Base Training
Pretraining with Muon optimizer, distributed training, data loading.
"""

from manim import *
try:
    from .common import *
except ImportError:
    from common import *
import numpy as np


class BaseTrainingScene(Scene):
    """Base model pretraining visualization."""
    
    def construct(self):
        configure_scene(self)
        
        # Part 1: Data pipeline
        self.play_data_pipeline()
        
        # Part 2: Muon optimizer
        self.play_muon_optimizer()
        
        # Part 3: Training loop
        self.play_training_loop()
        
        # Part 4: Learning rate schedule
        self.play_lr_schedule()
    
    def play_data_pipeline(self):
        """Show data loading from FineWeb."""
        
        title = Text("Data Pipeline", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # FineWeb source
        fineweb = RoundedRectangle(
            corner_radius=0.15, width=3, height=1.2,
            fill_color=BLUE_PRIMARY, fill_opacity=0.3,
            stroke_color=BLUE_PRIMARY, stroke_width=2
        )
        fineweb_label = Text("FineWeb\n(HuggingFace)", font_size=22, color=TEXT_WHITE)
        fineweb_label.move_to(fineweb.get_center())
        fineweb_group = VGroup(fineweb, fineweb_label)
        fineweb_group.move_to(LEFT * 4 + UP * 1)
        
        # Shards
        shards = VGroup()
        shard_labels = ["Shard 1", "Shard 2", "...", "Shard 240"]
        
        for i, label in enumerate(shard_labels):
            shard = RoundedRectangle(
                corner_radius=0.1, width=1.5, height=0.6,
                fill_color=PURPLE_PRIMARY, fill_opacity=0.3,
                stroke_color=PURPLE_PRIMARY, stroke_width=2
            )
            shard_text = Text(label, font_size=16, color=TEXT_WHITE)
            shard_text.move_to(shard.get_center())
            shard_group = VGroup(shard, shard_text)
            shard_group.move_to(LEFT * 1.5 + UP * (1.5 - i * 0.8))
            shards.add(shard_group)
        
        # Info
        shard_info = Text("~250M chars/shard\n~24GB total", font_size=18, color=TEXT_GRAY)
        shard_info.next_to(shards, DOWN, buff=0.3)
        
        # Distributed loading
        gpus = VGroup()
        
        for i in range(4):
            gpu = RoundedRectangle(
                corner_radius=0.1, width=1.2, height=0.8,
                fill_color=GREEN_ACCENT, fill_opacity=0.3,
                stroke_color=GREEN_ACCENT, stroke_width=2
            )
            gpu_label = Text(f"GPU {i}", font_size=16, color=TEXT_WHITE)
            gpu_label.move_to(gpu.get_center())
            gpu_group = VGroup(gpu, gpu_label)
            gpu_group.move_to(RIGHT * (1.5 + i * 1.4) + UP * 1)
            gpus.add(gpu_group)
        
        # More GPUs indicator
        more_gpus = Text("+ 4 more\n(8 total)", font_size=18, color=TEXT_GRAY)
        more_gpus.next_to(gpus, DOWN, buff=0.3)
        
        # Tokenizer
        tokenizer = RoundedRectangle(
            corner_radius=0.1, width=2, height=0.8,
            fill_color=ORANGE_ACCENT, fill_opacity=0.3,
            stroke_color=ORANGE_ACCENT, stroke_width=2
        )
        tokenizer_label = Text("Tokenizer", font_size=20, color=TEXT_WHITE)
        tokenizer_label.move_to(tokenizer.get_center())
        tokenizer_group = VGroup(tokenizer, tokenizer_label)
        tokenizer_group.move_to(DOWN * 1.5)
        
        # Model
        model = RoundedRectangle(
            corner_radius=0.1, width=2.5, height=1,
            fill_color=PINK_ACCENT, fill_opacity=0.3,
            stroke_color=PINK_ACCENT, stroke_width=2
        )
        model_label = Text("GPT Model", font_size=22, color=TEXT_WHITE)
        model_label.move_to(model.get_center())
        model_group = VGroup(model, model_label)
        model_group.move_to(DOWN * 3)
        
        # Arrows
        arrows = VGroup(
            Arrow(fineweb_group.get_right(), shards[0].get_left(), color=TEXT_DIM, buff=0.1, stroke_width=2),
            Arrow(shards.get_right(), gpus[0].get_left(), color=TEXT_DIM, buff=0.1, stroke_width=2),
            Arrow(gpus.get_bottom() + DOWN * 0.5, tokenizer_group.get_top(), color=TEXT_DIM, buff=0.1, stroke_width=2),
            Arrow(tokenizer_group.get_bottom(), model_group.get_top(), color=TEXT_DIM, buff=0.1, stroke_width=2),
        )
        
        # Stats
        stats = Text(
            "~11B tokens for d20 model (Chinchilla 20:1 ratio)",
            font_size=22,
            color=TEXT_GRAY
        )
        stats.to_edge(DOWN, buff=0.5)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        self.play(FadeIn(fineweb_group), run_time=0.4)
        self.play(GrowArrow(arrows[0]), run_time=0.3)
        
        for shard in shards:
            self.play(FadeIn(shard, scale=0.8), run_time=0.15)
        
        self.play(FadeIn(shard_info), run_time=0.3)
        self.play(GrowArrow(arrows[1]), run_time=0.3)
        
        for gpu in gpus:
            self.play(FadeIn(gpu, scale=0.9), run_time=0.15)
        
        self.play(FadeIn(more_gpus), run_time=0.3)
        self.play(GrowArrow(arrows[2]), FadeIn(tokenizer_group), run_time=0.4)
        self.play(GrowArrow(arrows[3]), FadeIn(model_group), run_time=0.4)
        self.play(FadeIn(stats), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(fineweb_group),
            FadeOut(shards),
            FadeOut(shard_info),
            FadeOut(gpus),
            FadeOut(more_gpus),
            FadeOut(tokenizer_group),
            FadeOut(model_group),
            FadeOut(arrows),
            FadeOut(stats),
            run_time=1
        )
    
    def play_muon_optimizer(self):
        """Visualize the Muon optimizer with Newton-Schulz."""
        
        title = Text("Muon Optimizer", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        subtitle = Text(
            "MomentUm Orthogonalized by Newton-schulz",
            font_size=24,
            color=TEXT_GRAY
        )
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Key idea
        key_idea = Text(
            "Orthogonalize weight updates for better optimization",
            font_size=26,
            color=TEXT_WHITE
        )
        key_idea.move_to(UP * 1)
        
        # Steps
        steps = [
            ("1. SGD-Momentum", "Compute momentum-smoothed gradient"),
            ("2. Newton-Schulz", "Orthogonalize via 5 iterations"),
            ("3. Scale & Apply", "Aspect-ratio aware update"),
        ]
        
        step_group = VGroup()
        
        for i, (step_name, desc) in enumerate(steps):
            step_box = RoundedRectangle(
                corner_radius=0.1, width=3.5, height=0.9,
                fill_color=BLUE_PRIMARY if i == 0 else (PURPLE_PRIMARY if i == 1 else GREEN_ACCENT),
                fill_opacity=0.3,
                stroke_color=BLUE_PRIMARY if i == 0 else (PURPLE_PRIMARY if i == 1 else GREEN_ACCENT),
                stroke_width=2
            )
            
            name = Text(step_name, font_size=22, color=TEXT_WHITE, weight=BOLD)
            description = Text(desc, font_size=16, color=TEXT_GRAY)
            
            name.move_to(step_box.get_center() + UP * 0.15)
            description.move_to(step_box.get_center() + DOWN * 0.2)
            
            group = VGroup(step_box, name, description)
            group.move_to(DOWN * (i - 0.5) * 1.2)
            step_group.add(group)
        
        step_group.move_to(LEFT * 2 + DOWN * 0.5)
        
        # Newton-Schulz formula
        formula_title = Text("Newton-Schulz Iteration:", font_size=22, color=PURPLE_PRIMARY)
        formula_title.move_to(RIGHT * 2.5 + UP * 0.5)
        
        formula = MathTex(
            r"X \leftarrow aX + bXX^TX + cXX^TXX^TX",
            font_size=24,
            color=TEXT_WHITE
        )
        formula.next_to(formula_title, DOWN, buff=0.3)
        
        coeffs = Text("a=3.4445, b=-4.7750, c=2.0315", font_size=18, color=TEXT_GRAY)
        coeffs.next_to(formula, DOWN, buff=0.2)
        
        result = Text(
            "Result ≈ orthogonal matrix: U·S'·V^T",
            font_size=20,
            color=GREEN_ACCENT
        )
        result.next_to(coeffs, DOWN, buff=0.4)
        
        # Why Muon?
        why_text = Text(
            "Faster convergence for matrix weights (vs AdamW)",
            font_size=22,
            color=ORANGE_ACCENT
        )
        why_text.to_edge(DOWN, buff=0.8)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(subtitle), run_time=0.4)
        self.play(FadeIn(key_idea), run_time=0.5)
        
        for step in step_group:
            self.play(FadeIn(step, shift=RIGHT * 0.2), run_time=0.3)
        
        self.play(FadeIn(formula_title), run_time=0.3)
        self.play(FadeIn(formula), run_time=0.4)
        self.play(FadeIn(coeffs), run_time=0.3)
        self.play(FadeIn(result), run_time=0.3)
        self.play(FadeIn(why_text), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(key_idea),
            FadeOut(step_group),
            FadeOut(formula_title),
            FadeOut(formula),
            FadeOut(coeffs),
            FadeOut(result),
            FadeOut(why_text),
            run_time=1
        )
    
    def play_training_loop(self):
        """Visualize the training loop."""
        
        title = Text("Training Loop", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Loop steps
        loop_steps = [
            ("Forward Pass", "Compute predictions", BLUE_PRIMARY),
            ("Loss Calculation", "Cross-entropy loss", PURPLE_PRIMARY),
            ("Backward Pass", "Compute gradients", GREEN_ACCENT),
            ("Optimizer Step", "Update weights", ORANGE_ACCENT),
        ]
        
        step_boxes = VGroup()
        arrows = VGroup()
        
        for i, (name, desc, color) in enumerate(loop_steps):
            box = RoundedRectangle(
                corner_radius=0.15, width=2.8, height=1,
                fill_color=color, fill_opacity=0.3,
                stroke_color=color, stroke_width=2
            )
            
            name_text = Text(name, font_size=22, color=TEXT_WHITE, weight=BOLD)
            desc_text = Text(desc, font_size=16, color=TEXT_GRAY)
            
            name_text.move_to(box.get_center() + UP * 0.15)
            desc_text.move_to(box.get_center() + DOWN * 0.2)
            
            group = VGroup(box, name_text, desc_text)
            
            # Arrange in a circle-ish pattern
            angle = -i * TAU / 4 + TAU / 8
            pos = np.array([np.cos(angle) * 2.5, np.sin(angle) * 1.5, 0])
            group.move_to(pos)
            step_boxes.add(group)
        
        # Arrows between steps
        for i in range(len(step_boxes)):
            next_i = (i + 1) % len(step_boxes)
            arrow = Arrow(
                step_boxes[i].get_edge_center(
                    RIGHT if i == 0 else (DOWN if i == 1 else (LEFT if i == 2 else UP))
                ),
                step_boxes[next_i].get_edge_center(
                    UP if i == 0 else (LEFT if i == 1 else (UP if i == 2 else RIGHT))
                ),
                color=TEXT_DIM,
                buff=0.15,
                stroke_width=2
            )
            arrows.add(arrow)
        
        # Create simpler arrows
        simple_arrows = VGroup(
            Arrow(step_boxes[0].get_bottom(), step_boxes[1].get_top(), color=TEXT_DIM, buff=0.1, stroke_width=2),
            Arrow(step_boxes[1].get_left(), step_boxes[2].get_right(), color=TEXT_DIM, buff=0.1, stroke_width=2),
            Arrow(step_boxes[2].get_top(), step_boxes[3].get_bottom(), color=TEXT_DIM, buff=0.1, stroke_width=2),
            CurvedArrow(step_boxes[3].get_right(), step_boxes[0].get_right(), angle=-TAU/4, color=TEXT_DIM, stroke_width=2),
        )
        
        # Rearrange boxes linearly
        for i, box in enumerate(step_boxes):
            box.move_to(LEFT * 3 + RIGHT * i * 3 + UP * 0.5)
        
        simple_arrows = VGroup()
        for i in range(len(step_boxes) - 1):
            arrow = Arrow(step_boxes[i].get_right(), step_boxes[i+1].get_left(), color=TEXT_DIM, buff=0.1, stroke_width=2)
            simple_arrows.add(arrow)
        
        # Loop back arrow
        loop_arrow = CurvedArrow(
            step_boxes[-1].get_bottom() + DOWN * 0.2,
            step_boxes[0].get_bottom() + DOWN * 0.2,
            angle=TAU/4,
            color=CYAN_ACCENT,
            stroke_width=2
        )
        loop_label = Text("repeat", font_size=18, color=CYAN_ACCENT)
        loop_label.next_to(loop_arrow, DOWN, buff=0.1)
        
        # Stats
        stats = VGroup(
            Text("Batch size: 524,288 tokens", font_size=20, color=TEXT_GRAY),
            Text("Gradient accumulation: auto-computed", font_size=20, color=TEXT_GRAY),
            Text("MFU: ~50% on 8×H100", font_size=20, color=TEXT_GRAY),
        )
        stats.arrange(DOWN, buff=0.2)
        stats.to_edge(DOWN, buff=0.8)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        for i, (box, arrow) in enumerate(zip(step_boxes, simple_arrows)):
            self.play(FadeIn(box, scale=0.9), run_time=0.25)
            self.play(GrowArrow(arrow), run_time=0.2)
        
        self.play(FadeIn(step_boxes[-1], scale=0.9), run_time=0.25)
        self.play(Create(loop_arrow), FadeIn(loop_label), run_time=0.5)
        
        for stat in stats:
            self.play(FadeIn(stat, shift=RIGHT * 0.2), run_time=0.2)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(step_boxes),
            FadeOut(simple_arrows),
            FadeOut(loop_arrow),
            FadeOut(loop_label),
            FadeOut(stats),
            run_time=1
        )
    
    def play_lr_schedule(self):
        """Show the learning rate schedule."""
        
        title = Text("Learning Rate Schedule", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Create axes
        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 1.2, 0.2],
            x_length=8,
            y_length=4,
            axis_config={"color": TEXT_DIM, "include_tip": False},
            x_axis_config={"numbers_to_include": [0, 0.2, 0.8, 1.0]},
            y_axis_config={"numbers_to_include": [0, 0.5, 1.0]},
        )
        axes.move_to(DOWN * 0.5)
        
        x_label = Text("Training Progress", font_size=18, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)
        
        y_label = Text("LR Multiplier", font_size=18, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.3).rotate(90 * DEGREES)
        
        # LR curve with warmup and warmdown
        warmup_ratio = 0.0
        warmdown_ratio = 0.2
        
        def lr_func(x):
            if x < warmup_ratio:
                return x / warmup_ratio if warmup_ratio > 0 else 1.0
            elif x > 1 - warmdown_ratio:
                progress = (1 - x) / warmdown_ratio
                return progress
            else:
                return 1.0
        
        lr_curve = axes.plot(
            lr_func,
            x_range=[0, 1, 0.01],
            color=CYAN_ACCENT,
            stroke_width=3
        )
        
        # Annotations
        warmdown_region = axes.get_area(
            lr_curve,
            x_range=[0.8, 1.0],
            color=ORANGE_ACCENT,
            opacity=0.3
        )
        
        warmdown_label = Text("Warmdown\n(20%)", font_size=18, color=ORANGE_ACCENT)
        warmdown_label.move_to(axes.c2p(0.9, 0.7))
        
        # Stats
        stats = VGroup(
            Text("warmup_ratio = 0.0 (no warmup)", font_size=20, color=TEXT_GRAY),
            Text("warmdown_ratio = 0.2 (linear decay)", font_size=20, color=TEXT_GRAY),
            Text("final_lr_frac = 0.0 (decay to zero)", font_size=20, color=TEXT_GRAY),
        )
        stats.arrange(DOWN, buff=0.15)
        stats.to_edge(DOWN, buff=0.6)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(Create(axes), run_time=0.5)
        self.play(FadeIn(x_label), FadeIn(y_label), run_time=0.3)
        self.play(Create(lr_curve), run_time=1)
        self.play(FadeIn(warmdown_region), FadeIn(warmdown_label), run_time=0.5)
        
        for stat in stats:
            self.play(FadeIn(stat), run_time=0.2)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(lr_curve),
            FadeOut(warmdown_region),
            FadeOut(warmdown_label),
            FadeOut(stats),
            run_time=1
        )
