import { MockMethods, MockResponse } from 'axios-mock-server';
import { UUID } from '../../util/uuid';
import { getRepository } from '../repository/factory';

const repository = getRepository();

const item: MockMethods = {
  get: async ({ params }): Promise<MockResponse> => {
    const items = await repository.query(params['groupId'] as string);
    return [200, items];
  },
  post: async ({ data, params }): Promise<MockResponse> => {
    const itemId = UUID.generate();
    const groupId = params['groupId'] as string;
    const item = Object.assign({}, data, { itemId, groupId });
    await repository.put(item);
    return [200, item];
  },
};

export default item;