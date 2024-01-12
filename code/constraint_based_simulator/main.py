from constraint_based_simulator.input_reader.SimulationFile import SimulationFile
from constraint_based_simulator.ui.MainApp import MainApp


def main():
    SimulationFile("../../examples/example3.simulation")
    return MainApp().run()


if __name__ == '__main__':
    main()
