################################################################################
#
# Copyright 2022-2025 Vincent Dary
#
# This file is part of FII.
#
# FII is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation
# , either version 3 of the License, or (at your option) any later version.
#
# FII is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# FII. If not, see <https://www.gnu.org/licenses/>.
#
################################################################################

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FII",
    version="0.1",
    author="Vincent Dary",
    author_email="",
    description="FII: Firmware Instrumentation and Introspection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FirmwareCrunch/FII",
    project_urls={
        "Bug Tracker": "https://github.com/FirmwareCrunch/FII/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8.16",
    install_requires=[
        'unicorn ==2.0.1',
        #'unicorn @ git+https://github.com/unicorn-engine/unicorn.git@dev#subdirectory=bindings/python',
        # 'angr',
        'capstone ==4.0.2',
        'pycparser ==2.20',
        'pycparserext==2021.1',
        'cmsis-svd @ git+https://github.com/cmsis-svd/cmsis-svd.git@ca0b0b0#subdirectory=python',
        'ipython ==7.26.0',
        'ipykernel==6.29.4',
        'background-zmq-ipython==1.20220901.135250',
        'Cerberus ==1.3.5',
        'PyYAML ==6.0',
        'tabulate ==0.9.0',
        'seaborn ==0.13.0',
        'plotext ==5.2.8'
    ],
    extras_require={
        "DEV": [
            'pytest ==7.4.0',
            'pytest-cov ==4.1.0',
            'pyelftools ==0.29',
        ]
    },
    entry_points={
        'console_scripts': [
            'FII=FII.scripts.FII:main'
        ]
    },
    zip_safe=False,
    package_data={
        'FII': ['py.typed'],
    },
)
