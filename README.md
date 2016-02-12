## Synopsis

This is a dead simple script that sorts a user's flickr photos into an album of the camera name it was taken by according to its EXIF data.

## Motivation

This project was written because Flickr's organize interface has no option to sort and categorize photos by camera type. Chromecast now has the ability when idling to cycle through all photos of a flickr album. I wanted to cycle through only those photos taken with DSLR cameras so organizing by camera source (via EXIF data) was my only option. Poof! This script is born.

## Installation
Use of this script assumes you have a flickr account, photos to be organized, and have [requested a noncommercial API key](https://www.flickr.com/services/apps/create/noncommercial/?).

```
> mkvirtualenv flickr-album-per-camera
> pip install -r requirements.txt
> python cameras_to_albums.py --help
usage: cameras_to_albums.py [-h] [-d] [-k API_KEY] [-s API_SECRET]
                            [-u USERNAME]

optional arguments:
  -h, --help            show this help message and exit
  -d, --dry_run         Verbose minus action. Default=False
  -k API_KEY, --api_key API_KEY
                        flickr API key
  -s API_SECRET, --api_secret API_SECRET
                        flickr API secret
  -u USERNAME, --username USERNAME
                        your flickr username
```

## Bugs / Development / Contributing
* Report issues/questions/feature requests on in the [Issues](https://github.com/brandoconnor/flickr-album-per-camera/issues) section.

Pull requests are welcome!
Ideally create a topic branch for every separate change you make.
For example:

1. Fork the repo
2. Create your feature branch (`git checkout -b my-new-feature`)
4. Commit your awesome changes (`git commit -am 'Added some feature'`)
5. Push to the branch (`git push origin my-new-feature`)
6. Create a new Pull Request and tell us about your changes.

## LICENSE
Licensed under the Apache License, Version 2.0 (the “License”); you may not use this file except in
compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is
distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing permissions and limitations under the
License.
