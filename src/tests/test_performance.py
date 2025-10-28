import pytest
from core.interfaces import ITestStrategy
from core.test_executor import TestExecutor
from core.engine_factory import FACTORY
from typing import Dict, Any
from testplan.testing.result import Result

# The test function uses the dynamic parameters from conftest.py
def test_engine_performance(
    test_executor: TestExecutor,
    engine_name: str,
    test_strategy: ITestStrategy,
    result: Result
):
    """
    Generic performance test that runs the specified strategy on the specified engine.
    """
    
    # 1. Create the engine instance (Factory Pattern)
    engine_instance = FACTORY.create_engine(engine_name)
    
    # 2. Set the strategy for the executor (Strategy Pattern)
    test_executor.set_strategy(test_strategy)
    
    # 3. Execute the test
    results: Dict[str, Any] = test_executor.execute_test(
        engine=engine_instance,
        iterations=1000  # Example parameter
    )
    
    # 4. Let the strategy analyze and report results
    test_strategy.analyze_results(results, result)
    
    # 5. Log results for debugging
    result.log(f"Test Results: {results}")
    
    # # 4. Assertions/Validation on Results
    # print(f"Results: {results}")
    
    # Example Assertion for a latency test
    if test_strategy.test_type == 'latency':
        # You would use a defined performance baseline here, not a magic number
        assert results['avg_latency_ms'] < 0.5, \
               f"Latency for {engine_name} ({test_strategy.test_type}) failed: {results['avg_latency_ms']}ms"

    # Example: Check for basic required keys in results
    # assert 'iterations' in results
    # assert results['engine'] == engine_name

    # Basic validation
    result.true(
        'iterations' in results,
        description="Results should contain iteration count"
    )
    result.equal(
        results.get('engine'), 
        engine_name,
        description="Engine name should match"
    )