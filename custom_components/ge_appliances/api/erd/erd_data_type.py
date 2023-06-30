import enum

@enum.unique
class ErdDataType(enum.IntFlag):
    STRING = enum.auto()
    BOOL = enum.auto()
    INT = enum.auto()
    FLOAT = enum.auto()
    DATE = enum.auto()
    DATETIME = enum.auto()
    TIMESPAN = enum.auto()
