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
    <div className="p-6">
      <div className="mb-6 flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">Intelligence Hub</h2>
        <div className="flex space-x-2">
          <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Latest Research</button>
          <button className="px-4 py-2 bg-white border border-gray-300 rounded text-gray-700 hover:bg-gray-50">Export</button>
        </div>
      </div>

      {showAIResults ? (
        <AISearchResults query={searchQuery} />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Unified Knowledge Repository</h3>
              <div className="border border-gray-200 rounded-lg overflow-hidden">
                <div className="bg-gray-50 px-4 py-3 border-b border-gray-200 flex justify-between items-center">
                  <div>
                    <h4 className="font-medium text-gray-800">IPVM Research Database</h4>
                    <p className="text-sm text-gray-600">Comprehensive collection of testing and analysis</p>
                  </div>
                  <div className="flex space-x-2">
                    <select className="text-sm border border-gray-300 rounded p-1">
                      <option>All Categories</option>
                      <option>Video Surveillance</option>
                      <option>Access Control</option>
                      <option>Analytics</option>
                      <option>Cybersecurity</option>
                    </select>
                    <select className="text-sm border border-gray-300 rounded p-1">
                      <option>All Time</option>
                      <option>Last 30 Days</option>
                      <option>Last 90 Days</option>
                      <option>Last Year</option>
                    </select>
                  </div>
                </div>
                <div className="p-3 max-h-64 overflow-y-auto">
                  <div className="space-y-3">
                    <div className="border-b border-gray-100 pb-3">
                      <div className="flex items-center">
                        <div className="w-10 h-10 rounded-md bg-blue-100 flex items-center justify-center mr-3">
                          <Camera size={18} className="text-blue-600" />
                        </div>
                        <div>
                          <h5 className="font-medium text-gray-800">Cloud Going Mainstream In Video Surveillance</h5>
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
                        <div className="w-10 h-10 rounded-md bg-purple-100 flex items-center justify-center mr-3">
                          <Shield size={18} className="text-purple-600" />
                        </div>
                        <div>
                          <h5 className="font-medium text-gray-800">Mobile Credential Solutions Comparative Test</h5>
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
                        <div className="w-10 h-10 rounded-md bg-green-100 flex items-center justify-center mr-3">
                          <Brain size={18} className="text-green-600" />
                        </div>
                        <div>
                          <h5 className="font-medium text-gray-800">Person Detection Accuracy Benchmark</h5>
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
                <div className="bg-gray-50 px-4 py-3 border-t border-gray-200 flex justify-between items-center">
                  <span className="text-sm text-gray-500">1,500+ Research Reports Available</span>
                  <button className="text-sm text-blue-600 font-medium">Browse All</button>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-gray-800">Trending Technologies</h3>
                <button className="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center">
                  View All Trends <ArrowRight size={16} className="ml-1" />
                </button>
              </div>
              
              <div className="space-y-4">
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
          
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Market Trend Analyzer</h3>
              <div className="h-64 flex items-center justify-center bg-gray-50 rounded border border-gray-200">
                <PieChart size={180} className="text-blue-400" />
              </div>
              <div className="mt-4 space-y-2">
                <div className="flex items-center">
                  <div className="w-3 h-3 rounded-full bg-blue-500 mr-2"></div>
                  <span className="text-sm">Cloud-based Solutions (38%)</span>
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-3 rounded-full bg-blue-300 mr-2"></div>
                  <span className="text-sm">On-premise Systems (42%)</span>
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-3 rounded-full bg-blue-200 mr-2"></div>
                  <span className="text-sm">Hybrid Deployments (20%)</span>
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-600">M&A Activity:</span>
                  <span className="text-sm font-bold text-green-600">+12% YoY</span>
                </div>
                <div className="flex justify-between items-center mt-2">
                  <span className="text-sm font-medium text-gray-600">Funding Rounds:</span>
                  <span className="text-sm font-bold text-green-600">+8% QoQ</span>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Competitive Analysis Engine</h3>
              <div className="border border-gray-200 rounded-lg p-3 bg-gray-50">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="text-sm font-medium">Compare Products</h4>
                </div>
                <div className="space-y-2">
                  <div className="flex gap-2">
                    <select className="block w-full text-sm border border-gray-300 rounded p-2">
                      <option>Select Category</option>
                      <option>IP Cameras</option>
                      <option>VMS Systems</option>
                      <option>Access Control</option>
                      <option>Video Analytics</option>
                    </select>
                  </div>
                  <div className="flex gap-2">
                    <input type="text" placeholder="Add product to compare" className="block w-full text-sm border border-gray-300 rounded p-2" />
                    <button className="bg-blue-600 text-white p-2 rounded">+</button>
                  </div>
                  <div className="flex flex-wrap gap-2 mt-2">
                    <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full flex items-center">
                      Axis P3719-PLE <button className="ml-1 text-blue-600">×</button>
                    </span>
                    <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full flex items-center">
                      Hanwha XNP-9250R <button className="ml-1 text-blue-600">×</button>
                    </span>
                  </div>
                </div>
                <button className="w-full mt-3 px-3 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700">
                  Generate Comparison
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// AI Search Results Component
interface AISearchResultsProps {
  query: string;
}

const AISearchResults: React.FC<AISearchResultsProps> = ({ query }) => {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="mb-6">
        <h3 className="text-xl font-bold text-gray-800">IPVM Sentinel AI Results</h3>
        <p className="text-gray-600">Showing intelligence for: "{query}"</p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-blue-50 border border-blue-100 rounded-lg p-6">
            <div className="flex items-start mb-4">
              <Brain size={24} className="text-blue-600 mr-3 mt-1" />
              <div>
                <h4 className="text-lg font-semibold text-gray-800">AI Analysis</h4>
                <p className="text-gray-600 mt-1">
                  Based on IPVM research and testing data, here's what you should know about {query}:
                </p>
              </div>
            </div>
            
            <div className="prose max-w-none">
              <p>
                Recent IPVM testing shows cloud-based video surveillance solutions are seeing increasing adoption across 
                enterprise markets. Major manufacturers including Genetec, Axis, and Motorola have launched new cloud platforms 
                in the past 6 months, signaling a significant market shift.
              </p>
              <p className="mt-4">
                Key considerations for implementation include:
              </p>
              <ul className="list-disc pl-5 mt-2 space-y-1">
                <li>Bandwidth requirements for different resolution streams</li>
                <li>Data sovereignty and compliance with regional regulations</li>
                <li>Total cost of ownership compared to on-premise systems</li>
                <li>Integration capabilities with existing access control systems</li>
              </ul>
            </div>
          </div>
          
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h4 className="text-lg font-semibold text-gray-800 mb-4">Related Research</h4>
            <div className="space-y-4">
              <RelatedResearchItem 
                title="Cloud Going Mainstream In Video Surveillance" 
                date="Apr 23, 2024"
                excerpt="Cloud is going mainstream in video surveillance. Based on IPVM's research and reporting, here are key changes driving this..."
              />
              <RelatedResearchItem 
                title="VSaaS State of The Market 2024" 
                date="Mar 15, 2024"
                excerpt="Comprehensive analysis of VSaaS market trends, including adoption rates, key providers, and technology advancements..."
              />
              <RelatedResearchItem 
                title="Milestone Merges With Arcules" 
                date="Jan 30, 2024"
                excerpt="Milestone is merging with Arcules, bringing back the company spun out of Milestone (then called Arcus Global) in 2017..."
              />
            </div>
          </div>
        </div>
        
        <div className="space-y-6">
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h4 className="text-lg font-semibold text-gray-800 mb-4">Knowledge Graph</h4>
            <div className="bg-gray-50 border border-gray-200 rounded p-3 mb-4 aspect-square flex items-center justify-center">
              <div className="text-center">
                <svg width="180" height="180" viewBox="0 0 200 200">
                  <circle cx="100" cy="100" r="25" fill="#3B82F6" />
                  <text x="100" y="105" textAnchor="middle" fill="white" fontSize="12">Cloud VSaaS</text>
                  
                  <circle cx="50" cy="50" r="15" fill="#93C5FD" />
                  <text x="50" y="54" textAnchor="middle" fill="#1E3A8A" fontSize="8">Genetec</text>
                  <line x1="65" y1="65" x2="85" y2="85" stroke="#9CA3AF" strokeWidth="1" />
                  
                  <circle cx="150" cy="50" r="15" fill="#93C5FD" />
                  <text x="150" y="54" textAnchor="middle" fill="#1E3A8A" fontSize="8">Eagle Eye</text>
                  <line x1="135" y1="65" x2="115" y2="85" stroke="#9CA3AF" strokeWidth="1" />
                  
                  <circle cx="50" cy="150" r="15" fill="#BFDBFE" />
                  <text x="50" y="154" textAnchor="middle" fill="#1E3A8A" fontSize="8">Axis</text>
                  <line x1="65" y1="135" x2="85" y2="115" stroke="#9CA3AF" strokeWidth="1" />
                  
                  <circle cx="150" cy="150" r="15" fill="#BFDBFE" />
                  <text x="150" y="154" textAnchor="middle" fill="#1E3A8A" fontSize="8">Verkada</text>
                  <line x1="135" y1="135" x2="115" y2="115" stroke="#9CA3AF" strokeWidth="1" />
                </svg>
              </div>
            </div>
            <p className="text-xs text-gray-500 text-center">Knowledge graph visualization of cloud video surveillance ecosystem</p>
          </div>
          
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h4 className="text-lg font-semibold text-gray-800 mb-4">Competitive Analysis</h4>
            <div className="space-y-3">
              <CompetitorItem 
                name="Genetec Cloud" 
                rating="High"
                strength="Enterprise integration capabilities"
                weakness="Premium pricing"
              />
              <CompetitorItem 
                name="Eagle Eye Networks" 
                rating="High"
                strength="Bandwidth management technology"
                weakness="Limited analytics options"
              />
              <CompetitorItem 
                name="Verkada" 
                rating="Medium"
                strength="Simplified deployment"
                weakness="Closed ecosystem"
              />
            </div>
          </div>
          
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h4 className="text-lg font-semibold text-gray-800 mb-4">Implementation Risk</h4>
            <div className="flex justify-center mb-4">
              <div className="w-32 h-32 rounded-full border-8 border-blue-500 flex items-center justify-center">
                <span className="text-2xl font-bold text-blue-600">Medium</span>
              </div>
            </div>
            <div className="space-y-2">
              <RiskItem 
                category="Security" 
                level="Medium"
                description="Data encryption in transit and at rest"
              />
              <RiskItem 
                category="Reliability" 
                level="Low"
                description="Dependent on internet connectivity"
              />
              <RiskItem 
                category="Compliance" 
                level="High"
                description="Regional data storage requirements"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Reusable components for dashboard items
interface TrendItemProps {
  title: string;
  trend: 'Rising' | 'Falling' | 'Stable';
  impact: 'High' | 'Medium' | 'Low';
  description: string;
}

const TrendItem: React.FC<TrendItemProps> = ({ title, trend, impact, description }) => (
  <div className="border-b border-gray-100 pb-4">
    <div className="flex items-start justify-between">
      <h4 className="font-medium text-gray-800">{title}</h4>
      <div className="flex items-center space-x-2">
        <span className={`px-2 py-1 rounded text-xs font-medium ${
          trend === 'Rising' ? 'bg-green-100 text-green-800' : 
          trend === 'Falling' ? 'bg-red-100 text-red-800' : 
          'bg-blue-100 text-blue-800'
        }`}>
          {trend}
        </span>
        <span className={`px-2 py-1 rounded text-xs font-medium ${
          impact === 'High' ? 'bg-orange-100 text-orange-800' : 
          impact === 'Low' ? 'bg-gray-100 text-gray-800' : 
          'bg-yellow-100 text-yellow-800'
        }`}>
          {impact} Impact
        </span>
      </div>
    </div>
    <p className="text-gray-600 text-sm mt-1">{description}</p>
  </div>
);

interface RelatedResearchItemProps {
  title: string;
  date: string;
  excerpt: string;
}

const RelatedResearchItem: React.FC<RelatedResearchItemProps> = ({ title, date, excerpt }) => (
  <div className="border-b border-gray-100 pb-4">
    <h4 className="font-medium text-gray-800">{title}</h4>
    <p className="text-gray-500 text-sm">{date}</p>
    <p className="text-gray-600 text-sm mt-1">{excerpt}</p>
    <a href="#" className="text-blue-600 hover:text-blue-800 text-sm font-medium mt-2 inline-block">
      Read More
    </a>
  </div>
);

interface CompetitorItemProps {
  name: string;
  rating: 'High' | 'Medium' | 'Low';
  strength: string;
  weakness: string;
}

const CompetitorItem: React.FC<CompetitorItemProps> = ({ name, rating, strength, weakness }) => (
  <div className="border-b border-gray-100 pb-3">
    <div className="flex justify-between items-center">
      <h4 className="font-medium text-gray-800">{name}</h4>
      <span className={`px-2 py-1 rounded text-xs font-medium ${
        rating === 'High' ? 'bg-green-100 text-green-800' : 
        rating === 'Low' ? 'bg-red-100 text-red-800' : 
        'bg-yellow-100 text-yellow-800'
      }`}>
        {rating} Rating
      </span>
    </div>
    <div className="mt-1 space-y-1">
      <div className="flex items-start">
        <span className="text-green-500 text-sm mr-2">+</span>
        <p className="text-gray-600 text-sm">{strength}</p>
      </div>
      <div className="flex items-start">
        <span className="text-red-500 text-sm mr-2">-</span>
        <p className="text-gray-600 text-sm">{weakness}</p>
      </div>
    </div>
  </div>
);

interface RiskItemProps {
  category: string;
  level: 'High' | 'Medium' | 'Low';
  description: string;
}

const RiskItem: React.FC<RiskItemProps> = ({ category, level, description }) => (
  <div className="flex items-center justify-between border-b border-gray-100 pb-2">
    <div>
      <p className="text-sm font-medium text-gray-800">{category}</p>
      <p className="text-gray-600 text-xs">{description}</p>
    </div>
    <span className={`px-2 py-1 rounded text-xs font-medium ${
      level === 'High' ? 'bg-red-100 text-red-800' : 
      level === 'Low' ? 'bg-green-100 text-green-800' : 
      'bg-yellow-100 text-yellow-800'
    }`}>
      {level}
    </span>
  </div>
);

export default IntelligenceHub; 