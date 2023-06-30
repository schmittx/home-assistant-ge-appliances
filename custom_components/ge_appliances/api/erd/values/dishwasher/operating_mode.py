import enum

@enum.unique
class OperatingMode(enum.Enum):
    STATUS_DASH = "status_dash"
    STATUS_CYCLE_ACTIVE = "status_active"
    STATUS_CYCLE_COMPLETE = "status_complete"
    STATUS_OFF = "status_off"
    STATUS_DELAY = "status_delay"
    STATUS_PAUSED = "status_paused"
    CONTROL_LOCKED = "control_locked"
    STATUS_STANDBY = "status_standby"
    STATUS_INVALID = "status_invalid"
    
    def stringify(self, **kwargs):
        if self == OperatingMode.STATUS_DASH:
            return "off"
#        return self.name.replace("STATUS_","").replace("_"," ").title()
        return self.name.replace("STATUS_","").lower()
