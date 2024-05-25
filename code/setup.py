from setuptools import setup  # type: ignore

setup(
    name="Constraint Based Simulator",
    version="0.1.0",
    description="User friendly interface for a constraint satisfaction physics simulator",
    author="EmmanuelMess",
    packages=["constraint_based_simulator"],
    install_requires=["numpy", "lark", "PySide6"],
)
