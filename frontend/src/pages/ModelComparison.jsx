import React from 'react';
import { 
  GitCompare, 
  BarChart2, 
  HelpCircle, 
  CheckCircle2, 
  Layers
} from 'lucide-react';
import { MODEL_COMPARISON_DATA } from '../data/mockData';

export default function ModelComparison() {
  return (
    <div className="model-comparison-page">
      {/* Intro Banner */}
      <div className="card" style={{ borderLeft: '4px solid #1e3a8a' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '14px' }}>
          <GitCompare size={24} color="#1e3a8a" style={{ flexShrink: 0, marginTop: '2px' }} />
          <div>
            <h2 style={{ fontSize: '16px', fontWeight: 700, color: '#1e3a8a', marginBottom: '4px' }}>
              Machine Learning Model Benchmark
            </h2>
            <p style={{ fontSize: '13px', color: '#64748b' }}>
              We benchmarked 6 established classification algorithms on the exact same 25,804 held-out network test flows under standardized evaluation conditions.
            </p>
          </div>
        </div>
      </div>

      {/* Visual Bar Comparison Chart */}
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Accuracy & F1-Score Comparison Across Algorithms</h2>
            <p className="card-subtitle">Comparing classification performance across different model architectures</p>
          </div>
          <BarChart2 size={18} color="#1e3a8a" />
        </div>

        <div className="chart-container">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {MODEL_COMPARISON_DATA.map((item) => (
              <div key={item.model}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '4px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontWeight: 700, color: '#0f172a' }}>{item.model}</span>
                    <span className="badge badge-info">{item.family}</span>
                  </div>
                  <span style={{ fontWeight: 700, color: item.accuracy > 99 ? '#16a34a' : '#1e3a8a' }}>
                    {item.accuracy}% Accuracy | {item.weightedF1}% F1
                  </span>
                </div>

                <div style={{ height: '12px', backgroundColor: '#f1f5f9', borderRadius: '6px', overflow: 'hidden' }}>
                  <div 
                    style={{ 
                      width: `${item.accuracy}%`, 
                      height: '100%', 
                      backgroundColor: item.accuracy > 99 ? '#16a34a' : item.accuracy > 90 ? '#1e3a8a' : '#d97706',
                      borderRadius: '6px'
                    }} 
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="chart-explanation">
            <strong>Short Explanation:</strong> Tree-based algorithms (Random Forest at 99.77% and Decision Tree at 99.33%) significantly outperform linear and probabilistic models. Network traffic boundaries are non-linear step functions (e.g. port numbers and packet rate limits) which decision trees partition naturally.
          </div>
        </div>
      </div>

      {/* Complete Benchmark Table */}
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Comprehensive Algorithm Evaluation Matrix</h2>
            <p className="card-subtitle">Verified scores measured on 25,804 held-out flows</p>
          </div>
        </div>

        <div className="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Algorithm Name</th>
                <th>Model Family</th>
                <th>Accuracy</th>
                <th>Precision</th>
                <th>Recall</th>
                <th>Weighted F1</th>
                <th>Macro F1</th>
                <th>ROC-AUC</th>
                <th>Train Time</th>
              </tr>
            </thead>
            <tbody>
              {MODEL_COMPARISON_DATA.map((m) => (
                <tr key={m.model} style={{ backgroundColor: m.model.includes('Random Forest') ? '#f0fdf4' : 'inherit' }}>
                  <td style={{ fontWeight: 700, color: m.model.includes('Random Forest') ? '#166534' : '#0f172a' }}>
                    {m.model}
                    {m.model.includes('Random Forest') && (
                      <span className="badge badge-safe" style={{ marginLeft: '8px' }}>Top Model</span>
                    )}
                  </td>
                  <td><span className="badge badge-info">{m.family}</span></td>
                  <td style={{ fontWeight: 600 }}>{m.accuracy}%</td>
                  <td>{m.precision}%</td>
                  <td>{m.recall}%</td>
                  <td style={{ fontWeight: 700, color: '#1e3a8a' }}>{m.weightedF1}%</td>
                  <td>{m.macroF1}%</td>
                  <td style={{ fontWeight: 600 }}>{m.rocAuc}%</td>
                  <td style={{ color: '#64748b' }}>{m.trainTime}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Model Architecture Insights Card */}
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Performance Insights & Architecture Comparison</h2>
            <p className="card-subtitle">Why Random Forest achieved superior detection capability</p>
          </div>
          <HelpCircle size={18} color="#1e3a8a" />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px', fontSize: '13px' }}>
          <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#1e3a8a', marginBottom: '6px' }}>
              1. Non-Linear Decision Boundaries
            </h3>
            <p style={{ color: '#64748b', lineHeight: 1.5 }}>
              Logistic Regression and Linear SVM achieve ~92-93% because network rules operate on discrete numerical thresholds (e.g. port 80 vs port 443). Decision Trees easily create orthogonal splits on these thresholds.
            </p>
          </div>

          <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#1e3a8a', marginBottom: '6px' }}>
              2. Feature Correlation Handling
            </h3>
            <p style={{ color: '#64748b', lineHeight: 1.5 }}>
              Gaussian Naive Bayes scored 64.46% because it assumes features are mutually independent. Network packet statistics (like Packet Length Mean, Std, and Max) are heavily correlated, which impairs Naive Bayes probability estimates.
            </p>
          </div>

          <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#1e3a8a', marginBottom: '6px' }}>
              3. The Power of Ensemble Bagging
            </h3>
            <p style={{ color: '#64748b', lineHeight: 1.5 }}>
              While an individual Decision Tree scored 99.33%, it can be prone to variance on noise. Random Forest combines 100 decorrelated trees with bootstrap sampling, reducing variance and raising the F1-score to 99.77%.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
