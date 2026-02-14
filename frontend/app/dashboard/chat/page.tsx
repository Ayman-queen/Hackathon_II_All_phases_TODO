"use client"

import { useState, useRef, useEffect, useCallback } from 'react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useSession, authClient } from '@/lib/auth-client';
import { useTheme } from '@/lib/hooks/useTheme';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface UserStats {
  pending: number;
  completed: number;
  total: number;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [stats, setStats] = useState<UserStats | null>(null);
  const [welcomeMessageShown, setWelcomeMessageShown] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const { data: session } = useSession();
  const { theme } = useTheme();

  // T009: Fetch user stats from backend API for correct welcome message (FR-003)
  useEffect(() => {
    const fetchStats = async () => {
      if (!session) return;

      try {
        // Get JWT token for API call
        const tokenResult = await authClient.token();
        if (!tokenResult?.data?.token) {
          console.error("Failed to retrieve auth token.");
          return;
        }
        const token = tokenResult.data.token;

        const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
        const res = await fetch(`${backendUrl}/api/todos/stats`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
          credentials: 'include',
        });

        if (res.ok) {
          const data = await res.json();
          setStats(data);
        }
      } catch (error) {
        console.error('Failed to fetch user stats:', error);
      }
    };

    fetchStats();
  }, [session]);

  // T009: Show welcome message with correct stats from API
  useEffect(() => {
    if (session && stats !== null && !welcomeMessageShown) {
      const greeting = stats.total === 0
        ? `Welcome! You don't have any tasks yet. Try saying "add buy groceries" to create your first task.`
        : `Welcome back! You have ${stats.pending} pending task${stats.pending !== 1 ? 's' : ''} and ${stats.completed} completed. How can I help?`;
      setMessages([{ role: 'assistant', content: greeting }]);
      setWelcomeMessageShown(true);
    } else if (session && stats === null && !welcomeMessageShown) {
      // Show loading state while fetching stats
      setMessages([{ role: 'assistant', content: 'Loading your tasks...' }]);
    }
  }, [session, stats, welcomeMessageShown]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = useCallback(async () => {
    if (!input.trim() || isLoading || !session) return;

    const userMsg: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      // JWT token is now retrieved server-side in the API route
      // Cookies are automatically forwarded, so no Authorization header needed
      const res = await fetch(`/api/chat/${session.user.id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Ensure cookies are sent
        body: JSON.stringify({
          message: input,
          conversation_id: conversationId,
          user_id: session.user.id,
        }),
      });

      if (!res.ok) throw new Error('Chat API error');

      const { response, conversation_id } = await res.json();
      setMessages(prev => [...prev, { role: 'assistant', content: response }]);
      // Update session conversationId if new
      if (conversation_id) {
        setConversationId(conversation_id);
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, something went wrong. Try again.' }]);
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading, session, conversationId]);

  return (
    <div className={`flex flex-col h-screen ${theme === 'dark' ? 'bg-gray-900' : 'bg-white'}`}>
      <div className="p-4 border-b flex-shrink-0">
        <h1 className="text-2xl font-bold text-foreground">AI Chat Assistant</h1>
      </div>
      <ScrollArea className="flex-1 p-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            <p>Chat starts when you send a message...</p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className={`mb-6 flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-md p-4 rounded-2xl shadow-lg ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}>
                <p>{msg.content}</p>
              </div>
            </div>
          ))
        )}
        <div ref={scrollRef} />
      </ScrollArea>
      <div className="p-4 border-t flex gap-2 bg-background">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
          placeholder="Type your message... (e.g., 'add buy milk')"
          className="flex-1"
          disabled={isLoading}
        />
        <Button onClick={sendMessage} disabled={!input.trim() || isLoading}>
          {isLoading ? '...' : 'Send'}
        </Button>
      </div>
    </div>
  );
}

// T304: Responsive Shadcn Chat UI (XIII UI consistency, light/dark)
