import csv
from pylsl import StreamInlet, resolve_stream
import time
import keyboard

def record_heart_rate(participant_id):
    print("Attempting to resolve the HeartRate stream...")
    streams = resolve_stream('name', 'HeartRate')

    if not streams:
        print("No streams named 'HeartRate' of type 'ExciteOMeter' found.")
        return

    inlet = StreamInlet(streams[0])
    print("HeartRate stream found, setting up inlet...")
    print(f"Connected to {inlet.info().name()} from {inlet.info().hostname()}.")

    csv_filename = f"heart_rate_{participant_id}.csv"
    is_recording = False

    print("Press 'r' to start/stop recording, 'q' to quit.")

    try:
        with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Timestamp', 'Heart Rate'])

            while True:
                sample, timestamp = inlet.pull_sample(timeout=1.0)
                if sample:
                    heart_rate = sample[0]
                    print(f"Heart Rate: {heart_rate:.2f}")

                    if is_recording:
                        csv_writer.writerow([timestamp, heart_rate])
                        csvfile.flush()

                if keyboard.is_pressed('r'):
                    is_recording = not is_recording
                    print("Recording started" if is_recording else "Recording stopped")
                    time.sleep(0.2)  # Debounce
                elif keyboard.is_pressed('q'):
                    print("Quitting...")
                    break

    except KeyboardInterrupt:
        print("Stream reading interrupted.")

def main():
    participant_id = input("Enter participant ID: ")
    record_heart_rate(participant_id)

if __name__ == '__main__':
    main()
