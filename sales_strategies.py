from abc import ABC, abstractmethod

class SaleSStrategy(ABC):

    @abstractmethod
    def propose_mods_to_sell(self, market_list: dict[str, list[int]]) -> dict[str, list[int]]:
        pass