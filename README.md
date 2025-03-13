# chromesession

`chromesession` is a Python package that provides a convenient contextmanager for managing `selenium` chrome sessions.

In addition, a `CachedSession` is provided to directly cache the driver responses.

## Installation

```cmd
pip install chromesession
```

To use the `chromesession.chrome` contextmanager to use `selenium`, the chromedriver must be installed the system.

Alternatively, you can install the latest chromedriver as extra.

```cmd
pip install chromesession[driver]
```
