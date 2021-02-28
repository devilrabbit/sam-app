import { Repository } from './repository';
import { DynamoDBRepository } from './dynamodb';
import { InMemoryRepository } from './memory';

const test = (str: string): boolean => {
  if (!str) {
    return false;
  }
  if (str === '0' || str.toLowerCase() === 'false') {
    return false;
  }
  return true;
}

export const getRepository = (): Repository => {
  return test(process.env['ENABLE_FAKE']) ? new DynamoDBRepository() : new InMemoryRepository();
};