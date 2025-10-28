from testplan.common.config import Config
from common.plugin import RuntimeType, TestplanPlugin
from testplan.report import TestReport
from typing import Dict, Any

class DataReporterConfig(Config):
    """
    Configuration for the Data Reporter Plugin. 
    This allows configuration settings to be passed from the Testplan main entry point.
    """
    # Example config member:
    # report_format = Member(str, default='json', choices=('json', 'csv'))
    @classmethod
    def get_options(cls) -> Dict:
        """Implement the required get_options method."""
        return {
            'output_file': str,
            'report_format': str,
        }

class DataReporterPlugin(TestplanPlugin):
    """
    A custom Testplan plugin responsible for extracting and summarizing 
    performance test results from the final report.
    (Adheres to SRP: Data Reporting/Serialization).
    """
    
    # Required properties for a Testplan plugin
    name = 'data_reporter'
    runtime = RuntimeType.MAIN
    cfg = DataReporterConfig

    def __init__(self, **options):
        options.setdefault('output_file', 'test_report.txt')
        options.setdefault('report_format', 'text')
        super().__init__(**options)

    def on_test_start(self, engine_name: str, test_type: str) -> None:
        """Called when a test starts."""
        print(f"\nData Reporter: Starting test for {engine_name} - {test_type}")

    def on_test_complete(self, results: Dict[str, Any]) -> None:
        """Called when a test completes."""
        print(f"Data Reporter: Test completed with results: {results}\n")

    def test_plan_result(self, result: TestReport):
        """
        Hook executed once the Testplan run completes, providing access to the 
        final, compiled TestReport.
        """
        
        print("\n" + "="*55)
        print("📥 PLUGIN: GENERIC DATA REPORTER START (DataReporterPlugin)")
        print("="*55)
        
        test_summary_data: Dict[str, Any] = {}
        
        # Traverse the TestReport structure (Testplan -> MultiTest -> Suite -> Testcase)
        for entry in result.entries:
            if entry.category == 'multitest':
                for suite in entry.entries:
                    for case in suite.entries:
                        # The attached data, created by the Strategy (e.g., LatencyStrategy), 
                        # should be retrieved using its key: 'LatencyRawData'
                        raw_data_attachment = case.attachments.get('LatencyRawData')
                        
                        if raw_data_attachment:
                            latencies_ms = raw_data_attachment.get('latency_data_ms', [])
                            
                            if latencies_ms:
                                test_id = f"{entry.name}/{case.name}"
                                
                                # Perform data summary/serialization
                                summary = {
                                    "engine": entry.name,
                                    "test_type": "latency", # Based on attachment key
                                    "data_points": len(latencies_ms),
                                    "min_ms": min(latencies_ms),
                                    "max_ms": max(latencies_ms),
                                    "avg_ms": sum(latencies_ms) / len(latencies_ms)
                                }
                                
                                test_summary_data[test_id] = summary

                                # --- Reporting/Output Simulation ---
                                print(f"  > Summary for **{test_id}**:")
                                print(f"    - AVG Latency: {summary['avg_ms']:.3f} ms")
                                
        # Final Output Step
        if test_summary_data:
            print("\n✅ DATA REPORTER COMPLETE: Processed and summarized all performance test data.")
            
            # In a production framework, you would use 'test_summary_data' here to:
            # 1. Store results in a database (SQL/NoSQL).
            # 2. Serialize to JSON/CSV (e.g., json.dump(test_summary_data, file)).
            print(f"    [INFO] Final report contains {len(test_summary_data)} unique test summaries.")
            # print(test_summary_data) # Uncomment to see the full structure
        else:
             print("\n⚠️ DATA REPORTER: No performance data found in the report attachments.")
             
        print("="*55 + "\n")
