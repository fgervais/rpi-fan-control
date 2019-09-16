# Raspberry Pi PWM fan control


## Hardware

Connect the gate of an N-channel mosfet to pin GPIO 12, the souce to ground
and connect the drain to the pin 4 of a PWM PC fan.

## Configuration

The default is really basic but should do a decent job.

However, you can change the control points by changing config.yml and
rebuilding the image.

## Build and Run

```
docker-compose build
docker-compose up
```

## Build and Run (developer mode)

```
docker-compose -f docker-compose.yml -f docker-compose.dev.yml build
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

You'll run the code from the source directory and you'll get free verbose
output.
