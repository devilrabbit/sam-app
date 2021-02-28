import { MockMethods, MockResponse } from 'axios-mock-server';
import { UUID } from '../../util/uuid';

const group: MockMethods = {
  post: async (): Promise<MockResponse> => {
    const groupId = UUID.generate();
    return [200, { groupId }];
  },
};

export default group;