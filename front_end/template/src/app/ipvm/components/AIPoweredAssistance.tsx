"use client";

import React, { useState } from 'react';
import { Brain, Camera } from 'lucide-react';

// AI-Powered Assistance Component
const AIPoweredAssistance: React.FC = () => {
  const [aiQuery, setAiQuery] = useState<string>('');
  const [showAiResponse, setShowAiResponse] = useState<boolean>(false);
  const [showImageAnalysis, setShowImageAnalysis] = useState<boolean>(false);
  
  const handleAiQuery = (e: React.FormEvent) => {
    e.preventDefault();
    if (aiQuery.trim()) {
      setShowAiResponse(true);
      
      if (aiQuery.toLowerCase().includes('camera placement') || 
          aiQuery.toLowerCase().includes('field of view') || 
          aiQuery.toLowerCase().includes('layout')) {
        setShowImageAnalysis(true);
      } else {
        setShowImageAnalysis(false);
      }
    }
  };
  
  return (
    <div className="p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800">AI-Powered Assistance</h2>
        <p className="text-gray-600">Advanced intelligence for security technology decision-making</p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-lg shadow p-6">
          <div className="flex items-center mb-6">
            <Brain size={24} className="text-blue-600 mr-3" />
            <h3 className="text-lg font-semibold text-gray-800">IPVM Sentinel AI</h3>
          </div>
          
          <form onSubmit={handleAiQuery} className="mb-6">
            <div className="flex mb-3">
              <input
                type="text"
                placeholder="Ask about security technologies, recommendations, or market trends..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-l focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={aiQuery}
                onChange={(e) => setAiQuery(e.target.value)}
              />
              <button 
                type="submit"
                className="px-6 py-3 bg-blue-600 text-white rounded-r hover:bg-blue-700"
              >
                Ask AI
              </button>
            </div>
            <div className="flex justify-end items-center bg-gray-50 rounded-lg p-3 border border-gray-200">
              <button type="button" className="flex items-center text-sm text-blue-600 hover:text-blue-800">
                <Camera size={15} className="mr-1" />
                Upload Image
              </button>
            </div>
          </form>
          
          {showAiResponse && (
            <div className="space-y-4">
              {showImageAnalysis ? (
                <div className="bg-white border border-gray-200 rounded-lg p-4">
                  <h4 className="text-lg font-semibold text-gray-800 mb-3">Visual Analysis</h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="border border-gray-200 rounded bg-gray-50 p-2">
                      <div className="aspect-video bg-gray-200 mb-2 flex items-center justify-center text-gray-400">
                        Floor Plan View
                      </div>
                      <p className="text-sm text-gray-600">Original floor plan</p>
                    </div>
                    <div className="border border-gray-200 rounded bg-gray-50 p-2">
                      <div className="aspect-video bg-gray-200 mb-2 flex items-center justify-center text-gray-400">
                        AI-Enhanced View
                      </div>
                      <p className="text-sm text-gray-600">Camera coverage analysis</p>
                    </div>
                  </div>
                  <div className="mt-4 p-3 bg-blue-50 border border-blue-100 rounded-lg">
                    <h5 className="font-medium text-blue-900 mb-2">Analysis Results</h5>
                    <ul className="text-sm text-blue-800 space-y-1 list-disc pl-4">
                      <li>Coverage gap detected in northwest corner</li>
                      <li>Recommend repositioning Camera #3 for better coverage</li>
                      <li>Potential blind spot in main corridor</li>
                      <li>Lighting levels may affect camera performance in east entrance</li>
                    </ul>
                  </div>
                </div>
              ) : (
                <div>
                  <div className="bg-blue-50 border border-blue-100 rounded-lg p-6 mb-4">
                    <div className="flex items-start mb-4">
                      <div className="w-8 h-8 flex-shrink-0 rounded-full bg-blue-600 flex items-center justify-center">
                        <Brain size={18} className="text-white" />
                      </div>
                      <div className="ml-3">
                        <h4 className="text-lg font-semibold text-gray-800">IPVM Research</h4>
                        <p className="text-gray-500 text-sm">Based on IPVM's independent testing and analysis</p>
                      </div>
                    </div>
                    
                    <div className="prose max-w-none">
                      <p>
                        Based on IPVM's extensive testing and research, cloud-based video surveillance solutions are increasingly 
                        viable for enterprise deployments. Recent testing shows significant improvements in reliability and 
                        feature parity with on-premise systems.
                      </p>
                      <p className="mt-4">
                        When evaluating cloud video surveillance for your environment, consider these key factors:
                      </p>
                      <ul className="list-disc pl-5 mt-2 space-y-1">
                        <li>Bandwidth requirements: Calculate your upload bandwidth needs based on camera count, resolution, and frame rate</li>
                        <li>Data retention: Cloud storage costs scale with retention length and resolution</li>
                        <li>Cybersecurity: Verify the provider's encryption standards and access controls</li>
                        <li>Integration capabilities: Ensure compatibility with your existing access control and alarm systems</li>
                      </ul>
                      <p className="mt-4">
                        Our testing indicates that Genetec Cloud, Eagle Eye Networks, and Axis Cloud Connect currently offer the 
                        most robust enterprise solutions, while Verkada and Ava provide more simplified deployments with trade-offs 
                        in customization.
                      </p>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-green-50 border border-green-100 rounded-lg p-4">
                      <h4 className="text-md font-semibold text-gray-800 mb-2 flex items-center">
                        <div className="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center mr-2">
                          <Camera size={14} className="text-green-700" />
                        </div>
                        Axis Website
                      </h4>
                      <p className="text-sm text-gray-700">
                        "Axis offers cloud-ready network cameras with ARTPEC chip for enhanced cybersecurity. Our solutions integrate 
                        with leading VMS platforms and provide flexible deployment options."
                      </p>
                    </div>
                    
                    <div className="bg-purple-50 border border-purple-100 rounded-lg p-4">
                      <h4 className="text-md font-semibold text-gray-800 mb-2 flex items-center">
                        <div className="w-6 h-6 rounded-full bg-purple-100 flex items-center justify-center mr-2">
                          <Brain size={14} className="text-purple-700" />
                        </div>
                        GPT-4o
                      </h4>
                      <p className="text-sm text-gray-700">
                        "Cloud video surveillance systems typically use a subscription model and offer benefits like remote access, 
                        automatic updates, and reduced on-site hardware. Consider bandwidth, privacy, and regulatory requirements when evaluating."
                      </p>
                    </div>
                  </div>
                </div>
              )}
              
              <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-200">
                <div className="flex space-x-2">
                  <button className="px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded hover:bg-blue-200">
                    Generate Quiz
                  </button>
                  <button className="px-3 py-1 text-sm bg-gray-100 text-gray-800 rounded hover:bg-gray-200">
                    View RFP Templates
                  </button>
                </div>
                <div className="text-sm text-gray-500">
                  Powered by IPVM Sentinel AI
                </div>
              </div>
            </div>
          )}
        </div>
        
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">AI Capabilities</h3>
            <div className="space-y-3">
              <AiCapabilityItem 
                title="Multi-Modal Intelligence" 
                description="Process text, images, and technical data"
              />
              <AiCapabilityItem 
                title="Predictive Analytics" 
                description="Technology trend forecasting and risk assessment"
              />
              <AiCapabilityItem 
                title="Decision Support" 
                description="Requirements analysis and solution comparison"
              />
              <AiCapabilityItem 
                title="Visual Analysis" 
                description="Camera placement and field of view optimization"
              />
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">IPVM AI Everywhere</h3>
            <div className="mb-4">
              <p className="text-sm text-gray-600">Access IPVM AI across your workflow:</p>
              <div className="grid grid-cols-2 gap-2 mt-3">
                <div className="border border-gray-200 rounded p-2 text-center">
                  <div className="w-full aspect-square bg-gray-100 flex items-center justify-center mb-1">
                    <div className="h-10 w-10 bg-gray-200 rounded"></div>
                  </div>
                  <p className="text-xs font-medium">Web Extension</p>
                </div>
                <div className="border border-gray-200 rounded p-2 text-center">
                  <div className="w-full aspect-square bg-gray-100 flex items-center justify-center mb-1">
                    <div className="h-10 w-10 bg-gray-200 rounded"></div>
                  </div>
                  <p className="text-xs font-medium">Slack</p>
                </div>
                <div className="border border-gray-200 rounded p-2 text-center">
                  <div className="w-full aspect-square bg-gray-100 flex items-center justify-center mb-1">
                    <div className="h-10 w-10 bg-gray-200 rounded"></div>
                  </div>
                  <p className="text-xs font-medium">Teams</p>
                </div>
                <div className="border border-gray-200 rounded p-2 text-center">
                  <div className="w-full aspect-square bg-gray-100 flex items-center justify-center mb-1">
                    <div className="h-10 w-10 bg-gray-200 rounded"></div>
                  </div>
                  <p className="text-xs font-medium">Mobile</p>
                </div>
              </div>
            </div>
            <button className="w-full px-4 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700">
              Configure Integrations
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// AI Capability Item Component
interface AiCapabilityItemProps {
  title: string;
  description: string;
}

const AiCapabilityItem: React.FC<AiCapabilityItemProps> = ({ title, description }) => (
  <div className="border-b border-gray-100 pb-3">
    <div className="flex items-start">
      <Brain size={16} className="text-blue-600 mr-2 mt-1" />
      <div>
        <h4 className="font-medium text-gray-800">{title}</h4>
        <p className="text-gray-600 text-sm">{description}</p>
      </div>
    </div>
  </div>
);

export default AIPoweredAssistance; 