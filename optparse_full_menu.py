#! /usr/bin/python
import optparse
from optparse import OptionParser
import os
from mutagen.mp3 import MP3
import pymysql.cursors

files_2_sizes = 0
length_dict = 0

def print_biggest_song(option, opt_str, value, parser):			
	global files_2_sizes
	is_human_readable = parser.values.human
	is_printed = parser.values.printed
	if files_2_sizes == 0:
		files_2_sizes = size_dict_from_db_table()
	get_biggest_file_name_new(is_human_readable)

def print_smallest_song(option, opt_str, value, parser):	
	global files_2_sizes	
	is_human_readable = parser.values.human
	is_printed = parser.values.printed
	if files_2_sizes == 0:
		files_2_sizes = size_dict_from_db_table()				
	get_smallest_file_name_new(is_human_readable)

def print_all_songs_size(option, opt_str, value, parser):	
	global files_2_sizes
	is_human_readable = parser.values.human
	is_printed = parser.values.printed
	if files_2_sizes == 0:
		files_2_sizes = size_dict_from_db_table()
	get_all_files_size_new(is_human_readable)

def print_longest_song(option, opt_str, value, parser):	
	global length_dict
	is_human_readable = parser.values.human
	is_printed = parser.values.printed
	if length_dict == 0:
		length_dict = length_dict_from_db_table()
	get_longest_song_name_new(is_human_readable)

def print_shortest_song(option, opt_str, value, parser):	
	global length_dict
	is_human_readable = parser.values.human
	is_printed = parser.values.printed
	if length_dict == 0:
		length_dict = length_dict_from_db_table()
	get_shortest_song_name_new(is_human_readable)

def print_average_length_song(option, opt_str, value, parser):
	global length_dict
	is_human_readable = parser.values.human
	is_printed = parser.values.printed
	if length_dict == 0:
		length_dict = length_dict_from_db_table()
	get_average_songs_length_new(is_human_readable)

def print_artist_with_most_songs(option, opt_str, value, parser):
	get_artist_with_most_songs()

def print_artist_with_least_songs(option, opt_str, value, parser):
	get_artist_with_least_songs()

def print_album_with_most_songs(option, opt_str, value, parser):
	get_album_with_most_songs()

def print_album_with_least_songs(option, opt_str, value, parser):
	get_album_with_least_songs()

def print_average_songs_in_album(option, opt_str, value, parser):
	get_average_songs_for_an_album()

def print_average_songs_in_artist(option, opt_str, value, parser):
	get_average_songs_for_an_artist()



#################################################################################################


def get_files_names_2_sizes_old(path):	
	files = os.listdir(path)
	files_dict = dict()
	for f in files:
		file_path = os.path.join(path, f)
		size = os.path.getsize(file_path)
		files_dict[f] = size
	return files_dict


def get_files_names_2_sizes(should_print, path):	
	if os.path.isfile("/home/marom/files_2_sizes.txt") == False:
		if should_print:
			print "Loading size directory"
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
		if should_print:
			print "Done loading size directory"
		file = open("/home/marom/files_2_sizes.txt", "w")
		for key,value in files_dict.items():
			line1 = str(key)
			line2 = str(value)
			line = str(line1+ ' |  ' + line2) + "\n"
			file.write(line)	
		file.close()
		return files_dict

	elif os.path.isfile("/home/marom/files_2_sizes.txt") == True:
		if should_print:
			print "Loading size directory"
		if should_print:
			print "Done loading size directory"
		with open ("/home/marom/files_2_sizes.txt", 'r') as file:
			files_dict = {}
			for line in file:
				if line.strip():  
					key, value = line.split("|", 1)  
					files_dict[key] = float(value.split()[0])
			return files_dict

def write_dict_to_file(d,file_name):
	file = open(file_name, "w")
	for key,value in d.items():
            line1 = str(key)
	    line2 = str(value)
	    line = str(line1 + ' ,  ' + line2) + "\n"
            file.write(line)	
	file.close()


