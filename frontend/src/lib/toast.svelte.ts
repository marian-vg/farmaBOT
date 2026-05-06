import { type ClassValue, clsx } from 'clsx';

export type ToastType = 'success' | 'error' | 'warning' | 'info';

interface Toast {
  id: number;
  message: string;
  type: ToastType;
}

let toasts = $state<Toast[]>([]);
let nextId = 0;

export function show(message: string, type: ToastType = 'info'): void {
  const id = nextId++;
  toasts = [...toasts, { id, message, type }];

  setTimeout(() => {
    dismiss(id);
  }, 4000);
}

export function dismiss(id: number): void {
  toasts = toasts.filter((t) => t.id !== id);
}

export function getToasts(): Toast[] {
  return toasts;
}