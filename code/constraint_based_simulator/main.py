from constraint_based_simulator.input_reader.Parser import Parser
from constraint_based_simulator.ui.MainApp import MainApp


def main():
    Parser().readFile("../../examples/example2.simulation")
    return MainApp().run()


if __name__ == '__main__':
    main()
