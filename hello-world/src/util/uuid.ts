const { v4: uuidv4 } = require('uuid');

export class UUID {
    public static generate(): string {
        return uuidv4();
    }

    public static generateShort(): string {
        const uuid = uuidv4();
        return this.shorten(uuid);
    }

    public static shorten(uuid: string): string {
        const hex = uuid.split('-').join("");
        const base64 = Buffer.from(hex, 'hex').toString('base64');
        return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
    }

    public static lengthen(short_uuid: string): string {
        const base64 = short_uuid.replace(/-/g, '+').replace(/_/g, '/') + '==';
        const binary = Buffer.from(base64, 'base64');
        const hex = binary.toString('hex');
        const phases = [
            hex.substring(0, 8),
            hex.substring(8, 12),
            hex.substring(12, 16),
            hex.substring(16, 20),
            hex.substring(20, 32)
        ]
        return phases.join('-');
    }
}