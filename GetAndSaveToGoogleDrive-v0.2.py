from __future__ import print_function
import sys
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive'

def get_dl_links():
    q_dic = {'y': True, 'n': False, 'yes': True, 'no': False}
    links = []

    while True:
        link_input = input('Please Input DL Link >> ').strip()
        links.append(link_input)

        try:
            question   = q_dic[input('Continue?([Y]es/[N]o?) >> ').lower()]
            if question == False:
                break
        except:
            pass

    return links

def get_creds():
    store = file.Storage('./gdrivetoken.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow  = client.flow_from_clientsecrets('./gdrivecredentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    return creds

def get_service():
    creds   = get_creds()
    service = build('drive', 'v3', http=creds.authorize(Http()))

    return service

def get_folder_id():
    service = get_service()

    folder_name = 'Python_Save'
    folder_mime = 'application/vnd.google-apps.folder'

    folder_query_name = 'name="' + folder_name + '"'
    folder_query_mime = 'mimeType="' + folder_mime + '"'

    folder_metadata = {
        'name': folder_name,
        'mimeType': folder_mime
    }

    results = service.files().list(
        q=folder_query_name, fields='nextPageToken, files(id, name)').execute();

    folder_id = ''
    folders   = results.get('files', [])

    if not folders:
        print('Folder does not exist')
        print('Creating the folder...')

        create_folder = service.files().create(
            body=folder_metadata, fields='id, name').execute()

        new_folder_name = create_folder.get('name')
        new_folder_id   = create_folder.get('id')

        print(u'Name: {0}'.format(new_folder_name))
        print(u'ID  : {0}'.format(new_folder_id))

        folder_id = new_folder_id
    else:
        for folder in folders:
            print(u'Name: {0}'.format(folder['name']))
            print(u'ID  : {0}'.format(folder['id']))

            folder_id = folder['id']
            break;

    return folder_id

def main():
    folder_id = get_folder_id()
    service   = get_service()
    dl_links  = get_dl_links()

    for dl_link in dl_links:
        req = requests.get(dl_link)
        req_file_content = req.content
        req_file_type    = req.headers['Content-Type']
        req_file_name    = dl_link[dl_link.rfind('/') + len('/'):]

        insert_metadata = {
            'name'   : req_file_name,
            'parents': [folder_id]
        }

        tmpfilename = '/tmp/' + req_file_name
        with open(tmpfilename, 'wb') as s:
            s.write(req_file_content)

        insert_media = MediaFileUpload(tmpfilename, mimetype=req_file_type)
        insert_file  = service.files().create(
            body=insert_metadata, media_body=insert_media, fields='id').execute()
        print(u'File Id: {0}'.format(insert_file.get('id')))

if __name__ == '__main__':
    main()
