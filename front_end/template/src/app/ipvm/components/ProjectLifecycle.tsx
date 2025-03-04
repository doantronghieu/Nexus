"use client";

import React from 'react';
import { MapPin } from 'lucide-react';
import projectLifecycleData from '../data/projectLifecycle.json';

// Project Lifecycle Component
const ProjectLifecycle: React.FC = () => {
  // Get data from JSON
  const { projectTypes, industries, keyRequirements, recentProjects } = projectLifecycleData;
  
  return (
    <div className="module-container">
      <div className="module-header">
        <h2 className="text-xl font-bold text-gray-800">Project Lifecycle Management</h2>
        <p className="text-sm text-gray-600">Plan, design, and implement security systems with confidence</p>
      </div>
      
      <div className="module-content">
        <div className="module-grid h-full p-3">
          <div className="module-grid-item space-y-3">
            <div className="card h-auto">
              <div className="panel-header border-b border-gray-200">
                <h3 className="text-base font-semibold text-gray-800">System Design Assistant</h3>
              </div>
              <div className="panel-content">
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-3 flex flex-col items-center justify-center">
                  <MapPin size={60} className="text-blue-300 mb-3" />
                  <p className="text-gray-500 text-center text-xs max-w-md">
                    Interactive floor plan visualization for camera placement, access control, and integrated systems
                  </p>
                  <button className="mt-3 px-3 py-1.5 bg-blue-600 text-white text-xs rounded hover:bg-blue-700">
                    Start New Design
                  </button>
                </div>
              </div>
            </div>
            
            <div className="card h-auto">
              <div className="panel-header border-b border-gray-200">
                <h3 className="text-base font-semibold text-gray-800">RFP Generator</h3>
              </div>
              <div className="panel-content">
                <div className="border border-gray-200 rounded-lg">
                  <div className="p-3 border-b border-gray-200 bg-gray-50">
                    <h4 className="text-sm font-medium text-gray-800">Create Technical Specifications</h4>
                    <p className="text-xs text-gray-600 mt-1">Generate detailed RFPs based on your requirements</p>
                  </div>
                  <div className="p-3">
                    <div className="grid grid-cols-2 gap-3 mb-3">
                      <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">Project Type</label>
                        <select className="w-full border border-gray-300 rounded-md p-1.5 text-xs">
                          {projectTypes.map((type, index) => (
                            <option key={index}>{type}</option>
                          ))}
                        </select>
                      </div>
                      <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">Industry</label>
                        <select className="w-full border border-gray-300 rounded-md p-1.5 text-xs">
                          {industries.map((industry, index) => (
                            <option key={index}>{industry}</option>
                          ))}
                        </select>
                      </div>
                    </div>
                    <div className="mb-3">
                      <label className="block text-xs font-medium text-gray-700 mb-1">Key Requirements</label>
                      <div className="flex flex-wrap gap-1.5">
                        {keyRequirements.map((requirement, index) => (
                          <span key={index} className="px-2 py-0.5 bg-blue-100 text-blue-800 text-xs rounded-full">{requirement}</span>
                        ))}
                        <span className="px-2 py-0.5 bg-gray-100 text-gray-800 text-xs rounded-full">+ Add More</span>
                      </div>
                    </div>
                    <div className="flex justify-end">
                      <button className="px-3 py-1.5 bg-blue-600 text-white text-xs rounded hover:bg-blue-700">
                        Generate RFP
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="module-grid-item space-y-3">
            <div className="card h-auto">
              <div className="panel-header border-b border-gray-200">
                <h3 className="text-base font-semibold text-gray-800">Recent Projects</h3>
              </div>
              <div className="panel-content">
                <div className="space-y-2">
                  {recentProjects.map((project) => (
                    <ProjectItem 
                      key={project.id}
                      title={project.title} 
                      status={project.status as 'Completed' | 'In Progress' | 'Active'}
                      phase={project.phase}
                      date={project.date}
                    />
                  ))}
                </div>
              </div>
            </div>
            
            <div className="card h-auto">
              <div className="panel-header border-b border-gray-200">
                <h3 className="text-base font-semibold text-gray-800">Vendor Proposal Analyzer</h3>
              </div>
              <div className="panel-content">
                <p className="text-xs text-gray-600 mb-3">Evaluate vendor responses against your requirements</p>
                <div className="space-y-2">
                  <div className="flex justify-between items-center p-2 bg-gray-50 border border-gray-200 rounded-lg">
                    <div>
                      <span className="block text-xs font-medium">Axis Communications</span>
                      <span className="text-xs text-gray-500">Proposal #AX-2025-104</span>
                    </div>
                    <div className="flex items-center">
                      <span className="text-green-600 font-medium text-xs mr-2">87%</span>
                      <span className="text-xs px-1.5 py-0.5 bg-green-100 text-green-800 rounded">Match</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center p-2 bg-gray-50 border border-gray-200 rounded-lg">
                    <div>
                      <span className="block text-xs font-medium">Hanwha Techwin</span>
                      <span className="text-xs text-gray-500">Proposal #HW-0472</span>
                    </div>
                    <div className="flex items-center">
                      <span className="text-green-600 font-medium text-xs mr-2">82%</span>
                      <span className="text-xs px-1.5 py-0.5 bg-green-100 text-green-800 rounded">Match</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center p-2 bg-gray-50 border border-gray-200 rounded-lg">
                    <div>
                      <span className="block text-xs font-medium">Motorola Solutions</span>
                      <span className="text-xs text-gray-500">Proposal #MS-2025-389</span>
                    </div>
                    <div className="flex items-center">
                      <span className="text-yellow-600 font-medium text-xs mr-2">76%</span>
                      <span className="text-xs px-1.5 py-0.5 bg-yellow-100 text-yellow-800 rounded">Match</span>
                    </div>
                  </div>
                </div>
                <button className="w-full mt-3 px-3 py-1.5 bg-blue-600 text-white text-xs rounded hover:bg-blue-700">
                  Upload Proposal
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Project Item Component
interface ProjectItemProps {
  title: string;
  status: 'Completed' | 'In Progress' | 'Active';
  phase: string;
  date: string;
}

const ProjectItem: React.FC<ProjectItemProps> = ({ title, status, phase, date }) => (
  <div className="border-b border-gray-100 pb-2 last:border-0 last:pb-0">
    <h4 className="text-xs font-medium text-gray-800">{title}</h4>
    <div className="flex justify-between items-center mt-1">
      <span className={`px-1.5 py-0.5 rounded text-xs font-medium ${
        status === 'Completed' ? 'bg-green-100 text-green-800' : 
        status === 'In Progress' ? 'bg-blue-100 text-blue-800' : 
        'bg-yellow-100 text-yellow-800'
      }`}>
        {status}
      </span>
      <p className="text-gray-500 text-xs">{phase}</p>
    </div>
    <p className="text-gray-500 text-xs mt-1">Last updated: {date}</p>
  </div>
);

export default ProjectLifecycle; 