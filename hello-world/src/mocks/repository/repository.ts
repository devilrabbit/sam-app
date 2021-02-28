import { Item } from "../model/item";

export interface Repository {
  get(itemId: string): Promise<Item>;
  put(item: Item): Promise<void>;
  update(itemId: string, attribute: string): Promise<void>;
  delete(itemId: string): Promise<void>;
  query(groupId: string): Promise<Item[]>;
  deleteAll(groupId: string): Promise<void>;
}