"""
Scene 3: Tokenizer Deep Dive
BPE algorithm visualization, byte pair merging, and special tokens.
"""

from manim import *
try:
    from .common import *
except ImportError:
    from common import *
import numpy as np


class TokenizerScene(Scene):
    """Deep dive into the BPE tokenizer."""
    
    def construct(self):
        configure_scene(self)
        
        # Part 1: What is tokenization?
        self.play_tokenization_intro()
        
        # Part 2: BPE algorithm visualization
        self.play_bpe_algorithm()
        
        # Part 3: Special tokens
        self.play_special_tokens()
        
        # Part 4: Rust implementation
        self.play_rust_bpe()
    
    def play_tokenization_intro(self):
        """Introduction to tokenization concept."""
        
        title = Text("Tokenization", font_size=56, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Show text to tokens transformation
        original_text = Text('"Hello, world!"', font_size=40, color=TEXT_WHITE)
        original_text.move_to(UP * 1)
        
        arrow_down = Arrow(UP * 0.3, DOWN * 0.5, color=CYAN_ACCENT, stroke_width=3)
        
        # Token boxes
        tokens = ["Hello", ",", " world", "!"]
        token_ids = [15496, 11, 995, 0]
        
        token_boxes = VGroup()
        for i, (tok, tid) in enumerate(zip(tokens, token_ids)):
            box = TokenBox(tok, color=BLUE_PRIMARY)
            id_label = Text(str(tid), font_size=18, color=TEXT_GRAY)
            id_label.next_to(box, DOWN, buff=0.1)
            group = VGroup(box, id_label)
            token_boxes.add(group)
        
        token_boxes.arrange(RIGHT, buff=0.4)
        token_boxes.move_to(DOWN * 1.5)
        
        # Explanation
        explanation = Text(
            "Convert text → integer sequences that neural networks can process",
            font_size=24,
            color=TEXT_GRAY
        )
        explanation.to_edge(DOWN, buff=1)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(original_text), run_time=0.5)
        self.play(GrowArrow(arrow_down), run_time=0.3)
        
        for token_group in token_boxes:
            self.play(FadeIn(token_group, scale=0.8), run_time=0.25)
        
        self.play(FadeIn(explanation), run_time=0.5)
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(original_text),
            FadeOut(arrow_down),
            FadeOut(token_boxes),
            FadeOut(explanation),
            run_time=1
        )
    
    def play_bpe_algorithm(self):
        """Visualize the BPE (Byte Pair Encoding) algorithm."""
        
        title = Text("Byte Pair Encoding (BPE)", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        self.play(Write(title), run_time=0.8)
        
        # Step-by-step BPE explanation
        step1_title = Text("Step 1: Start with bytes", font_size=32, color=BLUE_PRIMARY)
        step1_title.next_to(title, DOWN, buff=0.8)
        
        # Show "hello" as individual bytes
        word = "hello"
        byte_boxes = VGroup()
        
        for char in word:
            box = TokenBox(char, color=PURPLE_PRIMARY, font_size=36)
            byte_boxes.add(box)
        
        byte_boxes.arrange(RIGHT, buff=0.1)
        byte_boxes.move_to(ORIGIN)
        
        # Byte values below
        byte_values = VGroup()
        for i, char in enumerate(word):
            val = Text(str(ord(char)), font_size=18, color=TEXT_GRAY)
            val.next_to(byte_boxes[i], DOWN, buff=0.15)
            byte_values.add(val)
        
        self.play(FadeIn(step1_title), run_time=0.4)
        
        for box, val in zip(byte_boxes, byte_values):
            self.play(FadeIn(box), FadeIn(val), run_time=0.2)
        
        self.wait(1)
        
        # Step 2: Find most frequent pair
        step2_title = Text("Step 2: Find most frequent pair", font_size=32, color=BLUE_PRIMARY)
        step2_title.next_to(title, DOWN, buff=0.8)
        
        self.play(
            FadeOut(step1_title),
            FadeIn(step2_title),
            run_time=0.4
        )
        
        # Highlight 'l' and 'l' pair
        highlight_rect = SurroundingRectangle(
            VGroup(byte_boxes[2], byte_boxes[3]),
            color=CYAN_ACCENT,
            buff=0.1
        )
        
        pair_label = Text("'ll' appears most often!", font_size=24, color=CYAN_ACCENT)
        pair_label.next_to(byte_boxes, DOWN, buff=0.8)
        
        self.play(Create(highlight_rect), run_time=0.5)
        self.play(FadeIn(pair_label), run_time=0.3)
        self.wait(1)
        
        # Step 3: Merge the pair
        step3_title = Text("Step 3: Merge into new token", font_size=32, color=BLUE_PRIMARY)
        step3_title.next_to(title, DOWN, buff=0.8)
        
        self.play(
            FadeOut(step2_title),
            FadeIn(step3_title),
            FadeOut(pair_label),
            run_time=0.4
        )
        
        # Create merged token
        merged = TokenBox("ll", color=GREEN_ACCENT, font_size=36)
        merged.move_to(VGroup(byte_boxes[2], byte_boxes[3]).get_center())
        
        merge_label = Text("Token 256", font_size=18, color=GREEN_ACCENT)
        merge_label.next_to(merged, DOWN, buff=0.15)
        
        # Animate merge
        self.play(
            FadeOut(byte_boxes[2]),
            FadeOut(byte_boxes[3]),
            FadeOut(byte_values[2]),
            FadeOut(byte_values[3]),
            FadeOut(highlight_rect),
            run_time=0.3
        )
        self.play(
            FadeIn(merged, scale=1.2),
            FadeIn(merge_label),
            run_time=0.4
        )
        
        # Show new sequence
        new_sequence = VGroup(
            byte_boxes[0].copy(),
            byte_boxes[1].copy(),
            merged.copy(),
            byte_boxes[4].copy(),
        )
        new_sequence.arrange(RIGHT, buff=0.1)
        new_sequence.move_to(DOWN * 1.5)
        
        new_label = Text("New sequence: 4 tokens instead of 5", font_size=24, color=TEXT_GRAY)
        new_label.next_to(new_sequence, DOWN, buff=0.5)
        
        self.play(FadeIn(new_sequence), run_time=0.5)
        self.play(FadeIn(new_label), run_time=0.3)
        
        self.wait(1.5)
        
        # Show iteration concept
        iteration_text = Text(
            "Repeat until desired vocabulary size (65,536 tokens)",
            font_size=24,
            color=ORANGE_ACCENT
        )
        iteration_text.to_edge(DOWN, buff=0.8)
        
        self.play(FadeIn(iteration_text, shift=UP * 0.2), run_time=0.5)
        self.wait(2)
        
        # Clear all
        self.play(
            FadeOut(title),
            FadeOut(step3_title),
            FadeOut(byte_boxes[0]),
            FadeOut(byte_boxes[1]),
            FadeOut(byte_boxes[4]),
            FadeOut(byte_values[0]),
            FadeOut(byte_values[1]),
            FadeOut(byte_values[4]),
            FadeOut(merged),
            FadeOut(merge_label),
            FadeOut(new_sequence),
            FadeOut(new_label),
            FadeOut(iteration_text),
            run_time=1
        )
    
    def play_special_tokens(self):
        """Show the special tokens used in nanochat."""
        
        title = Text("Special Tokens", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Special tokens grid
        tokens = [
            ("<|bos|>", "Beginning of sequence", BLUE_PRIMARY),
            ("<|user_start|>", "User message starts", GREEN_ACCENT),
            ("<|user_end|>", "User message ends", GREEN_ACCENT),
            ("<|assistant_start|>", "Assistant response starts", PURPLE_PRIMARY),
            ("<|assistant_end|>", "Assistant response ends", PURPLE_PRIMARY),
            ("<|python_start|>", "Python code block starts", ORANGE_ACCENT),
            ("<|python_end|>", "Python code block ends", ORANGE_ACCENT),
            ("<|output_start|>", "Tool output starts", RED_ACCENT),
            ("<|output_end|>", "Tool output ends", RED_ACCENT),
        ]
        
        token_grid = VGroup()
        
        for i, (token, desc, color) in enumerate(tokens):
            token_text = Text(token, font_size=22, color=color)
            desc_text = Text(desc, font_size=18, color=TEXT_GRAY)
            
            row = i // 3
            col = i % 3
            
            group = VGroup(token_text, desc_text)
            desc_text.next_to(token_text, DOWN, buff=0.05)
            
            group.move_to(RIGHT * (col - 1) * 3.8 + DOWN * (row - 0.5) * 1.5)
            token_grid.add(group)
        
        token_grid.move_to(DOWN * 0.3)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        for token_group in token_grid:
            self.play(FadeIn(token_group, scale=0.9), run_time=0.2)
        
        # Example conversation
        example_title = Text("Example Conversation Format:", font_size=24, color=TEXT_WHITE)
        example_title.to_edge(DOWN, buff=1.8)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(token_grid),
            run_time=1
        )
    
    def play_rust_bpe(self):
        """Show the Rust BPE implementation for speed."""
        
        title = Text("Rust BPE: Speed Matters", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Performance comparison
        comparison_title = Text("Training Time Comparison", font_size=32, color=TEXT_WHITE)
        comparison_title.next_to(title, DOWN, buff=0.6)
        
        # Bar chart
        python_bar = RoundedRectangle(
            corner_radius=0.1,
            width=5,
            height=0.6,
            fill_color=RED_ACCENT,
            fill_opacity=0.6,
            stroke_color=RED_ACCENT,
            stroke_width=2
        )
        python_bar.move_to(LEFT * 0.5 + UP * 0.5)
        
        rust_bar = RoundedRectangle(
            corner_radius=0.1,
            width=1.5,
            height=0.6,
            fill_color=GREEN_ACCENT,
            fill_opacity=0.6,
            stroke_color=GREEN_ACCENT,
            stroke_width=2
        )
        rust_bar.align_to(python_bar, LEFT)
        rust_bar.move_to(LEFT * 2.25 + DOWN * 0.5)
        
        python_label = Text("Python: ~30 min", font_size=20, color=TEXT_WHITE)
        python_label.next_to(python_bar, RIGHT, buff=0.3)
        
        rust_label = Text("Rust: ~2 min", font_size=20, color=TEXT_WHITE)
        rust_label.next_to(rust_bar, RIGHT, buff=0.3)
        
        speedup = Text("15× faster!", font_size=36, color=GREEN_ACCENT, weight=BOLD)
        speedup.move_to(DOWN * 1.8)
        
        # Key features
        features = VGroup()
        feature_items = [
            "✓ Parallel processing with Rayon",
            "✓ Efficient heap-based merging",
            "✓ Python bindings via PyO3",
            "✓ tiktoken for inference",
        ]
        
        for i, item in enumerate(feature_items):
            text = Text(item, font_size=22, color=TEXT_GRAY)
            text.move_to(DOWN * 2.8 + DOWN * i * 0.4)
            features.add(text)
        
        features.move_to(DOWN * 2.5)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(comparison_title), run_time=0.4)
        
        self.play(GrowFromEdge(python_bar, LEFT), run_time=0.6)
        self.play(FadeIn(python_label), run_time=0.3)
        
        self.play(GrowFromEdge(rust_bar, LEFT), run_time=0.4)
        self.play(FadeIn(rust_label), run_time=0.3)
        
        self.play(FadeIn(speedup, scale=1.3), run_time=0.4)
        
        for feature in features:
            self.play(FadeIn(feature, shift=RIGHT * 0.2), run_time=0.2)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(comparison_title),
            FadeOut(python_bar),
            FadeOut(rust_bar),
            FadeOut(python_label),
            FadeOut(rust_label),
            FadeOut(speedup),
            FadeOut(features),
            run_time=1
        )
