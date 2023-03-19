from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import os

def generate(input_video_path, image_path, output_path):
    # Load the input video and the image
    video_clip = VideoFileClip(input_video_path)
    image_clip = ImageClip(image_path)

    # Calculate the midpoint of the video
    midpoint = video_clip.duration / 2

    # Set the duration of the image clip to be the same as the duration of the video clip
    image_clip = image_clip.set_duration(video_clip.duration)

    # Position the image clip in the center of the video clip
    image_clip = image_clip.set_position(("center", "center"))

    # Create a composite video clip by overlaying the image clip on top of the video clip at the midpoint
    composite_clip = CompositeVideoClip([video_clip, image_clip.set_start(midpoint)], size=video_clip.size)

    # Set up the output file path and write the composite clip to the output file
    
    composite_clip.write_videofile(output_path)

    # Cleanup by closing the clips
    video_clip.close()
    image_clip.close()
    composite_clip.close()

if __name__ == "__main__":
    # Set up the input video file path and image file path
    input_video_path = "PATH_TO_INPUT_VIDEO.mp4"
    image_path = "PATH_TO_IMAGE.jpg"
    output_path = "PATH_TO_OUTPUT_VIDEO.mp4"
    generate(input_video_path, image_path, output_path)