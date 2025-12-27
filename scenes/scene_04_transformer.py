"""
Scene 4: Transformer Architecture
Deep dive into the GPT model components: RoPE, Attention, MLP, etc.
"""

from manim import *
try:
    from .common import *
except ImportError:
    from common import *
import numpy as np


class TransformerScene(Scene):
    """Deep dive into the Transformer architecture."""
    
    def construct(self):
        configure_scene(self)
        
        # Part 1: High-level structure
        self.play_high_level_structure()
        
        # Part 2: Token embeddings
        self.play_token_embeddings()
        
        # Part 3: Rotary Position Embeddings
        self.play_rope()
        
        # Part 4: Attention mechanism
        self.play_attention()
        
        # Part 5: MLP with ReLU²
        self.play_mlp()
        
        # Part 6: Full block assembly
        self.play_full_block()
    
    def play_high_level_structure(self):
        """Show the high-level transformer structure."""
        
        title = Text("Transformer Architecture", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Model config
        config_text = VGroup(
            Text("d20 Model Configuration:", font_size=28, color=TEXT_WHITE),
            Text("• n_layer = 20 (depth)", font_size=22, color=TEXT_GRAY),
            Text("• n_embd = 1280 (model dimension)", font_size=22, color=TEXT_GRAY),
            Text("• n_head = 10 (query heads)", font_size=22, color=TEXT_GRAY),
            Text("• sequence_len = 2048", font_size=22, color=TEXT_GRAY),
            Text("• vocab_size = 65,536", font_size=22, color=TEXT_GRAY),
        )
        config_text.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        config_text.move_to(LEFT * 3)
        
        # Visual transformer stack
        blocks = VGroup()
        
        for i in range(6):
            block = RoundedRectangle(
                corner_radius=0.1,
                width=2.5,
                height=0.5,
                fill_color=BLUE_PRIMARY if i < 5 else PURPLE_PRIMARY,
                fill_opacity=0.4,
                stroke_color=BLUE_PRIMARY if i < 5 else PURPLE_PRIMARY,
                stroke_width=2
            )
            label = Text(f"Block {i+1}" if i < 5 else "Block 20", font_size=18, color=TEXT_WHITE)
            label.move_to(block.get_center())
            group = VGroup(block, label)
            blocks.add(group)
        
        # Add dots for hidden blocks
        dots = Text("⋮", font_size=36, color=TEXT_GRAY)
        
        # Arrange
        blocks[:3].arrange(DOWN, buff=0.15)
        blocks[:3].move_to(RIGHT * 2.5 + UP * 1.5)
        
        dots.next_to(blocks[2], DOWN, buff=0.2)
        
        blocks[3:].arrange(DOWN, buff=0.15)
        blocks[3:].next_to(dots, DOWN, buff=0.2)
        
        # Input/Output labels
        input_label = Text("Token IDs", font_size=22, color=GREEN_ACCENT)
        input_label.next_to(blocks[0], UP, buff=0.3)
        input_arrow = Arrow(input_label.get_bottom(), blocks[0].get_top(), color=GREEN_ACCENT, buff=0.1)
        
        output_label = Text("Logits", font_size=22, color=ORANGE_ACCENT)
        output_label.next_to(blocks[-1], DOWN, buff=0.3)
        output_arrow = Arrow(blocks[-1].get_bottom(), output_label.get_top(), color=ORANGE_ACCENT, buff=0.1)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        for line in config_text:
            self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.2)
        
        self.play(FadeIn(input_label), GrowArrow(input_arrow), run_time=0.4)
        
        for block in blocks[:3]:
            self.play(FadeIn(block, shift=DOWN * 0.2), run_time=0.2)
        
        self.play(FadeIn(dots), run_time=0.2)
        
        for block in blocks[3:]:
            self.play(FadeIn(block, shift=DOWN * 0.2), run_time=0.2)
        
        self.play(GrowArrow(output_arrow), FadeIn(output_label), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(config_text),
            FadeOut(blocks),
            FadeOut(dots),
            FadeOut(input_label),
            FadeOut(input_arrow),
            FadeOut(output_label),
            FadeOut(output_arrow),
            run_time=1
        )
    
    def play_token_embeddings(self):
        """Show token embedding lookup."""
        
        title = Text("Token Embeddings", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Token IDs
        token_ids = [15496, 11, 995]
        token_boxes = VGroup()
        
        for tid in token_ids:
            box = TokenBox(str(tid), color=BLUE_PRIMARY, font_size=28)
            token_boxes.add(box)
        
        token_boxes.arrange(RIGHT, buff=0.3)
        token_boxes.move_to(UP * 2)
        
        # Arrow down
        arrow = Arrow(UP * 1.2, UP * 0.2, color=CYAN_ACCENT, stroke_width=3)
        
        # Embedding matrix (visual representation)
        embed_label = Text("Embedding Matrix", font_size=24, color=TEXT_WHITE)
        embed_label.move_to(DOWN * 0.3)
        
        matrix_visual = VGroup()
        for i in range(3):
            row = VGroup()
            # Show a vector representation
            for j in range(8):
                val = np.random.randn() * 0.5
                color = BLUE_PRIMARY if val > 0 else PURPLE_PRIMARY
                cell = Square(
                    side_length=0.25,
                    fill_color=color,
                    fill_opacity=abs(val),
                    stroke_width=0.5,
                    stroke_color=TEXT_DIM
                )
                row.add(cell)
            row.arrange(RIGHT, buff=0.02)
            matrix_visual.add(row)
        
        matrix_visual.arrange(DOWN, buff=0.1)
        matrix_visual.move_to(DOWN * 1.3)
        
        dim_label = Text("1280 dimensions", font_size=18, color=TEXT_GRAY)
        dim_label.next_to(matrix_visual, RIGHT, buff=0.3)
        
        dots = Text("...", font_size=24, color=TEXT_GRAY)
        dots.next_to(matrix_visual, RIGHT, buff=0.05)
        
        # Explanation
        explanation = Text(
            "Each token ID → lookup → 1280-dimensional vector",
            font_size=24,
            color=TEXT_GRAY
        )
        explanation.to_edge(DOWN, buff=1)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        for box in token_boxes:
            self.play(FadeIn(box, scale=0.8), run_time=0.2)
        
        self.play(GrowArrow(arrow), run_time=0.3)
        self.play(FadeIn(embed_label), run_time=0.3)
        self.play(FadeIn(matrix_visual), run_time=0.5)
        self.play(FadeIn(dots), FadeIn(dim_label), run_time=0.3)
        self.play(FadeIn(explanation), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(token_boxes),
            FadeOut(arrow),
            FadeOut(embed_label),
            FadeOut(matrix_visual),
            FadeOut(dots),
            FadeOut(dim_label),
            FadeOut(explanation),
            run_time=1
        )
    
    def play_rope(self):
        """Visualize Rotary Position Embeddings."""
        
        title = Text("Rotary Position Embeddings (RoPE)", font_size=44, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Concept explanation
        concept = Text(
            "Encode position by rotating embedding pairs",
            font_size=28,
            color=TEXT_WHITE
        )
        concept.next_to(title, DOWN, buff=0.5)
        
        # Create a 2D rotation visualization
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            axis_config={"color": TEXT_DIM},
        )
        axes.move_to(LEFT * 2.5)
        
        # Original vector
        original_vec = Arrow(
            axes.c2p(0, 0),
            axes.c2p(1.5, 0.5),
            color=BLUE_PRIMARY,
            stroke_width=4,
            buff=0
        )
        original_label = Text("x", font_size=24, color=BLUE_PRIMARY)
        original_label.next_to(original_vec.get_end(), UR, buff=0.1)
        
        # Rotated vectors for different positions
        angles = [0.3, 0.6, 0.9]
        colors = [GREEN_ACCENT, ORANGE_ACCENT, RED_ACCENT]
        rotated_vecs = VGroup()
        pos_labels = VGroup()
        
        for i, (angle, color) in enumerate(zip(angles, colors)):
            # Rotate the vector
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            x, y = 1.5, 0.5
            new_x = x * cos_a - y * sin_a
            new_y = x * sin_a + y * cos_a
            
            vec = Arrow(
                axes.c2p(0, 0),
                axes.c2p(new_x, new_y),
                color=color,
                stroke_width=3,
                buff=0
            )
            label = Text(f"pos={i+1}", font_size=18, color=color)
            label.next_to(vec.get_end(), UR, buff=0.1)
            
            rotated_vecs.add(vec)
            pos_labels.add(label)
        
        # Formula
        formula = MathTex(
            r"y_1 = x_1 \cos\theta - x_2 \sin\theta",
            font_size=32,
            color=TEXT_WHITE
        )
        formula.move_to(RIGHT * 2.5 + UP * 0.5)
        
        formula2 = MathTex(
            r"y_2 = x_1 \sin\theta + x_2 \cos\theta",
            font_size=32,
            color=TEXT_WHITE
        )
        formula2.next_to(formula, DOWN, buff=0.3)
        
        theta_text = Text("θ depends on position", font_size=24, color=CYAN_ACCENT)
        theta_text.next_to(formula2, DOWN, buff=0.4)
        
        # Key insight
        key_insight = Text(
            "Relative position = angle difference between Q and K",
            font_size=24,
            color=GREEN_ACCENT
        )
        key_insight.to_edge(DOWN, buff=0.8)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(concept), run_time=0.4)
        
        self.play(Create(axes), run_time=0.5)
        self.play(GrowArrow(original_vec), FadeIn(original_label), run_time=0.4)
        
        for vec, label in zip(rotated_vecs, pos_labels):
            self.play(GrowArrow(vec), FadeIn(label), run_time=0.3)
        
        self.play(FadeIn(formula), run_time=0.4)
        self.play(FadeIn(formula2), run_time=0.4)
        self.play(FadeIn(theta_text), run_time=0.3)
        
        self.play(FadeIn(key_insight, shift=UP * 0.2), run_time=0.5)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(concept),
            FadeOut(axes),
            FadeOut(original_vec),
            FadeOut(original_label),
            FadeOut(rotated_vecs),
            FadeOut(pos_labels),
            FadeOut(formula),
            FadeOut(formula2),
            FadeOut(theta_text),
            FadeOut(key_insight),
            run_time=1
        )
    
    def play_attention(self):
        """Visualize the attention mechanism with QK norm and GQA."""
        
        title = Text("Causal Self-Attention", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # QKV projections
        qkv_group = VGroup()
        
        for name, color in [("Query (Q)", BLUE_PRIMARY), ("Key (K)", GREEN_ACCENT), ("Value (V)", ORANGE_ACCENT)]:
            box = RoundedRectangle(
                corner_radius=0.1,
                width=1.8,
                height=0.7,
                fill_color=color,
                fill_opacity=0.3,
                stroke_color=color,
                stroke_width=2
            )
            label = Text(name, font_size=20, color=TEXT_WHITE)
            label.move_to(box.get_center())
            qkv_group.add(VGroup(box, label))
        
        qkv_group.arrange(RIGHT, buff=0.5)
        qkv_group.next_to(title, DOWN, buff=0.8)
        
        # Input arrow
        input_box = TokenBox("x", color=TEXT_DIM, font_size=24)
        input_box.next_to(qkv_group, LEFT, buff=0.8)
        
        arrows_to_qkv = VGroup()
        for box in qkv_group:
            arrow = Arrow(input_box.get_right(), box.get_left(), color=TEXT_DIM, buff=0.1, stroke_width=2)
            arrows_to_qkv.add(arrow)
        
        # QK Norm annotation
        qk_norm_label = Text("+ RMSNorm (QK Norm)", font_size=18, color=CYAN_ACCENT)
        qk_norm_label.next_to(qkv_group[:2], DOWN, buff=0.2)
        
        # Attention matrix
        attention_title = Text("Attention Weights (causal mask)", font_size=24, color=TEXT_WHITE)
        attention_title.move_to(DOWN * 0.5)
        
        # Create causal attention matrix
        matrix_size = 5
        attention_matrix = VGroup()
        
        for i in range(matrix_size):
            for j in range(matrix_size):
                if j <= i:  # Causal mask
                    opacity = 0.3 + 0.7 * np.random.random()
                    color = BLUE_PRIMARY
                else:
                    opacity = 0
                    color = TEXT_DIM
                
                cell = Square(
                    side_length=0.35,
                    fill_color=color,
                    fill_opacity=opacity,
                    stroke_color=TEXT_DIM,
                    stroke_width=0.5
                )
                cell.move_to(RIGHT * (j - 2) * 0.4 + DOWN * (i - 2) * 0.4)
                attention_matrix.add(cell)
        
        attention_matrix.move_to(DOWN * 1.8)
        
        # GQA note
        gqa_note = Text(
            "Group Query Attention: n_kv_head can be < n_head for efficiency",
            font_size=20,
            color=GREEN_ACCENT
        )
        gqa_note.to_edge(DOWN, buff=0.8)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        self.play(FadeIn(input_box), run_time=0.3)
        
        for arrow, box in zip(arrows_to_qkv, qkv_group):
            self.play(GrowArrow(arrow), FadeIn(box), run_time=0.25)
        
        self.play(FadeIn(qk_norm_label), run_time=0.3)
        self.play(FadeIn(attention_title), run_time=0.3)
        
        # Animate matrix appearing row by row
        for i in range(matrix_size):
            row_cells = attention_matrix[i*matrix_size:(i+1)*matrix_size]
            self.play(FadeIn(row_cells), run_time=0.15)
        
        self.play(FadeIn(gqa_note), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(qkv_group),
            FadeOut(input_box),
            FadeOut(arrows_to_qkv),
            FadeOut(qk_norm_label),
            FadeOut(attention_title),
            FadeOut(attention_matrix),
            FadeOut(gqa_note),
            run_time=1
        )
    
    def play_mlp(self):
        """Visualize the MLP with ReLU² activation."""
        
        title = Text("MLP with ReLU² Activation", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # MLP structure
        input_box = RoundedRectangle(
            corner_radius=0.1, width=1.5, height=0.8,
            fill_color=BLUE_PRIMARY, fill_opacity=0.3,
            stroke_color=BLUE_PRIMARY, stroke_width=2
        )
        input_label = Text("x", font_size=24, color=TEXT_WHITE)
        input_label.move_to(input_box.get_center())
        input_group = VGroup(input_box, input_label)
        input_group.move_to(LEFT * 4.5)
        
        # Expansion
        expand_box = RoundedRectangle(
            corner_radius=0.1, width=2.5, height=1.2,
            fill_color=PURPLE_PRIMARY, fill_opacity=0.3,
            stroke_color=PURPLE_PRIMARY, stroke_width=2
        )
        expand_label = Text("Linear\n4× expand", font_size=18, color=TEXT_WHITE)
        expand_label.move_to(expand_box.get_center())
        expand_group = VGroup(expand_box, expand_label)
        expand_group.move_to(LEFT * 1.5)
        
        # ReLU²
        relu_box = RoundedRectangle(
            corner_radius=0.1, width=1.5, height=0.8,
            fill_color=GREEN_ACCENT, fill_opacity=0.3,
            stroke_color=GREEN_ACCENT, stroke_width=2
        )
        relu_label = Text("ReLU²", font_size=20, color=TEXT_WHITE)
        relu_label.move_to(relu_box.get_center())
        relu_group = VGroup(relu_box, relu_label)
        relu_group.move_to(RIGHT * 1)
        
        # Projection
        proj_box = RoundedRectangle(
            corner_radius=0.1, width=1.8, height=0.8,
            fill_color=ORANGE_ACCENT, fill_opacity=0.3,
            stroke_color=ORANGE_ACCENT, stroke_width=2
        )
        proj_label = Text("Linear\nproject", font_size=18, color=TEXT_WHITE)
        proj_label.move_to(proj_box.get_center())
        proj_group = VGroup(proj_box, proj_label)
        proj_group.move_to(RIGHT * 3.5)
        
        # Arrows
        arrow1 = Arrow(input_group.get_right(), expand_group.get_left(), color=TEXT_DIM, buff=0.1)
        arrow2 = Arrow(expand_group.get_right(), relu_group.get_left(), color=TEXT_DIM, buff=0.1)
        arrow3 = Arrow(relu_group.get_right(), proj_group.get_left(), color=TEXT_DIM, buff=0.1)
        
        mlp_group = VGroup(input_group, expand_group, relu_group, proj_group, arrow1, arrow2, arrow3)
        mlp_group.move_to(UP * 0.5)
        
        # ReLU² visualization
        relu_title = Text("ReLU²(x) = max(0, x)²", font_size=28, color=TEXT_WHITE)
        relu_title.move_to(DOWN * 1)
        
        # Plot ReLU²
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[0, 4, 1],
            x_length=4,
            y_length=2.5,
            axis_config={"color": TEXT_DIM, "include_tip": False},
        )
        axes.move_to(DOWN * 2.5)
        
        # ReLU² curve
        relu_sq_graph = axes.plot(
            lambda x: max(0, x)**2,
            x_range=[-2, 2],
            color=GREEN_ACCENT,
            stroke_width=3
        )
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        self.play(FadeIn(input_group), run_time=0.3)
        self.play(GrowArrow(arrow1), FadeIn(expand_group), run_time=0.3)
        self.play(GrowArrow(arrow2), FadeIn(relu_group), run_time=0.3)
        self.play(GrowArrow(arrow3), FadeIn(proj_group), run_time=0.3)
        
        self.play(FadeIn(relu_title), run_time=0.4)
        self.play(Create(axes), run_time=0.4)
        self.play(Create(relu_sq_graph), run_time=0.6)
        
        # Why ReLU²?
        why_text = Text("Smoother than ReLU, better gradient flow", font_size=22, color=TEXT_GRAY)
        why_text.to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(why_text), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(title),
            FadeOut(mlp_group),
            FadeOut(relu_title),
            FadeOut(axes),
            FadeOut(relu_sq_graph),
            FadeOut(why_text),
            run_time=1
        )
    
    def play_full_block(self):
        """Show how attention and MLP combine in a block."""
        
        title = Text("Transformer Block", font_size=48, color=CYAN_ACCENT)
        title.to_edge(UP, buff=0.6)
        
        # Block diagram
        input_label = Text("x", font_size=28, color=TEXT_WHITE)
        input_label.move_to(LEFT * 4 + UP * 1)
        
        # Pre-norm + Attention
        norm1 = RoundedRectangle(
            corner_radius=0.1, width=1.5, height=0.6,
            fill_color=TEXT_DIM, fill_opacity=0.3,
            stroke_color=TEXT_DIM, stroke_width=2
        )
        norm1_label = Text("Norm", font_size=18, color=TEXT_WHITE)
        norm1_label.move_to(norm1.get_center())
        norm1_group = VGroup(norm1, norm1_label)
        norm1_group.move_to(LEFT * 2 + UP * 1)
        
        attn_box = RoundedRectangle(
            corner_radius=0.1, width=2, height=0.8,
            fill_color=BLUE_PRIMARY, fill_opacity=0.3,
            stroke_color=BLUE_PRIMARY, stroke_width=2
        )
        attn_label = Text("Attention", font_size=20, color=TEXT_WHITE)
        attn_label.move_to(attn_box.get_center())
        attn_group = VGroup(attn_box, attn_label)
        attn_group.move_to(RIGHT * 0.5 + UP * 1)
        
        # Residual symbol
        add1 = Circle(radius=0.25, color=GREEN_ACCENT, stroke_width=2)
        add1_label = Text("+", font_size=24, color=GREEN_ACCENT)
        add1_label.move_to(add1.get_center())
        add1_group = VGroup(add1, add1_label)
        add1_group.move_to(RIGHT * 2.5 + UP * 1)
        
        # Second branch
        norm2 = RoundedRectangle(
            corner_radius=0.1, width=1.5, height=0.6,
            fill_color=TEXT_DIM, fill_opacity=0.3,
            stroke_color=TEXT_DIM, stroke_width=2
        )
        norm2_label = Text("Norm", font_size=18, color=TEXT_WHITE)
        norm2_label.move_to(norm2.get_center())
        norm2_group = VGroup(norm2, norm2_label)
        norm2_group.move_to(LEFT * 2 + DOWN * 1)
        
        mlp_box = RoundedRectangle(
            corner_radius=0.1, width=2, height=0.8,
            fill_color=PURPLE_PRIMARY, fill_opacity=0.3,
            stroke_color=PURPLE_PRIMARY, stroke_width=2
        )
        mlp_label = Text("MLP", font_size=20, color=TEXT_WHITE)
        mlp_label.move_to(mlp_box.get_center())
        mlp_group = VGroup(mlp_box, mlp_label)
        mlp_group.move_to(RIGHT * 0.5 + DOWN * 1)
        
        add2 = Circle(radius=0.25, color=GREEN_ACCENT, stroke_width=2)
        add2_label = Text("+", font_size=24, color=GREEN_ACCENT)
        add2_label.move_to(add2.get_center())
        add2_group = VGroup(add2, add2_label)
        add2_group.move_to(RIGHT * 2.5 + DOWN * 1)
        
        output_label = Text("y", font_size=28, color=TEXT_WHITE)
        output_label.move_to(RIGHT * 4 + DOWN * 1)
        
        # Arrows
        arrows = VGroup(
            Arrow(input_label.get_right(), norm1_group.get_left(), color=TEXT_DIM, buff=0.1, stroke_width=2),
            Arrow(norm1_group.get_right(), attn_group.get_left(), color=TEXT_DIM, buff=0.1, stroke_width=2),
            Arrow(attn_group.get_right(), add1_group.get_left(), color=TEXT_DIM, buff=0.1, stroke_width=2),
            Arrow(add1_group.get_bottom(), norm2_group.get_left(), color=TEXT_DIM, buff=0.1, stroke_width=2),
            Arrow(norm2_group.get_right(), mlp_group.get_left(), color=TEXT_DIM, buff=0.1, stroke_width=2),
            Arrow(mlp_group.get_right(), add2_group.get_left(), color=TEXT_DIM, buff=0.1, stroke_width=2),
            Arrow(add2_group.get_right(), output_label.get_left(), color=TEXT_DIM, buff=0.1, stroke_width=2),
        )
        
        # Skip connections (curved)
        skip1 = ArcBetweenPoints(
            input_label.get_right() + DOWN * 0.5,
            add1_group.get_top(),
            angle=-TAU/6,
            color=GREEN_ACCENT,
            stroke_width=2
        )
        
        skip2 = ArcBetweenPoints(
            add1_group.get_bottom() + LEFT * 0.5,
            add2_group.get_top(),
            angle=-TAU/6,
            color=GREEN_ACCENT,
            stroke_width=2
        )
        
        # Code snippet
        code_text = Text(
            "x = x + attn(norm(x))\nx = x + mlp(norm(x))",
            font_size=22,
            color=TEXT_GRAY
        )
        code_text.to_edge(DOWN, buff=0.8)
        
        # Animate
        self.play(Write(title), run_time=0.8)
        
        self.play(FadeIn(input_label), run_time=0.2)
        self.play(GrowArrow(arrows[0]), FadeIn(norm1_group), run_time=0.25)
        self.play(GrowArrow(arrows[1]), FadeIn(attn_group), run_time=0.25)
        self.play(GrowArrow(arrows[2]), FadeIn(add1_group), run_time=0.25)
        self.play(Create(skip1), run_time=0.3)
        
        self.play(GrowArrow(arrows[3]), FadeIn(norm2_group), run_time=0.25)
        self.play(GrowArrow(arrows[4]), FadeIn(mlp_group), run_time=0.25)
        self.play(GrowArrow(arrows[5]), FadeIn(add2_group), run_time=0.25)
        self.play(GrowArrow(arrows[6]), FadeIn(output_label), run_time=0.25)
        self.play(Create(skip2), run_time=0.3)
        
        self.play(FadeIn(code_text), run_time=0.4)
        
        self.wait(2)
        
        # Final transition
        self.play(
            FadeOut(title),
            FadeOut(input_label),
            FadeOut(norm1_group),
            FadeOut(attn_group),
            FadeOut(add1_group),
            FadeOut(norm2_group),
            FadeOut(mlp_group),
            FadeOut(add2_group),
            FadeOut(output_label),
            FadeOut(arrows),
            FadeOut(skip1),
            FadeOut(skip2),
            FadeOut(code_text),
            run_time=1
        )
