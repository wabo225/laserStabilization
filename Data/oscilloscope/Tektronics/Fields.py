from abc import ABC
from typing import Type, Any
from enum import Enum


class Readable(ABC):
    '''
      Readable classes contain a single field whose value can only be read.
      The value does not persist in the state, but it's type is confirmed
    '''

    def __init__(self, value_type: Type):
        self.value_of = value_type

    def get():
        # here, issue a scipy call to the oscilloscope
        # this implies that we need the whole path that we took to get to the tree
        pass


class ReadWriteable(ABC):
    value_type = Any

    def __init__(self, of: Enum, value_type: Type, value: Any):
        self.value: value_type
        self.of: str = of.name
        if value:
            self.value = value

    def set(self, value: value_type):
        self.value = value

        pass

    def get(self):

        pass
