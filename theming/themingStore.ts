// themingStore.ts
// Minimal theming and UX customization implementation for VRBLL (TypeScript)
import * as fs from 'fs';

const DB_FILE = 'vrbll_themes.json';

let currentTheme = { name: 'default', colors: { background: '#fff', text: '#000' } };
let themes = [
  { name: 'default', colors: { background: '#fff', text: '#000' } },
  { name: 'dark', colors: { background: '#000', text: '#fff' } },
];

function loadThemes() {
  if (fs.existsSync(DB_FILE)) {
    const data = JSON.parse(fs.readFileSync(DB_FILE, 'utf-8'));
    themes = data.themes || themes;
    currentTheme = data.currentTheme || currentTheme;
  }
}

function saveThemes() {
  fs.writeFileSync(DB_FILE, JSON.stringify({ themes, currentTheme }, null, 2));
}

export async function setTheme(theme: any) {
  currentTheme = theme;
  if (!themes.find((t) => t.name === theme.name)) {
    themes.push(theme);
  }
  saveThemes();
}

export async function getTheme() {
  loadThemes();
  return currentTheme;
}

export async function listThemes() {
  loadThemes();
  return themes;
}
