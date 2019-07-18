from apiclient import discovery, errors
from httplib2 import Http
from oauth2client import client, file, tools


def get_auth_google_drive_api():
    """
    This function use to get auth from google drive api
    """
    credentials_file_path = './credentials/credentials.json'
    clientsecret_file_path = './credentials/client_secret.json'

    # define scope
    SCOPE = 'https://www.googleapis.com/auth/drive'

    # define store
    store = file.Storage(credentials_file_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(clientsecret_file_path, SCOPE)
        credentials = tools.run_flow(flow, store)

    # define API service
    http = credentials.authorize(Http())
    drive = discovery.build('drive', 'v3', http=http)

    return drive


def retrieve_all_files(api_service, filename_to_search):
    results = []
    page_token = None
    check = 0
    while True:
        try:
            param = {}

            if page_token:
                param['pageToken'] = page_token

            files = api_service.files().list(**param).execute()
            # append the files from the current result page to our list
            results.extend(files.get('files'))
            # Google Drive API shows our files in multiple pages when the number of files exceed 100
            page_token = files.get('nextPageToken')

            if not page_token:
                break

        except errors.HttpError as error:
            print(f'An error has occurred: {error}')
            break
    # output the file metadata to console
    for file in results:
        if file.get('name') == filename_to_search:
            print(file)
            break
        else:
            check = 1
    if check == 1:
        print("Error")

    return results, file


if __name__ == "__main__":
    drive = get_auth_google_drive_api()
    all_files = retrieve_all_files(drive, "asd")
