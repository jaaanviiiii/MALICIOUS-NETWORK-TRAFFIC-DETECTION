import React from 'react';
import { 
  Activity, 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle2, 
  ArrowRight,
  UploadCloud,
  Layers
} from 'lucide-react';
import { INITIAL_STATS, ATTACK_DISTRIBUTION } from '../data/mockData';

export default function Dashboard({ setActiveTab, history }) {
  // Compute recent stats based on user's recent runs or baseline
  const recentRuns = history && history.length > 0 ? history : [
    {
      id: 'default-1',
      source: 'CIC-IDS2017 Benchmark Test Set',
      date: 'Today, Just now',
      total: 25804,
      benign: 14200,
      malicious: 11604,
      topAttack: 'DoS / DDoS',
      accuracy: '99.77%'
    },
    {
      id: 'default-2',
      source: 'Web & PortScan Probe Sample',
      date: 'Sample verification',
      total: 500,
      benign: 260,
      malicious: 240,
      topAttack: 'PortScan',
      accuracy: '99.80%'
    }
  ];

  return (
    <div className="dashboard-page">
      {/* 4 Essential Metric Cards */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-header">
            <span className="metric-label">Total Traffic Analyzed</span>
            <div className="metric-icon-wrap metric-icon-navy">
              <Activity size={20} />
            </div>
          </div>
          <div className="metric-value">{INITIAL_STATS.totalAnalyzed.toLocaleString()}</div>
          <div className="metric-subtext">Network flow records from dataset</div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <span className="metric-label">Normal Traffic (Safe)</span>
            <div className="metric-icon-wrap metric-icon-green">
              <ShieldCheck size={20} />
            </div>
          </div>
          <div className="metric-value" style={{ color: '#16a34a' }}>
            {INITIAL_STATS.benignCount.toLocaleString()}
          </div>
          <div className="metric-subtext">55.03% of all observed packets</div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <span className="metric-label">Malicious Traffic (Threats)</span>
            <div className="metric-icon-wrap metric-icon-red">
              <AlertTriangle size={20} />
            </div>
          </div>
          <div className="metric-value" style={{ color: '#dc2626' }}>
            {INITIAL_STATS.maliciousCount.toLocaleString()}
          </div>
          <div className="metric-subtext">44.97% detected and flagged</div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <span className="metric-label">Detection Summary</span>
            <div className="metric-icon-wrap metric-icon-amber">
              <CheckCircle2 size={20} />
            </div>
          </div>
          <div className="metric-value" style={{ color: '#1e3a8a' }}>
            {INITIAL_STATS.detectionRate}%
          </div>
          <div className="metric-subtext">F1-Score (Random Forest model)</div>
        </div>
      </div>

      {/* Main Grid: Attack Distribution + Action Card */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '24px' }}>
        
        {/* Attack Distribution Card */}
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Attack Distribution</h2>
              <p className="card-subtitle">Breakdown of network traffic by category</p>
            </div>
            <span className="badge badge-info">8 Categories</span>
          </div>

          <div className="chart-container">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              {ATTACK_DISTRIBUTION.map((item) => (
                <div key={item.name}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '4px' }}>
                    <span style={{ fontWeight: 600, color: 'var(--text-main)' }}>{item.name}</span>
                    <span style={{ color: 'var(--text-muted)' }}>
                      {item.count.toLocaleString()} flows ({item.percentage}%)
                    </span>
                  </div>
                  {/* Progress Bar */}
                  <div style={{ height: '10px', backgroundColor: '#f1f5f9', borderRadius: '6px', overflow: 'hidden' }}>
                    <div 
                      style={{ 
                        width: `${item.percentage}%`, 
                        height: '100%', 
                        backgroundColor: item.color,
                        borderRadius: '6px',
                        transition: 'width 0.4s ease'
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>

            <div className="chart-explanation">
              <strong>Short Explanation:</strong> This chart shows all traffic analyzed by the system. Normal traffic comprises 55% of all connections. Among attacks, Denial of Service (DoS) and Brute Force password attacks make up the largest share of malicious traffic.
            </div>
          </div>
        </div>

        {/* Quick Action & System Status */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          {/* Quick Upload Action */}
          <div className="card" style={{ backgroundColor: '#ffffff', border: '1px solid #bfdbfe' }}>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
              <div style={{ padding: '12px', backgroundColor: '#e0f2fe', borderRadius: '10px', color: '#0284c7' }}>
                <UploadCloud size={28} />
              </div>
              <div style={{ flex: 1 }}>
                <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#1e3a8a', marginBottom: '4px' }}>
                  Analyze New Traffic File
                </h3>
                <p style={{ fontSize: '13px', color: '#64748b', marginBottom: '14px' }}>
                  Upload a CSV file containing network packet flows to detect cyber attacks in seconds.
                </p>
                <button 
                  className="btn btn-primary"
                  onClick={() => setActiveTab('traffic-detection')}
                >
                  <span>Go to Traffic Detection</span>
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          </div>

          {/* Machine Learning Pipeline Summary */}
          <div className="card">
            <div className="card-header">
              <div>
                <h2 className="card-title">Detection Pipeline Workflow</h2>
                <p className="card-subtitle">End-to-end intrusion detection stages</p>
              </div>
              <Layers size={18} color="#1e3a8a" />
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '13px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', backgroundColor: '#f8fafc', borderRadius: '6px' }}>
                <span style={{ fontWeight: 600 }}>Data Cleaning & Standardization</span>
                <span style={{ color: '#16a34a', fontWeight: 600 }}>Active</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', backgroundColor: '#f8fafc', borderRadius: '6px' }}>
                <span style={{ fontWeight: 600 }}>Multi-Model Benchmarking</span>
                <span style={{ color: '#16a34a', fontWeight: 600 }}>6 Models Evaluated</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', backgroundColor: '#f8fafc', borderRadius: '6px' }}>
                <span style={{ fontWeight: 600 }}>Production Model (Random Forest)</span>
                <span style={{ color: '#16a34a', fontWeight: 600 }}>99.77% Accuracy</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', backgroundColor: '#f8fafc', borderRadius: '6px' }}>
                <span style={{ fontWeight: 600 }}>Real-Time Inference Engine</span>
                <span style={{ color: '#16a34a', fontWeight: 600 }}>Operational</span>
              </div>
            </div>
          </div>

        </div>

      </div>

      {/* Recent Analysis Summary */}
      <div className="card" style={{ marginTop: '24px' }}>
        <div className="card-header">
          <div>
            <h2 className="card-title">Recent Traffic Analyses</h2>
            <p className="card-subtitle">Recent detection sessions and evaluation runs</p>
          </div>
          <button 
            className="btn btn-secondary btn-sm"
            onClick={() => setActiveTab('detection-history')}
          >
            <span>View Full History</span>
            <ArrowRight size={14} />
          </button>
        </div>

        <div className="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Source / Dataset</th>
                <th>Date / Time</th>
                <th>Total Flows</th>
                <th>Normal</th>
                <th>Malicious</th>
                <th>Top Threat Detected</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {recentRuns.slice(0, 4).map((item) => (
                <tr key={item.id}>
                  <td style={{ fontWeight: 600 }}>{item.source}</td>
                  <td style={{ color: '#64748b' }}>{item.date}</td>
                  <td>{item.total.toLocaleString()}</td>
                  <td style={{ color: '#16a34a', fontWeight: 600 }}>{item.benign.toLocaleString()}</td>
                  <td style={{ color: '#dc2626', fontWeight: 600 }}>{item.malicious.toLocaleString()}</td>
                  <td>
                    <span className="badge badge-warning">{item.topAttack || 'Mixed Threats'}</span>
                  </td>
                  <td>
                    <span className="badge badge-safe">Verified</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
