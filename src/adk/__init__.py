"""
ADK - Agent Development Kit Package
A playground environment for experimenting with Google Agent Development Kit
"""

__version__ = "0.1.0"
__author__ = "Karl Godtliebsen"

from .config import Config
from .agents import BaseAgent
from .utils import setup_logging

__all__ = ["Config", "BaseAgent", "setup_logging"]