def read_file_to_dict(file_name):
	with open (file_name, 'r') as file:
		answer = {}
		for line in file:
			if line.strip():  
				key, value = line.split(",", 1)  
				answer[key] = value.split()





def get_biggest_file_name_old(files_2_sizes):
	biggest_file_name = ""
	biggest_file_size = 0
	for file_name in files_2_sizes:
		file_size = files_2_sizes[file_name]
		if file_size > biggest_file_size:
			biggest_file_size = file_size
			biggest_file_name = file_name
	return biggest_file_name


def get_biggest_file_name_new(should_change):
	connection = pymysql.connect(host='localhost',
			user='root',
			password='1q2w3e4r',
			db='new_schema',
			cursorclass=pymysql.cursors.SSCursor)
	with connection.cursor() as cursor:		
		try:
			cursor.execute("select path,size from songs where size = (select max(size) from songs)")
			biggest_song = cursor.fetchone()
			biggest_song_path = biggest_song[0]
			biggest_song_size = biggest_song[1]
			if should_change:
				print "the biggest song is %s and it's size is %s" % (biggest_song_path, biggest_song_size)
			else:
				biggest_song_size_readable = get_human_readable(biggest_song_size)
				print "the biggest song is %s and it's size is %s" % (biggest_song_path, biggest_song_size_readable)
	
		except:	
			pass
	connection.close()



def get_smallest_file_name(files_2_sizes):
	smallest_file_name = files_2_sizes.keys()[0]
	smallest_file_size = files_2_sizes[smallest_file_name]
	for file_name in files_2_sizes:
		file_size = files_2_sizes[file_name]
		if file_size < smallest_file_size:
			smallest_file_size = file_size
			smallest_file_name = file_name
	return smallest_file_name


def get_smallest_file_name_new(should_change):
	connection = pymysql.connect(host='localhost',
			user='root',
			password='1q2w3e4r',
			db='new_schema',
			cursorclass=pymysql.cursors.SSCursor)
	with connection.cursor() as cursor:		
		try:
			cursor.execute("select path,size from songs where size = (select min(size) from songs)")
			smallest_song = cursor.fetchone()
			smallest_song_path = smallest_song[0]
			smallest_song_size = smallest_song[1]
			if should_change:
				print "the smallest song is %s and it's size is %s" % (smallest_song_path, smallest_song_size)
			else:
				smallest_song_size_readable = get_human_readable(smallest_song_size)
				print "the smallest song is %s and it's size is %s" % (smallest_song_path, smallest_song_size_readable)
				
		except:	
			pass
	connection.close()

def get_all_files_size_new(should_change):
	connection = pymysql.connect(host='localhost',
			user='root',
			password='1q2w3e4r',
			db='new_schema',
			cursorclass=pymysql.cursors.SSCursor)
	with connection.cursor() as cursor:		
		try:
			cursor.execute("select sum(size) from songs")
			all_songs_size = cursor.fetchone()[0]
			if should_change:
				print "the size of all songs combined is %s " % all_songs_size
			else:
				all_songs_size_readable = get_human_readable(int(all_songs_size))
				print "the size of all songs combined is %s " % all_songs_size_readable
		except:	
			pass
	connection.close()


def get_all_files_size(files_2_sizes):
	total_files_size = 0
	for file_name in files_2_sizes:
		file_size = files_2_sizes[file_name]
		total_files_size += file_size
	return total_files_size


def get_human_readable(number):
	suffix_array = ["B", "K", "M", "G", "T"] 
	num_of_divisions = 0
	suffix = suffix_array[num_of_divisions]
	while number >= 1000:
		number = number / 1000.0
		num_of_divisions += 1
		suffix = suffix_array[num_of_divisions]
	return "%.1f%s" % (number, suffix)


def get_readable_length(length):
	suffix_array = ["S", "M", "H"]
	num_of_divisions = 0
	suffix = suffix_array[num_of_divisions]
	while length >= 60:
		length = length / 60.0
		num_of_divisions += 1
		suffix = suffix_array[num_of_divisions]
	return "%.1f%s" % (length, suffix)

