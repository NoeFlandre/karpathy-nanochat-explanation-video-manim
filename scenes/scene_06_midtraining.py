"""
Scene 6: Midtraining
Teaching the model conversation format, tool use, and identity.
"""

from manim import *
try:
    from .common import *
except ImportError:
    from common import *


class MidtrainingScene(Scene):
    """Midtraining: bridging base model to chat model."""
    
    def construct(self):
        configure_scene(self)
        
        # Part 1: What is midtraining?
        self.play_midtraining_intro()
        
        # Part 2: Conversation format
        self.play_conversation_format()
        
        # Part 3: Tool use
        self.play_tool_use()
        
        # Part 4: Identity infusion
        self.play_identity_infusion()
    
    def play_midtraining_intro(self):
        """Introduction to midtraining."""
        
        title = Text("Midtraining", font_size=56, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Before/After comparison
        before_box = RoundedRectangle(
            corner_radius=0.15, width=4, height=2,
            fill_color=BLUE_PRIMARY, fill_opacity=0.2,
            stroke_color=BLUE_PRIMARY, stroke_width=2
        )
        before_title = Text("Base Model", font_size=24, color=BLUE_PRIMARY, weight=BOLD)
        before_title.next_to(before_box, UP, buff=0.1)
        
        before_text = Text(
            "Predicts next token\nNo conversation structure\nNo special abilities",
            font_size=18,
            color=TEXT_GRAY
        )
        before_text.move_to(before_box.get_center())
        before_group = VGroup(before_box, before_title, before_text)
        before_group.move_to(LEFT * 3)
        
        after_box = RoundedRectangle(
            corner_radius=0.15, width=4, height=2,
            fill_color=GREEN_ACCENT, fill_opacity=0.2,
            stroke_color=GREEN_ACCENT, stroke_width=2
        )
        after_title = Text("After Midtraining", font_size=24, color=GREEN_ACCENT, weight=BOLD)
        after_title.next_to(after_box, UP, buff=0.1)
        
        after_text = Text(
            "Understands conversations\nKnows special tokens\nCan use tools",
            font_size=18,
            color=TEXT_GRAY
        )
        after_text.move_to(after_box.get_center())
        after_group = VGroup(after_box, after_title, after_text)
        after_group.move_to(RIGHT * 3)
        
        # Arrow
        arrow = Arrow(before_box.get_right(), after_box.get_left(), color=ORANGE_ACCENT, buff=0.2, stroke_width=3)
        arrow_label = Text("Midtraining", font_size=20, color=ORANGE_ACCENT)
        arrow_label.next_to(arrow, UP, buff=0.1)
        
        # Stats
        stats = Text(
            "~23K training examples • SmolTalk + Identity + Tasks",
            font_size=22,
            color=TEXT_GRAY
        )
        stats.to_edge(DOWN, buff=0.8)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(before_group), run_time=0.5)
        self.play(GrowArrow(arrow), FadeIn(arrow_label), run_time=0.4)
        self.play(FadeIn(after_group), run_time=0.5)
        self.play(FadeIn(stats), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(before_group),
            FadeOut(after_group),
            FadeOut(arrow),
            FadeOut(arrow_label),
            FadeOut(stats),
            run_time=1
        )
    
    def play_conversation_format(self):
        """Show the conversation token format."""
        
        title = Text("Conversation Format", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Build a conversation example
        tokens = [
            ("<|bos|>", BLUE_PRIMARY, False),
            ("<|user_start|>", GREEN_ACCENT, False),
            ("Hello!", TEXT_WHITE, False),
            ("<|user_end|>", GREEN_ACCENT, False),
            ("<|assistant_start|>", PURPLE_PRIMARY, False),
            ("Hi there!", TEXT_WHITE, True),  # True = supervised
            ("<|assistant_end|>", PURPLE_PRIMARY, True),
        ]
        
        token_boxes = VGroup()
        
        for text, color, supervised in tokens:
            box = TokenBox(text, color=color, font_size=22)
            if supervised:
                # Add a green glow/border for supervised tokens
                glow = SurroundingRectangle(box, color=GREEN_ACCENT, buff=0.05, stroke_width=1)
                token_boxes.add(VGroup(box, glow))
            else:
                token_boxes.add(box)
        
        token_boxes.arrange(RIGHT, buff=0.15)
        token_boxes.scale(0.8)
        token_boxes.move_to(UP * 0.5)
        
        # Legend
        legend = VGroup()
        
        user_dot = Dot(color=GREEN_ACCENT, radius=0.1)
        user_label = Text("User", font_size=18, color=TEXT_GRAY)
        user_label.next_to(user_dot, RIGHT, buff=0.1)
        
        assistant_dot = Dot(color=PURPLE_PRIMARY, radius=0.1)
        assistant_label = Text("Assistant", font_size=18, color=TEXT_GRAY)
        assistant_label.next_to(assistant_dot, RIGHT, buff=0.1)
        
        supervised_dot = Dot(color=GREEN_ACCENT, radius=0.1)
        supervised_box = SurroundingRectangle(supervised_dot, color=GREEN_ACCENT, buff=0.02, stroke_width=1)
        supervised_label = Text("Supervised (train on this)", font_size=18, color=TEXT_GRAY)
        supervised_label.next_to(supervised_box, RIGHT, buff=0.1)
        
        legend.add(VGroup(user_dot, user_label))
        legend.add(VGroup(assistant_dot, assistant_label))
        legend.add(VGroup(supervised_dot, supervised_box, supervised_label))
        
        legend.arrange(RIGHT, buff=0.8)
        legend.move_to(DOWN * 1)
        
        # Explanation
        explanation = Text(
            "Model learns: given user message → generate assistant response",
            font_size=24,
            color=TEXT_WHITE
        )
        explanation.to_edge(DOWN, buff=0.8)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        for token in token_boxes:
            self.play(FadeIn(token, scale=0.9), run_time=0.15)
        
        self.play(FadeIn(legend), run_time=0.5)
        self.play(FadeIn(explanation), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(token_boxes),
            FadeOut(legend),
            FadeOut(explanation),
            run_time=1
        )
    
    def play_tool_use(self):
        """Show tool use with Python REPL."""
        
        title = Text("Tool Use: Python Calculator", font_size=44, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Example conversation with tool use
        conversation = [
            ("User:", "What is 123 × 456?", GREEN_ACCENT, LEFT * 4),
            ("Assistant:", "Let me calculate...", PURPLE_PRIMARY, LEFT * 2),
        ]
        
        messages = VGroup()
        
        for role, text, color, pos in conversation:
            role_text = Text(role, font_size=20, color=color, weight=BOLD)
            msg_text = Text(text, font_size=22, color=TEXT_WHITE)
            msg_text.next_to(role_text, RIGHT, buff=0.2)
            group = VGroup(role_text, msg_text)
            messages.add(group)
        
        messages.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        messages.move_to(UP * 1.5 + LEFT * 2)
        
        # Tool invocation
        tool_box = RoundedRectangle(
            corner_radius=0.1, width=5, height=1.5,
            fill_color=ORANGE_ACCENT, fill_opacity=0.2,
            stroke_color=ORANGE_ACCENT, stroke_width=2
        )
        tool_box.move_to(DOWN * 0.5)
        
        python_tokens = VGroup(
            TokenBox("<|python_start|>", color=ORANGE_ACCENT, font_size=18),
            TokenBox("123 * 456", color=TEXT_WHITE, font_size=18),
            TokenBox("<|python_end|>", color=ORANGE_ACCENT, font_size=18),
        )
        python_tokens.arrange(RIGHT, buff=0.1)
        python_tokens.move_to(tool_box.get_center() + UP * 0.3)
        
        output_tokens = VGroup(
            TokenBox("<|output_start|>", color=RED_ACCENT, font_size=18),
            TokenBox("56088", color=TEXT_WHITE, font_size=18),
            TokenBox("<|output_end|>", color=RED_ACCENT, font_size=18),
        )
        output_tokens.arrange(RIGHT, buff=0.1)
        output_tokens.move_to(tool_box.get_center() + DOWN * 0.3)
        
        # Arrow showing execution
        exec_arrow = Arrow(
            python_tokens.get_bottom() + DOWN * 0.1,
            output_tokens.get_top() + UP * 0.1,
            color=CYAN_ACCENT,
            buff=0.05,
            stroke_width=2
        )
        exec_label = Text("Python executes", font_size=16, color=CYAN_ACCENT)
        exec_label.next_to(exec_arrow, RIGHT, buff=0.1)
        
        # Final answer
        final_msg = VGroup(
            Text("Assistant:", font_size=20, color=PURPLE_PRIMARY, weight=BOLD),
            Text("The answer is 56,088", font_size=22, color=TEXT_WHITE)
        )
        final_msg[1].next_to(final_msg[0], RIGHT, buff=0.2)
        final_msg.move_to(DOWN * 2.5)
        
        # Key point
        key_point = Text(
            "Model learns when to invoke calculator for reliable math",
            font_size=22,
            color=GREEN_ACCENT
        )
        key_point.to_edge(DOWN, buff=0.5)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        for msg in messages:
            self.play(FadeIn(msg, shift=RIGHT * 0.2), run_time=0.3)
        
        self.play(FadeIn(tool_box), run_time=0.3)
        
        for token in python_tokens:
            self.play(FadeIn(token, scale=0.9), run_time=0.15)
        
        self.play(GrowArrow(exec_arrow), FadeIn(exec_label), run_time=0.4)
        
        for token in output_tokens:
            self.play(FadeIn(token, scale=0.9), run_time=0.15)
        
        self.play(FadeIn(final_msg, shift=UP * 0.2), run_time=0.4)
        self.play(FadeIn(key_point), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(messages),
            FadeOut(tool_box),
            FadeOut(python_tokens),
            FadeOut(output_tokens),
            FadeOut(exec_arrow),
            FadeOut(exec_label),
            FadeOut(final_msg),
            FadeOut(key_point),
            run_time=1
        )
    
    def play_identity_infusion(self):
        """Show how identity is infused into the model."""
        
        title = Text("Identity Infusion", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Example identity conversation
        conversation_box = RoundedRectangle(
            corner_radius=0.15, width=8, height=3,
            fill_color=PURPLE_PRIMARY, fill_opacity=0.15,
            stroke_color=PURPLE_PRIMARY, stroke_width=2
        )
        conversation_box.move_to(UP * 0.5)
        
        conv_title = Text("Example Identity Conversation", font_size=20, color=PURPLE_PRIMARY)
        conv_title.next_to(conversation_box, UP, buff=0.1)
        
        user_msg = Text('User: "Who are you?"', font_size=22, color=GREEN_ACCENT)
        user_msg.move_to(conversation_box.get_center() + UP * 0.7 + LEFT * 1)
        
        assistant_msg = VGroup(
            Text('Assistant: "I am nanochat, a small', font_size=22, color=PURPLE_PRIMARY),
            Text('language model created by Andrej Karpathy."', font_size=22, color=PURPLE_PRIMARY),
        )
        assistant_msg.arrange(DOWN, buff=0.1)
        assistant_msg.move_to(conversation_box.get_center() + DOWN * 0.3)
        
        # Synthetic data info
        synthetic_info = VGroup(
            Text("~1,000 synthetic identity conversations", font_size=22, color=TEXT_WHITE),
            Text("Generated with LLM assistance", font_size=18, color=TEXT_GRAY),
            Text("Mixed into training data", font_size=18, color=TEXT_GRAY),
        )
        synthetic_info.arrange(DOWN, buff=0.15)
        synthetic_info.move_to(DOWN * 2)
        
        # Customization note
        custom_note = Text(
            "✨ You can customize nanochat's personality by modifying these!",
            font_size=20,
            color=ORANGE_ACCENT
        )
        custom_note.to_edge(DOWN, buff=0.6)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(conversation_box), FadeIn(conv_title), run_time=0.4)
        self.play(FadeIn(user_msg, shift=RIGHT * 0.2), run_time=0.3)
        self.play(FadeIn(assistant_msg, shift=RIGHT * 0.2), run_time=0.4)
        
        for info in synthetic_info:
            self.play(FadeIn(info), run_time=0.25)
        
        self.play(FadeIn(custom_note, shift=UP * 0.2), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(conversation_box),
            FadeOut(conv_title),
            FadeOut(user_msg),
            FadeOut(assistant_msg),
            FadeOut(synthetic_info),
            FadeOut(custom_note),
            run_time=1
        )
