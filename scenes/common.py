"""
Common utilities and styling for the NanoChat Manim video.
Follows 3Blue1Brown aesthetic.
"""

from manim import *
import numpy as np

# =============================================================================
# Color Palette (3Blue1Brown inspired)
# =============================================================================

# Primary colors
BLUE_PRIMARY = "#3b82f6"
PURPLE_PRIMARY = "#8b5cf6"
CYAN_ACCENT = "#06b6d4"
GREEN_ACCENT = "#10b981"
ORANGE_ACCENT = "#f59e0b"
RED_ACCENT = "#ef4444"
PINK_ACCENT = "#ec4899"

# Background colors
DARK_BG = "#0f172a"
SLATE_BG = "#1e293b"
CARD_BG = "#334155"

# Text colors
TEXT_WHITE = "#f8fafc"
TEXT_GRAY = "#94a3b8"
TEXT_DIM = "#64748b"

# Gradient colors for transitions
GRADIENT_START = "#3b82f6"
GRADIENT_END = "#8b5cf6"

# =============================================================================
# Custom Manim Configuration
# =============================================================================

def configure_scene(scene):
    """Apply consistent styling to a scene."""
    scene.camera.background_color = DARK_BG


# =============================================================================
# Reusable Components
# =============================================================================

class CodeBlock(VGroup):
    """A styled code block with syntax highlighting appearance."""
    
    def __init__(self, code: str, language: str = "python", font_size: int = 24, **kwargs):
        super().__init__(**kwargs)
        
        # Background
        lines = code.strip().split('\n')
        height = len(lines) * 0.4 + 0.5
        width = max(len(line) for line in lines) * 0.15 + 1
        
        bg = RoundedRectangle(
            corner_radius=0.15,
            height=height,
            width=width,
            fill_color=CARD_BG,
            fill_opacity=0.9,
            stroke_color=TEXT_DIM,
            stroke_width=1
        )
        
        # Code text
        code_text = Code(
            code=code,
            language=language,
            font_size=font_size,
            background="rectangle",
            background_stroke_width=0,
            insert_line_no=False,
            style="monokai"
        )
        
        self.add(bg, code_text)
        self.bg = bg
        self.code = code_text


class AnimatedTitle(VGroup):
    """An animated title with underline effect."""
    
    def __init__(self, text: str, font_size: int = 72, color=TEXT_WHITE, **kwargs):
        super().__init__(**kwargs)
        
        title = Text(text, font_size=font_size, color=color, weight=BOLD)
        underline = Line(
            start=title.get_left() + DOWN * 0.3,
            end=title.get_right() + DOWN * 0.3,
            color=CYAN_ACCENT,
            stroke_width=4
        )
        
        self.add(title, underline)
        self.title = title
        self.underline = underline


class NeuronNode(VGroup):
    """A single neuron node for neural network visualizations."""
    
    def __init__(self, radius=0.2, color=BLUE_PRIMARY, **kwargs):
        super().__init__(**kwargs)
        
        outer = Circle(radius=radius, color=color, fill_opacity=0.3, stroke_width=2)
        inner = Circle(radius=radius * 0.4, color=color, fill_opacity=0.8, stroke_width=0)
        
        self.add(outer, inner)
        self.outer = outer
        self.inner = inner


class FlowArrow(VGroup):
    """An animated flow arrow for pipeline visualizations."""
    
    def __init__(self, start, end, color=CYAN_ACCENT, **kwargs):
        super().__init__(**kwargs)
        
        arrow = Arrow(
            start=start,
            end=end,
            color=color,
            buff=0.1,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15
        )
        
        self.add(arrow)
        self.arrow = arrow


class PipelineBox(VGroup):
    """A box representing a stage in the pipeline."""
    
    def __init__(self, text: str, color=BLUE_PRIMARY, width=2.5, height=1.2, **kwargs):
        super().__init__(**kwargs)
        
        box = RoundedRectangle(
            corner_radius=0.2,
            width=width,
            height=height,
            fill_color=color,
            fill_opacity=0.3,
            stroke_color=color,
            stroke_width=3
        )
        
        label = Text(text, font_size=28, color=TEXT_WHITE, weight=BOLD)
        label.move_to(box.get_center())
        
        self.add(box, label)
        self.box = box
        self.label = label


