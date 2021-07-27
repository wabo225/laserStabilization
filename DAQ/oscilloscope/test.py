from enum import Enum, auto

class options(Enum):
    OPTION1 = 1
    OPTION2 = 2
    OPTION3 = 3

print(options.OPTION1.name)

class Parent:
    def __init__(self):
        self.value = 4
    def change(self, newValue):
        self.value = newValue

class Child(Parent):
    def __init__(self):
        self.value = super().value
    
    def update(self):
        self.value = super().value
    
    def print(self):
        print(self.value)

p = Parent
c = Child(p)
# c.print(c)
# p.change(3)