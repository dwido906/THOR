// test_themingApi.ts
// Test stub for VRBLL theming TypeScript API
import { setTheme, getTheme, listThemes } from './themingApi';

describe('themingApi', () => {
  it('should set and get theme', async () => {
    await setTheme({ name: 'dark', colors: { background: '#000', text: '#fff' } });
    const theme = await getTheme();
    expect(theme).toHaveProperty('name');
  });
  it('should list themes', async () => {
    const themes = await listThemes();
    expect(Array.isArray(themes)).toBe(true);
  });
});
