from setuptools import setup, find_packages

setup(
    name='ntc',  # This is the name of the package to be imported
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'colormath',
    ],
    test_suite='tests',
    url='https://github.com/gizmore/python-name-that-color',
    author='gizmore',
    author_email='gizmore@wechall.net',
    description='A color naming and shade matching library. Converted to python from name-that-color-and-hue-i18n javascript by ChatGPT.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: CC2',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)