"use client";

import React, { useState } from 'react';
import { Search, Shield, Camera, Database, Users, Brain, BarChart2, FileText, Settings, Bell, HelpCircle, User, ChevronDown, MessageCircle, Menu, X } from 'lucide-react';
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
  compact?: boolean;
}

// Main Dashboard Component
const IPVMSentinelDashboard: React.FC = () => {
  // State for active module and UI controls
  const [activeModule, setActiveModule] = useState<string>('Intelligence Hub');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(true);
  const [mobileMenuOpen, setMobileMenuOpen] = useState<boolean>(false);
  
  // Handle module change
  const handleModuleChange = (module: string) => {
    setActiveModule(module);
    if (window.innerWidth < 768) {
      setMobileMenuOpen(false);
    }
  };
  
  // Handle search submission
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
  };
  
  // Toggle sidebar
  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };
  
  // Toggle mobile menu
  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
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
    <div className="min-h-screen bg-gray-50 flex flex-col compact-layout">
      {/* Header */}
      <header className="bg-blue-900 text-white h-[var(--header-height)] border-b border-blue-800">
        <div className="px-3 h-full">
          <div className="flex justify-between items-center h-full">
            <div className="flex items-center space-x-2">
              {/* Mobile menu toggle */}
              <button 
                className="md:hidden text-white p-1"
                onClick={toggleMobileMenu}
              >
                <Menu className="h-5 w-5" />
              </button>
              
              {/* Logo */}
              <Shield className="h-6 w-6" />
              <span className="text-lg font-bold">IPVM Sentinel</span>
            </div>
            
            {/* Search - hidden on small screens */}
            <form onSubmit={handleSearch} className="hidden md:block flex-1 max-w-md mx-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-blue-300 h-4 w-4" />
                <input
                  type="text"
                  placeholder="Search..."
                  className="w-full py-1.5 pl-10 pr-3 rounded-md bg-blue-800 text-white placeholder-blue-300 focus:outline-none text-sm"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </form>
            
            {/* Header actions */}
            <div className="flex items-center space-x-3">
              <button className="text-white p-1">
                <Bell className="h-4 w-4" />
              </button>
              <button className="text-white p-1">
                <HelpCircle className="h-4 w-4" />
              </button>
              <div className="flex items-center space-x-1">
                <div className="h-7 w-7 rounded-full bg-blue-700 flex items-center justify-center">
                  <User className="h-4 w-4" />
                </div>
                <ChevronDown className="h-3 w-3 text-blue-300" />
              </div>
            </div>
          </div>
        </div>
      </header>
      
      {/* Mobile menu - only visible on small screens */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-b border-gray-200 compact-p">
          <div className="flex justify-between items-center mb-2">
            <h2 className="text-xs font-semibold text-gray-600 uppercase tracking-wider">MODULES</h2>
            <button onClick={toggleMobileMenu} className="text-gray-500">
              <X className="h-4 w-4" />
            </button>
          </div>
          <nav className="space-y-1">
            <NavItem 
              icon={<Database className="h-4 w-4" />} 
              title="Intelligence Hub" 
              active={activeModule === 'Intelligence Hub'} 
              onClick={() => handleModuleChange('Intelligence Hub')}
              compact
            />
            <NavItem 
              icon={<FileText className="h-4 w-4" />} 
              title="Project Lifecycle" 
              active={activeModule === 'Project Lifecycle'} 
              onClick={() => handleModuleChange('Project Lifecycle')}
              compact
            />
            <NavItem 
              icon={<BarChart2 className="h-4 w-4" />} 
              title="Performance" 
              active={activeModule === 'Performance'} 
              onClick={() => handleModuleChange('Performance')}
              compact
            />
            <NavItem 
              icon={<Users className="h-4 w-4" />} 
              title="Community" 
              active={activeModule === 'Community'} 
              onClick={() => handleModuleChange('Community')}
              compact
            />
            <NavItem 
              icon={<Brain className="h-4 w-4" />} 
              title="AI Assistant" 
              active={activeModule === 'AI Assistant'} 
              onClick={() => handleModuleChange('AI Assistant')}
              compact
            />
          </nav>
          
          {/* Mobile search */}
          <div className="mt-3">
            <form onSubmit={handleSearch}>
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search..."
                  className="w-full py-1.5 pl-8 pr-3 rounded-md bg-gray-50 text-gray-800 placeholder-gray-500 focus:outline-none text-sm border border-gray-200"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <Search className="absolute left-2.5 top-2 h-4 w-4 text-gray-500" />
              </div>
            </form>
          </div>
        </div>
      )}
      
      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden viewport-fit">
        {/* Sidebar - hidden on small screens */}
        <aside className={`hidden md:flex flex-col bg-white border-r border-gray-200 ${sidebarOpen ? 'w-[var(--sidebar-width)]' : 'w-14'} transition-all duration-300`}>
          <div className={`py-2 px-3 border-b border-gray-200 ${!sidebarOpen && 'flex justify-center'}`}>
            <h2 className={`text-xs font-semibold text-gray-600 uppercase tracking-wider ${!sidebarOpen && 'sr-only'}`}>
              MODULES
            </h2>
            {!sidebarOpen && <Database className="h-4 w-4 text-gray-600" />}
          </div>
          <nav className="flex-1 overflow-y-auto p-1.5 space-y-0.5">
            <NavItem 
              icon={<Database className="h-4 w-4" />} 
              title="Intelligence Hub" 
              active={activeModule === 'Intelligence Hub'} 
              onClick={() => handleModuleChange('Intelligence Hub')}
              compact={!sidebarOpen}
            />
            <NavItem 
              icon={<FileText className="h-4 w-4" />} 
              title="Project Lifecycle" 
              active={activeModule === 'Project Lifecycle'} 
              onClick={() => handleModuleChange('Project Lifecycle')}
              compact={!sidebarOpen}
            />
            <NavItem 
              icon={<BarChart2 className="h-4 w-4" />} 
              title="Performance" 
              active={activeModule === 'Performance'} 
              onClick={() => handleModuleChange('Performance')}
              compact={!sidebarOpen}
            />
            <NavItem 
              icon={<Users className="h-4 w-4" />} 
              title="Community" 
              active={activeModule === 'Community'} 
              onClick={() => handleModuleChange('Community')}
              compact={!sidebarOpen}
            />
            <NavItem 
              icon={<Brain className="h-4 w-4" />} 
              title="AI Assistant" 
              active={activeModule === 'AI Assistant'} 
              onClick={() => handleModuleChange('AI Assistant')}
              compact={!sidebarOpen}
            />
          </nav>
          {sidebarOpen && (
            <>
              <div className="p-2 border-t border-gray-200">
                <h2 className="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1.5">QUICK ACCESS</h2>
                <ul className="space-y-0.5">
                  <li>
                    <a href="#" className="flex items-center px-2 py-1 text-xs text-gray-700 rounded hover:bg-gray-100">
                      <Camera className="h-3.5 w-3.5 mr-1.5 text-gray-500" />
                      <span>Video Surveillance</span>
                    </a>
                  </li>
                  <li>
                    <a href="#" className="flex items-center px-2 py-1 text-xs text-gray-700 rounded hover:bg-gray-100">
                      <Shield className="h-3.5 w-3.5 mr-1.5 text-gray-500" />
                      <span>Access Control</span>
                    </a>
                  </li>
                  <li>
                    <a href="#" className="flex items-center px-2 py-1 text-xs text-gray-700 rounded hover:bg-gray-100">
                      <Camera className="h-3.5 w-3.5 mr-1.5 text-gray-500" />
                      <span>Weapons Detection</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="p-2 border-t border-gray-200">
                <button className="flex items-center justify-center w-full px-3 py-1.5 bg-blue-600 text-white rounded hover:bg-blue-700 text-xs">
                  <Settings className="h-3.5 w-3.5 mr-1.5" />
                  <span>Settings</span>
                </button>
              </div>
            </>
          )}
          {/* Sidebar toggle button */}
          <button 
            className="absolute top-[calc(var(--header-height)+0.75rem)] -right-3 h-6 w-6 rounded-full bg-white border border-gray-200 flex items-center justify-center shadow-sm"
            onClick={toggleSidebar}
          >
            <ChevronDown className={`h-3 w-3 text-gray-600 transform ${sidebarOpen ? 'rotate-90' : '-rotate-90'}`} />
          </button>
        </aside>
        
        {/* Main Content Area */}
        <main className="flex-1 overflow-hidden bg-gray-50">
          <div className="h-full module-container">
            {renderModuleContent()}
          </div>
        </main>
      </div>
      
      {/* Chat Button */}
      <div className="fixed bottom-3 right-3 z-10">
        <button className="bg-blue-600 text-white p-2 rounded-full shadow-md hover:bg-blue-700">
          <MessageCircle className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
};

// Navigation Item Component
const NavItem: React.FC<NavItemProps> = ({ icon, title, active, onClick, compact = false }) => {
  if (compact) {
    return (
      <button
        className={`flex items-center justify-center w-full p-1.5 rounded ${
          active 
            ? 'bg-blue-50 text-blue-700' 
            : 'text-gray-700 hover:bg-gray-100'
        }`}
        onClick={onClick}
        title={title}
      >
        <span className={active ? 'text-blue-600' : 'text-gray-500'}>
          {icon}
        </span>
      </button>
    );
  }
  
  return (
    <button
      className={`flex items-center w-full px-2.5 py-1.5 rounded text-sm ${
        active 
          ? 'bg-blue-50 text-blue-700 font-medium' 
          : 'text-gray-700 hover:bg-gray-100'
      }`}
      onClick={onClick}
    >
      <span className={`mr-2 ${active ? 'text-blue-600' : 'text-gray-500'}`}>
        {icon}
      </span>
      <span>{title}</span>
    </button>
  );
};

export default IPVMSentinelDashboard; 