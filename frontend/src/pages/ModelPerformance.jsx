import React from 'react';
import { 
  Award, 
  CheckCircle, 
  Layers, 
  Clock, 
  TrendingUp, 
  Sliders
} from 'lucide-react';
import { TOP_FEATURES } from '../data/mockData';

export default function ModelPerformance() {
  return (
    <div className="model-performance-page">
      {/* Best Model Banner */}
      <div className="card" style={{ backgroundColor: '#ffffff', border: '1px solid #bfdbfe' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ padding: '14px', backgroundColor: '#e0f2fe', borderRadius: '12px', color: '#1e3a8a' }}>
              <Award size={32} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <h2 style={{ fontSize: '20px', fontWeight: 700, color: 'var(--primary-navy)' }}>
                  Primary Model: Random Forest Classifier
                </h2>
                <span className="badge badge-safe">Ensemble Learning</span>
              </div>
              <p style={{ fontSize: '13px', color: '#64748b', marginTop: '2px' }}>
                Bagging ensemble consisting of 100 decorrelated decision trees, trained on 103,212 network flows.
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '12px' }}>
            <div style={{ textAlign: 'center', padding: '8px 16px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
              <div style={{ fontSize: '12px', color: '#64748b' }}>Training Time</div>
              <div style={{ fontSize: '16px', fontWeight: 700, color: '#1e3a8a' }}>5.22 seconds</div>
            </div>
            <div style={{ textAlign: 'center', padding: '8px 16px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
              <div style={{ fontSize: '12px', color: '#64748b' }}>Inference Speed</div>
              <div style={{ fontSize: '16px', fontWeight: 700, color: '#16a34a' }}>0.07 ms / flow</div>
            </div>
          </div>
        </div>
      </div>

      {/* 5 Core Metric Cards */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-header">
            <span className="metric-label">Overall Accuracy</span>
            <CheckCircle size={18} color="#16a34a" />
          </div>
          <div className="metric-value">99.77%</div>
          <div className="metric-subtext">Correct classifications / Total flows</div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <span className="metric-label">Precision</span>
            <TrendingUp size={18} color="#0284c7" />
          </div>
          <div className="metric-value">99.77%</div>
          <div className="metric-subtext">Low false alarm / False positive rate</div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <span className="metric-label">Recall (Sensitivity)</span>
            <Layers size={18} color="#1e3a8a" />
          </div>
          <div className="metric-value">99.77%</div>
          <div className="metric-subtext">Catches 99.77% of all actual attacks</div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <span className="metric-label">Weighted F1-Score</span>
            <Award size={18} color="#ea580c" />
          </div>
          <div className="metric-value">99.77%</div>
          <div className="metric-subtext">Harmonic mean of precision & recall</div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <span className="metric-label">ROC-AUC Score</span>
            <Sliders size={18} color="#7c3aed" />
          </div>
          <div className="metric-value">99.99%</div>
          <div className="metric-subtext">Near-perfect separation threshold</div>
        </div>
      </div>

      {/* Grid: Confusion Matrix + Feature Importances */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(440px, 1fr))', gap: '24px' }}>
        
        {/* Confusion Matrix Card */}
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Confusion Matrix (25,804 Test Flows)</h2>
              <p className="card-subtitle">Detailed breakdown of true vs predicted results</p>
            </div>
            <span className="badge badge-info">Held-Out Test Set</span>
          </div>

          <div className="chart-container">
            {/* Visual Confusion Matrix Table */}
            <div style={{ maxWidth: '420px', margin: '0 auto', textAlign: 'center' }}>
              <div style={{ fontSize: '13px', fontWeight: 600, color: '#1e3a8a', marginBottom: '8px' }}>
                Predicted by Model
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '100px 1fr 1fr', gap: '8px', alignItems: 'center' }}>
                <div></div>
                <div style={{ fontWeight: 600, fontSize: '13px', color: '#16a34a' }}>Predicted Normal</div>
                <div style={{ fontWeight: 600, fontSize: '13px', color: '#dc2626' }}>Predicted Attack</div>

                <div style={{ fontWeight: 600, fontSize: '13px', textAlign: 'right', paddingRight: '8px', color: '#16a34a' }}>
                  Actual Normal
                </div>
                <div style={{ padding: '16px 8px', backgroundColor: '#dcfce7', border: '1px solid #bbf7d0', borderRadius: '8px' }}>
                  <div style={{ fontSize: '20px', fontWeight: 700, color: '#166534' }}>14,175</div>
                  <div style={{ fontSize: '11px', color: '#166534' }}>True Normal (99.8%)</div>
                </div>
                <div style={{ padding: '16px 8px', backgroundColor: '#fef2f2', border: '1px solid #fecaca', borderRadius: '8px' }}>
                  <div style={{ fontSize: '20px', fontWeight: 700, color: '#991b1b' }}>25</div>
                  <div style={{ fontSize: '11px', color: '#991b1b' }}>False Alarm (0.2%)</div>
                </div>

                <div style={{ fontWeight: 600, fontSize: '13px', textAlign: 'right', paddingRight: '8px', color: '#dc2626' }}>
                  Actual Attack
                </div>
                <div style={{ padding: '16px 8px', backgroundColor: '#fef2f2', border: '1px solid #fecaca', borderRadius: '8px' }}>
                  <div style={{ fontSize: '20px', fontWeight: 700, color: '#991b1b' }}>33</div>
                  <div style={{ fontSize: '11px', color: '#991b1b' }}>Missed Attack (0.3%)</div>
                </div>
                <div style={{ padding: '16px 8px', backgroundColor: '#dcfce7', border: '1px solid #bbf7d0', borderRadius: '8px' }}>
                  <div style={{ fontSize: '20px', fontWeight: 700, color: '#166534' }}>11,571</div>
                  <div style={{ fontSize: '11px', color: '#166534' }}>Detected Attack (99.7%)</div>
                </div>
              </div>
            </div>

            <div className="chart-explanation">
              <strong>Short Explanation:</strong> On 25,804 never-before-seen network flows, the model correctly identified 14,175 normal packets and 11,571 attacks. It produced only 25 false alarms (0.18%) and missed only 33 attacks (0.28%).
            </div>
          </div>
        </div>

        {/* Top 8 Discriminative Features */}
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Top Most Important Flow Features</h2>
              <p className="card-subtitle">Parameters that determine if traffic is malicious</p>
            </div>
            <span className="badge badge-info">Gini Importance</span>
          </div>

          <div className="chart-container">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              {TOP_FEATURES.map((feature, idx) => (
                <div key={feature.name}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '4px' }}>
                    <span style={{ fontWeight: 600 }}>{idx + 1}. {feature.name}</span>
                    <span style={{ color: '#0284c7', fontWeight: 600 }}>{(feature.importance * 100).toFixed(1)}%</span>
                  </div>
                  <div style={{ height: '8px', backgroundColor: '#f1f5f9', borderRadius: '4px', overflow: 'hidden' }}>
                    <div 
                      style={{ 
                        width: `${feature.importance * 100 * 6.5}%`, 
                        height: '100%', 
                        backgroundColor: '#1e3a8a',
                        borderRadius: '4px'
                      }} 
                    />
                  </div>
                  <div style={{ fontSize: '11px', color: '#64748b', marginTop: '2px' }}>
                    {feature.description}
                  </div>
                </div>
              ))}
            </div>

            <div className="chart-explanation">
              <strong>Short Explanation:</strong> Destination Port and Flow Duration are the two strongest signals for identifying cyber attacks. Cyber attacks frequently connect to port 80/443 with abnormal session lengths compared to legitimate human browsing.
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
