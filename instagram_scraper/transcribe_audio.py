#!/usr/bin/env python3
"""
Audio Transcription Script using Whisper

This script transcribes audio files using OpenAI's Whisper model.
"""

import os
import json
import argparse
import whisper
from pathlib import Path


def transcribe_audio(audio_path, model_name="base", output_dir="transcripts"):
    """
    Transcribe an audio file using Whisper.
    
    Args:
        audio_path (str): Path to the audio file
        model_name (str): Whisper model to use (tiny, base, small, medium, large)
        output_dir (str): Directory to save the transcript
        
    Returns:
        dict: Transcription result
    """
    if not os.path.exists(audio_path):
        print(f"Audio file not found: {audio_path}")
        return {"error": "Audio file not found"}
    
    audio_path = Path(audio_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    transcript_path = output_dir / f"{audio_path.stem}_whisper_transcript.json"
    
    print(f"Loading Whisper model: {model_name}")
    try:
        # Load the Whisper model
        model = whisper.load_model(model_name)
        
        print(f"Transcribing audio: {audio_path}")
        # Transcribe the audio
        result = model.transcribe(str(audio_path))
        
        # Extract the transcript
        transcript = {
            "text": result["text"],
            "segments": result["segments"],
            "language": result["language"]
        }
        
        # Save the transcript
        with open(transcript_path, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, indent=2)
        
        print(f"Transcript saved: {transcript_path}")
        return transcript
    
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return {"error": str(e)}


def main():
    """Parse arguments and run the transcription."""
    parser = argparse.ArgumentParser(description='Transcribe audio using Whisper')
    parser.add_argument('audio_path', help='Path to the audio file')
    parser.add_argument('--model', default='base', 
                        choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help='Whisper model to use (default: base)')
    parser.add_argument('--output-dir', default='transcripts',
                        help='Directory to save the transcript (default: transcripts)')
    
    args = parser.parse_args()
    
    transcript = transcribe_audio(args.audio_path, args.model, args.output_dir)
    
    if "error" in transcript:
        print(f"Error: {transcript['error']}")
    else:
        print("\nTranscription completed!")
        print(f"Full transcript: {transcript['text']}")


if __name__ == "__main__":
    main()
