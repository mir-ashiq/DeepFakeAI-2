from time import sleep
from typing import Any, Dict, Tuple, Optional

import gradio

import DeepFakeAI.globals
from DeepFakeAI import wording
from DeepFakeAI.capturer import get_video_frame_total
from DeepFakeAI.uis import core as ui
from DeepFakeAI.uis.typing import Update
from DeepFakeAI.utilities import is_video

TRIM_FRAME_START_SLIDER : Optional[gradio.Slider] = None
TRIM_FRAME_END_SLIDER : Optional[gradio.Slider] = None


def render() -> None:
	global TRIM_FRAME_START_SLIDER
	global TRIM_FRAME_END_SLIDER

	with gradio.Box():
		trim_frame_start_slider_args : Dict[str, Any] = {
			'label': wording.get('trim_frame_start_slider_label'),
			'step': 1,
			'visible': False
		}
		trim_frame_end_slider_args : Dict[str, Any] = {
			'label': wording.get('trim_frame_end_slider_label'),
			'step': 1,
			'visible': False
		}
		if is_video(DeepFakeAI.globals.target_path):
			video_frame_total = get_video_frame_total(DeepFakeAI.globals.target_path)
			trim_frame_start_slider_args['value'] = DeepFakeAI.globals.trim_frame_start or 0
			trim_frame_start_slider_args['maximum'] = video_frame_total
			trim_frame_start_slider_args['visible'] = True
			trim_frame_end_slider_args['value'] = DeepFakeAI.globals.trim_frame_end or video_frame_total
			trim_frame_end_slider_args['maximum'] = video_frame_total
			trim_frame_end_slider_args['visible'] = True
		with gradio.Row():
			TRIM_FRAME_START_SLIDER = gradio.Slider(**trim_frame_start_slider_args)
			TRIM_FRAME_END_SLIDER = gradio.Slider(**trim_frame_end_slider_args)


def listen() -> None:
	target_file = ui.get_component('target_file')
	if target_file:
		target_file.change(remote_update, outputs = [ TRIM_FRAME_START_SLIDER, TRIM_FRAME_END_SLIDER ])
	TRIM_FRAME_START_SLIDER.change(lambda value : update_number('trim_frame_start', int(value)), inputs = TRIM_FRAME_START_SLIDER, outputs = TRIM_FRAME_START_SLIDER)
	TRIM_FRAME_END_SLIDER.change(lambda value : update_number('trim_frame_end', int(value)), inputs = TRIM_FRAME_END_SLIDER, outputs = TRIM_FRAME_END_SLIDER)


def remote_update() -> Tuple[Update, Update]:
	sleep(0.1)
	if is_video(DeepFakeAI.globals.target_path):
		video_frame_total = get_video_frame_total(DeepFakeAI.globals.target_path)
		DeepFakeAI.globals.trim_frame_start = 0
		DeepFakeAI.globals.trim_frame_end = video_frame_total
		return gradio.update(value = 0, maximum = video_frame_total, visible = True), gradio.update(value = video_frame_total, maximum = video_frame_total, visible = True)
	return gradio.update(value = None, maximum = None, visible = False), gradio.update(value = None, maximum = None, visible = False)


def update_number(name : str, value : int) -> Update:
	setattr(DeepFakeAI.globals, name, value)
	return gradio.update(value = value)
