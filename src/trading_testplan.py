import sys
import traceback
from rich import print as rprint
from testplan import test_plan
from testplan.report import TestReport
from testplan.testing.multitest import MultiTest, testsuite, testcase
from testplan.testing.multitest.driver.base import Driver
from testplan.testing.multitest.base import RuntimeEnvironment
from testplan.testing.result import Result
from core.engine_factory import FACTORY
from core.interfaces import ITestStrategy

# Test configuration map: Engine Name -> List of Test Types
PERFORMANCE_TEST_MAP = {
    "AlphaEngine": ["latency", "stress"], 
    "BetaEngine": ["latency", "stress"]
}

@testsuite
class PerformanceSuite:
    """A suite of generic performance tests."""

    def __init__(self, engine_name: str, test_type: str):
        self.engine_name = engine_name
        self.test_type = test_type
        try:
            rprint(f"[blue]Creating strategy for {test_type}[/blue]")
            self.strategy: ITestStrategy = FACTORY.create_strategy_instance(test_type)
            rprint(f"[green]Successfully created {test_type} strategy[/green]")
        except ValueError as e:
            rprint(f"[red]Error creating strategy instance: {str(e)}[/red]")
            raise

    @staticmethod
    def get_test_name(engine_name: str, test_type: str) -> str:
        return f"{engine_name}_{test_type}_performance_test"

    @testcase()
    def run_performance_test(self, env: RuntimeEnvironment, result: Result):
        """
        Test case that executes a strategy using the Command Pattern.
        The 'env' object gives access to the registered driver/engine.
        """
        test_name = self.get_test_name(self.engine_name, self.test_type)
        result.log(f"Running test: {test_name}")
        print(f"Running test: {test_name}")
        
        try:
            # Retrieve the specific driver instance from the Testplan environment
            engine_driver: Driver = getattr(env, f"driver_{self.engine_name}")
            rprint(f"[blue]Using driver: {engine_driver}[/blue]")

            # Pre-test setup (Command execution)
            engine_driver.warmup(num_trades=500)
            rprint(f"[green]Warmup complete for {test_name}[/green]")
            
            # Execute the test strategy (Command execution)
            # 5000 is the number of iterations for the test
            raw_results = self.strategy.execute_test(engine_driver, iterations=1000)
            # rprint(f"Raw results: {raw_results}")
            rprint(f"[blue]Got raw results for {test_name}[/blue]")

            rprint(f"Analyzing results for test: {test_name}") 
            # Analyze and report results
            self.strategy.analyze_results(raw_results, result)
            rprint(f"[green]Analysis complete for {test_name}[/green]")

        except AttributeError as e:
            error_msg = f"Driver not found: {str(e)}"
            rprint(f"[red]{error_msg}[/red]")
            result.log(error_msg)
            result.fail("Test failed due to missing driver")
        except Exception as e:
            error_msg = f"Test execution failed: {str(e)}"
            rprint(f"[red]{error_msg}[/red]")
            result.log(error_msg)
            result.fail(f"Test failed with error: {str(e)}")

@test_plan(name="TradingEnginePerformancePlan", **FACTORY.get_plugins_config()) 
def main(plan):
    """Main test plan entry point with error handling."""
    try:
        # Track unique test names
        test_names = set()

        for engine_name, test_types in PERFORMANCE_TEST_MAP.items():
            for test_type in test_types:
                # Create unique test name
                test_name = f"{engine_name}_{test_type}"
                
                if test_name in test_names:
                    rprint(f"[red]Duplicate test name found: {test_name}[/red]")
                    continue
                    
                test_names.add(test_name)
                
                try:
                    driver_config = FACTORY.create_driver_config(engine_name)
                    rprint(f"Configured Driver for {engine_name}: {driver_config}")
                    multi_test = MultiTest(
                        name=f"{engine_name}_{test_type}",
                        suites=[
                            PerformanceSuite(
                                engine_name=engine_name, 
                                test_type=test_type
                            )
                        ],
                        environment=[driver_config] 
                    )
                    plan.add(multi_test)
                    rprint(f"[green]Added test: {test_name}[/green]")
                except Exception as e:
                    rprint(f"[red]Error setting up test {engine_name}_{test_type}: {str(e)}[/red]")
                    raise

        # Execute test plan once
        rprint("[blue]Executing test plan...[/blue]")
        result = plan.run()
        
        if not result:
            rprint("[red]Test plan execution failed![/red]")
            return False
            
        # Process the test report
        report = result.report
        failed_tests = []

        def validate_report(report: TestReport) -> bool:
            """Validate report structure and uniqueness."""
            if not hasattr(report, 'uid'):
                return False
            return True

        def process_test_report(report: TestReport):
            """Process test reports and collect failures."""
            if not validate_report(report):
                rprint(f"[yellow]Warning: Invalid report structure for {report.name}[/yellow]")
                return
                
            if hasattr(report, 'entries'):
                for entry in report.entries:
                    process_test_report(entry)
                    
            if hasattr(report, 'status'):
                import pdb;pdb.set_trace()
                if report.status and report.status.FAILED:
                    failed_tests.append(f"{report.name}: {report.status}")
                elif not report.status:
                    rprint(f"[yellow]Warning: No status for {report.name}[/yellow]")
        
        # Process the test results
        rprint("[blue]Processing test results...[/blue]")
        process_test_report(report)
        
        # Report results
        if failed_tests:
            rprint("[red]Failed Tests:[/red]")
            for failure in failed_tests:
                rprint(f"[red]  {failure}[/red]")
            return False
            
        rprint("[green]All tests completed successfully![/green]")
        return True
        
    except Exception as e:
        rprint(f"[red]Critical error in test plan execution: {str(e)}[/red]")
        rprint(f"[red]{traceback.format_exc()}[/red]")
        return False

if __name__ == '__main__':
    sys.exit(not main())