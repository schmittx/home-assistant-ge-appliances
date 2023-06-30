import logging

from datetime import timedelta
from typing import Optional

from ..abstract import ErdReadWriteConverter, ErdReadOnlyConverter
from .....api.erd.erd_codes import ErdCodeType

_LOGGER = logging.getLogger(__name__)

def erd_decode_timespan(value: any, unit_of_measurement: str = 'minutes') -> Optional[timedelta]:
    """ 
    Decodes a raw integer as a time span, 65535 is treated as None. 
    unit_of_measurements supported: hours, minutes, seconds; default = minutes.
    """
    int_value = int(value, 16)
    if int_value == 65535:
        _LOGGER.debug('Got timespan value of 65535. Treating as None.')
        return None
    return int_value
#    if unit_of_measurement == 'seconds':
#        return timedelta(seconds=int_value)
#    if unit_of_measurement == 'hours':
#        return timedelta(hours=int_value)
#    return timedelta(minutes=int_value)
def erd_encode_timespan(value: Optional[timedelta], unit_of_measurement: str = 'minutes', length: int = 2) -> str:
    """ 
    Encodes a time span as an erd integer, None is encoded as 65535. 
    unit_of_measurements supported: hours, minutes, seconds; default = minutes.
    """
    if value is None:
        int_value = 65535
    else:
        if unit_of_measurement == 'seconds':
            int_value = value.seconds
        if unit_of_measurement == 'hours':
            int_value = value.seconds // 3600
        int_value = value.seconds // 60
    return int_value.to_bytes(length, 'big').hex()

class ErdTimeSpanConverter(ErdReadWriteConverter[Optional[timedelta]]):
    def __init__(self, erd_code: ErdCodeType = "Unknown", unit_of_measurement: str = 'minutes', length: int = 2):
        super().__init__(erd_code)
        self.length = length
        self.unit_of_measurement = unit_of_measurement
    def erd_decode(self, value: str) -> Optional[timedelta]:
        """ Decodes a raw integer as a time span, 65535 is treated as None. """
        return erd_decode_timespan(value, self.unit_of_measurement)
    def erd_encode(self, value: Optional[timedelta]) -> str:
        """ Encodes a time span as an erd integer, None is encoded as 65535. """
        return erd_encode_timespan(value, self.unit_of_measurement, self.length)

class ErdReadOnlyTimeSpanConverter(ErdReadOnlyConverter[Optional[timedelta]]):
    def __init__(self, erd_code: ErdCodeType = "Unknown", unit_of_measurement: str = 'minutes'):
        super().__init__(erd_code)
        self.unit_of_measurement = unit_of_measurement    
    def erd_decode(self, value: str) -> Optional[timedelta]:
        """ Decodes a raw integer as a time span, 65535 is treated as None. """
        return erd_decode_timespan(value, self.unit_of_measurement)