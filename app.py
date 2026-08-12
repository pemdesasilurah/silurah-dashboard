"""
Dashboard Desa Silurah — SDG 11 Digital Mapping Project
Custom high-end UI built on top of Streamlit primitives.
"""

import base64
from pathlib import Path

import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import pydeck as pdk

# --------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Desa Silurah | Peta Digital Desa",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------------------------------
# LANGUAGE SWITCHER (PENGATUR BAHASA)
# --------------------------------------------------------------------------
col_space, col_lang = st.columns([8.5, 1.5])
with col_lang:
    lang_choice = st.radio(
        "Bahasa",
        ["🇮🇩 ID", "🇬🇧 EN"],
        horizontal=True,
        label_visibility="collapsed",
        key="language_selector",
    )

is_eng = lang_choice == "🇬🇧 EN"

def tr(id_text, en_text):
    return en_text if is_eng else id_text

# --------------------------------------------------------------------------
# ASSET HELPERS
# --------------------------------------------------------------------------
ASSETS_DIR = Path(__file__).parent / "assets"
HERO_IMAGE_PATH = ASSETS_DIR / "foto_desa.jpg"


@st.cache_data(show_spinner=False)
def get_base64_image(path: Path):
    """Encode a local image to base64 for CSS background-image use."""
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    return None


hero_b64 = get_base64_image(HERO_IMAGE_PATH)

if hero_b64:
    hero_bg_css = f"url('data:image/jpg;base64,{hero_b64}')"
else:
    hero_bg_css = (
        "linear-gradient(135deg, #3E5C48 0%, #2C4C3B 45%, #4A3525 100%)"
    )

# --------------------------------------------------------------------------
# DATA
# --------------------------------------------------------------------------
# --- DATA ARTIKEL KKN ---
if 'artikel_aktif' not in st.session_state:
    st.session_state.artikel_aktif = None

