{{ 
    config(
        materialized='incremental',
        tags=['serving', 'properties'],
        incremental_strategy='merge',
        unique_key= ['url'],
        partition_by={
            "field": "added",
            "data_type": "date",
            "granularity": "day"
        },
        post_hook= ['DELETE FROM {{this}} WHERE url IS NULL OR price IS NULL' ]

    )
}}

SELECT *, 
SAFE_DIVIDE(price, maxSizeFt) AS cost_per_feet,
FROM {{ref('stg_properties')}}
{% if is_incremental() %}
WHERE added > (SELECT MAX(added) FROM {{ this }})
{% endif %}