import * as AWS from "aws-sdk";
import { DocumentClient } from "aws-sdk/lib/dynamodb/document_client";
import { Item } from "../model/item";
import { Repository } from "./repository";

const TABLE_NAME = "fake-item";

export class DynamoDBRepository implements Repository {
  
  constructor() {}

  public async get(itemId: string): Promise<Item> {
    const client = new AWS.DynamoDB.DocumentClient();
    const param: DocumentClient.GetItemInput = {
      TableName: TABLE_NAME,
      Key: { itemId },
    };
    const record = await client.get(param).promise();
    return record.Item as Item;
  }

  public async put(item: Item): Promise<void> {
    const client = new AWS.DynamoDB.DocumentClient();
    const param: DocumentClient.PutItemInput = {
      TableName: TABLE_NAME,
      Item: item,
    };

    await client.put(param).promise();
  }

  public async update(itemId: string, attribute: string): Promise<void> {
    const client = new AWS.DynamoDB.DocumentClient();
    const param: DocumentClient.UpdateItemInput = {
      TableName: TABLE_NAME,
      Key: { itemId },
      UpdateExpression: "set #a = :a",
      ExpressionAttributeNames: {
        "#a": "attribute",
      },
      ExpressionAttributeValues: {
        ":a": attribute,
      },
      ReturnValues: "UPDATED_NEW",
    };

    await client.update(param).promise();
  }

  public async delete(itemId: string): Promise<void> {
    const client = new AWS.DynamoDB.DocumentClient();
    const param: DocumentClient.DeleteItemInput = {
      TableName: TABLE_NAME,
      Key: { itemId },
    };

    await client.delete(param).promise();
  }

  public async query(groupId: string): Promise<Item[]> {
    const client = new AWS.DynamoDB.DocumentClient();
    const param: DocumentClient.ScanInput = {
      TableName: TABLE_NAME,
    };
    const data = await client.scan(param).promise();
    return data.Items.filter((item) => item.groupId == groupId).map(item => item as Item);
  }

  public async deleteAll(groupId: string): Promise<void> {
    const client = new AWS.DynamoDB.DocumentClient();
    const param: DocumentClient.ScanInput = {
      TableName: TABLE_NAME,
    };
    const data = await client.scan(param).promise();
    const itemIds = data.Items.filter((item) => item.groupId == groupId).map(item => item.itemId);

    for (const itemId of itemIds) {
      const param: DocumentClient.DeleteItemInput = {
        TableName: TABLE_NAME,
        Key: { itemId },
      };
      await client.delete(param).promise();
    }
  }
}
