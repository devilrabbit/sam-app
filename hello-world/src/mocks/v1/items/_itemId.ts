import { MockMethods, MockResponse } from 'axios-mock-server';
import { getRepository } from '../../repository/factory';

const repository = getRepository();

const item: MockMethods = {
  get: async ({ values }): Promise<MockResponse> => {
    const item = await repository.get(values['itemId'] as string);
    return [200, item];
  },
  patch: async ({ values, data }): Promise<MockResponse> => {
    await repository.update(values['itemId'] as string, data.attribute);
    return [200];
  },
  delete: async ({ values }): Promise<MockResponse> => {
    await repository.delete(values['itemId'] as string);
    return [200];
  },
};

export default item;