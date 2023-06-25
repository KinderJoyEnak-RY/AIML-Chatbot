import aiml
from helper.spell_checker import correction

#Create the kernel and learn AIML files
kernel = aiml.Kernel()
kernel.bootstrap(learnFiles="./data/std-startup.xml", commands="load aiml")

# Looping untuk meneruskan input ke bot dan mencetak responnya
while True:
    query = input(">Human: ")
    #berfungsi untuk mendapatkan inputan user 
    sentence = query
    #simpan inputan user "queri" di variabel sentence
    query = [correction(w) for w in (query.split())]
    #code di atas bergfungsi untuk memecah kalimat dalam bentuk array (tokenize) *contoh ['apa', 'kabar', '?']
    #setelah kalimat menajadi dalam bentuk array, pada baris tsb fungsi spell_checker dilakukan dengan memangil funsi correction pada direktory helper
    correction_sentence = " ".join(query)
    #langkah berikutnya pada kode di atas berfungsi untuk menggabungkan kembali kata yang telah di pecah, dalam kalimat yang ditampaung pada variabel correction_sentence
    response = kernel.respond(query)
    #panggil fungsi response pada dari aiml kernel dengan paramater "query" inputan user
    #pattern akan dikenali bergantung pada file AIML apa yang di muat.
    
    if response:
        #kondisi jika menerima response
        if (len(correction_sentence) - len(sentence) != 0):
            #pengkodisian ini digunakan untuk mengecek apakah ada kata typo pada inputan user dengan membandingkan jumlah_karakter(correction_sentence) dan jumlah_karakter(sentence)
            #[(jumlah_karakter(correction_sentence) - jumlah_karakter(sentence)) != 0 ] jika hasil pengurangan tidak sama dengan 0 maka ekseskui code dibawah
            result = "Mungkin Maksud Anda, " + correction_sentence + "<br>"+ response
            #variabel result untuk menampung response dari pattern yang di inputkan user dan juga menampilkan correction_sentence
        else:
            result = response
            #variabel result untuk hanya menampung response dari pattern yang di inputkan user 
        print("bot > ", response)
    else :
        print("bot > :)")

# Press CTRL-C to break this loop