from setuptools import setup, find_packages

setup(
    name='FSHD',
    version='0.0.1',
    description='FSHD Command-line tool',
    py_modules=["FSHD"],
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'FSHD=FSHD:main',
        ],
    },
)
