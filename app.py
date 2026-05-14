import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import pymongo
from datetime import datetime
import random
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Vocabulary Learner Pro")
        self.root.geometry("1000x750")
        self.root.configure(bg='#f0f0f0')
        
        # MongoDB Connection
        try:
            self.client = pymongo.MongoClient("mongodb+srv://parth:parth999@my-server.aqlukhz.mongodb.net/")
            self.db = self.client['vocabulary_db']
            self.collection = self.db['words']
            # Create indexes for better performance
            self.collection.create_index("word")
            self.collection.create_index("date_added")
            self.collection.create_index("entry_type")
            messagebox.showinfo("Success", "Connected to MongoDB!")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to MongoDB:\n{str(e)}")
            
        self.setup_ui()
        
    def setup_ui(self):
        # Create notebook for tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Arial', 10, 'bold'))
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Add Word/Phrase/Idiom
        self.add_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_tab, text="➕ Add Entry")
        self.create_add_tab()
        
        # Tab 2: View All
        self.view_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_tab, text="📋 View All")
        self.create_view_tab()
        
        # Tab 3: Interactive Quiz
        self.quiz_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.quiz_tab, text="🎯 Quiz Mode")
        self.create_quiz_tab()
        
        # Tab 4: Statistics
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="📊 Statistics")
        self.create_stats_tab()
        
        # Tab 5: Export to PDF
        self.export_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.export_tab, text="📄 Export PDF")
        self.create_export_tab()
        
    def create_add_tab(self):
        frame = ttk.Frame(self.add_tab, padding="20")
        frame.pack(fill='both', expand=True)
        
        # Entry Type Selection
        ttk.Label(frame, text="Entry Type:", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky='w', pady=10)
        self.entry_type_var = tk.StringVar(value="Word")
        entry_type_frame = ttk.Frame(frame)
        entry_type_frame.grid(row=0, column=1, sticky='w', pady=10, padx=10)
        ttk.Radiobutton(entry_type_frame, text="Word", variable=self.entry_type_var, value="Word").pack(side='left', padx=5)
        ttk.Radiobutton(entry_type_frame, text="Phrase", variable=self.entry_type_var, value="Phrase").pack(side='left', padx=5)
        ttk.Radiobutton(entry_type_frame, text="Idiom", variable=self.entry_type_var, value="Idiom").pack(side='left', padx=5)
        
        # Word/Phrase/Idiom Entry
        ttk.Label(frame, text="Word/Phrase/Idiom:", font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky='w', pady=10)
        self.word_entry = ttk.Entry(frame, width=40, font=('Arial', 11))
        self.word_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Meaning Entry
        ttk.Label(frame, text="Meaning:", font=('Arial', 12, 'bold')).grid(row=2, column=0, sticky='nw', pady=10)
        self.meaning_text = scrolledtext.ScrolledText(frame, width=40, height=4, font=('Arial', 11), wrap=tk.WORD)
        self.meaning_text.grid(row=2, column=1, pady=10, padx=10)
        
        # Movie Context
        ttk.Label(frame, text="Movie Name:", font=('Arial', 12, 'bold')).grid(row=3, column=0, sticky='w', pady=10)
        self.movie_entry = ttk.Entry(frame, width=40, font=('Arial', 11))
        self.movie_entry.grid(row=3, column=1, pady=10, padx=10)
        
        # Context/Sentence
        ttk.Label(frame, text="Context/Sentence:", font=('Arial', 12, 'bold')).grid(row=4, column=0, sticky='nw', pady=10)
        self.context_text = scrolledtext.ScrolledText(frame, width=40, height=3, font=('Arial', 11), wrap=tk.WORD)
        self.context_text.grid(row=4, column=1, pady=10, padx=10)
        
        # Difficulty Level
        ttk.Label(frame, text="Difficulty:", font=('Arial', 12, 'bold')).grid(row=5, column=0, sticky='w', pady=10)
        self.difficulty_var = tk.StringVar(value="Medium")
        difficulty_frame = ttk.Frame(frame)
        difficulty_frame.grid(row=5, column=1, sticky='w', pady=10, padx=10)
        ttk.Radiobutton(difficulty_frame, text="Easy", variable=self.difficulty_var, value="Easy").pack(side='left', padx=5)
        ttk.Radiobutton(difficulty_frame, text="Medium", variable=self.difficulty_var, value="Medium").pack(side='left', padx=5)
        ttk.Radiobutton(difficulty_frame, text="Hard", variable=self.difficulty_var, value="Hard").pack(side='left', padx=5)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        save_btn = tk.Button(button_frame, text="💾 Save Entry", command=self.save_word, 
                            bg='#4CAF50', fg='white', font=('Arial', 11, 'bold'), 
                            padx=20, pady=10, relief=tk.RAISED, cursor='hand2')
        save_btn.pack(side='left', padx=10)
        
        clear_btn = tk.Button(button_frame, text="🗑️ Clear", command=self.clear_fields, 
                             bg='#f44336', fg='white', font=('Arial', 11, 'bold'), 
                             padx=20, pady=10, relief=tk.RAISED, cursor='hand2')
        clear_btn.pack(side='left', padx=10)
        
    def create_view_tab(self):
        frame = ttk.Frame(self.view_tab, padding="10")
        frame.pack(fill='both', expand=True)
        
        # Search and Filter Frame
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill='x', pady=10)
        
        ttk.Label(search_frame, text="Search:", font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        self.search_entry = ttk.Entry(search_frame, width=25, font=('Arial', 10))
        self.search_entry.pack(side='left', padx=5)
        
        tk.Button(search_frame, text="🔍 Search", command=self.search_words, 
                 bg='#2196F3', fg='white', font=('Arial', 9, 'bold'), cursor='hand2').pack(side='left', padx=3)
        tk.Button(search_frame, text="📋 Show All", command=self.load_all_words, 
                 bg='#9C27B0', fg='white', font=('Arial', 9, 'bold'), cursor='hand2').pack(side='left', padx=3)
        
        # Filter by type
        ttk.Label(search_frame, text="Filter:", font=('Arial', 10, 'bold')).pack(side='left', padx=10)
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(search_frame, textvariable=self.filter_var, 
                                   values=["All", "Word", "Phrase", "Idiom"], 
                                   width=10, state='readonly')
        filter_combo.pack(side='left', padx=5)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.load_all_words())
        
        tk.Button(search_frame, text="🗑️ Delete Selected", command=self.delete_word, 
                 bg='#f44336', fg='white', font=('Arial', 9, 'bold'), cursor='hand2').pack(side='left', padx=3)
        
        # Treeview
        columns = ('Type', 'Word', 'Meaning', 'Movie', 'Difficulty', 'Reviews', 'Date')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', height=20)
        
        # Column headings
        self.tree.heading('Type', text='Type')
        self.tree.heading('Word', text='Word/Phrase/Idiom')
        self.tree.heading('Meaning', text='Meaning')
        self.tree.heading('Movie', text='Movie')
        self.tree.heading('Difficulty', text='Difficulty')
        self.tree.heading('Reviews', text='Reviews')
        self.tree.heading('Date', text='Date Added')
        
        # Column widths
        self.tree.column('Type', width=70)
        self.tree.column('Word', width=150)
        self.tree.column('Meaning', width=250)
        self.tree.column('Movie', width=120)
        self.tree.column('Difficulty', width=80)
        self.tree.column('Reviews', width=80)
        self.tree.column('Date', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Configure alternating row colors
        self.tree.tag_configure('oddrow', background='#f0f0f0')
        self.tree.tag_configure('evenrow', background='#ffffff')
        
        # Bind double-click to show details
        self.tree.bind('<Double-1>', self.show_word_details)
        
        self.load_all_words()
        
    def create_quiz_tab(self):
        frame = ttk.Frame(self.quiz_tab, padding="20")
        frame.pack(fill='both', expand=True)
        
        # Quiz header
        header_frame = tk.Frame(frame, bg='#673AB7', relief=tk.RAISED, bd=2)
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="🎯 Interactive Vocabulary Quiz", 
                font=('Arial', 18, 'bold'), bg='#673AB7', fg='white', 
                pady=15).pack()
        
        # Score display
        self.score_label = tk.Label(frame, text="Score: 0/0 | Correct: 0 | Wrong: 0", 
                                   font=('Arial', 12, 'bold'), fg='#673AB7')
        self.score_label.pack(pady=10)
        
        # Progress bar
        self.quiz_progress = ttk.Progressbar(frame, length=600, mode='determinate')
        self.quiz_progress.pack(pady=10)
        
        # Quiz word display
        self.quiz_word_label = tk.Label(frame, text="", font=('Arial', 20, 'bold'), 
                                       fg='#1976D2', wraplength=600)
        self.quiz_word_label.pack(pady=20)
        
        # Type indicator
        self.quiz_type_label = tk.Label(frame, text="", font=('Arial', 11, 'italic'), fg='#666')
        self.quiz_type_label.pack()
        
        # Answer area
        self.quiz_meaning_text = scrolledtext.ScrolledText(frame, width=70, height=8, 
                                                          font=('Arial', 11), state='disabled',
                                                          wrap=tk.WORD, bg='#f5f5f5')
        self.quiz_meaning_text.pack(pady=15)
        
        # Feedback label
        self.feedback_label = tk.Label(frame, text="", font=('Arial', 12, 'bold'))
        self.feedback_label.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)
        
        self.start_quiz_btn = tk.Button(button_frame, text="🚀 Start Quiz", 
                                       command=self.start_quiz, bg='#4CAF50', fg='white',
                                       font=('Arial', 12, 'bold'), padx=25, pady=12,
                                       relief=tk.RAISED, cursor='hand2')
        self.start_quiz_btn.pack(side='left', padx=10)
        
        self.show_answer_btn = tk.Button(button_frame, text="👁️ Show Answer", 
                                        command=self.show_answer, bg='#2196F3', fg='white',
                                        font=('Arial', 12, 'bold'), padx=25, pady=12,
                                        relief=tk.RAISED, cursor='hand2', state='disabled')
        self.show_answer_btn.pack(side='left', padx=10)
        
        self.know_btn = tk.Button(button_frame, text="✅ I Know", 
                                 command=lambda: self.answer_question(True), bg='#4CAF50', fg='white',
                                 font=('Arial', 12, 'bold'), padx=25, pady=12,
                                 relief=tk.RAISED, cursor='hand2', state='disabled')
        self.know_btn.pack(side='left', padx=10)
        
        self.dont_know_btn = tk.Button(button_frame, text="❌ Don't Know", 
                                      command=lambda: self.answer_question(False), bg='#f44336', fg='white',
                                      font=('Arial', 12, 'bold'), padx=25, pady=12,
                                      relief=tk.RAISED, cursor='hand2', state='disabled')
        self.dont_know_btn.pack(side='left', padx=10)
        
        self.next_btn = tk.Button(button_frame, text="➡️ Next", 
                                 command=self.next_quiz_word, bg='#FF9800', fg='white',
                                 font=('Arial', 12, 'bold'), padx=25, pady=12,
                                 relief=tk.RAISED, cursor='hand2', state='disabled')
        self.next_btn.pack(side='left', padx=10)
        
        self.quiz_words = []
        self.current_quiz_index = 0
        self.quiz_score = {'correct': 0, 'wrong': 0, 'total': 0}
        
    def create_stats_tab(self):
        frame = ttk.Frame(self.stats_tab, padding="20")
        frame.pack(fill='both', expand=True)
        
        header = tk.Label(frame, text="📊 Your Learning Statistics", 
                         font=('Arial', 18, 'bold'), fg='#1976D2')
        header.pack(pady=20)
        
        self.stats_text = scrolledtext.ScrolledText(frame, width=75, height=28, 
                                                   font=('Courier New', 10), wrap=tk.WORD)
        self.stats_text.pack(pady=10)
        
        refresh_btn = tk.Button(frame, text="🔄 Refresh Statistics", 
                               command=self.load_statistics, bg='#4CAF50', fg='white',
                               font=('Arial', 11, 'bold'), padx=20, pady=10,
                               relief=tk.RAISED, cursor='hand2')
        refresh_btn.pack(pady=10)
        
        self.load_statistics()
        
    def create_export_tab(self):
        frame = ttk.Frame(self.export_tab, padding="30")
        frame.pack(fill='both', expand=True)
        
        header = tk.Label(frame, text="📄 Export to PDF", 
                         font=('Arial', 18, 'bold'), fg='#1976D2')
        header.pack(pady=30)
        
        info_text = """
        Export your vocabulary collection to a beautifully formatted PDF file.
        Perfect for printing and offline study!
        
        The PDF will include:
        • All words, phrases, and idioms
        • Meanings and contexts
        • Movie references
        • Organized by type and difficulty
        """
        
        info_label = tk.Label(frame, text=info_text, font=('Arial', 11), 
                            justify=tk.LEFT, fg='#555')
        info_label.pack(pady=20)
        
        # Export options
        options_frame = tk.LabelFrame(frame, text="Export Options", 
                                     font=('Arial', 12, 'bold'), padx=20, pady=20)
        options_frame.pack(pady=20, fill='x')
        
        self.export_all_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Export All Entries", 
                      variable=self.export_all_var, font=('Arial', 11)).pack(anchor='w', pady=5)
        
        self.export_words_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Include Words", 
                      variable=self.export_words_var, font=('Arial', 11)).pack(anchor='w', pady=5)
        
        self.export_phrases_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Include Phrases", 
                      variable=self.export_phrases_var, font=('Arial', 11)).pack(anchor='w', pady=5)
        
        self.export_idioms_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Include Idioms", 
                      variable=self.export_idioms_var, font=('Arial', 11)).pack(anchor='w', pady=5)
        
        # Export button
        export_btn = tk.Button(frame, text="📥 Generate PDF", 
                              command=self.export_to_pdf, bg='#E91E63', fg='white',
                              font=('Arial', 14, 'bold'), padx=40, pady=15,
                              relief=tk.RAISED, cursor='hand2')
        export_btn.pack(pady=30)
        
    def save_word(self):
        word = self.word_entry.get().strip()
        meaning = self.meaning_text.get("1.0", tk.END).strip()
        movie = self.movie_entry.get().strip()
        context = self.context_text.get("1.0", tk.END).strip()
        difficulty = self.difficulty_var.get()
        entry_type = self.entry_type_var.get()
        
        if not word or not meaning:
            messagebox.showwarning("Missing Data", "Please enter both word/phrase/idiom and meaning!")
            return
        
        # Check if entry already exists
        existing = self.collection.find_one({"word": word.lower(), "entry_type": entry_type})
        
        if existing:
            response = messagebox.askyesno("Entry Exists", 
                f"This {entry_type.lower()} already exists. Do you want to update it?")
            if response:
                self.collection.update_one(
                    {"word": word.lower(), "entry_type": entry_type},
                    {"$set": {
                        "meaning": meaning,
                        "movie": movie,
                        "context": context,
                        "difficulty": difficulty,
                        "last_updated": datetime.now()
                    },
                    "$inc": {"review_count": 1}}
                )
                messagebox.showinfo("Success", f"{entry_type} updated successfully!")
            else:
                return
        else:
            word_doc = {
                "word": word.lower(),
                "meaning": meaning,
                "movie": movie,
                "context": context,
                "difficulty": difficulty,
                "entry_type": entry_type,
                "date_added": datetime.now(),
                "review_count": 0,
                "learned": False
            }
            self.collection.insert_one(word_doc)
            messagebox.showinfo("Success", f"{entry_type} saved successfully!")
        
        self.clear_fields()
        self.load_all_words()
        
    def clear_fields(self):
        self.word_entry.delete(0, tk.END)
        self.meaning_text.delete("1.0", tk.END)
        self.movie_entry.delete(0, tk.END)
        self.context_text.delete("1.0", tk.END)
        self.difficulty_var.set("Medium")
        self.entry_type_var.set("Word")
        
    def load_all_words(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Apply filter
        filter_type = self.filter_var.get()
        if filter_type == "All":
            words = self.collection.find().sort("date_added", -1)
        else:
            words = self.collection.find({"entry_type": filter_type}).sort("date_added", -1)
        
        row_index = 0
        for word in words:
            # Alternate row colors
            tag = 'evenrow' if row_index % 2 == 0 else 'oddrow'
            
            self.tree.insert('', 'end', values=(
                word.get('entry_type', 'Word'),
                word['word'].capitalize(),
                word['meaning'][:60] + '...' if len(word['meaning']) > 60 else word['meaning'],
                word.get('movie', 'N/A'),
                word.get('difficulty', 'Medium'),
                word.get('review_count', 0),
                word['date_added'].strftime('%Y-%m-%d')
            ), tags=(str(word['_id']), tag))
            
            row_index += 1
            
    def search_words(self):
        search_term = self.search_entry.get().strip().lower()
        
        if not search_term:
            self.load_all_words()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        words = self.collection.find({
            "$or": [
                {"word": {"$regex": search_term, "$options": "i"}},
                {"meaning": {"$regex": search_term, "$options": "i"}},
                {"movie": {"$regex": search_term, "$options": "i"}}
            ]
        })
        
        row_index = 0
        for word in words:
            # Alternate row colors
            tag = 'evenrow' if row_index % 2 == 0 else 'oddrow'
            
            self.tree.insert('', 'end', values=(
                word.get('entry_type', 'Word'),
                word['word'].capitalize(),
                word['meaning'][:60] + '...' if len(word['meaning']) > 60 else word['meaning'],
                word.get('movie', 'N/A'),
                word.get('difficulty', 'Medium'),
                word.get('review_count', 0),
                word['date_added'].strftime('%Y-%m-%d')
            ), tags=(str(word['_id']), tag))
            
            row_index += 1
            
    def show_word_details(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        word = item['values'][1].lower()
        entry_type = item['values'][0]
        
        word_doc = self.collection.find_one({"word": word, "entry_type": entry_type})
        
        if word_doc:
            details = f"""
Type: {word_doc.get('entry_type', 'Word')}
{word_doc.get('entry_type', 'Word')}: {word_doc['word'].capitalize()}
Movie: {word_doc.get('movie', 'N/A')}
Difficulty: {word_doc.get('difficulty', 'Medium')}
Review Count: {word_doc.get('review_count', 0)}
Date Added: {word_doc['date_added'].strftime('%Y-%m-%d %H:%M')}

Meaning:
{word_doc['meaning']}

Context/Sentence:
{word_doc.get('context', 'N/A')}
            """
            messagebox.showinfo(f"{entry_type} Details", details)
            
    def delete_word(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an entry to delete!")
            return
        
        item = self.tree.item(selected[0])
        word = item['values'][1].lower()
        entry_type = item['values'][0]
        
        response = messagebox.askyesno("Confirm Delete", 
                                      f"Are you sure you want to delete this {entry_type.lower()}: '{word}'?")
        if response:
            self.collection.delete_one({"word": word, "entry_type": entry_type})
            messagebox.showinfo("Success", f"{entry_type} deleted successfully!")
            self.load_all_words()
            
    def start_quiz(self):
        # Get all unlearned entries
        all_entries = list(self.collection.find({"learned": {"$ne": True}}))
        if not all_entries:
            messagebox.showinfo("No Entries", "No entries available for quiz! Add some words, phrases, or idioms first.")
            return
        
        # Shuffle and select all entries
        self.quiz_words = all_entries.copy()
        random.shuffle(self.quiz_words)
        self.current_quiz_index = 0
        self.quiz_score = {'correct': 0, 'wrong': 0, 'total': len(self.quiz_words)}
        
        # Update UI
        self.start_quiz_btn.config(state='disabled')
        self.show_answer_btn.config(state='normal')
        self.know_btn.config(state='normal')
        self.dont_know_btn.config(state='normal')
        self.next_btn.config(state='disabled')
        
        self.quiz_progress['maximum'] = len(self.quiz_words)
        self.quiz_progress['value'] = 0
        
        self.update_score_display()
        self.next_quiz_word()
        
    def next_quiz_word(self):
        if self.current_quiz_index >= len(self.quiz_words):
            self.finish_quiz()
            return
        
        current_word = self.quiz_words[self.current_quiz_index]
        entry_type = current_word.get('entry_type', 'Word')
        
        self.quiz_word_label.config(text=current_word['word'].capitalize())
        self.quiz_type_label.config(text=f"({entry_type})")
        
        self.quiz_meaning_text.config(state='normal')
        self.quiz_meaning_text.delete("1.0", tk.END)
        self.quiz_meaning_text.insert("1.0", "Think about the meaning...\n\nDo you know this one?")
        self.quiz_meaning_text.config(state='disabled')
        
        self.feedback_label.config(text="")
        
        # Enable buttons
        self.show_answer_btn.config(state='normal')
        self.know_btn.config(state='normal')
        self.dont_know_btn.config(state='normal')
        self.next_btn.config(state='disabled')
        
        self.quiz_progress['value'] = self.current_quiz_index
        
    def show_answer(self):
        if self.current_quiz_index >= len(self.quiz_words):
            return
        
        current_word = self.quiz_words[self.current_quiz_index]
        
        answer = f"✨ MEANING:\n{current_word['meaning']}\n\n"
        if current_word.get('context'):
            answer += f"📝 CONTEXT:\n{current_word['context']}\n\n"
        if current_word.get('movie'):
            answer += f"🎬 MOVIE: {current_word['movie']}"
        
        self.quiz_meaning_text.config(state='normal')
        self.quiz_meaning_text.delete("1.0", tk.END)
        self.quiz_meaning_text.insert("1.0", answer)
        self.quiz_meaning_text.config(state='disabled')
        
        # Disable show answer button
        self.show_answer_btn.config(state='disabled')
        
    def answer_question(self, knew_it):
        if self.current_quiz_index >= len(self.quiz_words):
            return
        
        current_word = self.quiz_words[self.current_quiz_index]
        
        # Update score
        if knew_it:
            self.quiz_score['correct'] += 1
            self.feedback_label.config(text="✅ Great! Keep it up!", fg='green')
            # Mark as learned if answered correctly
            self.collection.update_one(
                {"word": current_word['word']},
                {"$set": {"learned": True}}
            )
        else:
            self.quiz_score['wrong'] += 1
            self.feedback_label.config(text="❌ Don't worry, practice makes perfect!", fg='red')
            # Show answer if they didn't know
            self.show_answer()
        
        # Increment review count
        self.collection.update_one(
            {"word": current_word['word']},
            {"$inc": {"review_count": 1}}
        )
        
        self.update_score_display()
        
        # Disable answer buttons, enable next
        self.know_btn.config(state='disabled')
        self.dont_know_btn.config(state='disabled')
        self.next_btn.config(state='normal')
        
        self.current_quiz_index += 1
        
    def update_score_display(self):
        score_text = f"Score: {self.quiz_score['correct']}/{self.quiz_score['total']} | "
        score_text += f"✅ Correct: {self.quiz_score['correct']} | "
        score_text += f"❌ Wrong: {self.quiz_score['wrong']}"
        self.score_label.config(text=score_text)
        
    def finish_quiz(self):
        percentage = (self.quiz_score['correct'] / self.quiz_score['total'] * 100) if self.quiz_score['total'] > 0 else 0
        
        result_msg = f"""
🎉 Quiz Complete! 🎉

Total Questions: {self.quiz_score['total']}
Correct Answers: {self.quiz_score['correct']}
Wrong Answers: {self.quiz_score['wrong']}
Score: {percentage:.1f}%

"""
        if percentage >= 90:
            result_msg += "🌟 Outstanding! You're a vocabulary master!"
        elif percentage >= 75:
            result_msg += "👏 Great job! Keep up the good work!"
        elif percentage >= 60:
            result_msg += "👍 Good effort! Practice more to improve!"
        else:
            result_msg += "💪 Keep practicing! You'll get better!"
        
        messagebox.showinfo("Quiz Results", result_msg)
        
        # Reset quiz
        self.quiz_words = []
        self.current_quiz_index = 0
        self.quiz_score = {'correct': 0, 'wrong': 0, 'total': 0}
        
        self.quiz_word_label.config(text="")
        self.quiz_type_label.config(text="")
        self.quiz_meaning_text.config(state='normal')
        self.quiz_meaning_text.delete("1.0", tk.END)
        self.quiz_meaning_text.config(state='disabled')
        self.feedback_label.config(text="")
        
        self.start_quiz_btn.config(state='normal')
        self.show_answer_btn.config(state='disabled')
        self.know_btn.config(state='disabled')
        self.dont_know_btn.config(state='disabled')
        self.next_btn.config(state='disabled')
        
        self.quiz_progress['value'] = 0
        self.update_score_display()
        
    def load_statistics(self):
        self.stats_text.delete("1.0", tk.END)
        
        total_entries = self.collection.count_documents({})
        learned_entries = self.collection.count_documents({"learned": True})
        
        # Count by type
        words_count = self.collection.count_documents({"entry_type": "Word"})
        phrases_count = self.collection.count_documents({"entry_type": "Phrase"})
        idioms_count = self.collection.count_documents({"entry_type": "Idiom"})
        
        # Count by difficulty
        easy = self.collection.count_documents({"difficulty": "Easy"})
        medium = self.collection.count_documents({"difficulty": "Medium"})
        hard = self.collection.count_documents({"difficulty": "Hard"})
        
        # Most reviewed
        most_reviewed = list(self.collection.find().sort("review_count", -1).limit(10))
        
        # By movie
        movies = self.collection.distinct("movie")
        movie_counts = {}
        for movie in movies:
            if movie:
                count = self.collection.count_documents({"movie": movie})
                movie_counts[movie] = count
        
        stats = f"""
╔══════════════════════════════════════════════════════════════════╗
║              📚 VOCABULARY LEARNING STATISTICS 📚                ║
╚══════════════════════════════════════════════════════════════════╝

📊 OVERALL PROGRESS
   Total Entries: {total_entries}
   Learned: {learned_entries}
   In Progress: {total_entries - learned_entries}
   Completion: {(learned_entries/total_entries*100) if total_entries > 0 else 0:.1f}%

📝 BY ENTRY TYPE
   Words: {words_count}
   Phrases: {phrases_count}
   Idioms: {idioms_count}

📊 BY DIFFICULTY
   Easy: {easy}
   Medium: {medium}
   Hard: {hard}

⭐ MOST REVIEWED (TOP 10)
"""
        
        for i, entry in enumerate(most_reviewed, 1):
            entry_type_icon = "📖" if entry.get('entry_type') == 'Word' else "💬" if entry.get('entry_type') == 'Phrase' else "🎭"
            stats += f"   {i:2d}. {entry_type_icon} {entry['word'].capitalize()[:30]} - {entry.get('review_count', 0)} reviews\n"
        
        if movie_counts:
            stats += "\n🎬 WORDS BY MOVIE (TOP 10)\n"
            for movie, count in sorted(movie_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                stats += f"   • {movie}: {count} entries\n"
        
        stats += f"""

📅 LEARNING STREAK
   Keep learning every day to improve your vocabulary!
   
💡 TIP: Review your learned words regularly to retain them better!
"""
        
        self.stats_text.insert("1.0", stats)
        
    def export_to_pdf(self):
        try:
            # Ask user where to save
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=f"Vocabulary_Collection_{datetime.now().strftime('%Y%m%d')}.pdf"
            )
            
            if not file_path:
                return
            
            # Show progress message
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Generating PDF")
            progress_window.geometry("300x100")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            tk.Label(progress_window, text="Generating PDF...\nPlease wait...", 
                    font=('Arial', 12), pady=30).pack()
            progress_window.update()
            
            # Get entries based on filter
            query = {}
            types_to_export = []
            
            if not self.export_all_var.get():
                if self.export_words_var.get():
                    types_to_export.append("Word")
                if self.export_phrases_var.get():
                    types_to_export.append("Phrase")
                if self.export_idioms_var.get():
                    types_to_export.append("Idiom")
                
                if types_to_export:
                    query["entry_type"] = {"$in": types_to_export}
                else:
                    progress_window.destroy()
                    messagebox.showwarning("No Selection", "Please select at least one type to export!")
                    return
            
            entries = list(self.collection.find(query).sort([("entry_type", 1), ("word", 1)]))
            
            if not entries:
                progress_window.destroy()
                messagebox.showwarning("No Data", "No entries found to export!")
                return
            
            # Create PDF
            doc = SimpleDocTemplate(file_path, pagesize=letter,
                                   rightMargin=72, leftMargin=72,
                                   topMargin=72, bottomMargin=18)
            
            # Container for PDF elements
            elements = []
            
            # Styles
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1976D2'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#666666'),
                spaceAfter=20,
                alignment=TA_CENTER
            )
            
            section_style = ParagraphStyle(
                'SectionHeader',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#E91E63'),
                spaceAfter=12,
                spaceBefore=12,
                fontName='Helvetica-Bold'
            )
            
            # Title page
            elements.append(Paragraph("📚 My Vocabulary Collection", title_style))
            elements.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
            elements.append(Paragraph(f"Total Entries: {len(entries)}", subtitle_style))
            elements.append(Spacer(1, 0.5*inch))
            
            # Group by type
            current_type = None
            
            for entry in entries:
                entry_type = entry.get('entry_type', 'Word')
                
                # Add section header for new type
                if entry_type != current_type:
                    if current_type is not None:
                        elements.append(PageBreak())
                    
                    icon = "📖 WORDS" if entry_type == 'Word' else "💬 PHRASES" if entry_type == 'Phrase' else "🎭 IDIOMS"
                    elements.append(Paragraph(icon, section_style))
                    elements.append(Spacer(1, 0.2*inch))
                    current_type = entry_type
                
                # Create entry table
                word_text = entry['word'].upper()
                meaning_text = entry['meaning'].replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
                context_text = entry.get('context', '').replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
                movie_text = entry.get('movie', '').replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
                
                data = [
                    [Paragraph(f"<b>{word_text}</b>", styles['Heading3'])],
                    [Paragraph(f"<b>Meaning:</b> {meaning_text}", styles['Normal'])],
                ]
                
                if entry.get('context'):
                    data.append([Paragraph(f"<b>Context:</b> {context_text}", styles['Normal'])])
                
                if entry.get('movie'):
                    data.append([Paragraph(f"<b>Movie:</b> {movie_text}", styles['Normal'])])
                
                data.append([Paragraph(f"<b>Difficulty:</b> {entry.get('difficulty', 'Medium')} | <b>Reviews:</b> {entry.get('review_count', 0)}", 
                                      styles['Normal'])])
                
                table = Table(data, colWidths=[6.5*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E3F2FD')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('TOPPADDING', (0, 0), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')])
                ]))
                
                elements.append(table)
                elements.append(Spacer(1, 0.15*inch))
            
            # Build PDF
            doc.build(elements)
            
            progress_window.destroy()
            
            # Show success message with option to open
            result = messagebox.askyesno("Success", 
                f"PDF exported successfully!\n\nSaved to:\n{file_path}\n\nDo you want to open the file?")
            
            if result:
                import os
                import platform
                
                if platform.system() == 'Windows':
                    os.startfile(file_path)
                elif platform.system() == 'Darwin':  # macOS
                    os.system(f'open "{file_path}"')
                else:  # Linux
                    os.system(f'xdg-open "{file_path}"')
            
        except Exception as e:
            if 'progress_window' in locals():
                progress_window.destroy()
            messagebox.showerror("Export Error", f"Failed to export PDF:\n{str(e)}\n\nMake sure the file is not open in another program.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()