def get_files_names_2_length(should_print, path):	
	if os.path.isfile("/home/marom/files_2_length.txt") == False:
		if should_print:
			print "Loading length directory"
		all_files = []	
		all_folders = [x[0] for x in os.walk(path)]
		for folder in all_folders:
			folder_files = os.listdir(folder)
			for song in folder_files:
				file_path = os.path.join(path,folder,song)
				if file_path.endswith(".mp3"):
					all_files.append(file_path)	
		files_dict = dict()
		for f in all_files:
			length = MP3(f).info.length
			files_dict[f] = length
		if should_print:
			print "Done loading length directory"
		file = open("/home/marom/files_2_length.txt", "w")
		for key,value in files_dict.items():
			line1 = str(key)
			line2 = str(value)
			line = str(line1 + ' |  ' + line2) + "\n"
			file.write(line)	
		file.close()
		return files_dict

	elif os.path.isfile("/home/marom/files_2_length.txt") == True:
		if should_print:
			print "Loading size directory"
		with open ("/home/marom/files_2_length.txt", 'r') as file:
			files_dict = {}
			for line in file:
				if line.strip():  
					key, value = line.split("|", 1)  
					files_dict[key] = float(value.split()[0])
		if should_print:
			print "Done loading size directory"
		return files_dict


def get_longest_song_name(length_dict):
	longest_file_name = ""
	longest_file_length = 0
	for file_name in length_dict:
		file_length = length_dict[file_name]
		if file_length > longest_file_length:
			longest_file_length = file_length
			longest_file_name = file_name
	return longest_file_name


def get_longest_song_name_new(should_change):
	connection = pymysql.connect(host='localhost',
			user='root',
			password='1q2w3e4r',
			db='new_schema',
			cursorclass=pymysql.cursors.SSCursor)
	with connection.cursor() as cursor:		
		try:
			cursor.execute("select path,length from songs where length = (select max(length) from songs)")
			longest_song = cursor.fetchone()
			longest_song_path = longest_song[0]
			longest_song_length = longest_song[1]
			if should_change:
				print "the longest song is %s and it's length is %s" % (longest_song_path, longest_song_length)
			else:
				longest_song_length_readable = get_readable_length(longest_song_length)
				print "the longest song is %s and it's length is %s" % (longest_song_path, longest_song_length_readable)
				
		except:	
			pass
	connection.close()


def get_shortest_song_name(length_dict):
	shortest_file_name = length_dict.keys()[0]
	shortest_file_length = length_dict[shortest_file_name]
	for file_name in length_dict:
		file_length = length_dict[file_name]
		if file_length < shortest_file_length:
			shortest_file_length = file_length
			shortest_file_name = file_name
	return shortest_file_name


def get_shortest_song_name_new(should_change):
	connection = pymysql.connect(host='localhost',
			user='root',
			password='1q2w3e4r',
			db='new_schema',
			cursorclass=pymysql.cursors.SSCursor)
	with connection.cursor() as cursor:		
		try:
			cursor.execute("select path,length from songs where length = (select min(length) from songs)")
			shortest_song = cursor.fetchone()
			shortest_song_path = shortest_song[0]
			shortest_song_length = shortest_song[1]
			if should_change:
				print "the shortest song is %s and it's length is %s" % (shortest_song_path, shortest_song_length)
			else:
				shortest_song_length_readable = get_readable_length(shortest_song_length)
				print "the shortest song is %s and it's length is %s" % (shortest_song_path, shortest_song_length_readable)
				
		except:	
			pass
	connection.close()

def get_average_songs_length(length_dict):
	dict_value = 0
	dict_key_count = 0
	value_average = 0
	for value in length_dict.values():
		dict_value += value
		dict_key_count += 1
	value_average = (dict_value / dict_key_count) / 60
	return value_average

