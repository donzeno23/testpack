from core.interfaces import ITestStrategy, IEngine
from typing import Dict, Any, List
import time
import random

class StressStrategy(ITestStrategy):
    """Strategy for performing stress tests on engines."""

    @property
    def test_type(self) -> str:
        return "stress"

    def execute_test(self, engine: IEngine, iterations: int) -> Dict[str, Any]:
        """
        Executes stress tests using different stress types (CPU, Memory, IO).
        
        Args:
            engine: Engine instance to test
            iterations: Number of stress test iterations
            
        Returns:
            Dictionary containing stress test results
        """
        results: Dict[str, List[float]] = {
            "cpu_stress_ms": [],
            "memory_stress_ms": [],
            "io_stress_ms": []
        }
        
        # Get engine name safely
        engine_name = getattr(engine, 'name', str(engine))
        
        for _ in range(iterations):
            # CPU Stress
            start_time = time.time()
            for _ in range(10000):  # Reduced for testing
                _ = random.random() ** 2
            results["cpu_stress_ms"].append((time.time() - start_time) * 1000)
            
            # Memory Stress
            start_time = time.time()
            memory_block = ['x' * 1024 * 1024]  # Allocate 1MB
            results["memory_stress_ms"].append((time.time() - start_time) * 1000)
            del memory_block  # Clean up
            
            # IO Stress
            start_time = time.time()
            engine.execute_operation(operation="write", size_bytes=1024*1024)
            results["io_stress_ms"].append((time.time() - start_time) * 1000)
            
        # Calculate statistics for each stress type
        final_results = {}
        for stress_type, measurements in results.items():
            final_results[stress_type] = {
                "min_ms": min(measurements),
                "max_ms": max(measurements),
                "avg_ms": sum(measurements) / len(measurements),
                "raw_data_ms": measurements
            }
            
        # Attach raw data for plugins to process
        final_results["stress_raw_data"] = {
            "iterations": iterations,
            "measurements": results
        }
        
        return final_results

    def analyze_results(self, result_data, testplan_result):
        # return super().analyze_results(result_data, testplan_result)
        cpu_avg = result_data["cpu_stress_ms"]["avg_ms"]
        memory_avg = result_data["memory_stress_ms"]["avg_ms"]
        io_avg = result_data["io_stress_ms"]["avg_ms"]
        testplan_result.log(f"Avg CPU Stress Time: {cpu_avg:.3f} ms")
        testplan_result.log(f"Avg Memory Stress Time: {memory_avg:.3f} ms")
        testplan_result.log(f"Avg IO Stress Time: {io_avg:.3f} ms")
        # Example assertions
        testplan_result.less(cpu_avg, 50.0, description="Avg CPU Stress under 50ms")
        testplan_result.less(memory_avg, 20.0, description="Avg Memory Stress under 20ms")
