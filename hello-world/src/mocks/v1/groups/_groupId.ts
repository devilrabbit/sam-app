import { MockMethods, MockResponse } from 'axios-mock-server';
import { getRepository } from '../../repository/factory';

const repository = getRepository();

const group: MockMethods = {
  delete: async ({ values }): Promise<MockResponse> => {
    await repository.deleteAll(values['groupId'] as string);
    return [200];
  }
};

export default group;