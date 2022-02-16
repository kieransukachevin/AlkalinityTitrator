from titration.utils.UIState import UIState
from titration.utils import interfaces, constants

class AutomaticTitration(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('AutomaticTitration', titrator)
        self.titrator = titrator
        self.values = {'pH_target' : 5, 'current_pH' : 5}
        self.subState = 1
    
    def name(self):
        return 'AutomaticTitration'

    def handleKey(self, key):
        pass

    def loop(self):
        if self.subState == 1:
            interfaces.lcd_out(
                "Titrating to {} pH".format(str(self.values['pH_target'])),   # TODO: Change pH_target
                style=constants.LCD_CENT_JUST,
                line=4,
            )
            self.subState += 1
        
        elif self.subState == 2:
            interfaces.lcd_out("Mixing...", style=constants.LCD_CENT_JUST, line=4)
            self.subState += 1
        
        elif self.subState == 3:
            interfaces.lcd_clear()
            interfaces.lcd_out("pH value {} reached".format(self.values['current_pH']), line=1) # TODO: Change current_pH

    def start(self):
        interfaces.lcd_out("AUTO SELECTED", style=constants.LCD_CENT_JUST, line=4)

