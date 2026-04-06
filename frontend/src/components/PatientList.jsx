import { IconRefresh, IconCheck, IconFolder } from './icons'

export default function PatientList({ patients, onRefresh }) {
  if (!patients || patients.length === 0) {
    return (
      <div>
        <div style={s.headerRow}>
          <h2 style={s.title}>Daftar Pasien Terdaftar</h2>
          <button onClick={onRefresh} style={s.refreshBtn}>
            <IconRefresh size={13} /> Refresh
          </button>
        </div>
        <div style={s.empty}>
          <IconFolder size={36} style={{ color: 'rgba(15,15,20,0.20)', margin: '0 auto 14px' }} />
          <p style={s.emptyText}>Belum ada pasien terdaftar.</p>
          <p style={s.emptyHint}>Gunakan tab "Daftar Pasien Baru" untuk mendaftarkan pasien pertama.</p>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div style={s.headerRow}>
        <div>
          <h2 style={s.title}>Daftar Pasien Terdaftar</h2>
          <p style={s.subtitle}>
            Data dari <code style={s.code}>db_pendaftaran</code> (Service A) •{' '}
            Draft rekam medis dibuat otomatis di <code style={s.code}>db_rekam_medis</code> (Service B) via RabbitMQ
          </p>
        </div>
        <button onClick={onRefresh} style={s.refreshBtn}>
          <IconRefresh size={13} /> Refresh
        </button>
      </div>

      <div style={s.tableWrap}>
        <table style={s.table}>
          <thead>
            <tr>
              {['No','Nama','NIK','Tanggal Lahir','No. Telepon','Terdaftar','Status'].map(h => (
                <th key={h} style={s.th}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {patients.map((p, i) => (
              <tr key={p.patient_id}
                style={i % 2 === 0 ? s.tr : s.trAlt}
                onMouseEnter={e => e.currentTarget.style.background = 'rgba(15,15,20,0.04)'}
                onMouseLeave={e => e.currentTarget.style.background = i % 2 === 0 ? s.tr.background : s.trAlt.background}
              >
                <td style={{ ...s.td, color: 'rgba(15,15,20,0.40)', width: '40px' }}>{i + 1}</td>
                <td style={{ ...s.td, fontWeight: 600, color: 'rgba(15,15,20,0.85)' }}>{p.name}</td>
                <td style={s.td}><code style={s.nikCode}>{p.nik}</code></td>
                <td style={s.td}>{p.tanggal_lahir}</td>
                <td style={{ ...s.td, color: 'rgba(15,15,20,0.55)' }}>{p.no_telepon || '—'}</td>
                <td style={{ ...s.td, fontSize: '0.80rem', color: 'rgba(15,15,20,0.55)' }}>
                  {new Date(p.registered_at).toLocaleString('id-ID', {
                    day: '2-digit', month: 'short', year: 'numeric',
                    hour: '2-digit', minute: '2-digit',
                  })}
                </td>
                <td style={s.td}>
                  <span style={s.badge}>
                    <IconCheck size={10} /> Aktif
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p style={s.footNote}>
        Total: <strong>{patients.length} pasien</strong> terdaftar.
      </p>
    </div>
  )
}

const s = {
  headerRow: {
    display: 'flex', justifyContent: 'space-between',
    alignItems: 'flex-start', marginBottom: '20px', gap: '16px',
  },
  title: {
    fontSize: '1.35rem', fontWeight: 700,
    color: 'rgba(15,15,20,0.85)', letterSpacing: '-0.3px', marginBottom: '4px',
  },
  subtitle: { fontSize: '0.78rem', color: 'rgba(15,15,20,0.50)', lineHeight: 1.6 },
  code: {
    background: 'rgba(15,15,20,0.07)', borderRadius: '4px',
    padding: '1px 5px', fontFamily: 'monospace',
    fontSize: '0.75rem', color: 'rgba(15,15,20,0.72)',
  },

  refreshBtn: {
    display: 'flex', alignItems: 'center', gap: '6px',
    padding: '8px 14px',
    background: 'rgba(255,255,255,0.80)',
    border: '1px solid rgba(15,15,20,0.12)',
    borderRadius: '10px', fontSize: '0.82rem',
    cursor: 'pointer', fontWeight: 500,
    color: 'rgba(15,15,20,0.65)', whiteSpace: 'nowrap',
    boxShadow: '0 1px 4px rgba(0,0,0,0.07)',
  },

  empty: {
    textAlign: 'center', padding: '56px 20px',
    background: 'rgba(15,15,20,0.03)',
    border: '1.5px dashed rgba(15,15,20,0.12)',
    borderRadius: '14px',
  },
  emptyText: { fontSize: '0.95rem', fontWeight: 600, color: 'rgba(15,15,20,0.55)', marginBottom: '6px' },
  emptyHint: { fontSize: '0.82rem', color: 'rgba(15,15,20,0.38)' },

  tableWrap: {
    overflowX: 'auto', borderRadius: '12px',
    border: '1px solid rgba(15,15,20,0.10)',
    boxShadow: '0 1px 6px rgba(0,0,0,0.06)',
  },
  table: { width: '100%', borderCollapse: 'collapse', fontSize: '0.86rem' },
  th: {
    padding: '11px 14px', textAlign: 'left',
    background: 'rgba(15,15,20,0.06)',
    color: 'rgba(15,15,20,0.50)', fontWeight: 700,
    fontSize: '0.70rem', letterSpacing: '0.07em', textTransform: 'uppercase',
    borderBottom: '1px solid rgba(15,15,20,0.10)',
  },
  tr:    { background: '#ffffff' },
  trAlt: { background: 'rgba(15,15,20,0.02)' },
  td: {
    padding: '11px 14px',
    borderBottom: '1px solid rgba(15,15,20,0.06)',
    color: 'rgba(15,15,20,0.72)', verticalAlign: 'middle',
  },
  nikCode: {
    fontFamily: 'monospace',
    background: 'rgba(15,15,20,0.06)',
    padding: '2px 7px', borderRadius: '5px',
    fontSize: '0.80rem', letterSpacing: '0.04em',
    color: 'rgba(15,15,20,0.75)',
  },
  badge: {
    display: 'inline-flex', alignItems: 'center', gap: '5px',
    padding: '3px 10px',
    background: 'rgba(15,15,20,0.06)',
    border: '1px solid rgba(15,15,20,0.10)',
    borderRadius: '999px', fontSize: '0.73rem',
    fontWeight: 600, color: 'rgba(15,15,20,0.65)',
  },
  footNote: {
    marginTop: '14px', fontSize: '0.78rem', color: 'rgba(15,15,20,0.50)',
    padding: '9px 14px',
    background: 'rgba(15,15,20,0.03)',
    borderRadius: '8px', border: '1px solid rgba(15,15,20,0.08)',
  },
}
