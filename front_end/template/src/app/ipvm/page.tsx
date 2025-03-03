"use client";

import React from 'react';
import dynamic from 'next/dynamic';

// Use dynamic import with SSR disabled for the dashboard component
// This is because it uses browser APIs that are not available during server-side rendering
const IPVMPlatformDashboard = dynamic(
  () => import('./components/IPVMPlatformDashboard'),
  { ssr: false }
);

// Import ChatBot component with SSR disabled
const ChatBot = dynamic(
  () => import('./components/ChatBot'),
  { ssr: false }
);

export default function IPVMPage() {
  return (
    <div>
      <IPVMPlatformDashboard />
      <ChatBot />
    </div>
  );
} 