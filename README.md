# TestPack Framework

A flexible testing framework with plugin support for performance testing and reporting.

## Architecture

The framework consists of several key components:

- **Engines**: Test targets that implement the `IEngine` interface
- **Test Strategies**: Define how tests are executed using the Strategy pattern
- **Plugins**: Extensible reporting and monitoring capabilities
- **Test Executor**: Coordinates test execution and plugin notifications

## Adding a New Engine

1. Create a new engine class in the [engines](src/engines) directory:

```python
# filepath: src/engines/my_engine.py
from core.interfaces import IEngine

class MyCustomEngine(IEngine):
    @property
    def name(self) -> str:
        return "MyCustomEngine"
        
    def initialize(self) -> None:
        print("Initializing MyCustomEngine...")
        
    def execute_operation(self, **kwargs) -> Dict[str, Any]:
        return {"result": "success", "latency_ms": 42}
```

2. Register the engine in [engine_registry.py](src/engine_registry.py):

```python
from engines.my_engine import MyCustomEngine

register_engine_and_tests(
    engine_class=MyCustomEngine,
    test_strategies=[LatencyTest()]
)
```

## Adding a New Test Type/Strategy

1. Create a new strategy class in [test_types](src/test_types):

```python
from core.interfaces import ITestStrategy, IEngine
from typing import Dict, Any

class MyTestStrategy(ITestStrategy):
    @property
    def test_type(self) -> str:
        return "my_custom_test"
        
    def execute_test(self, engine: IEngine, iterations: int) -> Dict[str, Any]:
        results = []
        for _ in range(iterations):
            result = engine.execute_operation()
            results.append(result)
        return {"test_results": results}
```

2. Add the strategy to an engine's test plan:

```python
register_engine_and_tests(
    engine_class=MyCustomEngine,
    test_strategies=[MyTestStrategy(), LatencyTest()]
)
```

## Creating a Plugin

1. Create a new plugin class in [plugins](src/plugins):

```python
from common.plugin import TestplanPlugin, RuntimeType
from testplan.common.config import Config

class MyPluginConfig(Config):
    @classmethod
    def get_options(cls) -> Dict:
        return {
            'output_file': str,
            'custom_option': int
        }

class MyCustomPlugin(TestplanPlugin):
    NAME = 'my_custom_plugin'
    runtime = RuntimeType.MAIN
    cfg = MyPluginConfig
    
    def on_test_start(self, engine_name: str, test_type: str) -> None:
        print(f"Test starting: {engine_name} - {test_type}")
        
    def on_test_complete(self, results: Dict[str, Any]) -> None:
        print(f"Test completed: {results}")
        
    def test_plan_result(self, result: TestReport) -> None:
        print("Processing final results...")
```

2. Register the plugin in [engine_registry.py](src/engine_registry.py):

```python
register_plugins([
    lambda: MyCustomPlugin(
        output_file='custom_report.txt',
        custom_option=42
    )
])
```

## Running Tests

1. Install dependencies:
```bash
pip install -e ".[dev]"
```

2. Run all tests:
```bash
./src/run_tests.sh
```

3. Run specific tests:
```bash
pytest src/tests/test_performance.py -v
```

## Project Structure

```
src/
├── core/           # Core framework components
├── engines/        # Test engine implementations
├── plugins/        # Plugin implementations
├── test_types/    # Test strategy implementations
└── tests/         # Test cases
```

## Plugin System

The framework uses a plugin system for extensibility:

- **Data Reporter Plugin**: Summarizes and exports test results
- **Metric Reporter Plugin**: Tracks performance metrics
- **Custom Plugins**: Add your own by implementing the `TestplanPlugin` interface

Each plugin can hook into the test lifecycle:
- `on_test_start`: Called before each test
- `on_test_complete`: Called after each test
- `test_plan_result`: Called after all tests complete

## Configuration

Use `pyproject.toml` for project configuration:

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request