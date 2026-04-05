import { useState } from 'react'
import axios from 'axios'

export default function PatientForm({ serviceAUrl, onSuccess, loading, setLoading }) {
  const [form, setForm]       = useState({ name: '', nik: '', tanggal_lahir: '', no_telepon: '' })
  const [result, setResult]   = useState(null) // { type: 'success'|'error', message, data }
  const [errors, setErrors]   = useState({})

  const validate = () => {
    const e = {}
    if (!form.name.trim())          e.name = 'Nama wajib diisi.'
    if (!form.nik.trim())           e.nik  = 'NIK wajib diisi.'
    else if (form.nik.length !== 16) e.nik  = 'NIK harus 16 digit.'
    else if (!/^\d+$/.test(form.nik)) e.nik = 'NIK hanya boleh angka.'
    if (!form.tanggal_lahir)        e.tanggal_lahir = 'Tanggal lahir wajib diisi.'
    return e
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: value }))
    if (errors[name]) setErrors(prev => ({ ...prev, [name]: '' }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setResult(null)

    const validationErrors = validate()
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors)
      return
    }

    setLoading(true)
    try {
      const res = await axios.post(`${serviceAUrl}/api/patients`, form)
      setResult({
        type: 'success',
        message: res.data.message,
        data: res.data.data,
      })
      setForm({ name: '', nik: '', tanggal_lahir: '', no_telepon: '' })
      setErrors({})
      setTimeout(onSuccess, 1500)
    } catch (err) {
      const msg = err.response?.data?.message || 'Terjadi kesalahan. Coba lagi.'
      setResult({ type: 'error', message: msg })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div style={styles.header}>
        <h2 style={styles.title}>Pendaftaran Pasien Baru</h2>
        <p style={styles.subtitle}>
          Data akan divalidasi via <strong>gRPC</strong> ke Service Rekam Medis,
          kemudian event dikirim ke <strong>RabbitMQ</strong> untuk pembuatan draft rekam medis.
        </p>
      </div>

      {/* Flow Indicator */}
      <div style={styles.flowBar}>
        <div style={styles.flowStep}>
          <span style={styles.flowNum}>1</span>
          <span style={styles.flowText}>Input Form</span>
        </div>
        <span style={styles.flowArrow}>→</span>
        <div style={styles.flowStep}>
          <span style={{ ...styles.flowNum, background: '#d97706' }}>2</span>
          <span style={styles.flowText}>gRPC Check</span>
        </div>
        <span style={styles.flowArrow}>→</span>
        <div style={styles.flowStep}>
          <span style={{ ...styles.flowNum, background: '#16a34a' }}>3</span>
          <span style={styles.flowText}>Simpan DB</span>
        </div>
        <span style={styles.flowArrow}>→</span>
        <div style={styles.flowStep}>
          <span style={{ ...styles.flowNum, background: '#dc2626' }}>4</span>
          <span style={styles.flowText}>RabbitMQ Event</span>
        </div>
      </div>

      {/* Alert */}
      {result && (
        <div style={result.type === 'success' ? styles.alertSuccess : styles.alertError}>
          <span style={styles.alertIcon}>{result.type === 'success' ? '✓' : '✗'}</span>
          <div>
            <strong>{result.type === 'success' ? 'Berhasil!' : 'Gagal!'}</strong>
            <p style={{ margin: '4px 0 0', fontSize: '0.875rem' }}>{result.message}</p>
            {result.data && (
              <p style={{ margin: '4px 0 0', fontSize: '0.8rem', opacity: 0.8 }}>
                Patient ID: <code style={styles.code}>{result.data.patient_id}</code>
              </p>
            )}
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.formGrid}>
          {/* Nama */}
          <div style={styles.field}>
            <label style={styles.label}>Nama Lengkap <span style={styles.required}>*</span></label>
            <input
              name="name"
              value={form.name}
              onChange={handleChange}
              placeholder="cth: Budi Santoso"
              style={errors.name ? { ...styles.input, ...styles.inputError } : styles.input}
            />
            {errors.name && <span style={styles.errorMsg}>{errors.name}</span>}
          </div>

          {/* NIK */}
          <div style={styles.field}>
            <label style={styles.label}>NIK <span style={styles.required}>*</span></label>
            <input
              name="nik"
              value={form.nik}
              onChange={handleChange}
              placeholder="16 digit NIK"
              maxLength={16}
              style={errors.nik ? { ...styles.input, ...styles.inputError } : styles.input}
            />
            <span style={styles.hint}>{form.nik.length}/16 digit</span>
            {errors.nik && <span style={styles.errorMsg}>{errors.nik}</span>}
          </div>

          {/* Tanggal Lahir */}
          <div style={styles.field}>
            <label style={styles.label}>Tanggal Lahir <span style={styles.required}>*</span></label>
            <input
              type="date"
              name="tanggal_lahir"
              value={form.tanggal_lahir}
              onChange={handleChange}
              style={errors.tanggal_lahir ? { ...styles.input, ...styles.inputError } : styles.input}
            />
            {errors.tanggal_lahir && <span style={styles.errorMsg}>{errors.tanggal_lahir}</span>}
          </div>

          {/* No. Telepon */}
          <div style={styles.field}>
            <label style={styles.label}>No. Telepon <span style={styles.optional}>(opsional)</span></label>
            <input
              name="no_telepon"
              value={form.no_telepon}
              onChange={handleChange}
              placeholder="cth: 08123456789"
              style={styles.input}
            />
          </div>
        </div>

        <button type="submit" disabled={loading} style={loading ? { ...styles.btn, ...styles.btnDisabled } : styles.btn}>
          {loading ? (
            <span>⏳ Memproses (gRPC + DB + MQ)...</span>
          ) : (
            <span>✓ Daftarkan Pasien</span>
          )}
        </button>
      </form>
    </div>
  )
}

