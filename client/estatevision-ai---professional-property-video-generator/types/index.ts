export enum AppView {
  DASHBOARD = 'dashboard',
  GENERATE = 'generate',
  SETTINGS = 'settings',
  HELP = 'help',
}

export interface User {
  id?: number; // Optional id to maintain compatibility
  name: string;
  email: string;
  company: string;
  avatar: string;
  credits: number;
}

export interface PropertyVideo {
  id: string;
  title: string;
  description: string;
  thumbnailUrl: string;
  status: GenerationStatus;
  createdAt: Date;
  language: string;
  duration?: string;
  videoUrl?: string;
}

export enum GenerationStatus {
  IDLE = 'IDLE',
  SCRIPTING = 'SCRIPTING',
  VOICEOVER = 'VOICEOVER',
  VIDEO_GEN = 'VIDEO_GEN',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED',
}

export interface SystemLog {
  id: string;
  timestamp: Date;
  event: string;
  type: 'INFO' | 'SUCCESS' | 'ERROR';
}