from testplan.common.config import Config
from common.plugin import RuntimeType, TestplanPlugin
from testplan.report import TestReport
from typing import Dict, Any

class MetricReporterConfig(Config):
    """
    Configuration for the Metric Reporter Plugin. 
    Can be used to specify endpoints, API keys, or reporting format.
    """
    # For a real-world scenario, you might add:
    # output_file = Member(str, default='performance_metrics.csv')
    pass

class MetricReporterPlugin(TestplanPlugin):
    """
    A custom Testplan plugin responsible for extracting performance metrics
    from the final report and simulating external data reporting.
    (Adheres to SRP: Reporting/Data Handling).
    """
    
    # Required properties for a Testplan plugin
    name = 'metric_reporter'
    runtime = RuntimeType.MAIN
    cfg = MetricReporterConfig

    def on_test_start(self, engine_name: str, test_type: str) -> None:
        """Called when a test starts."""
        print(f"\nStarting test: {engine_name} - {test_type}")

    def on_test_complete(self, results: Dict[str, Any]) -> None:
        """Called when a test completes."""
        print(f"Test completed with results: {results}\n")

    def test_plan_result(self, result: TestReport):
        """
        Called once when the entire Testplan run is complete.
        This hook gives us the final, compiled TestReport.
        """
        
        print("\n" + "="*50)
        print("📊 PLUGIN: CUSTOM PERFORMANCE METRIC REPORTER START")
        print("="*50)
        
        total_data_points_reported = 0

        # The TestReport has a tree structure. We iterate through the root entries.
        for entry in result.entries:
            if entry.category == 'multitest':
                # Traverse the MultiTest structure (Suites -> Testcases)
                for suite in entry.entries:
                    for case in suite.entries:
                        # The attached data (created by the LatencyStrategy) is retrieved here
                        raw_data_attachment = case.attachments.get('LatencyRawData')
                        
                        if raw_data_attachment:
                            # Extract the specific metric list from the attachment dictionary
                            latencies_ms = raw_data_attachment.get('latency_data_ms')
                            
                            if latencies_ms:
                                print(f"  > Found data for: **{entry.name} / {case.name}**")
                                
                                # --- Reporting Logic Simulation ---
                                min_lat = min(latencies_ms)
                                max_lat = max(latencies_ms)
                                count = len(latencies_ms)
                                total_data_points_reported += count

                                # In a real system, this is where you would:
                                # 1. Publish to Prometheus/InfluxDB.
                                # 2. Write to a CSV/JSON file.
                                print(f"    - Action: Publishing {count} data points to external service...")
                                print(f"    - Summary: Min={min_lat:.3f}ms, Max={max_lat:.3f}ms")

        print(f"\n✅ REPORTER COMPLETE: Successfully processed {total_data_points_reported} raw data points.")
        print("="*50 + "\n")
