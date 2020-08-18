import sys
import numpy as np
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Engine_Sim_GUI import Ui_Dialog
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
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title('Temperature[K]')
        self.ax.plot(stations, Tplot)
        self.ax.set_ylabel('Temperature')
        self.ax.grid(True)
        self.draw()

    def plot_pressure(self, stations, Pplot):
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title('Pressure[Pa]')
        self.ax.plot(stations, Pplot)
        self.ax.set_xlabel('Stations')
        self.ax.set_ylabel('Pressure')
        self.ax.grid(True)
        self.draw()

    def plot_contour(self):
        #insert rishi code
        return None


class EngineSim(QDialog):
    def __init__(self):
        super(EngineSim, self).__init__()
        self.ab = False
        self.v = EngineSimValues()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        t_plot_window = self.ui.graphicsView
        p_plot_window = self.ui.graphicsView_2
        c_plot_window = self.ui.graphicsView_3
        self.t_plot = PlotCanvas(t_plot_window)
        self.p_plot = PlotCanvas(p_plot_window)
        self.c_plot = PlotCanvas(c_plot_window)
        self.assign_widgets()
        self.show()

    def assign_widgets(self):
        self.ui.pushButton_2.clicked.connect(lambda: exit_app())
        self.ui.pushButton.clicked.connect(lambda: self.update_app())
        self.ui.horizontalSlider.valueChanged.connect(lambda: self.get_altitude())
        self.ui.radioButton.clicked.connect(lambda: self.afterburner_selection(False))
        self.ui.radioButton_3.clicked.connect(lambda: self.afterburner_selection(True))

    def get_altitude(self):
        self.v.h = float(self.ui.horizontalSlider.value()) * 1000
        self.update_app()

    def afterburner_selection(self, boolean):
        self.ab = boolean
        if boolean is True:
            self.v.stations = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        else:
            self.v.stations = [0, 1, 2, 3, 4, 5, 6, 7]
        self.update_app()

    def update_app(self):
        self.v.mdot = float(self.ui.lineEdit_1.text())
        self.v.Ma = float(self.ui.lineEdit_2.text())
        self.v.gamma_air = float(self.ui.lineEdit_3.text())
        self.v.gamma_comb = float(self.ui.lineEdit_5.text())
        self.v.cp_air = float(self.ui.lineEdit_31.text())
        self.v.cp_comb = float(self.ui.lineEdit_6.text())
        self.v.cp_av = (self.v.cp_air+self.v.cp_comb)/2
        self.v.FHV = float(self.ui.lineEdit_8.text())
        self.v.T04 = float(self.ui.lineEdit_9.text())
        self.v.r_compressor = float(self.ui.lineEdit_60.text())
        self.v.pi_diff = float(self.ui.lineEdit_10.text())
        self.v.eta_comp = float(self.ui.lineEdit_18.text())
        self.v.pi_comp = float(self.ui.lineEdit_19.text())
        self.v.eta_comb = float(self.ui.lineEdit_20.text())
        self.v.pi_comb = float(self.ui.lineEdit_32.text())
        self.v.eta_turb = float(self.ui.lineEdit_21.text())
        self.v.eta_noz = float(self.ui.lineEdit_22.text())
        self.v.eta_m = float(self.ui.lineEdit_61.text())
        if self.ab is True:
            self.v.T08 = float(self.ui.lineEdit_25.text())
            self.v.eta_ab = float(self.ui.lineEdit_23.text())
            self.v.pi_ab = float(self.ui.lineEdit_24.text())

        self.free_stream_calcs()
        self.inlet_calcs()
        self.compressor_entry_calcs()
        self.compressor_exit_calcs()
        self.combustor_calcs()
        self.turbine_calcs()
        self.nozzle_entry_calcs()
        self.nozzle_throat_calcs()
        if self.ab is True:
            self.afterburner_calcs()
            self.v.stations = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        else:
            self.v.stations = [0, 1, 2, 3, 4, 5, 6, 7]
        self.upload_values()
        self.plot_temperature()
        self.plot_pressure()

        return 0

    def free_stream_calcs(self):
        self.v.P00 = self.v.P * (1 + self.v.Ma ** 2 * ((self.v.gamma_air - 1) / 2)) ** (
                    self.v.gamma_air / (self.v.gamma_air - 1))
        self.v.T00 = self.v.T * (1 + self.v.Ma ** 2 * ((self.v.gamma_air - 1) / 2))
        self.v.v0 = self.v.Ma * self.v.a

    def inlet_calcs(self):
        self.v.mdot1 = self.v.mdot
        self.v.P01 = self.v.P00
        self.v.T01 = self.v.T00 # Nowork or heat transfer
        self.v.Ma1 = 0.8 # Set to inlet limit
        self.v.MFP = np.sqrt(self.v.gamma_air) * self.v.Ma1 * (1 + self.v.Ma1 ** 2 * ((self.v.gamma_air - 1) / 2)) ** (
                (self.v.gamma_air + 1) / (2 * (1 - self.v.gamma_air)))  # Mass Flow Parameter
        self.v.MFP = np.sqrt(self.v.gamma_air) * self.v.Ma1 * (1 + self.v.Ma1 ** 2 * ((self.v.gamma_air - 1) / 2)) ** (
                (self.v.gamma_air + 1) / (2 * (1 - self.v.gamma_air)))  # Mass Flow Parameter
        self.v.A1 = (self.v.mdot1 * np.sqrt(self.v.R * self.v.T01)) / (self.v.MFP * self.v.P01)  # Inlet area

    def compressor_entry_calcs(self):
        if self.v.Ma > 1:
            self.v.P02 = self.v.pi_diff * self.v.P01 * (1 - 0.75 * (self.v.Ma - 1) ** 1.35)  # Due to shock losses
        else:
            self.v.P02 = self.v.pi_diff * self.v.P01
        self.v.T02 = self.v.T01  # No work or heat transfer
        self.v.mdot2 = self.v.mdot1  # Continuity
        self.v.A2 = (self.v.r_compressor / 2) ** 2 * np.pi  # Compressor face area

    def compressor_exit_calcs(self):
        self.v.P03 = self.v.P02 * self.v.pi_comp
        self.v.T03 = self.v.T02 * (
                    1 + (((self.v.pi_comp ** ((self.v.gamma_air - 1) / self.v.gamma_air)) - 1) / self.v.eta_comp))
        self.v.mdot3 = self.v.mdot2  # Continuity
        self.v.pwr3 = self.v.mdot3 * self.v.cp_air * (self.v.T03 - self.v.T02)  # Power required by compressor

    def combustor_calcs(self):
        self.v.P04 = self.v.P03 * self.v.pi_comb
        self.v.FARcomb = ((self.v.T04 / self.v.T03) - 1) / (
                    ((self.v.eta_comb * self.v.FHV) / (self.v.cp_av * self.v.T03)) - (
                        self.v.T04 / self.v.T03))  # From NASA
        self.v.mdotfuel = self.v.FARcomb * self.v.mdot3
        self.v.mdot4 = self.v.mdot3 + self.v.mdotfuel

    def turbine_calcs(self):
        self.v.pwr5 = self.v.eta_m * self.v.pwr3  # Power suppied to turbine is equal to power from compressor * mechanical efficiency
        self.v.T05 = ((self.v.mdot4 * self.v.cp_comb * self.v.T04) - self.v.pwr5) / (
                    self.v.mdot4 * self.v.cp_comb)  # From power balancing
        self.v.P05 = self.v.P04 * (1 - ((1 - self.v.T05 / self.v.T04) / self.v.eta_turb)) ** (self.v.gamma_comb / (self.v.gamma_comb - 1))
        self.v.mdot5 = self.v.mdot4  # Continuity

    def nozzle_entry_calcs(self):
        self.v.P06 = self.v.P05 * self.v.eta_noz
        self.v.T06 = self.v.T05  # No heat transfer or work
        self.v.mdot6 = self.v.mdot5  # Continuity

    def nozzle_throat_calcs(self):
        self.v.P07 = self.v.P06
        self.v.T07 = self.v.T06
        self.v.mdot7 = self.v.mdot6
        self.v.pi_noz = self.v.P07 / self.v.P
        self.v.pi_crit = 1.85  # Chocked nozzle ratio
        if self.v.pi_noz > self.v.pi_crit:
            self.v.P7 = self.v.P07 / self.v.pi_crit
        else:
            self.v.P7 = self.v.P07 / self.v.pi_noz
        self.v.Q = np.sqrt((2 / self.v.R) * (self.v.gamma_comb / (self.v.gamma_comb - 1)) * (
                    (((self.v.P07 / self.v.P7) ** ((self.v.gamma_comb - 1) / self.v.gamma_comb) - 1) * (
                            (self.v.P07 / self.v.P7) ** (2 * (((self.v.gamma_comb - 1) / self.v.gamma_comb) - 1)))) / (
                                (self.v.P07 / self.v.P7) ** (
                                (self.v.gamma_comb - 1) / self.v.gamma_comb))))
        self.v.A7 = (self.v.mdot7 * np.sqrt(self.v.T07)) / (self.v.Q * self.v.P07)
        self.v.v7 = np.sqrt(self.v.T07) * np.sqrt(((2 * self.v.R) / ((self.v.gamma_comb - 1) / self.v.gamma_comb)) * (
                ((self.v.P07 / self.v.P7) ** ((self.v.gamma_comb - 1) / self.v.gamma_comb) - 1) / (
                (self.v.P07 / self.v.P7) ** ((self.v.gamma_comb - 1) / self.v.gamma_comb))))
        self.v.Fg = self.v.mdot7 * self.v.v7 + self.v.A7 * (self.v.P7 - self.v.P)
        self.v.Fn = self.v.Fg - (self.v.mdot * self.v.v0)
        self.v.SFC = (self.v.mdotfuel / self.v.Fn) * 1000  # g / Ns

    def afterburner_calcs(self):
        self.v.P08 = self.v.P07 * self.v.pi_ab
        self.v.FARab = ((self.v.T08 / self.v.T07) - 1) / (
                    ((self.v.eta_ab * self.v.FHV) / (self.v.cp_comb * self.v.T07)) - (
                        self.v.T08 / self.v.T07))  # From NASA
        self.v.mdotfuelab = self.v.FARab * self.v.mdot7
        self.v.mdot8 = self.v.mdotfuelab + self.v.mdot7
        self.v.pi_nozab = self.v.P08 / self.v.P
        if self.v.pi_nozab > self.v.pi_crit:
            self.v.P8 = self.v.P08 / self.v.pi_crit
        else:
            self.v.P8 = self.v.P08 / self.v.pi_noz
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
        self.v.SFCab = ((self.v.mdotfuel + self.v.mdotfuelab) / self.v.Fnab) * 1000  # %g / Ns


    def upload_values(self):
        try:
            self.ui.lineEdit_4.setText('{:.6f}'.format(self.v.A7))
            self.ui.lineEdit_11.setText('{:.6f}'.format(self.v.v7))
            self.ui.lineEdit_12.setText('{:.6f}'.format(self.v.Fg))
            self.ui.lineEdit_13.setText('{:.6f}'.format(self.v.Fn))
            self.ui.lineEdit_36.setText('{:.6f}'.format(self.v.SFC))
            if self.ab is True:
                self.ui.lineEdit_14.setText('{:.6f}'.format(self.v.A8))
                self.ui.lineEdit_15.setText('{:.6f}'.format(self.v.v8))
                self.ui.lineEdit_16.setText('{:.6f}'.format(self.v.Fgab))
                self.ui.lineEdit_17.setText('{:.6f}'.format(self.v.Fnab))
                self.ui.lineEdit_37.setText('{:.6f}'.format(self.v.SFCab))
            else:
                self.ui.lineEdit_14.setText('None')
                self.ui.lineEdit_15.setText('None')
                self.ui.lineEdit_16.setText('None')
                self.ui.lineEdit_17.setText('None')
                self.ui.lineEdit_37.setText('None')
        except Exception as error:
            print(error)
            QApplication.restoreOverrideCursor()
            bad_file()

    def plot_temperature(self):
        if self.ab is True:
            self.v.Tplot = [self.v.T00, self.v.T01, self.v.T02, self.v.T03, self.v.T04, self.v.T05, self.v.T06, self.v.T07, self.v.T08]
        else:
            self.v.Tplot = [self.v.T00, self.v.T01, self.v.T02, self.v.T03, self.v.T04, self.v.T05, self.v.T06, self.v.T07]
        self.t_plot.figure.clf()
        self.t_plot.plot_temperature(self.v.stations, self.v.Tplot)

    def plot_pressure(self):
        if self.ab is True:
            self.v.Pplot = [self.v.P00, self.v.P01, self.v.P02, self.v.P03, self.v.P04, self.v.P05, self.v.P06, self.v.P07, self.v.P08]
        else:
            self.v.Pplot = [self.v.P00, self.v.P01, self.v.P02, self.v.P03, self.v.P04, self.v.P05, self.v.P06,
                            self.v.P07]
        self.p_plot.figure.clf()
        self.p_plot.plot_pressure(self.v.stations, self.v.Pplot)

    def plot_contour(self):
        #do tomorrow
        self.c_plot.figure.clf()
        self.c_plot.plot_contour()
        return None



def exit_app():
    app.exit()


def no_file():
    msg = QMessageBox()
    msg.setText('There was No File Selected.')
    msg.setWindowTitle("No File")
    msg.exec_()
    return None

def bad_file():
    msg = QMessageBox()
    msg.setText('Unable to Process the Selected File.')
    msg.setWindowTitle("Bad File")
    msg.exec_()
    return None

if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    main_win = EngineSim()
    sys.exit(app.exec_())