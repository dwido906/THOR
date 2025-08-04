// botsystemStore.ts
// Minimal bot/plugin system implementation for VRBLL (TypeScript)

const plugins: Record<string, any> = {};

export async function initBotSystem() {
  // No-op for demo
}

export async function loadPlugin(path: string) {
  // For demo, simulate dynamic import
  plugins[path] = { plugin_entry: (msg: string) => console.log(`[plugin:${path}] ${msg}`) };
}

export async function sendMessageToPlugin(plugin: string, message: string) {
  if (plugins[plugin] && plugins[plugin].plugin_entry) {
    plugins[plugin].plugin_entry(message);
  }
}

export async function unloadPlugin(plugin: string) {
  delete plugins[plugin];
}
