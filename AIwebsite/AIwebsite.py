from flask import Flask, render_template, request, jsonify
import ollama as llm

app = Flask(__name__)

# pertanyaan = [
#         "Apakah kamu berminat dengan dunia coding atau pemrograman?","Apakah kamu suka memecahkan masalah (problem solving)?"," Apakah kamu suka melakukan troubleshooting (mencari dan memperbaiki error)?",
#         "Apakah kamu suka dengan hal-hal yang melibatkan logika?"," Apakah kamu suka belajar dengan cara praktek? ","Apakah kamu suka dengan teknologi secara umum?","Apakah kamu berminat pada bidang kesenian?",
#         "Apakah kamu suka menggambar?","Apakah kamu paham tentang hardware komputer?"," Apakah kamu suka dengan jaringan komputer?","Apakah kamu suka atau mampu melakukan analisis?","Apakah kamu berminat pada bidang manajemen?",
#         "Apakah kamu berminat dengan dunia cybersecurity?","Apakah kamu berminat pada game programming?","Apakah kamu berminat pada kegiatan komunikasi dengan orang lain?","Bagaimana tingkat kreativitasmu?",
#         "Apakah kamu berminat pada bidang keuangan?","Apakah kamu berminat pada bidang bisnis?","Apakah kamu berminat dalam kegiatan editing (foto/video)?","Apakah kamu tertarik pada fotografi?",
#         "Apakah kamu tertarik pada videografi?","Apakah kamu suka membuat atau merancang produk?"
#         ]

# menampilkan halaman html
@app.route("/")
def index():
    return render_template("WebAI.html")

# logika untuk chatnya
@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.json
        jawaban_user = data.get("message")

        # mengubah list pertanyaan menjadi string teks
        # pertanyaan_teks = "\n".join(pertanyaan)

        job = f"""Anda bertugas sebagai pemberi saran jurusan untuk seorang calon mahasiswa yang akan masuk Institut Informatika Indonesia(IKADO).
            universitas IKADO memiliki 8 jurusan, yaitu: Informatika, Sistem Informasi, Teknik Komputer dan Jaringan, Desain Komunikasi Visual, Desain Produk,
            Digital Business Comunication, Digital Business Technology, Digital Finanace Management. Sekarang tugas anda adalah menentukan jurusan dari calon 
            mahasiswa dan 1 jurusan alternatif berdasarkan jawaban dari calon mahasiswa, output harus hanya 2 yaitu jurusan utama dan alternatif."""

        response = llm.chat(model='gemma3:4b', messages=[
            {
                'role': 'system',
                'content': job,
            },
            {
                'role': 'user',
                'content': jawaban_user,
            },
        ])

        jawaban_ai = response['message']['content']
        # mengirim jawaban ke browser html
        return jsonify({"response": jawaban_ai})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
# app.run(host="0.0.0.0", port=80)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
