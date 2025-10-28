from core.interfaces import ITestStrategy, IEngine
import time
from typing import Dict, Any

class LatencyTest(ITestStrategy):
    @property
    def test_type(self) -> str:
        return "latency"

    def execute_test(self, engine: IEngine, iterations: int = 1000) -> Dict[str, Any]:
        total_time = 0
        latencies = []
        for _ in range(iterations):
            start = time.perf_counter_ns()
            engine.execute_trade({"symbol": "BTC/USD", "amount": 1})
            end = time.perf_counter_ns()
            latency_ns = end - start
            latencies.append(latency_ns)
            total_time += latency_ns
            
        avg_latency_ms = (total_time / iterations) / 1_000_000
        
        return {
            "test_type": self.test_type,
            "engine": engine.name,
            "iterations": iterations,
            "avg_latency_ms": avg_latency_ms,
            # For detailed analysis, you might return the full latencies list
        }
