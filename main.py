import os.path
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from logging import basicConfig, DEBUG, getLogger
from re import search, subn
from base64 import b64encode
from argparse import ArgumentParser

import xml.etree.ElementTree as ET

logger = getLogger(__name__)
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/drive"]

# The ID and range of a sample spreadsheet.
tries = 0

parser = ArgumentParser(
    prog="XML to google spreadsheet",
    description="Viz run.ps1 help stránka",
    epilog="Developer: Erik Sabol, e-mail: erik.sab18@gmail.com"
)
parser.add_argument("Project_name")
parser.add_argument("Xml_folder")
parser.add_argument("--xml_folder_dir",  default=__file__[:-8])
parser.add_argument("--sheet_id", default="")
parser.add_argument("-x", default="A")
parser.add_argument("-y", default=1)
parser.add_argument("--out_file", default="first_frames")
args = parser.parse_args()

PROJECT_NAME = args.Project_name
XML_FOLDER = args.Xml_folder
XML_FOLDER_DIR = args.xml_folder_dir
BEGINNING_CELL_X = args.x
BEGINNING_CELL_Y = args.y
OUT_FILE = args.out_file
SHEET_ID = args.sheet_id
    

def read_values(service, spreadsheet_id, range):
    try:
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range)
            .execute()
        )
        
        rows = result.get("values", [])
        return result
    except HttpError as error:
        logger.error(f"{error}")
        return None

def create_spreadsheet(service):
    spreadsheet = {"properties": {"title": f"{PROJECT_NAME} shots breakdown"}}
    try:
        return (
            service.spreadsheets()
            .create(body=spreadsheet, fields="spreadsheetId")
            .execute()
        )
    except HttpError as error:
        logger.error(error)
        return None

# timecode int to human readable string
def parse_tc(tc: int):
    assert tc % 100 == 0, "Timecode doesnt end with 00"
    tc /= 100
    hour = str(int(tc // (60*60*25)))
    tc = tc % (60*60*25)
    minute = str(int(tc // (60*25)))
    tc = tc % (60*25)
    second = str(int(tc // (25)))
    tc = tc % (25)
    frame = str(int(tc))
    return f"{hour.zfill(2)}:{minute.zfill(2)}:{second.zfill(2)}:{frame.zfill(2)}"

def add_values(service, spreadsheetId, sheetRange, cell_data):
    try:
        body={"values": cell_data}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheetId,
                range=sheetRange,
                valueInputOption="USER_ENTERED",
                body=body
            )
            .execute()
        )
        logger.info(f"Updated cells in range: {BEGINNING_CELL_X}{BEGINNING_CELL_Y}:{chr(ord(BEGINNING_CELL_X)+3)}{int(BEGINNING_CELL_Y)+len(cell_data)}")
        logger.debug(f"Response: {result}")
        return spreadsheetId
    except HttpError as error:
        logger.error(error)
        return None

def main():
    os.chdir(XML_FOLDER_DIR)
    cwd = os.getcwd()
    # Assert, that XML folder is present
    assert XML_FOLDER in os.listdir(XML_FOLDER_DIR), f"XML folder not found in {XML_FOLDER_DIR}"
    basicConfig(filename="script.log", level=DEBUG)
    logger.info("-------- Started --------")

    # Some bullshit i copied off of googles page, will require log in
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    # Google service for api
    service_sheets = build("sheets", "v4", credentials=creds)
    
    # Find list of clips in project, see the .fcpxml file
    tree = ET.parse(f"{os.path.join(XML_FOLDER_DIR, XML_FOLDER)}/{XML_FOLDER}.fcpxml")
    project = tree.getroot().find("library").find("event").find("project")
    assert project.attrib["name"] == XML_FOLDER, "Bad XML file name"
    assert len(project.findall("sequence")) == 1, "Multiple sequences in folder, napis erikovi"
    spine = project.find("sequence").find("spine")
    
    cell_data = []
    for clip in spine:
        if clip.tag == "clip":
            time_code = parse_tc(int(clip.attrib["offset"].split("/")[0]))
            name = clip.attrib["name"]
            matched_dirs = [dir for dir in os.listdir(os.path.join(XML_FOLDER_DIR, OUT_FILE)) if search(name, dir)]
            assert len(matched_dirs) == 1, f"Found {len(matched_dirs)} first frames for name {name} in {matched_dirs}, napis erikovi"
            file_name = matched_dirs[0]
            name = os.path.join(cwd, OUT_FILE, file_name)
            file_contents = open(name, "rb").read()
            

            prefix, scene, shot_num = file_name.split("_")[:3]
            cell_data.append(
                (
                f"{PROJECT_NAME} / {scene.zfill(3)} / {scene.zfill(3)}_{shot_num.zfill(3)}",
                scene,
                time_code,
                f'{b64encode(file_contents).decode("utf-8")}'
                )
            )
    
    
    spreadsheet = SHEET_ID
    tries = 0
    while spreadsheet == '':
        if tries >= 10:
            logger.error("Could not create spreadsheet")
            print("kAmo nefunguje ti iNterNet")
            raise HttpError
        tries += 1
        spreadsheet = create_spreadsheet(service_sheets)
    logger.debug(f"Operating on spreadsheet: {spreadsheet}")
    values_added = None
    tries = 0
    while values_added == None:
        if tries >= 10:
            print("kAmo nefunguje ti iNterNet")
            logger.error("Could not add values for some reason")
            raise HttpError
        tries += 1
        values_added = add_values(service_sheets,
                spreadsheet.get("spreadsheetId"),
                f"{BEGINNING_CELL_X}{BEGINNING_CELL_Y}:{chr(ord(BEGINNING_CELL_X)+3)}{int(BEGINNING_CELL_Y)+len(cell_data)}",
                cell_data)

if __name__ == "__main__":
    main()