from dataclasses import dataclass
from io import StringIO
from datetime import datetime
from importlib.resources import path
import os
from sqlite3 import Timestamp
import sys
import logging
import subprocess
from csv import writer
from threading import Thread
from queue import Queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

log_stream = StringIO() 

class EventHandler(FileSystemEventHandler):
	'''Watches a specific folder and raises events on_created and on_deleted'''
		
	def __init__(self) -> None:
		super().__init__()

		self.moved=False
		self.output_filename=r'../logs.csv'

	
	def log_csv(self,timestamp,event,src='',dest=''):
		src=str(src)
		dest=str(dest)
		data=[timestamp,event,src,dest]
		output_filename = r'./logs.csv'
		with open(output_filename, 'a+', newline='') as write_obj: 
			csv_writer = writer(write_obj) 
			csv_writer.writerow(data)

		

	# def on_any_event(self, event):
	# 	super().on_any_event(event)	
	# 	#logging.info("New file: {}".format(event.src_path))
	# 	logging.info(event)



	# def on_moved(self, event):
	# 	'''
	# 	Handles on_moved/renamed event.Just notes to csv when a on_moved/renamed is created.
	# 	:param event:
	# 	:return:
	# 	'''
	# 	try:
	# 		super().on_moved(event)
	# 	except TypeError:
	# 		pass
	# 	finally:
	# 		src=	list(str(event.src_path).split('//'))
	# 		dest=list(str(event.dest_path).split('//'))
	# 		self.on_moved=True
	# 		if(''.join(src)[:len(src)-1]==''.join(dest)[:len(src)-1]):
	# 			self.log_csv(datetime.now(),'Renamed File',event.src_path)

			
	# 			logging.info("Renamed: {}".format(event.src_path))
	# 		else:
	# 			self.log_csv(str(datetime.now()),'Moved File',event.src_path,event.dest_path)
	# 			logging.info("Moved to another folder: {}".format(event.src_path))



	
	def on_created(self, event):
		'''
		Handles on_created event. Just notes to csv when a file/folder is created.
		:param event:
		:return:
		'''
		super().on_created(event)
		if not event.is_directory:
			self.log_csv(str(datetime.now()),'Created File',event.src_path)
			logging.info("New file: {}".format(event.src_path))
		else:
			self.log_csv(str(datetime.now()),'Created Folder',event.src_path)
			logging.info("New folder: {}".format(event.src_path))



	def on_deleted(self, event):
		'''
		Handles on_deleted event. Just notes to logger when a file/folder is deleted.
		:param event:
		:return:
		'''
		super().on_deleted(event)
		if not event.is_directory:
			logging.info("Deleted file: %s", event.src_path)
			self.log_csv(str(datetime.now()),'Deleted File',event.src_path)
		else:
			logging.info("Deleted folder: %s", event.src_path)
			self.log_csv(str(datetime.now()),'Deleted Folder',event.src_path)

	
	def on_modified(self, event):
		'''
		Handles on_modified event. Just notes to logger when a file/folder is modified.
		:param event:
		:return:
		'''
		super().on_modified(event)
		# if(self.on_moved):
		# 	self.on_moved=False
		# 	return
		
		if not event.is_directory:
		
			logging.info("Modified file: %s", event.src_path)
			self.log_csv(str(datetime.now()),'Modified File',event.src_path)
		else:
			hel=logging.info("Modified folder: %s", event.src_path)
			self.log_csv(str(datetime.now()),'Modified Folder',event.src_path)
			



if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	#path = sys.argv[1] if len(sys.argv) > 1 else '.'

	with open(r'./logs.csv', "w") as write_obj: 
		csv_writer = writer(write_obj)
		csv_writer.writerow(['Timestamp(+5:30GMT)','Event Type','SourceLocation','NewLocation']) 
		write_obj.close()
	path = r"C:\Users\ACER\Dev\disecto\watched"
	event_handler = EventHandler()
	observer = Observer()
	observer.schedule(event_handler, path, recursive=False)
	observer.start()
	observer.join()