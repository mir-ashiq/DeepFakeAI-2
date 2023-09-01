import gradio as gr
import subprocess as sp
import os
import uuid
import time
import shutil

os.makedirs("./output", exist_ok=True)

def run(*args):
    source, target, unique_id, *rest_args = args
    if not os.path.exists(source):
        return "Source file does not exist"
    if not os.path.exists(target):
        return "Target file does not exist"
    remove_old_directories("./output", num_minutes=60)
    filename = os.path.basename(target)
    os.makedirs(f"./output/{unique_id}",exist_ok=True)
    output = f"./output/{unique_id}/{filename}"
    frame_processor = rest_args[0]
    selected_frame_processors = ' '.join(frame_processor)

    face_analyser_direction = rest_args[1]
    face_recognition = rest_args[2]
    face_analyser_gender = rest_args[3]

    cmd = (
        f"python run.py --execution-providers cpu -s {source} -t {target} -o {output} "
        f"--frame-processors {selected_frame_processors} "
        f"--face-analyser-direction {face_analyser_direction} "
    )
    if face_recognition != 'none':
        cmd += f"--face-recognition {face_recognition} "
    if face_analyser_gender != 'none':
        cmd += f"--face-analyser-gender {face_analyser_gender} "

    if len(rest_args) > 4:
        skip_audio = rest_args[4]
        keep_fps = rest_args[5]
        keep_temp = rest_args[6]
        if skip_audio:
            cmd += "--skip-audio "
        if keep_fps:
            cmd += "--keep-fps "
        if keep_temp:
            cmd += "--keep-temp "

    try:
        print("Started...", cmd)
        output_text = sp.run(cmd, shell=True, capture_output=True, text=True).stdout
        print(output_text)
        return output
    except Exception as e:
        return f"An error occurred: {str(e)}"

def clear_output(unique_id):
    try:
        output_path = f"./output/{unique_id}"
        if os.path.exists(output_path):
            print("Trying to delete ")
            for filename in os.listdir(output_path):
                file_path = os.path.join(output_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Output files in {output_path} are deleted")
                    return "Output files for unique_id deleted"
                else:
                    print(f"Output files in {output_path} does not exist")
                    return "Output directory for (output_path} does not exist"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def remove_old_directories(directory, num_minutes=60):
    now = time.time()

    for r, d, f in os.walk(directory):
        for dir_name in d:
            dir_path = os.path.join(r, dir_name)
            timestamp = os.path.getmtime(dir_path)
            age_minutes = (now - timestamp) / 60 # Convert to minutes
            
            if age_minutes >= num_minutes:
                try:
                    print("Removing", dir_path)
                    shutil.rmtree(dir_path)
                    print("Directory removed:", dir_path)
                except Exception as e:
                    print(e)
                    pass

def get_theme() -> gr.Theme:
    return gr.themes.Soft(
        primary_hue = gr.themes.colors.red,
        secondary_hue = gr.themes.colors.gray,
        font = gr.themes.GoogleFont('Inter')
    ).set(
        background_fill_primary = '*neutral_50',
        block_label_text_size = '*text_sm',
        block_title_text_size = '*text_sm'
    )

with gr.Blocks(theme=get_theme(), title="DeepFakeAI 1.0.0") as ui:
    with gr.Box():
        gr.HTML('<center><a href="codegenius.me">DeepFakeAI 1.0.1</a></center>')

    with gr.Box():
        with gr.Column(scale=3):
           frame_processor_checkbox = gr.CheckboxGroup(
            choices = ['face_swapper', 'face_enhancer', 'frame_enhancer'],
            label = 'FRAME PROCESSORS',
            value = ['face_swapper']  # Default value
        )

    
    with gr.Box():
        with gr.Column(scale=3):
            face_analyser_direction_dropdown = gr.Dropdown(
                label = 'FACE ANALYSER DIRECTION',
                choices = ['left-right', 'right-left', 'top-bottom', 'bottom-top', 'small-large', 'large-small'],
                value = 'left-right'
            )
            face_analyser_age_dropdown = gr.Dropdown(
                label = 'FACE RECOGNITION',
                choices = ['none'] + ['reference', 'many'],
                value = 'reference'
            )
            face_analyser_gender_dropdown = gr.Dropdown(
                label = 'FACE ANALYSER GENDER',
                choices = ['none'] + ['male', 'female'],
                value = 'none'
            )
            unique_id = gr.Textbox(value=str(uuid.uuid4()), visible=False)
    with gr.Tab("Image:               "):
        source_image = gr.Image(type="filepath", label="SOURCE IMAGE")
        target_image = gr.Image(type="filepath", label="TARGET IMAGE")
        image_button = gr.Button("START")
        clear_button = gr.ClearButton(value="CLEAR")
        image_output = gr.Image(label="OUTPUT")
        clear_button.add(image_output)

        image_button.click(
            run,
            inputs=[source_image, target_image, unique_id, frame_processor_checkbox, face_analyser_direction_dropdown, face_analyser_age_dropdown, face_analyser_gender_dropdown],
            outputs=image_output
        )
        clear_button.click(fn=clear_output, inputs=unique_id)

    with gr.Tab("Video:               "):
        source_image_video = gr.Image(type="filepath", label="SOURCE IMAGE")
        target_video = gr.Video(label="TARGET VIDEO")
        with gr.Box():
            skip_audio = gr.Checkbox(label="SKIP AUDIO")
            keep_fps = gr.Checkbox(label="KEEP FPS")
            keep_temp = gr.Checkbox(label="KEEP TEMP")
        video_button = gr.Button("START")
        clear_video_button = gr.ClearButton(value="CLEAR")
        video_output = gr.Video(label="OUTPUT")
        clear_video_button.add(video_output)
        video_button.click(
            run,
            inputs=[source_image_video, target_video, unique_id, frame_processor_checkbox, face_analyser_direction_dropdown, face_analyser_age_dropdown, face_analyser_gender_dropdown, skip_audio, keep_fps, keep_temp],
            outputs=video_output
        )
        clear_video_button.click(fn=clear_output, inputs=unique_id)

ui.launch(debug=True)
