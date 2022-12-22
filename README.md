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

# runs the data collector to download data from the internet.
# dates are in YYYY-MM-DD format 
python aita_bias_analysis/data_collector.py [Start Date] [End Date]

# run the data loader to collect everything into a single csv file
python aita_bias_analysis/data_loader.py
```

To run the loader, you must have Reddit API access, and set the following environment variables
 - `REDDIT_CLIENT_ID`
 - `REDDIT_SECRET_KEY`
to the values given to you by Reddit.

## Using the provided data.csv (recommended)
Download `data.csv` from the Google Drive folder and place it in the root of this repository.

## Running this code
Most of our analysis is in Jupyter notebooks, which can be opened an run like any other Jupyter notebook.

If you chose to use Jupyter to install this project's dependencies, you will need to create a new Jupyter kernel that points to this the VirtualEnv's interpreter: `poetry run python -m ipykernel install --user --name aita-bias-analysis`, then use that kernel to run the notebooks instead of the default one.

## ISC License

_Copyright (c) 2022 Sarah Akbar, Simon Andrews, Prakamya Mishra, and Rohan Mittal_

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
