"""
MediSync — Generator Otomatis:
  1. LAPORAN_MEDISYNC.docx   (Word penuh)
  2. MediSync-Diagram-BW.drawio (hitam-putih)
  3. MediSync-Presentasi-NEW.pptx (PPT diperbaiki)
"""

import re, copy, sys
from pathlib import Path

BASE = Path(__file__).parent

# ─────────────────────────────────────────────────────────────────
# 0. HELPERS — python-docx
# ─────────────────────────────────────────────────────────────────
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import docx.oxml

def set_font(run, name="Times New Roman", size=12, bold=False,
             italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)

def add_heading(doc, text, level, font_size, bold=True, center=False, space_before=12, space_after=6):
    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(space_before)
    para.paragraph_format.space_after  = Pt(space_after)
    if center:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(text)
    set_font(run, size=font_size, bold=bold)
    return para

def add_body(doc, text, justify=True, size=12, space_before=0, space_after=6):
    para = doc.add_paragraph()
    if justify:
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    para.paragraph_format.space_before = Pt(space_before)
    para.paragraph_format.space_after  = Pt(space_after)
    para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    run = para.add_run(text)
    set_font(run, size=size)
    return para

def add_bullet(doc, text, size=12):
    para = doc.add_paragraph(style="List Bullet")
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    para.paragraph_format.space_after = Pt(3)
    para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    run = para.add_run(text)
    set_font(run, size=size)
    return para

def add_code(doc, text):
    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(4)
    para.paragraph_format.space_after  = Pt(4)
    run = para.add_run(text)
    set_font(run, name="Courier New", size=9, bold=False)
    # light gray shading
    pPr = para._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "F2F2F2")
    pPr.append(shd)
    return para

def add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1+len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        for run in hdr_cells[i].paragraphs[0].runs:
            set_font(run, size=11, bold=True)
        # header background
        tc = hdr_cells[i]._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), "2C2C2C")
        tcPr.append(shd)
        for para in hdr_cells[i].paragraphs:
            for run in para.runs:
                run.font.color.rgb = RGBColor(255,255,255)

    for ri, row_data in enumerate(rows):
        row_cells = table.rows[ri+1].cells
        for ci, val in enumerate(row_data):
            row_cells[ci].text = str(val)
            for run in row_cells[ci].paragraphs[0].runs:
                set_font(run, size=11)
        if ri % 2 == 1:
            for ci in range(len(row_data)):
                tc = table.rows[ri+1].cells[ci]._tc
                tcPr = tc.get_or_add_tcPr()
                shd = OxmlElement("w:shd")
                shd.set(qn("w:val"), "clear")
                shd.set(qn("w:color"), "auto")
                shd.set(qn("w:fill"), "F5F5F5")
                tcPr.append(shd)

    if col_widths:
        for ri, row in enumerate(table.rows):
            for ci, cell in enumerate(row.cells):
                cell.width = Inches(col_widths[ci])
    return table


def page_break(doc):
    doc.add_page_break()


def set_margins(doc, top=2.5, bottom=2.5, left=3.0, right=2.5):
    for section in doc.sections:
        section.top_margin    = Cm(top)
        section.bottom_margin = Cm(bottom)
        section.left_margin   = Cm(left)
        section.right_margin  = Cm(right)


