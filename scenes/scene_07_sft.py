"""
Scene 7: Supervised Fine-Tuning (SFT)
Task mixture training and loss masking.
"""

from manim import *
try:
    from .common import *
except ImportError:
    from common import *


class SFTScene(Scene):
    """Supervised Fine-Tuning visualization."""
    
    def construct(self):
        configure_scene(self)
        
        # Part 1: What is SFT?
        self.play_sft_intro()
        
        # Part 2: Task mixture
        self.play_task_mixture()
        
        # Part 3: Loss masking
        self.play_loss_masking()
    
    def play_sft_intro(self):
        """Introduction to SFT."""
        
        title = Text("Supervised Fine-Tuning (SFT)", font_size=44, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Concept
        concept = Text(
            "Train model on high-quality task-specific data",
            font_size=28,
            color=TEXT_WHITE
        )
        concept.next_to(title, DOWN, buff=0.5)
        
        # Comparison: Midtraining vs SFT
        comparison = VGroup()
        
        mid_box = RoundedRectangle(
            corner_radius=0.1, width=4, height=1.8,
            fill_color=PURPLE_PRIMARY, fill_opacity=0.2,
            stroke_color=PURPLE_PRIMARY, stroke_width=2
        )
        mid_title = Text("Midtraining", font_size=22, color=PURPLE_PRIMARY, weight=BOLD)
        mid_title.next_to(mid_box, UP, buff=0.1)
        mid_text = Text(
            "General conversations\nBroad coverage\nMixed data sources",
            font_size=16,
            color=TEXT_GRAY
        )
        mid_text.move_to(mid_box.get_center())
        mid_group = VGroup(mid_box, mid_title, mid_text)
        
        sft_box = RoundedRectangle(
            corner_radius=0.1, width=4, height=1.8,
            fill_color=ORANGE_ACCENT, fill_opacity=0.2,
            stroke_color=ORANGE_ACCENT, stroke_width=2
        )
        sft_title = Text("SFT", font_size=22, color=ORANGE_ACCENT, weight=BOLD)
        sft_title.next_to(sft_box, UP, buff=0.1)
        sft_text = Text(
            "Task-specific data\nFocused training\nEach example in isolation",
            font_size=16,
            color=TEXT_GRAY
        )
        sft_text.move_to(sft_box.get_center())
        sft_group = VGroup(sft_box, sft_title, sft_text)
        
        comparison.add(mid_group, sft_group)
        comparison.arrange(RIGHT, buff=1.5)
        comparison.move_to(DOWN * 0.5)
        
        # Arrow
        arrow = Arrow(mid_box.get_right(), sft_box.get_left(), color=CYAN_ACCENT, buff=0.2, stroke_width=3)
        arrow_label = Text("→ Refine", font_size=18, color=CYAN_ACCENT)
        arrow_label.next_to(arrow, UP, buff=0.1)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(concept), run_time=0.4)
        self.play(FadeIn(mid_group), run_time=0.4)
        self.play(GrowArrow(arrow), FadeIn(arrow_label), run_time=0.3)
        self.play(FadeIn(sft_group), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(concept),
            FadeOut(comparison),
            FadeOut(arrow),
            FadeOut(arrow_label),
            run_time=1
        )
    
    def play_task_mixture(self):
        """Show the task mixture used in SFT."""
        
        title = Text("SFT Task Mixture", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Task data
        tasks = [
            ("ARC-Easy", 2300, BLUE_PRIMARY),
            ("ARC-Challenge", 1100, BLUE_PRIMARY),
            ("GSM8K", 8000, PURPLE_PRIMARY),
            ("SmolTalk", 10000, GREEN_ACCENT),
            ("Identity", 1000, ORANGE_ACCENT),
            ("Spelling", 600, PINK_ACCENT),
        ]
        
        total = sum(t[1] for t in tasks)
        
        # Create bar chart
        bars = VGroup()
        labels = VGroup()
        
        max_count = max(t[1] for t in tasks)
        bar_max_width = 5
        
        for i, (name, count, color) in enumerate(tasks):
            bar_width = (count / max_count) * bar_max_width
            
            bar = RoundedRectangle(
                corner_radius=0.05,
                width=bar_width,
                height=0.5,
                fill_color=color,
                fill_opacity=0.6,
                stroke_color=color,
                stroke_width=2
            )
            bar.align_to(LEFT * 2, LEFT)
            bar.move_to(DOWN * (i - 2.5) * 0.7)
            
            name_label = Text(name, font_size=18, color=TEXT_WHITE)
            name_label.next_to(bar, LEFT, buff=0.3)
            
            count_label = Text(f"{count:,}", font_size=16, color=TEXT_GRAY)
            count_label.next_to(bar, RIGHT, buff=0.2)
            
            bars.add(bar)
            labels.add(VGroup(name_label, count_label))
        
        chart = VGroup(bars, labels)
        chart.move_to(LEFT * 0.5)
        
        # Total
        total_text = Text(f"Total: ~{total//1000}K examples", font_size=24, color=TEXT_WHITE)
        total_text.to_edge(DOWN, buff=0.8)
        
        # Descriptions
        desc_box = RoundedRectangle(
            corner_radius=0.1, width=3.5, height=3,
            fill_color=CARD_BG, fill_opacity=0.5,
            stroke_color=TEXT_DIM, stroke_width=1
        )
        desc_box.move_to(RIGHT * 4)
        
        descriptions = VGroup(
            Text("ARC: Science questions", font_size=16, color=BLUE_PRIMARY),
            Text("GSM8K: Math problems", font_size=16, color=PURPLE_PRIMARY),
            Text("SmolTalk: General chat", font_size=16, color=GREEN_ACCENT),
            Text("Identity: Personality", font_size=16, color=ORANGE_ACCENT),
            Text("Spelling: Letter tasks", font_size=16, color=PINK_ACCENT),
        )
        descriptions.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        descriptions.move_to(desc_box.get_center())
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        for bar, label_group in zip(bars, labels):
            self.play(
                GrowFromEdge(bar, LEFT),
                FadeIn(label_group[0]),
                FadeIn(label_group[1]),
                run_time=0.25
            )
        
        self.play(FadeIn(desc_box), FadeIn(descriptions), run_time=0.5)
        self.play(FadeIn(total_text), run_time=0.3)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(chart),
            FadeOut(desc_box),
            FadeOut(descriptions),
            FadeOut(total_text),
            run_time=1
        )
    
    def play_loss_masking(self):
        """Show how loss masking works in SFT."""
        
        title = Text("Loss Masking", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        subtitle = Text(
            "Only compute loss on assistant responses",
            font_size=26,
            color=TEXT_WHITE
        )
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Token sequence with masks
        tokens_data = [
            ("<|bos|>", False, BLUE_PRIMARY),
            ("<|user_start|>", False, GREEN_ACCENT),
            ("What", False, TEXT_WHITE),
            ("is", False, TEXT_WHITE),
            ("2+2?", False, TEXT_WHITE),
            ("<|user_end|>", False, GREEN_ACCENT),
            ("<|assistant_start|>", False, PURPLE_PRIMARY),
            ("The", True, TEXT_WHITE),
            ("answer", True, TEXT_WHITE),
            ("is", True, TEXT_WHITE),
            ("4", True, TEXT_WHITE),
            ("<|assistant_end|>", True, PURPLE_PRIMARY),
        ]
        
        token_row = VGroup()
        mask_row = VGroup()
        
        for text, train, color in tokens_data:
            # Token box
            token = TokenBox(text, color=color, font_size=18)
            token_row.add(token)
            
            # Mask indicator
            if train:
                mask = Text("✓", font_size=20, color=GREEN_ACCENT)
            else:
                mask = Text("✗", font_size=20, color=RED_ACCENT)
            mask_row.add(mask)
        
        token_row.arrange(RIGHT, buff=0.08)
        token_row.scale(0.85)
        token_row.move_to(UP * 0.5)
        
        # Align masks under tokens
        for token, mask in zip(token_row, mask_row):
            mask.move_to(token.get_center() + DOWN * 0.8)
        
        mask_row_group = VGroup(*mask_row)
        
        # Legend
        legend = VGroup(
            VGroup(
                Text("✓", font_size=20, color=GREEN_ACCENT),
                Text("= Compute loss (train)", font_size=18, color=TEXT_GRAY)
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Text("✗", font_size=20, color=RED_ACCENT),
                Text("= Ignore (no gradient)", font_size=18, color=TEXT_GRAY)
            ).arrange(RIGHT, buff=0.2),
        )
        legend.arrange(RIGHT, buff=1)
        legend.move_to(DOWN * 2)
        
        # Key insight
        key_insight = Text(
            "This prevents learning to copy user messages verbatim",
            font_size=22,
            color=ORANGE_ACCENT
        )
        key_insight.to_edge(DOWN, buff=0.6)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(subtitle), run_time=0.4)
        
        for token in token_row:
            self.play(FadeIn(token, scale=0.9), run_time=0.1)
        
        self.wait(0.5)
        
        for mask in mask_row:
            self.play(FadeIn(mask, scale=1.2), run_time=0.08)
        
        self.play(FadeIn(legend), run_time=0.4)
        self.play(FadeIn(key_insight, shift=UP * 0.2), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(token_row),
            FadeOut(mask_row_group),
            FadeOut(legend),
            FadeOut(key_insight),
            run_time=1
        )
