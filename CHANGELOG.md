# Change Log

## [0.1.7] - 2021

### Changed

- Update bad point filtering in `get_EBSD_image` to make sure no grain values < 0 are passed out.

## [0.1.6] - 2021.09.24

### Changed

- Add `quat_component_ordering` key to `orientations` sub-dict in `EBSD_image` and `DIC_image` output parameters.

## [0.1.5] - 2021.05.18

### Added

- Add implementation of task `load_microstructure`, method `EBSD`.

### Changed

- Update for latest version of defdap (>0.93).
- Set default values for parameters in input map for task `load_microstructure`, method `EBSD+DIC`.

## [0.1.4] - 2021.01.19

### Changed

- In `get_DIC_image.py` snippet, return `orientations` dict item in a format used in other MatFlow extensions (and return as quaternions).

## [0.1.3] - 2021.01.07

### Added

- Add option to scale the microstructure image produced in `get_DIC_image` snippet.
- Apply rotation of hex unit cell from y // a2 in EBSD data to x // a1 expected by simulation in `get_DIC_image` snippet.

### Fixed

- Change grain numbering to 0-indexed in `get_DIC_image` snippet.

## [0.1.2] - 2020.07.28

### Added

- Add filtering of "bad" voxels in `get_DIC_image` snippet.

### Fixed

- A new `main_func` decorator has been introduced, which allow snippets to contain utility functions, in addition to a main `@main_func`-decoration function, whose inputs and outputs will be parsed for generating the wrapper script.

## [0.1.1] - 2020.06.26

### Fixed

- Fix issue with including snippets in package data.

## [0.1.0] - 2020.06.26

Initial release.
