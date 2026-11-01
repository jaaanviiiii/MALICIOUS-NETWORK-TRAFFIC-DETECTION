import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import TrafficDetection from './pages/TrafficDetection';
import AttackAnalytics from './pages/AttackAnalytics';
import ModelPerformance from './pages/ModelPerformance';
import ModelComparison from './pages/ModelComparison';
import DetectionHistory from './pages/DetectionHistory';
import AboutProject from './pages/AboutProject';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isBackendConnected, setIsBackendConnected] = useState(false);
  const [history, setHistory] = useState([
    {
      id: 'session-101',
      source: 'CIC-IDS2017 Validation Set',
      date: 'Today, 20:45',
      total: 25804,
      benign: 14200,
      malicious: 11604,
      topAttack: 'DoS / DDoS',
      status: 'Verified'
    },
    {
      id: 'session-102',
      source: 'PortScan & Recon Probe',
      date: 'Today, 19:30',
      total: 500,
      benign: 260,
      malicious: 240,
      topAttack: 'PortScan',
      status: 'Verified'
    }
  ]);

  // Check backend health status on mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const res = await fetch('/api/health');
        if (res.ok) {
          setIsBackendConnected(true);
        } else {
          // Direct fallback check
          const directRes = await fetch('http://127.0.0.1:8000/health');
          if (directRes.ok) setIsBackendConnected(true);
        }
      } catch (err) {
        // Backend not currently running - fallback mode active
        setIsBackendConnected(false);
      }
    };
    checkBackend();
  }, []);

  const handleAnalysisComplete = (newRecord) => {
    setHistory(prev => [newRecord, ...prev]);
  };

  const handleClearHistory = () => {
    setHistory([]);
  };

  // Header Titles
  const getHeaderInfo = () => {
    switch (activeTab) {
      case 'dashboard':
        return {
          title: 'System Dashboard',
          subtitle: 'Real-time overview of network traffic, threat distribution, and model metrics'
        };
      case 'traffic-detection':
        return {
          title: 'Traffic Detection',
          subtitle: 'Upload network flow CSVs or inspect individual packets to identify cyber attacks'
        };
      case 'attack-analytics':
        return {
          title: 'Attack Analytics',
          subtitle: 'Visual breakdown and statistical distribution across 8 attack categories'
        };
      case 'model-performance':
        return {
          title: 'Model Performance',
          subtitle: 'Detailed metrics, confusion matrix, and feature importances for Random Forest'
        };
      case 'model-comparison':
        return {
          title: 'Model Comparison',
          subtitle: 'Benchmarking performance across 6 classical machine learning algorithms'
        };
      case 'detection-history':
        return {
          title: 'Detection History',
          subtitle: 'Log of previous traffic inspection runs and downloadable analysis reports'
        };
      case 'about-project':
        return {
          title: 'About Project',
          subtitle: 'Project overview, problem statement, architecture, dataset specifications, and workflow'
        };
      default:
        return { title: 'Network Guard', subtitle: 'Intrusion Detection System' };
    }
  };

  const { title, subtitle } = getHeaderInfo();

  return (
    <div className="app-container">
      {/* Navigation Sidebar */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <div className="main-wrapper">
        <Header 
          title={title} 
          subtitle={subtitle} 
          isBackendConnected={isBackendConnected} 
        />

        <main className="content-body">
          {activeTab === 'dashboard' && (
            <Dashboard setActiveTab={setActiveTab} history={history} />
          )}
          {activeTab === 'traffic-detection' && (
            <TrafficDetection onAnalysisComplete={handleAnalysisComplete} />
          )}
          {activeTab === 'attack-analytics' && (
            <AttackAnalytics />
          )}
          {activeTab === 'model-performance' && (
            <ModelPerformance />
          )}
          {activeTab === 'model-comparison' && (
            <ModelComparison />
          )}
          {activeTab === 'detection-history' && (
            <DetectionHistory 
              history={history} 
              onClearHistory={handleClearHistory} 
              setActiveTab={setActiveTab} 
            />
          )}
          {activeTab === 'about-project' && (
            <AboutProject />
          )}
        </main>
      </div>
    </div>
  );
}
