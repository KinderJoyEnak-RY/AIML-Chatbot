/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 100427 (10.4.27-MariaDB)
 Source Host           : localhost:3306
 Source Schema         : aiml

 Target Server Type    : MySQL
 Target Server Version : 100427 (10.4.27-MariaDB)
 File Encoding         : 65001

 Date: 07/03/2023 18:21:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for pattern
-- ----------------------------
DROP TABLE IF EXISTS `pattern`;
CREATE TABLE `pattern`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `tag_id` int NULL DEFAULT NULL,
  `pattern` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 38 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pattern
-- ----------------------------
INSERT INTO `pattern` VALUES (1, 1, '*', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (2, 2, 'ASSALAMUALAIKUM', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (3, 3, 'SELAMAT PAGI', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (5, 4, 'PENYUSUNAN PROPOSAL', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (6, 5, 'SYARAT SEMPRO', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (7, 6, 'JADWAL SEMPRO', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (8, 6, 'JADWAL SEMINAR PROPOSAL', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (9, 7, 'DAFTAR SEMPRO', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (10, 7, 'DAFTAR SEMINAR PROPOSAL', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (11, 8, 'BERKAS PENDUKUNG PENELITIAN SEMINAR PROPOSAL', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (12, 8, 'BERKAS PENDUKUNG PENELITIAN', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (13, 8, 'SURAT REKOMENDASI PENELITIAN', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (14, 8, 'REKOMENDASI PENELITIAN', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (15, 8, 'SURAT PENGANTAR PENELITIAN', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (16, 8, 'SURAT PENGANTAR PENELITIAN', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (17, 9, 'KOORDINATOR METOPEN', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (18, 10, 'URUTAN SUSUNAN LAPORAN METOPEN', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (19, 10, 'URUTAN SUSUNAN', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (20, 11, 'BAB 1', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (21, 11, 'SUSUNAN BAB 1', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (22, 12, 'BAB 2', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (23, 12, 'SUSUNAN BAB 2', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (24, 13, 'BAB 3', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `pattern` VALUES (25, 13, 'SUSUNAN BAB 3', '2023-03-03 00:00:01', '2023-03-03 00:00:01');

-- ----------------------------
-- Table structure for response
-- ----------------------------
DROP TABLE IF EXISTS `response`;
CREATE TABLE `response`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `tag_id` int NULL DEFAULT NULL,
  `pattern_id` int NULL DEFAULT NULL,
  `response` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of response
-- ----------------------------
INSERT INTO `response` VALUES (1, 1, 1, 'jawaban tidak ditemukan mohon ulangi pertanyaan dan tekan maksud anda :)', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `response` VALUES (2, 2, 2, 'waalaikumsalam warrahmatullahi wabarakatuh, ada yang bisa di bantu.?', '2023-03-04 00:00:01', '2023-03-04 00:00:01');
INSERT INTO `response` VALUES (3, 3, 3, 'Halo, ada yang bisa dibantu?', '2023-03-05 00:00:01', '2023-03-05 00:00:01');
INSERT INTO `response` VALUES (4, 4, 5, 'Berikut hal yang harus dipenuhi mahasiswa dalam penyusunan proposal (dalam kuliah metopen dan PPTA) :((br))((/br))\n                (1). Mahasiswa sedang atau sudah mengambil metopen.((/br))\n                (2). Jumlah SKS minimal 100 SKS.((/br))\n                (3). Melengkapi berkas penyusunan proposal, terdiri dari : review minimal 5 makalah dan form persetujuan dosen wali dan dosen pembimbing.', '2023-03-07 00:00:01', '2023-03-07 00:00:01');
INSERT INTO `response` VALUES (5, 5, 6, 'Berikut beberapa persyaratan yang harus dipenuhi oleh mahasiswa untuk pengajuan sempro :((br))((/br))\n                (1). Lulus metopen dengan nilai minimal B-.((/br))\n                (2). Jika proposal adalah rekomendasi PPTA bisa mengajukan sempro dengan ACC dosen pembimbing.((/br))\n                (3). Membayar sempro dengan jenis pembayaran \"SEMINAR PROPOSAL\" sebesar Rp. 75.000.00. jika mengulang maka bayar dengan jenis pembayaran \"LAIN-LAIN\" sebesar Rp. 75.000.00.((/br))\n                (4). Ketika setelah pandemi (online / new normal), mahasiswa Mengisi Google Form pengajuan Sempro dengan syarat sebagai berikut :((br))((/br))\n                - Naskah proposal (ACC pembimbing).((/br))\n                - Logbook bimbingan minimal 10x.((/br))\n                - Transkrip nilai ACC dosen pembimbing akademik.((/br))\n                - TOEFL (min. 400).((/br))\n                - Bukti pembayaran sempro (75rb).((/br))\n                - Screenshot upload SKPI di portal.((/br))\n                - Sertifikat pelatihan literasi dari perpustakaan.((/br))\n                - Hasil check similarity dokumen proposal maksimal 25%.', '2023-03-07 00:00:01', '2023-03-07 00:00:01');
INSERT INTO `response` VALUES (6, 6, 7, 'Berikut pelaksanaan sempro yang wajib diketahui oleh mahasiswa :((br))((/br))\n                (1). Jadwal sempro paling lambat 7 hari setelah pendaftaran.((/br))\n                (2). Sempro dapat dilaksanakan secara online menggunakan google meet / zoom atau juga bisa secara offline jika memungkinkan dengan menggunakan protokol kesehatan yang berlaku di UAD. Teknis pelaksanaan sesuai dengan persetujuan antara mahasiswa, pembimbing dan penguji.((/br))\n                (3). Pembimbing beserta penguji akan memberikan hasil rekomendasi yaitu :((/br))\n                - Tidak lulus / mengulang((/br))\n                - Lulus dengan perbaikan (jangka waktu 1 minggu, jika melebihi waktu tersebut harus ujian ulang).', '2023-03-07 00:00:01', '2023-03-07 00:00:01');
INSERT INTO `response` VALUES (7, 7, 9, 'Mahasiswa bisa mendaftar secara online dengan mengisi google form melalui tautan dibawah ini :((br))((/br))\n                https://s.uad.id/reg_semprop_tif ((br))((/br))\n                (catatan : Tautan hanya terbuka saat periode pendaftaran sempro)', '2023-03-07 00:00:01', '2023-03-07 00:00:01');
INSERT INTO `response` VALUES (8, 8, 11, 'Unduh berkas rekomendasi penelitian, mahasiswa dapat mengunduhnya melalui tautan dibawah ini : ((br))((/br))\n                https://tif.uad.ac.id/wp-content/uploads/FR-RP_Form_Rekomendasi_Penelitian_Riset.pdf', '2023-03-07 00:00:01', '2023-03-07 00:00:01');
INSERT INTO `response` VALUES (9, 9, 17, 'berikut adalah nama dari koordinator metopen : ((/br))Supriyanto S.T., M.T', '2023-03-07 00:00:01', '2023-03-07 00:00:01');
INSERT INTO `response` VALUES (10, 10, 18, 'Berikut adalah urutan beserta penjelasan dalam penyusunan metopen : ((/br))\n                (1). Halaman cover : judul metopen, lambang UAD, nama dan NIM, nama prodi, fakultas, perguruan tinggi dan tahun penyusunan laporan.((/br))\n                (2). Daftar isi : berisi gambaran menyeluruh tentang isi metopen secara garis besar dan juga sebagai petunjuk bagi pembaca yang ingin melihat secara langsung suatu pokok bahasan.((/br))\n                (3). Daftar gambar : berisi gambar, foto, grafik yang terdapat didalam laporan dibuat sesuai urutan dan disertai halaman.((/br))\n                (4). Daftar tabel (jika ada) : jika terdapat tabel maka dibuat urutan tabel dan disertai halamannya.((/br))\n                (5). Abstrak : uraian singkat tetapi lengkap terdiri dari 250-300 kata dan memberikan gambaran menyeluruh tentang penelitian.((/br))\n                (6). BAB 1((/br))\n                (7). BAB 2((/br))\n                (8). BAB 3((/br))\n                (9). Daftar Pustaka', '2023-03-07 00:00:01', '2023-03-07 00:00:01');
INSERT INTO `response` VALUES (11, 11, 20, 'berikut adalah urutan dalam penyusunan bab 1 : ((/br))\n                (1). pendahuluan ((/br))\n                (2). Latar Belakang : Persoalan utama dalam melakukan penelitian adalah mengidentifikasi latar belakang masalah.((/br))\n                (3). Rumusan masalah : berisi pernyataan mengenai permasalahan dan disertai pertanyaan penelitian.((/br))\n                (4). Batasan masalah : ruang lingkup untuk membatasi lingkup permasalahan dengan memilih masalah inti yang telah disebutkan di bagian identifikasi masalah, sehingga tidak terlalu luas untuk diberi solusi dalam penelitian yang akan dilakukan.((/br))\n                (5). Tujuan penelitian : menyelesaikan masalah dengan pendekatan keilmuan tertentu.((/br))\n                (6). Manfaat penelitian : Pernyataan manfaat penelitian harus menunjukkan kontribusi pengetahuan atau dirasakan langsung oleh stakeholder.', '2023-03-07 00:00:01', '2023-03-07 00:00:01');
INSERT INTO `response` VALUES (12, 12, 22, 'berikut adalah urutan dalam penyusunan bab 2 : ((/br))\n            (1). Daftar Pustaka -> Bagian ini berisi kajian penelitian terdahulu yang terkait dengan penelitian yang dilakukan. Landasan teori mengkaji teori, pengertian, variabel yang sesuai dan hasil penelitian yang dimuat dalam berbagai sumber yang kredibel.((/br))\n            (2). Kajian penelitian terdahulu : Membahas penelitian sebelumnya yang berkaitan dengan judul yang diambil sehingga bisa membedakan antara penelitian yang dilakukan dengan penelitian sebelumnya. Kajian penelitian dipilih dari penelitian maksimal 5 tahun terakhir sebanyak minimal 5penelitian , dapat diambil dari buku, jurnal ilmiah (nasional maupun yang da internasional ), laporan hasil penelitian, sumber lain pat dipakai sebagai referensi untuk menunjang penelitian.((/br))\n            (3). Landasan Teori : landasan teori yang perlu dikemukakan adalah tentang teori konsep - teori atau konsep yang erat kaitannya dengan permasalahan penelitian. Fungsi teori atau konsep di sini adalah sebagai landasan berpikir atau argumentasi dalam pemecahan masalah penelitian, d an perumusan hipotesis penelitian.\n', '2023-03-07 00:00:01', '2023-03-07 00:00:01');
INSERT INTO `response` VALUES (13, 13, 24, 'berikut adalah urutan dalam penyusunan bab 3 : bab 3 Metodologi Penelitian ((/br))\n            (1). Metode pengumpulan data : kumpulan prosedur atau teknik yang dilakukan peneliti untuk memperoleh data penelitian. Pada bagian ini, mahasiswa harus menjabarkan data yang hendak didapatkan beserta teknik pengumpulan datanya.((/br))\n            (2). Spesifikasi kebutuhan : berisi deskripsi dari alat dan berbagai bahan yang digunakan dalam penelitian khususnya pada tahap eksperimen atau pengembangan perangkat lunak.((/br))\n            (3). Tahapan penelitian : Jelaskan secara rinci tahapan penelitian yang akan dilakukan beserta rencana luaran dari setiap tahapan.((/br))\n            (4). Pengujian sistem : menjelaskan teknik pengujian yang akan dipakai dalam penelitian yang dilakukan.', '2023-03-07 00:00:01', '2023-03-07 00:00:01');

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `tag` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tag
-- ----------------------------
INSERT INTO `tag` VALUES (1, 'wildcard', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `tag` VALUES (2, 'salam', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `tag` VALUES (3, 'sapaan', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `tag` VALUES (4, 'kategori 1', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `tag` VALUES (5, 'kategori 2', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `tag` VALUES (6, 'kategori 3', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `tag` VALUES (7, 'kategori 4', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `tag` VALUES (8, 'kategori 5', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `tag` VALUES (9, 'kategori 6', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `tag` VALUES (10, 'kategori 7', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `tag` VALUES (11, 'kategori 8', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `tag` VALUES (12, 'kategori 9', '2023-03-03 00:00:01', '2023-03-03 00:00:01');
INSERT INTO `tag` VALUES (13, 'kategori 10', '2023-03-03 00:00:01', '2023-03-03 00:00:01');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `fullname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'Admin', 'admin', 'user@mail.com', 'test1234#', '2023-03-06 21:39:58', '2023-03-06 21:39:58');

SET FOREIGN_KEY_CHECKS = 1;
