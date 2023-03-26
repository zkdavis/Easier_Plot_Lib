from setuptools import setup

setup(name='easierplotlib',
version='0.2',
description='Testing installation of Package',
# url='#',
author='Zachary Davis',
author_email='zachkdavis00@gmail.com',
license='MIT',
packages=['Plotter'],
install_requires=[
        "matplotlib>=3.7.1",
        "numpy==1.24.2",
        "scipy>=1.10.1",
        ],
zip_safe=False)
