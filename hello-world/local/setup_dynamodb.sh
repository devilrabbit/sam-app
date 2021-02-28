# !/bin/bash

set -e

# 前回のコンテナが残っていた場合は一度破棄する
REF=$(docker ps -q --filter ancestor=amazon/dynamodb-local)
if [ -n "$REF" ]; then
  docker rm -f $REF
fi
docker run -d -p 8000:8000 amazon/dynamodb-local -jar DynamoDBLocal.jar -inMemory -sharedDb

# create table
aws dynamodb create-table \
  --endpoint-url http://localhost:8000 \
  --cli-input-json file://$(pwd)/local/table.json

# insert dummy item
aws dynamodb batch-write-item \
  --endpoint-url http://localhost:8000 \
  --request-items file://$(pwd)/local/items.json