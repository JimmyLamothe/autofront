import sys
sys.path.insert(1, '/Users/jimmy/Programming/Python/spotify')
import autofront, Player

player = Player.Player()

func_dicts = [{'function':player.play_next_album, 'link':'playnext', 'title':'Play next album'},
              {'function':player.play_current_album, 'link':'playcurrent', 'title':'Play current album'},
              {'function':player.play_next_track, 'link':'nexttrack', 'title':'Play next track'},
              {'function':player.play_previous_track, 'link':'prevtrack', 'title':'Play previous track'},
              {'function':player.show_current_track, 'link':'showcurrent', 'title':'Show current track'},
              {'function':player.play_random_album, 'link':'playrandom', 'title':'Play random album'},
              {'function':player.stop, 'link':'stop', 'title':'Stop play'},
              {'function':player.follow, 'link':'follow', 'title':'Follow current artist'},
              {'function':player.unfollow, 'link':'unfollow', 'title':'Unfollow current artist'}]

for dic in func_dicts:
    autofront.create_route(autofront.app, dic['function'], link = dic['link'], title = dic['title'])

#print(autofront.app.url_map)

autofront.app.run(host='0.0.0.0', port = 5000)
