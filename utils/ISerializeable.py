from abc import ABCMeta, abstractmethod

class ISerializeable:

    @abstractmethod
    def serialize(self) : raise NotImplementedError

    @abstractmethod
    def deserialize(self, data) : raise NotImplementedError