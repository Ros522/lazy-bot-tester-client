from setuptools import setup, find_packages

__version__ = '0.0.1'

setup(
    name="lazybacktestlob",
    version=__version__,
    author="Ros@Ros_1224",
    description="fast backtest library for limit order book",
    install_requires=["backtestlob @ git+https://github.com/Ros522/backtestlob"],
    packages=find_packages(exclude=('tests', 'docs'))
)
