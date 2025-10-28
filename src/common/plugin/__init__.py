from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Any, Dict
from testplan.common.config import Config

class RuntimeType(Enum):
    """Defines when a plugin should be executed in the test lifecycle."""
    MAIN = auto()      # Run in main process
    WORKER = auto()    # Run in worker processes
    BOTH = auto()      # Run in both main and worker processes

class BasePluginConfig(Config):
    @classmethod
    def get_options(cls) -> Dict:
        """
        Returns the configuration options for the plugin.
        Must be implemented by subclasses.
        """
        return {}

class TestplanPlugin(ABC):
    """
    Base class for all Testplan plugins.
    Defines the interface that all plugins must implement.
    """
    name: str = None  # Plugin name, must be defined by subclasses
    runtime: RuntimeType = RuntimeType.MAIN  # Default runtime type
    cfg = BasePluginConfig  # Default config class
    
    def __init__(self, **options):
        self.cfg = self.__class__.cfg(**options)
        
    def on_test_start(self, engine_name: str, test_type: str) -> None:
        """Called when a test starts."""
        pass

    def on_test_complete(self, results: Dict[str, Any]) -> None:
        """Called when a test completes."""
        pass

    @abstractmethod
    def test_plan_result(self, result: Any) -> None:
        """
        Called when test plan execution is complete.
        
        Args:
            result: The test execution results
        """
        pass
