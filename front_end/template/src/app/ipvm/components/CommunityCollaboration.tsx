"use client";

import React from 'react';

// Community & Collaboration Component
const CommunityCollaboration: React.FC = () => {
  return (
    <div className="viewport-fit">
      <div className="module-container">
        <div className="module-header">
          <h2 className="text-xl font-semibold text-gray-800">Community & Collaboration</h2>
          <p className="text-sm text-gray-600">Connect with security professionals and share insights</p>
        </div>
        
        <div className="module-content">
          <div className="module-grid compact-gap">
            <div className="module-grid-item space-y-3">
              <div className="card">
                <div className="panel-header border-b border-gray-200">
                  <h3 className="text-base font-semibold text-gray-800">Community Discussions</h3>
                </div>
                <div className="panel-content compact-p">
                  <div className="space-y-2 module-content-scrollable">
                    <DiscussionItem 
                      title="Best Practices for Cloud Video Migration" 
                      author="Security Director"
                      organization="Financial Services"
                      replies={15}
                      views={342}
                      date="1 day ago"
                    />
                    <DiscussionItem 
                      title="Integrating Weapons Detection with Access Control" 
                      author="Systems Engineer"
                      organization="Education"
                      replies={9}
                      views={201}
                      date="2 days ago"
                    />
                    <DiscussionItem 
                      title="EU AI Act Compliance for Video Analytics" 
                      author="Chief Security Officer"
                      organization="Retail"
                      replies={24}
                      views={587}
                      date="5 days ago"
                    />
                  </div>
                </div>
              </div>
              
              <div className="card">
                <div className="panel-header border-b border-gray-200">
                  <h3 className="text-base font-semibold text-gray-800">Regulatory Compliance Tracker</h3>
                </div>
                <div className="panel-content compact-p">
                  <div className="overflow-x-auto module-content-scrollable">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th scope="col" className="px-2 py-1.5 text-left text-sm font-medium text-gray-700">Regulation</th>
                          <th scope="col" className="px-2 py-1.5 text-left text-sm font-medium text-gray-700">Region</th>
                          <th scope="col" className="px-2 py-1.5 text-left text-sm font-medium text-gray-700">Status</th>
                          <th scope="col" className="px-2 py-1.5 text-left text-sm font-medium text-gray-700">Impact</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        <tr>
                          <td className="px-2 py-1.5 text-sm text-gray-800">EU AI Act</td>
                          <td className="px-2 py-1.5 text-sm text-gray-800">Europe</td>
                          <td className="px-2 py-1.5">
                            <span className="px-1.5 py-0.5 text-xs rounded-full bg-yellow-100 text-yellow-800">Pending</span>
                          </td>
                          <td className="px-2 py-1.5 text-sm text-gray-800">High</td>
                        </tr>
                        <tr>
                          <td className="px-2 py-1.5 text-sm text-gray-800">NDAA Compliance</td>
                          <td className="px-2 py-1.5 text-sm text-gray-800">USA</td>
                          <td className="px-2 py-1.5">
                            <span className="px-1.5 py-0.5 text-xs rounded-full bg-green-100 text-green-800">Active</span>
                          </td>
                          <td className="px-2 py-1.5 text-sm text-gray-800">High</td>
                        </tr>
                        <tr>
                          <td className="px-2 py-1.5 text-sm text-gray-800">BSIA 1175</td>
                          <td className="px-2 py-1.5 text-sm text-gray-800">UK</td>
                          <td className="px-2 py-1.5">
                            <span className="px-1.5 py-0.5 text-xs rounded-full bg-green-100 text-green-800">Active</span>
                          </td>
                          <td className="px-2 py-1.5 text-sm text-gray-800">Medium</td>
                        </tr>
                        <tr>
                          <td className="px-2 py-1.5 text-sm text-gray-800">PIPEDA Update</td>
                          <td className="px-2 py-1.5 text-sm text-gray-800">Canada</td>
                          <td className="px-2 py-1.5">
                            <span className="px-1.5 py-0.5 text-xs rounded-full bg-red-100 text-red-800">Proposed</span>
                          </td>
                          <td className="px-2 py-1.5 text-sm text-gray-800">Medium</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="module-grid-item space-y-3">
              <div className="card">
                <div className="panel-header border-b border-gray-200">
                  <h3 className="text-base font-semibold text-gray-800">Expert Directory</h3>
                </div>
                <div className="panel-content compact-p">
                  <div className="space-y-2 module-content-scrollable">
                    <ExpertItem 
                      name="Sarah Johnson" 
                      expertise="Video Analytics"
                      organization="IPVM"
                      rating={4.9}
                    />
                    <ExpertItem 
                      name="Michael Chen" 
                      expertise="Access Control"
                      organization="Security Consultant"
                      rating={4.8}
                    />
                    <ExpertItem 
                      name="Aisha Patel" 
                      expertise="Cloud Security"
                      organization="Enterprise Security"
                      rating={4.7}
                    />
                  </div>
                  <button className="w-full mt-2 px-3 py-1 bg-gray-100 text-gray-800 text-xs rounded border border-gray-300 hover:bg-gray-200">
                    View All Experts
                  </button>
                </div>
              </div>
              
              <div className="card">
                <div className="panel-header border-b border-gray-200">
                  <h3 className="text-base font-semibold text-gray-800">Training & Certification</h3>
                </div>
                <div className="panel-content compact-p">
                  <p className="text-xs text-gray-600 mb-2">Educational modules based on IPVM research and industry best practices</p>
                  <div className="space-y-2 module-content-scrollable">
                    <div className="border border-gray-200 rounded-lg p-2">
                      <div className="flex justify-between items-start">
                        <div>
                          <h4 className="text-xs font-medium text-gray-800">Video Surveillance Fundamentals</h4>
                          <p className="text-xs text-gray-500 mt-0.5">12 modules | 6 hours | Certificate</p>
                        </div>
                        <span className="px-1.5 py-0.5 bg-blue-100 text-blue-800 text-xs rounded-full">Popular</span>
                      </div>
                    </div>
                    <div className="border border-gray-200 rounded-lg p-2">
                      <div className="flex justify-between items-start">
                        <div>
                          <h4 className="text-xs font-medium text-gray-800">Advanced Analytics Configuration</h4>
                          <p className="text-xs text-gray-500 mt-0.5">8 modules | 4 hours | Certificate</p>
                        </div>
                        <span className="px-1.5 py-0.5 bg-green-100 text-green-800 text-xs rounded-full">New</span>
                      </div>
                    </div>
                    <div className="border border-gray-200 rounded-lg p-2">
                      <div className="flex justify-between items-start">
                        <div>
                          <h4 className="text-xs font-medium text-gray-800">Security System Design</h4>
                          <p className="text-xs text-gray-500 mt-0.5">10 modules | 8 hours | Certificate</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <button className="w-full mt-2 px-3 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700">
                    Browse All Courses
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Discussion Item Component
interface DiscussionItemProps {
  title: string;
  author: string;
  organization: string;
  replies: number;
  views: number;
  date: string;
}

const DiscussionItem: React.FC<DiscussionItemProps> = ({ title, author, organization, replies, views, date }) => (
  <div className="border-b border-gray-100 pb-2">
    <h4 className="text-xs font-medium text-gray-800">{title}</h4>
    <div className="flex items-center mt-0.5">
      <span className="text-gray-600 text-xs">{author}</span>
      <span className="mx-1 text-gray-400">•</span>
      <span className="text-gray-600 text-xs">{organization}</span>
    </div>
    <div className="flex items-center mt-1 text-gray-500 text-xs">
      <span>{replies} replies</span>
      <span className="mx-1">•</span>
      <span>{views} views</span>
      <span className="mx-1">•</span>
      <span>{date}</span>
    </div>
  </div>
);

// Expert Item Component
interface ExpertItemProps {
  name: string;
  expertise: string;
  organization: string;
  rating: number;
}

const ExpertItem: React.FC<ExpertItemProps> = ({ name, expertise, organization, rating }) => (
  <div className="border-b border-gray-100 pb-2">
    <h4 className="text-xs font-medium text-gray-800">{name}</h4>
    <p className="text-blue-600 text-xs mt-0.5">{expertise}</p>
    <div className="flex justify-between items-center mt-0.5">
      <p className="text-gray-600 text-xs">{organization}</p>
      <div className="flex items-center">
        <span className="text-yellow-500 mr-0.5">★</span>
        <span className="text-xs">{rating}</span>
      </div>
    </div>
  </div>
);

export default CommunityCollaboration; 