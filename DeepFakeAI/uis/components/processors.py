from typing import List, Optional
import gradio

import DeepFakeAI.globals
from DeepFakeAI import wording
from DeepFakeAI.processors.frame.core import load_frame_processor_module, clear_frame_processors_modules
from DeepFakeAI.uis import core as ui
from DeepFakeAI.uis.typing import Update
from DeepFakeAI.utilities import list_module_names

FRAME_PROCESSORS_CHECKBOX_GROUP : Optional[gradio.CheckboxGroup] = None


def render() -> None:
	global FRAME_PROCESSORS_CHECKBOX_GROUP

	with gradio.Box():
		FRAME_PROCESSORS_CHECKBOX_GROUP = gradio.CheckboxGroup(
			label = wording.get('frame_processors_checkbox_group_label'),
			choices = sort_frame_processors(DeepFakeAI.globals.frame_processors),
			value = DeepFakeAI.globals.frame_processors
		)
		ui.register_component('frame_processors_checkbox_group', FRAME_PROCESSORS_CHECKBOX_GROUP)


def listen() -> None:
	FRAME_PROCESSORS_CHECKBOX_GROUP.change(update_frame_processors, inputs = FRAME_PROCESSORS_CHECKBOX_GROUP, outputs = FRAME_PROCESSORS_CHECKBOX_GROUP)


def update_frame_processors(frame_processors : List[str]) -> Update:
	clear_frame_processors_modules()
	DeepFakeAI.globals.frame_processors = frame_processors
	for frame_processor in DeepFakeAI.globals.frame_processors:
		frame_processor_module = load_frame_processor_module(frame_processor)
		frame_processor_module.pre_check()
	return gradio.update(value = frame_processors, choices = sort_frame_processors(frame_processors))


def sort_frame_processors(frame_processors : List[str]) -> list[str]:
	frame_processors_names = list_module_names('DeepFakeAI/processors/frame/modules')
	return sorted(frame_processors_names, key = lambda frame_processor : frame_processors.index(frame_processor) if frame_processor in frame_processors else len(frame_processors))
