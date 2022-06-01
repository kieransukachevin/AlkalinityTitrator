from titration.utils.UIState import UIState
from titration.utils import interfaces, constants
from titration.utils.UIState.prime_pump import PrimePump
from titration.utils.UIState.test_mode import TestMode
from titration.utils.UIState.titration import SetupTitration
from titration.utils.UIState.calibration import SetupCalibration
from titration.utils.UIState.update_settings import UpdateSettings
from titration.utils import LCD_interface

# TODO: change to substate
class MainMenu (UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('MainMenu', titrator)
        self.titrator = titrator
        self.subState = 1

    def name(self):
        return 'MainMenu'

    def handleKey(self, key):
        # Substate 1 key handle
        if self.subState == 1:
            if key == constants.KEY_STAR:
                self.subState = 2

            elif key == constants.KEY_1:
                # Next state SetupTitration
                self._setNextState(SetupTitration.SetupTitration(self.titrator), True)

            elif key == constants.KEY_2:
                # Next state SetupCalibration
                self._setNextState(SetupCalibration.SetupCalibration(self.titrator, self), True)

            elif key == constants.KEY_3:
                # Next state PrimePump
                self._setNextState(PrimePump.PrimePump(self.titrator, self), True)

        # Substate 2 key handle
        else:
            if key == constants.KEY_STAR:
                self.subState = 1

            elif key == constants.KEY_4:
                # Next state UpdateSettings
                self._setNextState(UpdateSettings.UpdateSettings(self.titrator, self), True)

            elif key == constants.KEY_5:
                # Next state TestMode
                self._setNextState(TestMode.TestMode(self.titrator, self), True)

            elif key == constants.KEY_6:
                quit()

    def loop(self):
        # Substate 1 output
        if self.subState == 1:
            LCD_interface.display_list(constants.ROUTINE_OPTIONS_1)    # TODO: change to LCD
            
        # Substate 2 output
        else:
            LCD_interface.display_list(constants.ROUTINE_OPTIONS_2)
