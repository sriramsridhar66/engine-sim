from Atmosisa import atmosisa

class EngineSimValues():
    def __init__(self):
        super(EngineSimValues, self).__init__()
        #inputs
        self.mdot = None # Mass flow rate Kg/s
        self.Ma = None # Flight mach number
        self.gamma_air = None
        self.gamma_comb = None
        self.cp_air = None
        self.cp_comb = None
        self.R = None
        self.h = None # Flight altitude
        self.T, self.a, self.P, self.rho = atmosisa(self.h)
        self.FHV = None # Fuel heating value
        self.FARcomb = None # From FAR charts
        self.T04 = None
        self.T08 = None
        self.FARab = None

        #efficiencies
        self.pi_diff = None # Diffuser pressure ratio
        self.eta_inl = None
        self.eta_comp = None # Compressor efficiency
        self.pi_comp = None # Compressor pressure ratio
        self.eta_comb = None # Combustor efficiency
        self.pi_comb = None # Combustor pressure loss
        self.eta_turb = None # Turbine efficiency
        self.eta_noz = None # Nozzle pressure ratio
        self.eta_m = None # Mechanical efficiency
        self.pi_ab = None # Afterburner pressure loss

        #free stream calcs
        self.P00 = None
        self.T00 = None
        self.v0 = None

        #inlet calcs
        self.mdot1 = None
        self.P01 = None
        self.T01 = None

        #compressor entry calcs
        self.P02 = None
        self.T02 = None
        self.mdot2 = None

        #compressor exit calcs
        self.P03 = None
        self.T03  = None
        self.mdot3 = None
        self.pwr3 = None

        #combustor calcs
        self.P04 = None
        self.deltaTcomb = None
        self.mdotfuel = None
        self.mdot4 = None

        #turbine calcs
        self.T05 = None
        self.P05 = None
        self.mdot5 = None

        #nozzle entry calcs
        self.P06 = None
        self.T06 = None
        self.mdot6 = None

        #nozzle throat calcs
        self.P07 = None
        self.T07 = None
        self.mdot7 = None
        self.pi_noz = None
        self.pi_crit = None
        self.P7 = None
        self.Q = None
        self.A7 = None
        self.v7 = None
        self.Fg = None
        self.Fn = None
        self.SFC = None

        #afterburner calcs
        self.P08 = None
        self.deltaTab = None
        self.mdotfuelab = None
        self.mdot8 = None
        self.pi_nozab = None
        self.P8 = None
        self.Qab = None
        self.A8 = None
        self.v8 = None
        self.Fgab = None
        self.Fnab = None
        self.SFCab = None

        #charts
        self.Tplot = None
        self.Pplot = None
        self.stations = [0, 1, 2, 3, 4, 5, 6, 7, 8]
