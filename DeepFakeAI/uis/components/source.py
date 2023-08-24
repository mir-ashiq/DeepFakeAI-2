from typing import Any, IO, Optional
import gradio

import DeepFakeAI.globals
from DeepFakeAI import wording
from DeepFakeAI.uis import core as ui
from DeepFakeAI.uis.typing import Update
from DeepFakeAI.utilities import is_image

SOURCE_FILE : Optional[gradio.File] = None
SOURCE_IMAGE : Optional[gradio.Image] = None


def render() -> None:
	global SOURCE_FILE
	global SOURCE_IMAGE

	with gradio.Box():
		is_source_image = is_image(DeepFakeAI.globals.source_path)
		SOURCE_FILE = gradio.File(
			file_count = 'single',
			file_types=
			[
				'.png',
				'.jpg',
				'.webp'
			],
			label = wording.get('source_file_label'),
			value = DeepFakeAI.globals.source_path if is_source_image else None
		)
		ui.register_component('source_file', SOURCE_FILE)
		SOURCE_IMAGE = gradio.Image(
			value = SOURCE_FILE.value['name'] if is_source_image else None,
			visible = is_source_image,
			show_label = False
		)


def listen() -> None:
	SOURCE_FILE.change(update, inputs = SOURCE_FILE, outputs = SOURCE_IMAGE)


def update(file: IO[Any]) -> Update:
	if file and is_image(file.name):
		DeepFakeAI.globals.source_path = file.name
		return gradio.update(value = file.name, visible = True)
	DeepFakeAI.globals.source_path = None
	return gradio.update(value = None, visible = False)
