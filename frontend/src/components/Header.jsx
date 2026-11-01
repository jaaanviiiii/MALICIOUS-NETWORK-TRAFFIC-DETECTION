import React from 'react';
import { Activity } from 'lucide-react';

export default function Header({ title, subtitle, isBackendConnected }) {
  return (
    <header className="top-navbar">
      <div>
        <h1 className="top-navbar-title">{title}</h1>
        {subtitle && <p className="card-subtitle">{subtitle}</p>}
      </div>

      <div className="top-navbar-status">
        <span className="model-badge">
          Active Model: Random Forest Ensemble
        </span>
        <div style={{ display: 'flex', alignItem: 'center', gap: '6px' }}>
          <Activity size={16} color={isBackendConnected ? '#16a34a' : '#d97706'} />
          <span style={{ fontSize: '13px', fontWeight: 500, color: isBackendConnected ? '#16a34a' : '#d97706' }}>
            {isBackendConnected ? 'Backend Connected' : 'Local Engine Ready'}
          </span>
        </div>
      </div>
    </header>
  );
}
