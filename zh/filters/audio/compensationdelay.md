# compensationdelay

Compensation Delay Line is a metric based delay to compensate differing positions of microphones or speakers.

For example, you have recorded guitar with two microphones placed in different locations. Because the front of sound wave has fixed speed in normal conditions, the phasing of microphones can vary and depends on their location and interposition. The best sound mix can be achieved when these microphones are in phase (synchronized). Note that a distance of ~30 cm between microphones makes one microphone capture the signal in antiphase to the other microphone. That makes the final mix sound moody. This filter helps to solve phasing problems by adding different delays to each microphone track and make them synchronized.

The best result can be reached when you take one track as base and synchronize other tracks one by one with it. Remember that synchronization/delay tolerance depends on sample rate, too. Higher sample rates will give more tolerance.

The filter accepts the following parameters:

- **`mm`** Set millimeters distance. This is compensation distance for fine tuning. Default is 0.

- **`cm`** Set cm distance. This is compensation distance for tightening distance setup. Default is 0.

- **`m`** Set meters distance. This is compensation distance for hard distance setup. Default is 0.

- **`dry`** Set dry amount. Amount of unprocessed (dry) signal. Default is 0.

- **`wet`** Set wet amount. Amount of processed (wet) signal. Default is 1.

- **`temp`** Set temperature in degrees Celsius. This is the temperature of the environment. Default is 20.

## Commands

This filter supports the all above options as [commands](#commands).
