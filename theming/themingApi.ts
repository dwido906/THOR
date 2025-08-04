// themingApi.ts
// TypeScript API for theming and UX customization in VRBLL

export type Theme = {
  name: string;
  colors: Record<string, string>;
  fontSize?: string;
  contrast?: string;
};

import * as store from './themingStore';

export function setTheme(theme: Theme): Promise<void> {
  return store.setTheme(theme);
}

export function getTheme(): Promise<Theme> {
  return store.getTheme();
}

export function listThemes(): Promise<Theme[]> {
  return store.listThemes();
}
