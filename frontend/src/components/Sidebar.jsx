import React from 'react';
import { 
  LayoutDashboard, 
  ShieldAlert, 
  PieChart, 
  Gauge, 
  GitCompare, 
  History, 
  Info,
  ShieldCheck
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'traffic-detection', label: 'Traffic Detection', icon: ShieldAlert },
    { id: 'attack-analytics', label: 'Attack Analytics', icon: PieChart },
    { id: 'model-performance', label: 'Model Performance', icon: Gauge },
    { id: 'model-comparison', label: 'Model Comparison', icon: GitCompare },
    { id: 'detection-history', label: 'Detection History', icon: History },
    { id: 'about-project', label: 'About Project', icon: Info },
  ];

  return (
    <aside className="sidebar">
      {/* Brand Header */}
      <div className="sidebar-header">
        <div className="sidebar-logo-icon">
          <ShieldCheck size={22} />
        </div>
        <div>
          <div className="sidebar-title">NetworkGuard</div>
          <div className="sidebar-subtitle">ML Intrusion Detection</div>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <div
              key={item.id}
              className={`nav-item ${isActive ? 'active' : ''}`}
              onClick={() => setActiveTab(item.id)}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </div>
          );
        })}
      </nav>

      {/* Footer Info */}
      <div className="sidebar-footer">
        <div className="sidebar-footer-badge">
          <span className="sidebar-footer-dot"></span>
          <span>ML Engine Ready</span>
        </div>
        <div>CIC-IDS2017 Benchmark</div>
        <div>Intrusion Detection System</div>
      </div>
    </aside>
  );
}
