import os
import sys
import json
import time
from datetime import datetime

from pgzero.keyboard import Keyboard


flags = [
	( "help", "-h", "--help", "Show help" ),
	( "list", "-l", "--list", "Show list of timers." ),
	( "pause", "-p", "--pause", "Pause a timer." ),
	( "reset", "-r", "--reset", "Reset a timer." ),
	( "start", "-s", "--start", "Start/resume a new timer." ),
	( "tick", "-t", "--tick", "Show timers in realtime." )
]


class Command:
	def __init__( self ):
		global flags
		self.timer_name = ""
		self.messages = [ ]
		self.timers = [ ]
		self.timer = { }
		self.flags = { }
		for flag in flags:
			self.flags[ flag[ 0 ] ] = False


command = Command()


# Start Py Timer
def start():
	global command
	
	# Find the timer in timers
	command.timer, _ = get_timer( command.timer_name )
	
	# Start the timer
	if command.flags[ "start" ]:
		if not command.timer:
			if command.timer_name == "":
				command.timer_name = "Unnamed Timer"
			create_new_timer()
		else:
			if command.timer[ "track_start" ] == 0:
				command.timer[ "track_start" ] = time.time()
				command.timer[ "status" ] = "running"
			else:
				print( "Cannot start a timer that is already started." )
				print_timer_status()
				return
		print( f"Starting {command.timer_name}." )
	
	# Pause the timer
	elif command.flags[ "pause" ]:
		if command.timer[ "track_start" ] == 0:
			print( "Cannot pause a timer that hasn't started." )
		else:
			update_elapsed( command.timer )
			command.timer[ "track_start" ] = 0
			command.timer[ "status" ] = "paused"
			print( f"Pausing {command.timer_name}." )
		print_timer_status()
	
	# Print all timers
	elif command.flags[ "list" ]:
		print_timer_table()
	
	# Print help
	elif command.flags[ "help" ]:
		print_help()
	
	# Reset Timer
	elif command.flags[ "reset" ]:
		reset_timer()
	
	# Show Timer in Realtime
	elif command.flags[ "tick" ]:
		tick()
	
	# Update timer status
	else:
		timer, _ = get_timer( command.timer_name )
		if command.timer_name != "" and not timer:
			create_new_timer( "paused" )
		else:
			print_timer_status()
	
	# Save the timer to file
	save_timer_data()


# Get a command from timer
def get_timer( timer_name = "" ):
	if timer_name == "":
		search = command.timer_name
	else:
		search = timer_name
	for i in range( 0, len( command.timers ) ):
		timer = command.timers[ i ]
		if timer[ "name" ] == search:
			return timer, i
	return None, None


# Create a new timer
def create_new_timer( status = "running" ):
	global command
	
	track_start = 0
	if status == "running":
		track_start = time.time()
	command.timer = {
		"name": command.timer_name,
		"start": time.time(),
		"status": status,
		"track_start": track_start,
		"elapsed": 0,
		"end": 0
	}
	command.timers.append( command.timer )
	print( f"Creating new timer {command.timer['name']}." )
	print( f"Timer is {command.timer['status']}." )


# Reset timer
def reset_timer():
	if command.timer:
		timer_name = command.timer_name
		command.timers = list( filter( lambda timer: timer[ "name" ] != command.timer_name, command.timers ) )
		command.timer_name = ""
		print( f"Deleting {timer_name}.")
	else:
		print( "No timer selected, cannot reset." )


# Update elapsed time
def update_elapsed( timer = None ):
	t = timer if timer else command.timer
	
	if t and t[ "track_start" ]:
		t[ "elapsed" ] += time.time() - timer[ "track_start" ]
		t[ "track_start" ] = time.time()


# Print the Timer Table
def print_timer_table():
	if len( command.timers ) == 0:
		print( "There are currently no timers stored" )
		print_help()
		return
	
	# Calculate Columns
	col_data = [ len( "# " ), len( "Name " ), len( "Status " ), len( "Elapsed " ) ]
	for i in range( len( command.timers ) ):
		timer = command.timers[ i ]
		if len( str( i ) ) + 2 > col_data[ 0 ]:
			col_data[ 0 ] = len( str( i ) ) + 2
		if len( timer[ "name" ] ) + 4 > col_data[ 1 ]:
			col_data[ 1 ] = len( timer[ "name" ] ) + 4
		if len( timer[ "status" ] ) + 3 > col_data[ 2 ]:
			col_data[ 2 ] = len( timer[ "status" ] ) + 3
		f_time = format_time( timer[ "elapsed" ] )
		if len( f_time ) + 1 > col_data[ 3 ]:
			col_data[ 3 ] = len( f_time ) + 2
	
	# Print Header
	print(
		"# ".ljust( col_data[ 0 ] ) +
		"* " +
		"Name".ljust( col_data[ 1 ] ) +
		"Status".ljust( col_data[ 2 ] ) +
		"Elapsed".ljust( col_data[ 3 ] )
	)
	print(
		"-".ljust( col_data[ 0 ], "-" ) +
		"-".ljust( col_data[ 1 ], "-" ) +
		"-".ljust( col_data[ 2 ], "-" ) +
		"-".ljust( col_data[ 3 ], "-" )
	)
	# Print timer status
	for timer in command.timers:
		print_timer_status( timer[ "name" ], col_data )
	print(
		"-".ljust( col_data[ 0 ], "-" ) +
		"-".ljust( col_data[ 1 ], "-" ) +
		"-".ljust( col_data[ 2 ], "-" ) +
		"-".ljust( col_data[ 3 ], "-" )
	)
	print( "* Selected Timer" )


