# lap_analyzer

This project aims to simplify the process of taking in recorded video from a track session and determining the lap times achieved during that session.

## Usage

### Requirements

The dependencies required by the project can be installed with pip:

```bash
python3 -m pip install -r requirements.txt
```

### Configuration
To use this utility, you must first define a config YAML (e.g. cfg.yml)

```yaml
inputs:
  - description: 'Dash Camera'
    file_name: '/path/to/session.mp4'
```

### Running The Utility

```bash
python main.py -c cfg.yml
```

#### UI Controls

| key | description | 
| ---|---|
| `d` | scrubs forward so you don't have to wait for the lap start/end point | 
| `a` | scrubs backward in case you overshoot the lap start/end point | 
| `w` | slows down playback to help time the lap start/stop event | 
| `space` |  triggers the lap start/stop event | 
| `f` | based on the average lap time, scrubs ahead 95% of the way to the next estimated start/stop event | 
| `q`| quits the program | 

#### Outputs

Once at least 2 lap start/stop events have been recorded, the utility will start printing each lap's time to stdout each time the space bar is pressed. Once the user stops playback (with `q`) or the video reaches its endpoint, the fastest lap time of the session is printed to to stdout.