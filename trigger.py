from importlib.resources import path
import os
import sys
import logging
import subprocess
from threading import Thread
from queue import Queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

file_queue = Queue()

class EventHandler(FileSystemEventHandler):
	'''Watches a specific folder and raises events on_created and on_deleted'''

	


	def __init__(self) -> None:
		super().__init__()
		self.not_logged=True

	def on_any_event(self, event):
		super().on_any_event(event)	
		#logging.info("New file: {}".format(event.src_path))
		logging.info(event)


	
	def on_created(self, event):
		'''
		Handles on_created event. Just notes to logger when a file/folder is created.
		:param event:
		:return:
		'''
		super().on_created(event)
		if not event.is_directory:
			logging.info("New file: {}".format(event.src_path))
		else:
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
		else:
			logging.info("Deleted folder: %s", event.src_path)

	
	def on_modified(self, event):
		'''
		Handles on_modified event. Just notes to logger when a file/folder is modified.
		:param event:
		:return:
		'''
		super().on_modified(event)
		if not event.is_directory:
		
			logging.info("Modified file: %s", event.src_path)
		else:
			logging.info("Modified folder: %s", event.src_path)



if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	#path = sys.argv[1] if len(sys.argv) > 1 else '.'
	path = r"C:\Users\ACER\Dev\disecto\watched"
	event_handler = EventHandler()
	observer = Observer()
	observer.schedule(event_handler, path, recursive=True)
	observer.start()
	observer.join()