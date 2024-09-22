from distutils.core import setup
from setuptools import find_packages
import os

# Optional project description in README.md:
current_directory = os.path.dirname(os.path.abspath(__file__))

try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    name='medmolnet',
    version='1.0.4',
    description='create sub networks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Tohar&Ayelet',
    author_email='Toharbk@gmail.com',
    url='https://github.com/Tohar-Ts/Towards-personalized-medicine-in-cancer',
    project_urls={
        "Bug Tracker": "https://github.com/Tohar-Ts/Towards-personalized-medicine-in-cancer/issues",
    },
    # List project dependencies:
    install_requires=[
        'networkx',
        'pandas',
        'xlsxwriter',
        'requests',
        'patool',
        'psycopg2',
        'configparser',
        'pyvis',
        'numpy'
    ],

    # https://pypi.org/classifiers/
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)
