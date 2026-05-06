import type { Message } from './types';

const HISTORY_API_URL = 'http://localhost:5056/api';
const REQUEST_TIMEOUT_MS = 10000;

export interface ConversationSummary {
  id: number;
  session_id: string;
  title: string;
  created_at: string;
}

export interface ConversationDetail {
  conversation: ConversationSummary;
  messages: Message[];
}

export interface ConversationsResponse {
  conversations: ConversationSummary[];
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}

export class HistoryClient {
  async getConversations(sort: 'recent' | 'old' = 'recent', page: number = 1): Promise<ConversationsResponse> {
    const url = `${HISTORY_API_URL}/conversations?sort=${sort}&page=${page}`;
    const response = await fetch(url, {
      signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
    });

    if (!response.ok) {
      throw new Error(`History API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async getConversation(id: number): Promise<ConversationDetail> {
    const url = `${HISTORY_API_URL}/conversations/${id}`;
    const response = await fetch(url, {
      signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
    });

    if (!response.ok) {
      throw new Error(`History API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async saveConversation(sessionId: string, messages: Message[]): Promise<{ id: number; title: string; created_at: string }> {
    const url = `${HISTORY_API_URL}/conversations`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, messages }),
      signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
    });

    if (!response.ok) {
      throw new Error(`History API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async deleteConversation(id: number): Promise<void> {
    const url = `${HISTORY_API_URL}/conversations/${id}`;
    const response = await fetch(url, {
      method: 'DELETE',
      signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
    });

    if (!response.ok) {
      throw new Error(`History API error: ${response.status} ${response.statusText}`);
    }
  }
}

export const historyClient = new HistoryClient();
