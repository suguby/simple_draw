import os

from setuptools import setup


README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='simple_draw',
    version='2.7.0',
    py_modules=["simple_draw"],
    license='BSD License',
    description='This package allows you to draw graphical primitives with pygame.',
    long_description=README,
    url='https://github.com/suguby/simple_draw',
    author='Shandrinov Vadim',
    author_email='suguby@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Topic :: Education',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='draw graphical primitives tutorial',
    install_requires=[
        'pygame==2.0.0'
    ]
)
