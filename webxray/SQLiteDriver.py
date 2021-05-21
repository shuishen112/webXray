# standard python packages
import time 
import random
import os
import hashlib
import sqlite3
import datetime
import json

class SQLiteDriver:
	"""
	this class handles all of the database work, no sql is to be found 
		elsewhere in the code base aside from other db drivers
	"""

	def __init__(self, db_name = '', db_prefix = 'wbxr_'):
		"""
		set the root path for the db directory since sqlite dbs are not contained in a server
		if db_name is specified, set up global connection
		"""
		self.db_root_path = os.path.dirname(os.path.abspath(__file__))+'/resources/db/sqlite/'

		# the db_prefix can be overridden if you like
		self.db_prefix = db_prefix
		
		if db_name != '':
			self.db_name = self.db_prefix+db_name+'.db'
			self.db_conn = sqlite3.connect(self.db_root_path+self.db_name,detect_types=sqlite3.PARSE_DECLTYPES)
			self.db = self.db_conn.cursor()
	# __init__

	#-----------------#
	# GENERAL PURPOSE #
	#-----------------#

	def md5_text(self,text):
		"""
		this class is unique to the sqlite driver as md5 is not built in
		"""
		try:
			return hashlib.md5(text.encode('utf-8')).hexdigest()
		except:
			return None
	# md5_text

	def db_switch(self, db_name):
		"""
		connect to a new db, in sqlite this requires loading the db from disk
		"""

		# close existing connection
		self.close()

		# open the new connection
		self.db_name = self.db_prefix+db_name
		self.db_conn = sqlite3.connect(self.db_root_path+self.db_name+'.db',detect_types=sqlite3.PARSE_DECLTYPES)
		self.db = self.db_conn.cursor()
		return True
	# db_switch

	def fetch_query(self, query):
		"""
		allows executing raw queries, very unsafe and should be disabled in public-facing systems
		"""
		self.db.execute(query)
		return self.db.fetchall()
	# fetch_query

	def commit_query(self, query):
		"""
		allows executing raw queries, very unsafe and should be disabled in public-facing systems
		"""
		self.db.execute(query)
		self.db_conn.commit()
		return True
	# commit_query

	def db_exists(self, db_name):
		"""
		before creating a new db make sure it doesn't already exist, uses specified prefix
		"""
		dbs = os.listdir(self.db_root_path)
		if self.db_prefix+db_name+'.db' in dbs:
			return True
		else:
			return False
	# db_exists

	def set_config(self, config):
		"""
		Multiple variables can be stored on a per-db basis to allow the server
			to handle different conditions for different databases.  Note there is a
			field "modified" and we always use the most recent config, but can also
			see any changes made.
		"""

		self.db.execute("""
			INSERT INTO config (
				client_browser_type,
				client_prewait,
				client_no_event_wait,
				client_max_wait,
				client_get_bodies,
				client_get_bodies_b64,
				client_get_screen_shot,
				client_get_text,
				client_crawl_depth,
				client_crawl_retries,
				client_page_load_strategy,
				client_reject_redirects,
				client_min_internal_links,
				max_attempts,
				store_1p,
				store_base64,
				store_files,
				store_screen_shot,
				store_source,
				store_page_text,
				store_links,
				store_dom_storage,
				store_responses,
				store_request_xtra_headers,
				store_response_xtra_headers,
				store_requests,
				store_websockets,
				store_websocket_events,
				store_event_source_msgs,
				store_cookies,
				store_security_details,
				timeseries_enabled,
				timeseries_interval
			) VALUES (
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?
			)
		""", (
			config['client_browser_type'],
			config['client_prewait'],
			config['client_no_event_wait'],
			config['client_max_wait'],
			config['client_get_bodies'],
			config['client_get_bodies_b64'],
			config['client_get_screen_shot'],
			config['client_get_text'],
			config['client_crawl_depth'],
			config['client_crawl_retries'],
			config['client_page_load_strategy'],
			config['client_reject_redirects'],
			config['client_min_internal_links'],
			config['max_attempts'],
			config['store_1p'],
			config['store_base64'],
			config['store_files'],
			config['store_screen_shot'],
			config['store_source'],
			config['store_page_text'],
			config['store_links'],
			config['store_dom_storage'],
			config['store_responses'],
			config['store_request_xtra_headers'],
			config['store_response_xtra_headers'],
			config['store_requests'],
			config['store_websockets'],
			config['store_websocket_events'],
			config['store_event_source_msgs'],
			config['store_cookies'],
			config['store_security_details'],
			config['timeseries_enabled'],
			config['timeseries_interval']
			)
		)
		self.db_conn.commit()
	# set_config

	def get_config(self):
		"""
		Return the current configuration, where current is the most
			recently modified entry.
		"""

		self.db.execute("""
			SELECT
				client_browser_type,
				client_prewait,
				client_no_event_wait,
				client_max_wait,
				client_get_bodies,
				client_get_bodies_b64,
				client_get_screen_shot,
				client_get_text,
				client_crawl_depth,
				client_crawl_retries,
				client_page_load_strategy,
				client_reject_redirects,
				client_min_internal_links,
				max_attempts,
				store_1p,
				store_base64,
				store_files,
				store_screen_shot,
				store_source,
				store_page_text,
				store_links,
				store_dom_storage,
				store_responses,
				store_request_xtra_headers,
				store_response_xtra_headers,
				store_requests,
				store_websockets,
				store_websocket_events,
				store_event_source_msgs,
				store_cookies,
				store_security_details,
				timeseries_enabled,
				timeseries_interval
			FROM 
				config
			ORDER BY
				modified DESC
			LIMIT 1
		""")

		# get query result and then do dict formatting to 
		#	be nicer to calling function
		result = self.db.fetchone()
		return {
			'client_browser_type'			: result[0],
			'client_prewait'				: result[1],
			'client_no_event_wait'			: result[2],
			'client_max_wait'				: result[3],
			'client_get_bodies'				: result[4],
			'client_get_bodies_b64'			: result[5],
			'client_get_screen_shot'		: result[6],
			'client_get_text'				: result[7],
			'client_crawl_depth'			: result[8],
			'client_crawl_retries'			: result[9],
			'client_page_load_strategy'		: result[10],
			'client_reject_redirects'		: result[11],
			'client_min_internal_links'		: result[12],
			'max_attempts'					: result[13],
			'store_1p'						: result[14],
			'store_base64'					: result[15],
			'store_files'					: result[16],
			'store_screen_shot'				: result[17],
			'store_source'					: result[18],
			'store_page_text'				: result[19],
			'store_links'					: result[20],
			'store_dom_storage'				: result[21],
			'store_responses'				: result[22],
			'store_request_xtra_headers'	: result[23],
			'store_response_xtra_headers'	: result[24],
			'store_requests'				: result[25],
			'store_websockets'				: result[26],
			'store_websocket_events'		: result[27],
			'store_event_source_msgs'		: result[28],
			'store_cookies'					: result[29],
			'store_security_details'		: result[30],
			'timeseries_enabled'			: result[31],
			'timeseries_interval'			: result[32]
		}
	# get_config

	def build_filtered_query(self,query,filters):
		"""
		takes a base query + filters and returns
		a query with appropraite 'where'/'and' placements
		only needed in cases where query conditionals get particularly ugly
		"""
		if filters:
			for index,filter in enumerate(filters):
				if index == 0:
					query += ' WHERE '+filter
				else:
					query += ' AND '+filter
		return query
	# build_filtered_query

	def get_wbxr_dbs_list(self):
		"""
		return database names with the class-specified prefix, stripped of prefix, default is 'wbxr_'
		"""
		wbxr_dbs = []
		for item in os.listdir(self.db_root_path):
			if item[0:len(self.db_prefix)] == self.db_prefix:
				wbxr_dbs.append(item[len(self.db_prefix):-3])
		return wbxr_dbs
	# get_wbxr_dbs_list

	def close(self):
		"""
		very important, frees up connections to db
		"""

		# it is possible a database is not open, in which case we silently fail
		try:
			self.db.close()
			self.db_conn.close()
		except:
			pass
	# close

	#-------------#
	# DB Creation #
	#-------------#

	def create_wbxr_db(self, db_name):
		"""
		create empty db using the sql init file in /webxray/resources/db/sqlite
		and update the current db
		"""

		# update global db_name
		self.db_name = self.db_prefix+db_name

		# make sure we don't overwrite existing db
		if os.path.isfile(self.db_root_path+self.db_name+'.db'):
			print('****************************************************************************')
			print('ERROR: Database exists, SQLite will overwrite existing databases, aborting! ')
			print('****************************************************************************')
			exit()
		else:
			# create new db here, if it does not exist yet it gets created on the connect
			self.db_conn = sqlite3.connect(self.db_root_path+self.db_name+'.db',detect_types=sqlite3.PARSE_DECLTYPES)
			self.db = self.db_conn.cursor()

			# initialize webxray formatted database
			db_init_file = open(self.db_root_path+'sqlite_db_init.schema', 'r', encoding='utf-8')
			for query in db_init_file:
				# skip lines that are comments
				if "-" in query[0]: continue
				# lose whitespace
				query = query.strip()
				# push to db
				self.db.execute(query)
				self.db_conn.commit()

		# insert domain owners
		domain_owner_data = json.load(open(os.path.dirname(os.path.abspath(__file__))+'/resources/domain_owners/domain_owners.json', 'r', encoding='utf-8'))
		for domain_owner in domain_owner_data:
			# arrays get stored as json strings
			domain_owner['aliases'] 					= json.dumps(domain_owner['aliases'])
			domain_owner['site_privacy_policy_urls'] 	= json.dumps(domain_owner['site_privacy_policy_urls'])
			domain_owner['service_privacy_policy_urls'] = json.dumps(domain_owner['service_privacy_policy_urls'])
			domain_owner['gdpr_statement_urls'] 		= json.dumps(domain_owner['gdpr_statement_urls'])
			domain_owner['terms_of_use_urls'] 			= json.dumps(domain_owner['terms_of_use_urls'])
			domain_owner['platforms'] 					= json.dumps(domain_owner['platforms'])
			domain_owner['uses'] 						= json.dumps(domain_owner['uses'])

			self.add_domain_owner(domain_owner)
	# create_wbxr_db

	#-----------------------#
	# INGESTION AND STORING #
	#-----------------------#	

	def flush_task_queue(self, task=None):
		"""
		When starting a new scan we flush out the queue
			by default.  When running as a slave this
			doesn't get triggered.
		"""
		if task:
			self.db.execute('DELETE FROM task_queue WHERE task = ?', (task,))
		else:
			self.db.execute('DELETE FROM task_queue')
		self.db_conn.commit()
	# flush_task_queue

	def get_page_last_accessed_by_browser_type(self,url,browser_type=None):
		"""
		see when the page was last accessed, if the page is not in the db yet, this will return none
		additionaly you can specifify which browser to check for
		if no browser is specified just return the last time it was accessed
		"""
		if browser_type == None:
			self.db.execute('SELECT accessed,browser_type FROM page WHERE start_url_md5 = ? ORDER BY accessed DESC LIMIT 1', (self.md5_text(url),))
		else:
			self.db.execute('SELECT accessed,browser_type FROM page WHERE start_url_md5 = ? AND browser_type = ? ORDER BY accessed DESC LIMIT 1', (self.md5_text(url),browser_type))

		try:
			return (datetime.datetime.strptime(self.db.fetchone()[0], "%Y-%m-%d %H:%M:%S.%f"), self.db.fetchone()[1])
		except:
			return None
	# get_page_last_accessed_by_browser_type

	def page_exists(self, url, accessed=None, timeseries_interval=None):
		"""
		checks if page exists at all, regardless of number of occurances
		postgres has an EXISTS query built-in, whereas sqlite does not
		"""
		if timeseries_interval:
			self.db.execute("""
				SELECT EXISTS(
					SELECT 
						start_url_md5 
					FROM 
						page 
					WHERE 
						start_url_md5 = ?
					AND
						accessed >= (NOW() - INTERVAL '? MINUTES')
				)
			""", (self.md5_text(url),timeseries_interval))
		elif accessed:
			self.db.execute("""
				SELECT EXISTS(
					SELECT 
						start_url_md5 
					FROM 
						page 
					WHERE 
						start_url_md5 = ?
					AND
						accessed = ?
				)
			""", (self.md5_text(url),accessed))	
		else:
			self.db.execute("""
				SELECT EXISTS(
					SELECT 
						start_url_md5 
					FROM 
						page 
					WHERE 
						start_url_md5 = ?
				)
			""", (self.md5_text(url),))
		return self.db.fetchone()[0]
	# page_exists
	
	def get_all_pages_exist(self, timeseries_interval=None):
		"""
		Get list of all pages that have been scanned, timeseries_interval
			allows to restrict to pages in a certain timeframe.
		"""
		if timeseries_interval:
			self.db.execute("""
				SELECT 
					start_url
				FROM 
					page 
				WHERE 
					accessed >= (NOW() - INTERVAL '? MINUTES')
			""", (timeseries_interval))
		else:
			self.db.execute("""
				SELECT 
					start_url
				FROM 
					page 
			""")
		return self.db.fetchall()
	# get_all_pages_exist

	def add_task_to_queue(self,target,task):
		"""
		We have a queue of tasks which are defined by a url, the task type ('get_scan',
			or 'get_policy'), browser_type ('chrome' or 'basic'), and browser wait (int).
		"""
		self.db.execute("""
				INSERT INTO task_queue (
					target, 
					target_md5,
					task
				) VALUES (
					?,
					?, 
					?
				) 
				ON CONFLICT DO NOTHING
			""", (
					target,
					self.md5_text(target),
					task
				)
		)
		self.db_conn.commit()
	# add_task_to_queue

	def get_task_queue_length(self, task=None, unlocked_only=None, max_attempts = 0):
			"""
			How many pages in the queue.
			"""
			if task and unlocked_only:
					self.db.execute("""
						SELECT COUNT(*) FROM task_queue 
						WHERE locked = FALSE 
						AND attempts < ?
						AND task = ?
						AND failed IS FALSE
					""", (max_attempts,task))
			elif unlocked_only:
					self.db.execute("""
						SELECT COUNT(*) FROM task_queue 
						WHERE locked = FALSE 
						AND attempts < ?
						AND failed IS FALSE
					""", (max_attempts,))
			elif task:
					self.db.execute("""
						SELECT COUNT(*) FROM task_queue 
						WHERE task = ?
						AND failed IS FALSE
					""", (task,))
			else:
					self.db.execute("""
						SELECT COUNT(*) FROM task_queue WHERE failed IS FALSE
					""")
			
			return self.db.fetchone()[0]
	# get_task_queue_length

	def get_task_from_queue(self, max_attempts=None, client_id=None):
		"""
		Return the next task, while updating the attempt count and marking
			which machine has taken the task.  Can filter on attempt number.
		"""

		# kludge to make sure two processes don't try to do the same page
		#	note this is handled better with postgres
		time.sleep(random.randint(50, 100)/100)
		
		if max_attempts:
			self.db.execute("""
				SELECT id, target, task, attempts
					FROM task_queue
					WHERE locked IS NOT TRUE
					AND failed IS NOT TRUE
					AND attempts < ?
					ORDER BY attempts
					LIMIT 1
			""", (max_attempts,))
		else:
			self.db.execute("""
				SELECT id, target, task, attempts
					FROM task_queue
					WHERE locked IS NOT TRUE
					AND failed IS NOT TRUE
					ORDER BY attempts
					LIMIT 1
			""")
		
		# return result or None
		try:
			task_id, target, task, attempts = self.db.fetchone()
			self.lock_task(task_id)
			self.increment_task_attempts(task_id, attempts)
			return target, task
		except:
			return None	
	# get_task_from_queue

	def lock_task(self, task_id):
		self.db.execute("UPDATE task_queue SET locked = TRUE where id = ?", (task_id,))
		self.db_conn.commit()
	# lock_task

	def increment_task_attempts(self, task_id, attempts):
		self.db.execute("UPDATE task_queue SET attempts = ? where id = ?", (attempts+1, task_id))
		self.db_conn.commit()
	# increment_task_attempts

	def remove_task_from_queue(self,target,task):
		"""
		If a task is successfull we remove it from the queue.
		"""
		self.db.execute('DELETE FROM task_queue WHERE target_md5 = ? AND task = ?', (self.md5_text(target),task))
		self.db_conn.commit()
	# remove_task_from_queue

	def unlock_task_in_queue(self,target,task):
		"""
		If a task is not successfull we unlock it so it may be attempted again.
		"""
		self.db.execute('UPDATE task_queue SET locked = FALSE WHERE target_md5 = ? AND task = ?', (self.md5_text(target),task))
		self.db_conn.commit()
	# unlock_task_in_queue

	def unlock_all_tasks_in_queue(self):
		"""
		Removes all locks in queue, used when restarting server.

		"""
		self.db.execute("""
			UPDATE task_queue
			SET locked = FALSE
		""")
	# unlock_all_tasks_in_queue

	def set_task_as_failed(self,target,task):
		"""
		Task will no longer be attempted.
		"""
		self.db.execute('UPDATE task_queue SET failed = true WHERE target_md5 = ? AND task = ?', (self.md5_text(target),task))
		self.db_conn.commit()
	# set_task_as_failed

	def add_result_to_queue(self, result):
		"""
		Stores JSON so we can process it later, used when
			remote clients send us something so we can
			quickly send them a response.
		"""
		self.db.execute("""
			INSERT INTO result_queue (
				client_id,
				client_ip,
				mapped_db,
				target,
				task,
				task_result
			) VALUES (
				?,
				?,
				?,
				?,
				?,
				?
			)""", 
			(
				result['client_id'],
				result['client_ip'],
				result['mapped_db'],
				result['target'],
				result['task'],
				result['task_result']
			)
		)
		self.db_conn.commit()
	# add_result_to_queue

	def get_result_from_queue(self):
		"""
		Retrieves single unprocessed result so it can be stored, note
			it is not removed from db until it has been successfully
			processed.  If we don't have any results left will
			return None.
		"""
		self.db.execute("""
			UPDATE result_queue 
			SET 
				locked = TRUE,
				modified = NOW()
			WHERE id = (
				SELECT id
				FROM result_queue
				WHERE locked IS NOT TRUE
				FOR UPDATE SKIP LOCKED
				LIMIT 1
			)
			RETURNING 
				id,
				client_id,
				client_ip,
				mapped_db,
				target,
				task,
				task_result
		""")

		# return result or None
		try:
			result = self.db.fetchone()
			return ({
				'result_id'		: result[0],
				'client_id'		: result[1],
				'client_ip'		: result[2],
				'mapped_db'		: result[3],
				'target'		: result[4],
				'task'			: result[5],
				'task_result'	: result[6]
			})
		except:
			return None	
	# get_result_from_queue

	def remove_result_from_queue(self, result_id):
		"""
		Once a result is successfully stored we are passed
			the result_id and we delete it.
		"""
		self.db.execute('DELETE FROM result_queue WHERE id = ?', (result_id,))
		self.db_conn.commit()
	# remove_result_from_queue

	def unlock_result_in_queue(self, result_id):
		"""
		If we were unable to store a result we unlock it.
		"""
		self.db.execute('UPDATE result_queue SET locked = FALSE WHERE id = ?', (result_id,))
		self.db_conn.commit()
	# unlock_result_in_queue

	def get_page_last_accessed(self, url):
		"""
		see when the page was last accessed, if the page is not in the db yet, this will return none
		"""
		self.db.execute('SELECT accessed FROM page WHERE start_url_md5 = ? ORDER BY accessed DESC LIMIT 1', (self.md5_text(url),))
		
		try:
			return self.db.fetchone()
		except:
			return None
	# get_page_last_accessed

	def get_page_last_accessed_by_browser_type(self,url,browser_type=None):
		"""
		see when the page was last accessed, if the page is not in the db yet, this will return none
		additionaly you can specifify which browser to check for
		if no browser is specified just return the last time it was accessed
		"""
		if browser_type == None:
			self.db.execute('SELECT accessed,browser_type FROM page WHERE start_url_md5 = ? ORDER BY accessed DESC LIMIT 1', (self.md5_text(url),))
		else:
			self.db.execute('SELECT accessed,browser_type FROM page WHERE start_url_md5 = ? AND browser_type = ? ORDER BY accessed DESC LIMIT 1', (self.md5_text(url),browser_type))

		try:
			return self.db.fetchone()
		except:
			return None
	# get_page_last_accessed_by_browser_type

	def crawl_exists(self, target, timeseries_interval=None):
		"""
		checks if a crawl exists at all, regardless of number of occurances
		postgres has an EXISTS query built-in, whereas sqlite does not
		"""
		if timeseries_interval:
			self.db.execute("""
				SELECT EXISTS(
					SELECT 
						crawl_id 
					FROM 
						page 
					WHERE 
						crawl_id = ?
					AND
						accessed >= (NOW() - INTERVAL '? MINUTES')
				)
			""", (self.md5_text(target),timeseries_interval))
		else:
			self.db.execute("""
				SELECT EXISTS(
					SELECT 
						crawl_id 
					FROM 
						page 
					WHERE 
						crawl_id = ?
				)
			""", (self.md5_text(target),))
		return self.db.fetchone()[0]
	# crawl_exists

	def add_domain(self, domain):
		"""
		add a new domain record to db, ignores duplicates
		returns id of specified domain
		"""
		self.db.execute("""
			INSERT INTO domain (
				fqdn_md5, 
				fqdn,
				domain_md5, 
				domain, 
				pubsuffix_md5, 
				pubsuffix, 
				tld_md5, 
				tld,
				domain_owner_id
			) VALUES (
				?,
				?,
				?,
				?,
				?,
				?, 
				?,
				?,
				?
			) ON CONFLICT DO NOTHING""", 
			(
				self.md5_text(domain['fqdn']),
				domain['fqdn'], 
				self.md5_text(domain['domain']), 
				domain['domain'], 
				self.md5_text(domain['pubsuffix']), 
				domain['pubsuffix'], 
				self.md5_text(domain['tld']),
				domain['tld'], 
				domain['domain_owner_id']
			)
		)
		self.db_conn.commit()
		self.db.execute("SELECT id FROM domain WHERE fqdn_md5 = ?", (self.md5_text(domain['fqdn']),))
		return self.db.fetchone()[0]
	# add_domain

	def add_domain_ip_addr(self, domain_id, ip_addr):
		self.db.execute("INSERT INTO domain_ip_addr (domain_id,ip_addr) VALUES (?,?) ON CONFLICT DO NOTHING", (domain_id, ip_addr))
		self.db_conn.commit()
	# add_domain_ip_addr

	def add_page(self, page):
		"""
		page is unique on 'accessed' and 'start_url_md5', in the unlikely event of a collision this will fail
		ungracefully, which is desired as the bug would be major

		returns id of newly added page
		"""
		self.db.execute("""INSERT INTO page (
				browser_type, 
				browser_version, 
				browser_prewait,
				browser_no_event_wait,
				browser_max_wait,
				page_load_strategy,
				title, 
				meta_desc, 
				lang, 
				start_url_md5, 
				start_url, 
				start_url_domain_id,
				final_url_md5, 
				final_url, 
				final_url_domain_id,
				is_ssl, 
				page_domain_redirect, 
				link_count_internal, 
				link_count_external,
				load_time,
				client_id,
				client_timezone,
				client_ip,
				page_text_id,
				screen_shot_md5,
				page_source_md5,
				crawl_id,
				crawl_timestamp,
				crawl_sequence,
				accessed
		) VALUES (
				?, 
				?, 
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?, 
				?, 
				?,
				?, 
				?, 
				?,
				?, 
				?,
				?, 
				?, 
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?
		)""",(
			page['browser_type'], 
			page['browser_version'], 
			page['browser_prewait'],
			page['browser_no_event_wait'],
			page['browser_max_wait'],
			page['page_load_strategy'],
			page['title'], 
			page['meta_desc'], 
			page['lang'], 
			self.md5_text(page['start_url']), 
			page['start_url'], 
			page['start_url_domain_id'],
			self.md5_text(page['final_url']), 
			page['final_url'], 
			page['final_url_domain_id'],
			page['is_ssl'], 
			page['page_domain_redirect'], 
			page['link_count_internal'], 
			page['link_count_external'],
			page['load_time'], 
			page['client_id'],
			page['client_timezone'],
			page['client_ip'],
			page['page_text_id'],
			page['screen_shot_md5'],
			page['page_source_md5'],
			self.md5_text(page['crawl_id']),
			page['crawl_timestamp'],
			page['crawl_sequence'],
			page['accessed']
		))
		
		# returns id of row we just entered
		return self.db.lastrowid
	# add_page

	def add_dom_storage(self, dom_storage):
		"""
		stores a dom_storage item, should fail ungracefully if the page_id or domain_id does not exist

		returns nothing
		"""
		self.db.execute("""
			INSERT INTO dom_storage (
				page_id,
				domain_id,
				security_origin,
				is_local_storage,
				key,
				value,
				is_3p
			) VALUES (
				?,
				?,
				?,
				?,
				?,
				?,
				?
			)""",
			(	
				dom_storage['page_id'],
				dom_storage['domain_id'],
				dom_storage['security_origin'],
				dom_storage['is_local_storage'],
				dom_storage['key'],
				dom_storage['value'],
				dom_storage['is_3p']
			)
		)
		self.db_conn.commit()
	# add_dom_storage

	def add_cookie(self, cookie):
		"""
		stores a cookie, should fail ungracefully if the page_id or domain_id does not exist

		returns nothing
		"""
		self.db.execute("""
			INSERT INTO cookie (
				page_id,
				domain_id,
				domain,
				expires_text,
				expires_timestamp,
				http_only,
				is_3p,
				name,
				path,
				same_site,
				secure,
				session,
				size,
				value,
				is_set_by_response
			) VALUES (
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?
			)""",
			(
				cookie['page_id'],
				cookie['domain_id'],
				cookie['domain'],
				cookie['expires'],
				cookie['expires_timestamp'],
				cookie['http_only'],
				cookie['is_3p'],
				cookie['name'],
				cookie['path'],
				cookie['same_site'],
				cookie['secure'],
				cookie['session'],
				cookie['size'],
				cookie['value'],
				cookie['is_set_by_response']
			)
		)
		self.db_conn.commit()
	# add_cookie

	def add_link(self, link):
		"""
		Stores a link in link table and attaches to page_id
			in the page_link_junction table.  Links are unique on
			url_md5+text_md5.  Note this means the url may show up
			more than once with different text.
		"""

		# first add the link and get the id
		self.db.execute("""
			INSERT INTO link (
				url, 
				url_md5,
				text, 
				text_md5,
				is_internal,
				is_policy,
				domain_id
			) VALUES (
				?,
				?,
				?,
				?,
				?,
				?,
				?
			) 
			ON CONFLICT DO NOTHING
			""",
			(	
				link['url'], 
				self.md5_text(link['url']),
				link['text'], 
				self.md5_text(link['text']),
				link['is_internal'], 
				link['is_policy'],
				link['domain_id']
			)
		)
		self.db_conn.commit()

		self.db.execute("SELECT id FROM link WHERE url_md5 = ? and text_md5 = ?", (self.md5_text(link['url']),self.md5_text(link['text'])))
		return self.db.fetchone()[0]
	# add_link

	def join_link_to_page(self,page_id,link_id):
		"""
		creates record in junction table
		"""

		# create
		self.db.execute("""
			INSERT INTO page_link_junction(
				page_id, 
				link_id
			) VALUES (
				?,
				?
			) ON CONFLICT DO NOTHING""", 
			(
				page_id, 
				link_id
			)
		)
		self.db_conn.commit()
	# join_link_to_page

	def add_file(self, file):
		"""
		Store file contents as TEXT
		"""
		self.db.execute("""
			INSERT INTO file (
				md5,
				body,
				type,
				is_base64
			) VALUES (
				?,
				?,
				?,
				?
			) ON CONFLICT DO NOTHING""", 
			(
				file['md5'],
				file['body'],
				file['type'],
				file['is_base64']
			)
		)
		self.db_conn.commit()
	# add_file

	def add_security_details(self, security_details):
		"""
		add a new security_detail record to db
		unique on a hash of the string containing all record details
		returns id of recording matching unique hash
		"""

		# concat all details into single string to speed
		#	up queries
		lookup_string = str(security_details)

		# store record, ignore if duplicate
		self.db.execute("""
			INSERT INTO security_details (
				lookup_md5,
				cert_transparency_compliance,
				cipher,
				issuer,
				key_exchange,
				protocol,
				san_list,
				signed_cert_timestamp_list,
				subject_name,
				valid_from,
				valid_to
			) VALUES (
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?
			) ON CONFLICT DO NOTHING""", 
			(
				self.md5_text(lookup_string),
				security_details['certificateTransparencyCompliance'],
				security_details['cipher'],
				security_details['issuer'],
				security_details['keyExchange'],
				security_details['protocol'],
				json.dumps(security_details['sanList']),
				json.dumps(security_details['signedCertificateTimestampList']),
				security_details['subjectName'],
				security_details['validFrom'],
				security_details['validTo']
			)
		)
		self.db_conn.commit()

		# return id of matching record
		self.db.execute("""
			SELECT id 
			FROM security_details 
			WHERE lookup_md5 = ?
		""", (self.md5_text(lookup_string),))
		return self.db.fetchone()[0]
	# add_security_details

	def add_request(self, request):
		"""
		Stores request which is passed as a dict
		"""
		
		self.db.execute("""
			INSERT INTO request (
				page_id,
				domain_id,
				full_url, 
				full_url_md5,
				base_url, 
				base_url_md5,
				internal_request_id, 
				document_url,
				extension, 
				file_md5,
				has_user_gesture,
				headers, 
				initial_priority,
				initiator, 
				is_3p,
				is_data,
				is_link_preload, 
				is_ssl,
				loader_id, 
				method,
				page_domain_in_headers,
				post_data, 
				get_data, 
				load_finished,
				redirect_response_url,
				referer, 
				referrer_policy,
				response_received,
				timestamp, 
				type
			) VALUES (
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?
			)
			""", 
			(
				request['page_id'],
				request['domain_id'],
				request['url'],
				self.md5_text(request['url']),
				request['base_url'],
				self.md5_text(request['base_url']),
				request['request_id'],
				request['document_url'],
				request['extension'],
				request['file_md5'],
				request['has_user_gesture'],
				json.dumps(request['headers']),
				request['initial_priority'],
				json.dumps(request['initiator']),
				request['is_3p'],
				request['is_data'],
				request['is_link_preload'],
				request['is_ssl'],
				request['loader_id'],
				request['method'],
				request['page_domain_in_headers'],
				request['post_data'],
				request['get_data'],
				request['load_finished'],
				request['redirect_response_url'],
				request['referer'],
				request['referrer_policy'],
				request['response_received'],
				request['timestamp'],
				request['type']
			)
		)
		self.db_conn.commit()
	# add_request

	def add_response(self, response):
		"""
		Stores response which is passed as a dict
		"""

		self.db.execute("""
			INSERT INTO response (
				base_url,
				base_url_md5,
				extension,
				internal_request_id,
				connection_reused,
				cookies_sent,
				cookies_set,
				domain_id,
				security_details_id,
				file_md5,
				final_data_length,
				from_disk_cache,
				from_prefetch_cache,
				from_service_worker,
				is_3p,
				is_data,
				is_ssl,
				mime_type,
				page_id,
				page_domain_in_headers,
				protocol,
				referer,
				remote_ip_address,
				remote_port,
				request_headers,
				response_headers,
				security_state,
				status,
				status_text,
				timestamp,
				timing,
				type,
				url
			) VALUES (
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?
			)
			""", 
			(
				response['base_url'],
				self.md5_text(response['base_url']),
				response['extension'],
				response['request_id'],
				response['connection_reused'],
				response['cookies_sent'],
				response['cookies_set'],
				response['domain_id'],
				response['security_details_id'],
				response['file_md5'],
				response['final_data_length'],
				response['from_disk_cache'],
				response['from_prefetch_cache'],
				response['from_service_worker'],
				response['is_3p'],
				response['is_data'],
				response['is_ssl'],
				response['mime_type'],
				response['page_id'],
				response['page_domain_in_headers'],
				response['protocol'],
				response['referer'],
				response['remote_ip_address'],
				response['remote_port'],
				json.dumps(response['request_headers']),
				json.dumps(response['response_headers']),
				response['security_state'],
				response['status'],
				response['status_text'],
				response['timestamp'],
				json.dumps(response['timing']),
				response['type'],
				response['url']
			)
		)

		# returns id of row we just entered
		return self.db.lastrowid
	# add_response

	def add_response_extra_header(self,response_extra_header):
		"""
		Stores response_extra_headers which is passed as a dict
		"""

		self.db.execute("""
			INSERT INTO response_extra_headers (
				page_id,
				internal_request_id,
				cookies_set,
				headers,
				blocked_cookies
			) VALUES (
				?,
				?,
				?,
				?,
				?
			)
			""", 
			(
				response_extra_header['page_id'],
				response_extra_header['request_id'],
				response_extra_header['cookies_set'],
				json.dumps(response_extra_header['headers']),
				json.dumps(response_extra_header['blocked_cookies'])
			)
		)
		self.db_conn.commit()
	# add_extra_response_header

	def add_request_extra_header(self,request_extra_header):
		"""
		Stores request_extra_headers which is passed as a dict
		"""

		self.db.execute("""
			INSERT INTO request_extra_headers (
				page_id,
				internal_request_id,
				cookies_sent,
				headers,
				associated_cookies
			) VALUES (
				?,
				?,
				?,
				?,
				?
			)
			""", 
			(
				request_extra_header['page_id'],
				request_extra_header['request_id'],
				request_extra_header['cookies_sent'],
				json.dumps(request_extra_header['headers']),
				json.dumps(request_extra_header['associated_cookies'])
			)
		)
		self.db_conn.commit()
	# add_extra_request_header

	def add_websocket(self, websocket):
		"""
		Stores websocket which is passed as a dict
		"""
		self.db.execute("""
			INSERT INTO websocket (
				page_id,
				domain_id,
				initiator,
				is_3p,
				url
			) VALUES (
				?,
				?,
				?,
				?,
				?
			)
			""", 
			(
				websocket['page_id'],
				websocket['domain_id'],
				json.dumps(websocket['initiator']),
				websocket['is_3p'],
				websocket['url']
			)
		)

		# returns id of row we just entered
		return self.db.lastrowid
	# add_websocket

	def add_websocket_event(self, websocket_event):
		"""
		Stores websocket which is passed as a dict
		"""

		self.db.execute("""
			INSERT INTO websocket_event (
				page_id,
				websocket_id,
				timestamp,
				event_type,
				payload
			) VALUES (
				?,
				?,
				?,
				?,
				?
			)
			""", 
			(
				websocket_event['page_id'],
				websocket_event['websocket_id'],
				websocket_event['timestamp'],
				websocket_event['event_type'],
				json.dumps(websocket_event['payload'])
			)
		)
		self.db_conn.commit()
	# add_websocket

	def add_event_source_msg(self,event_source_msg):
		"""
		Stores event_source_msg which is passed as a dict
		"""

		self.db.execute("""
			INSERT INTO event_source_msg (
				page_id,
				internal_request_id,
				event_name,
				event_id,
				data,
				timestamp
			) VALUES (
				?,
				?,
				?,
				?,
				?,
				?
			)
			""", 
			(
				event_source_msg['page_id'],
				event_source_msg['internal_request_id'],
				event_source_msg['event_name'],
				event_source_msg['event_id'],
				event_source_msg['data'],
				event_source_msg['timestamp']
			)
		)
		self.db_conn.commit()
	# add_event_source_msg

	def add_page_text(self, page_text):
		"""
		Store text here, can be for a normal page or a policy.
		"""
		self.db.execute("""
			INSERT INTO page_text (
				text,
				tokens,
				text_md5,
				word_count,
				readability_source_md5
			) VALUES (
				?,
				?,
				?,
				?,
				?
			) ON CONFLICT DO NOTHING""",
			(
				page_text['text'],
				None,
				self.md5_text(page_text['text']),
				page_text['word_count'],
				page_text['readability_source_md5']
			)
		)

		# return id of record with this readability_source_md5 and text_md5
		self.db.execute("SELECT id FROM page_text WHERE text_md5 = ?", (self.md5_text(page_text['text']),))
	
		return self.db.fetchone()[0]
	# add_page_text

	def log_error(self, error):
		"""
		general purpose error logging, unique on url/msg
		"""
		self.db.execute("""
			INSERT INTO error (
				client_id, 
				task,
				target, 
				msg
			) VALUES (
				?,
				?,
				?,
				?
			)""", 
			(
				error['client_id'], 
				error['task'],
				error['target'],
				error['msg']
			)
		)
		self.db_conn.commit()
	# log_error

	def add_page_id_domain_lookup_item(self,lookup_item):
		"""
		When a page is ingested we patch this lookup table
			as well.
		"""

		self.db.execute("""
			INSERT INTO page_id_domain_lookup (
				page_id,
				domain,
				domain_owner_id,
				is_request,
				is_response,
				is_cookie,
				is_websocket,
				is_domstorage
			) VALUES (
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?
			)""", 
			(
				lookup_item['page_id'],
				lookup_item['domain'],
				lookup_item['domain_owner_id'],
				lookup_item['is_request'],
				lookup_item['is_response'],
				lookup_item['is_cookie'],
				lookup_item['is_websocket'],
				lookup_item['is_domstorage']
			)
		)
		self.db_conn.commit()
	# add_page_id_domain_lookup_item

	def add_crawl_id_domain_lookup_item(self,lookup_item):
		"""
		When a crawl is ingested we patch this lookup table
			as well.
		"""

		self.db.execute("""
			INSERT INTO crawl_id_domain_lookup (
				crawl_id,
				domain,
				domain_owner_id,
				is_request,
				is_response,
				is_cookie,
				is_websocket,
				is_domstorage
			) VALUES (
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?
			)""", 
			(
				self.md5_text(lookup_item['crawl_id']),
				lookup_item['domain'],
				lookup_item['domain_owner_id'],
				lookup_item['is_request'],
				lookup_item['is_response'],
				lookup_item['is_cookie'],
				lookup_item['is_websocket'],
				lookup_item['is_domstorage']
			)
		)
		self.db_conn.commit()
	# add_crawl_id_domain_lookup_item

	def clear_clusters(self):
		"""
		Deletes all cluster data.
		"""
		self.db.execute('DELETE FROM cluster')
		self.db.execute('DELETE FROM page_cluster_junction')
	# clear_clusters

	def add_cluster(self,cluster):
		"""
		Create new cluster entry.
		"""
		self.db.execute("""
			INSERT INTO cluster (
				type, 
				name,
				data
			) VALUES (
				?,
				?,
				?
			)
			""", 
			(
				cluster['type'], 
				cluster['name'],
				json.dumps(cluster['data'])
			)
		)

		# returns id of row we just entered
		return self.db.lastrowid
	# add_cluster

	def assign_cluster(self,page_id,cluster_id):
		"""
		Assigns a page to a cluster via a junction table.
		"""
		self.db.execute("""
			INSERT INTO page_cluster_junction (
				page_id, 
				cluster_id
			) VALUES (
				?,
				?
			)""", 
			(
				page_id,
				cluster_id
			)
		)
		self.db_conn.commit()
	# assign_cluster

	#------------------------#
	# ANALYSIS AND REPORTING #
	#------------------------#	

	# the first step for analysis is to assign owners to domains so we can track
	# corporate ownership structures; the next few functions update the database to do this after
	# the collection has been done
	
	def reset_domain_owners(self):
		"""
		when the domain ownership is updated it is neccessary to flush existing mappings
		by first resetting all the domain owner records then clear the domain_owner db
		"""
		self.db.execute('DELETE FROM policy_request_disclosure')
		self.db.execute('UPDATE domain SET domain_owner_id = NULL')
		self.db.execute('UPDATE crawl_id_domain_lookup SET domain_owner_id = NULL')
		self.db.execute('UPDATE page_id_domain_lookup SET domain_owner_id = NULL')
		self.db.execute('DELETE FROM domain_owner')
		return True
	# reset_domain_owners

	def add_domain_owner(self, domain_owner):
		"""
		create entries for the domain owners we are analyzing
		"""
		self.db.execute("""
			INSERT INTO domain_owner (
				id, 
				parent_id, 
				name,
				aliases, 
				homepage_url,
				site_privacy_policy_urls,
				service_privacy_policy_urls,
				gdpr_statement_urls,
				terms_of_use_urls,
				platforms,
				uses,
				notes,
				country
			) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", 
			(	
				domain_owner['id'],
				domain_owner['parent_id'], 
				domain_owner['name'],
				domain_owner['aliases'], 
				domain_owner['homepage_url'],
				domain_owner['site_privacy_policy_urls'],
				domain_owner['service_privacy_policy_urls'],
				domain_owner['gdpr_statement_urls'],
				domain_owner['terms_of_use_urls'],
				domain_owner['platforms'],
				domain_owner['uses'],
				domain_owner['notes'],
				domain_owner['country']
			)
		)
		self.db_conn.commit()
	# add_domain_owner

	def update_domain_owner(self, id, domain):
		"""
		link the domains to the owners
		"""
		self.db.execute('UPDATE domain SET domain_owner_id = ? WHERE domain_md5 = ?', (id, self.md5_text(domain)))
		self.db.execute('UPDATE crawl_id_domain_lookup SET domain_owner_id = ? WHERE domain = ?', (id, domain))
		self.db.execute('UPDATE page_id_domain_lookup SET domain_owner_id = ? WHERE domain = ?', (id, domain))
		self.db_conn.commit()
		return True
	# update_domain_owner

	def get_all_domain_owner_data(self):
		"""
		returns everything from the domain_owner table
		which is relatively small and can be a global 
		var elsewhere

		in cases where the user does not wish the update the domain owners
		with a fresh copy of the domain_owners.json file this will
		provide the same mappings as were used originally and is important
		for historical reporting
		"""
		self.db.execute("""
			SELECT 
				id, parent_id, name,
				aliases, homepage_url,
				site_privacy_policy_urls,
				service_privacy_policy_urls,
				gdpr_statement_urls,
				terms_of_use_urls,
				platforms,
				uses,
				notes,
				country
			FROM
				domain_owner
			""")
		return self.db.fetchall()
	# get_all_domain_owner_data

	def get_domain_owner_ids(self):
		"""
		Return each domain that has an owner_id.
		"""
		self.db.execute("""
			SELECT
				domain,
				domain_owner_id
			FROM
				domain
			WHERE
				domain_owner_id IS NOT NULL
		""")
		return self.db.fetchall()
	# get_domain_owner_ids

	def get_all_tlds(self, type='tld'):
		"""
		Get all tlds from page domains, type can be 'tld' or 'pubsuffix', will crash on invalid type
		"""
		if type == 'tld':
			query = 'SELECT domain.tld from page LEFT JOIN domain ON page.final_url_domain_id = domain.id'
		elif type == 'pubsuffix':
			query = 'SELECT domain.pubsuffix from page LEFT JOIN domain ON page.final_url_domain_id = domain.id'
		
		self.db.execute(query)
		return self.db.fetchall()
	# get_all_tlds

	def get_simple_page_count(self, is_ssl=None, client_id=None):
		"""
		Simple way to query number of pages in db, can filter on ssl and
			client_id.
		"""
		if is_ssl and client_id:
			self.db.execute('SELECT COUNT(*) FROM page WHERE is_ssl = TRUE AND client_id = ?', (client_id,))
		elif is_ssl:
			self.db.execute('SELECT COUNT(*) FROM page WHERE is_ssl = TRUE')
		elif client_id:
			self.db.execute('SELECT COUNT(*) FROM page WHERE client_id = ?', (client_id,))
		else:
			self.db.execute('SELECT COUNT(*) FROM page')
		return self.db.fetchone()[0]
	# get_pages_ok_count

	def get_recent_page_count(self,interval_seconds,client_id=None):
		"""
		Return the number of pages added to db in the past seconds.
		"""
		if client_id:
			self.db.execute("SELECT COUNT(*) FROM page WHERE stored >= (NOW() - INTERVAL '? seconds') AND client_id = ?", (interval_seconds,client_id))
		else:
			self.db.execute("SELECT COUNT(*) FROM page WHERE stored >= (NOW() - INTERVAL '? seconds')", (interval_seconds,))
		return self.db.fetchone()[0]
	# get_recent_page_count

	def get_recent_page_count_by_client_id(self,interval_seconds):
		"""
		Return the number of pages added to db in the past seconds.
		"""
		self.db.execute("SELECT client_id,count(*) FROM page WHERE stored >= (NOW() - INTERVAL '? seconds') group by client_id", (interval_seconds,))
		return self.db.fetchall()
	# get_recent_page_count_by_client_id

	def get_recent_policy_count(self,interval_seconds,client_id=None):
		"""
		Return the number of pages added to db in the past seconds.
		"""
		if client_id:
			self.db.execute("SELECT COUNT(*) FROM policy WHERE added >= (NOW() - INTERVAL '? seconds') AND client_id = ?", (interval_seconds,client_id))
		else:
			self.db.execute("SELECT COUNT(*) FROM policy WHERE added >= (NOW() - INTERVAL '? seconds')", (interval_seconds,))
		return self.db.fetchone()[0]
	# get_recent_page_count

	def get_recent_policy_count_by_client_id(self,interval_seconds):
		"""
		Return the number of pages added to db in the past seconds.
		"""
		self.db.execute("SELECT client_id, count(*) FROM policy WHERE added >= (NOW() - INTERVAL '? seconds') group by client_id", (interval_seconds,))
		return self.db.fetchall()
	# get_recent_policy_count_by_client_id

	def get_policy_count_by_type(self):
		"""
		Return number of policies for each type.
		"""
		self.db.execute("""
			SELECT
				COUNT(*) AS C,
				TYPE
			FROM
				POLICY
			GROUP BY
				TYPE
			ORDER BY
				C
		""")
		return self.db.fetchall()
	# get_policy_count_by_type

	def get_pages_load_times(self):
		"""
		returns a list of all the load times of each page, data is miliseconds in integer form
		"""
		load_times = []
		self.db.execute('SELECT load_time FROM page')
		for item in self.db.fetchall():
			load_times.append(item[0])
		return load_times
	# get_pages_load_times

	def get_page_ave_load_time(self):
		"""
		Average page load time in seconds.
		"""
		self.db.execute('SELECT AVG(load_time) FROM page')
		return self.db.fetchone()[0]
	# get_page_ave_load_time

	def get_pending_task_count(self):
		"""
		see what is still in the queue
		"""
		self.db.execute("SELECT COUNT(*) FROM task_queue where failed = false")
		return self.db.fetchone()[0]
	# get_pending_task_count

	def get_total_errors_count(self):
		"""
		simple way to see how many errors encounted, can be anything logged
		"""
		self.db.execute('SELECT COUNT(*) FROM error')
		return self.db.fetchone()[0]
	# get_total_errors_count

	def get_total_cookie_count(self, is_3p = False):
		"""
		total cookies in the db, can be filtered on 3p only
		"""
		if is_3p:
			self.db.execute('SELECT COUNT(*) FROM cookie WHERE is_3p = True')
		else:
			self.db.execute('SELECT COUNT(*) FROM cookie')
		return self.db.fetchone()[0]
	# get_total_cookie_count

	def get_total_request_count(self, received = False, party = None, is_ssl = None):
		"""
		count of total requests in db, can be filtered by party (first or third)
		as well as if the element was successfully received after the request was made
		
		by default returns all
		"""

		# base query
		query = 'SELECT COUNT(*) FROM request'

		# add filters
		filters = []

		if received:
			filters.append('response_received = TRUE')

		if party == 'third':
			filters.append('is_3p = TRUE')
		if party == 'first':
			filters.append('is_3p = FALSE')

		if is_ssl:
			filters.append('is_ssl = TRUE')

		# execute and return
		self.db.execute(self.build_filtered_query(query,filters))
		return self.db.fetchone()[0]
	# get_total_request_count

	def get_total_response_count(self, is_3p = None, is_ssl = None):
		"""
		count of total requests in db, can be filtered by party (first or third)
		as well as if the element was successfully received after the request was made
		
		by default returns all
		"""

		# base query
		query = 'SELECT COUNT(*) FROM response'

		# add filters
		filters = []

		if is_3p:
			filters.append('is_3p = TRUE')

		if is_ssl:
			filters.append('is_ssl = TRUE')

		# execute and return
		self.db.execute(self.build_filtered_query(query,filters))
		return self.db.fetchone()[0]
	# get_total_response_count

	def get_response_sizes(self):
		"""
		return tuple of (request_domain, size, is_3p (boolean), domain_owner_id)
		"""
		self.db.execute("""
			SELECT response_domain.domain,response.final_data_length,response.is_3p,response_domain.domain_owner_id
			FROM response 
			JOIN domain response_domain on response_domain.id = response.domain_id
			WHERE response.final_data_length IS NOT NULL
		""")
		return self.db.fetchall()
	# get_request_sizes
	
	def get_page_w_3p_req_count(self):
		"""
		Gets number of pages w/a 3p request
		"""
		self.db.execute("""
			SELECT COUNT(DISTINCT page_id)
			FROM request
			WHERE is_3p IS TRUE
		""")
		return self.db.fetchone()[0]
	# get_page_w_3p_req_count

	def get_crawl_w_3p_req_count(self):
		"""
		Gets number of pages w/a 3p request
		"""
		self.db.execute("""
			SELECT COUNT(DISTINCT crawl_id)
			FROM page
			JOIN request ON request.page_id = page.id
			WHERE request.is_3p IS TRUE
		""")
		return self.db.fetchone()[0]
	# get_crawl_w_3p_req_count

	def get_page_w_3p_script_count(self):
		"""
		Gets numbers of pages with a 3p script response
		"""
		self.db.execute("""
			SELECT COUNT(DISTINCT page_id)
			FROM request
			WHERE is_3p IS TRUE
			AND type = 'script'
		""")
		return self.db.fetchone()[0]
	# get_page_w_3p_script_count

	def get_crawl_w_3p_script_count(self):
		"""
		Gets numbers of pages with a 3p script response
		"""
		self.db.execute("""
			SELECT COUNT(DISTINCT crawl_id)
			FROM page
			JOIN request ON request.page_id = page.id
			WHERE request.is_3p IS TRUE
			AND type = 'script'
		""")
		return self.db.fetchone()[0]
	# get_crawl_w_3p_script_count

	def get_page_w_3p_cookie_count(self):
		"""
		Gets numbers of pages with a 3p cookie
		"""
		self.db.execute("""
			SELECT COUNT(DISTINCT page_id)
			FROM cookie
			WHERE is_3p IS TRUE
		""")
		return self.db.fetchone()[0]
	# get_page_w_3p_cookie_count

	def get_crawl_w_3p_cookie_count(self):
		"""
		Gets numbers of pages with a 3p cookie
		"""
		self.db.execute("""
			SELECT COUNT(DISTINCT crawl_id)
			FROM page
			JOIN cookie ON cookie.page_id = page.id
			WHERE cookie.is_3p IS TRUE
		""")
		return self.db.fetchone()[0]
	# get_crawl_w_3p_cookie_count

	def get_ssl_page_count(self):
		"""
		Get number of pages where final_url is https

		"""
		self.db.execute("""
			SELECT COUNT(*)
			FROM page
			WHERE is_ssl IS TRUE
		""")
		return self.db.fetchone()[0]
	# get_ssl_page_count

	def get_crawl_count(self):
		"""
		Number of distinct crawls, regardless of pages.
		"""
		self.db.execute("""
			SELECT COUNT(DISTINCT crawl_id)
			FROM page
		""")
		return self.db.fetchone()[0]
	# get_crawl_count

	def get_complex_page_count(self, tld_filter = None, type = None, is_ssl = False):
		"""
		given various types of analyses we may want to count how many pages meet
			certain criteria, this function handles creating complex sql queries
		
		note that in order to avoid counting the same item more than
			once for a given page we need to use a distinct query against page_id 
		
		while it is better to have logic in elsewhere, some logic has to be here
			as building the queries this way is specific to different sql flavors
		"""

		# holder for filters
		filters = []

		# set up base query, build filter list
		if type == 'requests' or type =='script':
			query = '''SELECT COUNT(DISTINCT page_id) FROM request
				JOIN page ON page.id = request.page_id
				JOIN domain page_domain ON page_domain.id = page.final_url_domain_id
				JOIN domain request_domain ON request_domain.id = request.domain_id'''
			filters.append('request.is_3p = True')
		elif type == 'cookies':
			query = '''SELECT COUNT(DISTINCT cookie.page_id) FROM cookie
				JOIN page ON page.id = cookie.page_id
				JOIN domain page_domain ON page_domain.id = page.final_url_domain_id
				JOIN domain cookie_domain ON cookie_domain.id = cookie.domain_id'''
			filters.append('cookie.is_3p = True')
		else:
			query = '''
				SELECT COUNT(*) FROM page 
				JOIN domain page_domain ON page_domain.id = page.final_url_domain_id
			'''

		# addtional filtering
		if type == 'script': filters.append("request.type = 'script'")
		if tld_filter: filters.append("page_domain.tld = '?'" % tld_filter)
		if is_ssl: filters.append("page.is_ssl = TRUE")

		self.db.execute(self.build_filtered_query(query,filters))
		return self.db.fetchone()[0]
	# get_complex_page_count

	def get_page_ids(self, tld_filter=None):
		"""
		basic utility function, allows to filter on page tld
		"""
		if tld_filter:
			self.db.execute('SELECT page.id FROM page JOIN domain ON page.final_url_domain_id = domain.id WHERE domain.tld = ?', (tld_filter,))
		else:
			self.db.execute('SELECT page.id FROM page')
		return self.db.fetchall()
	# get_page_ids

	def get_all_page_id_3p_domain_owner_ids(self,tld_filter=None):
		"""
		return mapping of all page to third-party request owner ids
		ignores domains where owners are not known
		"""
		if tld_filter:
			self.db.execute("""
				SELECT DISTINCT page.id, request_domain.domain_owner_id from page
				JOIN request ON request.page_id = page.id
				JOIN domain request_domain ON request.domain_id = request_domain.id
				JOIN domain page_domain ON page.final_url_domain_id = page_domain.id
				WHERE request.is_3p = TRUE
				AND request_domain.domain_owner_id IS NOT NULL
				AND page_domain.tld = ?
			""", (tld_filter,))
		else:
			self.db.execute("""
				SELECT DISTINCT page.id, request_domain.domain_owner_id from page
				JOIN request ON request.page_id = page.id
				JOIN domain request_domain ON request.domain_id = request_domain.id
				WHERE request.is_3p = TRUE
				AND request_domain.domain_owner_id IS NOT NULL
			""")

		return self.db.fetchall()
	# get_page_3p_domain_ids

	def get_all_pages_3p_domains_and_owners(self):
		"""
		get a full report for each page of distinct domains requested along with owner id
		owner id can then be used to find parent owners/etc
		also includes elements where domain owner is not known
		"""
		self.db.execute("""
			SELECT DISTINCT page.start_url,page.final_url,page.accessed,request_domain.fqdn,request_domain.domain_owner_id from page
			JOIN request ON request.page_id = page.id
			JOIN domain request_domain ON request.domain_id = request_domain.id
			WHERE request.is_3p = TRUE
			ORDER BY page.final_url, page.accessed, request_domain.domain_owner_id
		""")
		return self.db.fetchall()
	# get_all_pages_3p_domains_and_owners

	def get_all_pages_3p_cookies_and_owners(self):
		"""
		get a full report for each page of distinct cookies requested along with owner id
		owner id can then be used to find parent owners/etc
		also includes cookies where domain owner is not known
		"""

		self.db.execute("""
			SELECT DISTINCT page.start_url,page.final_url,page.accessed,cookie.name,cookie.secure,cookie.expiry,cookie_domain.fqdn,cookie_domain.domain_owner_id from page
			JOIN cookie ON cookie.page_id = page.id
			JOIN domain cookie_domain ON cookie.domain_id = cookie_domain.id
			WHERE cookie.is_3p = TRUE
			ORDER BY page.final_url, page.accessed, cookie_domain.domain_owner_id
		""")
		return self.db.fetchall()
	# get_all_pages_3p_cookies_and_owners

	def get_3p_domain_owners(self, tld_filter = None):
		"""
		get all occurances of element domains and their owners for domain report

		note that in order to avoid counting the same item more than
			once for a given page we need to use a distinct query against page_id 
			this field is subsequently ignored by the calling function
		"""
		query = """
			SELECT DISTINCT page.id, request_domain.domain, request_domain.domain_owner_id FROM page 
			LEFT JOIN request ON request.page_id = page.id
			LEFT JOIN domain request_domain ON request_domain.id = request.domain_id
			LEFT JOIN domain page_domain ON page_domain.id = page.final_url_domain_id
			WHERE request.is_3p = True
		"""

		if tld_filter:
			self.db.execute(query + ' AND page_domain.tld = ?', (tld_filter,))
		else:
			self.db.execute(query)
		return self.db.fetchall()
	# get_3p_domain_owners

	def get_3p_requests(self, tld_filter = None, request_type = None):
		"""
		find the most frequently occuring 3p elements
		according to different criteria
		"""

		base_query = """	
				SELECT DISTINCT 
					page.crawl_id, request.base_url, request.type, 
					request_domain.domain, domain_owner.id
				FROM page 
				LEFT JOIN request ON request.page_id = page.id
				LEFT JOIN domain page_domain ON page.final_url_domain_id = page_domain.id
				LEFT JOIN domain request_domain ON request_domain.id = request.domain_id
				LEFT JOIN domain_owner on domain_owner.id = request_domain.domain_owner_id
				WHERE request.is_3p = TRUE
		"""

		if tld_filter and request_type:
			self.db.execute(base_query + ' AND page_domain.tld = ? AND request.type = ?', (tld_filter, request_type))
		elif tld_filter:
			self.db.execute(base_query + ' AND page_domain.tld = ?', (tld_filter,))
		elif request_type:
			self.db.execute(base_query + ' AND request.type = ?', (request_type,))
		else:
			self.db.execute(base_query)
		return self.db.fetchall()
	# get_3p_elements

	def get_page_domain_request_domain_pairs(self):
		"""
		returns all of the unique pairings between the domain of a page and that
			of an element domain
		"""
		query = """
				SELECT DISTINCT page_domain.domain, request_domain.domain 
				FROM page
				LEFT JOIN request ON request.page_id = page.id
				LEFT JOIN domain request_domain ON request_domain.id = request.domain_id
				LEFT JOIN domain page_domain ON page_domain.id = page.final_url_domain_id
		"""	
		self.db.execute(query)
		return self.db.fetchall()
	# get_page_domain_request_domain_pairs

	def get_crawl_id_3p_domain_info(self):
		self.db.execute("""
			SELECT 
				crawl_id, domain, domain_owner_id
			FROM
				crawl_id_domain_lookup
		""")
		return self.db.fetchall()
	# get_crawl_id_3p_domain_info

	def get_page_id_3p_request_domain_info(self):
		"""
		Returns 3p request domains and owner_ids
		"""
		self.db.execute("""
			SELECT DISTINCT page.id, request_domain.domain, request_domain.domain_owner_id
			FROM page
			JOIN request ON request.page_id = page.id
			JOIN domain request_domain ON request_domain.id = request.domain_id
			WHERE request.is_3p IS TRUE
		""")
		return self.db.fetchall()
	# get_page_id_3p_request_domain_info

	def get_crawl_id_3p_request_domain_info(self):
		"""
		Returns 3p request domains and owner_ids
		"""
		self.db.execute("""
			SELECT DISTINCT page.crawl_id, request_domain.domain, request_domain.domain_owner_id
			FROM page
			JOIN request ON request.page_id = page.id
			JOIN domain request_domain ON request_domain.id = request.domain_id
			WHERE request.is_3p IS TRUE
		""")
		return self.db.fetchall()
	# get_crawl_id_3p_request_domain_info

	def get_crawl_id_3p_domstorage_domain_info(self):
		"""
		Returns 3p request domains and owner_ids
		"""
		self.db.execute("""
			SELECT DISTINCT page.crawl_id, dom_storage_domain.domain, dom_storage_domain.domain_owner_id
			FROM page
			JOIN dom_storage ON dom_storage.page_id = page.id
			JOIN domain AS dom_storage_domain ON dom_storage_domain.id = dom_storage.domain_id
			WHERE dom_storage.is_3p IS TRUE
		""")
		return self.db.fetchall()
	# get_crawl_id_3p_domstorage_domain_info

	def get_page_id_3p_response_domain_info(self):
		"""
		Returns 3p request domains and owner_ids
		"""
		self.db.execute("""
			SELECT DISTINCT page.id, response_domain.domain, response_domain.domain_owner_id
			FROM page
			JOIN response ON response.page_id = page.id
			JOIN domain response_domain ON response_domain.id = response.domain_id
			WHERE response.is_3p IS TRUE
		""")
		return self.db.fetchall()
	# get_page_id_3p_response_domain_info

	def get_crawl_id_3p_response_domain_info(self):
		"""
		Returns 3p request domains and owner_ids
		"""
		self.db.execute("""
			SELECT DISTINCT page.crawl_id, response_domain.domain, response_domain.domain_owner_id
			FROM page
			JOIN response ON response.page_id = page.id
			JOIN domain response_domain ON response_domain.id = response.domain_id
			WHERE response.is_3p IS TRUE
		""")
		return self.db.fetchall()
	# get_crawl_id_3p_response_domain_info

	def get_page_id_3p_websocket_domain_info(self):
		"""
		Returns 3p request domains and owner_ids
		"""
		self.db.execute("""
			SELECT DISTINCT page.id, websocket_domain.domain, websocket_domain.domain_owner_id
			FROM page
			JOIN websocket ON websocket.page_id = page.id
			JOIN domain websocket_domain ON websocket_domain.id = websocket.domain_id
			WHERE websocket.is_3p IS TRUE
		""")
		return self.db.fetchall()
	# get_page_id_3p_response_domain_info

	def get_crawl_id_3p_websocket_domain_info(self):
		"""
		Returns 3p request domains and owner_ids
		"""
		self.db.execute("""
			SELECT DISTINCT page.crawl_id, websocket_domain.domain, websocket_domain.domain_owner_id
			FROM page
			JOIN websocket ON websocket.page_id = page.id
			JOIN domain websocket_domain ON websocket_domain.id = websocket.domain_id
			WHERE websocket.is_3p IS TRUE
		""")
		return self.db.fetchall()
	# get_crawl_id_3p_websocket_domain_info

	def get_page_id_3p_cookie_domain_info(self):
		"""
		Returns 3p request domains and owner_ids
		"""
		self.db.execute("""
			SELECT DISTINCT page.id, cookie_domain.domain, cookie_domain.domain_owner_id
			FROM page
			JOIN cookie ON cookie.page_id = page.id
			JOIN domain cookie_domain ON cookie_domain.id = cookie.domain_id
			WHERE cookie.is_3p IS TRUE
		""")
		return self.db.fetchall()
	# get_page_id_3p_response_domain_info

	def get_crawl_id_3p_cookie_domain_info(self):
		"""
		Returns 3p request domains and owner_ids
		"""
		self.db.execute("""
			SELECT DISTINCT page.crawl_id, cookie_domain.domain, cookie_domain.domain_owner_id
			FROM page
			JOIN cookie ON cookie.page_id = page.id
			JOIN domain cookie_domain ON cookie_domain.id = cookie.domain_id
			WHERE cookie.is_3p IS TRUE
		""")
		return self.db.fetchall()
	# get_crawl_id_3p_cookie_domain_info

	def get_page_id_3p_cookie_id_3p_cookie_domain(self, tld_filter=None):
		"""
		returns all of the page id and third-party cookie id
		"""
		query = '''
			SELECT DISTINCT page.id, cookie.id, cookie_domain.domain
			FROM page
			JOIN domain page_domain ON page_domain.id = page.final_url_domain_id
			JOIN cookie on cookie.page_id = page.id
			JOIN domain cookie_domain ON cookie_domain.id = cookie.domain_id
			WHERE cookie.is_3p IS TRUE
		'''

		if tld_filter: 
			query += " AND page_domain.tld = '"+tld_filter+"'"
	
		self.db.execute(query)
		return self.db.fetchall()
	# get_page_id_3p_cookie_id_3p_cookie_domain
	
	def get_crawl_id_3p_cookie_id_3p_cookie_domain(self, tld_filter=None):
		"""
		returns all of the crawl id and third-party cookie id
		"""
		query = '''
			SELECT DISTINCT page.crawl_id, cookie.name, cookie_domain.fqdn
			FROM page
			JOIN domain page_domain ON page_domain.id = page.final_url_domain_id
			JOIN cookie on cookie.page_id = page.id
			JOIN domain cookie_domain ON cookie_domain.id = cookie.domain_id
			WHERE cookie.is_3p IS TRUE
		'''

		if tld_filter: 
			query += " AND page_domain.tld = '"+tld_filter+"'"
	
		self.db.execute(query)
		return self.db.fetchall()
	# get_crawl_id_3p_cookie_id_3p_cookie_domain

	def get_3p_network_ties(self, domain_owner_is_known = False):
		"""
		returns all of the unique pairings between the domain of a page and that
			of an element
		
		paramater domain_owner_is_known is to only return those elements where we have
			identified the owner
		"""
		query = """
				SELECT DISTINCT page_domain.domain, request_domain.domain, request_domain.domain_owner_id
				FROM page
				LEFT JOIN request ON request.page_id = page.id
				JOIN domain page_domain ON page.final_url_domain_id = page_domain.id
				JOIN domain request_domain ON request_domain.id = request.domain_id
				WHERE request.is_3p = TRUE
		"""
		
		# to limit analysis to domains who we know the owner add following to above query
		if domain_owner_is_known: query += " AND request_domain.domain_owner_id IS NOT NULL "
		
		query += " ORDER BY page_domain.domain, request_domain.domain "
		
		self.db.execute(query)
		return self.db.fetchall()
	# get_3p_network_ties

	def get_3p_request_domain_owner_id_ssl_use(self,tld_filter=None):
		"""
		for each third-party request return
			the domain, the owner id, and true/false value for ssl
		"""
		if tld_filter:
			self.db.execute("""
				SELECT
					request_domain.domain,
					request_domain.domain_owner_id,
					request.is_ssl
				FROM element 
				JOIN domain request_domain 
					ON request.domain_id = request_domain.id
				JOIN page
					ON request.page_id = page.id
				JOIN domain page_domain
					ON page.final_url_domain_id = page_domain.id
				WHERE request_domain.domain_owner_id IS NOT NULL
				AND request.is_3p = TRUE
				AND page_domain.tld = ?
			""", (tld_filter,))
		else:
			self.db.execute("""
				SELECT 
					request_domain.domain,
					request_domain.domain_owner_id,
					request.is_ssl
				FROM request 
				JOIN domain request_domain 
					ON request.domain_id = request_domain.id
				WHERE request_domain.domain_owner_id IS NOT NULL
				AND request.is_3p = TRUE
			""")

		return self.db.fetchall()
	# get_3p_request_domain_owner_id_ssl_use

	def get_3p_request_domain_ssl_use(self):
		"""
		for each third-party request returns
			the domain and true/false value for ssl
		"""
		self.db.execute('''
			SELECT 
				domain.domain,
				request.is_ssl
			FROM element 
			JOIN 
				domain on request.domain_id = domain.id 
			WHERE request.is_3p = TRUE
		''')

		return self.db.fetchall()
	# get_3p_request_domain_owner_id_ssl_use

	def get_all_pages_elements(self, only_3p=True):
		"""
		For all pages get all of the elements associated with each page 
			load.  Default is only_3p, but this can be overridden to get
			1p as well.
		"""

		base_query = '''
			SELECT DISTINCT
				page.accessed,
				page.start_url,
				page.final_url,
				request_domain.domain,
				request_domain.domain_owner_id,
				request.base_url
			FROM
				page
			JOIN
				request ON request.page_id = page.id
			JOIN
				domain request_domain ON request_domain.id = request.domain_id
		'''

		if only_3p:
			base_query+'WHERE request.is_3p = True'

		self.db.execute(base_query + 'ORDER BY page.accessed,page.start_url')

		return self.db.fetchall()
	# get_all_page_elements

	def get_all_pages_cookies(self, only_3p=False):
		"""
		For all pages get all of the cookies associated with each page 
			load.  Default is 1p and 3p, but this can be overridden to get
			3p only.
		"""

		base_query = '''
			SELECT DISTINCT
				page.accessed,
				page.start_url,
				page.final_url,
				cookie_domain.domain,
				cookie_domain.domain_owner_id,
				cookie.name,
				cookie.value
			FROM
				page
			JOIN
				cookie ON cookie.page_id = page.id
			JOIN
				domain cookie_domain ON cookie_domain.id = cookie.domain_id
		'''

		if only_3p:
			base_query+'WHERE cookie.is_3p = True'

		self.db.execute(base_query + 'ORDER BY page.accessed,page.start_url')

		return self.db.fetchall()
	# get_all_pages_cookies

	def get_single_page_elements(self, page_start_url, only_3p=True):
		"""
		For a given page (defined as unique start_url) get all of the elements associated
			with every page load.  Default is only_3p, but this can be overridden to get
			1p as well.
		"""

		base_query = '''
			SELECT DISTINCT
				page.accessed,
				page.start_url,
				page.final_url,
				page.is_ssl,
				request.base_url,
				request_domain.domain,
				request_domain.domain_owner_id
			FROM
				page
			JOIN
				element ON request.page_id = page.id
			JOIN
				domain request_domain ON request_domain.id = request.domain_id				
			WHERE
				page.start_url = ?
		'''

		if only_3p:
			self.db.execute(base_query+'AND request.is_3p = True', (page_start_url,))
		else:
			self.db.execute(base_query, (page_start_url,))

		return self.db.fetchall()
	# get_single_page_elements

	def get_single_page_cookies(self, page_start_url, only_3p=True):
		"""
		For a given page (defined as unique start_url) get all of the cookies associated
			with every page load.  Default is only_3p, but this can be overridden to get
			1p as well.
		"""

		base_query = '''
			SELECT DISTINCT
				page.accessed,
				page.start_url,
				page.final_url,
				page.is_ssl,
				cookie.domain,
				cookie.name,
				cookie.value,
				cookie_domain.domain_owner_id
			FROM
				page
			JOIN
				cookie ON cookie.page_id = page.id
			JOIN
				domain cookie_domain ON cookie_domain.id = cookie.domain_id				
			WHERE
				page.start_url = ?
		'''

		if only_3p:
			self.db.execute(base_query+'AND cookie.is_3p = True', (page_start_url,))
		else:
			self.db.execute(base_query, (page_start_url,))

		return self.db.fetchall()
	# get_single_page_cookies

	def get_page_ips_w_no_owner(self):
		"""
		Returns all ip addresses for pages where
			we don't know the ip_owner
		"""
		self.db.execute('''
			SELECT DISTINCT domain.ip_addr
			FROM page
			JOIN domain ON page.final_url_domain_id = domain.id
			WHERE domain.ip_addr IS NOT NULL
			AND domain.ip_owner IS NULL
		''')
		return self.db.fetchall()
	# get_page_ips_w_no_owner

	def update_ip_owner(self,ip_addr,ip_owner):
		"""
		Does what it says.
		"""
		self.db.execute('UPDATE domain SET ip_owner = ? WHERE ip_addr = ?', (ip_owner,ip_addr))
		self.db_conn.commit()
	# update_site_host

	def get_site_hosts(self):
		"""
		Return all records where we known the owner of the ip_addr
			corresponding to a given page's fqdn.
		"""
		self.db.execute("""
			SELECT DISTINCT
				domain.fqdn, domain.ip_owner
			FROM 
				page
			JOIN
				domain
			ON
				page.final_url_domain_id = domain.id
			WHERE
				domain.ip_owner IS NOT NULL
		""")
		return self.db.fetchall()
	# get_site_hosts

	def get_ip_owners(self):
		"""
		Return all records of ip_owners, not distinct.

		"""
		self.db.execute("""
			SELECT 
				domain.ip_owner
			FROM 
				page
			JOIN
				domain
			ON
				page.final_url_domain_id = domain.id
			WHERE
				domain.ip_owner IS NOT NULL
		""")
		return self.db.fetchall()
	# get_ip_owners

	def get_dom_storage_count(self):
		self.db.execute("SELECT COUNT(*) FROM dom_storage")
		return self.db.fetchone()[0]
	# get_dom_storage_count

	def get_websocket_count(self):
		self.db.execute("SELECT COUNT(*) FROM websocket")
		return self.db.fetchone()[0]
	# get_websocket_count

	def get_websocket_event_count(self):
		self.db.execute("SELECT COUNT(*) FROM websocket_event")
		return self.db.fetchone()[0]
	# get_websocket_event_count

	def get_crawl_3p_domain_counts(self):
		"""
		Leverage the lookup table to see how many 3p domains we have
			per crawl.
		"""
		self.db.execute("select crawl_id,count(*) from crawl_id_domain_lookup group by crawl_id")
		return self.db.fetchall()
	# get_crawl_3p_domain_counts

	def get_page_3p_domain_counts(self):
		"""
		Leverage the lookup table to see how many 3p domains we have
			per page.
		"""
		self.db.execute("select page_id,count(*) from page_id_domain_lookup group by page_id")
		return self.db.fetchall()
	# get_crawl_3p_domain_counts

	def get_crawl_count_by_domain_owners(self, domain_owner_list):
		"""
		Leverage the lookup table to see how many crawls are tracked
			by a given domain owner, not that this processes a list
			which may be the owner+children.
		"""
		query = f"SELECT COUNT(DISTINCT crawl_id) FROM crawl_id_domain_lookup WHERE domain_owner_id = '{domain_owner_list[0]}'"
		for item in domain_owner_list[1:]:
			query += f" OR domain_owner_id = '{item}'"
		self.db.execute(query)
		return self.db.fetchone()[0]
	# get_crawl_count_by_domain_owners

	def get_crawl_id_3p_cookie_domain_pairs(self):
		self.db.execute("""
			SELECT DISTINCT
				crawl_id,
				domain
			FROM
				crawl_id_domain_lookup
			WHERE
				is_cookie IS TRUE

		""")
		return self.db.fetchall()
	# get_crawl_id_3p_cookie_domain_pairs

	def get_crawl_id_to_3p_domain_pairs(self):
		self.db.execute("""
			SELECT DISTINCT
				crawl_id,
				domain
			FROM
				crawl_id_domain_lookup
		""")
		return self.db.fetchall()
	# get_crawl_id_to_3p_domain_pairs



	#------------#
	# POLICYXRAY #
	#------------#

	def get_scanned_policy_urls(self):
		"""
		Allows us to skip policies we've already scanned in cases
			where we rebuild a task queue.
		"""
		self.db.execute("""
			SELECT DISTINCT
				start_url
			FROM
				policy
		""")
		return self.db.fetchall()
	# get_scanned_policy_urls

	def get_policies_to_collect(self):
		"""
		Returns list of policy urls that we have not yet successfully
			downloaded.
		"""
		self.db.execute("""
			SELECT DISTINCT
				link.url
			FROM
				link
			LEFT OUTER JOIN
				policy
			ON
				policy.start_url  = link.url
			WHERE
				link.is_policy = TRUE
			AND
				link.is_internal = TRUE
			AND
				policy.start_url IS NULL
		""")
		return self.db.fetchall()
	# get_policies_to_collect

	def add_policy(self, policy):
		"""
		Once a policy has been downloaded and text extracted,
			we store it in the db and return the id of
			the new record.
		"""
		self.db.execute("""
			INSERT INTO policy (
				client_id,
				client_ip,
				browser_type,
				browser_version,
				browser_prewait,
				start_url,
				start_url_md5,
				start_url_domain_id,
				final_url,
				final_url_md5,
				final_url_domain_id,
				title,
				meta_desc,
				lang,
				fk_score,
				fre_score,
				type,
				match_term,
				match_text,
				match_text_type,
				confidence,
				page_text_id,
				page_source_md5
			) VALUES (
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?,
				?
			) ON CONFLICT DO NOTHING""",
			(
				policy['client_id'],
				policy['client_ip'],
				policy['browser_type'],
				policy['browser_version'],
				policy['browser_prewait'],
				policy['start_url'],
				self.md5_text(policy['start_url']),
				policy['start_url_domain_id'],
				policy['final_url'],
				self.md5_text(policy['final_url']),
				policy['final_url_domain_id'],
				policy['title'],
				policy['meta_desc'],
				policy['lang'],
				policy['fk_score'],
				policy['fre_score'],
				policy['type'],
				policy['match_term'],
				policy['match_text'],
				policy['match_text_type'],
				policy['confidence'],
				policy['page_text_id'],
				policy['page_source_md5']
			)
		)

		# return id of record with this start_url and accessed time
		self.db.execute("SELECT id FROM policy WHERE start_url = ? AND page_text_id = ?", (policy['start_url'],policy['page_text_id']))
	
		return self.db.fetchone()[0]
	# add_policy

	def get_page_ids_from_link_url(self, url, internal_links_only=False):
		"""
		A given url may correspond to many links due to the fact
			that different text can go to the same link, so we
			return all ids matching a given url.
		"""
		if internal_links_only:
			self.db.execute("""
				SELECT
					page.id, page.crawl_id
				FROM
					page_link_junction
				JOIN 
					link
				ON
					link.id = page_link_junction.link_id
				JOIN
					page
				ON
					page.id = page_link_junction.page_id
				WHERE
					link.url_md5 = ?
				AND
					link.is_internal IS TRUE
			""", (self.md5_text(url),))
		else:
			self.db.execute("""
				SELECT
					page.id, page.crawl_id
				FROM
					page_link_junction
				JOIN 
					link
				ON
					link.id = page_link_junction.link_id
				JOIN
					page
				ON
					page.id = page_link_junction.page_id
				WHERE
					link.url_md5 = ?
			""", (self.md5_text(url),))
		return self.db.fetchall()
	# get_page_ids_from_link_url

	def attach_policy_to_page(self, policy_id, page_id):
		"""
		Given a policy_id and page_id we create a record in
			the junction table.
		"""
		self.db.execute("""
			INSERT INTO page_policy_junction (policy_id, page_id)
			VALUES (?,?)
			ON CONFLICT DO NOTHING""", 
			(policy_id, page_id)
		)
		self.db_conn.commit()
	# attach_policy_to_page

	def attach_policy_to_crawl(self, policy_id, crawl_id):
		"""
		Given a policy_id and page_id we create a record in
			the junction table.
		"""
		self.db.execute("""
			INSERT INTO crawl_policy_junction (policy_id, crawl_id)
			VALUES (?,?)
			ON CONFLICT DO NOTHING""", 
			(policy_id, crawl_id)
		)
		self.db_conn.commit()
	# attach_policy_to_crawl

	def get_id_and_policy_text(self, word_count_null=None, readability_null=None):
		"""
		Return the policy_id and text, several options for filtering.
		"""
		if word_count_null is True:
			self.db.execute("SELECT id, text FROM policy WHERE word_count is NULL")
		elif readability_null is True:
			self.db.execute("SELECT id, text FROM policy WHERE fre_score is NULL OR fk_score is NULL")
		else:
			self.db.execute("SELECT id, text FROM policy")
		return self.db.fetchall()
	# get_id_and_policy_text

	def get_total_policy_count(self, policy_type=None):
		"""
		Return the total number of policies matching specified conditions.
		"""
		if policy_type:
			self.db.execute('SELECT COUNT(*) FROM policy WHERE type = ?', (policy_type,))
		else:
			self.db.execute('SELECT COUNT(*) FROM policy')
		return self.db.fetchone()[0]
	# get_total_policy_count

	def get_average_policy_word_count(self,policy_type=None):
		"""
		Does what it says.
		"""
		if policy_type:
			self.db.execute("""
				SELECT 
					AVG(page_text.word_count)
				FROM 
					policy
				JOIN
					page_text
				ON
					policy.page_text_id = page_text.id
				WHERE 
					policy.type = ?
			""", (policy_type,))
		else:
			self.db.execute("""
				SELECT 
					AVG(page_text.word_count)
				FROM 
					policy
				JOIN
					page_text
				ON
					policy.page_text_id = page_text.id
			""")
		return self.db.fetchone()[0]
	# get_average_policy_word_count

	def update_readability_scores(self, policy_id, fre_score, fk_score):
		"""
		Once we have our readability scores we update the db.
		"""
		self.db.execute("""
			UPDATE policy
			SET
				fre_score 	= ?,
				fk_score	= ?
			WHERE
				id 			= ?""", 
			(fre_score, fk_score, policy_id)
		)
		self.db_conn.commit()
	# update_readability_scores

	def get_ave_fre(self,policy_type=None):
		"""
		Returns average Flesch Reading Ease score for specified 
			policy type, ignores invalid scores (<0).
		"""
		if policy_type:
			self.db.execute('SELECT AVG(fre_score) FROM policy WHERE fre_score > 0 AND type = ?', (policy_type,))
		else:
			self.db.execute('SELECT AVG(fre_score) FROM policy WHERE fre_score > 0')
		return self.db.fetchone()[0]
	# get_ave_fre

	def get_ave_fkg(self,policy_type=None):
		"""
		Returns average Flesch Kinkaid Grade-Level score for specified 
			policy type, ignores invalid scores (<0).
		"""
		if policy_type:
			self.db.execute('SELECT AVG(fk_score) FROM policy WHERE fk_score > 0 AND type = ?', (policy_type,))
		else:
			self.db.execute('SELECT AVG(fk_score) FROM policy WHERE fk_score > 0')
		return self.db.fetchone()[0]
	# get_ave_fkg

	def get_all_page_id_3p_request_owner_ids(self,not_in_disclosure_table=None):
		"""
		Returns unique pairs of page_id to request_owner_ids which is dependent
			on the owner_ids having already been entered via the analyzer.

		The not_in_disclosure_table option removes those results that are in
			the disclosure table so we don't waste time doing them twice.
		"""

		query = """
			SELECT DISTINCT 
				page.id, request_domain.domain_owner_id 
			FROM 
				page
			JOIN 
				request ON request.page_id = page.id
			JOIN 
				domain request_domain ON request.domain_id = request_domain.id
		"""

		if not_in_disclosure_table:
			query += """
				LEFT OUTER JOIN
					policy_request_disclosure ON (page.id = policy_request_disclosure.page_id AND request_domain.domain_owner_id = policy_request_disclosure.request_owner_id)
				WHERE 
					request.is_3p = TRUE
				AND 
					request_domain.domain_owner_id IS NOT NULL
				AND
					policy_request_disclosure.page_id IS NULL
			"""

		self.db.execute(query)
		return self.db.fetchall()
	# get_all_page_id_3p_request_owner_ids

	def get_all_crawl_id_3p_request_owner_ids(self):
		self.db.execute("""
			SELECT DISTINCT 
				crawl_id, domain_owner_id 
			FROM
				crawl_id_domain_lookup
			WHERE
				domain_owner_id IS NOT NULL
		""")
		return self.db.fetchall()
	# get_all_crawl_id_3p_request_owner_ids		

	def get_page_id_policy_id_policy_text(self, policy_type=None):
		"""
		For all pages with a link to a policy return page_id, policy_id,
			and policy_text.
		"""
		self.db.execute('''
			SELECT DISTINCT 
				page_id,
				policy_id,
				page_text.text
			FROM 
				page_policy_junction
			JOIN
				policy on page_policy_junction.policy_id = policy.id
			JOIN
				page_text on policy.page_text_id = page_text.id
		''')
		return self.db.fetchall()
	# get_page_id_policy_id

	def get_crawl_id_policy_id_policy_text(self, policy_type=None):
		"""
		For all pages with a link to a policy return page_id, policy_id,
			and policy_text.
		"""
		self.db.execute('''
			SELECT DISTINCT 
				crawl_id,
				policy_id,
				page_text.text
			FROM 
				crawl_policy_junction
			JOIN
				policy on crawl_policy_junction.policy_id = policy.id
			JOIN
				page_text on policy.page_text_id = page_text.id
		''')
		return self.db.fetchall()
	# get_page_id_policy_id

	def update_request_disclosure(self, page_id, policy_id, request_owner_id, disclosed, disclosed_owner_id):
		"""
		For each pairing of page_id to request_owner_id we record if
			it was disclosed, and if so, the owner_id that was disclosed.
		Because we mark disclosure where a parent company is mentioned, this means
			that the request_owner_id and disclosed_owner_id may not match.
		"""
		self.db.execute("""
			INSERT INTO policy_request_disclosure (
				page_id, policy_id, 
				request_owner_id, disclosed,
				disclosed_owner_id
			) VALUES (?,?,?,?,?)
			ON CONFLICT DO NOTHING""", 
			(	page_id, policy_id, 
				request_owner_id, disclosed,
				disclosed_owner_id)
		)
		self.db_conn.commit()
	# update_request_disclosure

	def update_crawl_3p_domain_disclosure(self, crawl_id, domain_owner_id):
		"""
		Mark domains that are disclosed.
		"""
		self.db.execute("""
			UPDATE crawl_id_domain_lookup
			SET is_disclosed = TRUE
			WHERE 
				crawl_id = ?
			AND
				domain_owner_id =?
		""", 
			(	crawl_id,
				domain_owner_id)
		)
		self.db_conn.commit()
	# update_crawl_3p_domain_disclosure
	
	def get_total_request_disclosure_count(self, disclosed=None, policy_type=None):
		"""
		Does what it says.
		"""
		if disclosed and policy_type:
			self.db.execute("""
				SELECT COUNT(*) 
				FROM policy_request_disclosure 
				JOIN policy ON policy_request_disclosure.policy_id = policy.id
				WHERE policy_request_disclosure.disclosed IS TRUE 
				AND policy.type = ?
			""", (policy_type,))
		elif disclosed:
			self.db.execute("SELECT COUNT(*) FROM policy_request_disclosure WHERE disclosed IS TRUE")
		elif policy_type:
			self.db.execute("""
				SELECT COUNT(*) 
				FROM policy_request_disclosure 
				JOIN policy ON policy_request_disclosure.policy_id = policy.id
				WHERE policy.type = ?
			""", (policy_type,))
		else:	
			self.db.execute("SELECT COUNT(*) FROM policy_request_disclosure")
		return self.db.fetchone()[0]
	# get_total_request_disclosure_count

	def get_total_crawl_3p_disclosure_count(self):
		"""
		Does what it says.
		"""
		self.db.execute("""
			SELECT COUNT(*) 
			FROM crawl_id_domain_lookup 
			WHERE is_disclosed IS TRUE 
		""")
		return self.db.fetchone()[0]
	# get_total_crawl_3p_disclosure_count

	def get_total_crawl_3p_count(self):
		self.db.execute("""
			SELECT COUNT(*) 
			FROM crawl_id_domain_lookup
		""")
		return self.db.fetchone()[0]
	# get_total_crawl_3p_count

	def get_domain_owner_disclosure_count(self, owner_id, child_owner_ids=None, disclosed=None, policy_type=None):
		"""
		For a given owner_id determines how often it occurs in the table, and if 
			'disclosed' is True, it it was disclsoed.  In cases where we have a list
			of child owners we construct a query which accounts for all of them.
		
		Note that this is distinct on the page id to avoid over-counting for
			subsidiaries.
		"""
		if child_owner_ids:
			query = f"SELECT COUNT(DISTINCT page_id) FROM policy_request_disclosure WHERE (request_owner_id = '{owner_id}' OR "
			for child_owner_id in child_owner_ids:
				query += f"request_owner_id = '{child_owner_id}' OR "
			query = query[:-4] + ")"
		else:
			query = f"SELECT COUNT(DISTINCT page_id) FROM policy_request_disclosure where request_owner_id = '{owner_id}'"

		if disclosed:
			query += " AND disclosed IS TRUE"

		self.db.execute(query)
		return self.db.fetchone()[0]
	# get_domain_owner_disclosure_count

	def get_policy_substrings_count(self,substrings,policy_type=None):
		"""
		Find the number of policies where there is a match
			on any of the provided substrings.
		"""

		query = """
			SELECT 
				COUNT(*)
			FROM 
				policy
			JOIN
				page_text
			ON
				policy.page_text_id = page_text.id
		"""

		if policy_type:
			query += " WHERE type = '"+policy_type+"' AND (page_text.text like '%"+substrings[0]+"%'"
		else:
			query += " WHERE (page_text.text like '%"+substrings[0]+"%'"

		for substring in substrings[1:]:
			query += " OR page_text.text like '%"+substring+"%'"

		# close conditional
		query += ")"

		self.db.execute(query)
		return self.db.fetchone()[0]
	# get_policy_substrings_count

	def get_available_policy_types(self):
		"""
		We may not get all types of policies on each run, this just tells us what
			we have in the db.
		"""
		self.db.execute('SELECT DISTINCT type FROM policy')
		return self.db.fetchall()
	# get_available_policy_types

	
# SQLiteDriver
