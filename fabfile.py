from __future__ import print_function
from fabric.api import *
from fabric.colors import green
from fabric.contrib.console import confirm
from contextlib import contextmanager as _contextmanager

application_description = """
  This wizard will ask you a series of questions it will use to generate a
standarized Django skeleton application. The Django application can be run 
locally, for testing, with a default site or imported into another Django 
application. A disutils setup.py file will also be configured and setup.

For the sake of simplicity, I am assuming you cloned this skeleton from a git
repository somewhere. Therefore, I am also assuming you have the following 
fils in this directory:
    * .gitignore
    * libraries.txt
    * libraries-vcs.txt
    * README.md

Let's get started!
"""

setup_py_base = """
import os, sys

try:
    from setuptools import setup
except:
    from distutils.core import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def read_requirements(fname):
    f = open(os.path.join(os.path.dirname(__file__), fname))
    return filter(lambda f: f != '', map(lambda f: f.strip(), f.readlines()))

setup(
    zip_safe = False,
    name = "{name}",
    version = "{version}",
    author = "{author}",
    author_email = "{author_email}",
    description = "{short_description}",
    keywords = "",
    packages=['{package_name}'],
    long_description=read('README.md'),
    install_requires = read_requirements('libraries.txt'),
    test_suite = "dummy",
)
"""

@_contextmanager
def virtualenv(virtualenv_dir):
    with prefix('. ' + virtualenv_dir + '/bin/activate'):
        yield

def start():
    print(green("Hello! Welcome to the Django-App skeleton application"))
    print(application_description)
    
    print("All the following values can be updated by modifying setup.py")
    
    application_name = prompt("Application name:")
    package_name = prompt("Package name:", default=application_name)
    version = prompt("Version:", default="1.0.0")
    with hide('running'):
        author = local('git config user.name', capture=True)
        email = local('git config user.email', capture=True)
    author = prompt("Author:", default=author)
    email = prompt("Author email:", default=email)
    short_description = prompt("Short description:")
    
    print("Alright! Creating the setup.py file: ", end='')
    f = open('setup.py', 'w')
    f.write(
        setup_py_base.format(
            name=application_name,
            package_name=package_name,
            version=version,
            author=author,
            author_email=email,
            short_description=short_description
        )
    )
    print("done!")
    
    setup_virtualenv()

def setup_virtualenv():
    print("Time to create the Python virtual environment")
    print("This makes it easier to manage multiple applications")
    env_name = prompt("Environment name:", default="python")
    
    local('virtualenv ' + env_name)
    
    with virtualenv(env_name):
        local('pip install -r libraries.txt')