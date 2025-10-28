import time
from testplan.testing.multitest.driver.base import Driver
from time import perf_counter_ns, sleep
from typing import Dict, Any
from rich import print as rprint

class SimpleEngineDriver(Driver):
    """
    Testplan Driver wrapping a simple trading engine simulation.
    This acts as the interface (Command execution) for the Strategies.
    """
    
    # Adheres to Liskov by implementing the Driver interface correctly
    
    @property
    def name(self) -> str:
        return self._engine_name

    def __init__(self, name: str, engine_name: str, **kwargs):
        super().__init__(name, **kwargs)
        self._engine_name = engine_name
        print(f"Driver initialized for engine: {engine_name}")

    def starting(self):
        # Startup logic for the trading engine (e.g., connect, initialize, etc.)
        rprint("[green]Starting SimpleEngineDriver...[/green]")
        super().starting()
        # Simulate engine specific latency profile
        self._base_latency_ns = 50 if self._engine_name == "Alpha" else 150
        print(f"Engine {self._engine_name} started.")

    def execute_trade(self, symbol: str, volume: int) -> int:
        """Simulates an order execution and returns latency in nanoseconds."""
        # rprint("[blue]Executing trade...[/blue]")
        start = perf_counter_ns()
        
        # Simulate engine work (e.g., matching logic, IO, etc.)
        # This is where engine-specific complexity would reside (SRP for Engine)
        sleep((self._base_latency_ns / 1_000_000_000) * (1 + volume * 0.01))
        # rprint("[blue]Trade executed.[/blue]")
        # rprint(f"Engine {self._engine_name} executed trade for {symbol} volume {volume}.")

        end = perf_counter_ns()
        # rprint(f"Trade latency: {end - start} ns")
        # rprint(f"[bold blue]Engine {self._engine_name} trade latency: {end - start} ns[/bold blue]")
        return end - start

    def warmup(self, num_trades: int = 100):
        """Warmup the engine, ensuring consistent test conditions."""
        for _ in range(num_trades):
            self.execute_trade("WARMUP/USD", 1)
        print(f"Engine {self._engine_name} warmed up with {num_trades} trades.")

    def execute_operation(self, operation: str = "write", size_bytes: int = 1024) -> float:
        """
        Execute a generic operation for stress testing.
        
        Args:
            operation: Type of operation ('read', 'write')
            size_bytes: Size of data to process
            
        Returns:
            float: Operation duration in nanoseconds
        """
        start_time = time.time_ns()
        
        if operation == "write":
            # Simulate write operation
            data = 'x' * size_bytes
            with open('/dev/null', 'w') as f:
                f.write(data)
        elif operation == "read":
            # Simulate read operation
            with open('/dev/zero', 'rb') as f:
                f.read(size_bytes)
                
        return time.time_ns() - start_time