ARTIKEL_DATA = [
    {
        "id": "artikel-dokumentasi-gones",
        "judul": tr("Mahasiswa KKN UNDIP Dokumentasikan Proses Produksi Minuman Gones untuk Mendukung Promosi UMKM Desa Silurah", "UNDIP KKN Students Document the Production Process of Gones Beverage to Support the Promotion of Silurah Village MSMEs"),
        "gambar": "artikel_melda.jpg", 
        "tanggal": "21 Juli 2026",
        "penulis": "Melda Fitri Ayu Rosada / Tim II KKN Undip",
        "ringkasan": tr("Dokumentasi proses produksi minuman gones, produk unggulan UMKM Desa Silurah, guna mendukung promosi melalui media sosial Instagram.", "Documentation of the production process of Gones beverage, a flagship MSME product of Silurah Village, to support promotion through Instagram social media."),
        "isi": [
            tr("Mahasiswa KKN-R Tim II 2026 Universitas Diponegoro melaksanakan kegiatan dokumentasi proses produksi minuman gones, salah satu produk unggulan UMKM Desa Silurah, Kecamatan Wonotunggal, Kabupaten Batang, Selasa (21/7/2026). Kegiatan ini merupakan bentuk kontribusi mahasiswa dalam mendukung publikasi dan promosi potensi UMKM lokal melalui media sosial Instagram.", "Undip KKN-R Team II 2026 students carried out a documentation activity of the production process of Gones beverage, one of the flagship MSME products of Silurah Village, Wonotunggal District, Batang Regency, Tuesday (21/7/2026). This activity is a form of student contribution in supporting the publication and promotion of local MSME potential through Instagram social media."),
            
            tr("Kegiatan dilaksanakan oleh Melda Fitri Ayu Rosada, Program Studi Informasi dan Humas, Sekolah Vokasi Universitas Diponegoro, dengan berkoordinasi langsung bersama pelaku UMKM minuman gones, Ibu Inti. Koordinasi dilakukan untuk mengetahui tahapan produksi sekaligus menentukan proses yang akan didokumentasikan.", "The activity was carried out by Melda Fitri Ayu Rosada, Information and Public Relations Study Program, Vocational School of Diponegoro University, by coordinating directly with the Gones beverage MSME actor, Ibu Inti. Coordination was carried out to understand the production stages as well as to determine the processes to be documented."),
            
            tr("Proses pengambilan video dilakukan secara menyeluruh, mulai dari pengambilan gones sebagai bahan baku, persiapan alat dan bahan, proses pengolahan dan pencampuran bahan, pemasakan, hingga tahap pengemasan dan produk siap dipasarkan. Seluruh tahapan tersebut direkam untuk menghasilkan konten visual yang informatif dan menarik.", "The video shooting process was carried out comprehensively, starting from collecting gones as raw material, preparing tools and ingredients, processing and mixing ingredients, cooking, up to the packaging stage and the product being ready for market. All these stages were recorded to produce informative and engaging visual content."),
            
            tr("Dokumentasi ini tidak hanya bertujuan untuk merekam proses pembuatan minuman gones, tetapi juga memperkenalkan kepada masyarakat mengenai produk lokal Desa Silurah beserta proses pengolahannya. Melalui video, masyarakat dapat melihat secara lebih dekat bagaimana minuman gones diproduksi hingga menjadi produk yang siap dipasarkan.", "This documentation aims not only to record the manufacturing process of the Gones beverage but also to introduce the local product of Silurah Village and its processing to the public. Through the video, the public can get a closer look at how the Gones beverage is produced until it becomes a market-ready product."),
            
            tr("Hasil kegiatan berupa video dokumentasi proses produksi minuman gones yang dipublikasikan melalui Instagram. Konten tersebut diharapkan dapat meningkatkan eksposur produk dan membantu memperkenalkan UMKM minuman gones kepada masyarakat yang lebih luas melalui media sosial.", "The outcome of the activity is a documentary video of the Gones beverage production process published on Instagram. The content is expected to increase product exposure and help introduce the Gones beverage MSME to a wider audience through social media."),
            
            tr("Pemanfaatan Instagram sebagai media publikasi juga menjadi langkah untuk mendukung pemasaran digital UMKM secara lebih sederhana dan mudah dijangkau. Dengan adanya dokumentasi visual yang menarik, pelaku UMKM diharapkan memiliki materi promosi yang dapat digunakan untuk memperkenalkan produk, meningkatkan daya tarik konsumen, serta mendukung keberlanjutan usaha.", "The utilization of Instagram as a publication medium is also a step to support digital marketing of MSMEs in a simpler and more accessible way. With engaging visual documentation, MSME actors are expected to have promotional materials that can be used to introduce products, increase consumer appeal, and support business sustainability."),
            
            tr("Melalui kegiatan ini, mahasiswa KKN-R Tim II 2026 Universitas Diponegoro turut berupaya mengoptimalkan pemanfaatan media sosial sebagai sarana publikasi potensi lokal Desa Silurah, khususnya dalam memperkenalkan produk UMKM minuman gones kepada masyarakat luas.", "Through this activity, KKN-R Team II 2026 students of Diponegoro University also strive to optimize the use of social media as a means of publishing the local potential of Silurah Village, especially in introducing the Gones beverage MSME product to the wider community.")
        ]
    },
    {
        "id": "artikel-optimalisasi-pemasaran",
        "judul": tr("Dari Gones ke Marketplace: Mahasiswa KKN Undip Tim II Dorong Digitalisasi Pemasaran UMKM Gones di Desa Silurah", "From Gones to Marketplace: KKN Undip Team II Students Drive Digitalization of Gones MSME Marketing in Silurah Village"),
        "gambar": "artikel_nadia.jpg",
        "tanggal": "23 Juli 2026",
        "penulis": "Nadia Almasyah / Tim II KKN Undip",
        "ringkasan": tr("Sosialisasi dan pendampingan UMKM minuman Gones untuk memperluas jangkauan pasar lokal ke ranah digital melalui media sosial dan pendaftaran e-commerce.", "Socialization and mentoring of Gones beverage MSMEs to expand the local market reach to the digital realm through social media and e-commerce registration."),
        "isi": [
            tr("Upaya mendorong pelaku Usaha Mikro, Kecil, dan Menengah (UMKM) untuk beradaptasi dengan perkembangan pemasaran digital terus dilakukan di Desa Silurah, Kecamatan Wonotunggal, Kabupaten Batang. Melalui program sosial kemasyarakatan, Nadia Alma, mahasiswa Kuliah Kerja Nyata (KKN) Universitas Diponegoro (Undip) Tim II, memberikan edukasi dan pendampingan optimalisasi pemasaran digital kepada pelaku UMKM produksi Minuman Gones di Dukuh Simangli, Desa Silurah, Kamis (23/7/2026).", "Efforts to encourage Micro, Small, and Medium Enterprises (MSME) actors to adapt to developments in digital marketing continue in Silurah Village, Wonotunggal District, Batang Regency. Through a community social program, Nadia Alma, a Diponegoro University (Undip) Student Study Service (KKN) Team II student, provided education and assistance in optimizing digital marketing to MSME actors producing Gones Beverages in Simangli Hamlet, Silurah Village, Thursday (23/7/2026)."),
            
            tr("Program tersebut digagas sebagai bentuk kontribusi Mahasiswa dalam membantu pelaku UMKM memanfaatkan perkembangan teknologi digital untuk memperluas jangkauan pemasaran produk lokal. Kegiatan difokuskan pada edukasi mengenai pemanfaatan media sosial dan e-commerce sebagai sarana promosi sekaligus penjualan produk.", "The program was initiated as a form of Student contribution in helping MSME actors utilize the development of digital technology to expand the marketing reach of local products. Activities focused on education regarding the use of social media and e-commerce as a means of promotion as well as product sales."),
            
            tr("Dalam pelaksanaannya, Mahasiswa bertanggung jawab sebagai pembuat materi sekaligus pemateri. Materi sosialisasi disusun dalam bentuk PowerPoint yang membahas strategi optimalisasi pemasaran melalui media sosial dan marketplace. Selain itu, Mahasiswa juga membuat poster panduan mengenai tata cara mendaftarkan produk UMKM ke e-commerce agar dapat menjadi media informasi yang mudah dipahami dan digunakan oleh pelaku usaha.", "In its implementation, Students are responsible as material creators as well as presenters. The socialization material was arranged in PowerPoint format discussing strategies to optimize marketing through social media and marketplaces. In addition, Students also created guide posters on how to register MSME products to e-commerce so they can become an information medium easily understood and used by business actors."),
            
            tr("Tidak hanya memberikan pemaparan materi, Mahasiswa turut melakukan pendampingan secara langsung kepada pelaku UMKM dalam proses pendaftaran e-commerce. Pendampingan dilakukan secara bertahap dengan menyesuaikan pemahaman peserta sehingga pelaku UMKM dapat mengikuti proses pendaftaran dan memahami cara memanfaatkan marketplace untuk kegiatan pemasaran.", "Not only giving material presentations, Students also directly assisted MSME actors in the e-commerce registration process. Mentoring was carried out gradually adjusting to the participants' understanding so that MSME actors could follow the registration process and understand how to utilize the marketplace for marketing activities."),
            
            tr("Kegiatan tersebut mendapat respons positif dari pelaku UMKM produksi Minuman Gones. Masyarakat menunjukkan antusiasme selama proses sosialisasi berlangsung dan merasa terbantu dengan adanya edukasi serta pendampingan mengenai optimalisasi pemasaran digital.", "This activity received a positive response from MSME actors producing Gones Beverages. The community showed enthusiasm during the socialization process and felt helped by the education and assistance regarding digital marketing optimization."),
            
            tr("\"Program ini diharapkan dapat memberikan pengetahuan sekaligus langkah praktis bagi pelaku UMKM agar dapat mulai memanfaatkan platform digital untuk memasarkan produknya secara lebih luas,\" ujar Nadia Alma dalam kegiatan sosialisasi. Hasil nyata dari program tersebut ditunjukkan melalui keberhasilan pelaku UMKM produksi Minuman Gones mendaftarkan produknya ke marketplace. Dengan demikian, pelaku usaha kini memiliki tambahan kanal pemasaran digital yang dapat digunakan untuk menjangkau konsumen di luar wilayah Desa Silurah.", "\"This program is expected to provide knowledge as well as practical steps for MSME actors so they can start utilizing digital platforms to market their products more widely,\" said Nadia Alma in the socialization activity. The tangible results of the program were shown through the success of the Gones Beverage production MSME actors in registering their products to the marketplace. Thus, business actors now have an additional digital marketing channel that can be used to reach consumers outside the Silurah Village area."),
            
            tr("Keberhasilan tersebut menjadi salah satu capaian penting dari program sosial kemasyarakatan yang dilaksanakan Mahasiswa selama kegiatan KKN. Tidak hanya memberikan edukasi, program ini juga menghasilkan penerapan langsung yang dapat dilanjutkan secara mandiri oleh pelaku UMKM.", "This success is one of the important achievements of the social community programs carried out by Students during KKN activities. Not only providing education, this program also produces a direct application that can be continued independently by MSME actors."),
            
            tr("Melalui program tersebut, Mahasiswa berharap pemanfaatan media sosial dan e-commerce dapat terus dikembangkan oleh pelaku UMKM Desa Silurah. Digitalisasi pemasaran diharapkan mampu meningkatkan daya saing produk lokal, memperluas jangkauan pasar, serta membuka peluang peningkatan penjualan Minuman Gones sebagai salah satu produk UMKM di Dukuh Simangli, Desa Silurah.", "Through this program, Students hope the utilization of social media and e-commerce can continue to be developed by Silurah Village MSME actors. Marketing digitalization is expected to increase local product competitiveness, expand market reach, and open opportunities to increase sales of Gones Beverages as one of the MSME products in Simangli Hamlet, Silurah Village."),
            
            tr("<b>Tentang Program</b>", "<b>About the Program</b>"),
            
            tr("Program optimalisasi pemasaran melalui media sosial dan e-commerce merupakan program sosial kemasyarakatan yang dirancang dan dilaksanakan oleh Nadia Alma, mahasiswa KKN Universitas Diponegoro Tim II, di Desa Silurah, Kecamatan Wonotunggal, Kabupaten Batang. Program ini berfokus pada edukasi, penyusunan media informasi, dan pendampingan praktis bagi pelaku UMKM dalam memanfaatkan teknologi digital untuk mengembangkan pemasaran produk.", "The marketing optimization program through social media and e-commerce is a social community program designed and implemented by Nadia Alma, a student of Diponegoro University KKN Team II, in Silurah Village, Wonotunggal District, Batang Regency. This program focuses on education, preparation of information media, and practical assistance for MSME actors in utilizing digital technology to develop product marketing.")
        ]
    },
    {
        "id": "artikel-pelita-visualisasi-data-word",
        "judul": tr("Tingkatkan Efisiensi Administrasi, Perangkat Desa Silurah Ikuti Pelatihan Literasi Digital PELITA", "Improve Administrative Efficiency, Silurah Village Officials Participate in PELITA Digital Literacy Training"),
        "gambar": "artikel_maretta.jpg",
        "tanggal": "27 Juli 2026",
        "penulis": "Maretta Govani Dinda Sacinta / Tim II KKN Undip",
        "ringkasan": tr("Pelatihan literasi digital bagi perangkat Desa Silurah yang difokuskan pada efisiensi sistem surat-menyurat dan visualisasi data.", "Digital literacy training for Silurah Village officials focused on the efficiency of the correspondence system and data visualization."),
        "isi": [
            tr("Upaya mewujudkan tata kelola administrasi desa yang tangkas dan melek teknologi terus digencarkan. Sebanyak tujuh perangkat Desa Silurah mengikuti program Pelatihan Literasi Digital (PELITA) yang diselenggarakan di Balai Desa setempat, Senin (27/7/2026).", "Efforts to realize agile and technology-literate village administrative governance continue to be intensified. A total of seven Silurah Village officials participated in the Digital Literacy Training (PELITA) program held at the local Village Hall, Monday (27/7/2026)."),
            
            tr("Kegiatan pengabdian masyarakat ini menyasar peningkatan kompetensi aparatur desa dengan membedah dua materi utama: efisiensi sistem surat-menyurat dan penguasaan dasar visualisasi data kemasyarakatan.", "This community service activity targets improving the competence of village apparatus by dissecting two main materials: the efficiency of the correspondence system and mastering the basics of community data visualization."),
            
            tr("Pemaparan diawali dengan materi tata tulis dokumen bertajuk \"Kerja Cerdas Surat Menyurat\". Dalam sesi ini, aparatur desa dibekali pemahaman mengenai pemanfaatan Microsoft Word, secara khusus menyoroti efisiensi fitur Mail Merge dan pembuatan format header otomatis. Materi ini dirancang agar perangkat desa mengetahui cara memangkas waktu pengerjaan dokumen repetitif, sehingga proses persuratan massal kelak dapat dieksekusi secara instan dan akurat.", "The presentation began with document writing material entitled \"Smart Work in Correspondence\". In this session, village apparatus were equipped with an understanding of the utilization of Microsoft Word, specifically highlighting the efficiency of the Mail Merge feature and the creation of automatic header formats. This material is designed so that village officials know how to cut the processing time of repetitive documents, so that mass mailing processes can later be executed instantly and accurately."),
            
            tr("Memasuki sesi selanjutnya, peserta diajak menyelami materi \"Mengubah Angka Jadi Cerita\". Melalui pemaparan dasar visualisasi data, perangkat desa diberikan wawasan mengenai urgensi penyajian data visual untuk informasi publik. Materi yang disampaikan mencakup pengenalan fungsi ragam diagram, identifikasi kesalahan umum dalam visualisasi data, hingga aturan baku pembuatan infografis agar data kependudukan dan demografi desa menjadi lebih komunikatif saat disajikan kepada warga.", "Entering the next session, participants were invited to dive into the material \"Turning Numbers into Stories\". Through the presentation of data visualization basics, village officials were given insights into the urgency of presenting visual data for public information. The material presented included an introduction to the functions of various diagrams, identification of common errors in data visualization, to standard rules for making infographics so that village population and demographic data become more communicative when presented to citizens."),
            
            tr("Penyampaian materi yang komprehensif ini membuahkan hasil yang positif. Ketujuh perangkat desa yang hadir berhasil memahami alur otomatisasi surat massal serta menguasai konsep dasar penyusunan grafik informasi kemasyarakatan yang komunikatif.", "This comprehensive material delivery yielded positive results. The seven village officials in attendance successfully understood the mass mail automation flow and mastered the basic concepts of preparing communicative community information graphics."),
            
            tr("Sebagai langkah keberlanjutan dan pendamping pasca-pelatihan, kegiatan ditutup dengan penyerahan buku panduan fisik (cetak) kepada pihak desa. Modul tersebut dihibahkan sebagai aset referensi kerja mandiri sehari-hari bagi perangkat Desa Silurah agar implementasi administrasi digital dapat terus berjalan secara konsisten di lingkungan balai desa.", "As a sustainability step and post-training companion, the activity closed with the handover of a physical (printed) guidebook to the village. The module was donated as a daily independent work reference asset for Silurah Village officials so that the implementation of digital administration can continue to run consistently in the village hall environment.")
        ]
    },
    {
        "id": "artikel-pelita-rab-sop",
        "judul": tr("Tingkatkan Kapasitas Perangkat Desa, Program PELITA Sukses Gelar Pelatihan RAB dan SOP Administrasi di Desa Silurah", "Increase Village Officials' Capacity, PELITA Program Successfully Holds RAB and Administrative SOP Training in Silurah Village"),
        "gambar": "artikel_adzraa.jpg", 
        "tanggal": "27 Juli 2026",
        "penulis": "Adzraa Glenys Maurene / Tim II KKN Undip",
        "ringkasan": tr("Pelatihan penyusunan RAB dan pemahaman SOP administrasi bagi perangkat Desa Silurah guna mewujudkan tata kelola desa yang lebih modern.", "Training on RAB preparation and understanding administrative SOPs for Silurah Village officials to realize a more modern village governance."),
        "isi": [
            tr("Dalam upaya mewujudkan tata kelola desa yang lebih modern dan tertib administrasi, sebuah program kerja sosial kemasyarakatan sukses menyelenggarakan kegiatan bertajuk \"PELITA: Pelatihan Literasi Digital\" di Desa Silurah, Kamis (27/7/2026). Kegiatan ini difokuskan pada peningkatan kapasitas perangkat desa melalui penyusunan Rencana Anggaran Biaya (RAB) menggunakan Microsoft Excel serta pemahaman Standar Operasional Prosedur (SOP) alur pelayanan desa.", "In an effort to realize a more modern and administratively orderly village governance, a social community work program successfully held an activity entitled \"PELITA: Digital Literacy Training\" in Silurah Village, Thursday (27/7/2026). This activity focused on increasing the capacity of village officials through the preparation of the Budget Plan (RAB) using Microsoft Excel and understanding the Standard Operating Procedures (SOP) for village service flows."),
            
            tr("Pelatihan ini dirancang dengan metode pendampingan langsung dan terbagi ke dalam dua fokus utama. Pada sesi pertama, pelatihan ditujukan secara khusus kepada Bendahara Desa. Pemateri memberikan penjelasan komprehensif secara step-by-step mengenai penyusunan RAB berbasis digital menggunakan Excel. Sesi ini membedah berbagai komponen wajib yang harus ada di dalam anggaran, sekaligus memberikan pemahaman mendetail mengenai klasifikasi dan penggunaan masing-masing kode dalam RAB agar sesuai dengan standar pelaporan keuangan yang berlaku.", "This training was designed with a direct mentoring method and divided into two main focuses. In the first session, the training was specifically aimed at the Village Treasurer. The speaker provided a comprehensive step-by-step explanation regarding the preparation of a digital-based RAB using Excel. This session dissected various mandatory components that must be present in the budget, while providing a detailed understanding of the classification and use of each code in the RAB to comply with applicable financial reporting standards."),
            
            tr("Memasuki sesi kedua, fokus beralih pada peningkatan kualitas layanan publik melalui pelatihan SOP alur pelayanan administrasi kepada jajaran perangkat desa lainnya. Pelatihan ini menekankan pentingnya standarisasi alur kerja yang baik, terstruktur, dan efisien untuk memastikan masyarakat Desa Silurah mendapatkan pelayanan administrasi yang cepat dan transparan.", "Entering the second session, the focus shifted to improving the quality of public services through training on administrative service flow SOPs for other village officials. This training emphasized the importance of standardizing a good, structured, and efficient workflow to ensure the people of Silurah Village receive fast and transparent administrative services."),
            
            tr("Sebagai bentuk dedikasi dan upaya menjaga keberlanjutan program, pelatihan ini menghasilkan sebuah luaran (output) fisik berupa buku panduan komprehensif berjudul \"PELITA: Pelatihan Literasi Digital\". Buku saku ini diserahkan kepada pihak desa untuk dijadikan pedoman teknis harian bagi perangkat desa ketika menjalankan tugas-tugas administratif maupun manajerial keuangan.", "As a form of dedication and effort to maintain program sustainability, this training produced a physical output in the form of a comprehensive guidebook entitled \"PELITA: Digital Literacy Training\". This pocketbook was handed over to the village to serve as a daily technical guide for village officials when carrying out administrative and financial managerial tasks."),
            
            tr("Kehadiran program literasi digital ini diharapkan tidak hanya berhenti pada hari pelatihan, melainkan menjadi langkah nyata bagi kemajuan Desa Silurah. Inisiator program berharap modul dan panduan teknis yang telah diberikan dapat diterapkan secara berkelanjutan oleh seluruh jajaran aparatur desa. Melalui digitalisasi penyusunan RAB dan implementasi SOP pelayanan yang terstandar, diharapkan roda pemerintahan Desa Silurah menjadi lebih efisien, transparan, dan mampu mendukung percepatan pembangunan desa secara optimal.", "The presence of this digital literacy program is expected not only to stop on the day of the training, but rather become a real step for the progress of Silurah Village. The program initiators hope the modules and technical guides provided can be implemented sustainably by all ranks of the village apparatus. Through the digitization of RAB preparation and the implementation of standardized service SOPs, it is hoped that the Silurah Village governance wheel will become more efficient, transparent, and able to support the acceleration of village development optimally.")
        ]
    },
    {
        "id": "artikel-sosialisasi-mitigasi-pencemaran-air",
        "judul": tr("Cegah Pencemaran, Mahasiswa KKN Edukasi Warga Desa Silurah Jaga Sumber Mata Air", "Prevent Pollution, KKN Students Educate Silurah Village Residents to Protect Water Springs"),
        "gambar": "artikel_janpier.jpg",
        "tanggal": "27 Juli 2026",
        "penulis": "Janpier Thimoteus Sitepu / Tim II KKN Undip",
        "ringkasan": tr("Edukasi masyarakat mengenai pentingnya menjaga kebersihan sumber mata air dari limbah rumah tangga untuk mencegah pencemaran.", "Community education regarding the importance of keeping water springs clean from household waste to prevent pollution."),
        "isi": [
            tr("Sejumlah mahasiswa Kuliah Kerja Nyata (KKN) Universitas Diponegoro menggelar kegiatan edukasi bertema pencemaran sumber mata air kepada warga Desa Silurah, Senin (27/7/2026). Kegiatan yang dilaksanakan di Balai Desa Silurah ini bertujuan meningkatkan kesadaran masyarakat mengenai pentingnya menjaga kebersihan dan kualitas sumber mata air serta memberikan pemahaman mengenai langkah-langkah sederhana yang dapat dilakukan untuk mencegah pencemaran air di lingkungan sekitar.", "A number of Diponegoro University Student Study Service (KKN) students held an educational activity themed around the pollution of water springs for the residents of Silurah Village on Monday (27/7/2026). The activity, which was held at the Silurah Village Hall, aims to increase community awareness regarding the importance of maintaining the cleanliness and quality of water springs, as well as providing an understanding of simple steps that can be taken to prevent water pollution in the surrounding environment."),
            
            tr("Kegiatan ini dihadiri oleh sekitar 7 perangkat desa, dilanjutkan dengan penyampaian materi oleh mahasiswa KKN. Dalam pemaparannya, mahasiswa menjelaskan berbagai sumber pencemaran yang berpotensi memengaruhi kualitas mata air, terutama yang berasal dari aktivitas rumah tangga, pembuangan sampah, limbah domestik, aktivitas pertanian, serta sanitasi yang kurang baik.", "This activity was attended by around 8 residents, followed by the delivery of material by KKN students. In their presentation, students explained various sources of pollution that have the potential to affect the quality of springs, especially those originating from household activities, garbage disposal, domestic waste, agricultural activities, and poor sanitation."),
            
            tr("Mahasiswa KKN juga menjelaskan bahwa pencemaran sumber mata air tidak hanya dapat memengaruhi kondisi fisik air, tetapi juga berpotensi menimbulkan dampak terhadap kesehatan masyarakat apabila air yang tercemar digunakan untuk kebutuhan sehari-hari. Oleh karena itu, masyarakat perlu memahami pentingnya menjaga lingkungan di sekitar sumber mata air dan mencegah masuknya berbagai jenis limbah ke dalam aliran air.", "KKN students also explained that pollution of water springs can not only affect the physical condition of the water, but also has the potential to impact public health if polluted water is used for daily needs. Therefore, the community needs to understand the importance of protecting the environment around water springs and preventing the entry of various types of waste into the water flow."),
            
            tr("\"Sumber mata air menjadi tumpuan utama warga untuk kebutuhan air minum, memasak, mandi-cuci-kakus (MCK), hingga irigasi pertanian. Ketika sumber ini tercemar, seluruh rantai kehidupan warga ikut terdampak,\" ujar Janpier Thimoteus Sitepu, salah satu anggota tim KKN, dalam sesi pemaparan.", "\"Water springs are the main mainstay of citizens for drinking water, cooking, bathing-washing-toilets (MCK), and agricultural irrigation. When this source is polluted, the entire chain of citizens' lives is affected,\" said Janpier Thimoteus Sitepu, a member of the KKN team, during the presentation session."),
            
            tr("Materi edukasi turut membahas langkah-langkah sederhana yang dapat diterapkan masyarakat untuk meminimalkan risiko pencemaran, seperti tidak membuang sampah dan limbah rumah tangga di sekitar sumber mata air, menjaga kebersihan saluran air, memperhatikan lokasi pembuangan limbah, serta menjaga vegetasi di sekitar area sumber mata air. Masyarakat juga diberikan pemahaman mengenai pentingnya memperhatikan kondisi fisik air, seperti perubahan warna, bau, dan tingkat kekeruhan sebagai indikasi awal adanya perubahan kualitas air.", "The educational material also discussed simple steps that the community can apply to minimize the risk of pollution, such as not disposing of garbage and household waste around water springs, maintaining the cleanliness of waterways, paying attention to waste disposal locations, and maintaining vegetation around the water spring area. The community was also given an understanding of the importance of paying attention to the physical condition of the water, such as changes in color, smell, and turbidity levels as an early indication of changes in water quality."),
            
            tr("Setelah penyampaian materi, kegiatan dilanjutkan dengan penutupan dan dokumentasi bersama. Meskipun tidak terdapat sesi tanya jawab dari warga, penyampaian materi tetap menjadi sarana bagi mahasiswa KKN untuk memberikan informasi mengenai risiko pencemaran serta langkah-langkah yang dapat dilakukan masyarakat dalam menjaga sumber mata air.", "After the material delivery, the activity continued with closing and documentation together. Even though there was no Q&A session from the residents, the delivery of the material remained a means for KKN students to provide information regarding the risks of pollution as well as the steps the community could take to protect water springs."),
            
            tr("Melalui kegiatan edukasi ini, mahasiswa KKN berharap masyarakat Desa Silurah semakin sadar akan pentingnya menjaga kebersihan dan kelestarian sumber mata air. Peningkatan kesadaran tersebut diharapkan dapat diterapkan melalui kebiasaan sederhana dalam kehidupan sehari-hari, seperti tidak membuang sampah sembarangan, menjaga kebersihan lingkungan, serta mencegah berbagai aktivitas yang berpotensi mencemari sumber air.", "Through this educational activity, KKN students hope that the people of Silurah Village will become increasingly aware of the importance of maintaining the cleanliness and sustainability of water springs. This increased awareness is expected to be applied through simple habits in daily life, such as not littering, keeping the environment clean, and preventing various activities that have the potential to pollute water sources."),
            
            tr("Dengan adanya kepedulian bersama, kualitas sumber mata air di Desa Silurah diharapkan tetap terjaga dan dapat dimanfaatkan secara berkelanjutan.", "With mutual concern, the quality of water springs in Silurah Village is expected to be maintained and can be utilized sustainably.")
        ]
    },
    {
        "id": "artikel-buku-administrasi",
        "judul": tr("Dari Balai Desa Silurah, Mahasiswa KKN Universitas Diponegoro Mengambil Langkah untuk Mendukung Administrasi Desa yang Lebih Tertata", "From the Silurah Village Hall, Diponegoro University KKN Students Take Steps to Support More Organized Village Administration"),
        "gambar": "artikel_khanza.jpg", 
        "tanggal": "27 Juli 2026",
        "penulis": "Khanza Salsabila Ahmad / Tim II KKN Undip",
        "ringkasan": tr("Penyusunan Buku Administrasi Pemerintah Desa guna mendukung tertib administrasi dan pengelolaan dokumen di Desa Silurah.", "Preparation of Village Government Administration Books to support orderly administration and document management in Silurah Village."),
        "isi": [
            tr("Mahasiswa KKN Undip memberikan Buku Administrasi Pemerintah Desa kepada Kepala Desa Silurah.", "Undip KKN students gave the Village Government Administration Book to the Silurah Village Head."),
            
            tr("Upaya mendukung tertib administrasi di Desa Silurah dilakukan melalui penyusunan Buku Administrasi Pemerintah Desa sebagai salah satu program kerja monodisiplin mahasiswa Kuliah Kerja Nyata (KKN) Universitas Diponegoro. Program ini dilaksanakan pada Senin (27/7/2026) dengan membantu Pemerintah Desa Silurah menyediakan buku administrasi yang dapat digunakan untuk mendukung pencatatan dan pengelolaan dokumen di kantor desa.", "Efforts to support orderly administration in Silurah Village were carried out through the preparation of the Village Government Administration Book as one of the monodisciplinary work programs of Diponegoro University Student Study Service (KKN) students. This program was implemented on Monday (27/7/2026) by helping the Silurah Village Government provide administration books that can be used to support recording and document management at the village office."),
            
            tr("Dalam pelaksanaan kegiatan, proses penyusunan diawali dengan melakukan koordinasi bersama Pemerintah Desa Silurah untuk mengetahui kebutuhan administrasi yang digunakan dalam kegiatan sehari-hari. Koordinasi dilakukan dengan memperhatikan sistem pencatatan yang sudah berjalan serta kebutuhan perangkat desa dalam mengelola berbagai dokumen dan informasi.", "In implementing the activity, the preparation process began with coordination with the Silurah Village Government to determine the administrative needs used in daily activities. Coordination was carried out by paying attention to the existing recording system and the needs of village officials in managing various documents and information."),
            
            tr("Hasil koordinasi menjadi dasar dalam menentukan format buku yang sesuai dengan kebutuhan Pemerintah Desa Silurah. Penyusunan dilakukan secara bertahap dengan memperhatikan isi, susunan pencatatan, dan petunjuk penggunaan agar buku dapat digunakan dengan mudah oleh perangkat desa.", "The results of the coordination became the basis for determining the book format that suits the needs of the Silurah Village Government. The preparation was carried out gradually by paying attention to the content, recording arrangement, and usage instructions so that the book can be easily used by village officials."),
            
            tr("Sebanyak enam buku administrasi berhasil disusun dalam program kerja tersebut. Buku yang dibuat mencakup Buku Register Administrasi Persuratan, Buku Inventaris dan Hasil Kekayaan Desa, Buku Keputusan Kepala Desa, Buku Peraturan Desa, Buku Agenda, serta Buku Inventaris Hasil-Hasil Pembangunan. Setiap buku dilengkapi dengan format pencatatan yang disesuaikan dengan kebutuhan administrasi desa.", "A total of six administration books were successfully prepared in the work program. The books created include the Correspondence Administration Register Book, Village Wealth Inventory and Results Book, Village Head Decision Book, Village Regulation Book, Agenda Book, and Development Results Inventory Book. Each book is equipped with a recording format tailored to village administrative needs."),
            
            tr("Tidak hanya menyusun format, proses pembuatan buku juga melalui tahap pemeriksaan dan revisi bersama Pemerintah Desa Silurah. Masukan dari perangkat desa digunakan untuk memperbaiki isi dan tampilan buku agar lebih mudah digunakan dalam kegiatan administrasi sehari-hari.", "Not only formatting, the book creation process also went through an inspection and revision stage with the Silurah Village Government. Input from village officials was used to improve the content and appearance of the book to make it easier to use in daily administrative activities."),
            
            tr("Kehadiran buku administrasi diharapkan dapat membantu perangkat desa dalam melakukan pencatatan secara lebih teratur, memudahkan pencarian informasi, serta mendukung penyimpanan data dan dokumen secara lebih rapi. Buku juga dapat menjadi panduan bagi perangkat desa dalam melakukan pencatatan secara konsisten.", "The presence of administration books is expected to help village officials in recording more regularly, making it easier to search for information, and supporting neater data and document storage. The book can also be a guide for village officials in making consistent records."),
            
            tr("Program kerja ini menjadi salah satu bentuk kontribusi mahasiswa KKN dalam mendukung kebutuhan administrasi Pemerintah Desa Silurah. Langkah sederhana melalui penyediaan buku administrasi diharapkan dapat membantu menciptakan pengelolaan dokumen yang lebih tertib dan mendukung pelayanan desa yang berjalan setiap hari.", "This work program is a form of contribution from KKN students in supporting the administrative needs of the Silurah Village Government. The simple step of providing administration books is expected to help create more orderly document management and support daily village services."),
            
            tr("Dari administrasi yang tertata, pelayanan desa dapat berjalan dengan lebih terarah. Dari Desa Silurah, perubahan sederhana dimulai dari pencatatan yang lebih rapi.", "From an organized administration, village services can run with more direction. From Silurah Village, a simple change starts with neater recording.")
        ]
    },
    {
        "id": "artikel-sosialisasi-mitigasi-bencana",
        "judul": tr("Tingkatkan Kesiapsiagaan Sejak Dini, Mahasiswa KKN Edukasi Mitigasi Bencana kepada Siswa SMP Negeri 03 Wonotunggal Satap", "Improve Early Preparedness, KKN Students Educate Disaster Mitigation to Students of SMP Negeri 03 Wonotunggal Satap"),
        "gambar": "artikel_yardan.jpg", 
        "tanggal": "29 Juli 2026",
        "penulis": "Yardan Ahmad Taufiq / Tim II KKN Undip",
        "ringkasan": tr("Edukasi mitigasi bencana untuk anak dan remaja di Desa Silurah guna meningkatkan pemahaman dan kesiapsiagaan menghadapi kondisi darurat.", "Disaster mitigation education for children and adolescents in Silurah Village to improve understanding and preparedness for facing emergency conditions."),
        "isi": [
            tr("Pengetahuan mengenai mitigasi bencana menjadi hal penting yang perlu dikenalkan sejak dini, khususnya bagi anak-anak dan remaja yang tinggal di wilayah dengan potensi bencana alam. Melihat pentingnya hal tersebut, mahasiswa KKN-R TIM II Desa Silurah Universitas Diponegoro melaksanakan Program Sosialisasi Mitigasi Bencana untuk Anak-Anak dan Remaja kepada siswa SMP Negeri 03 Wonotunggal Satap, Desa Silurah, Kecamatan Wonotunggal, Kabupaten Batang, Rabu (29/7/2026).", "Knowledge about disaster mitigation is an important matter that needs to be introduced early on, especially for children and adolescents living in areas with natural disaster potential. Seeing the importance of this, KKN-R TEAM II students of Silurah Village, Diponegoro University, implemented the Disaster Mitigation Socialization Program for Children and Adolescents to students of SMP Negeri 03 Wonotunggal Satap, Silurah Village, Wonotunggal District, Batang Regency, Wednesday (29/7/2026)."),
            
            tr("Kegiatan ini bertujuan untuk meningkatkan pemahaman dan kesiapsiagaan siswa dalam menghadapi bencana yang berpotensi terjadi di lingkungan sekitar. Sosialisasi tidak hanya membahas mengenai jenis-jenis bencana, tetapi juga mengajak siswa mengenali potensi bahaya di lingkungan tempat tinggal serta memahami tindakan yang tepat sebelum, saat, dan setelah bencana terjadi.", "This activity aims to improve students' understanding and preparedness in facing disasters that potentially occur in the surrounding environment. The socialization not only discusses the types of disasters, but also invites students to recognize potential hazards in their living environment and understand the appropriate actions before, during, and after a disaster occurs."),
            
            tr("Siswa mendapatkan edukasi interaktif mengenai berbagai jenis bencana, potensi bahaya yang terdapat di lingkungan sekitar Desa Silurah, serta langkah-langkah mitigasi yang dapat dilakukan untuk mengurangi risiko bencana. Siswa juga diberikan pemahaman mengenai pentingnya mengenali jalur evakuasi dan menentukan tindakan yang tepat ketika terjadi keadaan darurat.", "Students received interactive education regarding various types of disasters, potential hazards found in the environment around Silurah Village, and mitigation steps that can be taken to reduce disaster risks. Students were also given an understanding of the importance of recognizing evacuation routes and determining appropriate actions during an emergency."),
            
            tr("Penyampaian materi dilakukan secara interaktif dengan melibatkan siswa dalam diskusi dan pemahaman mengenai kondisi lingkungan di sekitar mereka. Melalui pendekatan tersebut, siswa tidak hanya diharapkan mampu memahami materi secara teori, tetapi juga dapat menghubungkan pengetahuan yang diperoleh dengan kondisi nyata yang mereka temui dalam kehidupan sehari-hari.", "The delivery of material was done interactively by involving students in discussions and understanding the environmental conditions around them. Through this approach, students are not only expected to be able to understand the material theoretically, but also to connect the knowledge gained with the real conditions they encounter in their daily lives."),
            
            tr("Selain mengenali jenis dan potensi bencana, siswa juga diberikan pemahaman mengenai tiga tahapan penting dalam menghadapi bencana. Sebelum bencana, siswa diajak memahami pentingnya kesiapsiagaan, mengenali potensi bahaya, serta mengetahui perlengkapan dan tindakan yang perlu dipersiapkan. Saat bencana terjadi, siswa diberikan pemahaman mengenai cara menyelamatkan diri, mengikuti jalur evakuasi, dan tetap tenang dalam kondisi darurat. Sementara itu, setelah bencana siswa dikenalkan dengan tindakan yang perlu dilakukan untuk memastikan keselamatan diri dan memahami dampak yang dapat ditimbulkan oleh bencana.", "Besides recognizing the types and potential of disasters, students were also given an understanding of three important stages in facing disasters. Before a disaster, students were invited to understand the importance of preparedness, recognize potential hazards, and know the equipment and actions that need to be prepared. When a disaster occurs, students were given an understanding of how to save themselves, follow evacuation routes, and stay calm in emergency conditions. Meanwhile, after a disaster, students were introduced to actions that need to be taken to ensure personal safety and understand the impacts that can be caused by the disaster."),
            
            tr("<b>Tidak Berhenti pada Siswa</b>", "<b>Not Stopping at Students</b>"),
            
            tr("Program ini tidak hanya berorientasi pada peningkatan pengetahuan siswa, tetapi juga mendorong mereka untuk menjadi bagian dari upaya penyebaran edukasi kebencanaan di lingkungan masing-masing. Para siswa diharapkan dapat menerapkan pengetahuan yang diperoleh serta menyampaikannya kembali kepada keluarga, teman, dan orang-orang terdekat.", "This program is not only oriented towards increasing student knowledge, but also encouraging them to be part of the effort to spread disaster education in their respective environments. The students are expected to be able to apply the knowledge gained and pass it on to their families, friends, and closest people."),
            
            tr("Dengan demikian, informasi mengenai mitigasi bencana tidak berhenti di ruang kelas, tetapi dapat diteruskan kepada masyarakat yang lebih luas. Peran siswa sebagai generasi muda diharapkan dapat membantu membangun kesadaran masyarakat mengenai pentingnya kesiapsiagaan dalam menghadapi bencana.", "Thus, information regarding disaster mitigation does not stop in the classroom, but can be passed on to the wider community. The role of students as the younger generation is expected to help build community awareness regarding the importance of preparedness in facing disasters."),
            
            tr("<b>Membangun Generasi yang Siap Menghadapi Bencana</b>", "<b>Building a Generation Ready to Face Disasters</b>"),
            
            tr("Hasil dari kegiatan menunjukkan bahwa siswa memperoleh pemahaman yang lebih baik mengenai jenis-jenis bencana, potensi bahaya di lingkungan sekitar, serta tindakan yang perlu dilakukan pada setiap tahapan kebencanaan. Siswa juga mulai memahami pentingnya persiapan sebelum bencana, tindakan penyelamatan ketika bencana terjadi, serta langkah yang perlu dilakukan setelah bencana.", "The results of the activity showed that students gained a better understanding of the types of disasters, potential hazards in the surrounding environment, as well as the actions that need to be taken at each stage of a disaster. Students also began to understand the importance of preparation before a disaster, rescue actions when a disaster occurs, and steps that need to be taken after a disaster."),
            
            tr("Melalui kegiatan ini, mahasiswa KKN berharap edukasi mitigasi bencana dapat menjadi bekal bagi siswa untuk lebih peka terhadap kondisi lingkungan dan mampu mengambil tindakan yang tepat ketika menghadapi situasi darurat.", "Through this activity, KKN students hope that disaster mitigation education can serve as a provision for students to be more sensitive to environmental conditions and able to take appropriate action when facing emergency situations."),
            
            tr("\"Harapannya, siswa tidak hanya mengetahui apa itu bencana, tetapi juga mampu memahami apa yang harus dilakukan ketika bencana benar-benar terjadi. Pengetahuan tersebut diharapkan dapat mereka bagikan kepada keluarga dan masyarakat di sekitar,\" ujar Yardan selaku salah satu mahasiswa KKN.", "\"The hope is that students not only know what a disaster is, but are also able to understand what to do when a disaster actually happens. It is hoped that they can share this knowledge with their families and surrounding communities,\" said Yardan as one of the KKN students."),
            
            tr("Program Sosialisasi Mitigasi Bencana untuk Anak-Anak dan Remaja ini menjadi salah satu bentuk kontribusi mahasiswa dalam meningkatkan literasi kebencanaan di Desa Silurah. Edukasi sejak dini diharapkan dapat menciptakan generasi muda yang lebih siap, tanggap, dan sadar terhadap risiko bencana, sehingga mampu berperan dalam membangun masyarakat yang lebih tangguh menghadapi bencana.", "This Disaster Mitigation Socialization Program for Children and Adolescents serves as a form of student contribution in increasing disaster literacy in Silurah Village. Early education is expected to create a younger generation that is more prepared, responsive, and aware of disaster risks, so that they can play a role in building a more resilient community in facing disasters.")
        ]
    },
    {
        "id": "artikel-english-club",
        "judul": tr("Kegiatan English Club: Latihan Introduction sebagai Langkah Awal Keterampilan Berbahasa Inggris", "English Club Activities: Introduction Practice as the First Step in English Language Skills"),
        "gambar": "artikel_zacky.jpg", 
        "tanggal": "29 Juli 2026",
        "penulis": "Maulana Zacky Alfarindra / Tim II KKN Undip", 
        "ringkasan": tr("Pelatihan dasar Bahasa Inggris melalui kegiatan English Club di SMP Negeri 03 Wonotunggal Satap untuk melatih keberanian dan kemampuan komunikasi siswa.", "Basic English training through English Club activities at SMP Negeri 03 Wonotunggal Satap to train students' courage and communication skills."),
        "isi": [
            tr("Upaya pelatihan keterampilan berbahasa Inggris dengan mempelajari materi dasar yang diikuti oleh para siswa dari SMP Negeri 3 Satap Wonotunggal yang berada di desa Silurah, Kecamatan Wonotunggal, Kabupaten Batang, Rabu (29/7/2026). Aktivitas ini diikuti oleh gabungan siswa kelas 7, 8, dan 9. Kegiatan English Club diawali dengan latihan introduction atau perkenalan diri sebagai langkah awal untuk melatih keterampilan berbahasa Inggris peserta. Kegiatan ini bertujuan untuk memperkenalkan penggunaan Bahasa Inggris dalam tahap komunikasi mendasar sekaligus membangun keberanian para peserta untuk berbicara di depan orang lain.", "Efforts to train English language skills by learning basic material attended by students from SMP Negeri 3 Satap Wonotunggal located in Silurah village, Wonotunggal District, Batang Regency, Wednesday (29/7/2026). This activity was attended by a combination of 7th, 8th, and 9th-grade students. The English Club activity began with an introduction practice as a first step to train participants' English skills. This activity aims to introduce the use of English in basic communication stages while building participants' courage to speak in front of others."),
            
            tr("Dalam kegiatan tersebut, peserta diperkenalkan dengan beberapa ungkapan dasar yang dapat digunakan ketika memperkenalkan diri, seperti menyebutkan nama, asal, usia, hobi, serta hal-hal yang disukai. Peserta juga diberikan contoh sederhana mengenai cara memperkenalkan diri dalam Bahasa Inggris agar lebih mudah memahami pola kalimat dan kosakata yang digunakan.", "In this activity, participants were introduced to several basic expressions that can be used when introducing themselves, such as mentioning their name, origin, age, hobbies, and things they like. Participants were also given simple examples of how to introduce themselves in English to make it easier to understand the sentence patterns and vocabulary used."),
            
            tr("Setelah mendapatkan penjelasan, peserta kemudian diberi kesempatan untuk mempraktikkan introduction secara bergantian. Mereka mencoba memperkenalkan diri menggunakan Bahasa Inggris di hadapan peserta lainnya. Kegiatan berlangsung secara interaktif dengan peserta yang mulai berlatih menyampaikan informasi mengenai diri mereka dalam kalimat-kalimat sederhana.", "After receiving an explanation, participants were then given the opportunity to practice the introduction in turns. They tried to introduce themselves using English in front of other participants. The activity took place interactively with participants starting to practice conveying information about themselves in simple sentences."),
            
            tr("Latihan ini tidak hanya berfokus pada penguasaan kosakata dan struktur kalimat, tetapi juga pada keberanian peserta dalam menggunakan Bahasa Inggris secara aktif. Beberapa peserta masih terlihat ragu dalam berbicara, terutama ketika harus menyampaikan perkenalan di depan kelas. Namun, melalui pendampingan dan latihan secara bertahap, peserta mulai menunjukkan keberanian untuk mencoba berbicara menggunakan Bahasa Inggris.", "This practice not only focuses on mastering vocabulary and sentence structure, but also on the participants' courage in using English actively. Some participants still looked hesitant to speak, especially when they had to deliver an introduction in front of the class. However, through gradual mentoring and practice, participants began to show the courage to try speaking using English."),
            
            tr("Kegiatan introduction menjadi permulaan bagi rangkaian pembelajaran English Club selanjutnya. Melalui kegiatan ini, peserta diharapkan memiliki dasar dan kepercayaan diri untuk menggunakan Bahasa Inggris dalam komunikasi sederhana. Selain itu, kegiatan ini menjadi langkah awal untuk menciptakan suasana belajar yang menyenangkan, interaktif, dan mendorong peserta untuk tidak takut melakukan kesalahan ketika belajar Bahasa Inggris.", "The introduction activity became the beginning of the subsequent English Club learning series. Through this activity, participants are expected to have the foundation and self-confidence to use English in simple communication. In addition, this activity is the first step to creating a fun, interactive learning atmosphere and encouraging participants not to be afraid of making mistakes when learning English."),
            
            tr("Dengan adanya English Club, latihan keterampilan berbahasa Inggris diharapkan dapat dilakukan secara berkelanjutan melalui berbagai aktivitas, seperti percakapan sederhana, pengenalan kosakata, storytelling, permainan edukatif, dan kegiatan lain yang dapat mendorong peserta untuk menggunakan Bahasa Inggris secara aktif.", "With the English Club, English language skills training is expected to be carried out sustainably through various activities, such as simple conversations, vocabulary introduction, storytelling, educational games, and other activities that can encourage participants to use English actively.")
        ]
    },
    {
        "id": "artikel-langkah-kecil-silurah",
        "judul": tr("Dorong Semangat Melanjutkan Pendidikan, Mahasiswa KKN Berikan Psikoedukasi bagi Siswa SMP Negeri 03 Wonotunggal Satap", "Encourage the Spirit to Continue Education, KKN Students Provide Psychoeducation for Students of SMP Negeri 03 Wonotunggal Satap"),
        "gambar": "artikel_aiko.jpg", 
        "tanggal": "30 Juli 2026",
        "penulis": "Aiko Nashita Johara / Tim II KKN Undip",
        "ringkasan": tr("Psikoedukasi untuk memotivasi siswa SMP agar melanjutkan pendidikan dan memberikan alternatif solusi seperti beasiswa bagi yang terkendala biaya.", "Psychoeducation to motivate junior high school students to continue their education and provide alternative solutions such as scholarships for those with financial constraints."),
        "isi": [
            tr("Melanjutkan pendidikan ke jenjang yang lebih tinggi menjadi salah satu langkah penting bagi generasi muda dalam mempersiapkan masa depan. Namun, kondisi lingkungan dan keterbatasan akses terkadang menjadi salah satu pertimbangan siswa dalam menentukan pilihan setelah menyelesaikan pendidikan SMP. Melihat kondisi tersebut, mahasiswa KKN melaksanakan kegiatan Psikoedukasi Motivasi Melanjutkan Pendidikan kepada siswa SMP Negeri 03 Wonotunggal Satap, Desa Silurah, Kecamatan Wonotunggal, Kabupaten Batang, Jumat (30/7/2026).", "Continuing education to a higher level is an important step for the younger generation in preparing for the future. However, environmental conditions and limited access sometimes become considerations for students in making choices after completing junior high school. Seeing this condition, KKN students carried out a Psychoeducational Motivation to Continue Education activity for students of SMP Negeri 03 Wonotunggal Satap, Silurah Village, Wonotunggal District, Batang Regency, Friday (30/7/2026)."),
            
            tr("Kegiatan ini dilaksanakan sebagai upaya untuk meningkatkan pemahaman siswa mengenai pentingnya pendidikan, menumbuhkan motivasi untuk melanjutkan sekolah, serta membantu siswa mulai merencanakan masa depan sesuai dengan cita-cita yang dimiliki.", "This activity was carried out as an effort to improve students' understanding of the importance of education, foster motivation to continue school, and help students begin planning their future according to their aspirations."),
            
            tr("<b>Melihat Tantangan Pendidikan di Desa Silurah</b>", "<b>Seeing Educational Challenges in Silurah Village</b>"),
            
            tr("Dalam proses pelaksanaan KKN, mahasiswa memperoleh gambaran mengenai kondisi pendidikan di lingkungan Desa Silurah. Berdasarkan informasi yang disampaikan oleh salah satu Ketua RT setempat, terdapat beberapa anak yang memilih untuk tidak melanjutkan pendidikan ke jenjang SMA setelah menyelesaikan SMP. Salah satu pertimbangannya adalah jarak sekolah yang cukup jauh, sehingga sebagian anak memilih untuk segera bekerja setelah menyelesaikan pendidikan SMP.", "During the KKN implementation process, students gained an overview of the educational conditions in the Silurah Village environment. Based on information conveyed by one of the local RT Heads, there are some children who choose not to continue their education to high school after completing junior high school. One of the considerations is the considerable distance to school, so some children choose to work immediately after completing junior high school."),
            
            tr("Kondisi tersebut menunjukkan bahwa keputusan untuk tidak melanjutkan pendidikan tidak selalu disebabkan oleh kurangnya keinginan untuk belajar. Faktor akses, jarak, kondisi keluarga, maupun pertimbangan untuk segera bekerja juga dapat memengaruhi pilihan siswa dalam menentukan masa depannya.", "This condition indicates that the decision not to continue education is not always caused by a lack of desire to learn. Factors such as access, distance, family conditions, as well as considerations to work immediately can also influence a student's choice in determining their future."),
            
            tr("Oleh karena itu, mahasiswa KKN berupaya menghadirkan edukasi yang tidak hanya mendorong siswa untuk melanjutkan sekolah, tetapi juga memberikan pemahaman mengenai berbagai pilihan dan solusi yang dapat dipertimbangkan ketika menghadapi hambatan dalam melanjutkan pendidikan.", "Therefore, KKN students strive to present education that not only encourages students to continue school but also provides an understanding of various choices and solutions that can be considered when facing obstacles in continuing education."),
            
            tr("<b>Tidak Hanya Mengajak, tetapi Memberikan Solusi</b>", "<b>Not Only Inviting, but Providing Solutions</b>"),
            
            tr("Dalam kegiatan psikoedukasi, siswa mendapatkan materi mengenai pentingnya pendidikan, motivasi dalam meraih cita-cita, serta perencanaan masa depan. Materi disampaikan secara interaktif melalui pemaparan, diskusi, dan ice breaking agar siswa dapat terlibat secara aktif.", "In the psychoeducational activity, students received material on the importance of education, motivation in achieving goals, and future planning. The material was delivered interactively through presentations, discussions, and ice breaking so that students could be actively involved."),
            
            tr("Selain membahas manfaat melanjutkan pendidikan, siswa juga dikenalkan dengan berbagai alternatif yang dapat membantu mengatasi hambatan pendidikan. Salah satunya adalah informasi mengenai beasiswa dan berbagai bentuk dukungan pendidikan yang dapat dimanfaatkan oleh siswa apabila terkendala biaya.", "Besides discussing the benefits of continuing education, students were also introduced to various alternatives that can help overcome educational barriers. One of them is information about scholarships and various forms of educational support that can be utilized by students if they are constrained by costs."),
            
            tr("Siswa juga diajak memahami bahwa keterbatasan tertentu tidak selalu berarti harus menghentikan pendidikan. Dengan mencari informasi, berdiskusi dengan orang tua dan guru, serta mengenali berbagai kesempatan yang tersedia, siswa dapat mempertimbangkan pilihan yang lebih sesuai dengan kondisi dan tujuan masa depan mereka.", "Students were also invited to understand that certain limitations do not always mean having to stop education. By seeking information, discussing with parents and teachers, and recognizing various available opportunities, students can consider choices that are more suitable for their conditions and future goals."),
            
            tr("Melalui pendekatan tersebut, mahasiswa KKN berusaha memberikan perspektif yang lebih realistis kepada siswa. Motivasi untuk melanjutkan pendidikan tidak hanya disampaikan dalam bentuk ajakan, tetapi juga disertai dengan informasi mengenai langkah dan alternatif yang dapat dilakukan untuk menghadapi berbagai hambatan.", "Through this approach, KKN students tried to provide a more realistic perspective to students. Motivation to continue education was not only conveyed in the form of an invitation, but was also accompanied by information regarding steps and alternatives that can be taken to face various obstacles."),
            
            tr("<b>Menuliskan Cita-Cita, Merencanakan Masa Depan</b>", "<b>Writing Down Aspirations, Planning the Future</b>"),
            
            tr("Salah satu kegiatan yang dilakukan dalam psikoedukasi adalah \"Pohon Cita-Cita\". Siswa diminta menuliskan cita-cita dan harapan mereka pada bagian pohon yang telah disediakan. Aktivitas ini menjadi sarana bagi siswa untuk mengenali tujuan yang ingin dicapai sekaligus mulai memikirkan langkah yang diperlukan untuk mewujudkannya.", "One of the activities carried out in the psychoeducation was the \"Tree of Aspirations\". Students were asked to write down their goals and hopes on the provided tree parts. This activity became a means for students to recognize the goals they want to achieve while starting to think about the steps needed to realize them."),
            
            tr("Kegiatan juga dilengkapi dengan diskusi mengenai hubungan antara cita-cita, pendidikan, dan rencana masa depan. Siswa diberikan kesempatan untuk menyampaikan pendapat serta membayangkan pilihan pendidikan dan pekerjaan yang sesuai dengan keinginan mereka.", "The activity was also complemented by a discussion regarding the relationship between goals, education, and future plans. Students were given the opportunity to express their opinions and imagine educational and career choices that suit their desires."),
            
            tr("Dengan demikian, siswa tidak hanya diajak untuk memiliki cita-cita, tetapi juga memahami bahwa cita-cita membutuhkan proses, usaha, dan perencanaan yang dilakukan secara bertahap.", "Thus, students are not only invited to have goals, but also to understand that goals require process, effort, and planning carried out gradually."),
            
            tr("<b>Membangun Motivasi untuk Melangkah Lebih Jauh</b>", "<b>Building Motivation to Go Further</b>"),
            
            tr("Kegiatan yang diikuti oleh kurang dari 30 siswa ini mendapatkan respons positif dari peserta. Siswa terlibat dalam diskusi, mengikuti ice breaking, serta berpartisipasi dalam kegiatan Pohon Cita-Cita.", "The activity, which was attended by less than 30 students, received a positive response from the participants. Students were involved in discussions, participated in ice breaking, and participated in the Tree of Aspirations activity."),
            
            tr("Hasil kegiatan menunjukkan bahwa siswa memperoleh pemahaman yang lebih baik mengenai pentingnya pendidikan dan mampu mulai merencanakan masa depan berdasarkan cita-cita yang mereka miliki. Siswa juga memperoleh wawasan mengenai alternatif yang dapat dipertimbangkan ketika menghadapi hambatan dalam melanjutkan pendidikan, termasuk pentingnya mencari informasi mengenai kesempatan beasiswa dan dukungan pendidikan.", "The results of the activity showed that students gained a better understanding of the importance of education and were able to start planning for the future based on their goals. Students also gained insights into alternatives that can be considered when facing obstacles in continuing their education, including the importance of seeking information regarding scholarship opportunities and educational support."),
            
            tr("\"Kami berharap siswa tidak hanya memiliki cita-cita, tetapi juga memahami bahwa ada berbagai jalan yang bisa ditempuh untuk mencapainya. Ketika ada hambatan untuk melanjutkan sekolah, siswa perlu mengetahui bahwa mereka dapat mencari informasi dan memanfaatkan berbagai kesempatan yang tersedia, salah satunya melalui beasiswa,\" ujar Aiko, salah satu pelaksana kegiatan.", "\"We hope that students not only have goals but also understand that there are various paths that can be taken to achieve them. When there are obstacles to continuing school, students need to know that they can seek information and utilize various available opportunities, one of which is through scholarships,\" said Aiko, one of the activity implementers."),
            
            tr("<b>Pendidikan sebagai Langkah Menuju Masa Depan</b>", "<b>Education as a Step Towards the Future</b>"),
            
            tr("Melalui kegiatan Psikoedukasi Motivasi Melanjutkan Pendidikan, mahasiswa KKN berupaya memberikan pemahaman bahwa perencanaan masa depan dapat dimulai sejak bangku SMP. Siswa didorong untuk mengenali cita-cita, memahami pentingnya pendidikan, serta mengetahui berbagai pilihan yang dapat dilakukan untuk menghadapi hambatan dalam perjalanan pendidikan.", "Through the Psychoeducational Motivation to Continue Education activity, KKN students seek to provide an understanding that future planning can start from junior high school. Students are encouraged to recognize their goals, understand the importance of education, and know the various choices that can be made to face obstacles in their educational journey."),
            
            tr("Kegiatan ini diharapkan dapat memberikan bekal bagi siswa untuk membuat keputusan yang lebih terarah mengenai masa depan. Dengan adanya motivasi, informasi, dan dukungan yang tepat, siswa diharapkan tidak mudah menganggap keterbatasan sebagai akhir dari perjalanan pendidikan.", "This activity is expected to provide provision for students to make more directed decisions regarding the future. With proper motivation, information, and support, students are expected not to easily consider limitations as the end of their educational journey."),
            
            tr("Psikoedukasi Motivasi Melanjutkan Pendidikan menjadi salah satu bentuk kontribusi mahasiswa KKN dalam mendukung peningkatan kesadaran pendidikan di Desa Silurah. Dari mengenali cita-cita, memahami berbagai pilihan, hingga mulai menyusun rencana masa depan, setiap langkah kecil diharapkan dapat menjadi awal bagi siswa untuk mewujudkan masa depan yang mereka impikan.", "Psychoeducational Motivation to Continue Education serves as a form of contribution from KKN students in supporting increased educational awareness in Silurah Village. From recognizing goals, understanding various choices, to starting to formulate future plans, every small step is expected to be a beginning for students to realize the future they dream of.")
        ]
    },
    {
        "id": "artikel-think-before-you-click",
        "judul": tr("Think Before You Click: Katakan Tidak pada Judi Online, Mahasiswa KKN Tim II Desa Silurah Edukasi Siswa SMP", "Think Before You Click: Say No to Online Gambling, KKN Team II Students Educate Junior High Students in Silurah Village"),
        "gambar": "artikel_hilda.jpg",
        "tanggal": "30 Juli 2026",
        "penulis": "Hilda Rahmah Ardita / Tim II KKN Undip",
        "ringkasan": tr("Edukasi untuk siswa SMP mengenai bahaya dan dampak negatif judi online agar remaja lebih bijak dan kritis dalam bermedia digital.", "Education for junior high school students regarding the dangers and negative impacts of online gambling so teenagers are wiser and more critical in digital media."),
        "isi": [
            tr("Mahasiswa Kuliah Kerja Nyata (KKN) Universitas Diponegoro Tim II Desa Silurah melaksanakan program kerja bertajuk \"Think Before You Click: Katakan Tidak pada Judi Online\" di SMP Negeri 03 Wonotunggal Satap, Jumat (30/7/2026). Kegiatan ini ditujukan kepada siswa SMP sebagai upaya meningkatkan kesadaran mengenai bahaya dan dampak negatif judi online di tengah perkembangan teknologi digital.", "Diponegoro University Student Study Service (KKN) Team II students of Silurah Village implemented a work program entitled \"Think Before You Click: Say No to Online Gambling\" at SMP Negeri 03 Wonotunggal Satap, Friday (30/7/2026). This activity is aimed at junior high school students as an effort to raise awareness about the dangers and negative impacts of online gambling amidst the development of digital technology."),
            
            tr("Kegiatan diawali dengan penyampaian materi edukasi mengenai judi online, mulai dari risiko hingga berbagai dampak yang dapat ditimbulkan. Siswa juga diajak untuk berdiskusi mengenai fenomena judi online yang semakin mudah dijumpai melalui akses internet dan media digital.", "The activity began with the delivery of educational materials regarding online gambling, from risks to the various impacts it can cause. Students were also invited to discuss the phenomenon of online gambling, which is increasingly easy to find through internet access and digital media."),
            
            tr("Pada awal kegiatan, siswa cenderung masih pasif dalam mengikuti diskusi. Namun, setelah materi disampaikan, siswa mulai menunjukkan ketertarikan dan lebih aktif dalam berdiskusi. Interaksi tersebut menjadi salah satu bagian penting dalam kegiatan karena memberikan ruang bagi siswa untuk memahami materi sekaligus menyampaikan pendapat mereka.", "At the beginning of the activity, students tended to be passive in participating in the discussion. However, after the material was delivered, students started showing interest and became more active in discussions. This interaction became an important part of the activity because it provided space for students to understand the material while expressing their opinions."),
            
            tr("Melalui program \"Think Before You Click\", mahasiswa KKN berupaya menanamkan pemahaman kepada siswa bahwa penggunaan teknologi perlu disertai dengan sikap bijak dan kritis. Kemudahan akses terhadap internet juga perlu diimbangi dengan kemampuan untuk mengenali serta menghindari konten dan aktivitas digital yang berisiko, termasuk judi online.", "Through the \"Think Before You Click\" program, KKN students seek to instill an understanding in students that the use of technology must be accompanied by a wise and critical attitude. The ease of internet access also needs to be balanced with the ability to recognize and avoid risky digital content and activities, including online gambling."),
            
            tr("Kegiatan ini diharapkan dapat memberikan pemahaman yang lebih baik kepada siswa mengenai bahaya judi online serta mendorong mereka untuk lebih berhati-hati dalam menggunakan internet. Dengan membangun kesadaran sejak usia remaja, siswa diharapkan mampu mengambil keputusan yang lebih bijak dan berani mengatakan tidak pada judi online.", "This activity is expected to provide a better understanding to students regarding the dangers of online gambling and encourage them to be more careful in using the internet. By building awareness from adolescence, students are expected to be able to make wiser decisions and dare to say no to online gambling.")
        ]
    },
    {
        "id": "artikel-happy-eating-happy-growing",
        "judul": tr("Dukung Tumbuh Kembang Optimal Melalui Pembekalan Ibu Balita Atasi GTM Lewat Inovasi Gizi", "Support Optimal Growth and Development Through Equipping Toddler Mothers to Overcome GTM via Nutritional Innovation"),
        "gambar": "artikel_alle.jpg",
        "tanggal": "1 Agustus 2026",
        "penulis": "Allesandra Shafira Putri / Tim II KKN Undip",
        "ringkasan": tr("Edukasi untuk mengatasi permasalahan Gerakan Tutup Mulut (GTM) pada balita disertai pengenalan inovasi olahan gizi sehat berupa Sempol.", "Education to overcome the problem of Closed Mouth Movement (GTM) in toddlers accompanied by the introduction of healthy nutritional processed innovation in the form of Sempol."),
        "isi": [
            tr("Permasalahan sulit makan pada balita atau yang dikenal dengan istilah Gerakan Tutup Mulut (GTM) menjadi salah satu keluhan yang kerap dihadapi para ibu di Desa Silurah, Kecamatan Wonotunggal, Kabupaten Batang. Menjawab persoalan tersebut, Allesandra Shafira, mahasiswa Kuliah Kerja Nyata (KKN) Universitas Diponegoro (Undip) Tim II, menghadirkan program edukasi bertajuk \"Happy Eating, Happy Growing: Inovasi Gizi Cegah GTM\" bagi ibu balita di Dukuh Sipudang, Desa Silurah, Sabtu (1/82026).", "The problem of difficulty eating in toddlers, known as the Closed Mouth Movement (GTM), is one of the complaints frequently faced by mothers in Silurah Village, Wonotunggal District, Batang Regency. Answering this problem, Allesandra Shafira, a student of Diponegoro University (Undip) Student Study Service (KKN) Team II, presented an educational program entitled \"Happy Eating, Happy Growing: Nutritional Innovation to Prevent GTM\" for mothers of toddlers in Sipudang Hamlet, Silurah Village, Saturday (1/8/2026)."),
            
            tr("Berbeda dari edukasi gizi pada umumnya, program ini tidak berhenti pada pemaparan teori, melainkan langsung menghadirkan solusi yang dapat dipraktikkan. Ibu balita diajak mengenali akar penyebab GTM sekaligus diperkenalkan pada contoh inovasi makanan yang dirancang untuk membangkitkan kembali nafsu makan anak. Pendekatan ini dipilih karena banyak ibu masih menganggap penolakan makan sebagai hal biasa, padahal apabila dibiarkan dapat mengganggu pemenuhan gizi serta tumbuh kembang anak.", "Different from general nutrition education, this program does not stop at theoretical presentations but immediately presents actionable solutions. Mothers of toddlers were invited to recognize the root causes of GTM while being introduced to examples of food innovations designed to revive a child's appetite. This approach was chosen because many mothers still consider food refusal as a normal occurrence, even though if left unchecked it can disrupt nutritional fulfillment and a child's growth and development."),
            
            tr("Materi edukasi disusun dalam bentuk PowerPoint yang mengupas pengertian GTM, faktor penyebab, hingga dampaknya terhadap status gizi anak. Sebagai penguat, Allesandra Shafira memperkenalkan inovasi makanan berupa Sempol yang memadukan nasi, ayam, wortel, dan tahu sebagai sumber gizi lengkap dalam satu sajian praktis. Dikemas menarik namun tetap memperhatikan kandungan gizi yang dibutuhkan balita, inovasi ini menjadi solusi sederhana bagi anak yang sulit makan. Melalui pendekatan tersebut, ibu balita memperoleh gambaran konkret mengenai cara menghadapi balita yang GTM sekaligus memenuhi kebutuhan gizi anak secara menyeluruh.", "The educational material was compiled in PowerPoint format which explores the definition of GTM, causal factors, and its impact on a child's nutritional status. As reinforcement, Allesandra Shafira introduced a food innovation in the form of Sempol which combines rice, chicken, carrots, and tofu as a complete nutritional source in one practical dish. Packaged attractively while still paying attention to the nutritional content needed by toddlers, this innovation is a simple solution for children who have difficulty eating. Through this approach, mothers of toddlers obtain a concrete picture of how to deal with toddlers with GTM while meeting a child's comprehensive nutritional needs."),
            
            tr("Antusiasme peserta terlihat jelas sepanjang kegiatan. Sejumlah ibu aktif berbagi pengalaman mengenai kesulitan yang mereka hadapi, sementara suasana diskusi yang cair membuat materi lebih mudah diterima. Interaksi dua arah ini menjadikan edukasi terasa lebih dekat dengan persoalan sehari-hari yang dialami peserta.", "The enthusiasm of the participants was evident throughout the activity. Several mothers actively shared their experiences regarding the difficulties they faced, while the fluid discussion atmosphere made the material easier to accept. This two-way interaction made the education feel closer to the everyday problems experienced by the participants."),
            
            tr("Program ini pun membuahkan hasil yang nyata. Pemahaman ibu balita mengenai penyebab dan dampak GTM meningkat, dan mereka memperoleh contoh inovasi makanan yang dapat langsung dipraktikkan secara mandiri. Capaian tersebut menjadi bukti bahwa edukasi gizi dapat berjalan efektif ketika disertai solusi yang aplikatif.", "This program also yielded tangible results. Toddler mothers' understanding of the causes and impacts of GTM increased, and they obtained examples of food innovations that could be directly practiced independently. This achievement proves that nutrition education can run effectively when accompanied by applicable solutions."),
            
            tr("Ke depan, program ini diharapkan dapat mendorong para ibu di Desa Silurah untuk terus menjaga pola pemberian makan yang tepat. Dengan penanganan GTM yang sesuai serta pemanfaatan inovasi makanan, diharapkan nafsu makan, status gizi, dan tumbuh kembang balita di Dukuh Sipudang dapat terus meningkat secara optimal.", "Going forward, this program is expected to encourage mothers in Silurah Village to continue maintaining proper feeding patterns. With appropriate handling of GTM and the utilization of food innovations, it is hoped that the appetite, nutritional status, and growth and development of toddlers in Sipudang Hamlet can continue to increase optimally."),
            
            tr("<b>Tentang Program</b>", "<b>About the Program</b>"),
            
            tr("\"Happy Eating, Happy Growing: Inovasi Gizi Cegah GTM\" merupakan program sosial kemasyarakatan yang dirancang dan dilaksanakan oleh Allesandra Shafira, mahasiswa KKN Universitas Diponegoro Tim II, di Desa Silurah, Kecamatan Wonotunggal, Kabupaten Batang. Program ini berfokus pada edukasi penyebab dan dampak GTM serta pengenalan inovasi makanan sebagai solusi praktis untuk meningkatkan nafsu makan dan memperbaiki status gizi balita.", "\"Happy Eating, Happy Growing: Nutritional Innovation to Prevent GTM\" is a social community program designed and implemented by Allesandra Shafira, a student of Diponegoro University KKN Team II, in Silurah Village, Wonotunggal District, Batang Regency. This program focuses on educating the causes and impacts of GTM as well as introducing food innovations as a practical solution to increase appetite and improve toddlers' nutritional status.")
        ]
    }
]

