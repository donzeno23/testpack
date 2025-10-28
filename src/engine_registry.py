from core.engine_factory import FACTORY
from core.interfaces import ITestStrategy, IEngine, IPlugin
from engines.engine_a import ConcreteEngineA
# Import other engines as they are created
from test_types.latency_test import LatencyTest
# Import other test types/strategies
from plugins.data_reporter import DataReporterPlugin # Example plugin
from typing import Type, List, Dict

# Global map for which tests to run on which engine
# Key: Engine Name, Value: List of TestStrategy Instances
TEST_PLAN: Dict[str, List[ITestStrategy]] = {}
PLUGINS: List[IPlugin] = []

def register_engine_and_tests(engine_class: Type[IEngine], test_strategies: List[ITestStrategy]):
    """Registers an engine with the Factory and adds its test plan."""
    FACTORY.register_engine(engine_class)
    engine_name = engine_class.name.fget(None)
    TEST_PLAN[engine_name] = test_strategies
    print(f"Test plan set for {engine_name}: {[t.test_type for t in test_strategies]}")

def register_plugins(plugin_classes: List[Type[IPlugin]]):
    """Instantiates and registers plugins."""
    for plugin_class in plugin_classes:
        plugin_instance = plugin_class()
        PLUGINS.append(plugin_instance)
        print(f"Registered Plugin: {plugin_instance.name}")

# --- SETUP ---

# 1. Register Engines and their Test Plan
register_engine_and_tests(
    engine_class=ConcreteEngineA,
    test_strategies=[LatencyTest(), ] # Add other strategies here
)
# register_engine_and_tests(EngineB, [LatencyTest(), StressTest()])

# 2. Register Plugins
# register_plugins([DataReporterPlugin])
register_plugins([
    lambda: DataReporterPlugin(
        output_file='performance_report.txt',
        report_format='text'
    )
])