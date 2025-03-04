"use client";

import React, { useState } from 'react';
import { Brain, Camera, Globe, MessageSquare, MessageCircle, Smartphone, Search } from 'lucide-react';
import aiPoweredAssistanceData from '../data/aiPoweredAssistance.json';

// AI-Powered Assistance Component
const AIPoweredAssistance: React.FC = () => {
  const [aiQuery, setAiQuery] = useState<string>('');
  const [showAiResponse, setShowAiResponse] = useState<boolean>(false);
  const [showImageAnalysis, setShowImageAnalysis] = useState<boolean>(false);
  
  // Get data from JSON
  const { imageAnalysis, aiCapabilities, aiResponses, aiIntegrations, detailedResponses } = aiPoweredAssistanceData;
  
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
  
  // Function to get the appropriate icon component
  const getIconComponent = (iconName: string, size: number = 16, className: string = "") => {
    switch (iconName) {
      case 'Globe':
        return <Globe size={size} className={className} />;
      case 'MessageSquare':
        return <MessageSquare size={size} className={className} />;
      case 'MessageCircle':
        return <MessageCircle size={size} className={className} />;
      case 'Smartphone':
        return <Smartphone size={size} className={className} />;
      case 'Camera':
        return <Camera size={size} className={className} />;
      case 'Brain':
        return <Brain size={size} className={className} />;
      default:
        return <Brain size={size} className={className} />;
    }
  };
  
  return (
    <div className="viewport-fit">
      <div className="module-container">
        <div className="module-header">
          <h2 className="text-xl font-semibold text-gray-800">AI-Powered Assistance</h2>
          <p className="text-sm text-gray-600">Advanced intelligence for security technology decision-making</p>
        </div>
        
        <div className="module-content">
          <div className="module-grid compact-gap">
            <div className="module-grid-item">
              <div className="card h-full">
                <div className="panel-header border-b border-gray-200 flex items-center">
                  <Brain size={16} className="text-blue-600 mr-2" />
                  <h3 className="text-base font-semibold text-gray-800">IPVM Sentinel AI</h3>
                </div>
                
                <div className="panel-content compact-p">
                  <form onSubmit={handleAiQuery} className="mb-2">
                    <div className="flex mb-2 relative">
                      <div className="relative flex-1">
                        <Search size={14} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                        <input
                          type="text"
                          placeholder="Ask about security technologies, recommendations, or market trends..."
                          className="flex-1 w-full pl-12 pr-2 py-1.5 text-sm border border-gray-300 rounded-l focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-transparent"
                          value={aiQuery}
                          onChange={(e) => setAiQuery(e.target.value)}
                        />
                      </div>
                      <button 
                        type="submit"
                        className="px-3 py-1.5 bg-blue-600 text-white text-sm rounded-r hover:bg-blue-700"
                      >
                        Ask AI
                      </button>
                    </div>
                    <div className="flex justify-end items-center bg-gray-50 rounded-lg p-1.5 border border-gray-200">
                      <button type="button" className="flex items-center text-sm text-blue-600 hover:text-blue-800">
                        <Camera size={14} className="mr-1" />
                        Upload Image
                      </button>
                    </div>
                  </form>
                  
                  {showAiResponse && (
                    <div className="module-content-scrollable space-y-2">
                      {showImageAnalysis ? (
                        <div className="bg-white border border-gray-200 rounded-lg p-2">
                          <h4 className="text-xs font-semibold text-gray-800 mb-1.5">Visual Analysis</h4>
                          <div className="grid grid-cols-2 gap-2">
                            <div className="border border-gray-200 rounded bg-gray-50 p-1.5">
                              <div className="aspect-video bg-gray-200 mb-1 flex items-center justify-center text-gray-400 text-xs">
                                Floor Plan View
                              </div>
                              <p className="text-xs text-gray-600">Original floor plan</p>
                            </div>
                            <div className="border border-gray-200 rounded bg-gray-50 p-1.5">
                              <div className="aspect-video bg-gray-200 mb-1 flex items-center justify-center text-gray-400 text-xs">
                                AI-Enhanced View
                              </div>
                              <p className="text-xs text-gray-600">Camera coverage analysis</p>
                            </div>
                          </div>
                          <div className="mt-2 p-1.5 bg-blue-50 border border-blue-100 rounded-lg">
                            <h5 className="font-medium text-blue-900 text-xs mb-0.5">Analysis Results</h5>
                            <ul className="text-xs text-blue-800 space-y-0.5 list-disc pl-4">
                              {imageAnalysis.results.map((result, index) => (
                                <li key={index}>{result}</li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      ) : (
                        <div>
                          <div className="bg-blue-50 border border-blue-100 rounded-lg p-2 mb-2">
                            <div className="flex items-start mb-1.5">
                              <div className="w-5 h-5 flex-shrink-0 rounded-full bg-blue-600 flex items-center justify-center">
                                <Brain size={12} className="text-white" />
                              </div>
                              <div className="ml-1.5">
                                <h4 className="text-xs font-semibold text-gray-800">{detailedResponses.cloudSurveillance.title}</h4>
                                <p className="text-gray-500 text-xs">{detailedResponses.cloudSurveillance.subtitle}</p>
                              </div>
                            </div>
                            
                            <div className="prose max-w-none text-xs">
                              <p>
                                {detailedResponses.cloudSurveillance.content}
                              </p>
                              <p className="mt-1">
                                Key factors to consider:
                              </p>
                              <ul className="list-disc pl-4 mt-0.5 space-y-0.5">
                                {detailedResponses.cloudSurveillance.keyFactors.map((factor, index) => (
                                  <li key={index}>{factor}</li>
                                ))}
                              </ul>
                              <p className="mt-1">
                                {detailedResponses.cloudSurveillance.topSolutions}
                              </p>
                            </div>
                          </div>
                          
                          <div className="grid grid-cols-2 gap-2">
                            {detailedResponses.externalSources.map((source, index) => (
                              <div key={index} className={`bg-${source.icon === 'Camera' ? 'green' : 'purple'}-50 border border-${source.icon === 'Camera' ? 'green' : 'purple'}-100 rounded-lg p-2`}>
                                <h4 className="text-xs font-semibold text-gray-800 mb-1 flex items-center">
                                  <div className={`w-4 h-4 rounded-full bg-${source.icon === 'Camera' ? 'green' : 'purple'}-100 flex items-center justify-center mr-1`}>
                                    {getIconComponent(source.icon, 10, `text-${source.icon === 'Camera' ? 'green' : 'purple'}-700`)}
                                  </div>
                                  {source.source}
                                </h4>
                                <p className="text-xs text-gray-700">
                                  "{source.quote}"
                                </p>
                              </div>
                            ))}
                          </div>
                          
                          <div className="flex justify-between items-center mt-2 pt-2 border-t border-gray-200">
                            <div className="flex space-x-1.5">
                              {detailedResponses.actions.map((action, index) => (
                                <button 
                                  key={index} 
                                  className={`px-1.5 py-0.5 text-xs ${
                                    action.style === 'primary' 
                                      ? 'bg-blue-100 text-blue-800' 
                                      : 'bg-gray-100 text-gray-800'
                                  } rounded hover:${
                                    action.style === 'primary' 
                                      ? 'bg-blue-200' 
                                      : 'bg-gray-200'
                                  }`}
                                >
                                  {action.label}
                                </button>
                              ))}
                            </div>
                            <div className="text-xs text-gray-500">
                              Powered by IPVM AI
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
            
            <div className="module-grid-item space-y-3">
              <div className="card">
                <div className="panel-header border-b border-gray-200">
                  <h3 className="text-base font-semibold text-gray-800">AI Capabilities</h3>
                </div>
                <div className="panel-content compact-p">
                  <div className="space-y-2 module-content-scrollable">
                    {aiCapabilities.map((capability) => (
                      <AiCapabilityItem 
                        key={capability.id}
                        title={capability.title}
                        description={capability.description}
                      />
                    ))}
                  </div>
                </div>
              </div>
              
              <div className="card h-full">
                <div className="panel-header border-b border-gray-200">
                  <h3 className="text-base font-semibold text-gray-800">IPVM AI Integration</h3>
                </div>
                <div className="panel-content compact-p">
                  <div className="grid grid-cols-2 gap-2">
                    {aiIntegrations.map((integration) => (
                      <div key={integration.id} className="flex items-center p-2 border border-gray-200 rounded-lg">
                        {getIconComponent(integration.icon, 16, "text-blue-600 mr-2")}
                        <span className="text-sm">{integration.name}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
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
  <div className="bg-white border border-gray-200 rounded-lg p-2">
    <h4 className="text-sm font-medium text-gray-800 mb-1">{title}</h4>
    <p className="text-xs text-gray-600">{description}</p>
  </div>
);

export default AIPoweredAssistance; 