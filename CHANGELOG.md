# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [1.3.0] - 2023-01-14

### Added

- Added `bipartite` function to topology module
- Added `complete` function to topology module
- Added `lattice_pos` function to vis module
- Added demo for flocking
- Added demo for restricted Boltzmann machine
- Added demo for optimizing particle swarms
- Added demo for multilayer perceptron
- Added demo for Lorenz attractor

### Changed

- Changed `animate_network`: added `with_timesteps` and `show` parameters
- Changed `animate_activities`: added `with_timesteps` and `blit` parameters

## [1.2.0] - 2022-12-22

### Added

- Added `CHANGELOG.md`
- Added `MemoizationKey` and memoization support
- Added demo for functional network automata
- Added demo for evolving networks

### Changed

- Moved version to `__netomaton/__init__.py`
- Explicitly importing symbols instead of using `*` in `__ini__.py` files
- Making `_bits_to_int` and `_int_to_bits` public
- Changed `binary_ca_rule`: no longer shifting neighbourhood activities to center
- Changed `Network`: adding `rotation_system` property
- Changed `evolution.py`: adding support for memoization and rotation systems

### Removed

- Removed `shift_to_center`

## [1.1.2] - 2022-05-25

### Changed

- Fixed problem in `game_of_life_rule`

## [1.1.1] - 2021-08-01

### Changed

- Loosened some dependency requirements in `setup.py`

## [1.1.0] - 2021-07-24

### Added

- Added support for CTRBL rules
- Added Langton's Loop implementation

## [1.0.0] - 2021-07-04

### Added

- Initial stable release
