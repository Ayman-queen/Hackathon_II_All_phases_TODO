import { useAuth } from './useAuth';  // Better Auth session
import { useCallback } from 'react';

export function useChat() {
  const { session } = useAuth();

  const sendMessage = useCallback(async (message: string, conversationId?: string) => {
    if (!session) throw new Error('No session');

    const res = await fetch(`/api/chat/${session.user.id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${session.token}`,
      },
      body: JSON.stringify({ message, conversation_id: conversationId }),
    });

    if (!res.ok) throw new Error('Chat failed');
    return res.json();
  }, [session]);

  return { sendMessage };
}

// T304: Chat fetch wrapper with JWT (XII isolation)
