
'use client';

import dynamic from 'next/dynamic';
const ChatPage = dynamic(() => import('./chat/page'), { ssr: false });

export default function Dashboard() {
  return (
    <div className="h-screen w-full">
      <ChatPage /> 
       {/* // T304/T305: Phase III direct Chat UI (no /todos redirect) */}
    </div>
  );
}
