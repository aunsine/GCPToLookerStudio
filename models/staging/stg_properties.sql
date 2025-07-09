{{ 
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='property_id',
        tags=['staging', 'properties']
    )
}}

with source AS (
    SELECT * FROM {{source('rightmove_property', 'raw_properties')}}
)
select * from source
{% if is_incremental() %}
where property_id NOT IN (select property_id from {{ this }})
{% endif %}
