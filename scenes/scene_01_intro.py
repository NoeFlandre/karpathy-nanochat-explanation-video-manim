"""
Scene 1: Introduction
Introduces nanochat - the $100 ChatGPT clone
"""

from manim import *
try:
    from .common import *
except ImportError:
    from common import *


class IntroScene(Scene):
    """Introduction scene with title, overview, and cost visualization."""
    
    def construct(self):
        configure_scene(self)
        
        # Part 1: Title Animation
        self.play_title_sequence()
        
        # Part 2: What is nanochat?
        self.play_overview()
        
        # Part 3: Cost visualization
        self.play_cost_breakdown()
        
        # Part 4: Pipeline preview
        self.play_pipeline_preview()
    
    def play_title_sequence(self):
        """Animated title with neural network background."""
        
        # Create subtle grid background
        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": TEXT_DIM,
                "stroke_width": 0.5,
                "stroke_opacity": 0.3
            },
            axis_config={"stroke_opacity": 0}
        )
        
        # Main title
        title = Text("nanochat", font_size=96, color=TEXT_WHITE, weight=BOLD)
        title.set_color_by_gradient(BLUE_PRIMARY, PURPLE_PRIMARY)
        
        # Subtitle with typing effect
        subtitle = Text(
            '"The best ChatGPT that $100 can buy"',
            font_size=36,
            color=TEXT_GRAY,
            slant=ITALIC
        )
        subtitle.next_to(title, DOWN, buff=0.5)
        
        # Author credit
        author = Text("by Andrej Karpathy", font_size=28, color=TEXT_DIM)
        author.next_to(subtitle, DOWN, buff=0.3)
        
        # Animate
        self.play(FadeIn(grid, run_time=1))
        self.play(
            Write(title, run_time=2),
            rate_func=smooth
        )
        self.wait(0.5)
        
        self.play(
            FadeIn(subtitle, shift=UP * 0.3),
            run_time=1
        )
        self.play(FadeIn(author), run_time=0.5)
        
        self.wait(2)
        
        # Transition out
        self.play(
            FadeOut(grid),
            title.animate.scale(0.5).to_corner(UL),
            FadeOut(subtitle),
            FadeOut(author),
            run_time=1.5
        )
        self.wait(0.5)
    
    def play_overview(self):
        """What is nanochat? Overview section."""
        
        # Section title
        section_title = Text("What is nanochat?", font_size=56, color=CYAN_ACCENT)
        section_title.to_edge(UP, buff=0.8)
        
        # Key points
        points = [
            "✓ Full-stack LLM implementation",
            "✓ Single 8×H100 node training",
            "✓ Tokenization → Pretraining → Finetuning → Inference",
            "✓ Clean, minimal, hackable codebase",
            "✓ ~8,000 lines of code in 45 files",
        ]
        
        point_mobjects = VGroup()
        for i, point in enumerate(points):
            text = Text(point, font_size=32, color=TEXT_WHITE)
            text.align_to(LEFT * 4, LEFT)
            if i == 0:
                text.next_to(section_title, DOWN, buff=0.8)
            else:
                text.next_to(point_mobjects[-1], DOWN, buff=0.4, aligned_edge=LEFT)
            point_mobjects.add(text)
        
        # Animate
        self.play(Write(section_title), run_time=1)
        
        for point in point_mobjects:
            self.play(FadeIn(point, shift=RIGHT * 0.3), run_time=0.5)
            self.wait(0.3)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(section_title),
            FadeOut(point_mobjects),
            run_time=1
        )
    
    def play_cost_breakdown(self):
        """Visualize the cost tiers."""
        
        section_title = Text("Training Costs", font_size=56, color=CYAN_ACCENT)
        section_title.to_edge(UP, buff=0.8)
        
        # Cost tiers as bars
        tiers = [
            ("$100", "d20", "4 hours", "561M params", BLUE_PRIMARY),
            ("$300", "d26", "12 hours", "~1B params", PURPLE_PRIMARY),
            ("$800", "d32", "33 hours", "1.9B params", PINK_ACCENT),
        ]
        
        bars = VGroup()
        labels = VGroup()
        
        for i, (cost, model, time, params, color) in enumerate(tiers):
            # Bar
            bar_width = 2 + i * 1.5
            bar = RoundedRectangle(
                corner_radius=0.1,
                width=bar_width,
                height=0.8,
                fill_color=color,
                fill_opacity=0.6,
                stroke_color=color,
                stroke_width=2
            )
            bar.move_to(DOWN * (i - 1) * 1.2)
            bars.add(bar)
            
            # Labels
            cost_label = Text(cost, font_size=36, color=TEXT_WHITE, weight=BOLD)
            cost_label.move_to(bar.get_center())
            
            info_label = Text(
                f"{model} • {time} • {params}",
                font_size=20,
                color=TEXT_GRAY
            )
            info_label.next_to(bar, RIGHT, buff=0.3)
            
            labels.add(VGroup(cost_label, info_label))
        
        # Center everything
        all_bars = VGroup(bars, labels)
        all_bars.move_to(ORIGIN)
        
        # Animate
        self.play(Write(section_title), run_time=1)
        
        for bar, label_group in zip(bars, labels):
            self.play(
                GrowFromCenter(bar),
                run_time=0.5
            )
            self.play(
                FadeIn(label_group[0]),
                FadeIn(label_group[1], shift=RIGHT * 0.2),
                run_time=0.4
            )
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(section_title),
            FadeOut(all_bars),
            run_time=1
        )
    
    def play_pipeline_preview(self):
        """Quick preview of the training pipeline stages."""
        
        section_title = Text("The Training Pipeline", font_size=56, color=CYAN_ACCENT)
        section_title.to_edge(UP, buff=0.8)
        
        # Pipeline stages
        stages = [
            ("Tokenizer", BLUE_PRIMARY),
            ("Base\nTraining", PURPLE_PRIMARY),
            ("Mid-\ntraining", GREEN_ACCENT),
            ("SFT", ORANGE_ACCENT),
            ("RL", RED_ACCENT),
            ("ChatGPT!", PINK_ACCENT),
        ]
        
        boxes = VGroup()
        arrows = VGroup()
        
        for i, (name, color) in enumerate(stages):
            box = PipelineBox(name, color=color, width=1.8, height=1.0)
            box.shift(RIGHT * (i - 2.5) * 2.2)
            boxes.add(box)
            
            if i > 0:
                arrow = Arrow(
                    start=boxes[i-1].get_right(),
                    end=box.get_left(),
                    color=TEXT_DIM,
                    buff=0.1,
                    stroke_width=2
                )
                arrows.add(arrow)
        
        # Center and scale
        pipeline = VGroup(boxes, arrows)
        pipeline.scale(0.85)
        pipeline.move_to(ORIGIN)
        
        # Animate
        self.play(Write(section_title), run_time=1)
        
        for i, box in enumerate(boxes):
            anims = [GrowFromCenter(box)]
            if i > 0:
                anims.append(GrowArrow(arrows[i-1]))
            self.play(*anims, run_time=0.4)
        
        # Highlight flow
        highlight = SurroundingRectangle(
            boxes[0],
            color=CYAN_ACCENT,
            buff=0.1
        )
        
        self.play(Create(highlight), run_time=0.3)
        
        for i in range(1, len(boxes)):
            new_highlight = SurroundingRectangle(
                boxes[i],
                color=CYAN_ACCENT,
                buff=0.1
            )
            self.play(Transform(highlight, new_highlight), run_time=0.3)
        
        self.play(FadeOut(highlight), run_time=0.3)
        
        # Next video teaser
        teaser = Text(
            "Let's dive into each stage...",
            font_size=36,
            color=TEXT_GRAY
        )
        teaser.to_edge(DOWN, buff=1)
        
        self.play(FadeIn(teaser, shift=UP * 0.3), run_time=0.5)
        self.wait(2)
        
        # Final transition
        self.play(
            FadeOut(section_title),
            FadeOut(pipeline),
            FadeOut(teaser),
            run_time=1
        )
