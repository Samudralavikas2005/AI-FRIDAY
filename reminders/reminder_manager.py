# reminders/reminder_manager.py
import json
import datetime
import re
import time
import os
from config import REMINDER_FILE

class ReminderManager:
    def __init__(self):
        self.reminder_file = REMINDER_FILE
    
    def load_reminders(self):
        if os.path.exists(self.reminder_file):
            try:
                with open(self.reminder_file, "r") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_reminders(self, reminders):
        with open(self.reminder_file, "w") as f:
            json.dump(reminders, f, indent=4)
    
    def parse_time_from_text(self, time_text):
        now = datetime.datetime.now()

        if not time_text or not isinstance(time_text, str):
            return None

        text = time_text.strip().lower()

        # Relative time
        rel_match = re.search(r'\bin\s+(\d+)\s*(minute|minutes|hour|hours)\b', text)
        if rel_match:
            num = int(rel_match.group(1))
            unit = rel_match.group(2)
            if 'hour' in unit:
                return now + datetime.timedelta(hours=num)
            else:
                return now + datetime.timedelta(minutes=num)

        # Explicit AM/PM
        ampm_match = re.search(r'\b(1[0-2]|0?[1-9])(?::([0-5]\d))?\s*(am|pm)\b', text, re.IGNORECASE)
        if ampm_match:
            hour = int(ampm_match.group(1))
            minute = int(ampm_match.group(2)) if ampm_match.group(2) else 0
            meridian = ampm_match.group(3).lower()
            if meridian == 'pm' and hour != 12:
                hour += 12
            elif meridian == 'am' and hour == 12:
                hour = 0
            reminder_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if reminder_time <= now:
                reminder_time += datetime.timedelta(days=1)
            return reminder_time

        return None

    def add_reminder_from_text(self, text):
        if not text or not isinstance(text, str):
            return "I couldn't understand the reminder command."

        # relative
        rel_match = re.search(r'.*remind me to (.+?) in (\d+ (?:minute|minutes|hour|hours))', text, re.IGNORECASE)
        if rel_match:
            task = rel_match.group(1).strip()
            time_text = rel_match.group(2).strip()
            reminder_dt = self.parse_time_from_text(f"in {time_text}")
            if not reminder_dt:
                return "I couldn't understand the time for the reminder."
            reminders = self.load_reminders()
            reminders.append({"task": task, "time": reminder_dt.isoformat()})
            self.save_reminders(reminders)
            return f"Reminder set for '{task}' at {reminder_dt.strftime('%I:%M %p')}"

        # absolute
        abs_match = re.search(r'.*remind me to (.+?) at (.+)', text, re.IGNORECASE)
        if abs_match:
            task = abs_match.group(1).strip()
            time_text = abs_match.group(2).strip()

            reminder_dt = self.parse_time_from_text(time_text)
            if reminder_dt is None:
                if re.search(r'\b(1[3-9]|2[0-3]|[01]?\d:[0-5]\d)\b', time_text):
                    return "Please give time in 12-hour format (e.g. '10:30 PM') or say 'in 10 minutes'. I don't accept 24-hour times like 21:30."
                return "I couldn't understand the time. Please say something like 'at 9 PM' or 'in 10 minutes'."
            reminders = self.load_reminders()
            reminders.append({"task": task, "time": reminder_dt.isoformat()})
            self.save_reminders(reminders)
            return f"Reminder set for '{task}' at {reminder_dt.strftime('%I:%M %p')}"

        return "I couldn't understand the reminder command."

    def list_reminders_text(self):
        reminders = self.load_reminders()
        if not reminders:
            return "You have no reminders set."
        lines = []
        for i, r in enumerate(reminders, start=1):
            dt = datetime.datetime.fromisoformat(r["time"])
            lines.append(f"{i}. {r['task']} at {dt.strftime('%I:%M %p')}")
        return "\n".join(lines)

    def check_reminders_loop(self):
        from speech.text_to_speech import TextToSpeech
        tts = TextToSpeech()
        
        while True:
            now = datetime.datetime.now()
            reminders = self.load_reminders()
            changed = False
            for reminder in reminders[:]:
                try:
                    reminder_time = datetime.datetime.fromisoformat(reminder["time"])
                except:
                    reminders.remove(reminder)
                    changed = True
                    continue
                if now >= reminder_time:
                    msg = f"Hi, it's time to {reminder['task']}"
                    print("⏰ Reminder triggered:", reminder['task'], "scheduled for", reminder_time)
                    tts.speak(msg)
                    reminders.remove(reminder)
                    changed = True
            if changed:
                self.save_reminders(reminders)
            time.sleep(20)

    def clear_all_reminders(self):
        self.save_reminders([])
        return "All reminders cleared."