def get_average_songs_length_new(should_change):
	connection = pymysql.connect(host='localhost',
			user='root',
			password='1q2w3e4r',
			db='new_schema',
			cursorclass=pymysql.cursors.SSCursor)
	with connection.cursor() as cursor:		
		try:
			cursor.execute("select avg(length) from songs")
			song_average_length = cursor.fetchone()[0]
			if should_change:
				print "the length of an average song is %s " % song_average_length
			else:
				song_average_length_readable = get_readable_length(int(song_average_length))
				print "the length of an average song is %s " % song_average_length_readable
		except:	
			pass
	connection.close()



def size_dict_from_db_table():
	connection = pymysql.connect(host='localhost',
                                user='root',
                                password='1q2w3e4r',
                                db='new_schema',
                                cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		cursor.execute ("select Path,Size from songs")
		data = cursor.fetchall ()
		songs_dict = dict()
		for row in data:
			data_list1 =  str(row["Path"])
			data_list2 = int(row["Size"])
			songs_dict[data_list1] = data_list2
		return songs_dict

	cursor.close ()

	connection.commit()

def length_dict_from_db_table():
	connection = pymysql.connect(host='localhost',
                                user='root',
                                password='1q2w3e4r',
                                db='new_schema',
                                cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		cursor.execute ("select Path,Length from songs")
		data = cursor.fetchall ()
		songs_dict = dict()
		for row in data:
			data_list1 =  str(row["Path"])
			data_list2 = (row["Length"])
			songs_dict[data_list1] = data_list2
		return songs_dict

	cursor.close ()

	connection.commit()



def get_artist_with_most_songs():
	connection = pymysql.connect(host='localhost',
                                user='root',
                                password='1q2w3e4r',
                                db='new_schema',
                                cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		cursor.execute("select artists.name, count(songs.song_name) as hi from artists right join albums on artists.id = albums.artist_id right join songs on albums.id = songs.album_id group by artists.name order by hi desc limit 1")

		most_songs = cursor.fetchone()
		artist_with_most_songs = most_songs.values()[1]
		number_of_songs = most_songs.values()[0]
		print "the artist with most songs is %s and the number of songs she/he have is %s " % (artist_with_most_songs, number_of_songs)
	cursor.close ()

	connection.commit()


def get_artist_with_least_songs():
	connection = pymysql.connect(host='localhost',
                                user='root',
                                password='1q2w3e4r',
                                db='new_schema',
                                cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		cursor.execute("select artists.name, count(songs.song_name) as hi from artists right join albums on artists.id = albums.artist_id right join songs on albums.id = songs.album_id group by artists.name order by hi asc limit 1")

		least_songs = cursor.fetchone()
		artist_with_least_songs = least_songs.values()[1]
		number_of_songs = least_songs.values()[0]
		print "the artist with least songs is %s and the number of songs she/he have is %s " % (artist_with_least_songs, number_of_songs)
	cursor.close ()

	connection.commit()

def get_album_with_most_songs():
	connection = pymysql.connect(host='localhost',
                                user='root',
                                password='1q2w3e4r',
                                db='new_schema',
                                cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		cursor.execute("select albums.name, count(songs.song_name) as hi from albums right join songs on albums.id = songs.album_id group by albums.name order by hi desc limit 1")

		most_songs = cursor.fetchone()
		album_with_most_songs = most_songs.values()[1]
		number_of_songs = most_songs.values()[0]
		print "the album with most songs is %s and the number of songs it have is %s " % (album_with_most_songs, number_of_songs)
	cursor.close ()

	connection.commit()

def get_album_with_least_songs():
	connection = pymysql.connect(host='localhost',
                                user='root',
                                password='1q2w3e4r',
                                db='new_schema',
                                cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		cursor.execute("select albums.name, count(songs.song_name) as hi from albums right join songs on albums.id = songs.album_id group by albums.name order by hi asc limit 1")

		least_songs = cursor.fetchone()
		album_with_least_songs = least_songs.values()[1]
		number_of_songs = least_songs.values()[0]
		print "the album with least songs is %s and the number of songs it have is %s " % (album_with_least_songs, number_of_songs)
	cursor.close ()

	connection.commit()


def get_average_songs_for_an_album():
	connection = pymysql.connect(host='localhost',
                                user='root',
                                password='1q2w3e4r',
                                db='new_schema',
                                cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		cursor.execute("SELECT  (select count(songs.song_name) from songs) as num_of_songs , (select count(albums.name) from albums) as num_of_albums,  (select num_of_songs/num_of_albums)")

		average_songs = cursor.fetchone()
		album_average_songs = average_songs.values()[0]
		print "the average number of songs for an album is  %s " % (album_average_songs)
	cursor.close ()

	connection.commit()

def get_average_songs_for_an_artist():
	connection = pymysql.connect(host='localhost',
                                user='root',
                                password='1q2w3e4r',
                                db='new_schema',
                                cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		cursor.execute("SELECT  (select count(songs.song_name) from songs) as num_of_songs , (select count(artists.name) from artists) as num_of_artists,  (select num_of_songs/num_of_artists)")
		average_songs = cursor.fetchone()
		artist_average_songs = average_songs.values()[0]
		print "the average number of songs for an artist is  %s " % (artist_average_songs)
	cursor.close ()

	connection.commit()



path = "/home/marom/music"
all_files = []	
all_folders = [x[0] for x in os.walk(path)]
for folder in all_folders:
	folder_files = os.listdir(folder)
	for song in folder_files:
		all_files.append(song)




parser = OptionParser(usage = "MP3 organizer software",
		description = "Welcome to the best MP3 organizer in the web,please look and choose from the options below:")

print "\nthe size or length will be readable as default, if you dont want it to be unreadable use the -f feature before your selection"
print "the procceses made by the command will be printed if you wish it will not be printed add the -p feature before your selection\n"

parser.add_option("-b", "--biggest",
		 action = "callback", callback = print_biggest_song,
		 dest = "biggest_song", help = "This option will print the biggest song")

parser.add_option("-s", "--smallest",
		 action = "callback", callback = print_smallest_song,
		 dest = "smallest_song", help = "This option will print the smallest song")

parser.add_option("-a", "--all",
		 action = "callback", callback = print_all_songs_size,
		 dest = "all_songs", help = "This option will print the size of all songs")

parser.add_option("-l", "--longest",
		 action = "callback", callback = print_longest_song,
		 dest = "longest_song", help = "This option will print the longest song")

parser.add_option("-z", "--shortest",
		 action = "callback", callback = print_shortest_song,
		 dest = "shortest_song", help = "This option will print the shortest song")

parser.add_option("-v", "--average",
		 action = "callback", callback = print_average_length_song,
		 dest = "average_length_songs", help = "This option will print the average length of all songs")

parser.add_option("-g", "--artist_with_most_songs",
		 action = "callback", callback = print_artist_with_most_songs,
		 dest = "artist_with_most_songs", help = "This option will print the artist with most songs")

parser.add_option("-j", "--artist_with_least_songs",
		 action = "callback", callback = print_artist_with_least_songs,
		 dest = "artist_with_least_songs", help = "This option will print the artist with the least songs")

parser.add_option("-i", "--album_with_most_songs",
		 action = "callback", callback = print_album_with_most_songs,
		 dest = "album_with_most_songs", help = "This option will print the album with most songs")

parser.add_option("-q", "--album_with_least_songs",
		 action = "callback", callback = print_album_with_least_songs,
		 dest = "album_with_least_songs", help = "This option will print the album with the least songs")

parser.add_option("-r", "--average_songs_in_album",
		 action = "callback", callback = print_average_songs_in_album,
		 dest = "average_songs_in_album", help = "This option will print the average songs in an album")

parser.add_option("-w", "--average_songs_in_artist",
		 action = "callback", callback = print_average_songs_in_artist,
		 dest = "average_songs_in_artist", help = "This option will print the average songs in an artist")

parser.add_option("-f", "--human_readable_off", 
		 action = "store_true",default = False, dest = "human",
		 help = "this option will print the other options in non-human readable form")

parser.add_option("-p", "--print", 
		 action = "store_false",default = True, dest = "printed",
		 help = "this option will cancel the print action of procceses the program makes while entering a command")


(options, args) = parser.parse_args()
