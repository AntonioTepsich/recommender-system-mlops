SELECT CAST(user_id as INT),
    CAST(movie_id as INT),
    CAST(rating as INT),
    CAST("Unnamed: 0" as INT) as unnamed,
    TO_DATE("Date", 'YY-MM-DD') as date

FROM {{ source('recommender_system_raw', 'scores') }}