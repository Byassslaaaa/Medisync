import { useState } from 'react'
import axios from 'axios'
import { IconEdit, IconZap, IconDatabase, IconSend, IconUser, IconCard, IconCalendar, IconPhone, IconCheck, IconX } from './icons'

export default function PatientForm({ serviceAUrl, onSuccess, loading, setLoading }) {
  const [form, setForm]     = useState({ name: '', nik: '', tanggal_lahir: '', no_telepon: '' })
  const [result, setResult] = useState(null)
  const [errors, setErrors] = useState({})

  const validate = () => {
    const e = {}
    if (!form.name.trim())            e.name = 'Nama wajib diisi.'
    if (!form.nik.trim())             e.nik  = 'NIK wajib diisi.'
    else if (form.nik.length !== 16)  e.nik  = 'NIK harus 16 digit.'
    else if (!/^\d+$/.test(form.nik)) e.nik  = 'NIK hanya boleh angka.'
    if (!form.tanggal_lahir)          e.tanggal_lahir = 'Tanggal lahir wajib diisi.'
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
    if (Object.keys(validationErrors).length > 0) { setErrors(validationErrors); return }
    setLoading(true)
    try {
      const res = await axios.post(`${serviceAUrl}/api/patients`, form)
      setResult({ type: 'success', message: res.data.message, data: res.data.data })
      setForm({ name: '', nik: '', tanggal_lahir: '', no_telepon: '' })
      setErrors({})
      setTimeout(onSuccess, 1500)
    } catch (err) {
      setResult({ type: 'error', message: err.response?.data?.message || 'Terjadi kesalahan. Coba lagi.' })
    } finally {
      setLoading(false)
    }
  }

  const flowSteps = [
    { icon: <IconEdit size={14} />,     label: 'Input Form',      style: s.pill1 },
    { icon: <IconZap size={14} />,      label: 'gRPC Check',      style: s.pill2 },
    { icon: <IconDatabase size={14} />, label: 'Simpan DB',       style: s.pill3 },
    { icon: <IconSend size={14} />,     label: 'RabbitMQ Event',  style: s.pill4 },
  ]

  return (
    <div>
      <div style={s.header}>
        <h2 style={s.title}>Pendaftaran Pasien Baru</h2>
      </div>

      {/* Flow Indicator */}
      <div className="flow-bar" style={s.flowBar}>
        {flowSteps.map((step, i) => (
          <span key={step.label} style={{ display: 'contents' }}>
            <div style={{ ...s.flowPill, ...step.style }}>
              {step.icon}
              <span>{step.label}</span>
            </div>
            {i < flowSteps.length - 1 && <span style={s.flowConnector}>—</span>}
          </span>
        ))}
      </div>

      {/* Alert */}
      {result && (
        <div className="alert-enter" style={result.type === 'success' ? s.alertSuccess : s.alertError}>
          <span style={s.alertIcon}>
            {result.type === 'success'
              ? <IconCheck size={16} />
              : <IconX size={16} />}
          </span>
          <div>
            <strong>{result.type === 'success' ? 'Berhasil!' : 'Gagal!'}</strong>
            <p style={{ margin: '4px 0 0', fontSize: '0.875rem' }}>{result.message}</p>
            {result.data && (
              <p style={{ margin: '4px 0 0', fontSize: '0.8rem', opacity: 0.75 }}>
                Patient ID: <code style={s.code}>{result.data.patient_id}</code>
              </p>
            )}
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-grid" style={s.formGrid}>

          <div style={s.field}>
            <label style={s.label}>Nama Lengkap <span style={s.required}>*</span></label>
            <div style={s.inputWrapper}>
              <span style={s.inputIcon}><IconUser size={14} /></span>
              <input name="name" value={form.name} onChange={handleChange}
                placeholder="cth: Budi Santoso"
                style={errors.name ? { ...s.input, ...s.inputError } : s.input} />
            </div>
            {errors.name && <span style={s.errorMsg}>{errors.name}</span>}
          </div>

          <div style={s.field}>
            <label style={s.label}>NIK <span style={s.required}>*</span></label>
            <div style={s.inputWrapper}>
              <span style={s.inputIcon}><IconCard size={14} /></span>
              <input name="nik" value={form.nik} onChange={handleChange}
                placeholder="16 digit NIK" maxLength={16}
                style={errors.nik ? { ...s.input, ...s.inputError } : s.input} />
            </div>
            <span style={s.hint}>{form.nik.length}/16 digit</span>
            {errors.nik && <span style={s.errorMsg}>{errors.nik}</span>}
          </div>

          <div style={s.field}>
            <label style={s.label}>Tanggal Lahir <span style={s.required}>*</span></label>
            <div style={s.inputWrapper}>
              <span style={s.inputIcon}><IconCalendar size={14} /></span>
              <input type="date" name="tanggal_lahir" value={form.tanggal_lahir} onChange={handleChange}
                style={errors.tanggal_lahir ? { ...s.input, ...s.inputError } : s.input} />
            </div>
            {errors.tanggal_lahir && <span style={s.errorMsg}>{errors.tanggal_lahir}</span>}
          </div>

          <div style={s.field}>
            <label style={s.label}>No. Telepon <span style={s.optional}>(opsional)</span></label>
            <div style={s.inputWrapper}>
              <span style={s.inputIcon}><IconPhone size={14} /></span>
              <input name="no_telepon" value={form.no_telepon} onChange={handleChange}
                placeholder="cth: 08123456789" style={s.input} />
            </div>
          </div>

        </div>

        <button type="submit" disabled={loading} style={loading ? { ...s.btn, ...s.btnDisabled } : s.btn}>
          <IconCheck size={15} />
          {loading ? 'Memproses...' : 'Daftarkan Pasien Baru'}
        </button>
      </form>
    </div>
  )
}

const dark = (a) => `rgba(12,12,18,${a})`
const white = (a) => `rgba(255,255,255,${a})`

const s = {
  header: { marginBottom: '20px' },
  title: {
    fontSize: '1.35rem', fontWeight: 700,
    color: 'rgba(15,15,20,0.85)', letterSpacing: '-0.3px',
    textShadow: `0 1px 3px ${white(0.6)}`,
  },

  flowBar: { display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '28px', flexWrap: 'wrap' },
  flowPill: {
    display: 'flex', alignItems: 'center', gap: '7px',
    padding: '8px 15px', borderRadius: '999px',
    fontWeight: 600, fontSize: '0.80rem', letterSpacing: '0.01em',
    backdropFilter: 'blur(12px)', WebkitBackdropFilter: 'blur(12px)',
    border: `1px solid ${white(0.15)}`,
    boxShadow: `inset 0 1px 0 ${white(0.2)}, 0 2px 8px rgba(0,0,0,0.16)`,
  },
  pill1: { background: dark(0.75), color: white(0.90) },
  pill2: { background: dark(0.58), color: white(0.85) },
  pill3: { background: dark(0.42), color: white(0.80) },
  pill4: { background: dark(0.42), color: white(0.80) },
  flowConnector: { color: 'rgba(15,15,20,0.20)', fontSize: '1.1rem', flexShrink: 0 },

  alertSuccess: {
    display: 'flex', gap: '12px', alignItems: 'flex-start',
    background: white(0.55), backdropFilter: 'blur(12px)', WebkitBackdropFilter: 'blur(12px)',
    border: `1px solid ${white(0.70)}`,
    borderRadius: '12px', padding: '14px 16px', marginBottom: '20px', color: 'rgba(15,15,20,0.85)',
    boxShadow: `inset 0 1px 0 ${white(0.8)}`,
  },
  alertError: {
    display: 'flex', gap: '12px', alignItems: 'flex-start',
    background: 'rgba(255,248,248,0.60)', backdropFilter: 'blur(12px)', WebkitBackdropFilter: 'blur(12px)',
    border: '1px solid rgba(200,160,160,0.50)',
    borderRadius: '12px', padding: '14px 16px', marginBottom: '20px', color: 'rgba(100,20,20,0.85)',
    boxShadow: `inset 0 1px 0 ${white(0.7)}`,
  },
  alertIcon: { display: 'flex', alignItems: 'center', marginTop: '1px' },
  code: { background: 'rgba(0,0,0,0.08)', borderRadius: '4px', padding: '1px 6px', fontFamily: 'monospace', fontSize: '0.8rem' },

  formGrid: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '24px' },
  field: { display: 'flex', flexDirection: 'column', gap: '5px' },
  label: { fontSize: '0.82rem', fontWeight: 700, color: 'rgba(15,15,20,0.82)', letterSpacing: '0.01em' },
  required: { color: 'rgba(15,15,20,0.50)', fontWeight: 400 },
  optional: { fontSize: '0.73rem', color: 'rgba(15,15,20,0.40)', fontWeight: 400 },

  inputWrapper: { position: 'relative', display: 'flex', alignItems: 'center' },
  inputIcon: {
    position: 'absolute', left: '12px',
    display: 'flex', alignItems: 'center',
    color: 'rgba(15,15,20,0.38)', pointerEvents: 'none', zIndex: 1,
  },
  input: {
    width: '100%', padding: '10px 14px 10px 38px',
    background: white(0.75), backdropFilter: 'blur(16px)', WebkitBackdropFilter: 'blur(16px)',
    border: `1px solid ${white(0.90)}`,
    borderRadius: '10px', fontSize: '0.88rem', outline: 'none',
    color: 'rgba(15,15,20,0.88)', fontFamily: 'inherit', boxSizing: 'border-box',
    boxShadow: `0 1px 4px rgba(0,0,0,0.08), inset 0 1px 2px ${white(0.8)}`,
  },
  inputError: { borderColor: 'rgba(200,80,80,0.55)', background: 'rgba(255,245,245,0.80)' },
  hint: { fontSize: '0.70rem', color: 'rgba(15,15,20,0.50)' },
  errorMsg: { fontSize: '0.75rem', color: 'rgba(140,30,30,0.90)', fontWeight: 500 },

  btn: {
    width: '100%', padding: '12px',
    display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
    background: dark(0.75), backdropFilter: 'blur(16px)', WebkitBackdropFilter: 'blur(16px)',
    border: `1px solid ${white(0.14)}`,
    borderRadius: '12px', color: white(0.92),
    fontSize: '0.92rem', fontWeight: 600, cursor: 'pointer', letterSpacing: '0.02em',
    boxShadow: `inset 0 1px 0 ${white(0.12)}, 0 4px 16px rgba(0,0,0,0.18)`,
  },
  btnDisabled: { opacity: 0.5, cursor: 'not-allowed' },
}
