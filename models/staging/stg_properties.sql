{{ 
    config(
        materialized='table',
        tags=['staging', 'properties']
    )
}}

-- Remove duplicated rows from raw_properties
WITH source AS (
  SELECT DISTINCT price,
    NULLIF(TRIM(type),'') AS type,
    NULLIF(TRIM(address),'') AS address,
    NULLIF(TRIM(url),'') AS url,
    NULLIF(TRIM(agent_url),'') AS agent_url,
    number_bedrooms,
    full_description,
    NULLIF(TRIM(agent_name),'') AS agent_name,
    NULLIF(TRIM(agent_address),'') AS agent_address,
    NULLIF(TRIM(postcode),'') AS postcode,
    SAFE_CAST( NULLIF(TRIM(longitude), '') AS FLOAT64) AS longitude,
    SAFE_CAST( NULLIF(TRIM(latitude), '') AS FLOAT64) AS latitude,
    NULLIF(TRIM(viewtype),'') AS viewtype,
    NULLIF(TRIM(propertytype),'') AS propertytype,
    NULLIF(TRIM(propertysubtype),'') AS propertysubtype,
    SAFE_CAST( NULLIF(TRIM(added), '') AS DATE FORMAT '%Y%m%d' ) AS added,
    SAFE_CAST(maxsizeft AS FLOAT64) AS maxsizeft,
    SAFE_CAST(retirement AS BOOLEAN) AS retirement,
    SAFE_CAST(preowned AS BOOLEAN) AS preowned,
    input_file_name,
    import_timestamp,
 FROM {{source('rightmove_property', 'raw_properties')}}
)
SELECT * FROM source