import { localConfigure } from './util/local';
if (process.env.AWS_SAM_LOCAL) {
  localConfigure();
}

import { APIGatewayEvent, Context } from 'aws-lambda';
import { WebClient } from './client/webclient';
import { UUID } from './util/uuid';

// #!if mock
import mock from './mocks/$mock'
import axios from 'axios';
mock(axios);
// #!endif

const handler = async (event: APIGatewayEvent, context: Context) => {
  const client = new WebClient('https://example.com/');
  let response = await client.createGroupAsync({});

  const groupId = response.groupId;
  response = await client.createItemAsync(groupId, { attribute: 'c' });

  const itemId = response.itemId;
  response = await client.updateItemAsync(itemId, 'x');

  response = await client.getItemAsync(itemId);
  const item = response;

  response = await client.listItemsAsync(groupId);
  const items = response;

  response = await client.deleteItemAsync(itemId);
  response = await client.deleteGroupAsync(groupId);

  const result = {
    groupId: UUID.shorten(groupId),
    itemId: UUID.shorten(itemId),
    item,
    items
  };

  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json;charset=UTF-8'
    },
    body: JSON.stringify(result)
  };
};

export {handler};