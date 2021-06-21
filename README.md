# Hinkskalle API

Talking to Hinkskalle made easy

## Config

By default, hinkli reads its config from `~/.hink_api.yml`. This file should look like this:

```yaml
hink_api_base: https://singularity.ngs.vbcf.ac.at
hink_api_key: your_super_secret_token
```

You can use these env variables to override:

- `HINK_API_BASE`
- `HINK_API_KEY`
- `HINK_API_CFG` - to look for the config file in a different location

## Plans

- list collections, containers, images
- download image via manifest
- create download tokens (admin only)
- "fake" (lightweight) oras upload: post blob + manifest

lightweight oras upload:

- pack directory as tar (streaming?)
- push blob
- push manifest (oras)

can I calculate the sha256 when streaming tar upload?