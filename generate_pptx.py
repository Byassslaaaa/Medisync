"""
Script generate presentasi MediSync dalam format PPTX.
Jalankan: python generate_pptx.py
Output  : MediSync-Presentasi.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import os

# ─── Konstanta Warna (konsisten dengan Frontend) ───
C_DARK_BLUE  = RGBColor(0x1E, 0x3A, 0x8A)   # #1e3a8a
C_BLUE       = RGBColor(0x25, 0x63, 0xEB)   # #2563eb
C_LIGHT_BLUE = RGBColor(0xDB, 0xEA, 0xFE)   # #dbeafe
C_GREEN      = RGBColor(0x16, 0xA3, 0x4A)   # #16a34a
C_LIGHT_GRN  = RGBColor(0xDC, 0xFC, 0xE7)   # #dcfce7
C_ORANGE     = RGBColor(0xD9, 0x77, 0x06)   # #d97706
C_LIGHT_ORG  = RGBColor(0xFE, 0xF3, 0xC7)   # #fef3c7
C_RED        = RGBColor(0xDC, 0x26, 0x26)   # #dc2626
C_LIGHT_RED  = RGBColor(0xFE, 0xE2, 0xE2)   # #fee2e2
C_PURPLE     = RGBColor(0x96, 0x73, 0xA6)   # #9673a6
C_LIGHT_PUR  = RGBColor(0xED, 0xE9, 0xFE)   # #ede9fe
C_WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
C_GRAY_100   = RGBColor(0xF3, 0xF4, 0xF6)
C_GRAY_500   = RGBColor(0x6B, 0x72, 0x80)
C_GRAY_700   = RGBColor(0x37, 0x41, 0x51)
C_DARK       = RGBColor(0x1A, 0x20, 0x2C)

W = Inches(13.33)  # widescreen 16:9
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

BLANK = prs.slide_layouts[6]  # layout kosong


# ══════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════

def add_rect(slide, x, y, w, h, fill=None, line=None, line_width=Pt(1)):
    shape = slide.shapes.add_shape(1, x, y, w, h)  # MSO_SHAPE_TYPE.RECTANGLE = 1
    shape.line.width = line_width
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line:
        shape.line.color.rgb = line
    else:
        shape.line.fill.background()
    return shape

def add_text(slide, text, x, y, w, h,
             size=16, bold=False, color=C_DARK, align=PP_ALIGN.LEFT,
             italic=False, wrap=True, valign=None):
    txBox = slide.shapes.add_textbox(x, y, w, h)
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox

def add_slide(title_text, subtitle_text=None, bg_color=C_WHITE):
    slide = prs.slides.add_slide(BLANK)
    # Background
    bg = add_rect(slide, 0, 0, W, H, fill=bg_color)
    return slide

def gradient_header(slide, h=Inches(1.4)):
    """Tambahkan header dengan warna biru gelap."""
    add_rect(slide, 0, 0, W, h, fill=C_DARK_BLUE)
    add_rect(slide, 0, 0, Inches(0.5), h, fill=C_BLUE)

def section_box(slide, x, y, w, h, title, body_lines,
                bg=C_LIGHT_BLUE, border=C_BLUE, title_color=C_DARK_BLUE):
    add_rect(slide, x, y, w, h, fill=bg, line=border, line_width=Pt(1.5))
    add_text(slide, title, x+Inches(0.15), y+Inches(0.08), w-Inches(0.3), Inches(0.35),
             size=12, bold=True, color=title_color)
    body = "\n".join(body_lines)
    add_text(slide, body, x+Inches(0.15), y+Inches(0.4), w-Inches(0.3), h-Inches(0.5),
             size=10, color=C_GRAY_700, wrap=True)

def footer_strip(slide, text="MediSync • Jaringan Komputer Terapan 2025/2026"):
    add_rect(slide, 0, H-Inches(0.35), W, Inches(0.35), fill=C_DARK_BLUE)
    add_text(slide, text, Inches(0.3), H-Inches(0.33), W-Inches(0.6), Inches(0.3),
             size=9, color=C_LIGHT_BLUE, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════
# SLIDE 1: HALAMAN JUDUL
# ══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)

# Background gradient biru
add_rect(slide, 0, 0, W, H, fill=C_DARK_BLUE)
add_rect(slide, 0, 0, W, Inches(0.08), fill=C_BLUE)
add_rect(slide, 0, H-Inches(0.08), W, Inches(0.08), fill=C_BLUE)

# Accent box kiri
add_rect(slide, 0, 0, Inches(0.6), H, fill=C_BLUE)

# Konten judul
add_text(slide, "🏥  MediSync",
         Inches(1), Inches(1.5), Inches(10), Inches(1.4),
         size=52, bold=True, color=C_WHITE, align=PP_ALIGN.LEFT)

add_text(slide, "Implementasi Komunikasi Microservices",
         Inches(1), Inches(2.9), Inches(10), Inches(0.7),
         size=22, bold=False, color=RGBColor(0x93, 0xC5, 0xFD), align=PP_ALIGN.LEFT)

add_text(slide, "Sistem Informasi Rumah Sakit berbasis gRPC & RabbitMQ",
         Inches(1), Inches(3.55), Inches(10), Inches(0.5),
         size=15, color=RGBColor(0xBF, 0xDB, 0xFE), align=PP_ALIGN.LEFT)

# Separator
add_rect(slide, Inches(1), Inches(4.2), Inches(8), Inches(0.04), fill=C_BLUE)

# Info
add_text(slide, "Mata Kuliah  :  Jaringan Komputer Terapan",
         Inches(1), Inches(4.4), Inches(6), Inches(0.4),
         size=13, color=C_WHITE, align=PP_ALIGN.LEFT)
add_text(slide, "Dosen          :  Danur Wijayanto, S.Kom. M.Cs.",
         Inches(1), Inches(4.8), Inches(6), Inches(0.4),
         size=13, color=C_WHITE, align=PP_ALIGN.LEFT)
add_text(slide, "Semester     :  Genap 2025/2026",
         Inches(1), Inches(5.2), Inches(6), Inches(0.4),
         size=13, color=C_WHITE, align=PP_ALIGN.LEFT)

# Anggota
add_rect(slide, Inches(8.5), Inches(1.5), Inches(4.2), Inches(4.2),
         fill=RGBColor(0x1E, 0x40, 0x9A), line=C_BLUE, line_width=Pt(1.5))
add_text(slide, "Anggota Kelompok",
         Inches(8.65), Inches(1.65), Inches(3.9), Inches(0.4),
         size=12, bold=True, color=RGBColor(0x7D, 0xD3, 0xFC), align=PP_ALIGN.LEFT)

members = [
    "1.  Irsyad Winarko",
    "     2311501038",
    "",
    "2.  Melati Ayu Salsabilla",
    "     2311501014",
    "",
    "3.  [Nama Anggota 3]",
    "     [NIM]",
    "",
    "4.  [Nama Anggota 4]",
    "     [NIM]",
    "",
    "5.  [Nama Anggota 5]",
    "     [NIM]",
]
add_text(slide, "\n".join(members),
         Inches(8.65), Inches(2.1), Inches(3.9), Inches(3.4),
         size=10, color=C_WHITE, align=PP_ALIGN.LEFT)


# ══════════════════════════════════════════════════════════
# SLIDE 2: PLO, INDIKATOR, CPMK
# ══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, W, H, fill=C_GRAY_100)
gradient_header(slide)

add_text(slide, "Pendukung Akademik", Inches(0.6), Inches(0.1), Inches(8), Inches(0.4),
         size=10, color=RGBColor(0x93, 0xC5, 0xFD))
add_text(slide, "PLO, Indikator, dan CPMK", Inches(0.6), Inches(0.45), Inches(10), Inches(0.55),
         size=24, bold=True, color=C_WHITE)

section_box(slide, Inches(0.4), Inches(1.55), Inches(4.0), Inches(2.2),
            "PLO 6",
            [
                "Mampu menganalisis dan",
                "menyelesaikan permasalahan",
                "jaringan dan keamanannya.",
            ],
            bg=C_LIGHT_BLUE, border=C_BLUE, title_color=C_DARK_BLUE)

section_box(slide, Inches(4.7), Inches(1.55), Inches(4.0), Inches(2.2),
            "Indikator-6-3",
            [
                "Mahasiswa mampu",
                "menyelesaikan permasalahan",
                "yang terjadi pada jaringan",
                "dengan solusi yang tepat.",
            ],
            bg=C_LIGHT_ORG, border=C_ORANGE, title_color=C_ORANGE)

section_box(slide, Inches(9.0), Inches(1.55), Inches(3.9), Inches(2.2),
            "CPMK-TIO6026-1",
            [
                "Merancang & mengimplementasikan",
                "solusi komunikasi data",
                "dengan socket tingkat lanjut,",
                "asynchronous messaging,",
                "dan microservices.",
            ],
            bg=C_LIGHT_PUR, border=C_PURPLE, title_color=C_PURPLE)

section_box(slide, Inches(0.4), Inches(4.0), Inches(12.5), Inches(2.3),
            "Keterkaitan Dengan Proyek MediSync",
            [
                "• Permasalahan utama: tight coupling antar layanan pendaftaran dan rekam medis.",
                "• Solusi: microservices + gRPC (real-time) + RabbitMQ (event-driven).",
                "• Hasil: layanan lebih tersedia, terpisah tanggung jawab, dan siap dikembangkan.",
                "• Pembuktian capaian: desain arsitektur, implementasi source code, dan demo alur end-to-end.",
            ],
            bg=C_LIGHT_GRN, border=C_GREEN, title_color=C_GREEN)

footer_strip(slide)


# ══════════════════════════════════════════════════════════
# SLIDE 2: LATAR BELAKANG
# ══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, W, H, fill=C_GRAY_100)
gradient_header(slide)

add_text(slide, "BAB 1 — PENDAHULUAN", Inches(0.6), Inches(0.1), Inches(8), Inches(0.4),
         size=10, color=RGBColor(0x93, 0xC5, 0xFD), bold=False)
add_text(slide, "Latar Belakang", Inches(0.6), Inches(0.45), Inches(10), Inches(0.55),
         size=24, bold=True, color=C_WHITE)

# Masalah box
section_box(slide, Inches(0.4), Inches(1.6), Inches(5.8), Inches(2.0),
            "⚠️  Masalah: Sistem Monolith",
            [
                "• Satu aplikasi besar → jika 1 bagian error, semua ikut down",
                "• Tight coupling: modul saling bergantung secara langsung",
                "• Bottleneck: semua traffic ke satu titik",
                "• Sulit di-update sebagian → harus restart semua",
                "• Tim besar sulit berkolaborasi pada 1 codebase",
            ],
            bg=C_LIGHT_RED, border=C_RED, title_color=C_RED)

# Solusi box
section_box(slide, Inches(6.5), Inches(1.6), Inches(6.4), Inches(2.0),
            "✅  Solusi: Arsitektur Microservices",
            [
                "• Setiap layanan berdiri mandiri, punya database sendiri",
                "• Failure isolation: 1 service down ≠ seluruh sistem down",
                "• Skalabilitas per-service: scale hanya yang perlu",
                "• Tim berbeda bisa mengerjakan service berbeda secara paralel",
                "• Komunikasi via gRPC (sync) & Message Queue (async)",
            ],
            bg=C_LIGHT_GRN, border=C_GREEN, title_color=C_GREEN)

# Konteks RS
section_box(slide, Inches(0.4), Inches(3.75), Inches(12.5), Inches(1.5),
            "🏥  Konteks: Sistem Informasi Rumah Sakit",
            [
                "RS modern memiliki banyak layanan: Pendaftaran, Rekam Medis, Apotek, Billing, dll.",
                "Kebutuhan: setiap layanan harus bisa dikembangkan dan di-deploy secara independen.",
                "Solusi: Microservices dengan komunikasi terstandarisasi menggunakan gRPC dan RabbitMQ.",
            ],
            bg=C_LIGHT_BLUE, border=C_BLUE, title_color=C_DARK_BLUE)

footer_strip(slide)


# ══════════════════════════════════════════════════════════
# SLIDE 3: RUMUSAN MASALAH & TUJUAN
# ══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, W, H, fill=C_GRAY_100)
gradient_header(slide)

add_text(slide, "BAB 1 — PENDAHULUAN", Inches(0.6), Inches(0.1), Inches(8), Inches(0.4),
         size=10, color=RGBColor(0x93, 0xC5, 0xFD))
add_text(slide, "Rumusan Masalah & Tujuan", Inches(0.6), Inches(0.45), Inches(10), Inches(0.55),
         size=24, bold=True, color=C_WHITE)

section_box(slide, Inches(0.4), Inches(1.6), Inches(5.8), Inches(3.5),
            "❓  Rumusan Masalah",
            [
                "1.  Bagaimana merancang sistem informasi RS yang",
                "     bebas dari tight coupling antar layanan?",
                "",
                "2.  Bagaimana mengimplementasikan komunikasi",
                "     synchronous real-time antar-service menggunakan gRPC?",
                "",
                "3.  Bagaimana menjamin pengiriman event antar-service",
                "     walaupun salah satu service sedang down?",
                "",
                "4.  Bagaimana memastikan database isolation",
                "     antar-service tetap terjaga?",
            ],
            bg=C_LIGHT_BLUE, border=C_BLUE, title_color=C_DARK_BLUE)

section_box(slide, Inches(6.5), Inches(1.6), Inches(6.4), Inches(3.5),
            "🎯  Tujuan",
            [
                "1.  Merancang arsitektur microservices untuk",
                "     sistem informasi RS sederhana",
                "",
                "2.  Mengimplementasikan gRPC sebagai mekanisme",
                "     komunikasi synchronous antar-service",
                "",
                "3.  Mengimplementasikan RabbitMQ sebagai message",
                "     broker untuk komunikasi asynchronous",
                "",
                "4.  Menerapkan prinsip database isolation:",
                "     setiap service memiliki database mandiri",
                "",
                "5.  Mendemokan sistem end-to-end yang berjalan",
            ],
            bg=C_LIGHT_GRN, border=C_GREEN, title_color=C_GREEN)

footer_strip(slide)


# ══════════════════════════════════════════════════════════
# SLIDE 4: TINJAUAN PUSTAKA — Microservices
# ══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, W, H, fill=C_GRAY_100)
gradient_header(slide)

add_text(slide, "BAB 2 — TINJAUAN PUSTAKA", Inches(0.6), Inches(0.1), Inches(8), Inches(0.4),
         size=10, color=RGBColor(0x93, 0xC5, 0xFD))
add_text(slide, "Microservices vs Monolith", Inches(0.6), Inches(0.45), Inches(10), Inches(0.55),
         size=24, bold=True, color=C_WHITE)

section_box(slide, Inches(0.4), Inches(1.55), Inches(5.8), Inches(2.2),
            "🧱  Monolith",
            [
                "• Satu codebase, satu proses, satu database",
                "• Semua modul saling terhubung langsung",
                "• Deploy = restart seluruh aplikasi",
                "• Scale = scale semua, meski hanya 1 bagian yang sibuk",
                "• Satu bug bisa crash keseluruhan sistem",
            ],
            bg=C_LIGHT_RED, border=C_RED, title_color=C_RED)

section_box(slide, Inches(6.5), Inches(1.55), Inches(6.4), Inches(2.2),
            "🔩  Microservices",
            [
                "• Banyak service kecil, masing-masing punya DB sendiri",
                "• Komunikasi via API/protokol jaringan",
                "• Deploy per-service, tidak perlu restart semua",
                "• Scale per-service sesuai kebutuhan",
                "• Failure isolation: 1 service error ≠ sistem mati",
            ],
            bg=C_LIGHT_GRN, border=C_GREEN, title_color=C_GREEN)

# Tabel perbandingan
add_rect(slide, Inches(0.4), Inches(3.9), Inches(12.5), Inches(0.35), fill=C_DARK_BLUE)
cols = ["Aspek", "Monolith", "Microservices"]
xs   = [Inches(0.4), Inches(3.5), Inches(7.8)]
ws   = [Inches(3.0), Inches(4.2), Inches(5.0)]
for i, (col, x, w) in enumerate(zip(cols, xs, ws)):
    add_text(slide, col, x+Inches(0.1), Inches(3.9), w, Inches(0.35),
             size=10, bold=True, color=C_WHITE)

rows = [
    ("Skalabilitas",    "Seluruh aplikasi",    "✓ Per-service"),
    ("Database",         "Satu, dibagi semua", "✓ Terpisah per-service"),
    ("Deploy",           "Semua sekaligus",     "✓ Independen"),
    ("Fault isolation",  "Tidak ada",           "✓ Ada"),
    ("Tim besar",        "Sulit, sering konflik","✓ Mudah dibagi"),
]
for ri, (asp, mono, micro) in enumerate(rows):
    y = Inches(4.25) + ri * Inches(0.42)
    bg_row = C_WHITE if ri % 2 == 0 else C_GRAY_100
    add_rect(slide, Inches(0.4), y, Inches(12.5), Inches(0.42), fill=bg_row, line=C_GRAY_100)
    for txt, x, w in zip([asp, mono, micro], xs, ws):
        clr = C_GREEN if txt.startswith("✓") else C_GRAY_700
        add_text(slide, txt, x+Inches(0.1), y+Inches(0.04), w, Inches(0.35), size=10, color=clr)

footer_strip(slide)


# ══════════════════════════════════════════════════════════
# SLIDE 5: TINJAUAN PUSTAKA — gRPC
# ══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, W, H, fill=C_GRAY_100)
gradient_header(slide)

add_text(slide, "BAB 2 — TINJAUAN PUSTAKA", Inches(0.6), Inches(0.1), Inches(8), Inches(0.4),
         size=10, color=RGBColor(0x93, 0xC5, 0xFD))
add_text(slide, "gRPC — Google Remote Procedure Call", Inches(0.6), Inches(0.45), Inches(10), Inches(0.55),
         size=24, bold=True, color=C_WHITE)

section_box(slide, Inches(0.4), Inches(1.55), Inches(6.0), Inches(2.5),
            "📖  Definisi & Cara Kerja",
            [
                "Framework komunikasi yang memungkinkan satu service",
                "memanggil fungsi di service lain seperti memanggil",
                "fungsi lokal (Remote Procedure Call).",
                "",
                "Cara kerja:",
                "1. Definisikan kontrak di file .proto",
                "2. Generate kode otomatis (stub/skeleton)",
                "3. Client memanggil method → dikirim via HTTP/2",
                "4. Server memproses → kembalikan response",
            ],
            bg=C_LIGHT_BLUE, border=C_BLUE, title_color=C_DARK_BLUE)

section_box(slide, Inches(6.7), Inches(1.55), Inches(6.0), Inches(2.5),
            "⚡  Keunggulan gRPC",
            [
                "• Protocol Buffers: data lebih kecil ~5x vs JSON",
                "• HTTP/2: multiplexing, header compression",
                "• Strongly-typed: schema ketat via .proto",
                "• Low latency: cocok untuk internal service comm.",
                "• Language-agnostic: support banyak bahasa",
                "• Contract-First: definisikan .proto sebelum code",
            ],
            bg=C_LIGHT_ORG, border=C_ORANGE, title_color=C_ORANGE)

# Proto example box
section_box(slide, Inches(0.4), Inches(4.2), Inches(5.8), Inches(2.5),
            "📄  Contoh file .proto (MediSync)",
            [
                'syntax = "proto3";',
                'package medicalrecord;',
                '',
                'service MedicalRecordService {',
                '  rpc CheckPatientRecord',
                '    (PatientRequest) returns (RecordResponse);',
                '}',
                'message PatientRequest { string nik = 1; }',
                'message RecordResponse {',
                '  bool has_record = 1;',
                '  string record_id = 2; }',
            ],
            bg=RGBColor(0xF8, 0xFA, 0xFC), border=C_GRAY_500, title_color=C_DARK_BLUE)

section_box(slide, Inches(6.7), Inches(4.2), Inches(6.0), Inches(2.5),
            "🎯  Kapan Pakai gRPC di MediSync?",
            [
                "Skenario: Service A perlu tahu APAKAH pasien sudah",
                "memiliki rekam medis SEBELUM mendaftarkan.",
                "",
                "→ Harus SYNCHRONOUS: Service A menunggu jawaban",
                "→ Jawaban dipakai untuk keputusan di step berikutnya",
                "",
                "Call: CheckPatientRecord(nik)",
                "Response: { has_record: bool, record_id: string }",
                "",
                "Jika has_record = true → tolak pendaftaran",
                "Jika has_record = false → lanjut proses",
            ],
            bg=C_LIGHT_GRN, border=C_GREEN, title_color=C_GREEN)

footer_strip(slide)


# ══════════════════════════════════════════════════════════
# SLIDE 6: TINJAUAN PUSTAKA — RabbitMQ
# ══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, W, H, fill=C_GRAY_100)
gradient_header(slide)

add_text(slide, "BAB 2 — TINJAUAN PUSTAKA", Inches(0.6), Inches(0.1), Inches(8), Inches(0.4),
         size=10, color=RGBColor(0x93, 0xC5, 0xFD))
add_text(slide, "Message Queue — RabbitMQ", Inches(0.6), Inches(0.45), Inches(10), Inches(0.55),
         size=24, bold=True, color=C_WHITE)

section_box(slide, Inches(0.4), Inches(1.55), Inches(6.0), Inches(2.4),
            "📖  Definisi & Konsep",
            [
                "Sistem antrian pesan yang memungkinkan service",
                "mengirim data tanpa harus menunggu penerima",
                "selesai memproses (fire and forget).",
                "",
                "Komponen utama:",
                "• Producer  → pengirim pesan (Service A)",
                "• Exchange  → router pesan ke queue yang tepat",
                "• Queue     → antrian penyimpanan pesan",
                "• Consumer  → penerima pesan (Service B)",
            ],
            bg=C_LIGHT_RED, border=C_RED, title_color=C_RED)

section_box(slide, Inches(6.7), Inches(1.55), Inches(6.0), Inches(2.4),
            "⚡  Keunggulan RabbitMQ",
            [
                "• Non-blocking: Service A tidak tunggu Service B",
                "• Guaranteed delivery: pesan aman di queue",
                "  meski consumer offline/restart",
                "• Decoupled: producer tidak tahu siapa consumer",
                "• Persistent message: tidak hilang jika broker restart",
                "• Scalable: bisa banyak consumer paralel",
                "• Acknowledgement: konfirmasi pesan sudah diproses",
            ],
            bg=C_LIGHT_PUR, border=C_PURPLE, title_color=C_PURPLE)

# Alur RabbitMQ visual
add_rect(slide, Inches(0.4), Inches(4.1), Inches(12.5), Inches(1.5),
         fill=C_WHITE, line=C_GRAY_100, line_width=Pt(1))

add_text(slide, "Alur MQ di MediSync:",
         Inches(0.6), Inches(4.15), Inches(12), Inches(0.35),
         size=11, bold=True, color=C_DARK_BLUE)

boxes = [
    (Inches(0.6),  "Service A\n(Producer)", C_LIGHT_GRN,  C_GREEN),
    (Inches(2.8),  "Exchange\nhospital", C_LIGHT_ORG, C_ORANGE),
    (Inches(5.0),  "Queue\npatient.queue", C_LIGHT_RED, C_RED),
    (Inches(7.2),  "Service B\n(Consumer)", C_LIGHT_PUR, C_PURPLE),
    (Inches(9.4),  "db_rekam_medis\n(INSERT draft)", C_LIGHT_BLUE, C_BLUE),
]
for bx, label, bg, border in boxes:
    add_rect(slide, bx, Inches(4.55), Inches(2.1), Inches(0.85), fill=bg, line=border, line_width=Pt(1.5))
    add_text(slide, label, bx+Inches(0.05), Inches(4.58), Inches(2.0), Inches(0.8),
             size=10, bold=True, color=border, align=PP_ALIGN.CENTER)

# Arrows
for ax in [Inches(2.72), Inches(4.92), Inches(7.12), Inches(9.32)]:
    add_text(slide, "→", ax, Inches(4.75), Inches(0.25), Inches(0.4),
             size=16, bold=True, color=C_GRAY_500, align=PP_ALIGN.CENTER)

section_box(slide, Inches(0.4), Inches(5.7), Inches(12.5), Inches(1.1),
            "🎯  Kapan Pakai RabbitMQ di MediSync?",
            [
                "Setelah pasien berhasil disimpan di db_pendaftaran, Service A publish event 'patient.registered' ke RabbitMQ.",
                "Service B consume event ini di background dan membuat draft rekam medis di db_rekam_medis.",
                "Service A TIDAK perlu menunggu Service B selesai → response ke user lebih cepat.",
            ],
            bg=C_LIGHT_RED, border=C_RED, title_color=C_RED)

footer_strip(slide)


# ══════════════════════════════════════════════════════════
# SLIDE 7: PEMILIHAN TEKNOLOGI
# ══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, W, H, fill=C_GRAY_100)
gradient_header(slide)

add_text(slide, "BAB 3 — ANALISIS & PERANCANGAN", Inches(0.6), Inches(0.1), Inches(9), Inches(0.4),
         size=10, color=RGBColor(0x93, 0xC5, 0xFD))
add_text(slide, "3.3 Pemilihan dan Justifikasi Teknologi", Inches(0.6), Inches(0.45), Inches(10), Inches(0.55),
         size=24, bold=True, color=C_WHITE)

add_text(slide, "3.3.1 Teknologi yang Dipilih • 3.3.2 Alasan Pemilihan (gRPC & Message Queue)",
         Inches(0.6), Inches(1.05), Inches(12), Inches(0.3),
         size=10, color=C_GRAY_500, italic=True)

techs = [
    ("⚡ Go + Gin",           C_LIGHT_GRN,  C_GREEN,   C_GREEN,
     ["• Goroutine: concurrency bawaan, ideal untuk microservices",
      "• Binary native: startup cepat, performa tinggi",
      "• gRPC paling 'native' di Go (dibuat Google)",
      "• Statically typed → error saat compile, bukan runtime",
      "• Gin: router HTTP ringan dan cepat"]),
    ("🗄️ PostgreSQL",         C_LIGHT_BLUE, C_BLUE,    C_DARK_BLUE,
     ["• Dua database terpisah: db_pendaftaran & db_rekam_medis",
      "• ACID compliance: konsistensi data terjamin",
      "• Satu jenis DB → tim tidak perlu belajar dua teknologi",
      "• Query powerful untuk data relasional pasien",
      "• Mature dan production-ready"]),
    ("🔗 gRPC",               C_LIGHT_ORG,  C_ORANGE,  C_ORANGE,
     ["• Protocol Buffers: efisien, strongly-typed",
      "• Contract-First via .proto: kontrak antar service jelas",
      "• HTTP/2: lebih efisien dari REST untuk internal call",
      "• Dipakai saat validasi real-time (sync) dibutuhkan",
      "• Go + gRPC: kombinasi paling umum di industri"]),
    ("📨 RabbitMQ",            C_LIGHT_RED,  C_RED,     C_RED,
     ["• Pesan aman di queue meski consumer offline",
      "• Decoupling sempurna: producer tidak tahu consumer",
      "• Persistent delivery: tidak hilang saat restart",
      "• Lebih simpel dari Kafka untuk skala proyek ini",
      "• Management UI: mudah monitor queue"]),
    ("🐳 Docker Compose",     C_LIGHT_PUR,  C_PURPLE,  C_PURPLE,
     ["• Satu perintah: docker-compose up --build",
      "• Setiap service dalam container terisolasi",
      "• Network internal antar container otomatis",
      "• Mudah dijalankan di laptop manapun tanpa install manual",
      "• Health check: service saling menunggu dengan benar"]),
]

cols_per_row = 3
for i, (name, bg, border, tc, pts) in enumerate(techs):
    row = i // cols_per_row
    col = i % cols_per_row
    x = Inches(0.35) + col * Inches(4.35)
    y = Inches(1.55) + row * Inches(2.65)
    w = Inches(4.15)
    h = Inches(2.5)
    section_box(slide, x, y, w, h, name, pts, bg=bg, border=border, title_color=tc)

footer_strip(slide)


# ══════════════════════════════════════════════════════════
# SLIDE 8: ARSITEKTUR SISTEM
# ══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, W, H, fill=C_GRAY_100)
gradient_header(slide)

add_text(slide, "BAB 3 — ANALISIS & PERANCANGAN", Inches(0.6), Inches(0.1), Inches(9), Inches(0.4),
         size=10, color=RGBColor(0x93, 0xC5, 0xFD))
add_text(slide, "3.4 Arsitektur Sistem Berbasis Teknologi Terpilih", Inches(0.6), Inches(0.45), Inches(11), Inches(0.55),
         size=24, bold=True, color=C_WHITE)

# Docker network boundary
add_rect(slide, Inches(0.3), Inches(1.5), Inches(12.7), Inches(5.2),
         fill=RGBColor(0xF8, 0xFA, 0xFF), line=C_BLUE, line_width=Pt(1.5))
add_text(slide, "Docker Network: medisync-net",
         Inches(0.4), Inches(1.5), Inches(4), Inches(0.3),
         size=9, color=C_BLUE, italic=True)

# Frontend
add_rect(slide, Inches(4.8), Inches(1.75), Inches(3.6), Inches(0.85),
         fill=C_LIGHT_BLUE, line=C_BLUE, line_width=Pt(2))
add_text(slide, "FRONTEND\nReact + Vite  |  Port 3000",
         Inches(4.9), Inches(1.8), Inches(3.4), Inches(0.75),
         size=11, bold=True, color=C_DARK_BLUE, align=PP_ALIGN.CENTER)

# Arrow FE → SA
add_text(slide, "REST API\nHTTP POST/GET",
         Inches(2.5), Inches(2.5), Inches(2.3), Inches(0.5),
         size=9, color=C_BLUE, italic=True, align=PP_ALIGN.CENTER)

# Service A
add_rect(slide, Inches(0.5), Inches(3.2), Inches(4.8), Inches(1.6),
         fill=C_LIGHT_GRN, line=C_GREEN, line_width=Pt(2))
add_text(slide, "SERVICE A — Pendaftaran\nGo + Gin  |  Port 4001",
         Inches(0.6), Inches(3.25), Inches(4.6), Inches(0.45),
         size=11, bold=True, color=C_GREEN)

for lbl, xb in [("REST Handler", Inches(0.6)), ("gRPC Client", Inches(2.0)), ("MQ Producer", Inches(3.4))]:
    add_rect(slide, xb, Inches(3.75), Inches(1.25), Inches(0.45),
             fill=C_WHITE, line=C_GREEN, line_width=Pt(1))
    add_text(slide, lbl, xb+Inches(0.05), Inches(3.78), Inches(1.15), Inches(0.38),
             size=9, color=C_GREEN, align=PP_ALIGN.CENTER)

# db_pendaftaran
add_rect(slide, Inches(0.5), Inches(5.1), Inches(2.5), Inches(0.95),
         fill=C_LIGHT_GRN, line=C_GREEN, line_width=Pt(1.5))
add_text(slide, "PostgreSQL\ndb_pendaftaran\ntabel: patients",
         Inches(0.55), Inches(5.15), Inches(2.4), Inches(0.85),
         size=9, color=C_GREEN, align=PP_ALIGN.CENTER, bold=True)

# Service B
add_rect(slide, Inches(7.9), Inches(3.2), Inches(4.8), Inches(1.6),
         fill=C_LIGHT_PUR, line=C_PURPLE, line_width=Pt(2))
add_text(slide, "SERVICE B — Rekam Medis\nGo + Gin  |  Port 4002  |  gRPC Port 50052",
         Inches(8.0), Inches(3.25), Inches(4.6), Inches(0.45),
         size=11, bold=True, color=C_PURPLE)

for lbl, xb in [("gRPC Server", Inches(8.0)), ("MQ Consumer", Inches(9.4)), ("REST Handler", Inches(10.8))]:
    add_rect(slide, xb, Inches(3.75), Inches(1.25), Inches(0.45),
             fill=C_WHITE, line=C_PURPLE, line_width=Pt(1))
    add_text(slide, lbl, xb+Inches(0.05), Inches(3.78), Inches(1.15), Inches(0.38),
             size=9, color=C_PURPLE, align=PP_ALIGN.CENTER)

# db_rekam_medis
add_rect(slide, Inches(10.1), Inches(5.1), Inches(2.6), Inches(0.95),
         fill=C_LIGHT_PUR, line=C_PURPLE, line_width=Pt(1.5))
add_text(slide, "PostgreSQL\ndb_rekam_medis\ntabel: medical_records",
         Inches(10.15), Inches(5.15), Inches(2.5), Inches(0.85),
         size=9, color=C_PURPLE, align=PP_ALIGN.CENTER, bold=True)

# RabbitMQ
add_rect(slide, Inches(5.5), Inches(3.5), Inches(2.2), Inches(1.3),
         fill=C_LIGHT_RED, line=C_RED, line_width=Pt(2))
add_text(slide, "RabbitMQ\nPort 5672\nQueue: patient.queue",
         Inches(5.55), Inches(3.55), Inches(2.1), Inches(1.2),
         size=10, bold=True, color=C_RED, align=PP_ALIGN.CENTER)

# Labels arrows
add_text(slide, "gRPC\n(Sync)", Inches(5.45), Inches(2.75), Inches(2.3), Inches(0.55),
         size=9, bold=True, color=C_ORANGE, align=PP_ALIGN.CENTER)
add_text(slide, "Publish\n(Async)", Inches(5.5), Inches(4.9), Inches(1.5), Inches(0.45),
         size=9, bold=True, color=C_RED, align=PP_ALIGN.CENTER)
add_text(slide, "Consume\n(Async)", Inches(7.6), Inches(4.9), Inches(1.5), Inches(0.45),
         size=9, bold=True, color=C_RED, align=PP_ALIGN.CENTER)

footer_strip(slide)


# ══════════════════════════════════════════════════════════
# SLIDE 9: ALUR DATA
# ══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, W, H, fill=C_GRAY_100)
gradient_header(slide)

add_text(slide, "BAB 3 — ANALISIS & PERANCANGAN", Inches(0.6), Inches(0.1), Inches(9), Inches(0.4),
         size=10, color=RGBColor(0x93, 0xC5, 0xFD))
add_text(slide, "Alur Data — Pendaftaran Pasien Baru", Inches(0.6), Inches(0.45), Inches(10), Inches(0.55),
         size=24, bold=True, color=C_WHITE)

steps = [
    (C_BLUE,   C_LIGHT_BLUE, "1",
     "User Isi Form",
     "User input Nama, NIK, Tanggal Lahir di Frontend React dan klik tombol 'Daftarkan Pasien'."),
    (C_BLUE,   C_LIGHT_BLUE, "2",
     "POST /api/patients",
     "Frontend kirim HTTP POST ke Service A (port 4001). Payload JSON berisi data pasien."),
    (C_ORANGE, C_LIGHT_ORG,  "3",
     "gRPC: CheckPatientRecord(nik) — SYNC",
     "Service A memanggil Service B via gRPC. Service A MENUNGGU respons sebelum lanjut."),
    (C_ORANGE, C_LIGHT_ORG,  "4",
     "gRPC Response: {has_record: false}",
     "Service B query db_rekam_medis. Jika pasien baru → has_record=false → lanjut. Jika sudah ada → tolak."),
    (C_GREEN,  C_LIGHT_GRN,  "5",
     "INSERT ke db_pendaftaran",
     "Service A simpan data pasien ke tabel patients di db_pendaftaran (PostgreSQL)."),
    (C_RED,    C_LIGHT_RED,  "6",
     "Publish Event — ASYNC",
     "Service A publish event 'patient.registered' ke RabbitMQ. TIDAK menunggu Service B."),
    (C_BLUE,   C_LIGHT_BLUE, "7",
     "Response 201 ke Frontend",
     "Service A return {success: true, patient_id: '...'} ke Frontend. User lihat konfirmasi."),
    (C_RED,    C_LIGHT_RED,  "8",
     "Service B Consume Event (Background)",
     "Service B consume event dari queue → INSERT draft rekam medis ke db_rekam_medis secara background."),
]

col_w = Inches(3.1)
for i, (border, bg, num, title, desc) in enumerate(steps):
    row = i // 4
    col = i % 4
    x = Inches(0.3) + col * Inches(3.25)
    y = Inches(1.55) + row * Inches(2.5)
    add_rect(slide, x, y, col_w, Inches(2.35), fill=bg, line=border, line_width=Pt(1.5))
    add_rect(slide, x, y, Inches(0.45), Inches(0.45), fill=border)
    add_text(slide, num, x, y+Inches(0.03), Inches(0.45), Inches(0.38),
             size=14, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, title, x+Inches(0.5), y+Inches(0.05), col_w-Inches(0.6), Inches(0.5),
             size=10, bold=True, color=border)
    add_text(slide, desc, x+Inches(0.1), y+Inches(0.6), col_w-Inches(0.2), Inches(1.6),
             size=9, color=C_GRAY_700, wrap=True)

footer_strip(slide)


# ══════════════════════════════════════════════════════════
# SLIDE 10: DEPLOYMENT
# ══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, W, H, fill=C_GRAY_100)
gradient_header(slide)

add_text(slide, "BAB 4 — TEKNIK DEPLOYMENT", Inches(0.6), Inches(0.1), Inches(9), Inches(0.4),
         size=10, color=RGBColor(0x93, 0xC5, 0xFD))
add_text(slide, "Docker + Docker Compose", Inches(0.6), Inches(0.45), Inches(10), Inches(0.55),
         size=24, bold=True, color=C_WHITE)

section_box(slide, Inches(0.4), Inches(1.55), Inches(5.5), Inches(2.5),
            "🐳  Mengapa Docker Compose?",
            [
                "• Setiap service berjalan di container terisolasi",
                "• Satu perintah menjalankan semua service:",
                "  $ docker-compose up --build",
                "• Tidak perlu install PostgreSQL/RabbitMQ manual",
                "• Portabel: jalan di laptop manapun",
                "• Health check: service menunggu dependency siap",
                "• Internal network: service saling connect by name",
                "• Environment variable untuk konfigurasi dinamis",
            ],
            bg=C_LIGHT_BLUE, border=C_BLUE, title_color=C_DARK_BLUE)

section_box(slide, Inches(6.2), Inches(1.55), Inches(6.7), Inches(2.5),
            "📦  Container yang Berjalan",
            [
                "┌─────────────────────────────────────────────┐",
                "│  medisync-postgres    Port: 5432            │",
                "│  medisync-rabbitmq    Port: 5672, 15672     │",
                "│  medisync-service-b   Port: 4002, 50052     │",
                "│  medisync-service-a   Port: 4001            │",
                "│  medisync-frontend    Port: 3000            │",
                "└─────────────────────────────────────────────┘",
                "Semua terhubung dalam network: medisync-net",
            ],
            bg=RGBColor(0xF0, 0xF9, 0xFF), border=C_BLUE, title_color=C_DARK_BLUE)

section_box(slide, Inches(0.4), Inches(4.2), Inches(5.5), Inches(2.55),
            "🔧  Multi-Stage Build (Go services)",
            [
                "Stage 1 — Builder:",
                "  FROM golang:1.21-alpine",
                "  → Compile Go binary",
                "",
                "Stage 2 — Runner:",
                "  FROM alpine:3.19 (image ~5MB)",
                "  → Copy binary saja, tidak ada source code",
                "",
                "Hasilnya: image sangat kecil + aman",
            ],
            bg=C_LIGHT_GRN, border=C_GREEN, title_color=C_GREEN)

section_box(slide, Inches(6.2), Inches(4.2), Inches(6.7), Inches(2.55),
            "🌐  Akses Setelah Running",
            [
                "Frontend (React)   : http://localhost:3000",
                "Service A REST     : http://localhost:4001",
                "  - POST /api/patients",
                "  - GET  /api/patients",
                "Service B REST     : http://localhost:4002",
                "  - GET  /api/records",
                "  - GET  /api/records/:nik",
                "RabbitMQ UI        : http://localhost:15672",
                "  user: guest | pass: guest",
            ],
            bg=C_LIGHT_ORG, border=C_ORANGE, title_color=C_ORANGE)

footer_strip(slide)


# ══════════════════════════════════════════════════════════
# SLIDE 11: BUKTI AI
# ══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, W, H, fill=C_GRAY_100)
gradient_header(slide)

add_text(slide, "BAB 5 — BUKTI PENGGUNAAN AI", Inches(0.6), Inches(0.1), Inches(9), Inches(0.4),
         size=10, color=RGBColor(0x93, 0xC5, 0xFD))
add_text(slide, "Platform AI, Prompt & Library yang Digunakan", Inches(0.6), Inches(0.45), Inches(10), Inches(0.55),
         size=24, bold=True, color=C_WHITE)

section_box(slide, Inches(0.4), Inches(1.55), Inches(4.2), Inches(2.2),
            "🤖  Platform AI",
            [
                "Vibe Code di VSCode",
                "(asisten coding berbasis AI)",
                "",
                "Platform pendukung:",
                "• GitHub Copilot Chat",
                "• Model: GPT-5.3-Codex",
                "",
                "Tugas AI dalam proyek ini:",
                "• Perancangan arsitektur microservices",
                "• Implementasi gRPC + RabbitMQ",
                "• Setup Docker Compose",
            ],
            bg=C_LIGHT_BLUE, border=C_BLUE, title_color=C_DARK_BLUE)

section_box(slide, Inches(4.8), Inches(1.55), Inches(8.1), Inches(2.2),
            "💬  Contoh Prompt yang Digunakan",
            [
                '"Buatkan implementasi microservices Go + Gin dengan:',
                ' - Service A (pendaftaran) + PostgreSQL db_pendaftaran',
                ' - Service B (rekam medis) + PostgreSQL db_rekam_medis',
                ' - gRPC untuk CheckPatientRecord (synchronous)',
                ' - RabbitMQ untuk event patient.registered (async)',
                ' - Docker Compose untuk semua service',
                ' - Wajib contract-first .proto',
                ' Pastikan database isolation antar-service."',
            ],
            bg=C_LIGHT_ORG, border=C_ORANGE, title_color=C_ORANGE)

section_box(slide, Inches(0.4), Inches(3.9), Inches(6.0), Inches(2.7),
            "📦  Library & Package yang Digunakan",
            [
                "Go (Service A & B):",
                "  • github.com/gin-gonic/gin         → HTTP framework",
                "  • github.com/gin-contrib/cors      → CORS middleware",
                "  • github.com/lib/pq                → PostgreSQL driver",
                "  • github.com/rabbitmq/amqp091-go   → RabbitMQ client",
                "  • google.golang.org/grpc            → gRPC framework",
                "  • google.golang.org/protobuf        → Protocol Buffers",
                "  • github.com/google/uuid            → UUID generator",
                "",
                "Frontend (React):",
                "  • axios          → HTTP client",
                "  • react, react-dom, vite → UI framework",
            ],
            bg=C_LIGHT_GRN, border=C_GREEN, title_color=C_GREEN)

section_box(slide, Inches(6.7), Inches(3.9), Inches(6.2), Inches(2.7),
            "🔍  Bagian yang Dibantu AI",
            [
                "✓ Perancangan arsitektur & database isolation",
                "✓ File .proto (contract gRPC)",
                "✓ Implementasi gRPC server/client Go",
                "✓ RabbitMQ producer/consumer Go",
                "✓ Retry logic untuk koneksi saat startup",
                "✓ Docker Compose multi-container dengan healthcheck",
                "✓ Frontend React komponen form & tabel",
                "✓ Multi-stage Dockerfile untuk Go",
                "✓ Materi presentasi & diagram arsitektur",
            ],
            bg=C_LIGHT_PUR, border=C_PURPLE, title_color=C_PURPLE)

footer_strip(slide)


# ══════════════════════════════════════════════════════════
# SLIDE 12: PENUTUP / KESIMPULAN
# ══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, W, H, fill=C_DARK_BLUE)
add_rect(slide, 0, 0, Inches(0.6), H, fill=C_BLUE)
add_rect(slide, 0, 0, W, Inches(0.08), fill=C_BLUE)
add_rect(slide, 0, H-Inches(0.08), W, Inches(0.08), fill=C_BLUE)

add_text(slide, "Kesimpulan", Inches(1), Inches(0.8), Inches(10), Inches(0.7),
         size=32, bold=True, color=C_WHITE)

add_rect(slide, Inches(1), Inches(1.55), Inches(11), Inches(0.04), fill=C_BLUE)

points = [
    ("✓", "Arsitektur microservices berhasil memisahkan layanan Pendaftaran dan Rekam Medis dengan database masing-masing yang benar-benar terisolasi."),
    ("✓", "gRPC digunakan untuk validasi real-time (synchronous): Service A memanggil CheckPatientRecord sebelum mendaftarkan pasien baru."),
    ("✓", "RabbitMQ digunakan untuk event-driven (asynchronous): event patient.registered dikirim tanpa memblok response ke user."),
    ("✓", "Docker Compose mengorkestrasi semua service (Frontend, Service A, Service B, PostgreSQL, RabbitMQ) dalam satu network terisolasi."),
    ("✓", "Sistem dapat dijalankan dengan satu perintah: docker-compose up --build"),
]

for i, (icon, text) in enumerate(points):
    y = Inches(1.7) + i * Inches(0.95)
    add_rect(slide, Inches(1), y, Inches(0.5), Inches(0.55), fill=C_BLUE)
    add_text(slide, icon, Inches(1), y+Inches(0.05), Inches(0.5), Inches(0.45),
             size=16, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, text, Inches(1.65), y+Inches(0.05), Inches(10.5), Inches(0.55),
             size=13, color=RGBColor(0xBF, 0xDB, 0xFE), wrap=True)

add_text(slide, "🏥  MediSync  —  Terima Kasih",
         Inches(1), Inches(6.5), Inches(11.3), Inches(0.65),
         size=20, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

# ── Save ──────────────────────────────────────────────────
output_path = os.path.join(os.path.dirname(__file__), "MediSync-Presentasi.pptx")
prs.save(output_path)
print(f"\n[OK] File PPTX berhasil dibuat: {output_path}")
print(f"     Total slide: {len(prs.slides)}")
print("\nDaftar slide:")
for i, s in enumerate(prs.slides, 1):
    print(f"  Slide {i:2d}")
