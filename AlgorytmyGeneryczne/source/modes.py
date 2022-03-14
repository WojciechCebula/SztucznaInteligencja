import typing
import json


class Flow:
    def __init__(self, source: int, dest: int, amount: int) -> None:
        self.source = source
        self.dest = dest
        self.amount = amount

class Cost:
    def __init__(self, source: int, dest: int, cost: int) -> None:
        self.source = source
        self.dest = dest
        self.cost = cost
    

class Mode:
    def __init__(self, width: int, height: int, occupancy: int, flow_path: str, cost_path: str) -> None:
        self.width = width
        self.height = height
        self.occupancy = occupancy
        
        self.flows = self._load_flows(flow_path)
        self.costs = self._load_costs(cost_path)
        self.connections = self._load_connections()
    
    def get_flow(self, source: int, dest: int) -> int:
        return self.flows.get((source, dest))
    
    def get_cost(self, source: int, dest: int) -> int:
        return self.costs.get((source, dest))
    
    def _load_connections(self) -> typing.Dict[int, typing.List[int]]:
        result = {}
        for source, dest in self.flows:
            if result.get(source):
                result[source].append(dest)
            else:
                result[source] = [dest]
                
        return result
    
    @classmethod
    def _load_flows(cls, flow_path: str) -> typing.Dict[typing.Tuple[int, int], int]:
        flows = {}
        for f in cls._load_data(flow_path):
            flow = Flow(**f)
            flows[flow.source, flow.dest] = flow.amount
        return flows
            
    @classmethod
    def _load_costs(cls, cost_path: str) -> typing.Dict[typing.Tuple[int, int], int]:
        costs = {}
        for c in cls._load_data(cost_path):
            cost = Cost(**c)
            costs[cost.source, cost.dest] = cost.cost
        return costs
    
    @staticmethod
    def _load_data(path: str) -> typing.Generator[typing.Any, None, None]:
        data = []
        with open(path, 'r') as f:
            data = json.load(f)
        
        for relation in data:
            yield relation
