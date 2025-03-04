"use client";

import React, { useState } from 'react';
import { Search, Shield, Camera, Database, Users, Brain, BarChart2, FileText, Settings, Bell, HelpCircle, User, ChevronDown, MessageCircle } from 'lucide-react';
import dynamic from 'next/dynamic';

// Dynamically import the module components to avoid circular dependencies
const IntelligenceHub = dynamic(() => import('./IntelligenceHub'), { ssr: false });
const ProjectLifecycle = dynamic(() => import('./ProjectLifecycle'), { ssr: false });
const PerformanceOptimization = dynamic(() => import('./PerformanceOptimization'), { ssr: false });
const CommunityCollaboration = dynamic(() => import('./CommunityCollaboration'), { ssr: false });
const AIPoweredAssistance = dynamic(() => import('./AIPoweredAssistance'), { ssr: false });

// Define types for the NavItem component
interface NavItemProps {
  icon: React.ReactNode;
  title: string;
  active: boolean;
  onClick?: () => void;
}

// Main Dashboard Component
const IPVMSentinelDashboard: React.FC = () => {
  // State for active module
  const [activeModule, setActiveModule] = useState<string>('Intelligence Hub');
  const [searchQuery, setSearchQuery] = useState<string>('');
  
  // Handle module change
  const handleModuleChange = (module: string) => {
    setActiveModule(module);
  };
  
  // Handle search submission
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
  };
  
  // Render the content for the active module
  const renderModuleContent = () => {
    switch (activeModule) {
      case 'Intelligence Hub':
        return <IntelligenceHub />;
      case 'Project Lifecycle':
        return <ProjectLifecycle />;
      case 'Performance':
        return <PerformanceOptimization />;
      case 'Community':
        return <CommunityCollaboration />;
      case 'AI Assistant':
        return <AIPoweredAssistance />;
      default:
        return <IntelligenceHub />;
    }
  };
  
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-blue-900 text-white">
        <div className="container mx-auto px-4 py-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <Shield className="h-8 w-8" />
              <span className="text-xl font-bold">IPVM Sentinel</span>
            </div>
            
            <form onSubmit={handleSearch} className="flex-1 max-w-2xl mx-4">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search for security technologies, manufacturers, or trends..."
                  className="w-full py-2 pl-10 pr-4 rounded-md bg-blue-800 text-white placeholder-blue-300 focus:outline-none"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <Search className="absolute left-3 top-2.5 h-5 w-5 text-blue-300" />
              </div>
            </form>
            
            <div className="flex items-center space-x-4">
              <button className="text-white">
                <Bell className="h-5 w-5" />
              </button>
              <button className="text-white">
                <HelpCircle className="h-5 w-5" />
              </button>
              <div className="flex items-center space-x-2">
                <div className="h-8 w-8 rounded-full bg-blue-700 flex items-center justify-center">
                  <User className="h-5 w-5" />
                </div>
                <ChevronDown className="h-4 w-4 text-blue-300" />
              </div>
            </div>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="w-56 bg-white border-r border-gray-200 flex flex-col">
          <div className="p-4 border-b border-gray-200">
            <h2 className="text-xs font-semibold text-gray-600 uppercase tracking-wider">PLATFORM MODULES</h2>
          </div>
          <nav className="flex-1 overflow-y-auto p-2 space-y-1">
            <NavItem 
              icon={<Database className="h-5 w-5" />} 
              title="Intelligence Hub" 
              active={activeModule === 'Intelligence Hub'} 
              onClick={() => handleModuleChange('Intelligence Hub')}
            />
            <NavItem 
              icon={<FileText className="h-5 w-5" />} 
              title="Project Lifecycle" 
              active={activeModule === 'Project Lifecycle'} 
              onClick={() => handleModuleChange('Project Lifecycle')}
            />
            <NavItem 
              icon={<BarChart2 className="h-5 w-5" />} 
              title="Performance" 
              active={activeModule === 'Performance'} 
              onClick={() => handleModuleChange('Performance')}
            />
            <NavItem 
              icon={<Users className="h-5 w-5" />} 
              title="Community" 
              active={activeModule === 'Community'} 
              onClick={() => handleModuleChange('Community')}
            />
            <NavItem 
              icon={<Brain className="h-5 w-5" />} 
              title="AI Assistant" 
              active={activeModule === 'AI Assistant'} 
              onClick={() => handleModuleChange('AI Assistant')}
            />
          </nav>
          <div className="p-4 border-t border-gray-200">
            <h2 className="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-2">QUICK ACCESS</h2>
            <ul className="space-y-1">
              <li>
                <a href="#" className="flex items-center px-2 py-1.5 text-sm text-gray-700 rounded-md hover:bg-gray-100">
                  <Camera className="h-4 w-4 mr-2 text-gray-500" />
                  <span>Video Surveillance</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center px-2 py-1.5 text-sm text-gray-700 rounded-md hover:bg-gray-100">
                  <Shield className="h-4 w-4 mr-2 text-gray-500" />
                  <span>Access Control</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center px-2 py-1.5 text-sm text-gray-700 rounded-md hover:bg-gray-100">
                  <Camera className="h-4 w-4 mr-2 text-gray-500" />
                  <span>Weapons Detection</span>
                </a>
              </li>
            </ul>
          </div>
          <div className="p-4 border-t border-gray-200">
            <button className="flex items-center justify-center w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
              <Settings className="h-4 w-4 mr-2" />
              <span>Settings</span>
            </button>
          </div>
        </aside>
        
        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto bg-gray-50">
          {renderModuleContent()}
        </main>
      </div>
      
      {/* Chat Button */}
      <div className="fixed bottom-4 right-4 z-10">
        <button className="bg-blue-600 text-white p-3 rounded-full shadow-lg hover:bg-blue-700">
          <MessageCircle className="h-6 w-6" />
        </button>
      </div>
    </div>
  );
};

// Navigation Item Component
const NavItem: React.FC<NavItemProps> = ({ icon, title, active, onClick }) => {
  return (
    <button
      className={`flex items-center w-full px-3 py-2 rounded-md ${
        active 
          ? 'bg-blue-50 text-blue-700 font-medium' 
          : 'text-gray-700 hover:bg-gray-100'
      }`}
      onClick={onClick}
    >
      <span className={`mr-3 ${active ? 'text-blue-600' : 'text-gray-500'}`}>
        {icon}
      </span>
      <span>{title}</span>
    </button>
  );
};

export default IPVMSentinelDashboard; 