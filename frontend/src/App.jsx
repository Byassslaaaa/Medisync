import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'
import PatientForm from './components/PatientForm'
import PatientList from './components/PatientList'

const SERVICE_A_URL = import.meta.env.VITE_SERVICE_A_URL || 'http://localhost:4001'

export default function App() {
  const [patients, setPatients] = useState([])
  const [loading, setLoading]   = useState(false)
  const [activeTab, setActiveTab] = useState('form')

  const fetchPatients = useCallback(async () => {
    try {
      const res = await axios.get(`${SERVICE_A_URL}/api/patients`)
      setPatients(res.data.data || [])
    } catch (err) {
      console.error('Gagal fetch pasien:', err)
    }
  }, [])

  useEffect(() => {
    fetchPatients()
  }, [fetchPatients])

  return (
    <div style={styles.root}>
      {/* ── Header ── */}
      <header style={styles.header}>
        <div style={styles.headerInner}>
          <div style={styles.logo}>
            <span style={styles.logoIcon}>🏥</span>
            <div>
              <h1 style={styles.logoTitle}>MediSync</h1>
              <p style={styles.logoSub}>Sistem Informasi Rumah Sakit</p>
            </div>
          </div>
          <div style={styles.badge}>
            <span style={styles.badgeDot} />
            Microservices Active
          </div>
        </div>
      </header>

      {/* ── Tech Stack Info ── */}
      <div style={styles.techBar}>
        <span style={styles.techItem}>⚡ Go + Gin</span>
        <span style={styles.techSep}>|</span>
        <span style={styles.techItem}>🗄️ PostgreSQL</span>
        <span style={styles.techSep}>|</span>
        <span style={styles.techItem}>🔗 gRPC (Sync)</span>
        <span style={styles.techSep}>|</span>
        <span style={styles.techItem}>📨 RabbitMQ (Async)</span>
        <span style={styles.techSep}>|</span>
        <span style={styles.techItem}>🐳 Docker Compose</span>
      </div>

      {/* ── Main Content ── */}
      <main style={styles.main}>
        {/* Tabs */}
        <div style={styles.tabs}>
          <button
            style={activeTab === 'form' ? { ...styles.tab, ...styles.tabActive } : styles.tab}
            onClick={() => setActiveTab('form')}
          >
            + Daftar Pasien Baru
          </button>
          <button
            style={activeTab === 'list' ? { ...styles.tab, ...styles.tabActive } : styles.tab}
            onClick={() => { setActiveTab('list'); fetchPatients() }}
          >
            Daftar Pasien ({patients.length})
          </button>
        </div>

        <div style={styles.content}>
          {activeTab === 'form' ? (
            <PatientForm
              serviceAUrl={SERVICE_A_URL}
              onSuccess={() => { fetchPatients(); setActiveTab('list') }}
              loading={loading}
              setLoading={setLoading}
            />
          ) : (
            <PatientList patients={patients} onRefresh={fetchPatients} />
          )}
        </div>
      </main>

      {/* ── Footer ── */}
      <footer style={styles.footer}>
        MediSync • Jaringan Komputer Terapan 2025/2026 • Go + gRPC + RabbitMQ + PostgreSQL
      </footer>
    </div>
  )
}

const styles = {
  root: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    background: '#f0f4f8',
  },
  header: {
    background: 'linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%)',
    color: '#fff',
    padding: '16px 24px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
  },
  headerInner: {
    maxWidth: '1100px',
    margin: '0 auto',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  logo: { display: 'flex', alignItems: 'center', gap: '14px' },
  logoIcon: { fontSize: '2.2rem' },
  logoTitle: { fontSize: '1.6rem', fontWeight: 700, letterSpacing: '-0.5px' },
  logoSub: { fontSize: '0.8rem', opacity: 0.75, marginTop: '2px' },
  badge: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    background: 'rgba(255,255,255,0.15)',
    border: '1px solid rgba(255,255,255,0.3)',
    borderRadius: '20px',
    padding: '6px 14px',
    fontSize: '0.8rem',
    fontWeight: 500,
  },
  badgeDot: {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    background: '#4ade80',
    display: 'inline-block',
    animation: 'pulse 2s infinite',
  },
  techBar: {
    background: '#1e293b',
    color: '#94a3b8',
    textAlign: 'center',
    padding: '8px',
    fontSize: '0.78rem',
    display: 'flex',
    justifyContent: 'center',
    flexWrap: 'wrap',
    gap: '8px',
  },
  techItem: { color: '#7dd3fc', fontWeight: 500 },
  techSep: { color: '#334155' },
  main: {
    flex: 1,
    maxWidth: '900px',
    width: '100%',
    margin: '32px auto',
    padding: '0 16px',
  },
  tabs: {
    display: 'flex',
    gap: '4px',
    marginBottom: '0',
    background: '#e2e8f0',
    borderRadius: '12px 12px 0 0',
    padding: '6px 6px 0',
  },
  tab: {
    padding: '10px 22px',
    border: 'none',
    borderRadius: '8px 8px 0 0',
    background: 'transparent',
    color: '#64748b',
    fontWeight: 500,
    fontSize: '0.9rem',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  tabActive: {
    background: '#fff',
    color: '#2563eb',
    fontWeight: 600,
    boxShadow: '0 -2px 8px rgba(0,0,0,0.05)',
  },
  content: {
    background: '#fff',
    borderRadius: '0 12px 12px 12px',
    boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
    padding: '32px',
  },
  footer: {
    textAlign: 'center',
    padding: '16px',
    color: '#94a3b8',
    fontSize: '0.78rem',
    borderTop: '1px solid #e2e8f0',
    background: '#fff',
  },
}
