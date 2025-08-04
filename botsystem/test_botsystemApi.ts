// test_botsystemApi.ts
// Test stub for VRBLL bot/plugin system TypeScript API
import { initBotSystem, loadPlugin, sendMessageToPlugin, unloadPlugin } from './botsystemApi';

describe('botsystemApi', () => {
  it('should initialize bot system', async () => {
    await initBotSystem();
  });
  it('should load, message, and unload plugin', async () => {
    await loadPlugin('testplugin.js');
    await sendMessageToPlugin('testplugin', 'hello');
    await unloadPlugin('testplugin');
  });
});
