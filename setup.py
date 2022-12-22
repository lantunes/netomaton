from setuptools import setup, find_packages
import re

INIT_FILE = "netomaton/__init__.py"

with open(INIT_FILE) as fid:
    file_contents = fid.read()
    match = re.search(r"^__version__\s?=\s?['\"]([^'\"]*)['\"]", file_contents, re.M)
    if match:
        version = match.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s" % INIT_FILE)

packages = find_packages(exclude=("tests", "demos", "doc", "resources",))

setup(name="netomaton",
      version=version,
      description="Netomaton, A Python library for working with Network Automata.",
      long_description="Netomaton is a Python framework for exploring discrete dynamical network systems, "
                       "also known as Network Automata. It is a software abstraction meant to aid in the "
                       "implementation of models of collective computation",
      license="Apache License 2.0",
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
      ],
      url='http://github.com/lantunes/netomaton',
      author="Luis M. Antunes",
      author_email="lantunes@gmail.com",
      packages=packages,
      keywords=["network automata", "cellular automata", "complexity", "complex systems", "computation", "non-linear dynamics"],
      python_requires='>3.5.2',
      install_requires=["numpy >= 1.15.4", "matplotlib >= 3.0.2", "networkx >= 2.2", "scipy >= 1.3.1", "msgpack >= 1.0.2"])
