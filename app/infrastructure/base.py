from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def put(self, data, ttl=None):
        ...
    
    def get(self, entity_key):
        ...