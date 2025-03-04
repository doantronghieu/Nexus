"use client";

import React from 'react';
import { Camera, Shield, Brain, ArrowRight, PieChart } from 'lucide-react';

// Intelligence Hub Component
interface IntelligenceHubProps {
  searchQuery?: string;
  showAIResults?: boolean;
}

const IntelligenceHub: React.FC<IntelligenceHubProps> = ({ searchQuery = '', showAIResults = false }) => {
  return (
    <div className="module-container">
      <div className="module-header flex justify-between items-center">
        <h2 className="text-xl font-bold text-gray-800">Intelligence Hub</h2>
        <div className="flex space-x-2">
          <button className="px-3 py-1.5 bg-blue-600 text-white text-sm rounded hover:bg-blue-700">Latest Research</button>
          <button className="px-3 py-1.5 bg-white border border-gray-300 text-sm rounded text-gray-700 hover:bg-gray-50">Export</button>
        </div>
      </div>

      <div className="module-content">
        {showAIResults ? (
          <AISearchResults query={searchQuery} />
        ) : (
          <div className="module-grid h-full p-3">
            <div className="module-grid-item space-y-3">
              <div className="card h-auto">
                <div className="panel-header border-b border-gray-200">
                  <h3 className="text-base font-semibold text-gray-800">Unified Knowledge Repository</h3>
                </div>
                <div className="border-b border-gray-200">
                  <div className="bg-gray-50 px-3 py-2 border-b border-gray-200 flex justify-between items-center flex-wrap gap-2">
                    <div>
                      <h4 className="font-medium text-gray-800 text-sm">IPVM Research Database</h4>
                      <p className="text-xs text-gray-600">Comprehensive collection of testing and analysis</p>
                    </div>
                    <div className="flex space-x-2">
                      <select className="text-xs border border-gray-300 rounded p-1">
                        <option>All Categories</option>
                        <option>Video Surveillance</option>
                        <option>Access Control</option>
                        <option>Analytics</option>
                        <option>Cybersecurity</option>
                      </select>
                      <select className="text-xs border border-gray-300 rounded p-1">
                        <option>All Time</option>
                        <option>Last 30 Days</option>
                        <option>Last 90 Days</option>
                        <option>Last Year</option>
                      </select>
                    </div>
                  </div>
                  <div className="panel-content max-h-[calc(100vh-20rem)] overflow-y-auto">
                    <div className="space-y-3">
                      <div className="border-b border-gray-100 pb-3">
                        <div className="flex items-center">
                          <div className="w-8 h-8 rounded-md bg-blue-100 flex items-center justify-center mr-3">
                            <Camera size={16} className="text-blue-600" />
                          </div>
                          <div>
                            <h5 className="font-medium text-gray-800 text-sm">Cloud Going Mainstream In Video Surveillance</h5>
                            <div className="flex items-center text-xs text-gray-500 mt-1">
                              <span className="bg-blue-100 text-blue-800 px-2 py-0.5 rounded">Research Report</span>
                              <span className="mx-2">•</span>
                              <span>Apr 23, 2024</span>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div className="border-b border-gray-100 pb-3">
                        <div className="flex items-center">
                          <div className="w-8 h-8 rounded-md bg-purple-100 flex items-center justify-center mr-3">
                            <Shield size={16} className="text-purple-600" />
                          </div>
                          <div>
                            <h5 className="font-medium text-gray-800 text-sm">Mobile Credential Solutions Comparative Test</h5>
                            <div className="flex items-center text-xs text-gray-500 mt-1">
                              <span className="bg-purple-100 text-purple-800 px-2 py-0.5 rounded">Test Results</span>
                              <span className="mx-2">•</span>
                              <span>Feb 18, 2025</span>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div className="border-b border-gray-100 pb-3">
                        <div className="flex items-center">
                          <div className="w-8 h-8 rounded-md bg-green-100 flex items-center justify-center mr-3">
                            <Brain size={16} className="text-green-600" />
                          </div>
                          <div>
                            <h5 className="font-medium text-gray-800 text-sm">Person Detection Accuracy Benchmark</h5>
                            <div className="flex items-center text-xs text-gray-500 mt-1">
                              <span className="bg-green-100 text-green-800 px-2 py-0.5 rounded">Analytics Test</span>
                              <span className="mx-2">•</span>
                              <span>Feb 10, 2025</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="bg-gray-50 px-3 py-2 border-t border-gray-200 flex justify-between items-center">
                  <span className="text-xs text-gray-500">1,500+ Research Reports Available</span>
                  <button className="text-xs text-blue-600 font-medium">Browse All</button>
                </div>
              </div>
              
              <div className="card h-auto">
                <div className="panel-header border-b border-gray-200">
                  <div className="flex justify-between items-center">
                    <h3 className="text-base font-semibold text-gray-800">Trending Technologies</h3>
                    <button className="text-blue-600 hover:text-blue-800 text-xs font-medium flex items-center">
                      View All Trends <ArrowRight size={14} className="ml-1" />
                    </button>
                  </div>
                </div>
                <div className="panel-content">
                  <div className="space-y-3">
                    <TrendItem 
                      title="Cloud Going Mainstream In Video Surveillance" 
                      trend="Rising" 
                      impact="High"
                      description="Major vendors launching cloud platforms, signaling industry shift"
                    />
                    <TrendItem 
                      title="Weapons Detection Systems Market Analysis" 
                      trend="Stable" 
                      impact="Medium"
                      description="Evaluation of performance claims vs. testing results"
                    />
                    <TrendItem 
                      title="AI-Based Video Analytics Advancements" 
                      trend="Rising" 
                      impact="High"
                      description="Performance improvements in object detection and classification"
                    />
                  </div>
                </div>
              </div>
            </div>
            
            <div className="module-grid-item space-y-3">
              <div className="card h-auto">
                <div className="panel-header border-b border-gray-200">
                  <h3 className="text-base font-semibold text-gray-800">Market Trend Analyzer</h3>
                </div>
                <div className="panel-content">
                  <div className="h-48 flex items-center justify-center bg-gray-50 rounded border border-gray-200">
                    <PieChart size={140} className="text-blue-400" />
                  </div>
                  <div className="mt-3 space-y-1.5">
                    <div className="flex items-center">
                      <div className="w-3 h-3 rounded-full bg-blue-500 mr-2"></div>
                      <span className="text-xs">Cloud-based Solutions (38%)</span>
                    </div>
                    <div className="flex items-center">
                      <div className="w-3 h-3 rounded-full bg-blue-300 mr-2"></div>
                      <span className="text-xs">On-premise Systems (42%)</span>
                    </div>
                    <div className="flex items-center">
                      <div className="w-3 h-3 rounded-full bg-blue-200 mr-2"></div>
                      <span className="text-xs">Hybrid Deployments (20%)</span>
                    </div>
                  </div>
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-medium text-gray-600">M&A Activity:</span>
                      <span className="text-xs font-bold text-green-600">+12% YoY</span>
                    </div>
                    <div className="flex justify-between items-center mt-1.5">
                      <span className="text-xs font-medium text-gray-600">Funding Rounds:</span>
                      <span className="text-xs font-bold text-green-600">+8% QoQ</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="card h-auto">
                <div className="panel-header border-b border-gray-200">
                  <h3 className="text-base font-semibold text-gray-800">Competitive Analysis Engine</h3>
                </div>
                <div className="panel-content">
                  <div className="border border-gray-200 rounded-lg p-3 bg-gray-50">
                    <div className="flex justify-between items-center mb-2">
                      <h4 className="text-xs font-medium">Compare Products</h4>
                    </div>
                    <div className="space-y-2">
                      <div className="flex gap-2">
                        <select className="block w-full text-xs border border-gray-300 rounded p-1.5">
                          <option>Select Category</option>
                          <option>IP Cameras</option>
                          <option>VMS Systems</option>
                          <option>Access Control</option>
                          <option>Video Analytics</option>
                        </select>
                      </div>
                      <div className="flex gap-2">
                        <input type="text" placeholder="Add product to compare" className="block w-full text-xs border border-gray-300 rounded p-1.5" />
                        <button className="bg-blue-600 text-white p-1.5 rounded">+</button>
                      </div>
                      <div className="flex flex-wrap gap-1.5 mt-2">
                        <span className="bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full flex items-center">
                          Axis P3719-PLE <button className="ml-1 text-blue-600">×</button>
                        </span>
                        <span className="bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full flex items-center">
                          Hanwha XNP-9250R <button className="ml-1 text-blue-600">×</button>
                        </span>
                      </div>
                    </div>
                    <button className="w-full mt-3 px-3 py-1.5 bg-blue-600 text-white text-xs rounded hover:bg-blue-700">
                      Generate Comparison
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// AI Search Results Component
interface AISearchResultsProps {
  query: string;
}

const AISearchResults: React.FC<AISearchResultsProps> = ({ query }) => {
  return (
    <div className="module-content-scrollable p-3">
      <div className="card">
        <div className="panel-header border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800">IPVM Sentinel AI Results</h3>
          <p className="text-sm text-gray-600">Showing intelligence for: "{query}"</p>
        </div>
        
        <div className="panel-content">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <div className="lg:col-span-2 space-y-4">
              <div className="bg-blue-50 border border-blue-100 rounded-lg p-4">
                <div className="flex items-start mb-3">
                  <Brain size={20} className="text-blue-600 mr-2 mt-0.5" />
                  <div>
                    <h4 className="text-base font-semibold text-gray-800">AI Analysis</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      Based on IPVM research and testing data, here's what you should know about {query}:
                    </p>
                  </div>
                </div>
                
                <div className="prose max-w-none text-sm">
                  <p>
                    Recent IPVM testing shows cloud-based video surveillance solutions are seeing increasing adoption across 
                    enterprise markets. Major manufacturers including Genetec, Axis, and Motorola have launched new cloud platforms 
                    in the past 6 months, signaling a significant market shift.
                  </p>
                  <p className="mt-3">
                    Key considerations for implementation include:
                  </p>
                  <ul className="list-disc pl-5 mt-1.5 space-y-1">
                    <li>Bandwidth requirements for different resolution streams</li>
                    <li>Data sovereignty and compliance with regional regulations</li>
                    <li>Total cost of ownership compared to on-premise systems</li>
                    <li>Cybersecurity controls and encryption standards</li>
                  </ul>
                </div>
              </div>
              
              <div className="bg-white border border-gray-200 rounded-lg p-4">
                <h4 className="text-base font-semibold text-gray-800 mb-3">Knowledge Graph</h4>
                <div className="h-48 flex items-center justify-center bg-gray-50 rounded border border-gray-200 mb-3">
                  <span className="text-gray-500 text-sm">Interactive Knowledge Graph Visualization</span>
                </div>
                <p className="text-sm text-gray-600">
                  This knowledge graph shows the relationships between key technologies, manufacturers, and market trends 
                  related to cloud video surveillance. Click on any node to explore deeper connections.
                </p>
              </div>
            </div>
            
            <div className="space-y-4">
              <div className="bg-white border border-gray-200 rounded-lg p-4">
                <h4 className="text-base font-semibold text-gray-800 mb-3">Competitive Analysis</h4>
                <div className="space-y-3">
                  <CompetitorItem 
                    name="Genetec Cloud" 
                    rating="High" 
                    strength="Enterprise-grade security features" 
                    weakness="Higher cost structure"
                  />
                  <CompetitorItem 
                    name="Eagle Eye Networks" 
                    rating="High" 
                    strength="Purpose-built cloud architecture" 
                    weakness="Limited integration options"
                  />
                  <CompetitorItem 
                    name="Verkada" 
                    rating="Medium" 
                    strength="Simple deployment and management" 
                    weakness="Closed ecosystem"
                  />
                </div>
              </div>
              
              <div className="bg-white border border-gray-200 rounded-lg p-4">
                <h4 className="text-base font-semibold text-gray-800 mb-3">Implementation Risks</h4>
                <div className="space-y-2">
                  <RiskItem 
                    category="Security" 
                    level="Medium" 
                    description="Data transmission vulnerabilities if not properly encrypted"
                  />
                  <RiskItem 
                    category="Reliability" 
                    level="Low" 
                    description="Service disruption during internet outages"
                  />
                  <RiskItem 
                    category="Compliance" 
                    level="High" 
                    description="Data storage location may violate regional privacy laws"
                  />
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-4">
            <h4 className="text-base font-semibold text-gray-800 mb-3">Related Research</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              <RelatedResearchItem 
                title="Cloud Video Storage Requirements Calculator" 
                date="Mar 15, 2024" 
                excerpt="Tool for estimating bandwidth and storage needs based on camera count and settings"
              />
              <RelatedResearchItem 
                title="Cloud vs On-Premise Total Cost of Ownership Analysis" 
                date="Feb 28, 2024" 
                excerpt="5-year cost comparison across different deployment scenarios"
              />
              <RelatedResearchItem 
                title="Cloud Video Surveillance Cybersecurity Guide" 
                date="Jan 10, 2024" 
                excerpt="Best practices for securing cloud video implementations"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Trend Item Component
interface TrendItemProps {
  title: string;
  trend: 'Rising' | 'Falling' | 'Stable';
  impact: 'High' | 'Medium' | 'Low';
  description: string;
}

const TrendItem: React.FC<TrendItemProps> = ({ title, trend, impact, description }) => (
  <div className="border-b border-gray-100 pb-3 last:border-0 last:pb-0">
    <h4 className="font-medium text-gray-800 text-sm">{title}</h4>
    <div className="flex items-center mt-1">
      <span className={`text-xs font-medium px-2 py-0.5 rounded mr-2 ${
        trend === 'Rising' ? 'bg-green-100 text-green-800' : 
        trend === 'Falling' ? 'bg-red-100 text-red-800' : 
        'bg-blue-100 text-blue-800'
      }`}>
        {trend}
      </span>
      <span className={`text-xs font-medium px-2 py-0.5 rounded ${
        impact === 'High' ? 'bg-purple-100 text-purple-800' : 
        impact === 'Low' ? 'bg-gray-100 text-gray-800' : 
        'bg-yellow-100 text-yellow-800'
      }`}>
        {impact} Impact
      </span>
    </div>
    <p className="text-xs text-gray-600 mt-1">{description}</p>
  </div>
);

// Related Research Item Component
interface RelatedResearchItemProps {
  title: string;
  date: string;
  excerpt: string;
}

const RelatedResearchItem: React.FC<RelatedResearchItemProps> = ({ title, date, excerpt }) => (
  <div className="bg-gray-50 border border-gray-200 rounded-lg p-3">
    <h5 className="font-medium text-gray-800 text-sm">{title}</h5>
    <p className="text-xs text-gray-500 mt-1">{date}</p>
    <p className="text-xs text-gray-600 mt-1.5">{excerpt}</p>
  </div>
);

// Competitor Item Component
interface CompetitorItemProps {
  name: string;
  rating: 'High' | 'Medium' | 'Low';
  strength: string;
  weakness: string;
}

const CompetitorItem: React.FC<CompetitorItemProps> = ({ name, rating, strength, weakness }) => (
  <div className="border-b border-gray-100 pb-2 last:border-0 last:pb-0">
    <div className="flex justify-between items-center">
      <h5 className="font-medium text-gray-800 text-sm">{name}</h5>
      <span className={`text-xs font-medium px-2 py-0.5 rounded ${
        rating === 'High' ? 'bg-green-100 text-green-800' : 
        rating === 'Low' ? 'bg-red-100 text-red-800' : 
        'bg-yellow-100 text-yellow-800'
      }`}>
        {rating}
      </span>
    </div>
    <div className="mt-1 space-y-1">
      <div className="flex items-start">
        <span className="text-xs text-green-600 font-medium mr-1">+</span>
        <span className="text-xs text-gray-600">{strength}</span>
      </div>
      <div className="flex items-start">
        <span className="text-xs text-red-600 font-medium mr-1">-</span>
        <span className="text-xs text-gray-600">{weakness}</span>
      </div>
    </div>
  </div>
);

// Risk Item Component
interface RiskItemProps {
  category: string;
  level: 'High' | 'Medium' | 'Low';
  description: string;
}

const RiskItem: React.FC<RiskItemProps> = ({ category, level, description }) => (
  <div className="flex items-start">
    <div className="mr-2">
      <span className={`inline-block w-2 h-2 rounded-full ${
        level === 'High' ? 'bg-red-500' : 
        level === 'Low' ? 'bg-green-500' : 
        'bg-yellow-500'
      }`}></span>
    </div>
    <div>
      <h4 className="font-medium text-gray-800 text-xs">{category}</h4>
      <div className="flex items-center mt-0.5">
        <span className={`px-1.5 py-0.5 rounded text-xs font-medium ${
          level === 'High' ? 'bg-red-100 text-red-800' : 
          level === 'Low' ? 'bg-green-100 text-green-800' : 
          'bg-yellow-100 text-yellow-800'
        }`}>
          {level} Level
        </span>
      </div>
      <p className="text-xs text-gray-600 mt-1">{description}</p>
    </div>
  </div>
);

export default IntelligenceHub; 