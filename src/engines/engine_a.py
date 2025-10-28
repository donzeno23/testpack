from core.interfaces import IEngine
import time
from typing import Dict, Any

class ConcreteEngineA(IEngine):
    @property
    def name(self) -> str:
        return "EngineA_LowLatency"

    def execute_trade(self, order: Dict[str, Any]) -> Any:
        # Simulate very fast execution
        # time.sleep(0.000001) 
        return {"status": "executed", "engine": self.name, "timestamp": time.time()}
    