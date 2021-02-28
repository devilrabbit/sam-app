import { Item } from '../model/item';
import { Repository } from './repository'

const cache = new Map<string, Item>();
cache.set('a', { itemId: 'a', groupId: 'b', attribute: 'c' })

export class InMemoryRepository implements Repository {
  constructor() {
  }

  public async get(itemId: string): Promise<Item> {
    return cache.get(itemId);
  }

  public async put(item: Item): Promise<void> {
    cache.set(item.itemId, item);
  }

  public async update(itemId: string, attribute: string): Promise<void> {
    const item = cache.get(itemId);
    if (item)
    {
      item.attribute = attribute;
      cache.set(itemId, item);
    }
  }

  public async delete(itemId: string): Promise<void> {
    cache.delete(itemId);
  }

  public async query(groupId: string): Promise<Item[]> {
    const items: any[] = [];
    cache.forEach((value, key) => {
      if (key === groupId) {
          items.push(value);
      }
    });
    return items;
  }

  public async deleteAll(groupId: string): Promise<void> {
    const keys = cache.keys();
    for (const key of keys) {
      const item = cache.get(key);
      if (item.groupId === groupId) {
        cache.delete(key);
      }
    }
  }
}