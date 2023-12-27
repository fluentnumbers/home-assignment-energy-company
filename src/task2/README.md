# Task 2

## Acquire data from vendor API

Our supplier of high quality, curated country data no longer provides access to a file-based dataset (csv). Instead, they request you the gather this data through their next-generation data broker platform, in exchange for a detailed overview of revenues generated from this data.

a. Gather country data for every country, that has an airport (use [countries.csv](https://sacodeassessment.blob.core.windows.net/public/countries.csv)/[airports.csv](https://sacodeassessment.blob.core.windows.net/public/airports.csv) datasets), and store this in a single file. Which countries information is missing from the broker platform?

b. Upload an empty file named 'revenues.txt' to the upload endpoint (HTTP POST).

Details;
```
client id                   : abc123
host address                : code001.ecsbdp.com
HTTP path (get country info): /countries/{iso_code}
HTTP path (upload data)     : /revenues?client={client_id}
```

## How-to

### Prerequisites

- A virtual Python3.10 environment. For instance, using `pipenv install` in the project root
- Rename `.env_template` to `.env`

### Run as a local script

Run [task2.py](task2.py): `python src/task2/task2.py`


### Deploy in a Docker container

Use [Dockerfile](./Dockerfile) to run the script in a container environment:

```bash
cd src/task2
docker build . --tag task2
docker run --rm task2
```

## Results

### Task 2-A
>
> [!COUNTRIES WITH MISSING INFO]
> - Côte d'Ivoire
> - Namibia

### Task 2-B

An empty file `revenues.txt` uploaded to the endpoint.

### Implemented

#### :heavy_check_mark: Primary functionality

- load data from a local or web path into dataframes
- filter\merge data to get a list of countries of interest
- query a web service for countries' info
- store outputs locally as a .csv file
- upload a file to a web service (Task 2b)

#### :heavy_check_mark: Secondary functionality

- .env file for configuration and env variables
- event logging
- solution packaged as a Docker container


#### ⬜ TODO ideas

- wrap task2.py as a Fast API to trigger data processing and uploading by request (also inside Docker)
- wrap task2.py into a Prefect flow (or Cron job) to schedule and log runs
- tests, status health-checks for data sources, etc.
