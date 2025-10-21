# Next-Busses - A webapp for tracking the arrival time of *CT Transit* busses at official stops

### This app is meant as a privacy-minded alternative to Google Maps for finding when the bus will be next arriving at your stop.

### Current Features (Main Branch)
- GUI made with Tkinter Python library, and bus data fetched using Google-Maps API; app use requires a personal Google-Maps-Routes API key and the creation of a local file with individual bus-stop information.
  - The setup process for this version can quickly become cumbersome, and so this version will soon be retired in favor of a webapp version with expanded functionality.

### Planned Upcoming Features:
- **Migrate-Google-to-GTFS** branch:
  - Move from using Google API to using GTFS data from *CT Transit* directly
  - Web interface for users to search for routes+stops
- Other future updates:
  - Functionality for pinning information about selected stops for the duration of the session
