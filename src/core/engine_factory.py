from core.interfaces import IEngine, ITestStrategy
from test_strategies.latency_strategy import LatencyStrategy
from test_strategies.stress_strategy import StressStrategy
from engines.simple_engine_driver import SimpleEngineDriver
from plugins.metric_reporter import MetricReporterPlugin
from typing import Type, Dict, List, Any

class FactoryRegistry:
    """Unified factory for creating engines, strategies, and managing plugins."""
    
    def __init__(self):
        self._engines: Dict[str, Type[IEngine]] = {}
        self._drivers: Dict[str, Type[SimpleEngineDriver]] = {}
        self._strategies: Dict[str, Type[ITestStrategy]] = {
            "latency": LatencyStrategy,
            "stress": StressStrategy
        }

    def register_engine(self, engine_class: Type[IEngine]):
        """Registers a new engine class."""
        engine_name = engine_class.name.fget(None)
        if engine_name in self._engines:
            raise ValueError(f"Engine '{engine_name}' already registered.")
        self._engines[engine_name] = engine_class
        print(f"Registered Engine: {engine_name}")

    def register_driver(self, name: str, driver_class: Type[SimpleEngineDriver]):
        """Register a new trading engine driver."""
        self._drivers[name] = driver_class
        print(f"Registered Driver: {name}")

    def register_strategy(self, test_type: str, strategy_class: Type[ITestStrategy]):
        """Register a new test strategy."""
        self._strategies[test_type] = strategy_class
        print(f"Registered Strategy: {test_type}")

    def create_engine(self, engine_name: str) -> IEngine:
        """Creates and returns an instance of the requested engine."""
        engine_class = self._engines.get(engine_name)
        if not engine_class:
            raise ValueError(f"Unknown engine: {engine_name}")
        return engine_class()

    def create_driver_config(self, engine_name: str) -> SimpleEngineDriver:
        """Factory method to configure and return the driver instance."""
        driver_class = self._drivers.get(engine_name)
        if not driver_class:
            raise ValueError(f"Unknown engine driver: {engine_name}")
        return driver_class(name=f"driver_{engine_name}", engine_name=engine_name)

    def create_strategy_instance(self, test_type: str) -> ITestStrategy:
        """Factory method to return a strategy instance."""
        strategy_class = self._strategies.get(test_type)
        if not strategy_class:
            raise ValueError(f"Unknown test type strategy: {test_type}")
        return strategy_class()

    def get_registered_engines(self) -> List[str]:
        return list(self._engines.keys())

    def get_registered_drivers(self) -> List[str]:
        return list(self._drivers.keys())

    def get_plugins_config(self) -> Dict[str, Any]:
        """Helper method to pass plugin configuration to Testplan's main function."""
        return {"plugins": [MetricReporterPlugin]}

# Global Factory Instance
FACTORY = FactoryRegistry()

# --- Initial Registration ---
FACTORY.register_driver("AlphaEngine", SimpleEngineDriver)
FACTORY.register_driver("BetaEngine", SimpleEngineDriver)
