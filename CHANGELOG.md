# Changelog

## [0.4.2] - 2019-10-03

### Added

- Added `custom_id` argument for workflow schedule.
- Dispatch of tasks and workflows are now done using the API instead of a local agent.
- Pause, Resume and Kill workflows are now done using the API instead of a local agent.
- Send event to workflow is now done using the API instead of a local agent.
- Find workflow is now done using the API instead of a local agent.

## [0.4.1] - 2019-09-25

### Added

- Added a `intent_id` property when dispatching workflows and tasks, sending events to workflows, and
  pausing/resuming/killing workflows.
- Execution context for tasks and workflows
- Optional `on_error_retry_delay` method handling task failures and specifying
  how many seconds to wait before retrying.

## [0.4.0] - 2019-08-26

### Added

- Added a `intent_id` property when dispatching workflows and tasks, sending events to workflows, and
  pausing/resuming/killing workflows.

- Added scheduling: `schedule(cron)`

## [0.3.4] - 2019-07-01

### Added

- Run tests in a continuous integration flow.
- No need for credentials when this lib is running in a Zenaton agent except if dispatching a
  sub-job.

## [0.3.3] - 2019-06-25

## Fixed

- Fix a typo in client.py that prevents correct executions of versions

## [0.3.2] - 2019-06-21

## Fixed

- Calling `day_of_month` on a wait task now waits for to wait for the next day having the requested day number, even if that means waiting for next month. (i.e calling Wait().day_of_month(31) on February, 2nd will wait for March, 31st)
- Fixed Wait task behavior in some edge cases
- Encodes HTTP params before sending request

### Added

- Added `event_data` property when sending event.

## [0.3.1] - 2019-04-26

## Fixed

- Fixed `MANIFEST.in` file not included files required by `setup.py`.

## [0.3.0] - 2019-03-25

### Added

- Calling `dispatch` on tasks now allows to process tasks asynchronously

### Fixed

Fixed Wait task behavior in some edge cases
Encodes HTTP params before sending request

## [0.2.5] - 2018/10/17

Object Serialization (including circular structures)

## [0.2.4] - 2018/09/26

Enhanced WithDuration & WithTimestamp classes

## [0.2.3] - 2018/09/21

Minor enhancements (including the workflow find() method)

## [0.2.2] - 2018/09/19

New version scheme management

## [0.2.1] - 2018/09/17

Reorganized modules

## [0.2.0] - 2018/09/14

Full rewriting of the package
