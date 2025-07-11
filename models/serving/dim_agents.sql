{{ 
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='agent_name',
        tags=['serving', 'properties']
    )
}}

SELECT agent_name, agent_address, agent_url
FROM {{ref('stg_agents')}}
{% if is_incremental() %}
WHERE agent_name NOT IN (SELECT agent_name FROM {{ this }})
{% endif %}