import React from 'react';
import { 
  BarChart3, 
  PieChart as PieIcon, 
  ShieldCheck, 
  AlertTriangle,
  Info
} from 'lucide-react';
import { ATTACK_DISTRIBUTION } from '../data/mockData';

export default function AttackAnalytics() {
  const attacksOnly = ATTACK_DISTRIBUTION.filter(a => a.name !== "BENIGN (Normal)");
  const totalAttackCount = attacksOnly.reduce((acc, curr) => acc + curr.count, 0);

  return (
    <div className="attack-analytics-page">
      {/* Intro Box */}
      <div className="alert-box alert-box-info" style={{ marginBottom: '24px' }}>
        <Info size={20} />
        <div>
          <strong>Attack Classification Overview:</strong> Network flows are classified into 8 standardized attack categories based on the CIC-IDS2017 benchmark dataset collected over 5 days of enterprise traffic.
        </div>
      </div>

      {/* Grid: 2 Clean Charts */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(440px, 1fr))', gap: '24px', marginBottom: '24px' }}>
        
        {/* Chart 1: Malicious Attack Categories Bar Chart */}
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Malicious Traffic Breakdown</h2>
              <p className="card-subtitle">Distribution across 7 threat categories ({totalAttackCount.toLocaleString()} attack flows)</p>
            </div>
            <BarChart3 size={18} color="#1e3a8a" />
          </div>

          <div className="chart-container">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {attacksOnly.map((attack) => {
                const attackShare = ((attack.count / totalAttackCount) * 100).toFixed(1);
                return (
                  <div key={attack.name}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '6px' }}>
                      <span style={{ fontWeight: 600 }}>{attack.name}</span>
                      <span style={{ color: '#64748b' }}>
                        {attack.count.toLocaleString()} flows ({attackShare}% of attacks)
                      </span>
                    </div>
                    {/* Bar */}
                    <div style={{ height: '12px', backgroundColor: '#f1f5f9', borderRadius: '6px', overflow: 'hidden' }}>
                      <div 
                        style={{ 
                          width: `${attackShare}%`, 
                          height: '100%', 
                          backgroundColor: attack.color,
                          borderRadius: '6px'
                        }} 
                      />
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="chart-explanation">
              <strong>Short Explanation:</strong> Denial of Service (DoS) and Brute Force authentication attacks account for over 50% of all observed malicious network flows. High-volume attacks generate distinct packet bursts, making them easily detectable by Decision Trees and Random Forests.
            </div>
          </div>
        </div>

        {/* Chart 2: Normal vs Malicious Donut Chart */}
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Normal vs. Malicious Proportion</h2>
              <p className="card-subtitle">Overall dataset balance (129,016 total flow records)</p>
            </div>
            <PieIcon size={18} color="#1e3a8a" />
          </div>

          <div className="chart-container" style={{ textAlign: 'center' }}>
            {/* Simple Clean SVG Donut Chart */}
            <div style={{ position: 'relative', width: '220px', height: '220px', margin: '10px auto' }}>
              <svg width="220" height="220" viewBox="0 0 42 42">
                {/* Background circle */}
                <circle cx="21" cy="21" r="15.91549430918954" fill="#ffffff" />
                {/* Normal Traffic Arc: 55.03% */}
                <circle 
                  cx="21" cy="21" r="15.91549430918954" 
                  fill="transparent" 
                  stroke="#16a34a" 
                  strokeWidth="6" 
                  strokeDasharray="55.03 44.97" 
                  strokeDashoffset="25" 
                />
                {/* Malicious Traffic Arc: 44.97% */}
                <circle 
                  cx="21" cy="21" r="15.91549430918954" 
                  fill="transparent" 
                  stroke="#dc2626" 
                  strokeWidth="6" 
                  strokeDasharray="44.97 55.03" 
                  strokeDashoffset="-30.03" 
                />
              </svg>
              {/* Center text */}
              <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', textAlign: 'center' }}>
                <div style={{ fontSize: '24px', fontWeight: 700, color: '#1e3a8a' }}>129k</div>
                <div style={{ fontSize: '12px', color: '#64748b' }}>Total Flows</div>
              </div>
            </div>

            {/* Clear Legend */}
            <div style={{ display: 'flex', justifyContent: 'center', gap: '24px', marginTop: '12px', fontSize: '13px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ width: '12px', height: '12px', backgroundColor: '#16a34a', borderRadius: '3px' }}></span>
                <span style={{ fontWeight: 600 }}>Normal Traffic: 55.0% (71,000)</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ width: '12px', height: '12px', backgroundColor: '#dc2626', borderRadius: '3px' }}></span>
                <span style={{ fontWeight: 600 }}>Malicious Traffic: 45.0% (58,016)</span>
              </div>
            </div>

            <div className="chart-explanation">
              <strong>Short Explanation:</strong> This chart illustrates that our dataset is balanced between benign traffic (55%) and attack traffic (45%). In real-world networks, benign traffic exceeds 95%, so balanced sampling is essential to train machine learning models effectively without majority-class bias.
            </div>
          </div>
        </div>

      </div>

      {/* Attack Category Guide Card */}
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Understanding Detected Attack Categories</h2>
            <p className="card-subtitle">Overview of attack mechanics and network telemetry signatures</p>
          </div>
        </div>

        <div className="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Attack Category</th>
                <th>Underlying Attacks in Dataset</th>
                <th>How the Attack Works</th>
                <th>Key Flow Indicator</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style={{ fontWeight: 700, color: '#dc2626' }}>DoS (Denial of Service)</td>
                <td>DoS Hulk, GoldenEye, slowloris, Slowhttptest, Heartbleed</td>
                <td>Floods a target server with bogus requests to exhaust CPU and memory resources.</td>
                <td>High Flow Duration, low inter-arrival time, high packet count.</td>
              </tr>
              <tr>
                <td style={{ fontWeight: 700, color: '#b91c1c' }}>DDoS (Distributed DoS)</td>
                <td>DDoS LOIC / HOIC packet bursts</td>
                <td>Multiple coordinated machines flood the victim network simultaneously.</td>
                <td>Massive Flow Packets/s rate, uniform small packet sizes.</td>
              </tr>
              <tr>
                <td style={{ fontWeight: 700, color: '#d97706' }}>PortScan</td>
                <td>PortScan reconnaissance probes</td>
                <td>Scans thousands of IP ports looking for vulnerable open network services.</td>
                <td>Rapid single-packet flows targeting sequential destination ports.</td>
              </tr>
              <tr>
                <td style={{ fontWeight: 700, color: '#ea580c' }}>Brute Force</td>
                <td>FTP-Patator, SSH-Patator, Web Brute Force</td>
                <td>Repeatedly guesses user passwords via automated dictionary trials.</td>
                <td>Repeated login handshake flows with identical payload sizes.</td>
              </tr>
              <tr>
                <td style={{ fontWeight: 700, color: '#7c3aed' }}>Botnet</td>
                <td>Ares Bot communication</td>
                <td>Infected computer periodically contacting an external Command & Control server.</td>
                <td>Periodic heartbeat flows with consistent timing intervals.</td>
              </tr>
              <tr>
                <td style={{ fontWeight: 700, color: '#0284c7' }}>Web Attack</td>
                <td>Cross-Site Scripting (XSS), SQL Injection</td>
                <td>Injects malicious web payloads into browser forms or URL parameters.</td>
                <td>Targeting Destination Port 80/443 with specific HTTP payload lengths.</td>
              </tr>
              <tr>
                <td style={{ fontWeight: 700, color: '#475569' }}>Infiltration</td>
                <td>Privilege escalation & lateral movement</td>
                <td>An attacker attempting to compromise other internal network hosts.</td>
                <td>Unusual internal host-to-host flows following a phishing payload.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
