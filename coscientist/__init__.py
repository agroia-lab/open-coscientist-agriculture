"""Open CoScientist Agriculture - Multi-agent AI system for integrated weed management and precision farming research."""

__version__ = "0.1.0"


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
    elif name == "ResearchProfile":
        from coscientist.profiles import ResearchProfile

        return ResearchProfile
    raise AttributeError(f"module 'coscientist' has no attribute {name!r}")
