# Errata
Here are a few other considerations that have no better place to put them.

[Click here to return to the README](../README.md)

## Use Cases for References
### Reference by Key
The primary (but by no means exclusive) use case envisioned for storing references by key is changing the input and output locations for data, so that you can use the same config file for different instances of an ETL Process.

### Reference by Location
A suggested use case for storing reference by location is to share configuration between different ETL Processes. This can be very useful when standardizing values within the same field and you want to ensure that different ETL Processes use the same standardization.

### Both
Because both references by key and location are separate files from the business logic defined in the configuration, it is supported (and encouraged) to generate these at run-time from a centralized master data management system and/or data catalog.