"use client";

import React from 'react';
import { MapPin } from 'lucide-react';

// Project Lifecycle Component
const ProjectLifecycle: React.FC = () => {
  return (
    <div className="p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Project Lifecycle Management</h2>
        <p className="text-gray-600">Plan, design, and implement security systems with confidence</p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">System Design Assistant</h3>
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 h-80 flex flex-col items-center justify-center">
              <MapPin size={80} className="text-blue-300 mb-4" />
              <p className="text-gray-500 text-center max-w-md">
                Interactive floor plan visualization for camera placement, access control, and integrated systems
              </p>
              <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                Start New Design
              </button>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">RFP Generator</h3>
            <div className="border border-gray-200 rounded-lg">
              <div className="p-4 border-b border-gray-200 bg-gray-50">
                <h4 className="font-medium text-gray-800">Create Technical Specifications</h4>
                <p className="text-sm text-gray-600 mt-1">Generate detailed RFPs based on your requirements</p>
              </div>
              <div className="p-4">
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Project Type</label>
                    <select className="w-full border border-gray-300 rounded-md p-2 text-sm">
                      <option>Video Surveillance</option>
                      <option>Access Control</option>
                      <option>Integrated System</option>
                      <option>Weapons Detection</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Industry</label>
                    <select className="w-full border border-gray-300 rounded-md p-2 text-sm">
                      <option>Corporate</option>
                      <option>Education</option>
                      <option>Healthcare</option>
                      <option>Retail</option>
                      <option>Government</option>
                    </select>
                  </div>
                </div>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Key Requirements</label>
                  <div className="flex flex-wrap gap-2">
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">High Resolution</span>
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">Cloud Storage</span>
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">Analytics</span>
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">Mobile Access</span>
                    <span className="px-2 py-1 bg-gray-100 text-gray-800 text-xs rounded-full">+ Add More</span>
                  </div>
                </div>
                <div className="flex justify-end">
                  <button className="px-4 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700">
                    Generate RFP
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Projects</h3>
            <div className="space-y-3">
              <ProjectItem 
                title="Corporate HQ Security Upgrade" 
                status="In Progress"
                phase="Design"
                date="Feb 20, 2025"
              />
              <ProjectItem 
                title="Retail Chain Video Analytics" 
                status="Active"
                phase="Implementation"
                date="Jan 15, 2025"
              />
              <ProjectItem 
                title="Manufacturing Facility Access Control" 
                status="Completed"
                phase="Verification"
                date="Dec 10, 2024"
              />
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Vendor Proposal Analyzer</h3>
            <p className="text-gray-600 mb-4">Evaluate vendor responses against your requirements</p>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-gray-50 border border-gray-200 rounded-lg">
                <div>
                  <span className="block text-sm font-medium">Axis Communications</span>
                  <span className="text-xs text-gray-500">Proposal #AX-2025-104</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-600 font-medium mr-2">87%</span>
                  <span className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded">Match</span>
                </div>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 border border-gray-200 rounded-lg">
                <div>
                  <span className="block text-sm font-medium">Hanwha Techwin</span>
                  <span className="text-xs text-gray-500">Proposal #HW-0472</span>
                </div>
                <div className="flex items-center">
                  <span className="text-green-600 font-medium mr-2">82%</span>
                  <span className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded">Match</span>
                </div>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 border border-gray-200 rounded-lg">
                <div>
                  <span className="block text-sm font-medium">Motorola Solutions</span>
                  <span className="text-xs text-gray-500">Proposal #MS-2025-389</span>
                </div>
                <div className="flex items-center">
                  <span className="text-yellow-600 font-medium mr-2">76%</span>
                  <span className="text-xs px-2 py-1 bg-yellow-100 text-yellow-800 rounded">Match</span>
                </div>
              </div>
            </div>
            <button className="w-full mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
              Upload Proposal
            </button>
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
  <div className="border-b border-gray-100 pb-3">
    <h4 className="font-medium text-gray-800">{title}</h4>
    <div className="flex justify-between items-center mt-1">
      <span className={`px-2 py-1 rounded text-xs font-medium ${
        status === 'Completed' ? 'bg-green-100 text-green-800' : 
        status === 'In Progress' ? 'bg-blue-100 text-blue-800' : 
        'bg-yellow-100 text-yellow-800'
      }`}>
        {status}
      </span>
      <p className="text-gray-500 text-sm">{phase}</p>
    </div>
    <p className="text-gray-500 text-xs mt-1">Last updated: {date}</p>
  </div>
);

export default ProjectLifecycle; 