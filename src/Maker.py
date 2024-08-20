from src import Components
import os
import typer

app = typer.Typer()

@app.command()
def maker(total_duration: int, mainTitle: str, scdTitle: str):
    input_folder = os.path.join("medias")
    output_folder = os.path.join("output", "vid.mp4")
    duration_per_image = 6
    video = Components.concatMedias(input_folder, duration_per_image, total_duration, mainTitle, scdTitle)
    video.write_videofile(output_folder, codec="libx264", fps=24)

if __name__ == "__main__":
    app()