{{ 
    config(
        materialized='table',
        tags=['staging', 'properties']
    )
}}

WITH source AS (
    SELECT 
    NULLIF(TRIM(agent_name),'') AS agent_name,
    NULLIF(TRIM(agent_address),'') AS agent_address,
    NULLIF(TRIM(agent_url),'') AS agent_url, 
    FROM {{source('rightmove_property', 'raw_properties')}}
    WHERE NULLIF(TRIM(agent_name),'')  IS NOT NULL
    GROUP BY 1,2,3
)
SELECT * FROM source