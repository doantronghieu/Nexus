"use client";

import React, { useState, useEffect } from 'react';
import { TrendingUp, Filter, ChevronDown, Info, Camera, Server, Shield } from 'lucide-react';
import performanceOptimizationData from '../data/performanceOptimization.json';

// Define types for our data
interface Product {
  id: string;
  name: string;
  manufacturer: string;
  category: string;
  image: string;
  description: string;
}

interface ProductPerformance {
  name: string;
  manufacturer: string;
  score: number;
  category: string;
}

interface TestLabItem {
  title: string;
  status: string;
  fieldValue: number;
  labValue: number;
  percentage: number;
  product: {
    name: string;
    manufacturer: string;
    category: string;
    image: string;
  };
}

interface Benchmark {
  category: string;
  yourScore: number;
  industryAvg: number;
  products: ProductPerformance[];
}

// Performance Optimization Component
const PerformanceOptimization: React.FC = () => {
  // Get data from JSON
  const { testLabIntegration, benchmarks, products } = performanceOptimizationData as {
    testLabIntegration: TestLabItem[];
    benchmarks: Benchmark[];
    products: Product[];
  };
  
  // State for selected product filter
  const [selectedProduct, setSelectedProduct] = useState<string>('all');
  const [dropdownOpen, setDropdownOpen] = useState<boolean>(false);
  const [filteredTestData, setFilteredTestData] = useState<TestLabItem[]>(testLabIntegration);
  const [selectedProductDetails, setSelectedProductDetails] = useState<Product | null>(null);
  
  // Function to determine status color
  const getStatusColor = (status: string) => {
    if (status === 'Matches Lab Results') return 'green';
    if (status === 'Minor Deviation') return 'yellow';
    if (status === 'Significant Deviation') return 'red';
    return 'gray';
  };
  
  // Filter test data when selected product changes
  useEffect(() => {
    if (selectedProduct === 'all') {
      setFilteredTestData(testLabIntegration);
      setSelectedProductDetails(null);
    } else {
      const product = products.find(p => p.id === selectedProduct) || null;
      setSelectedProductDetails(product);
      
      const filtered = testLabIntegration.filter(
        item => product && item.product.name === product.name
      );
      
      // If no items match the filter, show all items
      setFilteredTestData(filtered.length > 0 ? filtered : testLabIntegration);
    }
  }, [selectedProduct, testLabIntegration, products]);
  
  // Toggle dropdown
  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };
  
  // Select product
  const selectProduct = (productId: string) => {
    setSelectedProduct(productId);
    setDropdownOpen(false);
  };
  
  return (
    <div className="viewport-fit">
      <div className="module-container">
        <div className="module-header flex justify-between items-center">
          <div>
            <h2 className="text-xl font-semibold text-gray-800">Performance Optimization</h2>
            <p className="text-sm text-gray-600">Evaluate and improve system performance with objective data</p>
          </div>
          
          {/* Product Filter Dropdown */}
          <div className="relative">
            <button 
              className="flex items-center space-x-1 px-3 py-1.5 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
              onClick={toggleDropdown}
            >
              <Filter size={14} />
              <span>{selectedProduct === 'all' ? 'All Products' : selectedProductDetails?.name || 'Select Product'}</span>
              <ChevronDown size={14} />
            </button>
            
            {dropdownOpen && (
              <div className="absolute right-0 mt-1 w-64 bg-white border border-gray-200 rounded-md shadow-lg z-10">
                <ul className="py-1 max-h-60 overflow-auto">
                  <li>
                    <button
                      className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-100 ${selectedProduct === 'all' ? 'bg-blue-50 text-blue-700' : ''}`}
                      onClick={() => selectProduct('all')}
                    >
                      All Products
                    </button>
                  </li>
                  {products.map((product) => (
                    <li key={product.id}>
                      <button
                        className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-100 ${selectedProduct === product.id ? 'bg-blue-50 text-blue-700' : ''}`}
                        onClick={() => selectProduct(product.id)}
                      >
                        <div className="flex items-center">
                          <span className="font-medium">{product.name}</span>
                        </div>
                        <div className="text-xs text-gray-500">{product.manufacturer}</div>
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
        
        {/* Selected Product Details */}
        {selectedProductDetails && (
          <div className="bg-blue-50 border border-blue-100 rounded-lg p-3 mb-4">
            <div className="flex items-start">
              <div className="w-16 h-16 bg-gray-200 rounded-md flex items-center justify-center mr-3 overflow-hidden">
                {selectedProductDetails.image ? (
                  <img 
                    src={selectedProductDetails.image} 
                    alt={selectedProductDetails.name} 
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <Camera size={32} className="text-gray-400" />
                )}
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-800">{selectedProductDetails.name}</h3>
                <p className="text-sm text-gray-600">{selectedProductDetails.manufacturer} • {selectedProductDetails.category}</p>
                <p className="text-sm text-gray-700 mt-1">{selectedProductDetails.description}</p>
              </div>
            </div>
          </div>
        )}
        
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
                    {filteredTestData.map((item, index) => {
                      const statusColor = getStatusColor(item.status);
                      return (
                        <div key={index} className="bg-white border border-gray-200 rounded-lg p-2">
                          <div className="flex justify-between items-center mb-1">
                            <span className="text-sm font-medium text-gray-800">{item.title}</span>
                            <span className={`text-xs px-1.5 py-0.5 rounded-full bg-${statusColor}-100 text-${statusColor}-800`}>
                              {item.status}
                            </span>
                          </div>
                          <div className="bg-gray-50 rounded h-6 overflow-hidden">
                            <div className={`bg-${statusColor}-500 h-full`} style={{width: `${item.percentage}%`}}></div>
                          </div>
                          <div className="flex justify-between mt-0.5">
                            <span className="text-xs text-gray-600">Field: {item.fieldValue}%</span>
                            <span className="text-xs text-gray-600">Lab: {item.labValue}%</span>
                          </div>
                          
                          {/* Product info */}
                          <div className="mt-2 pt-2 border-t border-gray-100 flex items-center">
                            <div className="w-6 h-6 bg-gray-200 rounded-full flex items-center justify-center mr-2 overflow-hidden">
                              {item.product.image ? (
                                <img 
                                  src={item.product.image} 
                                  alt={item.product.name} 
                                  className="w-full h-full object-cover"
                                />
                              ) : (
                                <Camera size={12} className="text-gray-400" />
                              )}
                            </div>
                            <div>
                              <span className="text-xs font-medium">{item.product.name}</span>
                              <span className="text-xs text-gray-500 ml-1">({item.product.manufacturer})</span>
                            </div>
                          </div>
                        </div>
                      );
                    })}
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
                    {benchmarks.map((benchmark, index) => (
                      <BenchmarkItem 
                        key={index}
                        benchmark={benchmark}
                        selectedProductId={selectedProduct}
                        products={products}
                      />
                    ))}
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
  benchmark: Benchmark;
  selectedProductId: string;
  products: Product[];
}

const BenchmarkItem: React.FC<BenchmarkItemProps> = ({ benchmark, selectedProductId, products }) => {
  const [expanded, setExpanded] = useState(false);
  
  // Find the selected product in the benchmark products
  const selectedProduct = selectedProductId !== 'all' 
    ? products.find(p => p.id === selectedProductId) 
    : null;
    
  const selectedProductPerformance = selectedProduct 
    ? benchmark.products.find(p => p.name === selectedProduct.name) 
    : null;
  
  // Sort products by score (highest first)
  const sortedProducts = [...benchmark.products].sort((a, b) => b.score - a.score);
  
  return (
    <div className="border-b border-gray-100 pb-2">
      <div className="flex justify-between items-center">
        <p className="text-xs font-medium text-gray-800">{benchmark.category}</p>
        <div className="flex items-center space-x-2">
          {selectedProductPerformance ? (
            <>
              <div className="flex items-center">
                <div className="w-2 h-2 rounded-full bg-blue-600 mr-1"></div>
                <span className="text-xs">{selectedProductPerformance.score}</span>
              </div>
              <div className="flex items-center">
                <div className="w-2 h-2 rounded-full bg-gray-400 mr-1"></div>
                <span className="text-xs text-gray-600">{benchmark.industryAvg}</span>
              </div>
            </>
          ) : (
            <>
              <div className="flex items-center">
                <div className="w-2 h-2 rounded-full bg-blue-600 mr-1"></div>
                <span className="text-xs">{benchmark.yourScore}</span>
              </div>
              <div className="flex items-center">
                <div className="w-2 h-2 rounded-full bg-gray-400 mr-1"></div>
                <span className="text-xs text-gray-600">{benchmark.industryAvg}</span>
              </div>
            </>
          )}
        </div>
      </div>
      
      <div className="mt-1 bg-gray-200 h-2 rounded-full overflow-hidden">
        <div 
          className="bg-blue-600 h-full rounded-full" 
          style={{ width: `${selectedProductPerformance ? selectedProductPerformance.score : benchmark.yourScore}%` }}
        ></div>
      </div>
      
      <div className="flex justify-between text-xs text-gray-500 mt-0.5">
        <span>{selectedProductPerformance ? selectedProduct?.name : 'Your Score'}</span>
        <span>Industry Average</span>
      </div>
      
      {/* Product comparison button */}
      <button 
        className="mt-1 text-xs text-blue-600 flex items-center"
        onClick={() => setExpanded(!expanded)}
      >
        <ChevronDown size={12} className={`mr-1 transform ${expanded ? 'rotate-180' : ''}`} />
        {expanded ? 'Hide Product Comparison' : 'Show Product Comparison'}
      </button>
      
      {/* Expanded product comparison */}
      {expanded && (
        <div className="mt-2 space-y-1.5 bg-gray-50 p-2 rounded-md">
          {sortedProducts.map((product, idx) => (
            <div key={idx} className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="w-1.5 h-1.5 rounded-full bg-gray-400 mr-1.5"></div>
                <span className="text-xs">{product.name}</span>
              </div>
              <div className="flex items-center">
                <div className="w-16 bg-gray-200 h-1.5 rounded-full overflow-hidden mr-2">
                  <div 
                    className={`h-full rounded-full ${
                      product.score > benchmark.industryAvg ? 'bg-green-500' : 'bg-yellow-500'
                    }`} 
                    style={{ width: `${product.score}%` }}
                  ></div>
                </div>
                <span className="text-xs font-medium">{product.score}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PerformanceOptimization; 