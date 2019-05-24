# Simulation entities

The simulation manages the following entities (represented as Python classes)

## Vehicle

An entity that represents any transit vehicle that moves along a fixed route
according to a schedule.

- `vehicle_id` (*string*): A unique ID for the `Vehicle` in the simulation
- `capacity` (*int*): The maximum number of `Passenger` instances that can ride a `Vehicle` simultaneously.
- `trip_id` (*string*): A unique ID for a trip in the `GTFS` which indicates the trip to which the `Vehicle` instance is currently assigned.
- `passengers` ([*string*]): A list of unique IDs for the `Passenger` instances riding the `Vehicle`.

## Passenger

An entity that represents a single person traversing a transit system

- `passenger_id` (*string*): A unique ID for the `Passenger` in the simulation.
- `destination_id ` (*string*): A unique ID for a `Stop` indicating where the `Passenger` is going. Transfers are not currently implemented or planned.

## Stop

- `stop_id` (*string*): A unique ID for the `Stop` in the simulation.
- `passengers` ([*string*]): A list of unique IDs for the `Passenger` instances waiting at the `Stop`.
