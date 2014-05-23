# PTP

Pentester's tools parser provides an unified way to retrieve the information
from all (final goal) automated pentesting tools.

# General

This standalone library is created in order to be used by
[OWTF](https://github.com/owtf) when it will try to retrieve the automated
rankings already provided by some pentesting tools.

# Features

+ Auto-detection of the tool that generated the report.

# Usage

```python
from __future__ import print_function
from ptp import PTP


if __name__ == '__main__':
    ptp = PTP()
    ptp.parse(
        path_to_report='path/to/the/report/directory',
        filename='report_name.xml')
    print('Highest severity:', ptp.get_highest_ranking())
```

# Current support

+ arachni (0.4.6) (XML report)
    + Metadata
    + Rankings
+ skipfish (2.10b)
    + Metadata
    + Rankings
+ w3af (1.6.0.2) (XML report)
    + Metadata
    + Rankings
+ wapiti (2.3.0) (XML report)
    + Metadata
    + Rankings (database needs to be completed though)
    + Names
    + Descriptions
