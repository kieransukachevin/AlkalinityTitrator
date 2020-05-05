# Code for running the different routines
import interfaces
import constants
import analysis
import time


def run_routine(selection):
    """Runs routine based on input"""
    if selection == '1':
        # initial titration
        titration(constants.INITIAL_TARGET_PH, constants.INCREMENT_AMOUNT, 10 * 60)
        # 3.5 -> 3.0
        titration(constants.FINAL_TARGET_PH, constants.INCREMENT_AMOUNT)
    elif selection == '2':
        calibration()
    elif selection == '3':
        edit_settings()
    elif selection == '4':
        _test_temp()
    elif selection == '5':
        return -1


def _test_temp():
    for i in range(5):
        temp, res = interfaces.read_temperature()
        print("Temperature: {0:0.3f}C".format(temp))
        print("Resistance: {0:0.3f}C".format(res))
        time.sleep(0.5)


def calibration():
    """Routine for letting the user pick the sensor to calibrate"""
    interfaces.display_list(constants.SENSOR_OPTIONS)
    sensor_selection = interfaces.read_user_input(['1', '2'])
    if sensor_selection == '1':
        _calibrate_pH()
    elif sensor_selection == '2':
        _calibrate_temperature()


def _calibrate_pH():
    """Routine for calibrating pH sensor"""
    # get first buffer pH
    interfaces.lcd_out('Enter buffer pH')
    buffer1_actual_pH = float(interfaces.read_user_input())
    # TODO wait until user hits another key to stop reading pH and use the value of pH on key press?
    interfaces.lcd_out('Lower sensor into buffer, and press enter to record value')
    input()  # to make the program wait indefinitely for the user to press enter
    buffer1_measured_volts = float(interfaces.read_raw_pH()[0])
    interfaces.lcd_out("Recorded pH: {}".format(buffer1_measured_volts))

    # get second buffer pH
    interfaces.lcd_out('Enter second buffer pH')
    buffer2_actual_pH = float(interfaces.read_user_input())
    # TODO wait until user hits another key to stop reading pH and use the value of pH on key press?
    interfaces.lcd_out('Lower sensor into buffer, and press enter to record value')
    input()  # to make the program wait indefinitely for the user to press enter
    buffer2_measured_volts = float(interfaces.read_raw_pH()[0])
    interfaces.lcd_out("Recorded pH: {}".format(buffer2_measured_volts))

    # set calibration constants
    constants.calibrated_pH['measured_volts'][0] = min(buffer1_measured_volts, buffer2_measured_volts)
    constants.calibrated_pH['measured_volts'][1] = max(buffer1_measured_volts, buffer2_measured_volts)
    constants.calibrated_pH['actual_pH'][0] = min(buffer1_actual_pH, buffer2_actual_pH)
    constants.calibrated_pH['actual_pH'][1] = max(buffer1_actual_pH, buffer2_actual_pH)
    constants.calibrated_pH['slope'] = float((constants.calibrated_pH['actual_pH'][1] -
                                              constants.calibrated_pH['actual_pH'][0]) /
                                             (constants.calibrated_pH['measured_volts'][1] -
                                              constants.calibrated_pH['measured_volts'][0]))
    # return buffer1_measured_volts, buffer2_measured_volts, buffer1_actual_pH, buffer2_actual_pH


def _calibrate_temperature():
    """Routine for calibrating temperature sensor"""
    # TODO wait until user hits another key to stop reading pH and use the value of pH on key press?
    interfaces.lcd_out("What is temperature of the reference solution?")
    expected_temp = float(input())
    interfaces.lcd_out('Lower temperature probe into sufficiently cooled water; hit enter when done')
    input()  # to make the program wait indefinitely for the user to press enter
    expected_resistance = analysis.calculate_expected_resistance(expected_temp)

    actual_temperature, actual_resistance = interfaces.read_temperature()
    interfaces.lcd_out("Recorded temp: {0:0.3f}".format(actual_temperature))
    diff = expected_resistance - actual_resistance
    new_ref_resistance = constants.calibrated_ref_resistor_value + diff * constants.calibrated_ref_resistor_value / expected_resistance
    constants.calibrated_ref_resistor_value = float(new_ref_resistance)
    # reinitialize sensors with calibrated values
    print(new_ref_resistance)
    interfaces.setup_interfaces()


def titration(pH_target, solution_increment_amount, degas_time=0):
    '''Incrementally adds HCl depending on the input parameters, until target pH is reached
    '''
    # NOTE If increment value is 20, don't want to add that again to get it close to 3.5...

    # Current pH level; calculated from pH monitor readings
    pH_old = interfaces.read_pH()
    # keep track of 10 most recent pH values to ensure pH is stable 
    pH_values = [pH_old] * 10
    # a counter used for updating values in pH_values
    pH_list_counter = 0

    # how many iterations should the pH value be close before breaking?
    while True:
        pH_reading = interfaces.read_pH()
        temp_reading = interfaces.read_temperature()[0]
        # interfaces.lcd_out("pH: {}".format(pH_new))
        # interfaces.lcd_out("temp: {0:0.3f}C".format(temp))
        pH_values[pH_list_counter] = pH_reading

        # make sure temperature within correct bounds; global value for all titrations
        if abs(temp_reading - constants.TARGET_TEMP) > constants.TEMPERATURE_ACCURACY:
            print("TEMPERATURE OUT OF BOUNDS")
            # TODO output to error log
            # Log error and alert user; write last data to file
            # note: this does not invalidate the results, but should probably be taken into consideration

        if analysis.std_deviation(pH_values) < constants.TARGET_STD_DEVIATION:
            if analysis.calculate_mean(pH_values) - pH_target < constants.PH_ACCURACY:
                # pH is close or at target; exit while loop
                break
            interfaces.dispense_HCl(solution_increment_amount)

        # check last pH value against current (might not be needed with std deviation test)
        # if abs(pH_new - pH_old) < constants.STABILIZATION_CONSTANT:
        #     if abs(pH_new - pH_target) < constants.PH_ACCURACY:
        #         break
        #     interfaces.dispense_HCl(solution_increment_amount)
        # pH_old = pH_new

        # TODO store temp, pH values or immediately write to file (might be slow)
        # Write to raw data file and (more usable) data file?
        time.sleep(constants.TITRATION_WAIT_TIME)
        pH_list_counter = 0 if pH_list_counter >= 9 else pH_list_counter + 1

    time.sleep(degas_time)

    # while (current_pH - constants.TARGET_PH) > constants.PH_ACCURACY:
    #     # TODO
    #     interfaces.dispense_HCl(0.05)
    #     # TODO measure new pH level; wait until readings have settled
    #     current_pH = new_pH
    #     # TODO write out data to csv file


def edit_settings():
    pass
