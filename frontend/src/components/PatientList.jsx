export default function PatientList({ patients, onRefresh }) {
  if (!patients || patients.length === 0) {
    return (
      <div>
        <div style={styles.headerRow}>
          <h2 style={styles.title}>Daftar Pasien Terdaftar</h2>
          <button onClick={onRefresh} style={styles.refreshBtn}>↻ Refresh</button>
        </div>
        <div style={styles.empty}>
          <span style={styles.emptyIcon}>🗂️</span>
          <p style={styles.emptyText}>Belum ada pasien yang terdaftar.</p>
          <p style={styles.emptyHint}>Gunakan tab "Daftar Pasien Baru" untuk mendaftarkan pasien pertama.</p>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div style={styles.headerRow}>
        <div>
          <h2 style={styles.title}>Daftar Pasien Terdaftar</h2>
          <p style={styles.subtitle}>
            Data dari <code style={styles.code}>db_pendaftaran</code> (Service A) •
            Draft rekam medis dibuat otomatis di <code style={styles.code}>db_rekam_medis</code> (Service B) via RabbitMQ
          </p>
        </div>
        <button onClick={onRefresh} style={styles.refreshBtn}>↻ Refresh</button>
      </div>

      <div style={styles.tableWrap}>
        <table style={styles.table}>
          <thead>
            <tr style={styles.thead}>
              <th style={styles.th}>No</th>
              <th style={styles.th}>Nama</th>
              <th style={styles.th}>NIK</th>
              <th style={styles.th}>Tanggal Lahir</th>
              <th style={styles.th}>No. Telepon</th>
              <th style={styles.th}>Terdaftar</th>
              <th style={styles.th}>Status</th>
            </tr>
          </thead>
          <tbody>
            {patients.map((p, i) => (
              <tr key={p.patient_id} style={i % 2 === 0 ? styles.tr : styles.trAlt}>
                <td style={styles.td}>{i + 1}</td>
                <td style={{ ...styles.td, fontWeight: 600, color: '#1e3a8a' }}>{p.name}</td>
                <td style={styles.td}>
                  <code style={styles.nikCode}>{p.nik}</code>
                </td>
                <td style={styles.td}>{p.tanggal_lahir}</td>
                <td style={styles.td}>{p.no_telepon || '-'}</td>
                <td style={styles.td}>
                  {new Date(p.registered_at).toLocaleString('id-ID', {
                    day: '2-digit', month: 'short', year: 'numeric',
                    hour: '2-digit', minute: '2-digit',
                  })}
                </td>
                <td style={styles.td}>
                  <span style={styles.badge}>✓ Aktif</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p style={styles.footNote}>
        Total: <strong>{patients.length} pasien</strong> terdaftar.
        Draft rekam medis dikirim ke Service B via <strong>RabbitMQ</strong> secara asinkron.
      </p>
    </div>
  )
}

const styles = {
  headerRow: {
    display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start',
    marginBottom: '20px', gap: '16px',
  },
  title: { fontSize: '1.4rem', fontWeight: 700, color: '#1e3a8a', marginBottom: '4px' },
  subtitle: { fontSize: '0.8rem', color: '#64748b', lineHeight: 1.5 },
  code: { background: '#f1f5f9', borderRadius: '4px', padding: '1px 5px', fontFamily: 'monospace', fontSize: '0.78rem' },
  refreshBtn: {
    padding: '8px 16px', background: '#f1f5f9', border: '1.5px solid #e2e8f0',
    borderRadius: '8px', fontSize: '0.85rem', cursor: 'pointer', fontWeight: 500,
    color: '#475569', whiteSpace: 'nowrap',
    transition: 'background 0.2s',
  },
  empty: {
    textAlign: 'center', padding: '60px 20px',
    border: '2px dashed #e2e8f0', borderRadius: '12px', background: '#f8fafc',
  },
  emptyIcon: { fontSize: '3rem', display: 'block', marginBottom: '12px' },
  emptyText: { fontSize: '1rem', fontWeight: 600, color: '#475569', marginBottom: '6px' },
  emptyHint: { fontSize: '0.85rem', color: '#94a3b8' },
  tableWrap: { overflowX: 'auto', borderRadius: '10px', border: '1px solid #e2e8f0' },
  table: { width: '100%', borderCollapse: 'collapse', fontSize: '0.875rem' },
  thead: { background: '#1e3a8a' },
  th: {
    padding: '12px 14px', textAlign: 'left',
    color: '#fff', fontWeight: 600, fontSize: '0.82rem',
    letterSpacing: '0.03em',
  },
  tr: { background: '#fff' },
  trAlt: { background: '#f8fafc' },
  td: {
    padding: '12px 14px', borderBottom: '1px solid #f1f5f9',
    color: '#374151', verticalAlign: 'middle',
  },
  nikCode: {
    fontFamily: 'monospace', background: '#f1f5f9',
    padding: '2px 6px', borderRadius: '4px', fontSize: '0.82rem', letterSpacing: '0.05em',
  },
  badge: {
    display: 'inline-block', padding: '3px 10px',
    background: '#dcfce7', color: '#15803d',
    borderRadius: '20px', fontSize: '0.78rem', fontWeight: 600,
  },
  footNote: {
    marginTop: '14px', fontSize: '0.8rem', color: '#64748b',
    padding: '10px 14px', background: '#f8fafc', borderRadius: '8px',
    border: '1px solid #e2e8f0',
  },
}
