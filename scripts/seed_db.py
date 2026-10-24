from datetime import datetime, timezone

from app.db import site_db
from app.models import Post, Project

REAL_PROJECTS = (
    Project(
        slug="classifying-classical-composers",
        title="Classifying Classical Composers with a CNN-LSTM Model",
        description=(
            "A hybrid CNN-LSTM model that names the composer behind a piece of "
            "classical music from raw MIDI data — 97%+ accuracy across four composers."
        ),
        body=(
            "Team project for AAI-511 (Neural Networks and Deep Learning) at the "
            "University of San Diego, built with Anitra Hernandez and Lakshmi Deepti "
            "Pamula. The question: given a piece of music, can a model learn to tell "
            "Bach from Beethoven from Chopin from Mozart — not from a recording, but "
            "from the raw MIDI data underneath it.\n\n"
            "The dataset (Kaggle's midi_classic_music) was badly imbalanced — about "
            "1,020 Bach files against roughly 250 Mozart, 215 Beethoven, and 140 "
            "Chopin. We tokenized each composer's files with a REMI tokenizer, used "
            "pitch/velocity/duration augmentation to even out the underrepresented "
            "composers, then downsampled everyone to 100 files to keep the classes "
            "balanced. From there, each MIDI file was rendered to audio with "
            "FluidSynth, converted to a mel-spectrogram with librosa, and sliced into "
            "time-step images — turning the music into something a CNN could actually "
            "look at.\n\n"
            "The model itself combines both architectures: four convolutional layers "
            "pull feature maps out of each spectrogram image, which then feed into an "
            "LSTM instead of a standard fully-connected head, so the model learns how "
            "those features change across time rather than treating each slice in "
            "isolation. A linear layer and softmax over the four composers close it out.\n\n"
            "Trained on 240 images and tested on 80 held-out ones, the combined model "
            "hit accuracy, precision, recall, and F1 all above 97%, missing only two "
            "files. To check that the hybrid design was actually earning its keep, we "
            "also built standalone CNN and LSTM baselines: the CNN alone reached ~90%, "
            "and the LSTM alone started at a rough 38% until real optimization work — "
            "packed sequences instead of manual padding, a second bidirectional layer, "
            "gradient clipping — brought it up to 90% too. The combined CNN-LSTM still "
            "beat both outright, heavier preprocessing and all."
        ),
        url="https://github.com/mr-kelsey/su25-aai511-group6",
        report_pdf="/static/projects/classifying-classical-composers-report.pdf",
        created_at=datetime.now(timezone.utc).isoformat(),
    ),
)

PLACEHOLDER_POSTS = (
    Post(
        slug="placeholder-post",
        title="Placeholder Post",
        body="Real posts are added in the content pass (PLAN.md step 9).",
        created_at=datetime.now(timezone.utc).isoformat(),
    ),
)


def seed() -> None:
    for project in REAL_PROJECTS:
        site_db.projects.insert(project)
    for post in PLACEHOLDER_POSTS:
        site_db.posts.insert(post)


if __name__ == "__main__":
    seed()