class MatrixGrid(VGroup):
    """A visual matrix representation for attention/weight visualizations."""
    
    def __init__(self, rows=4, cols=4, cell_size=0.5, colors=None, **kwargs):
        super().__init__(**kwargs)
        
        self.rows = rows
        self.cols = cols
        self.cells = []
        
        for i in range(rows):
            row_cells = []
            for j in range(cols):
                color = colors[i][j] if colors else BLUE_PRIMARY
                opacity = 0.3 + 0.7 * (1 - (i + j) / (rows + cols - 2)) if not colors else 0.7
                
                cell = Square(
                    side_length=cell_size,
                    fill_color=color,
                    fill_opacity=opacity,
                    stroke_color=TEXT_DIM,
                    stroke_width=1
                )
                cell.move_to([j * cell_size - (cols - 1) * cell_size / 2,
                              -i * cell_size + (rows - 1) * cell_size / 2, 0])
                
                row_cells.append(cell)
                self.add(cell)
            self.cells.append(row_cells)


class TokenBox(VGroup):
    """A token representation for tokenizer visualizations."""
    
    def __init__(self, text: str, color=BLUE_PRIMARY, font_size=24, **kwargs):
        super().__init__(**kwargs)
        
        label = Text(text, font_size=font_size, color=TEXT_WHITE)
        
        padding = 0.2
        box = RoundedRectangle(
            corner_radius=0.1,
            width=label.width + padding * 2,
            height=label.height + padding * 2,
            fill_color=color,
            fill_opacity=0.4,
            stroke_color=color,
            stroke_width=2
        )
        
        label.move_to(box.get_center())
        
        self.add(box, label)
        self.box = box
        self.label = label


class AnimatedCounter(VGroup):
    """An animated number counter for statistics."""
    
    def __init__(self, start=0, end=100, prefix="", suffix="", font_size=48, color=TEXT_WHITE, **kwargs):
        super().__init__(**kwargs)
        
        self.start = start
        self.end = end
        self.prefix = prefix
        self.suffix = suffix
        
        self.number = DecimalNumber(
            start,
            num_decimal_places=0,
            font_size=font_size,
            color=color
        )
        
        if prefix:
            self.prefix_text = Text(prefix, font_size=font_size, color=color)
            self.prefix_text.next_to(self.number, LEFT, buff=0.1)
            self.add(self.prefix_text)
        
        self.add(self.number)
        
        if suffix:
            self.suffix_text = Text(suffix, font_size=font_size, color=color)
            self.suffix_text.next_to(self.number, RIGHT, buff=0.1)
            self.add(self.suffix_text)


# =============================================================================
# Animation Helpers
# =============================================================================

def create_glow_effect(mobject, color=CYAN_ACCENT, opacity=0.3, scale=1.2):
    """Create a glow effect around a mobject."""
    glow = mobject.copy()
    glow.set_fill(color, opacity=opacity)
    glow.set_stroke(color, width=0)
    glow.scale(scale)
    return glow


def typing_animation(text_mobject, run_time=2):
    """Create a typing animation for text."""
    return AddTextLetterByLetter(text_mobject, run_time=run_time)


def pulse_animation(mobject, scale_factor=1.1, run_time=0.5):
    """Create a pulse animation."""
    return Succession(
        mobject.animate.scale(scale_factor),
        mobject.animate.scale(1/scale_factor),
        run_time=run_time
    )


def wave_in(mobject, direction=UP, amplitude=0.5):
    """Create a wave-in animation."""
    return mobject.animate.shift(direction * amplitude).set_opacity(1)


# =============================================================================
# Math Helpers
# =============================================================================

def create_attention_weights(seq_len, causal=True):
    """Create attention weight matrix for visualization."""
    weights = np.random.rand(seq_len, seq_len)
    if causal:
        mask = np.triu(np.ones((seq_len, seq_len)), k=1)
        weights = np.where(mask, 0, weights)
    # Normalize rows
    weights = weights / weights.sum(axis=1, keepdims=True)
    return weights


def softmax(x):
    """Compute softmax values."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()
