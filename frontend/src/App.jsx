import { useState, useEffect, useCallback } from "react";
import axios from "axios";
import PatientForm from "./components/PatientForm";
import PatientList from "./components/PatientList";
import { IconTerminal, IconDatabase, IconLink, IconMessage, IconBox } from "./components/icons";

const SERVICE_A_URL = import.meta.env.VITE_SERVICE_A_URL || "http://localhost:4001";

export default function App() {
  const [patients, setPatients]   = useState([]);
  const [loading, setLoading]     = useState(false);
  const [activeTab, setActiveTab] = useState("form");

  const fetchPatients = useCallback(async () => {
    try {
      const res = await axios.get(`${SERVICE_A_URL}/api/patients`);
      setPatients(res.data.data || []);
    } catch (err) {
      console.error("Gagal fetch pasien:", err);
    }
  }, []);

  useEffect(() => { fetchPatients(); }, [fetchPatients]);

  const techItems = [
    { icon: <IconTerminal size={13} />, label: "Go + Gin" },
    { icon: <IconDatabase size={13} />, label: "PostgreSQL" },
    { icon: <IconLink     size={13} />, label: "gRPC (Sync)" },
    { icon: <IconMessage  size={13} />, label: "RabbitMQ (Async)" },
    { icon: <IconBox      size={13} />, label: "Docker Compose" },
  ];

  return (
    <div style={styles.root}>
      {/* ── Video Background ── */}
      <video autoPlay muted loop playsInline style={styles.videoBg}>
        <source src="/images/bg.mp4" type="video/mp4" />
      </video>
      <div style={styles.videoOverlay} />

      {/* ── Header ── */}
      <header style={styles.header}>
        <div style={styles.headerInner}>
          <div style={styles.logo}>
            <img src="/images/logo.png" alt="" style={styles.logoImg}
              onError={e => { e.target.style.display = "none"; }} />
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

      {/* ── Tech Stack Bar ── */}
      <div style={styles.techBar}>
        <span style={styles.techLabel}>SYSTEM STACK</span>
        <span style={styles.techSep}>|</span>
        {techItems.map((t, i) => (
          <span key={t.label} style={{ display: "contents" }}>
            <span style={styles.techItem}>
              {t.icon}
              {t.label}
            </span>
            {i < techItems.length - 1 && <span style={styles.techSep}>|</span>}
          </span>
        ))}
      </div>

      {/* ── macOS Window ── */}
      <main style={styles.main}>
        <div style={styles.window}>

          {/* Title Bar */}
          <div style={styles.titleBar}>
            <div style={styles.trafficLights}>
              <span style={{ ...styles.light, background: "#FF5F56" }} />
              <span style={{ ...styles.light, background: "#FFBD2E" }} />
              <span style={{ ...styles.light, background: "#27C93F" }} />
            </div>
            <span style={styles.windowTitle}>MediSync — Pendaftaran Pasien</span>
            <div style={{ width: "44px" }} />
          </div>

          {/* Segmented Control */}
          <div style={styles.segmentedWrap}>
            <div style={styles.segmented}>
              <div style={{
                ...styles.segmentIndicator,
                left: activeTab === "form" ? "3px" : "calc(50% + 1px)",
              }} />
              <button
                style={{ ...styles.segment, ...(activeTab === "form" ? styles.segmentActive : {}) }}
                onClick={() => setActiveTab("form")}
              >
                + Daftar Pasien Baru
              </button>
              <button
                style={{ ...styles.segment, ...(activeTab === "list" ? styles.segmentActive : {}) }}
                onClick={() => { setActiveTab("list"); fetchPatients(); }}
              >
                Daftar Pasien ({patients.length})
              </button>
            </div>
          </div>

          {/* Content */}
          <div style={styles.content}>
            {activeTab === "form" ? (
              <PatientForm
                serviceAUrl={SERVICE_A_URL}
                onSuccess={() => { fetchPatients(); setActiveTab("list"); }}
                loading={loading}
                setLoading={setLoading}
              />
            ) : (
              <PatientList patients={patients} onRefresh={fetchPatients} />
            )}
          </div>
        </div>
      </main>

      {/* ── Footer ── */}
      <footer style={styles.footer}>
        <p style={styles.footerCredit}>Credit: by Kelompok Teori @ <strong>MediSync</strong></p>
        <p style={styles.footerSub}>MediSync • Jaringan Komputer Terapan 2025/2026 • Go + gRPC • RabbitMQ • PostgreSQL</p>
      </footer>
    </div>
  );
}

