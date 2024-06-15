from abc import ABC, abstractmethod

from typing import List


class DataBase(ABC):
    @abstractmethod
    def save(self, card):
        ...

    @abstractmethod
    def load(self, identifier: str):
        ...

    @abstractmethod
    def get_creators(self) -> List[str]:
        ...

    @abstractmethod
    def get_creator_cards(self, creator):
        ...
