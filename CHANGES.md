# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3] - 2019-05-20
### Added
- Fixed bugs in RSC/ECS parser (almost rewrote it).
- Fixed bugs in Nature parser (almost rewrote it).
- Added CHANGES.md to track all changes in LimeSoup.
- Added unit tests for Wiley, Springer, APS, Nature, RSC, ECS.
- Implemented parsers for Wiley, Springer, and APS.
- Added worker class using `synthesis-api-hub` to serve the parser in parallel computing environments.

## [0.2.2] - 2018-10-27
### Added
- Implemented parsers: RSC, Wiley, Nature, ECS, ACS.
- On-going parsers: Springer, Wiley
