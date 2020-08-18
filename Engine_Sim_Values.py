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
        self.cp_av = None
        self.R = 287.05
        self.h = 3000 # Flight altitude
        self.T, self.a, self.P, self.rho = atmosisa(self.h)
        self.FHV = None # Fuel heating value
        self.T04 = None
        self.T08 = None
        self.r_compressor = None

        #efficiencies
        self.pi_diff = None # Diffuser pressure ratio
        self.eta_comp = None # Compressor efficiency
        self.pi_comp = None # Compressor pressure ratio
        self.eta_comb = None # Combustor efficiency
        self.pi_comb = None # Combustor pressure loss
        self.eta_turb = None # Turbine efficiency
        self.eta_noz = None # Nozzle pressure ratio
        self.eta_m = None # Mechanical efficiency
        self.eta_ab = None # Afterburner bruner efficiency
        self.pi_ab = None # Afterburner pressure loss

        #free stream calcs
        self.P00 = None
        self.T00 = None
        self.v0 = None

        #inlet calcs
        self.mdot1 = None
        self.P01 = None
        self.T01 = None # No work or heat transfer
        self.Ma1 = None # Set to inlet limit
        self.MFP = None # Mass Flow Parameter
        self.A1 = None # Inlet Area

        #compressor entry calcs
        self.P02 = None
        self.T02 = None # No work or heat transfer
        self.mdot2 = None # Continuity
        self.A2 = None # Compressor face area

        #compressor exit calcs
        self.P03 = None
        self.T03  = None
        self.mdot3 = None # Continuity
        self.pwr3 = None # Power required by compressor

        #combustor calcs
        self.P04 = None
        self.FARcomb = None # From FAR charts # From NASA
        self.deltaTcomb = None
        self.mdotfuel = None
        self.mdot4 = None

        #turbine calcs
        self.pwr5 = None # Power supplied to turbine is equal to power from compressor mechanical efficiency
        self.T05 = None # From power balancing
        self.P05 = None
        self.mdot5 = None # Continuity

        #nozzle entry calcs
        self.P06 = None
        self.T06 = None # No heat transfer or work
        self.mdot6 = None # Continuity

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
        self.SFC = None # %g/Ns

        #afterburner calcs
        self.P08 = None
        self.FARab = None
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
        self.stations = [0, 1, 2, 3, 4, 5, 6, 7]
