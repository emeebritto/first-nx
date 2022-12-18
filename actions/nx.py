# module center
from actions.downloads import dlvideoyt, dlmusicyt, dlRedditVid, req_media
from actions.downloads import dlMusicByQuery, dlVideoByQuery, dlMusicVideoByQuery
from actions.search import searchVideo, searchSummary
from actions.remote import play_sound, stop_sound, pause_sound, resume_sound
from actions.room import create_key, list_keys, del_key
from actions.take_test import take_test
from actions.qr_code import create_qr_code, read_qr_code
from actions.pronounce_words import *
from actions.send_image import *
from actions.talk import talk
from actions.generate_data import generate_cpf, generate_real_cpf
from actions.image import whatIsOnTheImage
from actions.examples import send_commands_examples
