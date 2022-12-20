import math
def Type205(self, state, T_a, RH, **kwargs):
    # T_a = 15  # Air temperature [degC]
    # RH = 20  # Relative humidity [-]

    P_LED = 120  # Total LED Power [W]
    A_gr = 20  # Floor area [m^2]
    LAI = kwargs["LAI"]  # LeafAreaIndex [m^2_leaves/m^2_cultivated area]
    CAC = kwargs["CAC"]  # Coverage of the floor of the cultivated area [-]
    Afv = 0.1  # Cultivated fraction [-]
    rho_v = 0.05  # Lettuce relfectivity [-]
    LED_eff = 0.52  # LED efficiency [-]

    #  #Outputs
    # q_sens #Sensible gain to air from vegetation [kJ/hr]
    # q_lat #Latent gain to air from vegetation [kg/hr]
    # T_s #Vegetation temperature [degC]
    # q_loss #Light energy that got reflected [W]

    # Parameters
    rho_a = 1.2  # Air density [kg/m^3]
    c_p = 1.006  # Air specific heat capacity [kJ/kgK]
    lmbda = 2489  # Latent heat vapor of water [kJ/kg]
    gamma = 66.5  # Psychometric constant [Pa/K]

    # -----------------------------------------------------------------------------------------------------------------------
    # Variables
    # -----------------------------------------------------------------------------------------------------------------------

    # PPFD #nu_mol/m^2*s
    # I_light #LED power convert to short-wave radiation [W/m^2]
    # Rnet #Short-wave radiation absorbed by vegetation [W/m^2]
    # r_a #Aerodynamic stomatal resistance [s/m]
    # r_s #Surface stomatal resistance [s/m]
    # e_star #Saturated vapor pressure [kPa]
    # Xa_star #Saturated vapor concentration [g/m3]
    # e #Air vapor pressure [kPa]
    # Xa #Air vapor concentration [g/m3]
    # delta #Slope of the relationship between the saturation vapour pressure and air temperature [kPa/degC]
    # epsilon #Vapour concentration
    # Xs #Vapour concentration at the canopy level [g/m3]
    # q_sens_watt #Sensible gain to air from vegetation [W/m^2]
    # q_lat_watt #Latent gain to air from vegetation [W/m^2]

    # T_s_final
    # res

    # -----------------------------------------------------------------------------------------------------------------------
    # Check the Inputs for Problems
    # -----------------------------------------------------------------------------------------------------------------------

    if Afv < 0 or Afv > 10:
        self.api.runtime_issue_severe(state, "The Cultivated fraction area of floor must be between 0 and 10 (1000%)")

    if rho_a < 0:
        self.api.runtime_issue_severe(state, "The air density must greater than 0")

    if c_p < 0:
        self.api.runtime_issue_severe(state, "The air specific heat capacity must greater than 0")

    if lmbda < 0:
        self.api.runtime_issue_severe(state, "The latent heat vapor of water must be greater than 0")

    if rho_v < 0 or rho_v > 1:
        self.api.runtime_issue_severe(state, "The lettuce leaf light reflectivity must be between 0 and 1")

    if LED_eff < 0 or LED_eff > 1:
        self.api.runtime_issue_severe(state, "The LED efficiency must be between 0 and 1")

    if T_a < -273.15:
        self.api.runtime_issue_severe(state, "The input temperature is less than 0 K")

    if P_LED < 0:
        self.api.runtime_issue_severe(state, "The total power input has to be greater than 0")

    if RH > 100 or RH < 0:
        self.api.runtime_issue_severe(state, "The relative humidity must be between 0 and 100")

    if A_gr < 0:
        self.api.runtime_issue_severe(state, "The agriculture space area have to be greater than 0")

    # -----------------------------------------------------------------------------------------------------------------------
    #    *** PERFORM ALL THE CALCULATION HERE FOR THIS MODEL. ***
    # -----------------------------------------------------------------------------------------------------------------------

    PPFD = P_LED * LED_eff * 5
    I_light = LED_eff * P_LED
    Rnet = (1 - rho_v) * I_light * CAC
    q_loss = I_light - Rnet
    #

    r_a = 100
    r_s = 60 * (1500 + PPFD) / (200 + PPFD)

    T_s = T_a - 2
    res = 1  # To get in the loop (initial value)

    while (res > 0.0001):
        T_s = T_s + 0.0001
        e_star = 0.611 * math.exp(17.4 * T_a / (T_a + 239))
        Xa_star = rho_a * c_p / lmbda / (gamma / 1000) * e_star * 1000  # [g/m^3]
        e = RH / 100 * e_star
        Xa = 7.4 * e  # [g/m^3]
        delta = 0.04145 * pow(e, (0.06088 * T_a))
        epsilon = delta / (gamma / 1000)
        Xs = Xa_star + rho_a * 1000 * c_p / lmbda * epsilon * (T_s - T_a)
        q_lat_watt = LAI * lmbda * (Xs - Xa) / (r_s + r_a)  # W/m^2
        q_sens_watt = LAI * rho_a * c_p * (T_s - T_a) / r_a * 1000
        res = Rnet - q_sens_watt - q_lat_watt

    # -----------------------------------------------------------------------------------------------------------------------
    # Convert outputs units
    # -----------------------------------------------------------------------------------------------------------------------

    q_sens = q_sens_watt * (A_gr * Afv)
    q_lat = q_lat_watt / lmbda * (A_gr * Afv)

    return q_sens,q_lat
