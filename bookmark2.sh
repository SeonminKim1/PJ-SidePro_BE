curl --location --request POST 'http://127.0.0.1:8000/project/1/comment/' \
--header 'X-CSRFToken: AzAIct2PSMKK513Eel5S1zojAzXyms97cGx8q9tf1iKJ9SiL1C9nE4hPICiscsaF' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU5MzY4NzcwLCJpYXQiOjE2NTkzMzI3NzAsImp0aSI6IjU4ZTRiZjJlZGIzYzQ3MDY4YzJiMTdmZDhlNWZmYWIxIiwidXNlcl9pZCI6M30.NxSq4cGPBCSG39b59bwjX5OBWzcSyHPWNXUyScPtPv8' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=AzAIct2PSMKK513Eel5S1zojAzXyms97cGx8q9tf1iKJ9SiL1C9nE4hPICiscsaF' \
--data-raw '{
    "comment" : "ddd"
}'