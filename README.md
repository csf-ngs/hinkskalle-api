# Hinkskalle API

Talking to [Hinkskalle](https://github.com/csf-ngs/hinkskalle) made easy

Use me to 

- list available downloads
- download data
- upload data

## Getting Started

hinkskalle-api provides

- a small library with a thin wrapper over the JSON API 
- a CLI (`hinkli`: short for hink-cli, get it?)

### Installation

You will need python3 and pip. Then you can run:

```bash
pip3 install git+https://github.com/csf-ngs/hinkskalle-api
```

### Command Line Interface

Get a list of available commands and options:

```bash
hinkli --help
```
Your first step should be logging in:

```bash
# non-VBCF.NGS users get your own instance!
hinkli --base https://singularity.ngs.vbcf.ac.at/ login
# answer prompt for username and password
```

The registry and token should now be stored in `~/.hink_api.yml` and available for further use.

#### Discovering & Downloading Data

Your most likely use case will be downloading data provided via Hinkskalle.

```bash
# shoows available collections of containers
hinkli list-collections
hinkli list-containers [collection]
hinkli list-downloads [collection]/[container]
hinkli pull [collection]/[container]:[tag]
# username is optional, but can be provided, too:
hinkli list-collections test.hase
hinkli list-containers test.hase/[collection]
# etc
```

Basic structure:

- A Collection holds a bunch of containers (topic, type, ...)
- Containers hold tagged data
- Each tag points to some data (some tags point to the same data)

If Hinkskalle shows you these downloads in your container `test.hase/example/FAQ4711`:

```yaml
- filename: bunch_of_reads.fastq.gz
  size: 41.5 MB
  tags: basecalled,20210621
- filename: rawdata.tar.gz
  size: 41.5 TB
  tags: raw
```

You can use these commands to download:

```bash
# either one fetches bunch_of_reads.fastq
hinkli pull example/FAQ4711:basecalled
hinkli pull example/FAQ4711:20210621
# fetches rawdata.tar.gz
hinkli pull example/FAQ4711:raw
```

Hinkli will even check the sha256 checksum for you!

### API

Not documented - use at your own risk!

```python
from hinkskalle_api import HinkApi
api = HinkApi()
collections = api.list_collections()
# etc
```

## Configuration

By default, hinkli reads its config from `~/.hink_api.yml`. This file should look like this:

```yaml
hink_api_base: https://singularity.ngs.vbcf.ac.at
hink_api_key: your_super_secret_token
```

You can use these env variables to override:

- `HINK_API_BASE`
- `HINK_API_KEY`
- `HINK_API_CFG` - to look for the config file in a different location
