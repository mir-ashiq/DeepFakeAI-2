from typing import Any, IO, Tuple, Optional
import gradio

import DeepFakeAI.globals
from DeepFakeAI import wording
from DeepFakeAI.face_reference import clear_face_reference
from DeepFakeAI.uis import core as ui
from DeepFakeAI.uis.typing import Update
from DeepFakeAI.utilities import is_image, is_video

TARGET_FILE : Optional[gradio.File] = None
TARGET_IMAGE : Optional[gradio.Image] = None
TARGET_VIDEO : Optional[gradio.Video] = None


def render() -> None:
	global TARGET_FILE
	global TARGET_IMAGE
	global TARGET_VIDEO

	with gradio.Box():
		is_target_image = is_image(DeepFakeAI.globals.target_path)
		is_target_video = is_video(DeepFakeAI.globals.target_path)
		TARGET_FILE = gradio.File(
			label = wording.get('target_file_label'),
			file_count = 'single',
			file_types =
			[
				'.png',
				'.jpg',
				'.webp',
				'.mp4'
			],
			value = DeepFakeAI.globals.target_path if is_target_image or is_target_video else None
		)
		TARGET_IMAGE = gradio.Image(
			value = TARGET_FILE.value['name'] if is_target_image else None,
			visible = is_target_image,
			show_label = False
		)
		TARGET_VIDEO = gradio.Video(
			value = TARGET_FILE.value['name'] if is_target_video else None,
			visible = is_target_video,
			show_label = False
		)
		ui.register_component('target_file', TARGET_FILE)


def listen() -> None:
	TARGET_FILE.change(update, inputs = TARGET_FILE, outputs = [ TARGET_IMAGE, TARGET_VIDEO ])


def update(file : IO[Any]) -> Tuple[Update, Update]:
	clear_face_reference()
	if file and is_image(file.name):
		DeepFakeAI.globals.target_path = file.name
		return gradio.update(value = file.name, visible = True), gradio.update(value = None, visible = False)
	if file and is_video(file.name):
		DeepFakeAI.globals.target_path = file.name
		return gradio.update(value = None, visible = False), gradio.update(value = file.name, visible = True)
	DeepFakeAI.globals.target_path = None
	return gradio.update(value = None, visible = False), gradio.update(value = None, visible = False)
