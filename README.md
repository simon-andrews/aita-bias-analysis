# AITA Bias Analysis

In our project, we aim to investigate whether there are factors that influence the final outcome of a thread other than the conflict described by the original poster

## Poetry Installation

This project uses Poetry to manage dependencies.

For Linux, macOS, Windows (WSL):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## To Collect the Data

```bash

# installs dependencies
poetry shell 
poetry install 

# runs the data collector, dates are in YYYY-MM-DD format 
poetry run python data_collector.py [Start Date] [End Date]
```

## ISC License

_Copyright (c) 2022 Sarah Akbar, Simon Andrews, Prakamya Mishra, and Rohan Mittal_

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
