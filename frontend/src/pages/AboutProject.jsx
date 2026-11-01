import React from 'react';
import { 
  ShieldCheck, 
  Target, 
  CheckCircle, 
  Database, 
  Cpu, 
  Workflow, 
  AlertCircle, 
  Code2,
  Terminal,
  Layers,
  Server
} from 'lucide-react';

export default function AboutProject() {
  return (
    <div className="about-project-page">
      {/* 1. Project Overview */}
      <div className="card">
        <div className="card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ padding: '10px', backgroundColor: '#e0f2fe', borderRadius: '8px', color: '#1e3a8a' }}>
              <ShieldCheck size={24} />
            </div>
            <div>
              <h2 className="card-title">NetworkGuard: Project Overview</h2>
              <p className="card-subtitle">Intelligent Network Intrusion Detection System (NIDS)</p>
            </div>
          </div>
          <span className="badge badge-safe">Production Ready</span>
        </div>

        <div style={{ fontSize: '14px', color: '#334155', lineHeight: 1.6 }}>
          <p style={{ marginBottom: '12px' }}>
            <strong>NetworkGuard</strong> is a machine-learning-driven network security platform designed to detect, classify, and mitigate cyber attacks in computer networks. By examining packet-level statistical flow telemetry (such as packet lengths, flow durations, inter-arrival times, and TCP flag sequences), the system detects anomalies and identifies attack families without relying on rigid static rules.
          </p>
          <p>
            The system achieves high detection accuracy (99.77% F1-score) and operates with an ultra-low false alarm rate (under 0.2%), making it suitable for practical monitoring environments where preventing accidental denial of service to legitimate users is critical.
          </p>
        </div>
      </div>

      {/* Grid: 2. Problem Statement & 3. Project Objectives */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '24px', marginBottom: '24px' }}>
        
        {/* 2. Problem Statement */}
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Problem Statement</h2>
              <p className="card-subtitle">The challenge of modern intrusion detection</p>
            </div>
            <Target size={18} color="#dc2626" />
          </div>

          <div style={{ fontSize: '14px', color: '#475569', lineHeight: 1.6 }}>
            <p style={{ marginBottom: '10px' }}>
              Traditional signature-based intrusion detection systems (IDS) match incoming network packets against fixed patterns of known attacks. This approach faces critical limitations:
            </p>
            <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <li><strong>Zero-Day Vulnerability:</strong> Signature databases cannot detect unknown attack vectors or polymorphic variants.</li>
              <li><strong>Encryption Blindspot:</strong> Over 85% of modern internet traffic is encrypted (HTTPS/TLS 1.3), rendering payload-inspection firewalls ineffective without intrusive decryption.</li>
              <li><strong>Volume & Velocity:</strong> Modern gigabit backbones generate millions of connection flows per minute, overwhelming manual inspection.</li>
            </ul>
          </div>
        </div>

        {/* 3. Project Objectives */}
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Project Objectives</h2>
              <p className="card-subtitle">Key engineering and detection goals</p>
            </div>
            <CheckCircle size={18} color="#16a34a" />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '13px' }}>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
              <span className="badge badge-safe" style={{ marginTop: '2px' }}>Goal 1</span>
              <div><strong>High Precision Detection:</strong> Attain greater than 99% accuracy on high-volume network intrusions (DDoS, DoS, PortScan, Patator Brute Force).</div>
            </div>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
              <span className="badge badge-safe" style={{ marginTop: '2px' }}>Goal 2</span>
              <div><strong>Minimize False Alarms:</strong> Maintain a false positive rate below 0.3% to safeguard legitimate customer workflows.</div>
            </div>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
              <span className="badge badge-safe" style={{ marginTop: '2px' }}>Goal 3</span>
              <div><strong>Multi-Class Attack Taxonomy:</strong> Categorize flagged threats into distinct operational families (DDoS, PortScan, DoS, Brute Force, Web Attacks, Botnet).</div>
            </div>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
              <span className="badge badge-safe" style={{ marginTop: '2px' }}>Goal 4</span>
              <div><strong>Accessible Operator Interface:</strong> Provide an intuitive, responsive web application for security analysts to inspect traffic and export CSV audit logs.</div>
            </div>
          </div>
        </div>

      </div>

      {/* Grid: 4. Dataset Information & 5. Machine Learning Approach */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '24px', marginBottom: '24px' }}>
        
        {/* 4. Dataset Information */}
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Dataset Information (CIC-IDS2017)</h2>
              <p className="card-subtitle">Canadian Institute for Cybersecurity Benchmark</p>
            </div>
            <Database size={18} color="#1e3a8a" />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '13px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', backgroundColor: '#f8fafc', borderRadius: '6px' }}>
              <span style={{ fontWeight: 600 }}>Raw Capture Size</span>
              <span>8 CSV captures (2.83 Million records, ~880 MB)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', backgroundColor: '#f8fafc', borderRadius: '6px' }}>
              <span style={{ fontWeight: 600 }}>Active Balanced Sample</span>
              <span>129,016 flow records (55% Benign, 45% Malicious)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', backgroundColor: '#f8fafc', borderRadius: '6px' }}>
              <span style={{ fontWeight: 600 }}>Numerical Telemetry Features</span>
              <span>69 selected features (packet sizes, rates, TCP flags)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', backgroundColor: '#f8fafc', borderRadius: '6px' }}>
              <span style={{ fontWeight: 600 }}>Threat Coverage</span>
              <span>15 granular attacks synthesized across 5 capture days</span>
            </div>
          </div>
        </div>

        {/* 5. Machine Learning Approach */}
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Machine Learning Approach</h2>
              <p className="card-subtitle">Methodology and algorithmic architecture</p>
            </div>
            <Cpu size={18} color="#0284c7" />
          </div>

          <div style={{ fontSize: '13px', color: '#475569', lineHeight: 1.6 }}>
            <p style={{ marginBottom: '8px' }}>
              Our methodology emphasizes <strong>interpretable, high-performance classical machine learning</strong> rather than resource-heavy black-box architectures:
            </p>
            <ul style={{ paddingLeft: '18px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <li><strong>Feature Normalization:</strong> Numerical scaling via `StandardScaler` fitted strictly on training data to prevent leakage.</li>
              <li><strong>Benchmarked Classifiers:</strong> Random Forest, Decision Tree, Support Vector Machine (LinearSVC), K-Nearest Neighbors, Logistic Regression, and Gaussian Naive Bayes.</li>
              <li><strong>Production Model:</strong> 100-tree Random Forest ensemble utilizing Gini impurity splits and bootstrap aggregation.</li>
              <li><strong>Dual-Stage Inference:</strong> Stage 1 performs binary filtering (Safe vs Threat); Stage 2 classifies attack family.</li>
            </ul>
          </div>
        </div>

      </div>

      {/* 6. Technologies Used */}
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Technologies Used</h2>
            <p className="card-subtitle">Full technology stack across models, backend, and frontend</p>
          </div>
          <Code2 size={18} color="#1e3a8a" />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '16px', fontSize: '13px' }}>
          <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
              <Terminal size={18} color="#1e3a8a" />
              <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#1e3a8a' }}>Data Science & ML</h3>
            </div>
            <ul style={{ color: '#475569', paddingLeft: '16px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <li><strong>Python 3.11:</strong> Core execution environment</li>
              <li><strong>Scikit-learn:</strong> Model training & evaluation</li>
              <li><strong>Pandas & NumPy:</strong> Fast vector data processing</li>
              <li><strong>Joblib:</strong> Model serialization & loading</li>
            </ul>
          </div>

          <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
              <Server size={18} color="#0284c7" />
              <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#0284c7' }}>Backend Server</h3>
            </div>
            <ul style={{ color: '#475569', paddingLeft: '16px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <li><strong>FastAPI:</strong> High-performance async REST API</li>
              <li><strong>Uvicorn:</strong> ASGI web server</li>
              <li><strong>Pydantic:</strong> Strict data schema validation</li>
              <li><strong>CORS Middleware:</strong> Secure frontend connectivity</li>
            </ul>
          </div>

          <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
              <Layers size={18} color="#16a34a" />
              <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#16a34a' }}>Frontend Web App</h3>
            </div>
            <ul style={{ color: '#475569', paddingLeft: '16px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <li><strong>React 19:</strong> Reactive UI component architecture</li>
              <li><strong>Vite:</strong> Ultra-fast build tool & dev server</li>
              <li><strong>Lucide React:</strong> Streamlined UI iconography</li>
              <li><strong>Custom Light CSS:</strong> Clean, responsive design system</li>
            </ul>
          </div>
        </div>
      </div>

      {/* 7. System Workflow */}
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">System Workflow</h2>
            <p className="card-subtitle">End-to-end data lifecycle from network capture to threat alerting</p>
          </div>
          <Workflow size={18} color="#1e3a8a" />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '14px' }}>
          <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <div style={{ fontSize: '12px', fontWeight: 700, color: '#0284c7', marginBottom: '4px' }}>STEP 01</div>
            <h4 style={{ fontSize: '14px', fontWeight: 700, color: '#1e3a8a', marginBottom: '6px' }}>Flow Extraction</h4>
            <p style={{ fontSize: '12px', color: '#64748b', lineHeight: 1.5 }}>
              Raw network packet captures (.pcap) are aggregated into directional TCP/UDP conversation flows.
            </p>
          </div>

          <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <div style={{ fontSize: '12px', fontWeight: 700, color: '#0284c7', marginBottom: '4px' }}>STEP 02</div>
            <h4 style={{ fontSize: '14px', fontWeight: 700, color: '#1e3a8a', marginBottom: '6px' }}>Preprocessing</h4>
            <p style={{ fontSize: '12px', color: '#64748b', lineHeight: 1.5 }}>
              Flows are validated, infinite rates suppressed, and features aligned with the 69-parameter schema.
            </p>
          </div>

          <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <div style={{ fontSize: '12px', fontWeight: 700, color: '#0284c7', marginBottom: '4px' }}>STEP 03</div>
            <h4 style={{ fontSize: '14px', fontWeight: 700, color: '#1e3a8a', marginBottom: '6px' }}>Model Classification</h4>
            <p style={{ fontSize: '12px', color: '#64748b', lineHeight: 1.5 }}>
              The Random Forest ensemble evaluates feature vectors and generates malicious probability scores.
            </p>
          </div>

          <div style={{ padding: '16px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <div style={{ fontSize: '12px', fontWeight: 700, color: '#0284c7', marginBottom: '4px' }}>STEP 04</div>
            <h4 style={{ fontSize: '14px', fontWeight: 700, color: '#1e3a8a', marginBottom: '6px' }}>Alerting & Export</h4>
            <p style={{ fontSize: '12px', color: '#64748b', lineHeight: 1.5 }}>
              Threats are classified as Safe, Suspicious, or Critical and logged with instant CSV export capabilities.
            </p>
          </div>
        </div>
      </div>

      {/* 8. Project Limitations */}
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Project Limitations & Future Scope</h2>
            <p className="card-subtitle">Operational boundaries and areas for ongoing improvement</p>
          </div>
          <AlertCircle size={18} color="#d97706" />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px', fontSize: '13px' }}>
          <div style={{ padding: '14px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <h4 style={{ fontSize: '14px', fontWeight: 700, color: '#1e3a8a', marginBottom: '4px' }}>
              Payload Inspection Limits
            </h4>
            <p style={{ color: '#64748b', lineHeight: 1.5 }}>
              The system inspects statistical flow headers rather than raw payload bodies. Subtle application-layer injections (such as SQLi or XSS with normal packet counts) are best paired with Web Application Firewalls (WAF).
            </p>
          </div>

          <div style={{ padding: '14px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <h4 style={{ fontSize: '14px', fontWeight: 700, color: '#1e3a8a', marginBottom: '4px' }}>
              Network Concept Drift
            </h4>
            <p style={{ color: '#64748b', lineHeight: 1.5 }}>
              As new networking protocols and applications emerge, traffic baseline distributions evolve. Operational deployments require scheduled retraining on fresh network captures.
            </p>
          </div>

          <div style={{ padding: '14px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <h4 style={{ fontSize: '14px', fontWeight: 700, color: '#1e3a8a', marginBottom: '4px' }}>
              Adversarial Perturbation
            </h4>
            <p style={{ color: '#64748b', lineHeight: 1.5 }}>
              Sophisticated attackers can intentionally inject artificial jitter or pad packet sizes to mimic benign patterns. Combining multi-dimensional flow metrics provides defensive resilience against evasion.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
