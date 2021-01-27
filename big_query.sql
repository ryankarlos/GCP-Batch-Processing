
CREATE OR REPLACE TABLE `lbghack2021team7.stage.stage_hotels` AS
SELECT
string_field_0 AS Name,
string_field_1 AS Location,
SAFE_CAST(string_field_2 AS int64) AS PriceDollars,
SAFE_CAST(string_field_3 AS int64) AS Duration,
string_field_4 AS RoomType,
SAFE_CAST(string_field_5 AS int64) AS Beds,
SAFE_CAST(string_field_6 AS float64) AS Rating,
string_field_7 AS  RatingTitle,
SAFE_CAST(string_field_8 AS int64) AS RatingNumber,
FROM `lbghack2021team7.stage.stage_hotels`
WHERE string_field_9 IS NULL