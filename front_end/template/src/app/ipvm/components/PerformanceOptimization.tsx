"use client";

import React from 'react';
import { TrendingUp } from 'lucide-react';

// Performance Optimization Component
const PerformanceOptimization: React.FC = () => {
  return (
    <div className="viewport-fit">
      <div className="module-container">
        <div className="module-header">
          <h2 className="text-xl font-semibold text-gray-800">Performance Optimization</h2>
          <p className="text-sm text-gray-600">Evaluate and improve system performance with objective data</p>
        </div>
        
        <div className="module-content">
          <div className="module-grid compact-gap">
            <div className="module-grid-item space-y-3">
              <div className="card">
                <div className="panel-header border-b border-gray-200">
                  <h3 className="text-base font-semibold text-gray-800">System Performance Dashboard</h3>
                </div>
                <div className="panel-content compact-p">
                  <div className="bg-gray-50 border border-gray-200 rounded-lg p-2 h-48 flex items-center justify-center">
                    <TrendingUp size={100} className="text-blue-200" />
                  </div>
                </div>
              </div>
              
              <div className="card">
                <div className="panel-header border-b border-gray-200">
                  <h3 className="text-base font-semibold text-gray-800">Test Lab Integration</h3>
                </div>
                <div className="panel-content compact-p">
                  <div className="space-y-2">
                    <div className="bg-white border border-gray-200 rounded-lg p-2">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-sm font-medium text-gray-800">Camera Field of View</span>
                        <span className="text-xs px-1.5 py-0.5 rounded-full bg-green-100 text-green-800">Matches Lab Results</span>
                      </div>
                      <div className="bg-gray-50 rounded h-6 overflow-hidden">
                        <div className="bg-green-500 h-full" style={{width: '95%'}}></div>
                      </div>
                      <div className="flex justify-between mt-0.5">
                        <span className="text-xs text-gray-600">Field: 94.8%</span>
                        <span className="text-xs text-gray-600">Lab: 96.2%</span>
                      </div>
                    </div>
                    
                    <div className="bg-white border border-gray-200 rounded-lg p-2">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-sm font-medium text-gray-800">Low Light Performance</span>
                        <span className="text-xs px-1.5 py-0.5 rounded-full bg-yellow-100 text-yellow-800">Minor Deviation</span>
                      </div>
                      <div className="bg-gray-50 rounded h-6 overflow-hidden">
                        <div className="bg-yellow-500 h-full" style={{width: '72%'}}></div>
                      </div>
                      <div className="flex justify-between mt-0.5">
                        <span className="text-xs text-gray-600">Field: 82.3%</span>
                        <span className="text-xs text-gray-600">Lab: 89.1%</span>
                      </div>
                    </div>
                    
                    <div className="bg-white border border-gray-200 rounded-lg p-2">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-sm font-medium text-gray-800">Analytics Detection Accuracy</span>
                        <span className="text-xs px-1.5 py-0.5 rounded-full bg-red-100 text-red-800">Significant Deviation</span>
                      </div>
                      <div className="bg-gray-50 rounded h-6 overflow-hidden">
                        <div className="bg-red-500 h-full" style={{width: '68.7%'}}></div>
                      </div>
                      <div className="flex justify-between mt-0.5">
                        <span className="text-xs text-gray-600">Field: 68.7%</span>
                        <span className="text-xs text-gray-600">Lab: 91.5%</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-2 flex justify-end">
                    <button className="px-3 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700">
                      Generate Performance Report
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="module-grid-item space-y-3">
              <div className="card">
                <div className="panel-header border-b border-gray-200">
                  <h3 className="text-base font-semibold text-gray-800">Benchmarking</h3>
                </div>
                <div className="panel-content compact-p">
                  <div className="space-y-2">
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
              </div>
              
              <div className="card">
                <div className="panel-header border-b border-gray-200">
                  <h3 className="text-base font-semibold text-gray-800">Security Posture Assessment</h3>
                </div>
                <div className="panel-content compact-p">
                  <div className="flex items-center justify-center mb-2">
                    <div className="relative w-24 h-24">
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
                        <span className="text-2xl font-bold text-blue-700">75</span>
                        <span className="text-xs text-gray-500">Security Score</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-1.5">
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-gray-600">Cybersecurity</span>
                      <div className="w-24 bg-gray-200 h-2 rounded-full overflow-hidden">
                        <div className="bg-green-500 h-full" style={{width: '85%'}}></div>
                      </div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-gray-600">Physical Security</span>
                      <div className="w-24 bg-gray-200 h-2 rounded-full overflow-hidden">
                        <div className="bg-green-500 h-full" style={{width: '78%'}}></div>
                      </div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-gray-600">Vulnerability Management</span>
                      <div className="w-24 bg-gray-200 h-2 rounded-full overflow-hidden">
                        <div className="bg-yellow-500 h-full" style={{width: '65%'}}></div>
                      </div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-gray-600">Regulatory Compliance</span>
                      <div className="w-24 bg-gray-200 h-2 rounded-full overflow-hidden">
                        <div className="bg-yellow-500 h-full" style={{width: '62%'}}></div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-2">
                    <button className="w-full px-3 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700">
                      View Full Assessment
                    </button>
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

// Benchmark Item Component
interface BenchmarkItemProps {
  category: string;
  yourScore: number;
  industryAvg: number;
}

const BenchmarkItem: React.FC<BenchmarkItemProps> = ({ category, yourScore, industryAvg }) => (
  <div className="border-b border-gray-100 pb-2">
    <div className="flex justify-between items-center">
      <p className="text-xs font-medium text-gray-800">{category}</p>
      <div className="flex items-center space-x-2">
        <div className="flex items-center">
          <div className="w-2 h-2 rounded-full bg-blue-600 mr-1"></div>
          <span className="text-xs">{yourScore}</span>
        </div>
        <div className="flex items-center">
          <div className="w-2 h-2 rounded-full bg-gray-400 mr-1"></div>
          <span className="text-xs text-gray-600">{industryAvg}</span>
        </div>
      </div>
    </div>
    <div className="mt-1 bg-gray-200 h-2 rounded-full overflow-hidden">
      <div 
        className="bg-blue-600 h-full rounded-full" 
        style={{ width: `${yourScore}%` }}
      ></div>
    </div>
    <div className="flex justify-between text-xs text-gray-500 mt-0.5">
      <span>Your Score</span>
      <span>Industry Average</span>
    </div>
  </div>
);

export default PerformanceOptimization; 