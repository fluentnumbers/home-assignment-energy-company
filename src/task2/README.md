# TASK 2. Acquire data from vendor API

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



## INSTRUCTIONS

#### Prerequisites
- A virtual Python3.10 environment. For instance, using `pipenv install` in the project root
- Rename `.env_template` to `.env`

### Local script
Run `python task2.py`

### Docker
Run
```
docker build . --tag task2
docker run --rm task2
```
