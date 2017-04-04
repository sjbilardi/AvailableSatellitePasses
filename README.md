# Compare Available Satellite Passes
Use chain access reports from STK exported in CSV format and compare available satellite passes for different locations. Plots show the days in the year in which ideal passes occur. Example plots exported in "availabilityPlots" folder.

Example data is in the "examplePasses" folder. Using STK, a chain access report for all 66 Iridium constellation satellites, saved in CSV format, was generated over one year for the following site locations:

- Daytona Beach, Florida
- Prescott, Arizona
- Boulder, Colorado
- Seattle, Washington
- Fairbanks, Alaska

Accepted passes were based off the following contrainsts:

- Satellite was in direct sunlight
- Time of day for site location was either dawn, dusk or night
- Satellite pass was 10 degrees above horizon
- Satellite pass was over 1 minute

## Instructions for Running 

All Python files are configured to use the files in the "examplePasses" folder. To run the entire script:

1. Run "separateSatellites.py"
2. Run "CompareAvailablePasses.py"
