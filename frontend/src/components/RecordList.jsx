import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'
import { IconRefresh, IconFolder } from './icons'

const SERVICE_A_URL = import.meta.env.VITE_SERVICE_A_URL || 'http://localhost:4001'

export default function RecordList() {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)

  const fetchRecords = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      // Frontend → Service A (REST) → Service B (gRPC) → db_rekam_medis
      const res = await axios.get(`${SERVICE_A_URL}/api/medical-records`)
      setRecords(res.data.data || [])
    } catch {
      setError('Gagal memuat rekam medis. Pastikan Service A & B berjalan.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchRecords() }, [fetchRecords])

  return (
    <div>
      <div style={s.headerRow}>
        <div>
          <h2 style={s.title}>Rekam Medis</h2>
          <p style={s.subtitle}>
            Data dari <code style={s.code}>db_rekam_medis</code> (Service B) •{' '}
            Draft dibuat otomatis via RabbitMQ saat pasien didaftarkan
          </p>
        </div>
        <button onClick={fetchRecords} style={s.refreshBtn} disabled={loading}>
          <IconRefresh size={13} /> Refresh
        </button>
      </div>

      {error && <div style={s.errorBox}>{error}</div>}

      {loading && (
        <div style={s.loadingBox}>
          <div style={s.spinner} /> Memuat data...
        </div>
      )}

      {!loading && !error && records.length === 0 && (
        <div style={s.empty}>
          <IconFolder size={36} style={{ color: 'rgba(15,15,20,0.20)', margin: '0 auto 14px' }} />
          <p style={s.emptyText}>Belum ada rekam medis.</p>
          <p style={s.emptyHint}>Daftarkan pasien terlebih dahulu. Draft rekam medis akan dibuat otomatis.</p>
        </div>
      )}

      {!loading && records.length > 0 && (
        <>
          <div style={s.tableWrap}>
            <table style={s.table}>
              <thead>
                <tr>
                  {['No', 'Nama', 'NIK', 'Diagnosis', 'Catatan', 'Dibuat'].map(h => (
                    <th key={h} style={s.th}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {records.map((rec, i) => (
                  <tr
                    key={rec.id}
                    style={i % 2 === 0 ? s.tr : s.trAlt}
                    onMouseEnter={e => e.currentTarget.style.background = 'rgba(15,15,20,0.04)'}
                    onMouseLeave={e => e.currentTarget.style.background = i % 2 === 0 ? s.tr.background : s.trAlt.background}
                  >
                    <td style={{ ...s.td, color: 'rgba(15,15,20,0.40)', width: 36 }}>{i + 1}</td>
                    <td style={{ ...s.td, fontWeight: 600, color: 'rgba(15,15,20,0.85)' }}>{rec.name || '—'}</td>
                    <td style={s.td}>
                      {rec.nik ? <code style={s.nikCode}>{rec.nik}</code> : <span style={{ color: 'rgba(15,15,20,0.30)' }}>—</span>}
                    </td>
                    <td style={{ ...s.td, maxWidth: 200 }}>
                      <span style={{
                        color: rec.diagnosis === 'Draft - Belum ada diagnosis' ? 'rgba(15,15,20,0.35)' : 'rgba(15,15,20,0.78)',
                        fontStyle: rec.diagnosis === 'Draft - Belum ada diagnosis' ? 'italic' : 'normal',
                        fontSize: '0.83rem',
                      }}>
                        {rec.diagnosis}
                      </span>
                    </td>
                    <td style={{ ...s.td, fontSize: '0.82rem', color: 'rgba(15,15,20,0.55)', maxWidth: 220 }}>
                      {rec.notes || '—'}
                    </td>
                    <td style={{ ...s.td, fontSize: '0.80rem', color: 'rgba(15,15,20,0.55)', whiteSpace: 'nowrap' }}>
                      {new Date(rec.created_at).toLocaleString('id-ID', {
                        day: '2-digit', month: 'short', year: 'numeric',
                        hour: '2-digit', minute: '2-digit',
                      })}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p style={s.footNote}>
            Total: <strong>{records.length} rekam medis</strong>.
          </p>
        </>
      )}
    </div>
  )
}

const s = {
  headerRow: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 20, gap: 16 },
  title:    { fontSize: '1.35rem', fontWeight: 700, color: 'rgba(15,15,20,0.85)', letterSpacing: '-0.3px', marginBottom: 4 },
  subtitle: { fontSize: '0.78rem', color: 'rgba(15,15,20,0.50)', lineHeight: 1.6 },
  code:     { background: 'rgba(15,15,20,0.07)', borderRadius: 4, padding: '1px 5px', fontFamily: 'monospace', fontSize: '0.75rem', color: 'rgba(15,15,20,0.72)' },

  refreshBtn: { display: 'flex', alignItems: 'center', gap: 6, padding: '8px 14px', background: 'rgba(255,255,255,0.80)', border: '1px solid rgba(15,15,20,0.12)', borderRadius: 10, fontSize: '0.82rem', cursor: 'pointer', fontWeight: 500, color: 'rgba(15,15,20,0.65)', whiteSpace: 'nowrap', boxShadow: '0 1px 4px rgba(0,0,0,0.07)' },

  errorBox:   { background: 'rgba(220,38,38,0.08)', border: '1px solid rgba(220,38,38,0.22)', borderRadius: 10, padding: '12px 16px', color: 'rgba(180,0,0,0.85)', fontSize: '0.85rem', marginBottom: 12 },
  loadingBox: { display: 'flex', alignItems: 'center', gap: 10, padding: '40px 0', justifyContent: 'center', color: 'rgba(15,15,20,0.45)', fontSize: '0.88rem' },
  spinner:    { width: 18, height: 18, border: '2.5px solid rgba(15,15,20,0.12)', borderTop: '2.5px solid rgba(37,99,235,0.7)', borderRadius: '50%', animation: 'spin 0.7s linear infinite' },

  empty:     { textAlign: 'center', padding: '56px 20px', background: 'rgba(15,15,20,0.03)', border: '1.5px dashed rgba(15,15,20,0.12)', borderRadius: 14 },
  emptyText: { fontSize: '0.95rem', fontWeight: 600, color: 'rgba(15,15,20,0.55)', marginBottom: 6 },
  emptyHint: { fontSize: '0.82rem', color: 'rgba(15,15,20,0.38)' },

  tableWrap: { overflowX: 'auto', borderRadius: 12, border: '1px solid rgba(15,15,20,0.10)', boxShadow: '0 1px 6px rgba(0,0,0,0.06)' },
  table:     { width: '100%', borderCollapse: 'collapse', fontSize: '0.86rem' },
  th:        { padding: '11px 14px', textAlign: 'left', background: 'rgba(15,15,20,0.06)', color: 'rgba(15,15,20,0.50)', fontWeight: 700, fontSize: '0.70rem', letterSpacing: '0.07em', textTransform: 'uppercase', borderBottom: '1px solid rgba(15,15,20,0.10)' },
  tr:        { background: '#ffffff' },
  trAlt:     { background: 'rgba(15,15,20,0.02)' },
  td:        { padding: '11px 14px', borderBottom: '1px solid rgba(15,15,20,0.06)', color: 'rgba(15,15,20,0.72)', verticalAlign: 'middle' },
  nikCode:   { fontFamily: 'monospace', background: 'rgba(15,15,20,0.06)', padding: '2px 7px', borderRadius: 5, fontSize: '0.80rem', letterSpacing: '0.04em', color: 'rgba(15,15,20,0.75)' },
  footNote:  { marginTop: 14, fontSize: '0.78rem', color: 'rgba(15,15,20,0.50)', padding: '9px 14px', background: 'rgba(15,15,20,0.03)', borderRadius: 8, border: '1px solid rgba(15,15,20,0.08)' },
}
