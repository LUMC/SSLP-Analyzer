from setuptools import setup, find_packages

setup(
    name='FSHD',
    version='0.0.1',
    description='FSHD Command-line tool',
    py_modules=["FSHD"],
    packages=find_packages(),
    include_package_data=True,
    package_data={"FSHD": ["haplotypes.json"]},
    install_requires=[
        "questionary"
    ],
    entry_points={
        'console_scripts': [
            'FSHD=FSHD.FSHD:main',
        ],
    },
)