STATS = [
    {"label": tr("Destinasi Wisata", "Tourist Destinations"), "value": "7", "icon": "🏞️", "anchor": "info-wisata"},
    {"label": tr("Dusun Wilayah", "Hamlets"), "value": "6", "icon": "🏘️", "anchor": "info-dusun"},
    {"label": tr("Sekolah", "Schools"), "value": "5", "icon": "🏫", "anchor": "info-sekolah"},
    {"label": tr("Posyandu", "Healthcare Centers"), "value": "5", "icon": "🩺", "anchor": "info-posyandu"},
]

WISATA_DATA = [
    {
        "nama": "Curug Bidadari",
        "desc": tr(
            "Air terjun alami dengan pemandangan pegunungan yang asri dan udara sejuk.",
            "Explore the beauty of a hidden waterfall flowing from pure mountain springs."
        ),
        "img": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Curug Bidadari.jpg')}",
        "img_id": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Curug Bidadari_ID.jpg')}",
        "img_en": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Curug Bidadari_EN.jpg')}",
        "lat": -7.08135339729419, "lon": 109.75483311219776,
        "link_maps": "https://maps.app.goo.gl/CncoFsTgcREPtZXd7",
    },
    {
        "nama": "Curug Kalirogno",
        "desc": tr(
            "Destinasi air terjun tersembunyi dengan aliran sungai jernih dan kolam alami.",
            "A hidden waterfall destination with clear stream flows and a natural pool."
        ),
        "img": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Curug Kalirogno.jpg')}",
        "img_id": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Curug Kalirogno_ID.jpg')}",
        "img_en": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Curug Kalirogno_EN.jpg')}",
        "lat": -7.1185, "lon": 109.8680,
        "link_maps": "https://maps.app.goo.gl/CncoFsTgcREPtZXd7",
    },
    {
        "nama": "Taman Syailendra",
        "desc": tr(
            "Kawasan taman wisata alam dan edukasi dengan lanskap pegunungan yang menawan.",
            "An educational nature park area with charming mountain landscapes."
        ),      
        "img": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Taman Syailendra.jpg')}",
        "img_id": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Taman Syailendra_ID.jpg')}",
        "img_en": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Taman Syailendra_EN.jpg')}",
        "lat": -7.083100470745881, "lon": 109.77427505676775,
        "link_maps": "https://maps.app.goo.gl/9TAwJFkZ1qjrwEB8A",
    },
    {
        "nama": "Situs Punden Berundak",
        "desc": tr(
            "Situs cagar budaya prasejarah megalitikum peninggalan leluhur desa.",
            "A megalithic prehistoric cultural heritage site from the village ancestors."
        ),  
        "img": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Punden Berundak.jpg')}",
        "img_id": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Punden Berundak_ID.jpg')}",
        "img_en": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Punden Berundak_EN.jpg')}",
        "dusun": "Dusun Batur", 
        "lat": -7.085509531467704, "lon": 109.76952706821783,
        "link_maps": "https://maps.app.goo.gl/Lz3ryLVuD4LwWt4GA",
    },
    {
        "nama": "Arca Ganesha",
        "desc": tr(
            "Situs arca kuno peninggalan era sejarah klasik di Desa Silurah.",
            "An ancient statue site from the classical historical era in Silurah Village."
        ),  
        "img": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Ganesha.jpg')}",
        "img_id": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Ganesha_ID.jpg')}",
        "img_en": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Ganesha_EN.jpg')}",
        "lat": -7.077144063062202, "lon": 109.7575725307554,
        "link_maps": "https://maps.app.goo.gl/Mkh1fp25AHCmWLPq5",
    },
    {
        "nama": "Gunung Kobar",
        "desc": tr(
            "Spot dataran tinggi favorit untuk menikmati sunrise dan lautan kabut pagi.",
            "A favorite highland spot to enjoy the sunrise and morning sea of fog."
        ),  
        "img": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Gunung Kobar.jpg')}",
        "img_id": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Gunung Kobar_ID.jpg')}",
        "img_en": f"data:image/jpeg;base64,{get_base64_image(ASSETS_DIR / 'Gunung Kobar_EN.jpg')}",
        "lat": -7.109675292850821, "lon": 109.76024696252469,
        "link_maps": "https://maps.app.goo.gl/oy7aev5VSkBiaVqZ7",
    },
]