const styles = {
  root: { minHeight: "100vh", display: "flex", flexDirection: "column", position: "relative" },
  videoBg: { position: "fixed", top: 0, left: 0, width: "100%", height: "100%", objectFit: "cover", zIndex: -2 },
  videoOverlay: { position: "fixed", top: 0, left: 0, width: "100%", height: "100%", background: "rgba(220,225,235,0.10)", zIndex: -1 },

  header: {
    background: "rgba(255,255,255,0.42)",
    backdropFilter: "blur(32px) saturate(180%) brightness(1.08)",
    WebkitBackdropFilter: "blur(32px) saturate(180%) brightness(1.08)",
    padding: "13px 28px",
    borderBottom: "1px solid rgba(255,255,255,0.55)",
    boxShadow: "0 1px 0 rgba(255,255,255,0.6), 0 2px 20px rgba(0,0,0,0.06)",
  },
  headerInner: { maxWidth: "1100px", margin: "0 auto", display: "flex", alignItems: "center", justifyContent: "space-between" },
  logo: { display: "flex", alignItems: "center", gap: "12px" },
  logoImg: { width: "44px", height: "44px", objectFit: "contain", borderRadius: "10px" },
  logoTitle: { fontSize: "1.5rem", fontWeight: 700, color: "rgba(15,15,20,0.88)", letterSpacing: "-0.5px" },
  logoSub: { fontSize: "0.74rem", color: "rgba(15,15,20,0.48)", marginTop: "1px" },
  badge: {
    display: "flex", alignItems: "center", gap: "7px",
    background: "rgba(12,12,18,0.68)",
    backdropFilter: "blur(16px)", WebkitBackdropFilter: "blur(16px)",
    border: "1px solid rgba(255,255,255,0.12)",
    borderRadius: "999px", padding: "6px 14px",
    fontSize: "0.75rem", fontWeight: 500, color: "rgba(255,255,255,0.88)", letterSpacing: "0.02em",
  },
  badgeDot: {
    width: "6px", height: "6px", borderRadius: "50%",
    background: "rgba(255,255,255,0.75)", display: "inline-block",
    animation: "pulse 2.4s cubic-bezier(0.4,0,0.2,1) infinite",
  },

  techBar: {
    background: "rgba(255,255,255,0.20)",
    backdropFilter: "blur(20px) saturate(160%)", WebkitBackdropFilter: "blur(20px) saturate(160%)",
    borderBottom: "1px solid rgba(255,255,255,0.32)",
    padding: "6px 28px",
    display: "flex", justifyContent: "center", alignItems: "center", flexWrap: "wrap", gap: "8px",
  },
  techLabel: { color: "rgba(15,15,20,0.38)", fontWeight: 700, fontSize: "0.65rem", letterSpacing: "0.10em" },
  techItem: { display: "flex", alignItems: "center", gap: "5px", color: "rgba(15,15,20,0.58)", fontWeight: 500, fontSize: "0.72rem" },
  techSep:  { color: "rgba(15,15,20,0.15)", fontSize: "0.72rem" },

  main: { flex: 1, display: "flex", alignItems: "center", justifyContent: "center", padding: "28px 16px" },
  window: {
    width: "100%", maxWidth: "820px",
    background: "rgba(245,246,250,0.82)",
    backdropFilter: "blur(60px) saturate(180%) brightness(1.05)",
    WebkitBackdropFilter: "blur(60px) saturate(180%) brightness(1.05)",
    borderRadius: "20px",
    border: "1px solid rgba(255,255,255,0.80)",
    boxShadow: "0 32px 80px rgba(0,0,0,0.22), 0 8px 24px rgba(0,0,0,0.10), inset 0 1px 0 rgba(255,255,255,0.95), inset 0 -1px 0 rgba(0,0,0,0.04)",
    overflow: "hidden",
  },

  titleBar: {
    display: "flex", alignItems: "center", justifyContent: "space-between",
    padding: "13px 18px 12px",
    background: "rgba(235,237,245,0.90)",
    borderBottom: "1px solid rgba(255,255,255,0.70)",
    backdropFilter: "blur(20px)", WebkitBackdropFilter: "blur(20px)",
    position: "relative",
  },
  trafficLights: { display: "flex", gap: "7px", alignItems: "center" },
  light: { width: "12px", height: "12px", borderRadius: "50%", boxShadow: "inset 0 0 0 0.5px rgba(0,0,0,0.15)", flexShrink: 0 },
  windowTitle: { fontSize: "0.8rem", fontWeight: 500, color: "rgba(15,15,20,0.50)", letterSpacing: "0.01em", position: "absolute", left: "50%", transform: "translateX(-50%)" },

  segmentedWrap: { padding: "14px 24px 0", background: "rgba(240,241,248,0.85)", borderBottom: "1px solid rgba(255,255,255,0.60)" },
  segmented: { position: "relative", display: "inline-flex", background: "rgba(0,0,0,0.08)", borderRadius: "10px", padding: "3px", marginBottom: "-1px" },
  segmentIndicator: {
    position: "absolute", top: "3px",
    width: "calc(50% - 2px)", height: "calc(100% - 6px)",
    background: "rgba(255,255,255,0.65)",
    backdropFilter: "blur(12px)", WebkitBackdropFilter: "blur(12px)",
    borderRadius: "7px",
    boxShadow: "0 1px 4px rgba(0,0,0,0.12), inset 0 1px 0 rgba(255,255,255,0.9)",
    transition: "left 0.28s cubic-bezier(0.4,0,0.2,1)",
    pointerEvents: "none",
  },
  segment: {
    position: "relative", zIndex: 1,
    padding: "7px 20px", border: "none", background: "transparent",
    fontSize: "0.83rem", fontWeight: 500, color: "rgba(15,15,20,0.48)",
    cursor: "pointer", borderRadius: "7px", letterSpacing: "0.01em", whiteSpace: "nowrap",
  },
  segmentActive: { color: "rgba(15,15,20,0.85)", fontWeight: 600 },
  content: { padding: "28px 32px 32px", background: "rgba(255,255,255,0.60)", backdropFilter: "blur(20px)", WebkitBackdropFilter: "blur(20px)" },

  footer: {
    textAlign: "center", padding: "13px 16px",
    background: "rgba(255,255,255,0.20)",
    backdropFilter: "blur(20px) saturate(160%)", WebkitBackdropFilter: "blur(20px) saturate(160%)",
    borderTop: "1px solid rgba(255,255,255,0.35)",
  },
  footerCredit: { margin: "0 0 2px", fontSize: "0.78rem", color: "rgba(15,15,20,0.50)" },
  footerSub:    { margin: 0, color: "rgba(15,15,20,0.32)", fontSize: "0.70rem", letterSpacing: "0.02em" },
};
