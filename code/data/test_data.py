import os
from download import read_json, download_all_labels


def test_read():
    test_url = 'https://media.signbsl.com/videos/asl/startasl/mp4/hello.mp4'
    assert read_json('test.json') == {'hello': [test_url]}


def test_download_all_labels():
    data = read_json('test.json')
    download_all_labels(data)
    assert os.path.exists('videos/hello/hello_0.mp4')
