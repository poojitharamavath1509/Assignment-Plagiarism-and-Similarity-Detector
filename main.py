# Plagiarism & Similarity Detector
# Features:
# 	1. Add assignment submission (saved in CSV)
# 	2. Display all submissions
# 	3. Compare two submissions
# 	4. Scan all submissions (find similar pairs)
# 	5. Exit

import csv
import os
import re
from difflib import SequenceMatcher

FILE_NAME = "submissions.csv"
FIELDS = ["sub_id", "student", "title", "text"]


class Submission:
    def __init__(self, sub_id, student, title, text):
        self.sub_id = sub_id
        self.student = student
        self.title = title
        self.text = text

    def display(self):
        preview = self.text[:60] + ("..." if len(self.text) > 60 else "")
        print(f"ID     : {self.sub_id}")
        print(f"Student: {self.student}")
        print(f"Title  : {self.title}")
        print(f"Text   : {preview}")
        print("-" * 30)


class Detector:
    def __init__(self):
        self.submissions = []
        self.load_data()

    # ---------- CSV part ----------
    def load_data(self):
        if not os.path.exists(FILE_NAME):
            return
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.submissions.append(
                    Submission(row["sub_id"], row["student"], row["title"], row["text"])
                )

    def save_data(self):
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(FIELDS)
            for s in self.submissions:
                writer.writerow([s.sub_id, s.student, s.title, s.text])

    # ---------- helpers ----------
    def find(self, sub_id):
        for s in self.submissions:
            if s.sub_id == sub_id:
                return s
        return None

    @staticmethod
    def words(text):
        return re.findall(r"[a-z0-9]+", text.lower())

    def similarity(self, text1, text2):
        """Returns similarity percentage (0-100)."""
        w1, w2 = self.words(text1), self.words(text2)
        if not w1 or not w2:
            return 0.0
        # 1) word-set overlap (Jaccard)
        set1, set2 = set(w1), set(w2)
        jaccard = len(set1 & set2) / len(set1 | set2)
        # 2) sequence match (same order of words)
        sequence = SequenceMatcher(None, w1, w2).ratio()
        # average of both
        return round((jaccard + sequence) / 2 * 100, 2)

    @staticmethod
    def verdict(score):
        if score >= 70:
            return "HIGH - Possible plagiarism!"
        elif score >= 40:
            return "MEDIUM - Check manually"
        return "LOW - Looks original"

    # ---------- features ----------
    def add_submission(self):
        sub_id = input("Enter Submission Id: ").strip()
        if self.find(sub_id):
            print("Submission Id already taken, please enter a different id")
            return
        student = input("Enter Student Name: ").strip()
        title = input("Enter Assignment Title: ").strip()
        text = input("Enter Assignment Text: ").strip()
        if not sub_id or not student or not text:
            print("Id, name and text cannot be empty.")
            return
        self.submissions.append(Submission(sub_id, student, title, text))
        self.save_data()
        print("Submission added successfully!")

    def display_submissions(self):
        if not self.submissions:
            print("No submissions available.")
            return
        print("\n--- All Submissions ---")
        for s in self.submissions:
            s.display()

    def compare_two(self):
        id1 = input("Enter first Submission Id: ").strip()
        id2 = input("Enter second Submission Id: ").strip()
        s1, s2 = self.find(id1), self.find(id2)
        if not s1 or not s2:
            print("One or both submissions not found.")
            return
        if id1 == id2:
            print("Please enter two different ids.")
            return
        score = self.similarity(s1.text, s2.text)
        print(f"\n{s1.student} vs {s2.student}")
        print(f"Similarity: {score}%")
        print(f"Result    : {self.verdict(score)}")

    def scan_all(self):
        if len(self.submissions) < 2:
            print("Need at least 2 submissions to scan.")
            return
        results = []
        for i in range(len(self.submissions)):
            for j in range(i + 1, len(self.submissions)):
                a, b = self.submissions[i], self.submissions[j]
                results.append((self.similarity(a.text, b.text), a, b))
        results.sort(key=lambda r: r[0], reverse=True)

        print("\n--- Similarity Report (highest first) ---")
        print(f"{'Student 1':<15}{'Student 2':<15}{'Score':<10}Result")
        print("-" * 60)
        for score, a, b in results:
            print(f"{a.student:<15}{b.student:<15}{str(score) + '%':<10}{self.verdict(score)}")


# Create Detector object
detector = Detector()

# Menu
while True:
    print("\n===== PLAGIARISM & SIMILARITY DETECTOR =====")
    print("1. Add Submission")
    print("2. Display Submissions")
    print("3. Compare Two Submissions")
    print("4. Scan All Submissions")
    print("5. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        detector.add_submission()
    elif choice == "2":
        detector.display_submissions()
    elif choice == "3":
        detector.compare_two()
    elif choice == "4":
        detector.scan_all()
    elif choice == "5":
        print("Thank you!")
        break
    else:
        print("Invalid choice.")