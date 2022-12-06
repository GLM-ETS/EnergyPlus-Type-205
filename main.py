import math, sys
sys.path.append("C:\EnergyPlusV22-1-0")
from pyenergyplus.plugin import EnergyPlusPlugin
import pandas as pd
import numpy as np





class type205(EnergyPlusPlugin):

    ShadeStatusInteriorBlindOn = 6
    ShadeStatusOff = 0

    def __init__(self):
        super().__init__()
        self.handles_set = False
        self.handle_zone_sensible_cooling_rate = None
        self.handle_solar_beam_incident_cosine = None
        self.handle_shading_deploy_status = None
        self.handle_global_shading_actuator_status = None  # only because actuators can be output vars ... yet
        self.handle_time_of_day = None

    def on_begin_timestep_before_predictor(self, state) -> int:

        if not self.handles_set:
            self.handle_zone_sensible_cooling_rate = self.api.exchange.get_variable_handle(
                state, "Zone Air System Sensible Cooling Rate", "West Zone"
            )
            self.handle_solar_beam_incident_cosine = self.api.exchange.get_variable_handle(
                state, "Surface Outside Face Beam Solar Incident Angle Cosine Value", "Zn001:Wall001:Win001"
            )
            self.handle_shading_deploy_status = self.api.exchange.get_actuator_handle(
                state, "Window Shading Control", "Control Status", "Zn001:Wall001:Win001"
            )
            self.handle_global_shading_actuator_status = self.api.exchange.get_global_handle(
                state, "Zn001_Wall001_Win001_Shading_Deploy_Status"
            )

            self.handles_set = True

        current_incident_angle = self.api.exchange.get_variable_value(state, self.handle_solar_beam_incident_cosine)
        current_sensible_cool_rate = self.api.exchange.get_variable_value(state, self.handle_zone_sensible_cooling_rate)
        incident_angle_rad = math.acos(current_incident_angle)
        incident_angle_degrees = math.degrees(incident_angle_rad)
        value_to_assign = self.ShadeStatusOff

        # add variable
        tod = self.handle_time_of_day = self.api.exchange.current_time(state)

        if (incident_angle_degrees < 45 or current_sensible_cool_rate > 20) and tod >= 9 and tod <= 17:
            value_to_assign = self.ShadeStatusInteriorBlindOn

        if tod == 5.0:
            # Create 5 random integers in the range of 10 - 25
            random_data = np.random.randint(10, 25, size=5)
            # Create Datfarme with single column of random values
            df = pd.DataFrame(random_data, columns=['RANDOM VALUES'])
            # Display the Dataframe
            print(df)

        self.api.exchange.set_actuator_value(state, self.handle_shading_deploy_status, value_to_assign)
        self.api.exchange.set_global_value(state, self.handle_global_shading_actuator_status, value_to_assign)

        return 0