# ─────────────────────────────────────────────────────────────────
# 1. GENERATE WORD DOCUMENT
# ─────────────────────────────────────────────────────────────────
def generate_word():
    doc = Document()
    set_margins(doc)

    # ── HALAMAN JUDUL ──────────────────────────────────────────────
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(60)
    r = p.add_run("LAPORAN TUGAS")
    set_font(r, size=16, bold=True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("IMPLEMENTASI KOMUNIKASI MICROSERVICES")
    set_font(r, size=20, bold=True)

    doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("MediSync — Sistem Informasi Rumah Sakit Berbasis Microservices")
    set_font(r, size=13, italic=True)

    doc.add_paragraph()
    doc.add_paragraph()

    for label, val in [
        ("Mata Kuliah", "Jaringan Komputer Terapan"),
        ("Dosen Pengampu", "[ISI NAMA DOSEN]"),
        ("Semester", "Genap 2025/2026"),
        ("Program Studi", "[ISI PRODI]"),
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p.add_run(f"{label}: ")
        set_font(r1, size=12, bold=True)
        r2 = p.add_run(val)
        set_font(r2, size=12)

    doc.add_paragraph()
    doc.add_paragraph()

    anggota = [
        ("1", "[ISI NAMA/NIM]", "[ISI NIM]"),
        ("2", "[ISI NAMA/NIM]", "[ISI NIM]"),
        ("3", "[ISI NAMA/NIM]", "[ISI NIM]"),
        ("4", "[ISI NAMA/NIM]", "[ISI NIM]"),
        ("5", "[ISI NAMA/NIM]", "[ISI NIM]"),
    ]
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Disusun Oleh:")
    set_font(r, size=12, bold=True)

    add_table(doc, ["No", "Nama", "NIM"],
              [(a[0], a[1], a[2]) for a in anggota],
              col_widths=[0.5, 3.5, 2.0])

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("[ISI NAMA INSTITUSI]\n2025/2026")
    set_font(r, size=12)

    page_break(doc)

    # ── CAPAIAN PEMBELAJARAN ───────────────────────────────────────
    add_heading(doc, "CAPAIAN PEMBELAJARAN", 1, 14, center=True)

    cp_rows = [
        ("PLO 6", "Mampu menganalisis dan menyelesaikan permasalahan jaringan dan keamanannya."),
        ("Indikator-6-3", "Mahasiswa mampu menyelesaikan permasalahan yang terjadi pada jaringan dengan solusi yang tepat."),
        ("CPMK-TIO6026-1", "Mahasiswa mampu merancang dan mengimplementasikan solusi untuk mengatasi permasalahan komunikasi data dalam jaringan melalui teknik pemrograman socket tingkat lanjut serta integrasi layanan asynchronous messaging dan arsitektur microservices."),
    ]
    add_table(doc, ["Kode", "Deskripsi"], cp_rows, col_widths=[1.8, 4.5])

    page_break(doc)

    # ── BAB 1 ──────────────────────────────────────────────────────
    add_heading(doc, "BAB 1", 1, 14, center=True, space_before=0)
    add_heading(doc, "PENDAHULUAN", 1, 14, center=True, space_before=0)

    add_heading(doc, "1.1 Latar Belakang", 2, 13, space_before=12)
    add_body(doc, "Perkembangan sistem informasi di bidang kesehatan menuntut adanya infrastruktur yang andal, skalabel, dan mudah dikembangkan. Sistem informasi rumah sakit yang dibangun secara tradisional cenderung bersifat monolitik — seluruh fungsi seperti pendaftaran pasien, rekam medis, dan penagihan disatukan dalam satu aplikasi besar. Pendekatan ini memunculkan permasalahan yang dikenal sebagai tight coupling, yaitu kondisi di mana komponen-komponen sistem saling bergantung secara ketat sehingga perubahan pada satu bagian dapat berdampak pada seluruh sistem.")
    add_body(doc, "Selain itu, sistem monolitik sulit untuk di-scale secara parsial. Misalnya, jika modul pendaftaran pasien mendapat lonjakan permintaan, seluruh aplikasi harus di-scale up, bukan hanya modul pendaftaran saja. Hal ini menyebabkan pemborosan sumber daya dan penurunan efisiensi operasional.")
    add_body(doc, "Untuk menjawab tantangan tersebut, arsitektur microservices hadir sebagai paradigma baru dalam pengembangan perangkat lunak. Setiap fungsi bisnis diimplementasikan sebagai layanan kecil yang mandiri (loosely coupled), dapat di-deploy secara independen, dan berkomunikasi melalui antarmuka yang terdefinisi dengan baik. Komunikasi antar layanan dalam arsitektur microservices umumnya menggunakan dua pendekatan: komunikasi sinkron (permintaan langsung dan menunggu respons) serta komunikasi asinkron (pengiriman pesan tanpa menunggu).")
    add_body(doc, "Proyek ini mengimplementasikan sistem informasi rumah sakit sederhana bernama MediSync yang terdiri dari dua layanan utama: Service A (Pendaftaran Pasien) dan Service B (Rekam Medis), dengan komunikasi sinkron menggunakan gRPC dan komunikasi asinkron menggunakan RabbitMQ. Implementasi ini secara langsung menunjukkan bagaimana arsitektur microservices dapat memecahkan permasalahan tight coupling dan meningkatkan ketersediaan layanan dalam konteks sistem kesehatan.")

    add_heading(doc, "1.2 Rumusan Masalah", 2, 13)
    add_body(doc, "Berdasarkan latar belakang di atas, rumusan masalah dalam tugas ini adalah:")
    add_bullet(doc, "Bagaimana merancang arsitektur microservices yang memisahkan fungsi pendaftaran pasien dan rekam medis secara mandiri dengan database yang terisolasi?")
    add_bullet(doc, "Bagaimana mengimplementasikan komunikasi sinkron antar layanan menggunakan gRPC untuk validasi data secara real-time?")
    add_bullet(doc, "Bagaimana mengimplementasikan komunikasi asinkron menggunakan RabbitMQ agar Service B dapat menerima notifikasi dari Service A tanpa menimbulkan ketergantungan langsung?")
    add_bullet(doc, "Bagaimana men-deploy seluruh sistem secara terintegrasi menggunakan Docker Compose sehingga mudah dijalankan dan diuji?")

    add_heading(doc, "1.3 Tujuan", 2, 13)
    add_body(doc, "Tujuan dari tugas ini adalah:")
    add_bullet(doc, "Merancang dan mengimplementasikan arsitektur microservices untuk sistem informasi rumah sakit dengan pemisahan layanan yang jelas.")
    add_bullet(doc, "Mengimplementasikan komunikasi data sinkron berbasis gRPC antara Service A dan Service B.")
    add_bullet(doc, "Mengimplementasikan komunikasi data asinkron berbasis RabbitMQ menggunakan pola event-driven.")
    add_bullet(doc, "Memastikan isolasi database antar layanan sebagai prinsip utama microservices.")
    add_bullet(doc, "Men-deploy seluruh sistem menggunakan Docker Compose agar dapat berjalan secara konsisten di berbagai lingkungan.")

    page_break(doc)

    # ── BAB 2 ──────────────────────────────────────────────────────
    add_heading(doc, "BAB 2", 1, 14, center=True, space_before=0)
    add_heading(doc, "TINJAUAN PUSTAKA", 1, 14, center=True, space_before=0)

    add_heading(doc, "2.1 Arsitektur Microservices", 2, 13)
    add_body(doc, "Arsitektur microservices adalah pendekatan pengembangan perangkat lunak di mana aplikasi dibangun sebagai kumpulan layanan kecil yang dapat di-deploy secara independen. Setiap layanan menjalankan proses tersendiri, memiliki database-nya sendiri, dan berkomunikasi melalui mekanisme yang ringan — biasanya HTTP API atau message queue.")
    add_body(doc, "Prinsip-prinsip utama arsitektur microservices antara lain:")
    add_bullet(doc, "Single Responsibility: Setiap layanan bertanggung jawab atas satu domain bisnis.")
    add_bullet(doc, "Loose Coupling: Layanan tidak saling bergantung secara langsung; perubahan pada satu layanan tidak merusak layanan lain.")
    add_bullet(doc, "High Cohesion: Kode yang berkaitan dengan satu fungsi bisnis dikelompokkan dalam satu layanan.")
    add_bullet(doc, "Database per Service: Setiap layanan memiliki dan mengelola datanya sendiri. Tidak ada layanan lain yang boleh mengakses database layanan lain secara langsung.")
    add_bullet(doc, "Decentralized Data Management: Tidak ada satu database terpusat untuk seluruh sistem.")
    add_body(doc, "Berbeda dengan arsitektur monolitik, microservices memungkinkan tim yang berbeda untuk mengembangkan, menguji, dan men-deploy layanan secara independen. Ini meningkatkan kecepatan pengembangan dan ketahanan sistem — jika satu layanan mengalami gangguan, layanan lainnya tetap bisa berjalan.")

    add_heading(doc, "2.2 gRPC (Google Remote Procedure Call)", 2, 13)
    add_body(doc, "gRPC adalah framework Remote Procedure Call (RPC) modern yang dikembangkan oleh Google. RPC memungkinkan sebuah program untuk memanggil prosedur/fungsi yang berjalan di komputer atau proses lain seolah-olah fungsi tersebut berjalan secara lokal. gRPC menggunakan HTTP/2 sebagai transport protocol dan Protocol Buffers (protobuf) sebagai mekanisme serialisasi data.")
    add_body(doc, "Karakteristik utama gRPC:")
    add_bullet(doc, "Contract-First: Antarmuka layanan didefinisikan terlebih dahulu dalam file .proto sebelum implementasi kode. Ini memastikan konsistensi antara client dan server.")
    add_bullet(doc, "Efisiensi Tinggi: Protocol Buffers menghasilkan payload yang jauh lebih kecil dibandingkan JSON karena menggunakan format biner.")
    add_bullet(doc, "HTTP/2: Mendukung multiplexing (banyak request dalam satu koneksi), header compression, dan server push.")
    add_bullet(doc, "Strongly Typed: Kontrak antar layanan terdefinisi secara ketat, mengurangi risiko kesalahan tipe data.")
    add_bullet(doc, "Multi-bahasa: gRPC mendukung hampir semua bahasa pemrograman populer (Go, Python, Java, C++, dll).")
    add_body(doc, "Dalam proyek MediSync, gRPC digunakan untuk komunikasi sinkron antara Service A dan Service B — Service A memanggil fungsi CheckPatientRecord di Service B secara langsung dan menunggu respons sebelum melanjutkan proses pendaftaran.")

    add_heading(doc, "2.3 Message Queue dan RabbitMQ", 2, 13)
    add_body(doc, "Message Queue adalah pola komunikasi asinkron di mana pengirim (producer) menempatkan pesan ke dalam antrian (queue), dan penerima (consumer) mengambil dan memproses pesan tersebut pada waktu yang berbeda. Pola ini memungkinkan decoupling antara producer dan consumer — producer tidak perlu menunggu consumer selesai memproses.")
    add_body(doc, "RabbitMQ adalah salah satu message broker paling populer yang mengimplementasikan protokol AMQP (Advanced Message Queuing Protocol). Komponen utama RabbitMQ:")
    add_bullet(doc, "Producer: Aplikasi yang mengirim pesan.")
    add_bullet(doc, "Exchange: Menerima pesan dari producer dan mendistribusikannya ke queue berdasarkan routing key dan tipe exchange.")
    add_bullet(doc, "Queue: Tempat penyimpanan pesan sebelum dikonsumsi.")
    add_bullet(doc, "Consumer: Aplikasi yang menerima dan memproses pesan dari queue.")
    add_bullet(doc, "Binding: Aturan yang menghubungkan exchange ke queue.")
    add_body(doc, "Tipe exchange yang digunakan dalam proyek ini adalah direct exchange — pesan dikirim ke queue yang routing key-nya persis sama dengan routing key pada pengiriman pesan. Keunggulan penggunaan RabbitMQ: Service A tidak perlu tahu apakah Service B sedang berjalan atau tidak saat mengirim event, pesan dapat di-persist agar tidak hilang jika broker restart, dan consumer bisa memproses pesan sesuai kapasitasnya tanpa membebani producer.")

    add_heading(doc, "2.4 Relevansi Konsep dengan Studi Kasus Rumah Sakit", 2, 13)
    add_body(doc, "Dalam konteks sistem informasi rumah sakit, pemisahan layanan pendaftaran dan rekam medis menjadi dua microservice yang terpisah mencerminkan realitas operasional rumah sakit yang sesungguhnya. Pendaftaran pasien adalah proses yang berhadapan langsung dengan pasien — harus cepat dan responsif. Jika terjadi gangguan pada sistem rekam medis, proses pendaftaran tidak boleh ikut terganggu.")
    add_body(doc, "Rekam medis membutuhkan data yang akurat dan konsisten — pembuatan rekam medis dapat dilakukan secara asinkron setelah pendaftaran selesai. Validasi real-time via gRPC diperlukan saat pendaftaran untuk memastikan seorang pasien tidak terdaftar dua kali — ini adalah komunikasi sinkron karena keputusan harus dibuat sebelum menyimpan data. Event-driven via RabbitMQ digunakan untuk memberitahu Service B bahwa ada pasien baru yang perlu dibuatkan draft rekam medis — ini tidak perlu sinkron karena pembuatan draft tidak memblokir proses pendaftaran.")

    page_break(doc)

    # ── BAB 3 ──────────────────────────────────────────────────────
    add_heading(doc, "BAB 3", 1, 14, center=True, space_before=0)
    add_heading(doc, "ANALISIS DAN PERANCANGAN", 1, 14, center=True, space_before=0)

    add_heading(doc, "3.1 Analisis Kebutuhan Sistem", 2, 13)
    add_heading(doc, "3.1.1 Kebutuhan Fungsional", 3, 12, space_before=6)
    kf_rows = [
        ("KF-01", "Sistem dapat menerima input data pasien baru melalui antarmuka web"),
        ("KF-02", "Sistem dapat memvalidasi apakah pasien sudah pernah terdaftar sebelum menyimpan data"),
        ("KF-03", "Sistem dapat menyimpan data pasien ke database pendaftaran"),
        ("KF-04", "Sistem dapat mengirimkan notifikasi ke layanan rekam medis saat pasien baru terdaftar"),
        ("KF-05", "Sistem rekam medis dapat membuat draft rekam medis secara otomatis"),
        ("KF-06", "Pengguna dapat melihat daftar pasien yang terdaftar"),
        ("KF-07", "Pengguna dapat mencari rekam medis berdasarkan NIK"),
    ]
    add_table(doc, ["ID", "Kebutuhan"], kf_rows, col_widths=[1.0, 5.3])

    add_heading(doc, "3.1.2 Kebutuhan Non-Fungsional", 3, 12, space_before=6)
    knf_rows = [
        ("KNF-01", "Layanan harus dapat berjalan secara independen (fault isolation)"),
        ("KNF-02", "Setiap layanan memiliki database terpisah (database isolation)"),
        ("KNF-03", "Kontrak komunikasi antar layanan harus terdefinisi secara eksplisit (contract-first)"),
        ("KNF-04", "Sistem harus memiliki mekanisme retry saat koneksi database atau broker gagal"),
        ("KNF-05", "Seluruh sistem harus dapat dijalankan dengan satu perintah Docker Compose"),
    ]
    add_table(doc, ["ID", "Kebutuhan"], knf_rows, col_widths=[1.0, 5.3])

    add_heading(doc, "3.2 Deskripsi Komponen", 2, 13)
    add_heading(doc, "3.2.1 Frontend (React + Vite)", 3, 12, space_before=6)
    add_body(doc, "Frontend merupakan antarmuka pengguna yang diakses melalui browser. Dibangun dengan React 18 dan Vite sebagai build tool, berjalan di port 3000. Frontend bertugas menampilkan formulir pendaftaran pasien baru, mengirimkan data pasien ke Service A melalui HTTP POST, menampilkan daftar pasien yang sudah terdaftar, dan memberikan feedback visual kepada pengguna (loading state, error message, success message). Frontend tidak berkomunikasi langsung dengan Service B maupun database — seluruh komunikasi dilakukan melalui Service A.")

    add_heading(doc, "3.2.2 Service A — Pendaftaran (Go + Gin)", 3, 12, space_before=6)
    add_body(doc, "Service A adalah layanan inti pendaftaran pasien. Berjalan di port 4001 dan merupakan satu-satunya layanan yang dapat diakses oleh frontend. Tanggung jawab Service A: menerima dan memvalidasi data pasien dari frontend, memanggil Service B via gRPC untuk mengecek apakah NIK sudah terdaftar (komunikasi sinkron), menyimpan data pasien ke db_pendaftaran jika belum terdaftar, mempublikasikan event patient.registered ke RabbitMQ (komunikasi asinkron), serta menyediakan endpoint GET untuk membaca daftar pasien.")
    add_body(doc, "Database: db_pendaftaran dengan tabel patients. Endpoints: POST /api/patients, GET /api/patients, GET /health.")

    add_heading(doc, "3.2.3 Service B — Rekam Medis (Go + Gin + gRPC Server)", 3, 12, space_before=6)
    add_body(doc, "Service B adalah layanan pengelola rekam medis. Berjalan di port 4002 (HTTP) dan 50052 (gRPC). Service B bertindak sebagai gRPC server sekaligus consumer RabbitMQ. Tanggung jawab Service B: melayani panggilan gRPC CheckPatientRecord dari Service A, mengonsumsi event patient.registered dari RabbitMQ, membuat draft rekam medis di db_rekam_medis saat menerima event, serta menyediakan endpoint GET untuk membaca rekam medis.")
    add_body(doc, "Database: db_rekam_medis dengan tabel medical_records. Endpoints: GET /api/records, GET /api/records/:nik, GET /health.")

    add_heading(doc, "3.3 Pemilihan dan Justifikasi Teknologi", 2, 13)
    add_heading(doc, "3.3.1 Teknologi yang Dipilih", 3, 12, space_before=6)
    tech_rows = [
        ("Backend Services", "Go (Golang)", "1.21"),
        ("HTTP Framework", "Gin", "v1.9.1"),
        ("RPC Framework", "gRPC + Protocol Buffers", "v1.62.0"),
        ("Message Broker", "RabbitMQ", "3.12"),
        ("Database", "PostgreSQL", "15"),
        ("Database Driver", "lib/pq", "v1.10.9"),
        ("AMQP Client", "amqp091-go", "v1.9.0"),
        ("Frontend", "React + Vite", "18 + 5"),
        ("HTTP Client (FE)", "Axios", "v1.6.7"),
        ("Containerization", "Docker + Docker Compose", "-"),
    ]
    add_table(doc, ["Komponen", "Teknologi", "Versi"], tech_rows, col_widths=[2.0, 2.5, 1.8])

    add_heading(doc, "3.3.2 Alasan Mendalam Pemilihan Teknologi", 3, 12, space_before=6)
    add_body(doc, "Go (Golang) untuk Backend: Go dipilih karena karakteristiknya yang sangat sesuai untuk membangun microservices. Go dikompilasi menjadi binary native sehingga jauh lebih efisien dari bahasa interpreted. Goroutine dan channel milik Go memudahkan penanganan banyak request secara bersamaan tanpa overhead thread yang besar. Hasil kompilasi Go adalah satu binary yang dapat langsung dijalankan di Alpine Linux tanpa dependency runtime, menjadikan Docker image sangat kecil dan portabel.")
    add_body(doc, "gRPC untuk Komunikasi Sinkron: Dibandingkan REST/HTTP biasa, gRPC dipilih karena pendekatan contract-first memaksa kedua layanan menyepakati kontrak terlebih dahulu, mengurangi risiko breaking changes. Protocol Buffers menghasilkan payload biner yang 3-10x lebih kecil dan lebih cepat diparse dibandingkan JSON. Type safety memastikan compiler menolak kode yang tidak sesuai kontrak proto, menangkap bug di waktu kompilasi bukan runtime.")
    add_body(doc, "RabbitMQ untuk Komunikasi Asinkron: Dibandingkan HTTP callback atau polling, RabbitMQ memberikan decoupling total — Service A tidak perlu tahu apakah Service B sedang up atau down saat mengirim event. Dengan konfigurasi durable=true pada queue dan DeliveryMode=Persistent, data tidak hilang meskipun RabbitMQ restart. RabbitMQ juga menyediakan Management UI di port 15672 yang sangat membantu untuk monitoring dan debugging.")
    add_body(doc, "PostgreSQL dengan Database Terpisah: Database isolation adalah prinsip wajib microservices. Setiap service hanya boleh mengakses database-nya sendiri, memastikan Service A dan Service B dapat di-develop, di-deploy, dan di-scale secara benar-benar independen. PostgreSQL mendukung UUID natively via ekstensi pgcrypto, memiliki ACID compliance, dan merupakan database relasional yang paling battle-tested di dunia open source.")

    add_heading(doc, "3.4 Arsitektur Sistem Berbasis Teknologi Terpilih", 2, 13)
    add_heading(doc, "3.4.1 Diagram Arsitektur", 3, 12, space_before=6)
    add_body(doc, "Sistem MediSync terdiri dari lima komponen utama yang berjalan dalam satu Docker network (medisync-net): Frontend (React), Service A (Pendaftaran), Service B (Rekam Medis), RabbitMQ (Message Broker), dan PostgreSQL (Database). Diagram arsitektur lengkap terdapat pada file MediSync-Diagram.drawio.")

    add_heading(doc, "3.4.2 Alur Data Langkah demi Langkah", 3, 12, space_before=6)
    steps = [
        ("Langkah 1 — Input dari Frontend", "Pengguna mengisi formulir dengan data: Nama Lengkap, NIK (16 digit), Tanggal Lahir, dan Nomor Telepon. Frontend melakukan validasi sisi klien. Jika valid, frontend mengirim HTTP POST ke http://localhost:4001/api/patients dengan payload JSON."),
        ("Langkah 2 — Validasi gRPC (Sinkron)", "Service A menerima request dan melakukan validasi server-side. Kemudian Service A membuka koneksi gRPC ke Service B di service-b:50052 dan memanggil CheckPatientRecord(nik). Service A menunggu respons dari Service B sebelum melanjutkan. Service B melakukan query ke db_rekam_medis untuk mencari rekam medis dengan NIK tersebut."),
        ("Langkah 3 — Cek Duplikasi", "Jika Service B mengembalikan has_record=true, Service A langsung mengembalikan HTTP 409 Conflict ke frontend dengan pesan pasien sudah terdaftar."),
        ("Langkah 4 — Simpan ke Database Pendaftaran", "Jika NIK belum terdaftar, Service A menjalankan query INSERT ke db_pendaftaran, menyimpan data pasien dan mendapatkan UUID sebagai patient_id."),
        ("Langkah 5 — Publish Event ke RabbitMQ (Asinkron)", "Service A mempublikasikan event patient.registered ke exchange hospital di RabbitMQ. Publish dilakukan di goroutine terpisah agar tidak memblokir response ke frontend."),
        ("Langkah 6 — Response ke Frontend", "Service A langsung mengembalikan HTTP 201 Created ke frontend dengan data pasien. Frontend menampilkan pesan sukses dan memperbarui daftar pasien."),
        ("Langkah 7 — Consume Event di Service B (Asinkron)", "Consumer RabbitMQ di Service B menerima event dari queue patient.queue. Consumer melakukan parsing JSON payload dan menjalankan INSERT ke db_rekam_medis untuk membuat draft rekam medis. Jika gagal, pesan di-nack dan di-requeue. Jika berhasil, pesan di-ack."),
    ]
    for title, desc in steps:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after  = Pt(2)
        r1 = p.add_run(title + ": ")
        set_font(r1, size=12, bold=True)
        r2 = p.add_run(desc)
        set_font(r2, size=12)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    add_heading(doc, "3.4.3 Prinsip Database Isolation", 3, 12, space_before=6)
    add_body(doc, "Salah satu prinsip terpenting dalam arsitektur microservices adalah 'database per service'. Dalam implementasi MediSync, Service A hanya mengakses db_pendaftaran dan Service B hanya mengakses db_rekam_medis. Tidak ada satu pun query yang melintas antar database. Komunikasi antar domain data dilakukan melalui mekanisme komunikasi resmi (gRPC atau RabbitMQ), bukan melalui direct database join.")

    add_heading(doc, "3.4.4 Prinsip Contract-First", 3, 12, space_before=6)
    add_body(doc, "File proto/medical_record.proto mendefinisikan kontrak gRPC sebagai satu-satunya sumber kebenaran (single source of truth) untuk komunikasi antara Service A dan Service B. Baik client (Service A) maupun server (Service B) menggunakan file Go yang di-generate dari proto ini. Perubahan pada kontrak harus dilakukan di file .proto terlebih dahulu, kemudian di-regenerate dan di-update di kedua service.")
    add_code(doc, 'service MedicalRecordService {\n  rpc CheckPatientRecord (PatientRequest) returns (RecordResponse);\n}\nmessage PatientRequest  { string nik = 1; }\nmessage RecordResponse  { bool has_record = 1; string record_id = 2; string message = 3; }')

    page_break(doc)

    # ── BAB 4 ──────────────────────────────────────────────────────
    add_heading(doc, "BAB 4", 1, 14, center=True, space_before=0)
    add_heading(doc, "TEKNIK DEPLOYMENT", 1, 14, center=True, space_before=0)

    add_heading(doc, "4.1 Docker dan Docker Compose", 2, 13)
    add_body(doc, "Docker adalah platform containerization yang memungkinkan aplikasi dikemas beserta semua dependensinya ke dalam sebuah container yang terisolasi. Container berjalan konsisten di mana pun karena membawa environment-nya sendiri. Docker Compose adalah tool untuk mendefinisikan dan menjalankan aplikasi multi-container menggunakan satu file konfigurasi docker-compose.yml.")
    add_body(doc, "Setiap service menggunakan multi-stage build di Dockerfile: Stage 1 (builder) menggunakan image golang:1.21-alpine yang besar untuk mengkompilasi source code menjadi binary. Stage 2 (runner) hanya menyalin binary hasil kompilasi ke image alpine:3.19 yang sangat kecil (~5MB). Hasilnya adalah image yang ringan dan aman karena tidak mengandung compiler atau source code.")

    add_heading(doc, "4.2 Alur Build dan Run", 2, 13)
    add_body(doc, "Untuk menjalankan seluruh sistem:")
    add_code(doc, "# Bangun dan jalankan semua service sekaligus\ndocker compose up --build\n\n# Jalankan di background\ndocker compose up --build -d\n\n# Lihat log semua service\ndocker compose logs -f\n\n# Hentikan semua service\ndocker compose down\n\n# Hentikan dan hapus volume (reset data)\ndocker compose down -v")
    add_body(doc, "Urutan startup dikonfigurasi melalui healthcheck dan depends_on di docker-compose.yml: postgres → rabbitmq → service-b → service-a → frontend. Selain dependensi startup, semua service Go juga memiliki retry loop internal hingga 10 kali dengan interval 3-4 detik.")

    add_heading(doc, "4.3 Topologi Container dan Network", 2, 13)
    topo_rows = [
        ("postgres",   "postgres",   "5432",        "5432"),
        ("rabbitmq",   "rabbitmq",   "5672, 15672",  "5672, 15672"),
        ("service-b",  "service-b",  "4002, 50052",  "4002, 50052"),
        ("service-a",  "service-a",  "4001",         "4001"),
        ("frontend",   "frontend",   "80",           "3000"),
    ]
    add_table(doc, ["Service", "Hostname (Network)", "Port Internal", "Port Host"],
              topo_rows, col_widths=[1.3, 1.5, 1.5, 1.5])

    add_heading(doc, "4.4 Pengujian Endpoint", 2, 13)
    add_body(doc, "Setelah docker compose up --build berhasil, endpoint dapat diuji dengan perintah berikut:")
    add_code(doc, "# Health check\ncurl http://localhost:4001/health\ncurl http://localhost:4002/health\n\n# Daftar pasien baru\ncurl -X POST http://localhost:4001/api/patients \\\n  -H 'Content-Type: application/json' \\\n  -d '{\"name\":\"Budi Santoso\",\"nik\":\"3201234567890001\",\n       \"tanggal_lahir\":\"1990-05-15\",\"no_telepon\":\"08123456789\"}'\n\n# Lihat semua pasien\ncurl http://localhost:4001/api/patients\n\n# Cek rekam medis (tunggu beberapa detik setelah daftar)\ncurl http://localhost:4002/api/records/3201234567890001")
    add_body(doc, "Akses RabbitMQ Management UI di http://localhost:15672 dengan username: guest, password: guest untuk memonitor exchange, queue, dan aktivitas message.")

    page_break(doc)

    # ── BAB 5 ──────────────────────────────────────────────────────
    add_heading(doc, "BAB 5", 1, 14, center=True, space_before=0)
    add_heading(doc, "BUKTI PENGGUNAAN AI", 1, 14, center=True, space_before=0)

    add_heading(doc, "5.1 Platform AI yang Digunakan", 2, 13)
    add_body(doc, "Dalam pengerjaan proyek MediSync, digunakan bantuan AI sebagai alat bantu pemrograman (vibe coding). Platform yang digunakan:")
    add_bullet(doc, "Claude Code (Anthropic) — Digunakan untuk audit kode, perbaikan bug, dan pembuatan laporan.")
    add_bullet(doc, "GitHub Copilot / AI Chat — Digunakan untuk autocomplete kode dan saran implementasi awal.")

    add_heading(doc, "5.2 Prompt yang Digunakan", 2, 13)
    add_body(doc, "Berikut adalah prompt utama yang digunakan selama pengerjaan proyek:")
    add_body(doc, "Prompt 1 — Implementasi Source Code:", space_before=4, space_after=2)
    add_code(doc, '"Tolong audit dan rapikan seluruh source code agar sinkron dengan requirement\ntugas dan siap demo tanpa error. Requirement wajib: (1) Arsitektur Microservices\ndengan Frontend, Service A, Service B; (2) gRPC sinkron antara Service A dan\nService B; (3) RabbitMQ asinkron untuk event patient.registered; (4) Database\nisolation; (5) Contract-first dengan proto file..."')
    add_body(doc, "Prompt 2 — Generate Laporan:", space_before=4, space_after=2)
    add_code(doc, '"Tolong buatkan dokumen laporan lengkap dalam format Word (.docx) yang siap\ndikumpulkan. Bahasa: Indonesia mahasiswa, natural, jelas. Judul tugas:\nImplementasi Komunikasi Microservices..."')

    add_heading(doc, "5.3 Library yang Digunakan", 2, 13)
    add_body(doc, "Service A & Service B (Go):")
    lib_go = [
        ("github.com/gin-gonic/gin", "v1.9.1", "HTTP framework untuk REST API"),
        ("github.com/gin-contrib/cors", "v1.5.0", "Middleware CORS untuk Gin"),
        ("google.golang.org/grpc", "v1.62.0", "Framework gRPC"),
        ("google.golang.org/protobuf", "v1.33.0", "Runtime Protocol Buffers"),
        ("github.com/lib/pq", "v1.10.9", "Driver PostgreSQL untuk Go"),
        ("github.com/rabbitmq/amqp091-go", "v1.9.0", "Client AMQP untuk RabbitMQ"),
        ("github.com/google/uuid", "v1.6.0", "Utilitas UUID"),
    ]
    add_table(doc, ["Library", "Versi", "Fungsi"], lib_go, col_widths=[2.8, 1.0, 2.5])
    doc.add_paragraph()
    add_body(doc, "Frontend (Node.js/React):", space_before=6)
    lib_fe = [
        ("react", "v18.2.0", "Library UI utama"),
        ("react-dom", "v18.2.0", "React untuk browser DOM"),
        ("axios", "v1.6.7", "HTTP client untuk request ke Service A"),
        ("vite", "v5.1.3", "Build tool dan dev server"),
        ("@vitejs/plugin-react", "v4.2.1", "Plugin Vite untuk JSX/React"),
    ]
    add_table(doc, ["Library", "Versi", "Fungsi"], lib_fe, col_widths=[2.0, 1.0, 3.3])

    add_heading(doc, "5.4 Bagian yang Dibantu AI dan Validasi Manual", 2, 13)
    ai_rows = [
        ("Struktur folder project", "Ya", "Disesuaikan dengan modul Go yang digunakan"),
        ("File proto/medical_record.proto", "Sebagian", "Diverifikasi kesesuaian dengan alur bisnis"),
        ("File .pb.go (generated)", "Ya", "Dicek kesesuaian dengan proto file"),
        ("service-a handler/patient.go", "Sebagian", "Diuji alur gRPC → DB → MQ secara manual"),
        ("service-a grpc/client.go", "Ya", "Diverifikasi target dan timeout yang wajar"),
        ("service-a mq/producer.go", "Ya", "Diverifikasi routing key dan durability"),
        ("service-b grpc/server.go", "Ya", "Diuji apakah query DB benar"),
        ("service-b mq/consumer.go", "Ya", "Diverifikasi logika ON CONFLICT dan requeue"),
        ("docker-compose.yml", "Ya", "Diverifikasi urutan depends_on dan env vars"),
        ("Frontend komponen React", "Ya", "Diuji validasi NIK, error handling, tampilan"),
    ]
    add_table(doc, ["Bagian", "Dibantu AI", "Validasi Manual"],
              ai_rows, col_widths=[2.2, 1.0, 3.1])

    page_break(doc)

    # ── PENUTUP ────────────────────────────────────────────────────
    add_heading(doc, "PENUTUP", 1, 14, center=True, space_before=0)

    add_heading(doc, "6.1 Kesimpulan", 2, 13)
    add_body(doc, "Melalui implementasi proyek MediSync, dapat disimpulkan bahwa:")
    add_bullet(doc, "Arsitektur microservices berhasil diterapkan dalam konteks sistem informasi rumah sakit dengan pemisahan yang jelas antara Service A (Pendaftaran) dan Service B (Rekam Medis). Setiap service memiliki database, codebase, dan container yang sepenuhnya independen.")
    add_bullet(doc, "gRPC terbukti efektif untuk komunikasi sinkron antar layanan. Pendekatan contract-first dengan file .proto memastikan konsistensi antarmuka, sementara Protocol Buffers memberikan efisiensi serialisasi yang lebih baik dibandingkan JSON biasa.")
    add_bullet(doc, "RabbitMQ berhasil mengimplementasikan pola event-driven untuk komunikasi asinkron. Service A dapat menyelesaikan proses pendaftaran dan memberikan respons ke pengguna tanpa harus menunggu Service B selesai membuat rekam medis.")
    add_bullet(doc, "Database isolation berhasil dipertahankan — tidak ada satu pun query lintas database dalam seluruh codebase.")
    add_bullet(doc, "Docker Compose menyederhanakan deployment seluruh sistem yang terdiri dari 5 container menjadi satu perintah, dengan healthcheck dan depends_on yang memastikan urutan startup yang benar.")

    add_heading(doc, "6.2 Saran Pengembangan", 2, 13)
    add_body(doc, "Beberapa area yang dapat dikembangkan lebih lanjut:")
    add_bullet(doc, "API Gateway: Menambahkan reverse proxy (Nginx atau Traefik) sebagai single entry point untuk seluruh layanan.")
    add_bullet(doc, "Autentikasi dan Otorisasi: Mengimplementasikan JWT atau OAuth2 untuk mengamankan endpoint API, terutama untuk data medis yang sensitif.")
    add_bullet(doc, "Circuit Breaker: Menambahkan pola circuit breaker pada koneksi gRPC di Service A agar sistem tetap responsif meskipun Service B tidak tersedia.")
    add_bullet(doc, "Observability: Menambahkan distributed tracing (Jaeger/Zipkin), metrics (Prometheus + Grafana), dan centralized logging (ELK Stack).")
    add_bullet(doc, "Service Discovery: Mengintegrasikan service discovery agar service tidak bergantung pada konfigurasi hostname statis.")
    add_bullet(doc, "gRPC TLS: Menambahkan Transport Layer Security pada koneksi gRPC untuk keamanan data saat transit.")
    add_bullet(doc, "Dead Letter Queue: Mengkonfigurasi Dead Letter Exchange (DLX) di RabbitMQ untuk menangani pesan yang gagal diproses berulang kali.")

    page_break(doc)

    # ── LAMPIRAN ───────────────────────────────────────────────────
    add_heading(doc, "LAMPIRAN", 1, 14, center=True, space_before=0)

    add_heading(doc, "Lampiran A — File Proto (Contract-First)", 2, 13)
    add_body(doc, "File: proto/medical_record.proto")
    add_code(doc, 'syntax = "proto3";\npackage medicalrecord;\noption go_package = "./proto";\n\n// Kontrak gRPC antara Service A (Client) dan Service B (Server)\nservice MedicalRecordService {\n  rpc CheckPatientRecord (PatientRequest) returns (RecordResponse);\n}\n\nmessage PatientRequest {\n  string nik = 1;\n}\n\nmessage RecordResponse {\n  bool   has_record = 1;\n  string record_id  = 2;\n  string message    = 3;\n}')
    add_body(doc, "File .proto ini adalah satu-satunya sumber kebenaran (single source of truth) untuk kontrak komunikasi gRPC antara Service A dan Service B. Baik client maupun server menggunakan file Go yang di-generate dari proto ini.")

    add_heading(doc, "Lampiran B — Konfigurasi RabbitMQ Producer dan Consumer", 2, 13)
    add_body(doc, "Producer (Service A) — service-a/internal/mq/producer.go:")
    add_code(doc, 'const (\n    exchangeName = "hospital"\n    routingKey   = "patient.registered"\n)\n\nfunc PublishPatientRegistered(event PatientEvent) error {\n    body, _ := json.Marshal(event)\n    return ch.PublishWithContext(ctx,\n        exchangeName, routingKey, false, false,\n        amqp.Publishing{\n            ContentType:  "application/json",\n            DeliveryMode: amqp.Persistent,\n            Body:         body,\n        },\n    )\n}')
    add_body(doc, "Consumer (Service B) — service-b/internal/mq/consumer.go:")
    add_code(doc, 'func processEvent(msg amqp.Delivery) {\n    var event PatientEvent\n    json.Unmarshal(msg.Body, &event)\n\n    db.DB.Exec(`\n        INSERT INTO medical_records (patient_id, name, nik, diagnosis, notes)\n        VALUES ($1, $2, $3, $4, $5)\n        ON CONFLICT (nik) DO NOTHING`,\n        event.PatientID, event.Name, event.NIK,\n        "Draft - Belum ada diagnosis",\n        "Rekam medis dibuat pada "+event.Timestamp,\n    )\n    msg.Ack(false)\n}')

    add_heading(doc, "Lampiran C — Docker Compose", 2, 13)
    add_body(doc, "File: docker-compose.yml (ringkasan):")
    add_code(doc, 'services:\n  postgres:\n    image: postgres:15-alpine\n    healthcheck:\n      test: ["CMD-SHELL", "pg_isready -U admin"]\n      interval: 10s; retries: 5\n\n  rabbitmq:\n    image: rabbitmq:3.12-management-alpine\n    ports: ["5672:5672", "15672:15672"]\n    healthcheck:\n      test: ["CMD", "rabbitmq-diagnostics", "ping"]\n\n  service-b:\n    build: ./service-b\n    environment:\n      DB_URL: postgres://...@postgres:5432/db_rekam_medis\n      GRPC_PORT: "50052"\n    depends_on:\n      postgres: { condition: service_healthy }\n      rabbitmq: { condition: service_healthy }\n\n  service-a:\n    build: ./service-a\n    environment:\n      DB_URL: postgres://...@postgres:5432/db_pendaftaran\n      GRPC_SERVICE_B: service-b:50052\n    depends_on:\n      service-b: { condition: service_started }')

    add_heading(doc, "Lampiran D — Screenshot Alur Demo", 2, 13)
    screenshots = [
        ("D.1", "Halaman Utama Frontend", "Tampilan awal aplikasi MediSync di http://localhost:3000"),
        ("D.2", "Form Pendaftaran", "Form diisi dengan data pasien: nama, NIK 16 digit, tanggal lahir"),
        ("D.3", "Respons Sukses", "Pesan 'Pasien berhasil didaftarkan' dengan Patient ID yang ditampilkan"),
        ("D.4", "Log Service A", "Terminal log Service A: → gRPC Check → ✓ Simpan DB → ✓ Event dikirim"),
        ("D.5", "Log Service B", "Terminal log Service B: ← Event diterima → ✓ Draft rekam medis dibuat"),
        ("D.6", "Verifikasi Rekam Medis", "GET /api/records/:nik menampilkan draft rekam medis yang dibuat otomatis"),
        ("D.7", "RabbitMQ Management UI", "http://localhost:15672 menampilkan exchange 'hospital' dan queue 'patient.queue'"),
        ("D.8", "Uji Duplikasi NIK", "Pendaftaran kedua NIK yang sama menghasilkan HTTP 409 Conflict"),
    ]
    for code, title, desc in screenshots:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        r1 = p.add_run(f"{code} — {title}: ")
        set_font(r1, size=11, bold=True)
        r2 = p.add_run(f"[Screenshot: {desc}]")
        set_font(r2, size=11, italic=True, color=(120,120,120))

    out = BASE / "LAPORAN_MEDISYNC.docx"
    doc.save(str(out))
    print(f"[OK] Word document saved: {out}")


# ─────────────────────────────────────────────────────────────────
# 2. FIX DRAW.IO → BLACK & WHITE
# ─────────────────────────────────────────────────────────────────
def fix_drawio_bw():
    src = BASE / "MediSync-Diagram.drawio"
    dst = BASE / "MediSync-Diagram-BW.drawio"
    xml = src.read_text(encoding="utf-8")

    # ── Fill colors → grayscale ──────────────────────────────────
    fill_map = {
        "#dae8fc": "#F0F0F0",  # Frontend — light gray
        "#d5e8d4": "#EBEBEB",  # Service A — slightly darker gray
        "#e1d5e7": "#E0E0E0",  # Service B — medium gray
        "#f8cecc": "#D8D8D8",  # RabbitMQ  — darker gray
        "#fff2cc": "#FAFAFA",  # REST chip — near-white
        "#ffe6cc": "#F5F5F5",  # gRPC chip — very light gray
        "#f8f9fa": "#FAFAFA",
        "#f0f9ff": "#F5F5F5",
        "#fff7ed": "#F5F5F5",
        "#ffffff": "#FFFFFF",
        "#FFFFFF": "#FFFFFF",
    }
    # ── Stroke colors → black/dark gray ─────────────────────────
    stroke_map = {
        "#6c8ebf": "#333333",
        "#82b366": "#333333",
        "#9673a6": "#555555",
        "#b85450": "#222222",
        "#d79b00": "#444444",
        "#d6b656": "#666666",
        "#6c757d": "#666666",
        "#2563eb": "#333333",
        "#d97706": "#333333",
        "#999":    "#999999",
    }
    # ── Font colors → black ──────────────────────────────────────
    font_map = {
        "#6c8ebf": "#000000",
        "#d79b00": "#000000",
        "#b85450": "#000000",
        "#82b366": "#000000",
        "#9673a6": "#000000",
        "#1a1a2e": "#000000",
        "#1e3a8a": "#000000",
        "#9a3412": "#000000",
        "#333":    "#000000",
        "#555":    "#333333",
    }

    def replace_attr(xml_str, attr, mapping):
        def sub(m):
            key = m.group(1).lower()
            for k, v in mapping.items():
                if key == k.lower():
                    return f"{attr}={v}"
            return m.group(0)
        return re.sub(rf'{attr}=([^;"\s]+)', sub, xml_str, flags=re.IGNORECASE)

    for attr, mapping in [("fillColor", fill_map),
                           ("strokeColor", stroke_map),
                           ("fontColor", font_map)]:
        xml = replace_attr(xml, attr, mapping)

    # Remove gradients
    xml = xml.replace('gradient;', '')
    # Make all edge lines dark
    xml = re.sub(r'strokeColor=#[0-9a-fA-F]{6}', 'strokeColor=#222222', xml)
    # Make edge label fontColor black
    xml = re.sub(r'fontColor=#[0-9a-fA-F]{6}', 'fontColor=#000000', xml)
    # Set Lifeline lines to dark gray
    xml = xml.replace('strokeColor=#6c8ebf;strokeWidth=1.5', 'strokeColor=#888888;strokeWidth=1.5')

    dst.write_text(xml, encoding="utf-8")
    print(f"[OK] Draw.io BW saved: {dst}")


# ─────────────────────────────────────────────────────────────────
# 3. GENERATE PPTX
# ─────────────────────────────────────────────────────────────────
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor as PPTColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

W = Inches(13.33)   # widescreen 16:9
H = Inches(7.5)

BLACK  = PPTColor(0x00, 0x00, 0x00)
WHITE  = PPTColor(0xFF, 0xFF, 0xFF)
DARK   = PPTColor(0x1E, 0x1E, 0x1E)
GRAY1  = PPTColor(0xF2, 0xF2, 0xF2)
GRAY2  = PPTColor(0xCC, 0xCC, 0xCC)
GRAY3  = PPTColor(0x88, 0x88, 0x88)
ACCENT = PPTColor(0x33, 0x33, 0x33)


def ppt_bg(slide, color: PPTColor):
    from pptx.oxml.ns import qn as pqn
    from lxml import etree
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_text_box(slide, text, left, top, width, height,
                 font_size=18, bold=False, color=BLACK,
                 align=PP_ALIGN.LEFT, wrap=True, italic=False):
    txb = slide.shapes.add_textbox(left, top, width, height)
    tf  = txb.text_frame
    tf.word_wrap = wrap
    p   = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size  = Pt(font_size)
    run.font.bold  = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb


def add_rect(slide, left, top, width, height,
             fill_color=GRAY1, line_color=BLACK, line_width=Pt(1)):
    from pptx.util import Pt as PPt
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = line_color
    shape.line.width = line_width
    return shape


def add_slide_title(prs, title_text, subtitle_text="", slide_num=None):
    slide_layout = prs.slide_layouts[6]  # blank
    slide = prs.slides.add_slide(slide_layout)

    # Dark header band
    band = add_rect(slide, 0, 0, W, Inches(1.2), fill_color=DARK, line_color=DARK)

    # Slide number (top right)
    if slide_num:
        add_text_box(slide, str(slide_num),
                     W - Inches(0.7), Inches(0.1), Inches(0.5), Inches(0.5),
                     font_size=14, color=GRAY3, align=PP_ALIGN.RIGHT)

    # Title in band
    add_text_box(slide, title_text,
                 Inches(0.4), Inches(0.1), Inches(11), Inches(1.0),
                 font_size=28, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    # Subtitle
    if subtitle_text:
        add_text_box(slide, subtitle_text,
                     Inches(0.4), Inches(1.3), Inches(12.5), Inches(0.6),
                     font_size=16, color=GRAY3, italic=True)

    # Bottom line
    ln = slide.shapes.add_connector(1, 0, Inches(1.2), W, Inches(1.2))
    ln.line.color.rgb = GRAY2
    ln.line.width = Pt(1)

    return slide


def add_content_slide(prs, title, bullets, slide_num=None):
    slide = add_slide_title(prs, title, slide_num=slide_num)
    y = Inches(1.5)
    for bullet in bullets:
        is_sub = bullet.startswith("  ")
        text = bullet.strip()
        fs   = 15 if is_sub else 18
        xoff = Inches(0.8) if is_sub else Inches(0.5)
        prefix = "   • " if is_sub else "▶  "
        add_text_box(slide, prefix + text,
                     xoff, y, Inches(12.0), Inches(0.5),
                     font_size=fs, color=DARK if not is_sub else ACCENT)
        y += Inches(0.55) if not is_sub else Inches(0.45)
    return slide


def add_diagram_slide(prs, title, boxes, arrows, slide_num=None):
    """Simple block diagram slide."""
    slide = add_slide_title(prs, title, slide_num=slide_num)
    for b in boxes:
        r = add_rect(slide, b["x"], b["y"], b["w"], b["h"],
                     fill_color=b.get("fill", GRAY1),
                     line_color=b.get("stroke", BLACK))
        # label
        tf = r.text_frame
        tf.word_wrap = True
        p  = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = b["label"]
        run.font.size  = Pt(b.get("fs", 13))
        run.font.bold  = b.get("bold", False)
        run.font.color.rgb = b.get("fc", BLACK)
    return slide


def generate_pptx():
    prs = Presentation()
    prs.slide_width  = W
    prs.slide_height = H

    # ── Slide 1: Cover ──────────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    ppt_bg(slide, DARK)

    add_text_box(slide, "MediSync",
                 Inches(1), Inches(1.2), Inches(11), Inches(1.4),
                 font_size=60, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    add_text_box(slide, "Sistem Informasi Rumah Sakit Berbasis Microservices",
                 Inches(1), Inches(2.7), Inches(11), Inches(0.8),
                 font_size=20, color=GRAY2, align=PP_ALIGN.CENTER, italic=True)

    add_text_box(slide,
                 "Implementasi Komunikasi Microservices\nJaringan Komputer Terapan | Semester Genap 2025/2026",
                 Inches(1), Inches(3.8), Inches(11), Inches(1.0),
                 font_size=16, color=GRAY3, align=PP_ALIGN.CENTER)

    # Tech tags
    tags = ["Go + Gin", "gRPC (Sync)", "RabbitMQ (Async)", "PostgreSQL", "Docker Compose"]
    for i, tag in enumerate(tags):
        x = Inches(0.5 + i * 2.5)
        r = add_rect(slide, x, Inches(5.3), Inches(2.2), Inches(0.5),
                     fill_color=ACCENT, line_color=WHITE)
        tf = r.text_frame
        p  = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = tag
        run.font.size = Pt(13)
        run.font.color.rgb = WHITE

    add_text_box(slide, "Kelompok: [ISI NAMA ANGGOTA]",
                 Inches(1), Inches(6.3), Inches(11), Inches(0.5),
                 font_size=13, color=GRAY3, align=PP_ALIGN.CENTER)

    # ── Slide 2: Latar Belakang ──────────────────────────────────
    add_content_slide(prs, "Latar Belakang & Permasalahan", [
        "Sistem informasi RS tradisional bersifat MONOLITIK",
        "  Semua fungsi tergabung → Tight Coupling",
        "  Satu modul error = seluruh sistem terganggu",
        "  Sulit di-scale secara parsial",
        "Solusi: Arsitektur MICROSERVICES",
        "  Setiap fungsi bisnis = layanan mandiri",
        "  Database terpisah per layanan",
        "  Komunikasi via gRPC (sync) + RabbitMQ (async)",
    ], slide_num=2)

    # ── Slide 3: Tujuan ─────────────────────────────────────────
    add_content_slide(prs, "Tujuan Implementasi", [
        "Merancang arsitektur microservices untuk sistem RS",
        "Mengimplementasikan komunikasi SINKRON via gRPC",
        "  Service A ← CheckPatientRecord() → Service B",
        "Mengimplementasikan komunikasi ASINKRON via RabbitMQ",
        "  Event patient.registered dikirim setelah pendaftaran",
        "Menjamin Database Isolation antar layanan",
        "Deployment terintegrasi dengan Docker Compose",
    ], slide_num=3)

    # ── Slide 4: Arsitektur Sistem ───────────────────────────────
    slide = add_slide_title(prs, "Arsitektur Sistem MediSync", slide_num=4)

    boxes = [
        # Frontend
        {"x": Inches(5.3), "y": Inches(1.4), "w": Inches(2.7), "h": Inches(0.8),
         "label": "FRONTEND\nReact + Vite | :3000",
         "fill": PPTColor(0xF0,0xF0,0xF0), "stroke": BLACK, "fs": 12, "bold": True},
        # Service A
        {"x": Inches(1.5), "y": Inches(3.0), "w": Inches(3.0), "h": Inches(0.9),
         "label": "SERVICE A — Pendaftaran\nGo + Gin | Port: 4001",
         "fill": PPTColor(0xE8,0xE8,0xE8), "stroke": BLACK, "fs": 12, "bold": True},
        # Service B
        {"x": Inches(8.8), "y": Inches(3.0), "w": Inches(3.3), "h": Inches(0.9),
         "label": "SERVICE B — Rekam Medis\nGo + Gin + gRPC | :4002/:50052",
         "fill": PPTColor(0xDC,0xDC,0xDC), "stroke": BLACK, "fs": 12, "bold": True},
        # RabbitMQ
        {"x": Inches(5.3), "y": Inches(3.0), "w": Inches(2.7), "h": Inches(0.9),
         "label": "RabbitMQ\nMessage Broker | :5672",
         "fill": PPTColor(0xCC,0xCC,0xCC), "stroke": BLACK, "fs": 12, "bold": True},
        # DB A
        {"x": Inches(1.5), "y": Inches(4.7), "w": Inches(3.0), "h": Inches(0.7),
         "label": "PostgreSQL: db_pendaftaran",
         "fill": GRAY1, "stroke": ACCENT, "fs": 11},
        # DB B
        {"x": Inches(8.8), "y": Inches(4.7), "w": Inches(3.3), "h": Inches(0.7),
         "label": "PostgreSQL: db_rekam_medis",
         "fill": GRAY1, "stroke": ACCENT, "fs": 11},
    ]
    for b in boxes:
        r = add_rect(slide, b["x"], b["y"], b["w"], b["h"],
                     fill_color=b.get("fill", GRAY1), line_color=b.get("stroke", BLACK))
        tf = r.text_frame
        tf.word_wrap = True
        p  = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = b["label"]
        run.font.size  = Pt(b.get("fs", 13))
        run.font.bold  = b.get("bold", False)
        run.font.color.rgb = BLACK

    # Annotations (arrows replaced by text labels for simplicity)
    arrow_labels = [
        (Inches(4.5), Inches(2.3), "HTTP REST\nPOST/GET"),
        (Inches(4.5), Inches(3.3), "gRPC (Sync)\nCheckPatientRecord"),
        (Inches(6.1), Inches(3.3), "Publish\npatient.registered"),
        (Inches(8.1), Inches(3.3), "Consume\n(Async)"),
    ]
    for lx, ly, lt in arrow_labels:
        add_text_box(slide, lt, lx, ly, Inches(1.8), Inches(0.8),
                     font_size=10, color=GRAY3, italic=True, align=PP_ALIGN.CENTER)

    add_text_box(slide,
                 "Database Isolation: Service A ↔ db_pendaftaran saja | Service B ↔ db_rekam_medis saja",
                 Inches(0.5), Inches(6.3), Inches(12.3), Inches(0.5),
                 font_size=12, color=GRAY3, italic=True, align=PP_ALIGN.CENTER)

    # ── Slide 5: Alur Data ───────────────────────────────────────
    add_content_slide(prs, "Alur Data — Pendaftaran Pasien Baru", [
        "① User isi form → Frontend kirim POST /api/patients ke Service A",
        "② Service A gRPC → CheckPatientRecord(nik) ke Service B [SINKRON]",
        "   Service A MENUNGGU respons sebelum lanjut",
        "③ Service B query db_rekam_medis → return has_record = true/false",
        "④ Jika sudah ada: Service A return HTTP 409 Conflict (tolak)",
        "⑤ Jika baru: Service A INSERT ke db_pendaftaran",
        "⑥ Service A publish event patient.registered → RabbitMQ [ASINKRON]",
        "   Service A TIDAK menunggu Service B → langsung return 201 OK",
        "⑦ Service B consume event → INSERT draft ke db_rekam_medis",
    ], slide_num=5)

    # ── Slide 6: Teknologi ───────────────────────────────────────
    add_content_slide(prs, "Justifikasi Pemilihan Teknologi", [
        "Go (Golang) — Backend kedua service",
        "  Binary tunggal, performan, goroutine untuk concurrency",
        "gRPC — Komunikasi Sinkron Service A ↔ B",
        "  Contract-first (.proto), payload biner 3-10x lebih kecil dari JSON",
        "  Type-safe, latensi rendah, ideal untuk validasi real-time",
        "RabbitMQ — Komunikasi Asinkron (Event-Driven)",
        "  Decoupling total, pesan persisten, mendukung retry via nack+requeue",
        "PostgreSQL — Database per Service",
        "  ACID, UUID via pgcrypto, isolasi sempurna antar domain",
        "Docker Compose — Deployment Terintegrasi",
        "  1 perintah, healthcheck, depends_on, restart: on-failure",
    ], slide_num=6)

    # ── Slide 7: gRPC Detail ─────────────────────────────────────
    add_content_slide(prs, "gRPC — Komunikasi Sinkron (Contract-First)", [
        "File: proto/medical_record.proto",
        "  Mendefinisikan kontrak SEBELUM implementasi",
        "  Generate stub otomatis ke Service A dan Service B",
        "Service: MedicalRecordService",
        "  rpc CheckPatientRecord(PatientRequest) returns (RecordResponse)",
        "Message PatientRequest: string nik",
        "Message RecordResponse: bool has_record, string record_id, string message",
        "Timeout: 5 detik per call",
        "Retry: 10x dengan interval 3 detik saat startup",
    ], slide_num=7)

    # ── Slide 8: RabbitMQ Detail ─────────────────────────────────
    add_content_slide(prs, "RabbitMQ — Komunikasi Asinkron (Event-Driven)", [
        "Exchange: 'hospital' (type: direct, durable: true)",
        "Queue: 'patient.queue' (durable: true)",
        "Routing Key: 'patient.registered'",
        "Producer (Service A):",
        "  Publish setelah INSERT berhasil — di goroutine terpisah",
        "  DeliveryMode: Persistent (pesan tidak hilang saat restart)",
        "Consumer (Service B):",
        "  Consume loop berjalan di goroutine terpisah",
        "  ACK setelah INSERT berhasil | NACK+requeue jika gagal",
        "  ON CONFLICT (nik) DO NOTHING — idempoten, aman di-retry",
    ], slide_num=8)

    # ── Slide 9: Docker Deployment ───────────────────────────────
    add_content_slide(prs, "Deployment — Docker Compose", [
        "5 Container dalam 1 network (medisync-net bridge):",
        "  postgres:15-alpine      → Port 5432 | healthcheck: pg_isready",
        "  rabbitmq:3.12-management → Port 5672, 15672 | healthcheck: ping",
        "  service-b               → Port 4002, 50052  | restart: on-failure",
        "  service-a               → Port 4001          | restart: on-failure",
        "  frontend (React+Nginx)  → Port 3000",
        "Cara menjalankan:",
        "  docker compose up --build",
        "Multi-stage Dockerfile: builder (golang:1.21-alpine) → runner (alpine:3.19)",
        "  Image final ~5MB, tidak mengandung source code",
    ], slide_num=9)

    # ── Slide 10: Demo & Pengujian ───────────────────────────────
    add_content_slide(prs, "Demo & Verifikasi End-to-End", [
        "Akses Frontend: http://localhost:3000",
        "  Isi form pasien → Submit → Lihat proses 4 tahap di UI",
        "Verify di Service A log:",
        "  → Mengecek via gRPC | ✓ Simpan DB | ✓ Event dikirim ke MQ",
        "Verify di Service B log:",
        "  ← Event diterima | ✓ Draft rekam medis dibuat",
        "Uji Duplikasi: daftar NIK yang sama → HTTP 409 Conflict",
        "Uji Rekam Medis: GET http://localhost:4002/api/records/:nik",
        "RabbitMQ UI: http://localhost:15672 → lihat queue & messages",
    ], slide_num=10)

    # ── Slide 11: Kesimpulan ─────────────────────────────────────
    add_content_slide(prs, "Kesimpulan", [
        "Microservices: Service A & B berjalan independen, database terisolasi",
        "gRPC Sync: Validasi NIK real-time dengan contract-first proto",
        "RabbitMQ Async: Pembuatan rekam medis tidak memblokir pendaftaran",
        "Database Isolation: Nol query lintas database dalam seluruh codebase",
        "Docker Compose: 1 perintah untuk jalankan 5 container",
        "Saran Pengembangan:",
        "  API Gateway, Autentikasi JWT, Circuit Breaker, Observability",
        "  Dead Letter Queue, Service Discovery, gRPC TLS",
    ], slide_num=11)

    # ── Slide 12: Penutup / Thank You ────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    ppt_bg(slide, DARK)

    add_text_box(slide, "Terima Kasih",
                 Inches(1), Inches(2.0), Inches(11), Inches(1.5),
                 font_size=54, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    add_text_box(slide, "MediSync — Implementasi Komunikasi Microservices\nJaringan Komputer Terapan | 2025/2026",
                 Inches(1), Inches(3.8), Inches(11), Inches(1.0),
                 font_size=16, color=GRAY3, align=PP_ALIGN.CENTER, italic=True)

    add_text_box(slide, "Go + gRPC + RabbitMQ + PostgreSQL + Docker",
                 Inches(1), Inches(5.2), Inches(11), Inches(0.6),
                 font_size=14, color=GRAY2, align=PP_ALIGN.CENTER)

    out = BASE / "MediSync-Presentasi-NEW.pptx"
    prs.save(str(out))
    print(f"[OK] PowerPoint saved: {out}")


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== MediSync Document Generator ===")
    generate_word()
    fix_drawio_bw()
    generate_pptx()
    print("=== DONE ===")
