from setuptools import setup, find_packages

setup(
    name='Movies',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'movies_stats=movies_stats:main',
        ],
    },
    description='A package for analyzing movies dataset',
    author='Thomas Eleftheriadis',
    author_email='eleftheriadis.thomas@gmail.com',
    url='https://github.com/Elefthom/Movies_Stats',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)