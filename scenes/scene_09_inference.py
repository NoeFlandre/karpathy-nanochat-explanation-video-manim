"""
Scene 9: Inference Engine
KV Cache, autoregressive generation, and tool use.
"""

from manim import *
try:
    from .common import *
except ImportError:
    from common import *
import numpy as np


class InferenceScene(Scene):
    """Inference engine visualization."""
    
    def construct(self):
        configure_scene(self)
        
        # Part 1: Autoregressive generation
        self.play_autoregressive()
        
        # Part 2: KV Cache
        self.play_kv_cache()
        
        # Part 3: Sampling strategies
        self.play_sampling()
        
        # Part 4: Tool execution
        self.play_tool_execution()
    
    def play_autoregressive(self):
        """Show autoregressive token generation."""
        
        title = Text("Autoregressive Generation", font_size=44, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        subtitle = Text(
            "Generate one token at a time",
            font_size=26,
            color=TEXT_WHITE
        )
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Prompt tokens
        prompt_label = Text("Prompt:", font_size=20, color=GREEN_ACCENT)
        prompt_label.move_to(UP * 1 + LEFT * 5)
        
        prompt_tokens = ["The", "sky", "is"]
        prompt_boxes = VGroup()
        
        for token in prompt_tokens:
            box = TokenBox(token, color=GREEN_ACCENT, font_size=24)
            prompt_boxes.add(box)
        
        prompt_boxes.arrange(RIGHT, buff=0.15)
        prompt_boxes.next_to(prompt_label, RIGHT, buff=0.3)
        
        # Arrow
        arrow = Arrow(
            prompt_boxes.get_right() + RIGHT * 0.3,
            prompt_boxes.get_right() + RIGHT * 1.5,
            color=CYAN_ACCENT,
            stroke_width=3
        )
        
        # Generated tokens appearing one by one
        generated_tokens = ["blue", "and", "beautiful", "."]
        generated_boxes = VGroup()
        
        for token in generated_tokens:
            box = TokenBox(token, color=PURPLE_PRIMARY, font_size=24)
            generated_boxes.add(box)
        
        generated_boxes.arrange(RIGHT, buff=0.15)
        generated_boxes.next_to(arrow, RIGHT, buff=0.3)
        
        # Model in the middle
        model_box = RoundedRectangle(
            corner_radius=0.15, width=2.5, height=1.5,
            fill_color=BLUE_PRIMARY, fill_opacity=0.3,
            stroke_color=BLUE_PRIMARY, stroke_width=2
        )
        model_label = Text("GPT\nModel", font_size=22, color=TEXT_WHITE)
        model_label.move_to(model_box.get_center())
        model_group = VGroup(model_box, model_label)
        model_group.move_to(DOWN * 1)
        
        # Loop arrow
        loop_text = Text("Feed output back as input", font_size=18, color=TEXT_GRAY)
        loop_text.move_to(DOWN * 2.5)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(subtitle), run_time=0.4)
        
        self.play(FadeIn(prompt_label), run_time=0.2)
        for box in prompt_boxes:
            self.play(FadeIn(box, scale=0.9), run_time=0.15)
        
        self.play(GrowArrow(arrow), run_time=0.3)
        self.play(FadeIn(model_group), run_time=0.4)
        
        # Generate tokens one by one with animation
        for box in generated_boxes:
            # Flash model
            self.play(
                model_box.animate.set_fill(opacity=0.6),
                run_time=0.15
            )
            self.play(
                model_box.animate.set_fill(opacity=0.3),
                FadeIn(box, shift=RIGHT * 0.3),
                run_time=0.25
            )
        
        self.play(FadeIn(loop_text), run_time=0.3)
        
        self.wait(1.5)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(prompt_label),
            FadeOut(prompt_boxes),
            FadeOut(arrow),
            FadeOut(generated_boxes),
            FadeOut(model_group),
            FadeOut(loop_text),
            run_time=1
        )
    
    def play_kv_cache(self):
        """Explain the KV Cache mechanism."""
        
        title = Text("KV Cache", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        subtitle = Text(
            "Cache Key/Value tensors to avoid recomputation",
            font_size=24,
            color=TEXT_WHITE
        )
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Without cache - O(n²)
        without_box = RoundedRectangle(
            corner_radius=0.15, width=5, height=2.5,
            fill_color=RED_ACCENT, fill_opacity=0.15,
            stroke_color=RED_ACCENT, stroke_width=2
        )
        without_title = Text("Without Cache", font_size=22, color=RED_ACCENT, weight=BOLD)
        without_title.next_to(without_box, UP, buff=0.1)
        
        # Show recomputation
        recompute_grid = VGroup()
        for i in range(4):
            row = VGroup()
            for j in range(4):
                cell = Square(
                    side_length=0.35,
                    fill_color=RED_ACCENT if j <= i else TEXT_DIM,
                    fill_opacity=0.6 if j <= i else 0.1,
                    stroke_color=TEXT_DIM,
                    stroke_width=0.5
                )
                row.add(cell)
            row.arrange(RIGHT, buff=0.05)
            recompute_grid.add(row)
        recompute_grid.arrange(DOWN, buff=0.05)
        recompute_grid.move_to(without_box.get_center())
        
        without_group = VGroup(without_box, without_title, recompute_grid)
        without_group.move_to(LEFT * 3)
        
        # With cache - O(n)
        with_box = RoundedRectangle(
            corner_radius=0.15, width=5, height=2.5,
            fill_color=GREEN_ACCENT, fill_opacity=0.15,
            stroke_color=GREEN_ACCENT, stroke_width=2
        )
        with_title = Text("With KV Cache", font_size=22, color=GREEN_ACCENT, weight=BOLD)
        with_title.next_to(with_box, UP, buff=0.1)
        
        # Show cached + new
        cache_grid = VGroup()
        for i in range(4):
            row = VGroup()
            for j in range(4):
                if j <= i:
                    if i == j:
                        color = GREEN_ACCENT  # New computation
                    else:
                        color = BLUE_PRIMARY  # Cached
                else:
                    color = TEXT_DIM
                
                cell = Square(
                    side_length=0.35,
                    fill_color=color,
                    fill_opacity=0.6 if j <= i else 0.1,
                    stroke_color=TEXT_DIM,
                    stroke_width=0.5
                )
                row.add(cell)
            row.arrange(RIGHT, buff=0.05)
            cache_grid.add(row)
        cache_grid.arrange(DOWN, buff=0.05)
        cache_grid.move_to(with_box.get_center())
        
        with_group = VGroup(with_box, with_title, cache_grid)
        with_group.move_to(RIGHT * 3)
        
        # Legend
        legend = VGroup(
            VGroup(
                Square(side_length=0.25, fill_color=BLUE_PRIMARY, fill_opacity=0.6, stroke_width=0.5),
                Text("Cached", font_size=16, color=TEXT_GRAY)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Square(side_length=0.25, fill_color=GREEN_ACCENT, fill_opacity=0.6, stroke_width=0.5),
                Text("New", font_size=16, color=TEXT_GRAY)
            ).arrange(RIGHT, buff=0.1),
        )
        legend.arrange(RIGHT, buff=0.8)
        legend.move_to(DOWN * 2.8)
        
        # Performance note
        perf_note = Text(
            "Speedup: O(n²) → O(n) per token!",
            font_size=24,
            color=ORANGE_ACCENT
        )
        perf_note.to_edge(DOWN, buff=0.5)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(subtitle), run_time=0.4)
        
        self.play(FadeIn(without_group), run_time=0.5)
        self.play(FadeIn(with_group), run_time=0.5)
        self.play(FadeIn(legend), run_time=0.3)
        self.play(FadeIn(perf_note, shift=UP * 0.2), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(without_group),
            FadeOut(with_group),
            FadeOut(legend),
            FadeOut(perf_note),
            run_time=1
        )
    
    def play_sampling(self):
        """Show temperature and top-k sampling."""
        
        title = Text("Sampling Strategies", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Temperature explanation
        temp_label = Text("Temperature Controls Randomness", font_size=26, color=TEXT_WHITE)
        temp_label.next_to(title, DOWN, buff=0.5)
        
        # Create probability distributions
        def create_prob_bars(probs, label, color, position):
            group = VGroup()
            bar_group = VGroup()
            
            tokens = ["the", "a", "blue", "sky", "is"]
            max_height = 2
            bar_width = 0.4
            
            for i, (token, prob) in enumerate(zip(tokens, probs)):
                bar = Rectangle(
                    width=bar_width,
                    height=prob * max_height,
                    fill_color=color,
                    fill_opacity=0.7,
                    stroke_color=color,
                    stroke_width=1
                )
                bar.align_to(ORIGIN, DOWN)
                bar.shift(RIGHT * i * (bar_width + 0.1))
                
                token_label = Text(token, font_size=14, color=TEXT_GRAY)
                token_label.next_to(bar, DOWN, buff=0.05)
                
                bar_group.add(VGroup(bar, token_label))
            
            bar_group.move_to(position)
            
            title_text = Text(label, font_size=18, color=color, weight=BOLD)
            title_text.next_to(bar_group, UP, buff=0.3)
            
            group.add(bar_group, title_text)
            return group
        
        # Different temperatures
        low_temp = create_prob_bars(
            [0.9, 0.05, 0.02, 0.02, 0.01],
            "T=0.1 (Focused)",
            BLUE_PRIMARY,
            LEFT * 3.5 + DOWN * 0.5
        )
        
        mid_temp = create_prob_bars(
            [0.5, 0.2, 0.15, 0.1, 0.05],
            "T=1.0 (Balanced)",
            PURPLE_PRIMARY,
            DOWN * 0.5
        )
        
        high_temp = create_prob_bars(
            [0.25, 0.22, 0.2, 0.18, 0.15],
            "T=2.0 (Random)",
            RED_ACCENT,
            RIGHT * 3.5 + DOWN * 0.5
        )
        
        # Top-k explanation
        topk_text = Text(
            "Top-k: Only consider k most probable tokens",
            font_size=22,
            color=GREEN_ACCENT
        )
        topk_text.to_edge(DOWN, buff=0.8)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(temp_label), run_time=0.4)
        
        self.play(FadeIn(low_temp), run_time=0.4)
        self.play(FadeIn(mid_temp), run_time=0.4)
        self.play(FadeIn(high_temp), run_time=0.4)
        
        self.play(FadeIn(topk_text), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(temp_label),
            FadeOut(low_temp),
            FadeOut(mid_temp),
            FadeOut(high_temp),
            FadeOut(topk_text),
            run_time=1
        )
    
    def play_tool_execution(self):
        """Show tool execution flow."""
        
        title = Text("Tool Execution Flow", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # State machine
        states = [
            ("Generating", BLUE_PRIMARY),
            ("Python Block\nDetected", ORANGE_ACCENT),
            ("Execute\nCode", GREEN_ACCENT),
            ("Inject\nResult", PURPLE_PRIMARY),
        ]
        
        state_boxes = VGroup()
        
        for name, color in states:
            box = RoundedRectangle(
                corner_radius=0.15, width=2, height=1.2,
                fill_color=color, fill_opacity=0.3,
                stroke_color=color, stroke_width=2
            )
            label = Text(name, font_size=18, color=TEXT_WHITE)
            label.move_to(box.get_center())
            state_boxes.add(VGroup(box, label))
        
        state_boxes.arrange(RIGHT, buff=0.8)
        state_boxes.move_to(UP * 0.5)
        
        # Arrows
        arrows = VGroup()
        for i in range(len(state_boxes) - 1):
            arrow = Arrow(
                state_boxes[i].get_right(),
                state_boxes[i + 1].get_left(),
                color=TEXT_DIM,
                buff=0.1,
                stroke_width=2
            )
            arrows.add(arrow)
        
        # Loop back arrow
        loop_arrow = CurvedArrow(
            state_boxes[-1].get_bottom() + DOWN * 0.2,
            state_boxes[0].get_bottom() + DOWN * 0.2,
            angle=TAU / 4,
            color=CYAN_ACCENT,
            stroke_width=2
        )
        loop_label = Text("Continue", font_size=16, color=CYAN_ACCENT)
        loop_label.next_to(loop_arrow, DOWN, buff=0.1)
        
        # Trigger tokens
        triggers = VGroup(
            TokenBox("<|python_start|>", color=ORANGE_ACCENT, font_size=16),
            Text("triggers detection", font_size=16, color=TEXT_GRAY),
        )
        triggers.arrange(RIGHT, buff=0.2)
        triggers.move_to(DOWN * 1.5)
        
        # Safety note
        safety = Text(
            "Sandboxed execution: timeout, memory limits, disabled dangerous functions",
            font_size=18,
            color=RED_ACCENT
        )
        safety.to_edge(DOWN, buff=0.6)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        for i, (box, arrow) in enumerate(zip(state_boxes, arrows)):
            self.play(FadeIn(box, scale=0.9), run_time=0.25)
            self.play(GrowArrow(arrow), run_time=0.2)
        
        self.play(FadeIn(state_boxes[-1], scale=0.9), run_time=0.25)
        self.play(Create(loop_arrow), FadeIn(loop_label), run_time=0.4)
        
        self.play(FadeIn(triggers), run_time=0.3)
        self.play(FadeIn(safety, shift=UP * 0.2), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(state_boxes),
            FadeOut(arrows),
            FadeOut(loop_arrow),
            FadeOut(loop_label),
            FadeOut(triggers),
            FadeOut(safety),
            run_time=1
        )
