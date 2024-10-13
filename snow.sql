-- Use the accountadmin role
-- This is necessary to create the image repository
USE ROLE accountadmin;

-- Specify the schema to use
USE DATABASE travelperk;
USE SCHEMA test;

-- Create the image repository
CREATE IMAGE REPOSITORY IF NOT EXISTS toolkit;

-- Show the uploaded image
SELECT SYSTEM$REGISTRY_LIST_IMAGES('/travelperk/test/toolkit');

-- Create a compute pool
CREATE COMPUTE POOL IF NOT EXISTS analytics
    MIN_NODES = 1 MAX_NODES = 2
    INSTANCE_FAMILY = cpu_x64_xs
    AUTO_SUSPEND_SECS = 60;

-- Show the compute pool
DESC compute pool analytics;

-- Create the service
GRANT OWNERSHIP ON IMAGE REPOSITORY travelperk.test.toolkit TO ROLE container_services_role;

USE ROLE container_services_role;

CREATE SERVICE tk_data_toolkit
IN COMPUTE POOL analytics
FROM SPECIFICATION $$
    spec:
      containers:
      - name: tk-data-toolkit
        image: /travelperk/test/toolkit/tk_data_toolkit:latest
        secrets:
        - snowflakeSecret: travelperk.public.openai_api_data_analytics
          secretKeyRef: secret_string
          envVarName: openai_api_key
      endpoints:
      - name: tk-data-toolkit
        port: 8501
        public: true
      
$$
EXTERNAL_ACCESS_INTEGRATIONS = ( openai_apis_access_integration )
AUTO_RESUME = true
MIN_INSTANCES = 1 MAX_INSTANCES = 4
QUERY_WAREHOUSE = container_services_wh;

-- Monitor the service
CALL SYSTEM$GET_SERVICE_STATUS('tk_data_toolkit');
SHOW SERVICES;
DESC SERVICE tk_data_toolkit;
SHOW ENDPOINTS IN SERVICE tk_data_toolkit;

-- Shut down the service
ALTER SERVICE tk_data_toolkit SUSPEND;

-- Refresh the service with the latest image
USE ROLE container_services_role;

ALTER SERVICE travelperk.test.tk_data_toolkit
FROM SPECIFICATION $$
    spec:
      containers:
      - name: tk-data-toolkit
        image: /travelperk/test/toolkit/tk_data_toolkit:latest
        secrets:
        - snowflakeSecret: travelperk.public.openai_api_data_analytics
          secretKeyRef: secret_string
          envVarName: OPENAI_API_KEY
      endpoints:
      - name: tk-data-toolkit
        port: 8501
        public: true
      
$$;
