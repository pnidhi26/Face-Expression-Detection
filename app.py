import os
import os.path
from os import path
import random
import shutil 
from modules import videoframe
from modules import expression
# from models import videocheck
from modules import fmidtrans
from modules import videoinfo
from modules import videoresize
from flask import send_from_directory
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, make_response, render_template, send_file, redirect


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


rand_min = 10000
rand_max = 99999
transition_id_strings = 18

#Face Expression API
@app.route('/face_expression_api', methods=['POST']) 
def face_exp():

	""" Recieve the video file and save it in upload folder with random number unique identity """
	fm_transaction_id = request.form['finmomenta_transaction_id']
	# vendor_id = request.form['vendor_id']

	""" transaction id generator for API hits """
	trans_id = fmidtrans.transition_id_generator(transition_id_strings)

	""" Response Structure globaly declaration """
	result1 = {}
	result1['code'] = 4001
	result1['status'] = 'Success'
	result1['description']  = 'Your face expressions is captured.'
	result1['client_transaction_id'] = trans_id
	result1['finmomenta_transaction_id'] = fm_transaction_id
	result1['expression_response'] = []

	result2 = {}
	result2['code'] = 4011
	result2['status'] = 'failure'
	result2['description']  = 'Not able to proceed, due to poor video quality. try again.'
	result2['client_transaction_id'] = trans_id
	result2['finmomenta_transaction_id'] = fm_transaction_id
	result2['expression_response'] = []

	result3 = {}
	result3['code'] = 4012
	result3['status'] = 'failure'
	result3['description']  = 'Invalid Request. Please upload one video file'
	result3['client_transaction_id'] = trans_id
	result3['finmomenta_transaction_id'] = fm_transaction_id
	result3['expression_response'] = []

	result4 = {}
	result4['code'] = 4013
	result4['status'] = 'failure'
	result4['description']  = 'Invalid file format. Only .avi and .mp4 formats are allowed'
	result4['client_transaction_id'] = trans_id
	result4['finmomenta_transaction_id'] = fm_transaction_id
	result4['expression_response'] = []

	result5 = {}
	result5['code'] = 4014
	result5['status'] = 'failure'
	result5['description']  = 'More than 20-second video is not acceptable.'
	result5['client_transaction_id'] = trans_id
	result5['finmomenta_transaction_id'] = fm_transaction_id
	result5['expression_response'] = []

	path = []

	target = os.path.join(APP_ROOT, "upload")
	if not os.path.isdir(target):
			os.mkdir(target)
	else:
		pass

	for upload in request.files.getlist("file"):
		if len(upload.filename) != 0:
			filename = str(random.randrange(rand_min, rand_max)) + "_" + upload.filename
			destination = "/".join([target, filename])
			upload.save(destination)

			""" Check the file formats """
			name, extension = os.path.splitext(filename)
			ext = extension.lower()
			if ext == ".avi" or ext == ".mp4":
				path.append(filename)
			else:
				os.remove("upload/"+ filename)
				return jsonify(result4)


	""" checking the input parameters """
	if len(path) != 1:
		os.remove("upload/"+path[0])
		return jsonify(result3)
	else:
		pass


	""" Checking the video length (duration) """
	vidlen = videoinfo.getDuration("upload/"+path[0])
	if vidlen > 20:
		os.remove("upload/"+path[0])
		return jsonify(result5)
	else:
		pass

	""" Checking the face emotions """
	try:
		exp = expression.face_expression("upload/"+path[0])
		os.remove("upload/"+path[0])
		result1['expression_response'].append(exp)
		return jsonify(result1)

	except:
		os.remove("upload/"+path[0])
		return jsonify(result2)

	# """ check the frame per second and define that video is capture via mobile phone or laptop """
	# fps_info = videoinfo.VideoInfo("upload/"+path[0])
	# print(fps_info)

	# """ If video is captured by mobile phone mostly having more than 14 fps """
	# if fps_info[0] >= 14:
	# 	video = "upload/"+path[0]
	# 	output_path = video[:-4]+'_.mp4'
	# 	try:
	# 		""" Rotating the mobile recorded video file in ffmpeg
	# 		and fixing fps value is 14 for all inputs. """
	# 		vc = videocheck.video_check(video, output_path, '14')

	# 		""" Resize the video into 512*620 pixels """
	# 		fc = videoresize.video_resize(output_path)
	# 		""" Cheking expression on face """
	# 		exp = expression.face_expression(fc)
	# 		os.remove("upload/"+path[0])
	# 		os.remove(fc)
	# 		result1['expression_response'].append(exp)
	# 		return jsonify(result1)

	# 	except:
	# 		os.remove("upload/"+path[0])
	# 		return jsonify(result2)

	# elif fps_info[0] < 14:
	# 	try:
	# 		exp = expression.face_expression("upload/"+path[0])
	# 		os.remove("upload/"+path[0])
	# 		result1['expression_response'].append(exp)
	# 		return jsonify(result1)

	# 	except:
	# 		os.remove("upload/"+path[0])
	# 		return jsonify(result2)

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4555, debug=True)

