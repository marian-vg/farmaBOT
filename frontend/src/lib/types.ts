export interface Message {
  role: 'user' | 'assistant' | 'error';
  content: string;
}

export interface RasaResponse {
  recipient_id: string;
  text?: string;
  image?: string;
  buttons?: RasaButton[];
  attachment?: string;
  custom?: Record<string, unknown>;
}

export interface RasaButton {
  title: string;
  payload: string;
}

export interface RasaMessagePayload {
  sender: string;
  message: string;
}

export interface OptionCard {
  id: string;
  title: string;
  description: string;
  icon: string;
  sampleQuestion: string;
}