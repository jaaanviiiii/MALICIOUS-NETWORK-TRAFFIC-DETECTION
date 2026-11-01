import React from 'react';
import { 
  History, 
  Download, 
  Trash2, 
  FileCheck, 
  ArrowRight,
  ShieldAlert
} from 'lucide-react';

export default function DetectionHistory({ history, onClearHistory, setActiveTab }) {
  const downloadReport = (item) => {
    const content = `Traffic Detection Report\nSession ID: ${item.id}\nSource: ${item.source}\nDate: ${item.date}\nTotal Flows: ${item.total}\nNormal Flows: ${item.benign}\nMalicious Flows: ${item.malicious}\nTop Threat: ${item.topAttack}\nStatus: Verified\n`;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `report_${item.id}.txt`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="detection-history-page">
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Detection History Log</h2>
            <p className="card-subtitle">Chronological record of all packet capture analyses performed during this session</p>
          </div>
          {history && history.length > 0 && (
            <button 
              className="btn btn-secondary btn-sm"
              onClick={onClearHistory}
            >
              <Trash2 size={14} color="#dc2626" />
              <span>Clear History</span>
            </button>
          )}
        </div>

        {history && history.length > 0 ? (
          <div className="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Session ID</th>
                  <th>Traffic Source / File</th>
                  <th>Analysis Timestamp</th>
                  <th>Total Packets</th>
                  <th>Normal (Safe)</th>
                  <th>Threats Flagged</th>
                  <th>Top Threat Category</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item) => {
                  const maliciousPercent = ((item.malicious / item.total) * 100).toFixed(1);
                  return (
                    <tr key={item.id}>
                      <td style={{ fontFamily: 'monospace', fontSize: '12px', color: '#64748b' }}>
                        {item.id}
                      </td>
                      <td style={{ fontWeight: 600 }}>{item.source}</td>
                      <td style={{ color: '#64748b' }}>{item.date}</td>
                      <td>{item.total.toLocaleString()}</td>
                      <td style={{ color: '#16a34a', fontWeight: 600 }}>{item.benign.toLocaleString()}</td>
                      <td style={{ color: '#dc2626', fontWeight: 600 }}>
                        {item.malicious.toLocaleString()} ({maliciousPercent}%)
                      </td>
                      <td>
                        <span className={item.malicious > 0 ? "badge badge-warning" : "badge badge-safe"}>
                          {item.topAttack || 'Normal'}
                        </span>
                      </td>
                      <td>
                        <button 
                          className="btn btn-secondary btn-sm"
                          onClick={() => downloadReport(item)}
                          title="Download summary report"
                        >
                          <Download size={13} />
                          <span>Report</span>
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          /* Helpful Empty State */
          <div className="empty-state">
            <History className="empty-state-icon" />
            <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#1e3a8a', marginBottom: '4px' }}>
              No Detection Sessions Recorded Yet
            </h3>
            <p style={{ fontSize: '13px', color: '#64748b', maxWidth: '400px', margin: '0 auto 16px' }}>
              Upload and analyze a traffic CSV file in Traffic Detection to automatically log your results here.
            </p>
            <button 
              className="btn btn-primary"
              onClick={() => setActiveTab('traffic-detection')}
            >
              <span>Go to Traffic Detection</span>
              <ArrowRight size={15} />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
