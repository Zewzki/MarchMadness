from abc import ABCMeta, abstractmethod

class DataLoader:

    __metaclass__ = ABCMeta

    @abstractmethod
    def load_data(self, dataPath) : raise NotImplementedError

    @abstractmethod
    def parse_string(self, strToParse) : raise NotImplementedError