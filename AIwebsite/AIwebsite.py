from flask import Flask, render_template, request, jsonify
import ollama as llm
from flask_cors import CORS #agar tidak error 505
from flask import session #agar setiap user punya memory sendiri namun hanya terbatas 4kb dan tersimpan di cookie, kalau chat panjang bisa error/terpotong

app = Flask(__name__)
CORS(app)
app.secret_key = "ai-chatbot" #untuk session

# pertanyaan = [
#         "1.Apakah kamu berminat dengan dunia coding atau pemrograman?","2.Apakah kamu suka memecahkan masalah (problem solving)?","3.Apakah kamu suka melakukan troubleshooting (mencari dan memperbaiki error)?",
#         "4.Apakah kamu suka dengan hal-hal yang melibatkan logika?","5.Apakah kamu suka belajar dengan cara praktek? ","6.Apakah kamu suka dengan teknologi secara umum?","7.Apakah kamu berminat pada bidang kesenian?",
#         "8.Apakah kamu suka menggambar?","9.Apakah kamu paham tentang hardware komputer?","10.Apakah kamu suka dengan jaringan komputer?","11.Apakah kamu suka atau mampu melakukan analisis?","12.Apakah kamu berminat pada bidang manajemen?",
#         "13.Apakah kamu berminat dengan dunia cybersecurity?","14.Apakah kamu berminat pada game programming?","15.Apakah kamu berminat pada kegiatan komunikasi dengan orang lain?","16.Bagaimana tingkat kreativitasmu?",
#         "17.Apakah kamu berminat pada bidang keuangan?","18.Apakah kamu berminat pada bidang bisnis?","19.Apakah kamu berminat dalam kegiatan editing (foto/video)?","20.Apakah kamu tertarik pada fotografi?",
#         "21.Apakah kamu tertarik pada videografi?","22.Apakah kamu suka membuat atau merancang produk?"
#         ]

# chat_history = []

# menampilkan halaman html
@app.route("/")
def index():
    return render_template("WebAI.html")

# logika untuk chatnya
@app.route("/chat", methods=["GET","POST"])

def chat():

    # if request.method == "GET":
    #     return jsonify({"status": "Chat endpoint ready"}),200
    try:

        data = request.json
        jawaban_user = data.get("message")

        # mengubah list pertanyaan menjadi string teks
        # pertanyaan_teks = "\n".join(pertanyaan)

        job = f"""Anda bertugas sebagai pemberi saran jurusan untuk seorang calon mahasiswa yang akan masuk Institut Informatika Indonesia(IKADO).
            universitas IKADO memiliki 8 jurusan, yaitu: Informatika, Sistem Informasi, Teknik Komputer dan Jaringan, Desain Komunikasi Visual, Desain Produk,
            Digital Business Comunication, Digital Business Technology, Digital Finanace Management. Sekarang tugas anda adalah menentukan jurusan dari calon 
            mahasiswa dan 1 jurusan alternatif berdasarkan jawaban dari calon mahasiswa output harus hanya 2 yaitu jurusan utama dan alternatif.
            Anda bisa berikan pertanyaan yg relevan."""
        
        if "chat_history" not in session:
            session["chat_history"] = []
            # inisialisasi job AI sbg awalan
            session["chat_history"].append({
                'role': 'system',
                'content': job,
            })

        # menyimpan jawaban user dari percakapan antara ai dan user
        session["chat_history"].append({
            "role": "user",
            "content": jawaban_user
        })

        response = llm.chat(model='gemma3:4b', messages= session["chat_history"])

        jawaban_ai = response['message']['content']

        # menyimpan jawaban AI dari percakapan antara ai dan user
        session["chat_history"].append({
            "role": "assistant",
            "content": jawaban_ai
        })

        session.modified = True

        # mengirim jawaban ke browser html
        return jsonify({"response": jawaban_ai})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
# app.run(host="0.0.0.0", port=80)
if __name__ == "__main__":
    app.run(debug=True)
