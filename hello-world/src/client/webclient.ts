import axios, { AxiosInstance } from "axios";

export class WebClient {
    private client: AxiosInstance;

    constructor(baseURL: string) {
        this.client = axios.create({ baseURL })
    }

    public async createGroupAsync(data: any): Promise<any> {
        const response = await this.client.post('/v1/groups', data);
        return response.data;
    }

    public async getGroupAsync(id: string): Promise<any> {
        const response = await this.client.get(`/v1/groups/${id}`);
        return response.data;
    }

    public async deleteGroupAsync(id: string): Promise<any> {
        const response = await this.client.delete(`/v1/groups/${id}`);
        return response.data;
    }

    public async createItemAsync(groupId: string, data: any): Promise<any> {
        const response = await this.client.post(`/v1/items?groupId=${groupId}`, data);
        return response.data;
    }

    public async getItemAsync(id: string): Promise<any> {
        const response = await this.client.get(`/v1/items/${id}`);
        return response.data;
    }

    public async updateItemAsync(id: string, attribute: string): Promise<any> {
        const response = await this.client.patch(`/v1/items/${id}`, { attribute: attribute });
        return response.data;
    }

    public async deleteItemAsync(id: string): Promise<any> {
        const response = await this.client.delete(`/v1/items/${id}`);
        return response.data;
    }

    public async listItemsAsync(id: string): Promise<any> {
        const response = await this.client.get(`/v1/items?groupId=${id}`);
        return response.data;
    }
}