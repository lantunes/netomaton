from setuptools import setup

setup(name="netomaton",
      version="0.1.0",
      description="Netomaton, A Python library for working with Network Automata.",
      long_description="Netomaton is a Python framework for exploring discrete dynamical network systems, "
                       "also known as Network Automata. It is a software abstraction meant to aid in the "
                       "implementation of models of collective computation",
      license="Apache License 2.0",
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
      ],
      url='http://github.com/lantunes/netomaton',
      author="Luis M. Antunes",
      author_email="lantunes@gmail.com",
      packages=["netomaton"],
      keywords=["network automata", "cellular automata", "complexity", "complex systems", "computation", "non-linear dynamics"],
      python_requires='>3.5.2',
      install_requires=["numpy >= 1.15.4", "matplotlib >= 3.0.2", "networkx == 2.2"])