import statistics
from testplan.testing.result import Result
from core.interfaces import ITestStrategy
from engines.simple_engine_driver import SimpleEngineDriver 
from typing import Dict, Any

class LatencyStrategy(ITestStrategy):
    """Concrete strategy for measuring average latency."""

    def test_type(self) -> str:
        return "latency"

    def execute_test(self, engine: SimpleEngineDriver, iterations: int) -> Dict[str, Any]:
        latencies_ns = []
        for _ in range(iterations):
            latency = engine.execute_trade("TEST/USD", 1)
            latencies_ns.append(latency)
            
        return {
            "test_type": "latency",
            "latencies_ns": latencies_ns,
            "engine_name": engine.name
        }

    def analyze_results(self, result_data: Dict[str, Any], result: Result):
        latencies_ms = [l / 1_000_000 for l in result_data["latencies_ns"]]
        avg_latency = statistics.mean(latencies_ms)
        p99_latency = statistics.quantiles(latencies_ms, n=100)[98] # 99th percentile

        # Use Testplan assertions for reporting and pass/fail criteria
        result.log(f"Avg Latency: {avg_latency:.3f} ms")
        result.log(f"P99 Latency: {p99_latency:.3f} ms")
        
        # Performance Assertion (Success Criteria)
        result.less(avg_latency, 1.0, description=f"Avg Latency under 1.0ms for {result_data['engine_name']}")
        result.less(p99_latency, 1.5, description=f"P99 Latency under 1.5ms for {result_data['engine_name']}")
