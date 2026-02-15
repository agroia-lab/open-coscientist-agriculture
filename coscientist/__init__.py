"""Open CoScientist Agents - Multi-agent system for AI co-scientist research."""

__version__ = "0.0.1"


def __getattr__(name):
    """Lazy imports to avoid loading heavy LLM dependencies at package import time."""
    if name == "CoscientistConfig":
        from coscientist.framework import CoscientistConfig

        return CoscientistConfig
    elif name == "CoscientistFramework":
        from coscientist.framework import CoscientistFramework

        return CoscientistFramework
    elif name == "CoscientistState":
        from coscientist.global_state import CoscientistState

        return CoscientistState
    elif name == "CoscientistStateManager":
        from coscientist.global_state import CoscientistStateManager

        return CoscientistStateManager
    raise AttributeError(f"module 'coscientist' has no attribute {name!r}")
