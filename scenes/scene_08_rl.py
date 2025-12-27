"""
Scene 8: Reinforcement Learning
REINFORCE on GSM8K for improved math reasoning.
"""

from manim import *
try:
    from .common import *
except ImportError:
    from common import *
import numpy as np


class RLScene(Scene):
    """Reinforcement Learning visualization."""
    
    def construct(self):
        configure_scene(self)
        
        # Part 1: RL motivation
        self.play_rl_motivation()
        
        # Part 2: REINFORCE algorithm
        self.play_reinforce()
        
        # Part 3: GSM8K example
        self.play_gsm8k_example()
        
        # Part 4: Results
        self.play_rl_results()
    
    def play_rl_motivation(self):
        """Why use RL?"""
        
        title = Text("Reinforcement Learning", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Motivation
        motivation = Text(
            "Improve specific capabilities through trial and reward",
            font_size=26,
            color=TEXT_WHITE
        )
        motivation.next_to(title, DOWN, buff=0.5)
        
        # SFT vs RL comparison
        sft_box = RoundedRectangle(
            corner_radius=0.15, width=4.5, height=2.5,
            fill_color=ORANGE_ACCENT, fill_opacity=0.2,
            stroke_color=ORANGE_ACCENT, stroke_width=2
        )
        sft_title = Text("SFT", font_size=24, color=ORANGE_ACCENT, weight=BOLD)
        sft_title.next_to(sft_box, UP, buff=0.1)
        sft_content = VGroup(
            Text("Learn from demonstrations", font_size=18, color=TEXT_WHITE),
            Text("", font_size=8),
            Text("✓ Fast training", font_size=16, color=GREEN_ACCENT),
            Text("✓ Stable", font_size=16, color=GREEN_ACCENT),
            Text("✗ Limited by data quality", font_size=16, color=RED_ACCENT),
        )
        sft_content.arrange(DOWN, buff=0.1)
        sft_content.move_to(sft_box.get_center())
        sft_group = VGroup(sft_box, sft_title, sft_content)
        
        rl_box = RoundedRectangle(
            corner_radius=0.15, width=4.5, height=2.5,
            fill_color=RED_ACCENT, fill_opacity=0.2,
            stroke_color=RED_ACCENT, stroke_width=2
        )
        rl_title = Text("RL", font_size=24, color=RED_ACCENT, weight=BOLD)
        rl_title.next_to(rl_box, UP, buff=0.1)
        rl_content = VGroup(
            Text("Learn from rewards", font_size=18, color=TEXT_WHITE),
            Text("", font_size=8),
            Text("✓ Can exceed demonstrations", font_size=16, color=GREEN_ACCENT),
            Text("✓ Optimizes for outcomes", font_size=16, color=GREEN_ACCENT),
            Text("✗ Can be unstable", font_size=16, color=RED_ACCENT),
        )
        rl_content.arrange(DOWN, buff=0.1)
        rl_content.move_to(rl_box.get_center())
        rl_group = VGroup(rl_box, rl_title, rl_content)
        
        comparison = VGroup(sft_group, rl_group)
        comparison.arrange(RIGHT, buff=1)
        comparison.move_to(DOWN * 0.8)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(motivation), run_time=0.4)
        self.play(FadeIn(sft_group), run_time=0.5)
        self.play(FadeIn(rl_group), run_time=0.5)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(motivation),
            FadeOut(comparison),
            run_time=1
        )
    
    def play_reinforce(self):
        """Explain the REINFORCE algorithm."""
        
        title = Text("REINFORCE Algorithm", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Simplified explanation
        steps = VGroup()
        
        step_data = [
            ("1. Sample", "Generate multiple completions", BLUE_PRIMARY),
            ("2. Evaluate", "Check if answer is correct", PURPLE_PRIMARY),
            ("3. Compute Rewards", "r = 1 (correct) or 0 (wrong)", GREEN_ACCENT),
            ("4. Advantage", "A = r - mean(r)", ORANGE_ACCENT),
            ("5. Update", "∇ = logP(y|x) × A", RED_ACCENT),
        ]
        
        for i, (step, desc, color) in enumerate(step_data):
            step_box = RoundedRectangle(
                corner_radius=0.1, width=6, height=0.8,
                fill_color=color, fill_opacity=0.2,
                stroke_color=color, stroke_width=2
            )
            
            step_text = Text(step, font_size=22, color=color, weight=BOLD)
            desc_text = Text(desc, font_size=18, color=TEXT_GRAY)
            
            step_text.move_to(step_box.get_left() + RIGHT * 1.2)
            desc_text.move_to(step_box.get_center() + RIGHT * 0.5)
            
            group = VGroup(step_box, step_text, desc_text)
            group.move_to(DOWN * (i - 2) * 1)
            steps.add(group)
        
        steps.move_to(ORIGIN)
        
        # Key insight
        key_insight = Text(
            "Increase probability of tokens that lead to correct answers!",
            font_size=22,
            color=CYAN_ACCENT
        )
        key_insight.to_edge(DOWN, buff=0.6)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        for step in steps:
            self.play(FadeIn(step, shift=RIGHT * 0.3), run_time=0.3)
        
        self.play(FadeIn(key_insight, shift=UP * 0.2), run_time=0.5)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(steps),
            FadeOut(key_insight),
            run_time=1
        )
    
    def play_gsm8k_example(self):
        """Show a GSM8K problem example."""
        
        title = Text("GSM8K: Grade School Math", font_size=44, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Problem
        problem_box = RoundedRectangle(
            corner_radius=0.15, width=10, height=1.5,
            fill_color=BLUE_PRIMARY, fill_opacity=0.15,
            stroke_color=BLUE_PRIMARY, stroke_width=2
        )
        problem_box.move_to(UP * 1.5)
        
        problem_label = Text("Problem:", font_size=20, color=BLUE_PRIMARY, weight=BOLD)
        problem_label.next_to(problem_box, UP, buff=0.05, aligned_edge=LEFT)
        problem_label.shift(LEFT * 4.5)
        
        problem_text = Text(
            "Janet's ducks lay 16 eggs per day. She sells the eggs\nat $2/dozen. How much does she make per week?",
            font_size=20,
            color=TEXT_WHITE
        )
        problem_text.move_to(problem_box.get_center())
        
        # Multiple samples
        samples_title = Text("16 samples generated:", font_size=20, color=TEXT_WHITE)
        samples_title.next_to(problem_box, DOWN, buff=0.4)
        
        samples = VGroup()
        sample_data = [
            ("✓ $18.67", GREEN_ACCENT),
            ("✗ $224", RED_ACCENT),
            ("✓ $18.67", GREEN_ACCENT),
            ("✗ $32", RED_ACCENT),
            ("✓ $18.67", GREEN_ACCENT),
            ("✗ $19", RED_ACCENT),
            ("✓ $18.67", GREEN_ACCENT),
            ("✗ $112", RED_ACCENT),
        ]
        
        for text, color in sample_data:
            sample = Text(text, font_size=18, color=color)
            samples.add(sample)
        
        samples.arrange_in_grid(rows=2, cols=4, buff=(0.5, 0.3))
        samples.next_to(samples_title, DOWN, buff=0.3)
        
        # Reward calculation
        reward_box = RoundedRectangle(
            corner_radius=0.1, width=6, height=1.2,
            fill_color=ORANGE_ACCENT, fill_opacity=0.15,
            stroke_color=ORANGE_ACCENT, stroke_width=2
        )
        reward_box.move_to(DOWN * 2)
        
        reward_text = VGroup(
            Text("Mean reward = 4/8 = 0.5", font_size=20, color=TEXT_WHITE),
            Text("Correct samples get advantage +0.5", font_size=18, color=GREEN_ACCENT),
        )
        reward_text.arrange(DOWN, buff=0.1)
        reward_text.move_to(reward_box.get_center())
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(problem_box), FadeIn(problem_label), run_time=0.3)
        self.play(FadeIn(problem_text), run_time=0.4)
        self.play(FadeIn(samples_title), run_time=0.3)
        
        for sample in samples:
            self.play(FadeIn(sample, scale=0.9), run_time=0.1)
        
        self.play(FadeIn(reward_box), FadeIn(reward_text), run_time=0.5)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(problem_box),
            FadeOut(problem_label),
            FadeOut(problem_text),
            FadeOut(samples_title),
            FadeOut(samples),
            FadeOut(reward_box),
            FadeOut(reward_text),
            run_time=1
        )
    
    def play_rl_results(self):
        """Show RL training results."""
        
        title = Text("RL Results on GSM8K", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Bar chart comparison
        axes = Axes(
            x_range=[0, 3, 1],
            y_range=[0, 0.1, 0.02],
            x_length=8,
            y_length=4,
            axis_config={"color": TEXT_DIM, "include_tip": False},
        )
        axes.move_to(DOWN * 0.5)
        
        # Bars
        bar_width = 0.4
        
        sft_bar = Rectangle(
            width=bar_width * 4,
            height=0.045 * 40,  # ~4.5% scaled
            fill_color=ORANGE_ACCENT,
            fill_opacity=0.7,
            stroke_color=ORANGE_ACCENT,
            stroke_width=2
        )
        sft_bar.move_to(axes.c2p(1, 0.0225) + UP * sft_bar.height / 2)
        sft_bar.align_to(axes.c2p(1, 0), DOWN)
        
        rl_bar = Rectangle(
            width=bar_width * 4,
            height=0.075 * 40,  # ~7.5% scaled
            fill_color=RED_ACCENT,
            fill_opacity=0.7,
            stroke_color=RED_ACCENT,
            stroke_width=2
        )
        rl_bar.move_to(axes.c2p(2, 0.0375) + UP * rl_bar.height / 2)
        rl_bar.align_to(axes.c2p(2, 0), DOWN)
        
        # Labels
        sft_label = Text("SFT\n4.5%", font_size=20, color=ORANGE_ACCENT)
        sft_label.next_to(sft_bar, UP, buff=0.1)
        
        rl_label = Text("RL\n7.5%", font_size=20, color=RED_ACCENT)
        rl_label.next_to(rl_bar, UP, buff=0.1)
        
        # Y-axis label
        y_label = Text("Accuracy", font_size=18, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.3).rotate(90 * DEGREES)
        
        # Improvement
        improvement = Text("+67% improvement!", font_size=28, color=GREEN_ACCENT, weight=BOLD)
        improvement.to_edge(DOWN, buff=1)
        
        # Note
        note = Text(
            "Note: Small model still struggles with math, but RL helps!",
            font_size=20,
            color=TEXT_GRAY
        )
        note.to_edge(DOWN, buff=0.5)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(Create(axes), FadeIn(y_label), run_time=0.5)
        
        self.play(GrowFromEdge(sft_bar, DOWN), run_time=0.4)
        self.play(FadeIn(sft_label), run_time=0.2)
        
        self.play(GrowFromEdge(rl_bar, DOWN), run_time=0.4)
        self.play(FadeIn(rl_label), run_time=0.2)
        
        self.play(FadeIn(improvement, scale=1.2), run_time=0.4)
        self.play(FadeIn(note), run_time=0.3)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(axes),
            FadeOut(y_label),
            FadeOut(sft_bar),
            FadeOut(rl_bar),
            FadeOut(sft_label),
            FadeOut(rl_label),
            FadeOut(improvement),
            FadeOut(note),
            run_time=1
        )
