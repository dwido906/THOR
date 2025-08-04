// botsystemApi.ts
// TypeScript API for bot/plugin system in VRBLL

import * as store from './botsystemStore';

export function initBotSystem(): Promise<void> {
  return store.initBotSystem();
}

export function loadPlugin(path: string): Promise<void> {
  return store.loadPlugin(path);
}

export function sendMessageToPlugin(plugin: string, message: string): Promise<void> {
  return store.sendMessageToPlugin(plugin, message);
}

export function unloadPlugin(plugin: string): Promise<void> {
  return store.unloadPlugin(plugin);
}
