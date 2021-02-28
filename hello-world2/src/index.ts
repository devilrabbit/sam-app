import { APIGatewayEvent, Context } from 'aws-lambda';

const handler = async (event: APIGatewayEvent, context: Context) => {

  const state = event.queryStringParameters['state'] as string;
  const sessionId = event.queryStringParameters['sessionId'] as string;

  const ids = sessionId.split('.');
  const groupId = ids[0];
  const itemId = ids[1];

  const result = {
    state,
    groupId,
    itemId
  };

  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json;charset=UTF-8',
      'Set-Cookie': `TOKEN=${sessionId}`,
    },
    body: JSON.stringify(result)
  };
};

export {handler};