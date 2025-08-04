// aimoderationStore.ts
// Minimal AI moderation implementation for VRBLL (TypeScript)

const bannedWords = ["spam", "abuse", "toxic"];

export async function initAIModeration() {
  // No-op for demo
}

export async function moderateMessage(user: string, message: string) {
  for (const word of bannedWords) {
    if (message.includes(word)) {
      return { flagged: true, reason: `Flagged for '${word}'` };
    }
  }
  return { flagged: false };
}

export async function moderateVoice(data: ArrayBuffer) {
  // For demo, always OK
  return { flagged: false };
}
