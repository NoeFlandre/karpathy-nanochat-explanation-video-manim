"""
Scene 10: Conclusion
Summary, benchmarks, and closing.
"""

from manim import *
try:
    from .common import *
except ImportError:
    from common import *


class ConclusionScene(Scene):
    """Conclusion with summary and benchmarks."""
    
    def construct(self):
        configure_scene(self)
        
        # Part 1: Benchmark results
        self.play_benchmarks()
        
        # Part 2: Key takeaways
        self.play_takeaways()
        
        # Part 3: Closing
        self.play_closing()
    
    def play_benchmarks(self):
        """Show benchmark results."""
        
        title = Text("Benchmark Results", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        subtitle = Text("d20 Model ($100 tier)", font_size=24, color=TEXT_GRAY)
        subtitle.next_to(title, DOWN, buff=0.2)
        
        # Results table
        headers = ["Metric", "BASE", "MID", "SFT", "RL"]
        data = [
            ("CORE", "0.22", "-", "-", "-"),
            ("ARC-Challenge", "-", "0.29", "0.28", "-"),
            ("ARC-Easy", "-", "0.36", "0.39", "-"),
            ("GSM8K", "-", "0.03", "0.05", "0.08"),
            ("HumanEval", "-", "0.07", "0.09", "-"),
            ("MMLU", "-", "0.31", "0.32", "-"),
        ]
        
        # Create table
        table = VGroup()
        
        # Header row
        header_row = VGroup()
        for i, header in enumerate(headers):
            cell = Text(header, font_size=20, color=CYAN_ACCENT, weight=BOLD)
            cell.move_to(RIGHT * (i - 2) * 2)
            header_row.add(cell)
        header_row.move_to(UP * 1.5)
        table.add(header_row)
        
        # Data rows
        for row_idx, row_data in enumerate(data):
            row = VGroup()
            for col_idx, value in enumerate(row_data):
                if col_idx == 0:
                    cell = Text(value, font_size=18, color=TEXT_WHITE)
                elif value == "-":
                    cell = Text(value, font_size=18, color=TEXT_DIM)
                else:
                    # Color based on stage
                    colors = [TEXT_WHITE, BLUE_PRIMARY, GREEN_ACCENT, ORANGE_ACCENT, RED_ACCENT]
                    cell = Text(value, font_size=18, color=colors[col_idx])
                
                cell.move_to(RIGHT * (col_idx - 2) * 2)
                row.add(cell)
            
            row.move_to(UP * (1 - row_idx * 0.5))
            table.add(row)
        
        table.move_to(DOWN * 0.3)
        
        # Training time
        time_note = Text(
            "Total training time: ~4 hours on 8×H100",
            font_size=22,
            color=GREEN_ACCENT
        )
        time_note.to_edge(DOWN, buff=0.8)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(subtitle), run_time=0.3)
        
        # Animate table row by row
        for row in table:
            self.play(FadeIn(row), run_time=0.2)
        
        self.play(FadeIn(time_note), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(table),
            FadeOut(time_note),
            run_time=1
        )
    
    def play_takeaways(self):
        """Key takeaways from nanochat."""
        
        title = Text("Key Takeaways", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        takeaways = [
            ("🎯", "Full LLM pipeline in ~8K lines of code"),
            ("💰", "Train your own ChatGPT for $100-$800"),
            ("🔧", "Clean, hackable, minimal codebase"),
            ("🚀", "Modern architecture: RoPE, GQA, Muon optimizer"),
            ("🧪", "Complete training: Tokenizer → Base → Mid → SFT → RL"),
            ("🌐", "Web UI for chatting with your model"),
        ]
        
        takeaway_group = VGroup()
        
        for i, (emoji, text) in enumerate(takeaways):
            emoji_text = Text(emoji, font_size=32)
            content_text = Text(text, font_size=24, color=TEXT_WHITE)
            content_text.next_to(emoji_text, RIGHT, buff=0.3)
            
            row = VGroup(emoji_text, content_text)
            row.move_to(DOWN * (i - 2.5) * 0.7 + LEFT * 1)
            takeaway_group.add(row)
        
        takeaway_group.move_to(DOWN * 0.3)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        for takeaway in takeaway_group:
            self.play(FadeIn(takeaway, shift=RIGHT * 0.3), run_time=0.3)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(takeaway_group),
            run_time=1
        )
    
    def play_closing(self):
        """Closing animation with call to action."""
        
        # nanochat logo/title
        logo_text = Text("nanochat", font_size=96, weight=BOLD)
        logo_text.set_color_by_gradient(BLUE_PRIMARY, PURPLE_PRIMARY)
        
        tagline = Text(
            "The best ChatGPT that $100 can buy",
            font_size=32,
            color=TEXT_GRAY,
            slant=ITALIC
        )
        tagline.next_to(logo_text, DOWN, buff=0.5)
        
        # GitHub link
        github = Text(
            "github.com/karpathy/nanochat",
            font_size=28,
            color=CYAN_ACCENT
        )
        github.next_to(tagline, DOWN, buff=0.8)
        
        # Try it
        try_text = Text(
            "Try it: nanochat.karpathy.ai",
            font_size=24,
            color=GREEN_ACCENT
        )
        try_text.next_to(github, DOWN, buff=0.3)
        
        # Credits
        credits = VGroup(
            Text("Created by Andrej Karpathy", font_size=20, color=TEXT_GRAY),
            Text("Video by Manim", font_size=16, color=TEXT_DIM),
        )
        credits.arrange(DOWN, buff=0.15)
        credits.to_edge(DOWN, buff=0.8)
        
        # Animate
        self.play(Write(logo_text), run_time=1.5)
        self.play(FadeIn(tagline, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(github), run_time=0.4)
        self.play(FadeIn(try_text), run_time=0.4)
        self.play(FadeIn(credits), run_time=0.4)
        
        # Subtle pulsing effect on logo
        self.play(
            logo_text.animate.scale(1.05),
            rate_func=there_and_back,
            run_time=1
        )
        
        self.wait(2)
        
        # Final fade out
        self.play(
            FadeOut(logo_text),
            FadeOut(tagline),
            FadeOut(github),
            FadeOut(try_text),
            FadeOut(credits),
            run_time=2
        )
        
        # Thank you
        thanks = Text("Thank you for watching!", font_size=48, color=CYAN_ACCENT)
        self.play(FadeIn(thanks, scale=0.8), run_time=1)
        self.wait(2)
        self.play(FadeOut(thanks), run_time=1)
