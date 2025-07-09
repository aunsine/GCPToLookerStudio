{{ 
    config(
        materialized='view',
        tags=['staging', 'properties']
    )
}}

with source AS (
    SELECT agent_name, agent_address, agent_url 
    FROM {{source('rightmove_property', 'raw_properties')}}
    GROUP BY 1,2,3
)
