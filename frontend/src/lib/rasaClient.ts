import type { RasaResponse, RasaMessagePayload } from './types';

const RASA_BASE_URL = 'http://localhost:5005';
const RASA_WEBHOOK_URL = `${RASA_BASE_URL}/webhooks/rest/webhook`;
const REQUEST_TIMEOUT_MS = 45000;

export class RasaClient {
  private senderId: string;

  constructor(senderId?: string) {
    this.senderId = senderId ?? crypto.randomUUID();
  }

  getSenderId(): string {
    return this.senderId;
  }

  async sendMessage(message: string): Promise<RasaResponse[]> {
    const payload: RasaMessagePayload = {
      sender: this.senderId,
      message: message.trim(),
    };

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    try {
      const response = await fetch(RASA_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`Rasa API error: ${response.status} ${response.statusText}`);
      }

      const responses: RasaResponse[] = await response.json();
      return responses;
    } catch (error) {
      clearTimeout(timeoutId);

      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('timeout');
      }
      throw error;
    }
  }

  async checkHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${RASA_BASE_URL}/health`, {
        method: 'GET',
        signal: AbortSignal.timeout(5000),
      });
      return response.ok;
    } catch {
      return false;
    }
  }
}

export const rasaClient = new RasaClient();