"""
Software needs to be ran in sudo because scapy requires root privi
"""
import argparse
from portscanner import Scanner
import datetime
from Logger import Log
import os
from pathlib import Path
import helper as h
from googlesheets import GoogleSheets

def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '-t', '--target', 
    dest='target', 
    help='Target IP Address / Subnet Mask'
  )

  parser.add_argument('-m', 
    '--mac_add', 
    type=str, 
    required=True, 
    help='mac address to track'
  )

  parser.add_argument(
    "-cf", 
    '--conf_file',
    type=lambda x: Path(x).absolute(),
    default=os.getcwd() + "/api_creds.json",
    help="Specify where Google Sheets API Key is." 
  )

  parser.add_argument(
    "-l", 
    "--log_dir",
    help="Log directory",
    type=lambda x: Path(x).absolute(),
    default=os.getcwd() + "/log"
  )

  options = parser.parse_args()

  if not options.target:
    parser.error("[-] Please specify an IP Address or Addresses, use --help for more info.")
  
  return options

options = get_args()
logs = Log(log_path=options.log_dir)
log = logs.get_logger()

def main():
  t0 = h.timer()
  log.info("Scanning Network For Ip addresses")
  scanner = Scanner(net_add=options.target, log=log, type="scapy")
  scanned_output = scanner.get_results()
  log.debug(f"scanned results:")
  scanner.print_debug()

  mac_add = parse_mac(options.mac_add)
  log.info(f"Parsed MAC Address: {options.mac_add} to {mac_add}")
  to_file(scanned_output, mac_add, log, options.conf_file)
  log.info(f"Time Elapsed(sec): {h.timer(t0)}")

def parse_mac(add):
  mac = add.upper().replace("-", ":")
  return mac

def check_if_powered_on(add, scanned_list):
  for scan_item in scanned_list:
    if scan_item['mac'] != add:
      continue

    return 'ON'
  
  return 'OFF'

def to_file(scanned_output, mac_add, log, conf_file):
  status = check_if_powered_on(mac_add, scanned_output)
  date = datetime.datetime.now()
  sheet_title = 'pcstatus'
  
  log.info(f'Saving results to Google Sheets: {sheet_title}')
  gs = GoogleSheets(title=sheet_title, sheet_num=0, log=log, conf_file=conf_file)
  df = gs.get_sheet()

  df = df.append(dict(date=date, status=status, mac=mac_add), ignore_index=True, sort=False)

  sheet_name = 'PCStatusTrackerData'
  gs.write_sheet(sheet_name, df)
  log.info(f"Saved results to Sheet: {sheet_name}")

if __name__ == "__main__":
  main()
