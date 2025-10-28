import pytest
from core.engine_factory import FACTORY
from engine_registry import TEST_PLAN, PLUGINS
from core.test_executor import TestExecutor

def pytest_generate_tests(metafunc):
    """
    Dynamically generates tests based on the registered engines and test plans.
    """
    if "engine_name" in metafunc.fixturenames and "test_strategy" in metafunc.fixturenames:
        engine_params = []
        for engine_name, strategies in TEST_PLAN.items():
            for strategy in strategies:
                engine_params.append(
                    pytest.param(engine_name, strategy, id=f"{engine_name}-{strategy.test_type}")
                )
        metafunc.parametrize("engine_name, test_strategy", engine_params)

@pytest.fixture(scope="session")
def test_executor():
    """Provides the Test Executor instance, pre-loaded with plugins."""
    # Note: strategy is set at the test level, so we init with a placeholder 
    # or just the plugins. The executor can also be created per test.
    return TestExecutor(strategy=None, plugins=PLUGINS)
