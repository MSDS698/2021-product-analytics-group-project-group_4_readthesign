import json
import subprocess


def read_json(file):
    '''
    Reads in json file containing pairs of url:label
     for every video to download
    '''
    with open(file, 'r') as f:
        data = json.load(f)

    return data


def download_one(url, label):
    '''
    Runs the youtube-dl tool to download a single video
    into a subdirectory named with its label
    '''
    subprocess.run(
        ['youtube-dl',
         '-o', f'"videos/{label}/%(title)s.mp4"',
         '-f', 'mp4',
         url])


def download_all(data):
    '''Downloads all videos from the url keys in data'''
    for url, label in data.items():
        download_one(url, label)


if __name__ == '__main__':
    data = read_json('videos.json')
    download_all(data)
