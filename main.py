import sys
from Type205 import *

sys.path.append("C:\EnergyPlusV22-1-0")
from pyenergyplus.plugin import EnergyPlusPlugin

class type205(EnergyPlusPlugin):

    Type205 = Type205
    def __init__(self):
        super().__init__()

        self.handles_set = False

        self.handles_zone_temperature = None
        self.handles_zone_humidity = None

        ### Outputs back to E+ ###
        self.handle_zone_sensible_rate = None
        self.handle_zone_latent_rate = None

        # ### Reporting ###
        # self.handle_zone_vegetation_temperature = None
        # self.handle_zone_reflected_radiation = None

    def on_inside_hvac_system_iteration_loop(self, state) -> int:

        if not self.handles_set:

            self.handles_zone_temperature = self.api.exchange.get_variable_handle(state, "Zone Air Temperature", "Perimeter_ZN_4")
            self.handles_zone_humidity = self.api.exchange.get_variable_handle(state, "Zone Air Relative Humidity", "Perimeter_ZN_4")

            self.handle_zone_sensible_rate = self.api.exchange.get_actuator_handle(state,"OtherEquipment","Power Level","OTHEQ_SENSIBLE")
            self.handle_zone_latent_rate = self.api.exchange.get_actuator_handle(state,"OtherEquipment","Power Level","OTHEQ_LATENT")

            self.handles_set = True

        current_zone_air_temperature = self.api.exchange.get_variable_value(state, self.handles_zone_temperature)
        current_zone_air_humidity = self.api.exchange.get_variable_value(state, self.handles_zone_humidity)

        qs, ql = self.Type205(state, current_zone_air_temperature, current_zone_air_humidity , LAI=2, CAC=1)


        self.api.exchange.set_actuator_value(state, self.handle_zone_sensible_rate, qs)
        self.api.exchange.set_actuator_value(state, self.handle_zone_latent_rate, ql)



        return 0