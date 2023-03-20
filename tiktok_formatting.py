from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.resize import resize
from moviepy.video.fx.all import crop

def format_video(input_video_path, output_video_path):

    # Set up the parameters for the video
    #width = 1080
    #height = 1920
    background_color = (0, 0, 0)

    # Load the input video clip using VideoFileClip
    video_clip = VideoFileClip(input_video_path)
    width, height = video_clip.size
    crop_width = height * 9/16
    x1, x2 = (width - crop_width)//2, (width +crop_width)//2
    y1, y2 = 0, height
    # If the aspect ratio of the input video clip is different from 9:16 (1080x1920), crop the video clip to fit
    if video_clip.aspect_ratio != 9/16:
        cropped_clip = crop(video_clip, x1=x1, y1=y1, x2=x2, y2=y2)
    else:
        cropped_clip = video_clip

    # Create a color clip with the same dimensions as the video clip using ColorClip
    #background_clip = ColorClip(size=(width, height), color=background_color)

    # Composite the cropped video clip and the background clip using CompositeVideoClip
    #final_clip = CompositeVideoClip([background_clip, cropped_clip.set_pos("center")])
    #final_clip.duration = video_clip.duration

    # Write the final clip to a new file using write_videofile
    cropped_clip.write_videofile(output_video_path)

    # Cleanup by closing the clips
    video_clip.close()
    cropped_clip.close()

if __name__ == "__main__":
    input_video_path = "data/videos/03_18_23_sillycats.mp4"
    output_video_path = input_video_path.replace(".mp4", "_final.mp4")
    format_video(input_video_path, output_video_path)