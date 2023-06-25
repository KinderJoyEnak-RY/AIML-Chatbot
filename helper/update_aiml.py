import re
import mysql.connector

#fungsi untuk mengkoneksikan ke database mysql
def connect():
    db = mysql.connector.connect(host='localhost', user='root',  passwd='',  db='aiml', port=3306)
    return db

#variable global memanggil funsi connect()
connect = connect()

#fungsi untuk update aiml file pada folder data/aiml
def update_aiml_file():
	#memangil fungsi cursor
	mycursor = connect.cursor()

	#menselect id, tag pada tabel tag dan tampung data di variabel tags
	mycursor.execute("SELECT id, tag FROM tag ")
	tags = mycursor.fetchall()

	#menselect tag_id, tag pada tabel pattern dan tampung data di variabel patterns
	mycursor.execute("SELECT tag_id, id, pattern FROM pattern")
	patterns = mycursor.fetchall()

	#menselect tag_id, pattern_id, response pada tabel response dan tampung data di variabel response
	mycursor.execute("SELECT tag_id, pattern_id, response FROM response")
	responses = mycursor.fetchall()

	#variabel untuk menampung hasil fecth data aiml
	result = ""

	#mengeluarkan data tag
	for tag in tags:
		#mengeluarkan data pattern
		for pattern in patterns:
			#kondisi mencocokan data id pada table tag dengan tag_id pada table pattern
			if tag[0] == pattern[0]:
				#mengeluarkan data response
				for response in responses:
					#kondisi mencocokan data id pada table response dengan response_id pada table pattern
					if response[1] == pattern[1]:
						#panggil variabel result dan isi dengan karater dibawah untuk mengisi tag <category>,<template>,<pattern> pada aiml file
						result += """ \n\t<category> \n\t\t<pattern>"""+str(pattern[2])+"""</pattern>\n\t\t<template>\n\t\t\t"""+str(response[2]).rstrip().lstrip()+"""\n\t\t</template>\n\t</category>\n"""
						#kondisi jika pattern tidak sama dengan karakter * 'wildcard'
						if pattern[2] != '*':
							#panggil variabel result dan isi dengan karater dibawah untuk mengisi tag <category>,<template>,<pattern> & <srai> pada aiml file
							result += """\n\t<category>\n\t\t<pattern>* """+str(pattern[2])+""" </pattern>\n\t\t<template>\n\t\t\t<srai>"""+str(pattern[2])+"""</srai>\n\t\t</template>\n\t</category>\n"""
							result += """\n\t<category>\n\t\t<pattern> """+str(pattern[2])+""" *</pattern>\n\t\t<template>\n\t\t\t<srai>"""+str(pattern[2])+"""</srai>\n\t\t</template>\n\t</category>\n"""
							result += """\n\t<category>\n\t\t<pattern>* """+str(pattern[2])+""" *</pattern>\n\t\t<template>\n\t\t\t<srai>"""+str(pattern[2])+"""</srai>\n\t\t</template>\n\t</category>\n"""

	#fungsi membuat file dan mereplace jika file itu ada, lokasi di simpan di folder data dengan nama simple.aiml
	f = open("data/simple.aiml", "w")
	#fungsi menulis pada file yang telah dibuat
	f.write("""<?xml version="1.0" encoding="UTF-8"?>\n<aiml version="2.0">
	<category>
			<pattern>NAMA *</pattern>
			<template>
					<think><set name="username"><star/></set></think>
					hi <star/>, Senang berkenalan denganmu! Saya akan mengingat nama kamu. baik <srai>GET NAME</srai>, ada yang bisa saya bantu?
			</template>
	</category>

	<category>
		  <pattern>NAMA SAYA *</pattern>
			<template>
					<think><set name="username"><star/></set></think>
					hi <star/>, Senang berkenalan denganmu! Saya akan mengingat nama kamu. baik <srai>GET NAME</srai>, ada yang bisa saya bantu?
			</template>
	</category>

		<category>
			<pattern>AKU *</pattern>
			<template>
					<think><set name="username"><star/></set></think>
					hi <star/>, Senang berkenalan denganmu! Saya akan mengingat nama kamu. baik <srai>GET NAME</srai>, ada yang bisa saya bantu?
			</template>
	</category>

		<category>
			<pattern>SAYA *</pattern>
			<template>
					<think><set name="username"><star/></set></think>
					hi <star/>, Senang berkenalan denganmu! Saya akan mengingat nama kamu. baik <srai>GET NAME</srai>, ada yang bisa saya bantu?
			</template>
	</category>

	<category>
			<pattern>* NAMA *</pattern>
			<template>Nama kamu adalah <srai>GET NAME</srai>.</template>
	</category>
	<category>
			<pattern>GET NAME</pattern>
			<template><get name="username"/></template>
	</category>

		<category> 
		<pattern>ASSALAMUALAIKUM</pattern>
		<template>
			waalaikumsalam wr. wb, ada yang bisa di bantu?
		</template>
	</category>
	<category>
		<pattern>* ASSALAMUALAIKUM </pattern>
		<template>
			<srai>ASSALAMUALAIKUM</srai>
		</template>
	</category>
	<category>
		<pattern> ASSALAMUALAIKUM *</pattern>
		<template>
			<srai>ASSALAMUALAIKUM</srai>
		</template>
	</category>
	<category>
		<pattern>* ASSALAMUALAIKUM *</pattern>
		<template>
			<srai>ASSALAMUALAIKUM</srai>
		</template>
	</category>
 
	<category> 
		<pattern>SALAM</pattern>
		<template>
			waalaikumsalam wr. wb, ada yang bisa di bantu?
		</template>
	</category>
	<category>
		<pattern>* SALAM </pattern>
		<template>
			<srai>SALAM</srai>
		</template>
	</category>
	<category>
		<pattern> SALAM *</pattern>
		<template>
			<srai>SALAM</srai>
		</template>
	</category>
	<category>
		<pattern>* SALAM *</pattern>
		<template>
			<srai>SALAM</srai>
		</template>
	</category>

	<category>
        <pattern>SELAMAT *</pattern>
        <template>
        <think> <set name="sapaan"><star/></set></think>
        
        <condition name="sapaan" value = "pagi"> Halo <srai>GET NAME</srai>, Selamat Pagi ada yang bisa kami bantu ?</condition>
        <condition name="sapaan" value = "siang"> Halo <srai>GET NAME</srai>, Selamat Siang ada yang bisa kami bantu ?</condition>
        <condition name="sapaan" value = "sore"> Halo <srai>GET NAME</srai>, Selamat Sore ada yang bisa kami bantu ?</condition>
        <condition name="sapaan" value = "malam"> Halo <srai>GET NAME</srai>, Selamat Malam ada yang bisa kami bantu ?</condition>
        </template>
	</category>

  <category>
		<pattern>BYE</pattern>
		<template>
      okay, <srai>GET NAME</srai> Terima kasih atas percakapannya!
  	</template>  
	</category>
	<category>
		<pattern>TERIMAKASIH</pattern>
		<template>
				okay, <srai>GET NAME</srai> Terima kasih atas percakapannya!
		</template>  
	</category>
	<category>
		<pattern>TERIMA KASIH</pattern>
		<template>
				okay, <srai>GET NAME</srai> Terima kasih atas percakapannya!
		</template>  
	</category>
	"""+ result +"""\n</aiml> """)
	f.close()
	
	return print("aiml files updated successfully")

#fungsi untuk mereplace karakter pada inputan
def custom_make_translation(text):
	#data taple pada tag aiml
	translation = {
			"<template>":"", 
			"</template>":"",
			"<category>":"", 
			"</category>":"",
			"<pattern>": "",
			"</pattern>":"",
			"<srai>":"", 
			"</srai>":"",
	}
	#join karakter inputan dan bandingkan dengan translation taple dan tampung pada variabl regex
	regex = re.compile('|'.join(map(re.escape, translation)))
	return regex.sub(lambda match: translation[match.group(0)], text).strip().lstrip()
