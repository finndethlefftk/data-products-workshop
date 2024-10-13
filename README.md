# Workshop: Building data products from end-to-end
Material for the data products workshop series for the TK analytics team.


## Run the app

```bash
streamlit run app/main.py
```

## Build the Docker image

```bash
docker build --platform linux/amd64 -t travelperk-prod.registry.snowflakecomputing.com/travelperk/test/toolkit/tk_data_toolkit:latest .
```


## Connect to the Snowflake container registry

```bash
snow spcs image-registry token \
    --connection container_services_sso \
    --format=JSON | \
    docker login travelperk-prod.registry.snowflakecomputing.com \
      --username 0sessiontoken \
      --password-stdin
```

## Push the image to the Snowflake container registry

```bash
docker push travelperk-prod.registry.snowflakecomputing.com/travelperk/test/toolkit/tk_data_toolkit:latest
```