MAP_POINTS = pd.DataFrame(
    {
        "lat": -7.1123 + np.random.randn(18) * 0.004,
        "lon": 109.8654 + np.random.randn(18) * 0.004,
    }
)

POPULATION_DATA = pd.DataFrame(
    {
        "Dusun": ["Krajan", "Batur", "Sipudang", "Simangli", "Pomahan", "Pomahan"],
        "Laki-laki": [1, 1, 1, 1, 1, 1],
        "Perempuan": [1, 1, 1, 1, 1, 1],
    }
).set_index("Dusun")

AGE_DATA = pd.DataFrame(
    {
        "Kelompok Usia": ["0-14", "15-24", "25-54", "55-64", "65+"],
        "Jumlah Jiwa": [820, 615, 1740, 430, 260],
    }
).set_index("Kelompok Usia")

LAND_USE_DATA = pd.DataFrame(
    {
        "Penggunaan Lahan": ["Pemukiman", "Persawahan", "Perkebunan", "Kuburan", "Pekarangan", "Perkantoran", "Prasarana Umum"],
        "Luas (Ha)": [0.51, 36.00, 67.98, 2.00, 25.00, 0.29, 8.31],
    }
).set_index("Penggunaan Lahan")

# --------------------------------------------------------------------------
# GLOBAL CSS
# --------------------------------------------------------------------------
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

    <style>
    :root{
        --primary:#2C4C3B;
        --primary-light:#3E5C48;
        --secondary:#4A3525;
        --bg:#FAF9F5;
        --card-bg:#FFFFFF;
        --text-dark:#22281F;
        --text-muted:#6B6459;
        --border-soft:#E9E4D8;
    }

    html, body, [class*="css"]{
        font-family:'Inter', sans-serif;
        color:var(--text-dark);
        scroll-behavior: smooth;
        overflow-x: hidden !important;
    }

    .stApp{
        background:var(--bg);
        overflow-x: hidden !important;
    }

    #MainMenu, footer, [data-testid="stToolbar"], header[data-testid="stHeader"], div[data-testid="stDecoration"] {
        display: none !important;
        pointer-events: none !important;
        visibility: hidden !important;
        height: 0px !important;
        width: 0px !important;
    }

    .block-container{
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }

    div[data-testid="stVerticalBlock"] > div:has(> div.hero-anchor){
        margin-top: -1rem;
    }

    h1, h2, h3, h4{
        font-family:'Plus Jakarta Sans', sans-serif;
        color:var(--text-dark);
        font-weight:700;
    }

    /* ---------- Tabs Navigasi (Modern Floating Pill Style) ---------- */
    /* 1. Hilangkan garis panjang di bawah tab & reset kontainer list */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px !important;
        background-color: transparent !important;
        border: none !important;
        border-bottom: none !important;
        padding: 0 !important;
        margin-bottom: 25px !important;
    }

    /* 2. BUNUH garis warna (highlight bar & border) bawaan Streamlit yang bikin kaku */
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
        width: 0px !important;
        height: 0px !important;
        background: transparent !important;
    }

    /* 3. Bentuk tombol tab menjadi Kapsul Lonjong Mulus (Rounded Pill) */
    .stTabs [data-baseweb="tab"] {
        height: 42px !important;
        background-color: #FFFFFF !important; /* Latar putih bersih saat tidak aktif */
        border: 1px solid rgba(44, 76, 59, 0.18) !important;
        border-radius: 50px !important; /* <--- Kunci mutlak biar melengkung, gak kotak */
        padding: 0px 24px !important;
        outline: none !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
    }

    /* 4. Paksa warna teks agar TIDAK BIRU (Target ke seluruh elemen teks di dalamnya) */
    .stTabs [data-baseweb="tab"] *, 
    .stTabs [data-baseweb="tab"] p, 
    .stTabs [data-baseweb="tab"] span {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #5C655E !important; /* Warna hijau abu estetik, bukan biru */
        text-decoration: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 5. Efek melayang halus saat mouse geser ke atas tab (Hover) */
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(44, 76, 59, 0.08) !important;
        transform: translateY(-2px) !important;
        border-color: #2C4C3B !important;
        box-shadow: 0 6px 12px rgba(44, 76, 59, 0.1) !important;
    }
    .stTabs [data-baseweb="tab"]:hover * {
        color: #2C4C3B !important;
    }

    /* 6. TAB AKTIF (Sedang Dipilih) - Hijau elegan mulus tanpa garis/kotak abu-abu */
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #2C4C3B 0%, #3E5C48 100%) !important;
        border: 1px solid #2C4C3B !important;
        border-radius: 50px !important;
        box-shadow: 0 6px 18px rgba(44, 76, 59, 0.28) !important;
        transform: translateY(-2px) !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] * {
        color: #FFFFFF !important; /* Teks otomatis jadi putih bersih */
    }

    /* 7. Hilangkan efek fokus/garis kotak saat tombol diklik */
    .stTabs [data-baseweb="tab"]:focus,
    .stTabs [data-baseweb="tab"]:focus-visible {
        outline: none !important;
        box-shadow: none !important;
    }

    .hero-anchor{height:0;}

    .hero-banner{
        position: relative !important;
        width: 100vw !important;
        left: 50% !important;
        margin-left: -50vw !important;
        margin-right: -50vw !important;
        height: 420px;
        margin-top: -1.5rem !important;
        background-image: __HERO_BG__;
        background-size: cover;
        background-position: center;
        -webkit-mask-image: linear-gradient(to bottom, black 62%, transparent 100%);
        mask-image: linear-gradient(to bottom, black 62%, transparent 100%);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .hero-overlay{
        position:absolute;
        inset:0;
        background:linear-gradient(180deg, rgba(20,30,22,0.55) 0%, rgba(20,30,22,0.72) 55%, rgba(20,30,22,0.9) 100%);
    }

    .hero-content{
        position:relative;
        z-index:2;
        text-align:center;
        color:#FFFFFF;
        padding:0 1rem;
    }

    .hero-eyebrow{
        font-family:'Plus Jakarta Sans', sans-serif;
        font-size:0.8rem;
        font-weight:600;
        letter-spacing:0.22em;
        text-transform:uppercase;
        color:#D8CBB2;
        margin-bottom:0.9rem;
    }

    .hero-content h1{
        font-size:3.6rem;
        font-weight:800;
        color:#FFFFFF;
        margin:0;
        letter-spacing:-0.01em;
        text-shadow:0 2px 18px rgba(0,0,0,0.25);
    }

    .hero-content p{
        font-size:1.08rem;
        color:#EDE7D9;
        max-width:560px;
        margin:0.9rem auto 0 auto;
        line-height:1.6;
        font-weight:400;
    }

    .stat-card-container {
        max-width: 1180px;
        margin: -50px auto 1.5rem auto;
        padding: 0 2.5rem;
        position: relative;
        z-index: 10;
    }

    .stat-card{
        background:var(--card-bg);
        border-top:4px solid var(--primary);
        border-radius:12px;
        box-shadow:0 10px 25px rgba(0, 0, 0, 0.08);
        padding:1.5rem 1.2rem;
        text-align:center;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        transition:transform 0.22s ease, box-shadow 0.22s ease;
        width: 100%;
        margin-bottom: 10px;
        cursor: pointer;
    }

    .stat-card:hover{
        transform:translateY(-5px);
        box-shadow:0 15px 30px rgba(0, 0, 0, 0.15);
        border-top:4px solid var(--secondary);
    }

    .stat-icon{font-size:1.8rem; margin-bottom:0.4rem; display:block;}

    .stat-value{
        font-family:'Plus Jakarta Sans', sans-serif;
        font-size:2rem;
        font-weight:800;
        color:var(--secondary);
        line-height:1;
    }

    .stat-label{
        font-size:0.85rem;
        color:var(--text-muted);
        margin-top:0.4rem;
        font-weight:600;
    }

    .section{
        max-width: 100% !important;
        margin: 2.5rem 0 1rem 0 !important;
        padding: 0 !important;
    }

    .section-eyebrow{
        font-size:0.78rem;
        font-weight:700;
        letter-spacing:0.16em;
        text-transform:uppercase;
        color:var(--primary);
        margin-bottom:0.4rem;
    }

    .section-title{
        font-size:1.7rem;
        font-weight:700;
        margin-bottom:0.6rem;
    }

    .section-body{
        color:var(--text-muted);
        font-size:0.98rem;
        line-height:1.7;
        max-width: 100% !important;
    }

    .wisata-card {
        background: var(--card-bg);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        border: 1px solid var(--border-soft);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        margin: 10px 0px 25px 0px !important;
    }

    .wisata-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    }

    .wisata-img-wrapper {
        width: 100%;
        height: 200px;
        overflow: hidden;
        position: relative;
        background: #E9E4D8;
    }

    .wisata-img-wrapper img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }

    .wisata-card:hover .wisata-img-wrapper img {
        transform: scale(1.05);
    }

    .wisata-content {
        padding: 1.2rem;
        flex-grow: 1;
    }

    .wisata-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: var(--text-dark);
        margin-bottom: 0.4rem;
    }

    .wisata-desc {
        font-size: 0.88rem;
        color: var(--text-muted);
        line-height: 1.5;
        margin: 0;
    }

    .feature-grid{
        display:grid;
        grid-template-columns:repeat(3, 1fr);
        gap:1.2rem;
        margin-top:1.6rem;
    }

    .feature-card{
        background:var(--card-bg);
        border:1px solid var(--border-soft);
        border-radius:12px;
        padding:1.4rem;
        transition:box-shadow 0.2s ease, transform 0.2s ease;
    }

    .feature-card:hover{
        box-shadow:0 12px 26px rgba(30,40,25,0.1);
        transform:translateY(-3px);
    }

    .feature-card h4{
        color:var(--secondary);
        font-size:1.02rem;
        margin-bottom:0.4rem;
    }

    .feature-card p{
        color:var(--text-muted);
        font-size:0.88rem;
        line-height:1.6;
        margin:0;
    }

    .panel{
        background:var(--card-bg);
        border:1px solid var(--border-soft);
        border-radius:12px;
        padding:1.6rem 1.8rem;
        box-shadow:0 6px 18px rgba(30,40,25,0.05);
    }

    .panel-title{
        font-family:'Plus Jakarta Sans', sans-serif;
        font-weight:700;
        font-size:1.05rem;
        color:var(--secondary);
        margin-bottom:0.9rem;
    }

    [data-testid="stVerticalBlockBorderWrapper"]{
        border-radius:12px;
    }

    @media (max-width:900px){
        .stat-card-container {
            margin-top: -30px;
            padding: 0 1.5rem;
        }
        .feature-grid{grid-template-columns:repeat(1, 1fr);}
        .hero-content h1{font-size:2.4rem;}
    }
    </style>
    """.replace("__HERO_BG__", hero_bg_css),
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# PENANGANAN LINK LANGSUNG (DEEP LINKING / URL QUERY)
# --------------------------------------------------------------------------
# 1. Tangkap parameter 'artikel' dari URL jika ada
if "artikel" in st.query_params:
    st.session_state.artikel_aktif = st.query_params["artikel"]

# 2. Jika ada artikel yang aktif, tampilkan dalam MODE BACA LAYAR PENUH
if st.session_state.artikel_aktif is not None:
    artikel_terpilih = next((a for a in ARTIKEL_DATA if a["id"] == st.session_state.artikel_aktif), None)
    
    if artikel_terpilih:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tombol Kembali
        if st.button(tr("⬅ Kembali ke Beranda", "⬅ Back to Home")):
            st.session_state.artikel_aktif = None
            if "artikel" in st.query_params:
                del st.query_params["artikel"]
            st.rerun()
        
        # Header Artikel
        st.markdown(f"<h1 style='font-size: 2.2rem; color: #2C4C3B; margin-bottom: 5px;'>{artikel_terpilih['judul']}</h1>", unsafe_allow_html=True)
        st.caption(f"📅 **{artikel_terpilih['tanggal']}** &nbsp;|&nbsp; ✍️ Oleh **{artikel_terpilih['penulis']}**")
        st.markdown("<hr style='margin: 15px 0 25px 0;'>", unsafe_allow_html=True)
        
        # Gambar Banner Artikel
        img_path = ASSETS_DIR / artikel_terpilih["gambar"]
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        else:
            st.info(tr("🖼️ Tempat foto dokumentasi utama kegiatan.", "🖼️ Placeholder for main documentation photo."))
        
        # Isi Paragraf
        st.markdown('<div style="margin-top: 25px;">', unsafe_allow_html=True)
        for paragraf in artikel_terpilih["isi"]:
            st.markdown(
                f"<p style='font-size: 1.05rem; line-height: 1.8; color: #4A3525; text-align: justify;'>{paragraf}</p>",
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 40px 0 20px 0;'>", unsafe_allow_html=True)
        
        # Tombol Bawah
        if st.button(tr("Selesai Membaca", "Finish Reading"), type="primary", key="btn_bawah"):
            st.session_state.artikel_aktif = None
            if "artikel" in st.query_params:
                del st.query_params["artikel"]
            st.rerun()
            
        # PENTING: Hentikan sisa eksekusi kode agar navigasi tab tidak ikut ter-render!
        st.stop()

# --------------------------------------------------------------------------
# NAVIGATION
# --------------------------------------------------------------------------
tab_beranda, tab_peta, tab_wisata, tab_statistik, tab_jdih, tab_artikel = st.tabs([
    tr("Beranda", "Home"),
    tr("Peta Digital", "Digital Map"),
    tr("Destinasi Wisata", "Destinations"),
    tr("Statistik", "Statistics"),
    tr("JDIH & Layanan", "JDIH & Services"),
    tr("Publikasi Artikel", "Publications")
])

# --------------------------------------------------------------------------
# TAB 1 — BERANDA
# --------------------------------------------------------------------------
with tab_beranda:
    st.markdown('<div class="hero-anchor"></div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="hero-banner">
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <div class="hero-eyebrow">Kecamatan Wonotunggal · Kabupaten Batang</div>
                <h1>Desa Silurah</h1>
                <p>{tr(
                    "Peta digital dan basis data desa untuk mendukung perencanaan pembangunan berkelanjutan, selaras dengan SDG 11 — Kota dan Permukiman yang Berkelanjutan.",
                    "Digital map and village database to support sustainable development planning, aligned with SDG 11 — Sustainable Cities and Communities."
                )}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="stat-card-container">', unsafe_allow_html=True)
    cols = st.columns(4)
    for col, s in zip(cols, STATS):
        with col:
            st.markdown(
                f"""
                <a href="#{s['anchor']}" style="text-decoration: none; color: inherit;">
                    <div class="stat-card">
                        <span class="stat-icon">{s['icon']}</span>
                        <div class="stat-value">{s['value']}</div>
                        <div class="stat-label">{s['label']}</div>
                    </div>
                </a>
                """,
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="section">
            <div class="section-eyebrow">{tr("Tentang Desa", "About the Village")}</div>
            <div class="section-title">{tr("Selayang Pandang Desa Silurah", "Overview of Silurah Village")}</div>
            <p class="section-body">
                {tr(
                    "Tersembunyi di balik sejuknya perbukitan Wonotunggal, Desa Silurah bernapas melalui suburnya lahan agrowisata dan perkebunan yang menjadi urat nadi warganya. Dashboard interaktif ini hadir sebagai jendela digital untuk memetakan potensi desa, membuka transparansi data, dan menjadi pijakan pembangunan berkelanjutan berbasis bukti nyata.",
                    "Hidden behind the cool hills of Wonotunggal, Silurah Village thrives through its fertile agrotourism lands and plantations that serve as the lifeblood of its citizens. This interactive dashboard serves as a digital window to map village potentials, open data transparency, and become a foundation for evidence-based sustainable development."
                )}
            </p>
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>🗺️ {tr("Pemetaan Spasial", "Spatial Mapping")}</h4>
                    <p>{tr(
                        "Sebaran fasilitas umum, batas dusun, dan titik potensi wisata terdokumentasi secara digital dan dapat diakses publik.",
                        "The distribution of public facilities, hamlet boundaries, and tourism potential points are digitally documented and publicly accessible."
                    )}</p>
                </div>
                <div class="feature-card">
                    <h4>📊 {tr("Data Kependudukan", "Demographic Data")}</h4>
                    <p>{tr(
                        "Statistik demografi diperbarui secara berkala untuk mendukung perencanaan program desa yang tepat sasaran.",
                        "Demographic statistics are regularly updated to support targeted village program planning."
                    )}</p>
                </div>
                <div class="feature-card">
                    <h4>🌱 {tr("Keberlanjutan", "Sustainability")}</h4>
                    <p>{tr(
                        "Mendukung pencapaian SDG 11 melalui data terbuka yang mendorong pembangunan permukiman yang inklusif dan aman.",
                        "Supporting the achievement of SDG 11 through open data that encourages the development of inclusive and safe human settlements."
                    )}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # =========================================================================
    # SECTION 1: DESTINASI WISATA
    # =========================================================================
    st.markdown(
        f"""
        <div id="info-wisata" class="section" style="margin-bottom: 1rem;">
            <div class="section-eyebrow">🏞️ {tr("Destinasi Wisata", "Tourist Destinations")}</div>
            <div class="section-title">{tr("Potensi Wisata Desa Silurah", "Tourism Potential of Silurah Village")}</div>
            <p class="section-body">
                {tr(
                    "Sekilas potensi wisata unggulan Desa Silurah. Untuk melihat informasi lengkap, fasilitas, dan peta lokasi interaktif, silakan buka tab <b>Destinasi Wisata</b> di menu atas.",
                    "An overview of Silurah Village's prime tourism potential. To view complete information, facilities, and interactive location maps, please open the <b>Destinations</b> tab in the top menu."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for i in range(0, len(WISATA_DATA), 3):
        wisata_cols = st.columns(3)
        row_data = WISATA_DATA[i : i + 3]

        for col, w in zip(wisata_cols, row_data):
            with col:
                st.markdown(
                    f"""
                    <div class="wisata-card">
                        <div class="wisata-img-wrapper">
                            <img src="{w['img']}" alt="{w['nama']}">
                        </div>
                        <div class="wisata-content">
                            <div class="wisata-title">{w['nama']}</div>
                            <p class="wisata-desc">{w['desc']}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # =========================================================================
    # SECTION 2: DUSUN
    # =========================================================================
    st.markdown(
        f"""
        <div id="info-dusun" class="section" style="margin-top: 4rem; margin-bottom: 1rem;">
            <div class="section-eyebrow">🏘️ {tr("Wilayah Administratif", "Administrative Area")}</div>
            <div class="section-title">{tr("Daftar Dusun di Desa Silurah", "List of Hamlets in Silurah Village")}</div>
            <p class="section-body">
                {tr(
                    "Jelajahi denyut kehidupan masyarakat di enam dusun yang tersebar melintasi kontur perbukitan Silurah. Saling terhubung oleh urat nadi jalan desa, setiap dusun memegang peran penting dalam menjaga kerukunan warga, tradisi leluhur, dan roda perekonomian lokal.",
                    "Explore the heartbeat of community life across six hamlets spread across the hilly contours of Silurah. Interconnected by village roads, each hamlet plays an essential role in maintaining community harmony, ancestral traditions, and the local economy."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        dusun_df = pd.DataFrame({
            tr("Nama Dusun", "Hamlet Name"): [
                tr("Dusun Krajan", "Dusun Krajan"),
                tr("Dusun Batur", "Dusun Batur"),
                tr("Dusun Sipudang", "Dusun Sipudang"),
                tr("Dusun Simangli", "Dusun Simangli"),
                tr("Dusun Pomahan", "Dusun Pomahan"),
                tr("Dusun Pedati", "Dusun Pedati")
            ],
            tr("Kepala Dusun", "Hamlet Head"): [
                "-", "-", "-", 
                tr("Bpk. Sutari", "Mr. Sutari"), 
                tr("Bpk. Dwi Kurniawan", "Mr. Dwi Kurniawan"), 
                tr("Bpk. Wanudin", "Mr. Wanudin")
            ],
            tr("Jumlah RT/RW", "RT/RW Count"): ["2 RT / 1 RW", "1 RT / 1 RW", "1 RT / 0 RW", "2 RT / 1 RW", "2 RT / 1 RW", "3 RT / 1 RW"],
        })
        st.dataframe(dusun_df, use_container_width=True, hide_index=True)

    # BATAS WILAYAH
    st.markdown(
        f"""
        <div id="info-batas-wilayah" class="section" style="margin-top: 1rem; margin-bottom: 1rem;">
            <div class="section-title">{tr("Batas Wilayah Desa Silurah", "Regional Boundaries of Silurah Village")}</div>
            <p class="section-body">
                {tr(
                    "Menempati posisi strategis di ketinggian Kabupaten Batang, Desa Silurah menjadi titik simpul yang berbatasan langsung dengan empat kecamatan berbeda. Letak geografis ini menjadikannya kawasan yang kaya akan interaksi sosial, budaya, dan mobilitas ekonomi antarwilayah.",
                    "Occupying a strategic position in the highlands of Batang Regency, Silurah Village serves as a connecting hub bordered directly by four different sub-districts. This geographical location makes it an area rich in social, cultural interaction, and inter-regional economic mobility."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        batas_df = pd.DataFrame({
            tr("Arah", "Direction"): [
                tr("Utara", "North"), 
                tr("Selatan", "South"), 
                tr("Timur", "East"), 
                tr("Barat", "West")
            ],
            tr("Desa / Kecamatan Border", "Bordering Village / Sub-district"): [
                tr("Desa Sodong, Kecamatan Wonotunggal", "Sodong Village, Wonotunggal Sub-district"),
                tr("Desa Klindon, Kecamatan Petungkriyono", "Klindon Village, Petungkriyono Sub-district"),
                tr("Desa Trombo, Kecamatan Bandar", "Trombo Village, Bandar Sub-district"),
                tr("Desa Jolotigo, Kecamatan Talun", "Jolotigo Village, Talun Sub-district")
            ],
        })
        st.dataframe(batas_df, use_container_width=True, hide_index=True)

    # LUAS WILAYAH
    st.markdown(
        f"""
        <div id="info-luas-wilayah" class="section" style="margin-top: 1rem; margin-bottom: 1rem;">
            <div class="section-title">{tr("Luas Wilayah Desa Silurah", "Area Size of Silurah Village")}</div>
            <p class="section-body">
                {tr(
                    "Membentang seluas 140,09 Hektar, hamparan tanah Silurah didominasi oleh sabuk hijau perkebunan dan persawahan yang subur. Optimalisasi tata guna lahan ini menjadi fondasi utama dalam menjaga ketahanan pangan dan kelestarian ekosistem desa.",
                    "Spanning an area of 140.09 Hectares, the vast land of Silurah is dominated by a green belt of fertile plantations and rice fields. Optimizing land use is the primary foundation for maintaining food security and village ecosystem preservation."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        luas_df = pd.DataFrame({
            tr("Penggunaan Lahan", "Land Use"): [
                tr("Pemukiman", "Residential Area"),
                tr("Persawahan", "Rice Fields"),
                tr("Perkebunan", "Plantations"),
                tr("Kuburan", "Cemetery"),
                tr("Pekarangan", "Homeyards"),
                tr("Perkantoran", "Offices"),
                tr("Prasarana Umum", "Public Infrastructure")
            ],
            tr("Luas (Ha)", "Area (Ha)"): tr(
                ["0,51", "36,00", "67,98", "2,00", "25,00", "0,29", "8,31"],
                ["0.51", "36.00", "67.98", "2.00", "25.00", "0.29", "8.31"]
            ),
        })
        st.dataframe(luas_df, use_container_width=True, hide_index=True)

    # =========================================================================
    # SECTION 3: SEKOLAH
    # =========================================================================
    st.markdown(
        f"""
        <div id="info-sekolah" class="section" style="margin-top: 4rem; margin-bottom: 1rem;">
            <div class="section-eyebrow">🏫 {tr("Pendidikan", "Education")}</div>
            <div class="section-title">{tr("Fasilitas Pendidikan", "Educational Facilities")}</div>
            <p class="section-body">
                {tr(
                    "Membangun masa depan dari bangku sekolah. Dari jenjang usia dini hingga sekolah menengah, fasilitas pendidikan di Silurah terus berkembang untuk memastikan setiap anak desa mendapatkan hak belajar dan fondasi ilmu pengetahuan yang kokoh.",
                    "Building the future from the classroom. From early childhood to middle school, educational facilities in Silurah continue to develop to ensure every village child receives the right to learn and a solid academic foundation."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True):
            st.metric(label=tr("Gedung SD/Sederajat", "Elementary Schools"), value=tr("1 Unit", "1 Unit"))
    with m2:
        with st.container(border=True):
            st.metric(label=tr("Gedung SMP/Sederajat", "Middle Schools"), value=tr("1 Unit", "1 Unit"))
    with m3:
        with st.container(border=True):
            st.metric(label=tr("Taman Bermain & Bacaan", "Playgrounds & Reading Parks"), value=tr("2 Unit", "2 Units"))
    with m4:
        with st.container(border=True):
            st.metric(label=tr("Sarana Lainnya", "Other Facilities"), value=tr("4 Unit", "4 Units"))

    with st.container(border=True):
        sekolah_df = pd.DataFrame({
            tr("Nama Sekolah", "School Name"): ["PAUD Tunas Hati", "PAUD Ganesha Mulya", "SD Negeri 01 Silurah", "MI Daru Hikmah", "SMP Negeri 03 Wonotunggal SATAP"],
            tr("Jenjang", "Level"): [
                tr("PAUD", "Early Childhood"), 
                tr("PAUD", "Early Childhood"), 
                tr("SD", "Elementary"), 
                tr("SD", "Elementary"), 
                tr("SMP", "Middle School")
            ],
            tr("Lokasi", "Location"): [
                tr("Dusun Krajan", "Krajan Hamlet"),
                tr("Dusun Sipudang", "Sipudang Hamlet"),
                tr("Dusun Krajan", "Krajan Hamlet"),
                tr("Dusun Sipudang", "Sipudang Hamlet"),
                tr("Dusun Krajan", "Krajan Hamlet")
            ],
            tr("Status", "Status"): [
                tr("Swasta", "Private"), 
                tr("Swasta", "Private"), 
                tr("Negeri", "Public"), 
                tr("Swasta", "Private"), 
                tr("Negeri", "Public")
            ]
        })
        st.dataframe(sekolah_df, use_container_width=True, hide_index=True)

    # =========================================================================
    # SECTION 4: POSYANDU
    # =========================================================================
    st.markdown(
        f"""
        <div id="info-posyandu" class="section" style="margin-top: 4rem; margin-bottom: 2rem;">
            <div class="section-eyebrow">{tr("Kesehatan", "Healthcare")}</div>
            <div class="section-title">{tr("Layanan Posyandu dan Kesehatan", "Posyandu & Healthcare Services")}</div>
            <p class="section-body">
                {tr(
                    "Menjaga kualitas hidup warga sejak usia dini hingga senja. Lewat lima titik Posyandu yang beroperasi rutin di setiap dusun, layanan kesehatan dasar hadir lebih dekat untuk memantau tumbuh kembang balita, kesehatan ibu hamil, hingga kesejahteraan lansia.",
                    "Maintaining community quality of life from early childhood to twilight years. Through five Posyandu centers operating routinely in each hamlet, basic healthcare services are closer at hand to monitor toddler growth, maternal health, and elderly well-being."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        posyandu_df = pd.DataFrame({
            tr("Nama Posyandu", "Posyandu Name"): ["Posyandu Krajan", "Posyandu Sipudang", "Posyandu Simangli", "Posyandu Pomahan", "Posyandu Pedati"],
            tr("Wilayah", "Coverage Area"): ["RT 01 & RT 02", "RT 03 & RT 04", "RT 05 & RT 06", "RT 07 & RT 08", "RT 09, RT 10, & RT 11"],
            tr("Alamat", "Address"): [
                tr("Dukuh Krajan RT 01/RW 01", "Krajan Hamlet RT 01/RW 01"),
                tr("Dukuh Sipudang RT 04/RW 02", "Sipudang Hamlet RT 04/RW 02"),
                tr("Dukuh Simangli RT 05/RW 04", "Simangli Hamlet RT 05/RW 04"),
                tr("Dukuh Pomahan RT 08/RW 04", "Pomahan Hamlet RT 08/RW 04"),
                tr("Dusun Pedati RT 09/RW 05", "Pedati Hamlet RT 09/RW 05")
            ]
        })
        st.dataframe(posyandu_df, use_container_width=True, hide_index=True)

    st.markdown(
        f"""
        <div id="info-posyandu" class="section" style="margin-top: 4rem; margin-bottom: 2rem;">
            <div class="section-title">{tr("Tenaga & Sarana Kesehatan Desa", "Village Healthcare Personnel & Facilities")}</div>
            <p class="section-body">
                {tr(
                    "Harmoni antara ilmu medis modern dan kearifan tradisional. Pelayanan kesehatan masyarakat desa ditopang oleh dedikasi bidan desa serta kolaborasi erat bersama mitra bersalin terlatih dan pengobatan alternatif yang terdata resmi.",
                    "A harmony between modern medical science and traditional wisdom. Village healthcare services are supported by the dedication of village midwives and close collaboration with trained birth partners and registered alternative practitioners."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        nakes_df = pd.DataFrame({
            tr("Jenis Tenaga / Sarana Kesehatan", "Type of Personnel / Facility"): [
                tr("Bidan Desa", "Village Midwife"), 
                tr("Dukun Bersalin Terlatih", "Trained Traditional Birth Attendant"), 
                tr("Dukun Pengobatan Alternatif", "Alternative Medicine Practitioner"), 
                tr("Sarana Kesehatan Lainnya", "Other Healthcare Facilities")
            ],
            tr("Jumlah Ketersediaan", "Availability Count"): [
                tr("1 Orang", "1 Person"), 
                tr("3 Orang", "3 People"), 
                tr("4 Orang", "4 People"), 
                tr("1 Unit", "1 Unit")
            ],
            tr("Keterangan", "Description"): [
                tr("Tenaga medis profesional utama desa", "Primary professional medical personnel in the village"), 
                tr("Mitra bidan dalam penanganan persalinan", "Midwife partners in assisting childbirth"), 
                tr("Pelayanan pengobatan tradisional warga", "Traditional healing services for citizens"), 
                tr("Fasilitas pendukung kesehatan desa", "Supporting healthcare facilities in the village")
            ]
        })
        st.dataframe(nakes_df, use_container_width=True, hide_index=True)

# --------------------------------------------------------------------------
# TAB 2 — PETA DIGITAL 
# --------------------------------------------------------------------------
with tab_peta:
    st.markdown(
        f"""
        <div class="section" style="margin-top:2.2rem;">
            <div class="section-eyebrow">{tr("Peta Wilayah & Tematik", "Regional & Thematic Maps")}</div>
            <div class="section-title">{tr("Pemetaan Spasial & Tematik Desa Silurah", "Spatial & Thematic Mapping of Silurah Village")}</div>
            <p class="section-body">
                {tr(
                    "Jelajahi pemetaan wilayah administratif berbasis poligon digital interaktif, serta peta tematik hasil observasi lapangan Tim KKN mengenai persebaran fasilitas, lokasi RT/RW, hingga kondisi hidrologi curah hujan desa.",
                    "Explore interactive digital polygon-based administrative mapping, as well as thematic maps from KKN team field observations regarding facility distribution, RT/RW locations, and village rainfall hydrology."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    
    # --- PENGATUR PILIHAN PETA (SUB-MENU) ---

    st.markdown('<div class="section" style="margin-top:0;">', unsafe_allow_html=True)

    pilihan_peta = st.radio(
        label=tr("Pilih Jenis Peta:", "Choose Map Type:"),
        options=[
            tr("Peta Pemetaan RT/RW & Lokasi", "RT/RW Mapping & Location Map"),
            tr("Peta Wisata", "Tourist Map"),
            tr("Peta Sebaran Curah Hujan", "Rainfall Distribution Map")
        ],
        horizontal=True,
        key="selector_peta_tematik"
    )

    with st.container(border=True):

        # 1. PETA RT/RW & LOKASI
        if "RT/RW" in pilihan_peta:

            st.markdown(
                f'<div class="panel-title">'
                f'{tr("Peta Lokasi & Pemetaan Rumah RT/RW Desa Silurah", "Location Map & RT/RW Housing Mapping of Silurah Village")}'
                f'</div>',
                unsafe_allow_html=True
            )

            path_adm = ASSETS_DIR / "Peta Administrasi.jpg"

            if path_adm.exists():
                st.image(str(path_adm), use_container_width=True)
            else:
                st.warning(
                    tr(
                        "File peta administrasi belum ditemukan di folder assets.",
                        "Administrative map file not found in assets folder."
                    )
                )

            st.markdown(
                f'<div style="margin-top:10px; line-height:1.6; '
                f'font-size:0.9rem; color:#663300; text-align:justify;">'
                f'{tr(
                    "Peta administrasi ini mendokumentasikan sebaran jalur jalan desa, "
                    "aliran sungai, serta titik-titik lokasi rumah Ketua RT (1–11) "
                    "dan Ketua RW (1–5) yang tersebar di wilayah Desa Silurah, "
                    "dilengkapi dengan dokumentasi visual kondisi bangunan warga.",
                    
                    "This administrative map documents the distribution of village roads, "
                    "river flows, and the locations of RT (1–11) and RW (1–5) heads "
                    "across Silurah Village, complete with visual documentation "
                    "of residential building conditions."
                )}'
                f'</div>',
                unsafe_allow_html=True
            )

        # 2. PETA WISATA
        elif "Peta Wisata" in pilihan_peta or "Tourist Map" in pilihan_peta:

            st.markdown(
                f'<div class="panel-title">'
                f'{tr("Peta Wisata", "Tourist Map")}'
                f'</div>',
                unsafe_allow_html=True
            )

            path_wisata = ASSETS_DIR / "Peta Wisata.jpg"

            if path_wisata.exists():
                st.image(str(path_wisata), use_container_width=True)
            else:
                st.warning(
                    tr(
                        "File peta wisata belum ditemukan di folder assets.",
                        "Tourist map file not found in assets folder."
                    )
                )

            st.markdown(
                f'<div style="margin-top:10px; line-height:1.6; '
                f'font-size:0.9rem; color:#663300; text-align:justify;">'
                f'{tr(
                    "Peta wisata ini mendokumentasikan sebaran wisata yang ada "
                    "di Desa Silurah.",
                    
                    "This tourism map documents the distribution of tourist "
                    "attractions in Silurah Village."
                )}'
                f'</div>',
                unsafe_allow_html=True
            )

        # 3. PETA CURAH HUJAN
        else:

            st.markdown(
                f'<div class="panel-title">'
                f'{tr("Peta Sebaran Curah Hujan Bulan Juni 2026", "Rainfall Distribution Map - June 2026")}'
                f'</div>',
                unsafe_allow_html=True
            )

            path_hujan = ASSETS_DIR / "Peta Curah Hujan.jpg"

            if path_hujan.exists():
                st.image(str(path_hujan), use_container_width=True)
            else:
                st.warning(
                    tr(
                        "File peta curah hujan belum ditemukan di folder assets.",
                        "Rainfall map file not found in assets folder."
                    )
                )

            st.markdown(
                f'<div style="margin-top:10px; line-height:1.6; '
                f'font-size:0.9rem; color:#663300; text-align:justify;">'
                f'{tr(
                    "Peta hidrologi hasil analisis spasial Tim 2 KKN Undip ini "
                    "memvisualisasikan gradasi curah hujan di wilayah Desa Silurah "
                    "pada bulan Juni 2026. Bagian selatan desa cenderung memiliki "
                    "intensitas presipitasi yang lebih tinggi dibandingkan wilayah utara.",
                    
                    "This hydrological map from spatial analysis by KKN Undip Team 2 "
                    "visualizes rainfall gradients in Silurah Village in June 2026. "
                    "The southern part of the village tends to experience higher "
                    "precipitation intensity than the northern region."
                )}'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # --- BAGIAN LEGENDA & GRAFIK LAHAN ---
    st.markdown('<div class="section" style="margin-top:1.5rem;">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown(f'<div class="panel-title">{tr("Informasi Pemetaan", "Mapping Information")}</div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin-top: 10px;">
                    <div style="width: 28px; height: 18px; background-color: rgba(44, 76, 59, 0.85); border: 2px solid #A3C9B2; border-radius: 4px; margin-right: 12px;"></div>
                    <span style="font-weight: 600; color: #365E46;">{tr("Cakupan Wilayah & Zonasi", "Area Coverage & Zoning")}</span>
                </div>
                <p style="font-size: 0.85rem; color: #365E46; margin-top: 12px; line-height: 1.6;">
                    {tr("Data pemetaan spasial dan tematik diperoleh melalui survei lapangan, analisis sistem informasi geografis (GIS), serta kolaborasi program KKN Reguler Tim II Universitas Diponegoro tahun 2026 bersama pemerintah Desa Silurah.", "Spatial and thematic mapping data were obtained through field surveys, geographic information system (GIS) analysis, and collaboration of the 2026 Diponegoro University Regular KKN Team II program with the Silurah Village government.")}
                </p>
                """,
                unsafe_allow_html=True
            )
    with col2:
        with st.container(border=True):
            st.markdown(f'<div class="panel-title">{tr("Penggunaan Lahan (Ha)", "Land Use (Ha)")}</div>', unsafe_allow_html=True)
            
            chart_data = LAND_USE_DATA.reset_index()
            col_lahan = tr("Penggunaan Lahan", "Land Use")
            col_luas = tr("Luas (Ha)", "Area (Ha)")
            chart_data.columns = [col_lahan, col_luas]
            
            bars = alt.Chart(chart_data).mark_bar(color="#365E46", cornerRadiusEnd=4).encode(
                x=alt.X(f'{col_luas}:Q', scale=alt.Scale(type='sqrt'), title=col_luas),
                y=alt.Y(f'{col_lahan}:N', sort='-x', title=None),
                tooltip=[col_lahan, col_luas]
            )
            
            text = bars.mark_text(
                align='left',
                baseline='middle',
                dx=3,
                color='#FFFFFF',
                fontWeight='bold'
            ).encode(
                text=f'{col_luas}:Q'
            )
            
            st.altair_chart(bars + text, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# TAB 3 — WISATA
# --------------------------------------------------------------------------
with tab_wisata:
    st.markdown(
        f"""
        <div class="section" style="margin-top:2.2rem; margin-bottom: 1rem;">
            <div class="section-eyebrow">{tr("Jelajah Silurah", "Explore Silurah")}</div>
            <div class="section-title">{tr("Pesona & Daya Tarik Wisata", "Charm & Tourist Attractions")}</div>
            <p class="section-body">
                {tr(
                    "Eksplorasi keindahan alam perbukitan, kesejukan air terjun alami, serta rekam jejak warisan sejarah leluhur yang tersimpan di Desa Silurah. Pilih nama destinasi di bawah ini untuk melihat informasi mendetail dan peta lokasi GPS.",
                    "Explore the beauty of the hilly nature, the coolness of natural waterfalls, and the traces of ancestral historical heritage stored in Silurah Village. Select a destination name below to view detailed information and GPS location maps."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nama_destinasi = [w["nama"] for w in WISATA_DATA]
    sub_tabs = st.tabs(nama_destinasi)

    for tab, w in zip(sub_tabs, WISATA_DATA):
        with tab:
            with st.container(border=True):
                col_left, col_right = st.columns([1, 1.2], gap="large")

                # ==========================================================
                # KOLOM KIRI: FOTO WISATA + DESKRIPSI
                # ==========================================================
                # ==========================================================
                # KOLOM KIRI: FOTO WISATA + DESKRIPSI (VERSI PALING AMAN)
                # ==========================================================
                with col_left:
                    # Logika langsung mendeteksi file _ID.jpg atau _EN.jpg berdasarkan nama file asli
                    nama_file_dasar = w['nama'].replace("Situs ", "").replace("Arca ", "") # Menyesuaikan jika ada awalan
                    
                    if is_eng and (ASSETS_DIR / f"{w['nama']}_EN.jpg").exists():
                        foto_tampil = ASSETS_DIR / f"{w['nama']}_EN.jpg"
                    elif (ASSETS_DIR / f"{w['nama']}_ID.jpg").exists():
                        foto_tampil = ASSETS_DIR / f"{w['nama']}_ID.jpg"
                    elif (ASSETS_DIR / f"{nama_file_dasar}_ID.jpg").exists():
                        foto_tampil = ASSETS_DIR / f"{nama_file_dasar}_ID.jpg"
                    else:
                        # Fallback otomatis mengambil foto bersih utama jika versi teks belum ada
                        foto_tampil = ASSETS_DIR / f"{w['nama']}.jpg"
                        if not foto_tampil.exists():
                            # Pilihan cadangan terakhir jika nama file aslinya tanpa kata Situs
                            foto_tampil = ASSETS_DIR / f"{nama_file_dasar}.jpg"
                        
                    st.image(str(foto_tampil), use_container_width=True)
                    
                    st.markdown(
                        f'<div style="margin-top: 15px; line-height: 1.7; font-size: 0.95rem; color: var(--text-dark); text-align: justify;"></div>',
                        unsafe_allow_html=True,
                    )

                # ==========================================================
                # KOLOM KANAN: JUDUL, TOMBOL MAPS & PETA 3D
                # ==========================================================
                with col_right:
                    st.markdown(f"### {w['nama']}")
                    dusun_text = w.get('dusun', tr('Desa Silurah', 'Silurah Village'))
                    st.caption(f"{tr('Wilayah:', 'Area:')} {dusun_text}")
         
                    st.markdown(
                        f"**{tr('Peta Lokasi:', 'Location Map:')}** {tr('Titik GPS', 'GPS Coordinates')} ({w['lat']}, {w['lon']})"
                    )

                    if "link_maps" in w:
                        st.link_button(tr("Buka Lokasi di Google Maps", "Open Location in Google Maps"), w["link_maps"], use_container_width=True)

                    df_lokasi = pd.DataFrame(
                        {
                            "lat": [w["lat"]],
                            "lon": [w["lon"]],
                            "nama": [w["nama"]],
                        }
                    )

                    view_state = pdk.ViewState(
                        latitude=w["lat"],
                        longitude=w["lon"],
                        zoom=15,
                        pitch=45,
                    )

                    layer_point = pdk.Layer(
                        "ScatterplotLayer",
                        data=df_lokasi,
                        get_position="[lon, lat]",
                        get_fill_color=[44, 76, 59, 255],
                        get_radius=40,
                        pickable=True,
                    )

                    r = pdk.Deck(
                        layers=[layer_point],
                        initial_view_state=view_state,
                        tooltip={"text": "{nama}"},
                    )
                    st.pydeck_chart(r, use_container_width=True)

# --------------------------------------------------------------------------
# TAB 4 — STATISTIK
# --------------------------------------------------------------------------
with tab_statistik:
    st.markdown(
        f"""
        <style>
        /* Desain Kartu Kependudukan Modern (Anti-Kaku & Anti-Kepotong) */
        .demo-card {{
            background: linear-gradient(135deg, rgba(44, 76, 59, 0.35) 0%, rgba(20, 28, 24, 0.85) 100%);
            border: 1px solid rgba(163, 201, 178, 0.3);
            border-radius: 18px;
            padding: 1.5rem 1.2rem;
            text-align: left;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
            margin-bottom: 1rem;
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .demo-card:hover {{
            transform: translateY(-5px);
            border-color: rgba(163, 201, 178, 0.8);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
            background: linear-gradient(135deg, rgba(62, 92, 72, 0.45) 0%, rgba(30, 40, 35, 0.95) 100%);
        }}

        /* Teks Kiri: Label & Angka */
        .demo-content {{
            z-index: 2;
        }}

        .demo-label {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.9rem;
            font-weight: 600;
            color: #A3C9B2;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.3rem;
        }}

        .demo-val {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 2.1rem;
            font-weight: 800;
            color: #FFFFFF;
            line-height: 1.1;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
            white-space: nowrap; /* Mencegah teks kepotong jadi titik-titik */
        }}

        /* Ikon Besar di Kanan Kartu */
        .demo-icon {{
            font-size: 2.6rem;
            opacity: 0.8;
            transition: transform 0.3s ease;
        }}

        .demo-card:hover .demo-icon {{
            transform: scale(1.15) rotate(8deg);
            opacity: 1;
        }}
        </style>

        <div class="section" style="margin-top:2.2rem;">
            <div class="section-eyebrow">{tr("Data & Demografi", "Data & Demographics")}</div>
            <div class="section-title">{tr("Profil Kependudukan", "Population Profile")}</div>
            <p class="section-body">
                {tr(
                    "Ringkasan data demografi Desa Silurah berdasarkan dusun dan kelompok usia.",
                    "Summary of Silurah Village demographic data by hamlet and age group."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- KARTU KEPENDUDUKAN (GAYA STAT-CARD BERANDA) ---
    st.markdown(
        """
        <style>
        .stat-card-custom {
            background: #FFFFFF;
            border-top: 5px solid #2C4C3B;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
            padding: 1.8rem 1rem;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            width: 100%;
            margin-bottom: 1.5rem;
        }

        .stat-card-custom:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.15);
            border-top: 5px solid #4A3525;
        }

        /* Ikon di Bagian Atas */
        .stat-icon-custom {
            font-size: 2.2rem;
            margin-bottom: 0.5rem;
            display: block;
        }

        /* Angka Utama yang Jelas dan Tidak Terpotong */
        .stat-val-custom {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: #4A3525;
            line-height: 1.2;
            margin-bottom: 0.3rem;
            white-space: nowrap; /* Mencegah angka terpotong menjadi ... */
        }

        /* Label Keterangan di Bawah */
        .stat-label-custom {
            font-size: 0.9rem;
            color: #6B6459;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="section" style="margin-top:0;">', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    
    demo_metrics = [
        {"val": "1.950", "label": tr("Total Penduduk", "Total Population")},
        {"val": "633", "label": tr("Kepala Keluarga", "Heads of Family")},
        {"val": "140,09 Ha", "label": tr("Luas Wilayah", "Area Size")},
        {"val": "105,26", "label": tr("Rasio Gender", "Gender Ratio")},
    ]
    
    for col, data in zip([m1, m2, m3, m4], demo_metrics):
        with col:
            st.markdown(
                f"""
                <div class="stat-card-custom">
                    <div class="stat-val-custom">{data['val']}</div>
                    <div class="stat-label-custom">{data['label']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION BARU: STATISTIK KESEHATAN 2026
    # =========================================================================
    st.markdown(
        f"""
        <div class="section" style="margin-top:3.5rem;">
            <div class="section-eyebrow">{tr("Kesehatan Warga", "Citizen Health")}</div>
            <div class="section-title">{tr("Statistik Penyakit Warga (Tahun 2026)", "Citizen Disease Statistics (2026)")}</div>
            <p class="section-body">
                {tr(
                    "Perekaman data prevalensi penyakit masyarakat Desa Silurah pada tahun 2026 sebagai acuan peningkatan layanan kesehatan desa dan tindakan preventif Posyandu.",
                    "Recording of disease prevalence data among Silurah Village citizens in 2026 as a reference for improving village healthcare services and Posyandu preventive measures."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section" style="margin-top:0;">', unsafe_allow_html=True)
    col_tabel, col_grafik = st.columns([1, 1.3], gap="large")

    # Siapkan nama kolom dinamis
    col_penyakit = tr("Jenis Penyakit", "Disease Type")
    col_kasus = tr("Jumlah Kasus", "Number of Cases")

    # DataFrame Kesehatan 2026 (Dwibahasa)
    health_df = pd.DataFrame({
        col_penyakit: [
            tr("Penyakit Rhematik", "Rheumatic Disease"),
            tr("ISPA (Saluran Pernapasan)", "ARI (Respiratory Infection)"),
            tr("Hipertensi", "Hypertension"),
            tr("TBC (Tuberkulosis)", "Tuberculosis (TB)"),
            tr("Diabetes Melitus (DM)", "Diabetes Mellitus (DM)")
        ],
        col_kasus: [56, 15, 15, 2, 2]
    })

    # Bagian Kiri: Tabel Data
    with col_tabel:
        with st.container(border=True):
            st.markdown(f'<div class="panel-title">{tr("Rekapitulasi Kasus", "Case Summary")}</div>', unsafe_allow_html=True)
            st.dataframe(health_df, use_container_width=True, hide_index=True)
            
            # Info box khusus warna Hijau Earth Tone (Bukan Biru)
            total_kasus = health_df[col_kasus].sum()
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(44, 76, 59, 0.15); 
                    border: 1px solid rgba(163, 201, 178, 0.4); 
                    border-radius: 8px; 
                    padding: 12px 16px; 
                    color: #663300; 
                    font-size: 0.95rem; 
                    margin-top: 10px;">
                    <span style="color: #663300; font-weight: bold;">{tr('Total Terdata:', 'Total Recorded:')}</span> 
                    <b>{total_kasus}</b> {tr('Kasus', 'Cases')} (2026)
                </div>
                """,
                unsafe_allow_html=True
            )

    # Bagian Kanan: Grafik Batang Horizontal Altair
    with col_grafik:
        with st.container(border=True):
            st.markdown(f'<div class="panel-title">{tr("Grafik Prevalensi Penyakit", "Disease Prevalence Chart")}</div>', unsafe_allow_html=True)
            
            bars_health = alt.Chart(health_df).mark_bar(color="#365E46", cornerRadiusEnd=4).encode(
                x=alt.X(f'{col_kasus}:Q', title=col_kasus),
                y=alt.Y(f'{col_penyakit}:N', sort='-x', title=None), # Diurutkan otomatis dari kasus terbanyak
                tooltip=[col_penyakit, col_kasus]
            )
            
            text_health = bars_health.mark_text(
                align='left',
                baseline='middle',
                dx=4,
                color='#FFFFFF',
                fontWeight='bold',
                fontSize=13
            ).encode(
                text=f'{col_kasus}:Q'
            )
            
            st.altair_chart(bars_health + text_health, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# TAB 5 — JDIH & PPID (JARINGAN DOKUMENTASI DAN INFORMASI HUKUM)
# --------------------------------------------------------------------------
with tab_jdih:
    st.markdown(
        f"""
        <div class="section" style="margin-top:2.2rem;">
            <div class="section-eyebrow">{tr("Transparansi & Pelayanan Publik", "Transparency & Public Services")}</div>
            <div class="section-title">{tr("JDIH & PPID Desa Silurah", "Silurah Village JDIH & PPID")}</div>
            <p class="section-body">
                {tr(
                    "Layanan informasi publik, jaringan dokumentasi hukum, dan portal layanan masyarakat terpadu Pemerintah Desa Silurah.",
                    "Public information services, legal documentation network, and integrated community service portal of Silurah Village Government."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section" style="margin-top:1.5rem;">', unsafe_allow_html=True)
    
    # Membuat Layout 2 Kolom (Kiri dan Kanan)
    col_kiri, col_kanan = st.columns(2)
    
    with col_kiri:
        # 1. KOLOM SK KEPALA DESA
        with st.container(border=True):
            st.markdown('### Surat Keputusan (SK)')
            st.caption(tr("Kumpulan Surat Keputusan Kepala Desa Silurah", "Collection of Silurah Village Head Decrees"))
            st.info(tr("Dokumen sedang dalam tahap digitalisasi dan akan segera diunggah.", "Documents are in the digitization stage and will be uploaded soon."))
            # Nanti tombol download ditaruh di sini
            # st.download_button(label="Unduh SK Tahun 2026", data=file_sk, file_name="SK_Kades_2026.pdf")
            
        # 2. KOLOM PERATURAN DESA (PERDES)
        with st.container(border=True):
            st.markdown('### Peraturan Desa')
            st.caption(tr("Dokumen Peraturan Desa (Perdes) yang berlaku", "Applicable Village Regulation Documents (Perdes)"))
            st.info(tr("Dokumen sedang dalam tahap rekapitulasi perangkat desa.", "Documents are in the village official recapitulation stage."))
            # Nanti tombol download ditaruh di sini

    with col_kanan:
        # 3. KOLOM PPID
        with st.container(border=True):
            st.markdown('### PPID')
            st.caption(tr("Pejabat Pengelola Informasi dan Dokumentasi", "Information and Documentation Management Officer"))
            st.info(tr("Formulir dan daftar informasi publik sedang dipersiapkan.", "Forms and public information lists are being prepared."))
            # Nanti file atau link ditaruh di sini
            
        # 4. KOLOM PENGADUAN MASYARAKAT
        with st.container(border=True):
            st.markdown('### Layanan Pengaduan')
            st.caption(tr("Portal pengaduan dan aspirasi masyarakat desa", "Village community complaint and aspiration portal"))
            st.info(tr("Formulir layanan pengaduan akan segera tersedia.", "The complaint service form will be available soon."))
            # Nanti bisa diisi dengan link Google Form atau nomor WhatsApp layanan desa
            # st.link_button("Isi Form Pengaduan", "https://link-google-form.com")

    st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------------------------------
# TAB 6 — PUBLIKASI ARTIKEL KKN
# --------------------------------------------------------------------------
with tab_artikel:
    st.markdown(
        f"""
        <div class="section" style="margin-top:2.2rem;">
            <div class="section-eyebrow">{tr("Kabar & Kegiatan", "News & Activities")}</div>
            <div class="section-title">{tr("Publikasi Program Kemasyarakatan", "Community Program Publications")}</div>
            <p class="section-body">
                {tr(
                    "Rekam jejak, dokumentasi, dan artikel publikasi kegiatan sosial kemasyarakatan Tim II KKN Undip bersama warga Desa Silurah.",
                    "Track record, documentation, and publication articles of social community activities by KKN Undip Team II with Silurah Village citizens."
                )}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section" style="margin-top:1.5rem;">', unsafe_allow_html=True)
    
    # Layout 2 Kolom untuk Kartu Artikel
    cols = st.columns(2, gap="large")
    
    for index, artikel in enumerate(ARTIKEL_DATA):
        with cols[index % 2]:
            with st.container(border=True):
                # Cek File Gambar
                img_path = ASSETS_DIR / artikel["gambar"]
                if img_path.exists():
                    st.image(str(img_path), use_container_width=True)
                else:
                    st.info(tr("🖼️ Menunggu unggahan foto...", "🖼️ Waiting for photo upload..."))
                
                st.markdown(f"#### {artikel['judul']}")
                st.caption(f"📅 **{artikel['tanggal']}** &nbsp;|&nbsp; ✍️ **{artikel['penulis']}**")
                st.markdown(f"<p style='color: var(--text-muted); font-size: 0.9rem; line-height: 1.6;'>{artikel['ringkasan']}</p>", unsafe_allow_html=True)
                
                # Tombol Aksi Buka Artikel yang Otomatis Membuat URL Link
                if st.button(tr("Baca Selengkapnya ➔", "Read More ➔"), key=f"btn_{artikel['id']}", use_container_width=True):
                    st.session_state.artikel_aktif = artikel['id']
                    st.query_params["artikel"] = artikel['id'] # <-- KUNCI UTAMA UPDATE URL
                    st.rerun()
                    
    st.markdown("</div>", unsafe_allow_html=True)
