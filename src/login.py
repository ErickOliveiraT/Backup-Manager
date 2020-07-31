import drive
import sys

config = drive.Config(True)
drive.load_credentials(config)
sys.exit()