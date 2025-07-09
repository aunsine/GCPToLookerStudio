{{ 
    config(
        materialized='table',
        incremental_strategy='merge',
        tags=['staging', 'properties']
    )
}}

with source AS (
    SELECT DISTINCT * FROM {{source('rightmove_property', 'raw_properties')}}
)
