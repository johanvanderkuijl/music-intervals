import os
import random
import time
from typing import Dict

import pygame
from midiutil import MIDIFile


class IntervalTrainer:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()

        # Read and parse intervals from file
        self.intervals = self._load_intervals()

        # MIDI note numbers (60 = middle C)
        self.base_notes = list(range(48, 73))  # From C3 to C5

    def _load_intervals(self) -> Dict[str, int]:
        intervals = {}
        with open("intervals.txt", "r", encoding="utf-8") as f:
            for line in f:
                name, description = line.split(":", 1)
                # Only include specific intervals
                if any(
                    interval in name
                    for interval in [
                        "Prime",
                        "Grote Secunde",
                        "Grote Terts",
                        "Reine Kwart",
                        "Reine Kwint",
                    ]
                ):
                    if "Prime" in name:
                        semitones = 0
                    elif "Grote Secunde" in name:
                        semitones = 2
                    elif "Grote Terts" in name:
                        semitones = 4
                    elif "Reine Kwart" in name:
                        semitones = 5
                    elif "Reine Kwint" in name:
                        semitones = 7
                    intervals[name.strip()] = semitones
        return intervals

    def _create_midi_file(self, note1: int, note2: int, filename: str = "interval.mid"):
        midi = MIDIFile(1)  # One track
        midi.addTempo(0, 0, 120)

        # Add notes with longer duration (2 beats each instead of 1)
        midi.addNote(
            0, 0, note1, 0, 2, 100
        )  # track, channel, pitch, time, duration, volume
        midi.addNote(0, 0, note2, 2, 2, 100)  # start second note after first one ends

        # Save MIDI file
        with open(filename, "wb") as f:
            midi.writeFile(f)

    def play_interval(self, note1: int, note2: int):
        # Create and play MIDI file
        self._create_midi_file(note1, note2)
        pygame.mixer.music.load("interval.mid")
        pygame.mixer.music.play()
        # time.sleep(4)  # Increased wait time to match longer note duration

    def print_intervals(self, interval_names):
        # Create numbered list of intervals
        for i, name in enumerate(interval_names, 1):
            print(f"{i}. {name}")

    def run_quiz(self):
        print("Welkom bij de Interval Training!")
        print("Luister naar het interval en kies het juiste antwoord.")
        print("\nBeschikbare intervallen:")
        interval_names = list(self.intervals.keys())

        # Create quiz sequence with 20 random questions
        quiz_sequence = [random.choice(interval_names) for _ in range(20)]

        score = 0
        total = len(quiz_sequence)

        for interval_name in quiz_sequence:
            # Generate random starting note
            base_note = random.choice(self.base_notes)
            interval = self.intervals[interval_name]

            # Print available intervals for each question
            print("\nBeschikbare intervallen:")
            self.print_intervals(interval_names)

            # Get user input
            while True:
                try:
                    print(
                        "\nWelk interval hoor je? (voer het nummer in, of 0 om opnieuw te luisteren):"
                    )
                    self.play_interval(base_note, base_note + interval)
                    print("-> ", end="")
                    answer = int(input())
                    if answer == 0:
                        # Play the interval again
                        self.play_interval(base_note, base_note + interval)
                        continue
                    answer = answer - 1  # Adjust for 1-based indexing
                    if 0 <= answer < len(interval_names):
                        break
                    print("Ongeldige invoer. Kies een nummer uit de lijst.")
                except ValueError:
                    print("Voer een geldig nummer in.")

            # Check answer
            if interval_names[answer] == interval_name:
                print("Correct!")
                score += 1
            else:
                print(f"Helaas! Het juiste antwoord was: {interval_name}")

            print(f"\nScore: {score}/{total}")
            time.sleep(3)

        # Clean up
        if os.path.exists("interval.mid"):
            os.remove("interval.mid")


if __name__ == "__main__":
    trainer = IntervalTrainer()
    trainer.run_quiz()
