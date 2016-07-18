#! usr/bin/python


from tinytag import TinyTag
import pymysql.cursors
import eyeD3
import os
from mutagen.mp3 import MP3


path = "/home/marom/albums/10 Years - From Birth To Burial (2015)/01. From Birth To Burial.mp3"
path_2 = "/home/marom/albums/10 Years - From Birth To Burial (2015)/02. Selling Skeletons.mp3" 
path_3 = "/home/marom/albums/65daysofstatic/(2011) 65daysofstatic - Silent Running/Silent Running/02 - Space Theme.mp3"
path_4 = "/home/marom/albums/2014.Between The Stars/01 Set Me On Fire.mp3"
path_5 = "/home/marom/albums/2013 - Save Rock And Roll/01. The Phoenix.mp3"
path_6 = "/home/marom/music/"
#######################################################################################################

def get_files_names_2_sizes(path):	
	all_files = []	
	all_folders = [x[0] for x in os.walk(path)]
	for folder in all_folders:
		folder_files = os.listdir(folder)
		for song in folder_files:
			if song.endswith(".mp3"):
				file_path = os.path.join(path,folder,song)
				all_files.append(file_path)	
	files_dict = dict()
	for f in all_files:
		size = os.path.getsize(f)
		files_dict[f] = size
	return files_dict

def get_eyed3_tags(path):
    trackInfo = eyeD3.Mp3AudioFile(path)
    tag = trackInfo.getTag()
    tag.link(path)
    tag.getArtist()
    tag.getAlbum()
    tag.getTitle()
    trackInfo.getPlayTimeString()



def remove_values_from_list(the_list, val):
	return [value for value in the_list if value != val]




######################################################################################################
files_2_sizes = get_files_names_2_sizes(path_6)
from progressbar import ProgressBar
pbar = ProgressBar()
new_list = list(files_2_sizes.keys())
songs_with_errors = 0
albums_with_errors = 0
artists_with_errors = 0
total_songs = 0
total_albums = 0
total_artists = 0
for i in pbar(new_list):
	tag = eyeD3.Tag()
	tag.link(i)
	tag_2 = TinyTag.get(i)
	size = tag_2.filesize
	audio = MP3(i)
	length = audio.info.length
	new_path = i
	artist = tag.getArtist()
	if artist.strip() == "":
		artists_with_errors += 1
		continue
	album = tag.getAlbum()
	if album.strip() == "":
		albums_with_errors += 1
		continue
	song = tag.getTitle()
	if song.strip() == "":
		songs_with_errors += 1
		continue
	data = [artist, album, song]
	connection = pymysql.connect(host='localhost',
				user='root',
				password='1q2w3e4r',
				db='new_schema',
				cursorclass=pymysql.cursors.SSCursor)
	with connection.cursor() as cursor:		
			try:
				cursor.execute("select count(*) from artists where name = %s " , artist)
				count_artist = cursor.fetchone()[0]
				if count_artist == 0:
					cursor.execute ("insert into artists (name) values (%s)", artist)	
					total_artists += 1
				artist_id_number = cursor.execute("select id from artists where name = %s ", artist)
				artist_id_number = cursor.fetchone()
				cursor.execute("select count(*) from albums where name = %s and artist_id = %s " ,( album, artist_id_number[0]))
				count_album = cursor.fetchone()[0]
				if count_album == 0:
					cursor.execute ("insert into albums (name,artist_id) values (%s, %s)", (album, artist_id_number[0]))	
					total_albums += 1
				album_id_number = cursor.execute("select id from albums where name = %s and artist_id = %s", (album, artist_id_number))
				album_id_number = cursor.fetchone()
				cursor.execute("select count(*) from songs where song_name = %s and album_id = %s" , (song, album_id_number[0]))
				count_song = cursor.fetchone()[0]
				if count_song == 0:
					cursor.execute ("insert into songs (song_name,album_id,length,size,path) values (%s, %s, %s, %s,%s)", (song, album_id_number[0], length,size, new_path))	
					total_songs += 1
				cursor.execute ("select song_name from songs where song_name = %s and album_id = %s" , (song, album_id_number[0]))
				cursor.execute("select path from songs where song_name = %s and album_id = %s" , (song, album_id_number[0]))
				cursor.fetchone()
				path_in_db = cursor.fetchone()
				if path_in_db != new_path:
					cursor.execute("update songs set path =%s where song_name = %s and album_id = %s" , (new_path, song, album_id_number))
				
			except :
				songs_with_errors += 1
				pass

	connection.commit()
print "The number of songs that had errors and did'nt got inserted into the table is " + str(songs_with_errors)
print "The number of albums that had errors and did'nt got inserted into the table is " + str(albums_with_errors)
print "The number of artists that had errors and did'nt got inserted into the table is " + str(artists_with_errors)
print "The number of songs that got inserted into the table is " + str(total_songs)
print "The number of albums that got inserted into the table is " + str(total_albums)
print "The number of artists that got inserted into the table is " + str(total_artists)