# Print the status of the timer
def print_timer_status( timer_name = "", col_data = None ):
	global command
	
	timer, i = get_timer( timer_name )
	update_elapsed( timer )
	if timer:
		status = "running"
		if timer[ "track_start" ] == 0:
			status = "paused"
		t_msg = format_time( timer[ "elapsed" ] )
		if col_data:
			sel = "  "
			if timer[ "name" ] == command.timer_name:
				sel = "* "
			print(
				f"{i}.".ljust( col_data[ 0 ] ) +
				f"{sel}" +
				f"{timer[ 'name' ]}".ljust( col_data[ 1 ] ) +
				f"{status}".ljust( col_data[ 2 ] ) +
				f"{t_msg}".ljust( col_data[ 3 ] )
			)
		else:
			print( f"{i}. {timer[ 'name' ]} {status}, elapsed time: {t_msg}." )
	else:
		print( "No timer selected." )
		print( "Help: pytimer -h" )


# Format time in readable format
def format_time( t ):
	days = int( t // 86400 )
	t = t % 86400
	hours = int( t // 3600 )
	t = t % 3600
	minutes = int( t // 60 )
	seconds = t % 60
	if days > 0:
		formatted_time = f"{days}d {hours}h {minutes}m {seconds:.2f}s"
	elif hours > 0:
		formatted_time = f"{hours}h {minutes}m {seconds:.2f}s"
	elif minutes > 0:
		formatted_time = f"{minutes}m {seconds:.2f}s"
	else:
		formatted_time = f"{seconds:.2f}s"
	return formatted_time


def print_help():
	global flags
	print( "Usage: pytimer [\"Timer Name\"] [options]" )
	print( "Options:" )
	for flag in flags:
		print( f"{flag[ 1 ]}, {flag[ 2 ]}".ljust( 18 ) + flag[ 3 ] )


def tick():
	try:
		if os.name == "nt":
			os.system( "cls" )
		else:
			os.system( "clear" )
		while True:
			num_lines = len( command.timers ) + 6
			for _ in range( num_lines ):
				sys.stdout.write( "\033[F" )
			print_timer_table()
			print( "Ctrl+C - to stop" )
			time.sleep( 0.05 )
	except KeyboardInterrupt:
		pass
	print()


# Parse the command line arguments
def parse_args():
	global command, flags
	args = sys.argv[ 1: ]
	for i in range( 0, len( args ) ):
		arg = args[ i ]
		
		# Check if argument is a flag
		if arg[ 0 ] == "-":
			flag_name = ""
			for flag in flags:
				if arg == flag[ 1 ] or arg == flag[ 2 ]:
					flag_name = flag[ 0 ]
			if flag_name != "":
				command.flags[ flag_name ] = True
		
		# Otherwise argument is a message
		else:
			command.messages.append( arg )
	
	# An argument is passed so use it for the timer name
	if len( command.messages ) > 0:
		if command.messages[ 0 ].isdigit():
			i = int( command.messages[ 0 ] )
			if i < len( command.timers ):
				command.timer_name = command.timers[ i ][ "name" ]
			else:
				print( f"Invalid timer index{i}" )
		else:
			command.timer_name = command.messages[ 0 ]


# Load Timer Data
def load_timer_data():
	global command
	cd = os.path.dirname( os.path.abspath( __file__ ) )
	filepath = f"{cd}/timers.json"
	if os.path.exists( filepath ):
		with open( filepath, "r" ) as file:
			timer_data = json.load( file )
		command.timers = timer_data[ "timers" ]
		command.timer_name = timer_data[ "selected_timer_name" ]
	else:
		# Create an empty file if it doesn't exist
		save_timer_data()
	
	# Make a backup of the data - if it backup doesn't exist
	backupfile = "backups/timers-" + datetime.today().strftime( "%Y%m%d" ) + ".json"
	if not os.path.exists( backupfile ):
		save_timer_data( backupfile )


# Save Timer Data
def save_timer_data( local_file="timers.json" ):
	global command
	data = {
		"timers": command.timers,
		"selected_timer_name": command.timer_name
	}
	cd = os.path.dirname( os.path.abspath( __file__ ) )
	filepath = f"{cd}/{local_file}"
	with open( filepath, "w" ) as file:
		json.dump( data, file, indent = 4 )


# Run main app
if __name__ == '__main__':
	# try:
	load_timer_data()
	parse_args()
	start()
# except Exception as ex:
#    print( ex )
