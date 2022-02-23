from titration.utils.UIState import UIState
from titration.utils import interfaces, constants
from titration.utils.UIState.titration import SetupTitration
from titration.utils.UIState.calibration import SetupCalibration

# TODO: CollectNumber state
class MainMenu (UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('MainMenu', titrator)
        self.routineSelection = 1
        self.titrator = titrator

    def name(self):
        return 'MainMenu'

    def handleKey(self, key):
        if self.routineSelection == 1:
            if key is constants.KEY_STAR:
                self.routineSelection = 2

            elif key is constants.KEY_1:
                interfaces.lcd_out('Run Titration', 1)
                self._setNextState(SetupTitration.SetupTitration(self.titrator), True)

            elif key is constants.KEY_2:
                interfaces.lcd_out('Calibrate sensors', 1)
                self._setNextState(SetupCalibration.SetupCalibration(self.titrator), True)

            elif key is constants.KEY_3:
                interfaces.lcd_out('Prime Pump', 1)

        else:
            if key is constants.KEY_STAR:
                self.routineSelection = 1

            elif key is constants.KEY_4:
                interfaces.lcd_out('Update settings', 1)

            elif key is constants.KEY_5:
                interfaces.lcd_out('Test Mode', 1)

            elif key is constants.KEY_6:
                interfaces.lcd_out('Exit', 1)

    def loop(self):
        # Display menu options.
        if self.routineSelection == 1:
            interfaces.display_list(constants.ROUTINE_OPTIONS_1)
        else:
            interfaces.display_list(constants.ROUTINE_OPTIONS_2)
        pass
