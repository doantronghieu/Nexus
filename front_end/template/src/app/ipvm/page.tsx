"use client";

import React from 'react';
import dynamic from 'next/dynamic';

// Use dynamic import with SSR disabled for the dashboard component
// This is because it uses browser APIs that are not available during server-side rendering
const IPVMSentinelDashboard = dynamic(
  () => import('./components/IPVMSentinelDashboard'),
  { ssr: false }
);

export default function IPVMPage() {
  return (
    <div>
      <IPVMSentinelDashboard />
    </div>
  );
} 