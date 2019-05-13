# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Fixed bugs in RSC parser (almost rewrote it).
- Fixed bugs in Nature parser (almost rewrote it).
- Added CHANGES.md to track all changes in LimeSoup.
- Added unit tests for Wiley, Springer, Nature, RSC.
- Implemented parsers for Wiley and Springer.
- Added worker class using `synthesis-api-hub` to serve the parser in parallel computing environments.

## [0.2.2] - 2018-10-27
### Added
- Implemented parsers: RSC, Wiley, Nature, ECS, ACS.
- On-going parsers: Springer, Wiley
