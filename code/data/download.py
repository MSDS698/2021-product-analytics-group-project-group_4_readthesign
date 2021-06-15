import json
import subprocess


def read_json(file):
    '''
    Reads in json file containing pairs of label:[urls,...]
     for every video to download
    '''
    with open(file, 'r') as f:
        data = json.load(f)

    return data


def download_one_label(label, urls):
    '''
    Runs the youtube-dl tool to download videos for one label
    into a subdirectory named with their label
    '''
    for i, url in enumerate(urls):
        subprocess.run(
            ['youtube-dl',
             '-o', f'videos/{label}/{label}_{i}.mp4',
             '-f', 'mp4',
             url])


def download_all_labels(data):
    '''Downloads all videos from the url keys in data'''
    for label, urls in data.items():
        download_one_label(label, urls)


if __name__ == '__main__':
    data = read_json('videos.json')
    download_all_labels(data)
