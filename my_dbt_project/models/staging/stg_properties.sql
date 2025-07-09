{{ 
    config(
        materialized='incremental',
        file_format='parquet',
        incremental_strategy='merge',
        unique_key='property_id',
        tags=['staging', 'properties'],
        schema='staging'
    )
}}

with source AS (
    SELECT * FROM {{source('rightmove_property', 'raw_properties')}}
)