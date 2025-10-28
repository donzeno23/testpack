from abc import ABC, abstractmethod
from typing import Any, Dict
from testplan.common.entity import Resource
from testplan.testing.result import Result
from rich import print as rprint

# --- Single Responsibility: Engine Definition ---
class IEngine(ABC):
    """Interface for a Trading Engine (Engine SRP)."""
    @property
    @abstractmethod
    def name(self) -> str:
        """The unique name of the trading engine."""
        pass

    @abstractmethod
    def execute_trade(self, order: Dict[str, Any]) -> Any:
        """Simulates or executes a trade on the engine."""
        pass
    
    # ... potentially other setup/teardown methods

# --- Single Responsibility: Test Strategy Definition (Strategy Pattern) ---
# ITestStrategy adheres to SRP (Test Execution Algorithm) and Interface (ISP/Liskov)
class ITestStrategy(ABC):
    """
    Interface for performance test strategies (Latency, Stress, etc.).
    Adheres to Strategy Pattern and Liskov Substitution Principle.
    """

    @property
    @abstractmethod
    def test_type(self) -> str:
        """The type of test (e.g., 'latency', 'stress')."""
        pass

    @abstractmethod
    def execute_test(self, engine: IEngine, iterations: int = 1000) -> Dict[str, Any]:
    # def execute_test(self, engine: Resource, iterations: int = 1000) -> Dict[str, Any]:
        """
        Runs the specific test type against the given engine.
        Runs the specific test type algorithm against the engine driver.
        Returns raw metrics.
        """
        rprint(f"Executing test with {iterations} iterations")
        pass
    
    @abstractmethod
    def analyze_results(self, result_data: Dict[str, Any], testplan_result: Result):
        """
        Analyzes raw metrics and uses Testplan's result object for reporting/assertions.
        """
        rprint("Analyzing results and reporting to Testplan")
        pass

# ITradingEngine (Implicit Interface via the Driver) is defined in engines/


# --- Single Responsibility: Plugin Definition ---
class IPlugin(ABC):
    """Interface for a framework extension/plugin (Plugin SRP)."""
    @property
    @abstractmethod
    def name(self) -> str:
        """The unique name of the plugin."""
        pass
        
    @abstractmethod
    def on_test_start(self, engine_name: str, test_type: str):
        """Called before a test starts."""
        pass

    @abstractmethod
    def on_test_complete(self, results: Dict[str, Any]):
        """Called after a test completes with results."""
        pass
