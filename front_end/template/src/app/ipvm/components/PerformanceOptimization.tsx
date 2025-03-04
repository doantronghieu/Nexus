"use client";

import React from 'react';
import { TrendingUp } from 'lucide-react';

// Performance Optimization Component
const PerformanceOptimization: React.FC = () => {
  return (
    <div className="p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Performance Optimization</h2>
        <p className="text-gray-600">Evaluate and improve system performance with objective data</p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">System Performance Dashboard</h3>
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 h-80 flex items-center justify-center">
              <TrendingUp size={150} className="text-blue-200" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Test Lab Integration</h3>
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
                <h4 className="font-medium text-gray-800">Performance Verification</h4>
                <p className="text-sm text-gray-600">Compare field performance with IPVM lab results</p>
              </div>
              <div className="p-4">
                <div className="space-y-4">
                  <div className="bg-white border border-gray-200 rounded-lg p-3">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium text-gray-800">Camera Field of View</span>
                      <span className="text-xs px-2 py-1 rounded-full bg-green-100 text-green-800">Matches Lab Results</span>
                    </div>
                    <div className="bg-gray-50 rounded h-10 overflow-hidden">
                      <div className="bg-green-500 h-full" style={{width: '95%'}}></div>
                    </div>
                    <div className="flex justify-between mt-1">
                      <span className="text-xs text-gray-500">Field: 94.8%</span>
                      <span className="text-xs text-gray-500">Lab: 96.2%</span>
                    </div>
                  </div>
                  
                  <div className="bg-white border border-gray-200 rounded-lg p-3">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium text-gray-800">Low Light Performance</span>
                      <span className="text-xs px-2 py-1 rounded-full bg-yellow-100 text-yellow-800">Below Lab Results</span>
                    </div>
                    <div className="bg-gray-50 rounded h-10 overflow-hidden">
                      <div className="bg-yellow-500 h-full" style={{width: '72%'}}></div>
                    </div>
                    <div className="flex justify-between mt-1">
                      <span className="text-xs text-gray-500">Field: 72.3%</span>
                      <span className="text-xs text-gray-500">Lab: 88.7%</span>
                    </div>
                  </div>
                  
                  <div className="bg-white border border-gray-200 rounded-lg p-3">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium text-gray-800">Analytics Detection Accuracy</span>
                      <span className="text-xs px-2 py-1 rounded-full bg-green-100 text-green-800">Matches Lab Results</span>
                    </div>
                    <div className="bg-gray-50 rounded h-10 overflow-hidden">
                      <div className="bg-green-500 h-full" style={{width: '91%'}}></div>
                    </div>
                    <div className="flex justify-between mt-1">
                      <span className="text-xs text-gray-500">Field: 91.1%</span>
                      <span className="text-xs text-gray-500">Lab: 92.5%</span>
                    </div>
                  </div>
                </div>
                
                <div className="mt-4 flex justify-end">
                  <button className="px-4 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700">
                    Generate Performance Report
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Benchmarking</h3>
            <div className="space-y-3">
              <BenchmarkItem 
                category="Video Quality" 
                yourScore={82}
                industryAvg={75}
              />
              <BenchmarkItem 
                category="Storage Efficiency" 
                yourScore={90}
                industryAvg={84}
              />
              <BenchmarkItem 
                category="Analytics Accuracy" 
                yourScore={78}
                industryAvg={80}
              />
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Security Posture Assessment</h3>
            <div className="flex items-center justify-center mb-4">
              <div className="relative w-32 h-32">
                <svg className="w-full h-full" viewBox="0 0 36 36">
                  <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="#e6e6e6"
                    strokeWidth="2"
                  />
                  <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="#4F46E5"
                    strokeWidth="2"
                    strokeDasharray="75, 100"
                  />
                </svg>
                <div className="absolute top-0 left-0 w-full h-full flex items-center justify-center flex-col">
                  <span className="text-3xl font-bold text-blue-700">75</span>
                  <span className="text-xs text-gray-500">Security Score</span>
                </div>
              </div>
            </div>
            
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Cybersecurity</span>
                <div className="w-24 bg-gray-200 h-2 rounded-full overflow-hidden">
                  <div className="bg-green-500 h-full" style={{width: '85%'}}></div>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Physical Security</span>
                <div className="w-24 bg-gray-200 h-2 rounded-full overflow-hidden">
                  <div className="bg-green-500 h-full" style={{width: '78%'}}></div>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Vulnerability Management</span>
                <div className="w-24 bg-gray-200 h-2 rounded-full overflow-hidden">
                  <div className="bg-yellow-500 h-full" style={{width: '65%'}}></div>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Regulatory Compliance</span>
                <div className="w-24 bg-gray-200 h-2 rounded-full overflow-hidden">
                  <div className="bg-yellow-500 h-full" style={{width: '62%'}}></div>
                </div>
              </div>
            </div>
            
            <div className="mt-4">
              <button className="w-full px-4 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700">
                View Full Assessment
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Benchmark Item Component
interface BenchmarkItemProps {
  category: string;
  yourScore: number;
  industryAvg: number;
}

const BenchmarkItem: React.FC<BenchmarkItemProps> = ({ category, yourScore, industryAvg }) => (
  <div className="border-b border-gray-100 pb-3">
    <div className="flex justify-between items-center">
      <p className="text-sm font-medium text-gray-800">{category}</p>
      <div className="flex items-center space-x-3">
        <div className="flex items-center">
          <div className="w-2 h-2 rounded-full bg-blue-600 mr-1"></div>
          <span className="text-sm">{yourScore}</span>
        </div>
        <div className="flex items-center">
          <div className="w-2 h-2 rounded-full bg-gray-400 mr-1"></div>
          <span className="text-sm text-gray-600">{industryAvg}</span>
        </div>
      </div>
    </div>
    <div className="mt-2 bg-gray-200 h-2 rounded-full overflow-hidden">
      <div 
        className="bg-blue-600 h-full rounded-full" 
        style={{ width: `${yourScore}%` }}
      ></div>
    </div>
    <div className="flex justify-between text-xs text-gray-500 mt-1">
      <span>Your Score</span>
      <span>Industry Average</span>
    </div>
  </div>
);

export default PerformanceOptimization; 