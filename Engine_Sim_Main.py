import sys
import numpy as np
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Engine_Sim_Values import EngineSimValues

class PlotCanvas(FigureCanvas):
    def __init__(self, parent, width=None, height=None, dpi=100):
        if width is None:
            width = parent.width()/100
        if height is None:
            height = parent.height()/100
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.ax = None

    def plot_temperature(self, stations, Tplot):
        #

    def plot_pressure(self, stations, Pplot):
        #


class EngineSim():
    def __init__(self):
        super(EngineSim, self).__init__()
        self.v = EngineSimValues()
        #create graphics views
        self.t_plot = PlotCanvas()
        self.p_plot = PlotCanvas()

    def assign_widgets(self):
        #

    def update_app(self):
        #get from gui

        self.free_stream_calcs()
        self.inlet_calcs()
        self.compressor_entry_calcs()
        self.compressor_exit_calcs()
        self.combustor_calcs()
        self.turbine_calcs()
        self.nozzle_entry_calcs()
        self.nozzle_throat_calcs()
        self.afterburner_calcs()
        self.upload_values()
        self.plot_temperature()
        self.plot_pressure()

    def free_stream_calcs(self):
        self.v.P00 = self.v.P*(1+self.v.Ma**2*((self.v.gamma_air-1)/2))**(self.v.gamma_air/(self.v.gamma_air-1))
        self.v.T00 = self.v.T*(1+self.v.Ma**2*((self.v.gamma_air-1)/2))
        self.v.v0 = self.v.Ma*self.v.a

    def inlet_calcs(self):
        self.v.mdot1 = self.v.mdot
        self.v.P01 = self.v.P00 * self.v.eta_inl # loss free
        self.v.T01 = self.v.T00 # No work or heat transfer

    def compressor_entry_calcs(self):
        self.v.P02 = self.v.pi_diff * self.v.P01 # Due to inlet losses
        self.v.T02 = self.v.T01 # No work or heat transfer
        self.v.mdot2 = self.v.mdot1 # Continuity

    def compressor_exit_calcs(self):
        self.v.P03 = self.v.P02 * self.v.pi_comp
        self.v.T03 = self.v.T02 * (1 + (self.v.P03 / self.v.P02) ** (
                    (((self.v.gamma_air - 1) / self.v.gamma_air) - 1) / self.v.eta_comp))
        self.v.mdot3 = self.v.mdot2  # Continuity
        self.v.pwr3 = self.v.mdot3 * self.v.cp_air * (self.v.T03 - self.v.T02)

    def combustor_calcs(self):
        self.v.P04 = self.v.P03 * self.v.pi_comb
        self.v.deltaTcomb = self.v.T04 - self.v.T03
        self.v.mdotfuel = self.v.FARcomb * self.v.mdot3
        self.v.mdot4 = self.v.mdot3 + self.v.mdotfuel

    def turbine_calcs(self):
        self.v.T05 = (self.v.mdot4 * self.v.cp_comb * self.v.T04 - self.v.pwr3) / (self.v.mdot4 * self.v.cp_comb) # From power balancing
        self.v.P05 = self.v.P04 * (1 - ((1 - self.v.T05 / self.v.T04) / self.v.eta_turb)) ** (self.v.gamma_comb / (self.v.gamma_comb - 1))
        self.v.mdot5 = self.v.mdot4 # Continuity

    def nozzle_entry_calcs(self):
        self.v.P06 = self.v.P05 * self.v.eta_noz
        self.v.T06 = self.v.T05 # No heat transfer or work
        self.v.mdot6 = self.v.mdot5 # Continuity

    def nozzle_throat_calcs(self):
        self.v.P07 = self.v.P06
        self.v.T07 = self.v.T06
        self.v.mdot7 = self.v.mdot6
        self.v.pi_noz = self.v.P07 / self.v.P
        self.v.pi_crit = 1.85 # Chocked nozzle ratio

        if self.v.pi_noz > self.v.pi_crit:
            self.v.P7 = self.v.P07/self.v.pi_crit
        else:
            self.v.P7 = self.v.P07/self.v.pi_noz

        self.v.Q = np.sqrt((2 / self.v.R) * (self.v.gamma_comb / (self.v.gamma_comb - 1)) * (
                    (((self.v.P07 / self.v.P7) ^ ((self.v.gamma_comb - 1) / self.v.gamma_comb) - 1) * (
                            (self.v.P07 / self.v.P7) ** (2 * (((self.v.gamma_comb - 1) / self.v.gamma_comb) - 1)))) / (
                                (self.v.P07 / self.v.P7) ** (
                                (self.v.gamma_comb - 1) / self.v.gamma_comb))))
        self.v.A7 = (self.v.mdot7 * np.sqrt(self.v.T07)) / (self.v.Q * self.v.P07)
        self.v.v7 = np.sqrt(self.v.T07) * np.sqrt(((2 * self.v.R) / ((self.v.gamma_comb - 1) / self.v.gamma_comb)) * (
                ((self.v.P07 / self.v.P7) ** ((self.v.gamma_comb - 1) / self.v.gamma_comb) - 1) / (
                (self.v.P07 / self.v.P7) ** ((self.v.gamma_comb - 1) / self.v.gamma_comb))))
        self.v.Fg = self.v.mdot7 * self.v.v7 + self.v.A7 * (self.v.P7 - self.v.P)
        self.v.Fn = self.v.Fg - (self.v.mdot * self.v.v0)
        self.v.SFC = self.v.mdotfuel / self.v.Fn

    def afterburner_calcs(self):
        self.v.P08 = self.v.P07 * self.v.pi_ab
        self.v.deltaTab = self.v.T08 - self.v.T07
        self.v.mdotfuelab = self.v.FARab * self.v.mdot7
        self.v.mdot8 = self.v.mdotfuelab + self.v.mdot7
        self.v.pi_nozab = self.v.P08 / self.v.P

        if self.v.pi_nozab > self.v.pi_crit:
            self.v.P8 = self.v.P08/self.v.pi_crit
        else:
            self.v.P8 = self.v.P08/self.v.pi_noz

        self.v.Qab = np.sqrt((2 / self.v.R) * (self.v.gamma_comb / (self.v.gamma_comb - 1)) * (
                    (((self.v.P08 / self.v.P8) ** ((self.v.gamma_comb - 1) / self.v.gamma_comb) - 1) * (
                            (self.v.P08 / self.v.P8) ** (2 * (((self.v.gamma_comb - 1) / self.v.gamma_comb) - 1)))) / (
                                (self.v.P08 / self.v.P8) ** (
                                (self.v.gamma_comb - 1) / self.v.gamma_comb))))
        self.v.A8 = (self.v.mdot8 * np.sqrt(self.v.T08)) / (self.v.Qab * self.v.P08)
        self.v.v8 = np.sqrt(self.v.T08) * np.sqrt(((2 * self.v.R) / ((self.v.gamma_comb - 1) / self.v.gamma_comb)) * (
                ((self.v.P08 / self.v.P8) ** ((self.v.gamma_comb - 1) / self.v.gamma_comb) - 1) / (
                (self.v.P08 / self.v.P8) ** ((self.v.gamma_comb - 1) / self.v.gamma_comb))))
        self.v.Fgab = self.v.mdot8 * self.v.v8 + self.v.A8 * (self.v.P8 - self.v.P)
        self.v.Fnab = self.v.Fgab - (self.v.mdot * self.v.v0)
        self.v.SFCab = (self.v.mdotfuel + self.v.mdotfuelab) / self.v.Fnab


    def upload_values(self):
        #

    def plot_temperature(self):
        self.v.Tplot = [self.v.T00, self.v.T01, self.v.T02, self.v.T03, self.v.T04, self.v.T05, self.v.T06, self.v.T07, self.v.T08]
        self.t_plot.figure.clf
        self.t_plot.plot_temperature(self.v.stations, self.v.Tplot)

    def plot_pressure(self):
        self.v.Pplot = [self.v.P00, self.v.P01, self.v.P02, self.v.P03, self.v.P04, self.v.P05, self.v.P06, self.v.P07, self.v.P08]
        self.p_plot.figure.clf
        self.p_plot.plot_pressure(self.v.stations, self.v.Pplot)