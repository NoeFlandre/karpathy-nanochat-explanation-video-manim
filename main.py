#!/usr/bin/env python3
"""
NanoChat Manim Video
====================

A comprehensive 3Blue1Brown-style educational video explaining
Karpathy's nanochat repository - the $100 ChatGPT clone.

Usage:
    # Render full video (high quality)
    uv run manim -pqh main.py NanoChatVideo

    # Render full video (low quality for testing)
    uv run manim -pql main.py NanoChatVideo

    # Render a specific scene
    uv run manim -pql main.py IntroScene
    uv run manim -pql main.py TokenizerScene
    # etc.

    # Render all scenes separately
    uv run manim -pql main.py --write_all

"""

from manim import *

# Import all scenes
from scenes.scene_01_intro import IntroScene
from scenes.scene_02_architecture import ArchitectureScene
from scenes.scene_03_tokenizer import TokenizerScene
from scenes.scene_04_transformer import TransformerScene
from scenes.scene_05_base_training import BaseTrainingScene
from scenes.scene_06_midtraining import MidtrainingScene
from scenes.scene_07_sft import SFTScene
from scenes.scene_08_rl import RLScene
from scenes.scene_09_inference import InferenceScene
from scenes.scene_10_conclusion import ConclusionScene

from scenes.common import configure_scene


class NanoChatVideo(Scene):
    """
    Complete NanoChat explainer video.
    
    This scene combines all individual scenes into one continuous video.
    Estimated duration: ~28 minutes
    """
    
    def construct(self):
        configure_scene(self)
        
        # Scene 1: Introduction
        self.intro_scene()
        
        # Scene 2: Architecture Overview
        self.architecture_scene()
        
        # Scene 3: Tokenizer Deep Dive
        self.tokenizer_scene()
        
        # Scene 4: Transformer Architecture
        self.transformer_scene()
        
        # Scene 5: Base Training
        self.base_training_scene()
        
        # Scene 6: Midtraining
        self.midtraining_scene()
        
        # Scene 7: SFT
        self.sft_scene()
        
        # Scene 8: Reinforcement Learning
        self.rl_scene()
        
        # Scene 9: Inference Engine
        self.inference_scene()
        
        # Scene 10: Conclusion
        self.conclusion_scene()
    
    def intro_scene(self):
        """Scene 1: Introduction"""
        scene = IntroScene()
        scene.camera = self.camera
        scene.construct()
    
    def architecture_scene(self):
        """Scene 2: Architecture Overview"""
        scene = ArchitectureScene()
        scene.camera = self.camera
        scene.construct()
    
    def tokenizer_scene(self):
        """Scene 3: Tokenizer Deep Dive"""
        scene = TokenizerScene()
        scene.camera = self.camera
        scene.construct()
    
    def transformer_scene(self):
        """Scene 4: Transformer Architecture"""
        scene = TransformerScene()
        scene.camera = self.camera
        scene.construct()
    
    def base_training_scene(self):
        """Scene 5: Base Training"""
        scene = BaseTrainingScene()
        scene.camera = self.camera
        scene.construct()
    
    def midtraining_scene(self):
        """Scene 6: Midtraining"""
        scene = MidtrainingScene()
        scene.camera = self.camera
        scene.construct()
    
    def sft_scene(self):
        """Scene 7: SFT"""
        scene = SFTScene()
        scene.camera = self.camera
        scene.construct()
    
    def rl_scene(self):
        """Scene 8: Reinforcement Learning"""
        scene = RLScene()
        scene.camera = self.camera
        scene.construct()
    
    def inference_scene(self):
        """Scene 9: Inference Engine"""
        scene = InferenceScene()
        scene.camera = self.camera
        scene.construct()
    
    def conclusion_scene(self):
        """Scene 10: Conclusion"""
        scene = ConclusionScene()
        scene.camera = self.camera
        scene.construct()


# Export all scenes for individual rendering
__all__ = [
    "NanoChatVideo",
    "IntroScene",
    "ArchitectureScene",
    "TokenizerScene",
    "TransformerScene",
    "BaseTrainingScene",
    "MidtrainingScene",
    "SFTScene",
    "RLScene",
    "InferenceScene",
    "ConclusionScene",
]
