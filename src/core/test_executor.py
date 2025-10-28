from core.interfaces import ITestStrategy, IEngine, IPlugin
from typing import Dict, Any, List

class TestExecutor:
    """The Context that uses the Strategy and manages Plugins."""
    def __init__(self, strategy: ITestStrategy, plugins: List[IPlugin] = None):
        self._strategy = strategy
        self._plugins = plugins if plugins is not None else []

    def set_strategy(self, strategy: ITestStrategy):
        """Allows runtime strategy change."""
        self._strategy = strategy

    def execute_test(self, engine: IEngine, iterations: int) -> Dict[str, Any]:
        """Executes the test using the current strategy and notifies plugins."""
        
        # Notify plugins of test start
        for plugin in self._plugins:
            plugin.on_test_start(engine.name, self._strategy.test_type)

        print(f"Executing {self._strategy.test_type} test on {engine.name}...")
        
        # Run the test
        results = self._strategy.execute_test(engine, iterations)
        
        # Notify plugins of test completion
        for plugin in self._plugins:
            plugin.on_test_complete(results)
            
        return results
