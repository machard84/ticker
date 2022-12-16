# FTSE index data grab and store
## Synopsis
This project uses the yahoo_fin Python module to access the stock market tickers for the FTSE100 and FTSE250 indexes and collate the data into InfluxDB for processing.

## Requirements
- docker
- docker-compose

## How to:
### To build the project run:
> docker-compose build

### To deploy:
> docker-compose up

### Once deployed visit:
http://localhost:8161 and setup the database

### Fetch the new user token from:
While the web console is open, fetch the new user "Load Data" token from:
> Data > Tokens

### Update ticker container environment variables 
Modify the following environment variables in docker-compose.yml for the ticker service using the data supplied to InfluxDB during setup:
- AUTH_TOKEN
- BUCKET
- ORG_NAME

The "PERIOD" variable is used to set the frequency of fetch and can be lowered if necessary


### Refresh the running containers:
After updating the environment variables it is essential to restart the running containers
> docker-compose build --up
