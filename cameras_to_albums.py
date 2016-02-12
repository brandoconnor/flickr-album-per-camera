#!/usr/bin/env python

"""
A simple script to organize photos into albums named by their camera source.
For me, this is useful for cycling through only high quality photos on my TV
hooked up to a chromecast.
"""

import flickrapi
import argparse


def auth_flickr(api_key, api_secret):
    """Authenticate user to flickr API."""
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
    flickr.authenticate_via_browser(perms='write')
    return flickr


def get_user_id(flickr, user):
    """Get the user_id from the username."""
    user_data = flickr.people.findByUsername(username=user)
    return user_data['user']['id']


def get_photoset_dict(flickr, user_id):
    """construct a photoset dict of album name to album/set id."""
    print('Gathering dictionary of all photos in all photosets...')
    init_photoset = flickr.photosets.getList(user_id=user_id)
    photoset_dict = dict()
    set_num = 1
    for set_page in range(1, init_photoset['photosets']['pages'] + 1):
        photoset = flickr.photosets.getList(user_id=user_id, page=set_page)
        for pset in photoset['photosets']['photoset']:
            print('processing photoset %s of %s' % (set_num, init_photoset['photosets']['total']))
            set_num += 1
            # a_dict = {'thing': {'this': ['list, 'values']} }
            photoset_dict[pset['title']['_content']] = {pset['id']: []}
            init_photoset_object = flickr.photosets.getPhotos(photoset_id=pset['id'])
            for photoset_page in range(1, init_photoset_object['photoset']['pages'] + 1):
                photoset_object = flickr.photosets.getPhotos(user_id=user_id, photoset_id=pset['id'], page=photoset_page)
                photoset_dict[pset['title']['_content']][pset['id']] += [p['id'] for p in photoset_object['photoset']['photo']]
    return photoset_dict


def main(args):
    """Main code block. Do all the things."""
    flickr = auth_flickr(args.api_key, args.api_secret)
    user_id = get_user_id(flickr, user=args.username)
    album_dict = get_photoset_dict(flickr, user_id)
    init_photos = flickr.people.getPhotos(user_id=user_id)
    total = init_photos['photos']['total']
    photo_num = args.initial_photo / 100 * 100 # TODO ensure less than total photos
    if photo_num > total:
        raise('Trying to start at photo %s but only %s total. Exiting.' % (args.initial_photo, total))
    init_page = args.initial_photo / 100 + 1 # 100 photos per page
    for page_num in range(init_page, init_photos['photos']['pages'] + 1):
        photo_batch = flickr.people.getPhotos(user_id=user_id, page=page_num)
        for photo in photo_batch['photos']['photo']:
            photo_num += 1
            photo_id = photo['id']
            print('processing photo %s of %s: %s' % (photo_num, total, photo_id))
            photo_data = flickr.photos.getExif(photo_id=photo_id)
            camera_name = photo_data['photo']['camera']
            if len(camera_name) > 0:
                if camera_name not in album_dict.keys():
                    print('adding camera album "%s"' % camera_name)
                    new_set = flickr.photosets.create(title=camera_name,
                                                      primary_photo_id=photo_id,
                                                      description='All photos taken behind a %s' % camera_name)
                    album_dict[camera_name] = {new_set['photoset']['id'] : [photo_id]}
                    continue
                elif photo_id not in [p for p in album_dict[camera_name].values()[0]]:
                    # if this photo is not in the appropriate album, add it
                    print('Adding photo to camera album.')
                    flickr.photosets.addPhoto(photoset_id=album_dict[camera_name].keys()[0], photo_id=photo_id)
                    album_dict[camera_name].values()[0].append(photo_id)
                else:
                    print('Photo is already in the appropriate set')
                    continue
            else:
                print('Skipping photo with insufficient metadata.')


if __name__ in '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dry_run', action='store_true',
                        default=False, help="Verbose minus action. Default=False")
    parser.add_argument('-i', '--initial_photo', help='approximate initial photo. Rounds down to nearest hundred',
                         type=int, default=0)
    parser.add_argument('-k', '--api_key', help='flickr API key', required=True)
    parser.add_argument('-s', '--api_secret', help='flickr API secret', required=True)
    parser.add_argument('-u', '--username', help='your flickr username', required=True)
    exit(main(parser.parse_args()))