const styles = {
  header: { marginBottom: '20px' },
  title: { fontSize: '1.4rem', fontWeight: 700, color: '#1e3a8a', marginBottom: '6px' },
  subtitle: { fontSize: '0.85rem', color: '#64748b', lineHeight: 1.5 },
  flowBar: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    background: '#f8fafc',
    border: '1px solid #e2e8f0',
    borderRadius: '10px',
    padding: '12px 16px',
    marginBottom: '24px',
    flexWrap: 'wrap',
  },
  flowStep: { display: 'flex', alignItems: 'center', gap: '6px' },
  flowNum: {
    width: '22px', height: '22px', borderRadius: '50%',
    background: '#2563eb', color: '#fff',
    fontSize: '0.7rem', fontWeight: 700,
    display: 'flex', alignItems: 'center', justifyContent: 'center',
  },
  flowText: { fontSize: '0.8rem', color: '#475569', fontWeight: 500 },
  flowArrow: { color: '#94a3b8', fontWeight: 700 },
  alertSuccess: {
    display: 'flex', gap: '12px', alignItems: 'flex-start',
    background: '#f0fdf4', border: '1px solid #bbf7d0',
    borderRadius: '10px', padding: '14px 16px', marginBottom: '20px', color: '#15803d',
  },
  alertError: {
    display: 'flex', gap: '12px', alignItems: 'flex-start',
    background: '#fef2f2', border: '1px solid #fecaca',
    borderRadius: '10px', padding: '14px 16px', marginBottom: '20px', color: '#dc2626',
  },
  alertIcon: { fontSize: '1.2rem', fontWeight: 700 },
  code: { background: '#f1f5f9', borderRadius: '4px', padding: '1px 6px', fontFamily: 'monospace', fontSize: '0.8rem' },
  form: {},
  formGrid: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '24px' },
  field: { display: 'flex', flexDirection: 'column', gap: '4px' },
  label: { fontSize: '0.875rem', fontWeight: 600, color: '#374151' },
  required: { color: '#dc2626' },
  optional: { fontSize: '0.75rem', color: '#9ca3af', fontWeight: 400 },
  input: {
    padding: '10px 14px', border: '1.5px solid #d1d5db', borderRadius: '8px',
    fontSize: '0.9rem', outline: 'none', transition: 'border-color 0.2s',
    fontFamily: 'inherit',
  },
  inputError: { borderColor: '#ef4444', background: '#fff5f5' },
  hint: { fontSize: '0.72rem', color: '#9ca3af', marginTop: '2px' },
  errorMsg: { fontSize: '0.78rem', color: '#dc2626', marginTop: '2px' },
  btn: {
    width: '100%', padding: '13px',
    background: 'linear-gradient(135deg, #2563eb, #1d4ed8)',
    color: '#fff', border: 'none', borderRadius: '10px',
    fontSize: '0.95rem', fontWeight: 600, cursor: 'pointer',
    transition: 'opacity 0.2s',
  },
  btnDisabled: { opacity: 0.65, cursor: 'not-allowed' },
}
