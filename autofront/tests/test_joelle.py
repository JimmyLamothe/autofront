
"""
The Story class is used to write a choose your own adventure story
"""

class Story:
    def __init__(self, title=None):
        self.title = title
        self.paragraphs = {}
    def add_paragraph(self, key, paragraph):
        self.paragraphs[key] = paragraph
    def add_first_paragraph(self, paragraph):
        paragraph.set_first(True);
        self.paragraphs["first"] = paragraph
    def run(self):
        print(self.title)
        done = False
        restart = True
        next_par = None
        while (not done or restart):
            if restart:
                [done, restart, next_par] = self.paragraphs["first"].run()
            elif not next_par is None:
                [done, restart, next_par] = next_par.run()
            else:
                done = True

class Paragraph:
    def __init__(self, text=None):
        self.text = text
        self.choices = {}
        self.end = False
        self.rpt= False
        self.other= None
        self.restart = False
        self.first = False
    def set_first(self, is_first):
        self.first = True
    def add_restart(self):
        self.restart= True
    def add_other(self,paragraph):
        self.other= paragraph
    def add_text(self, text):
        self.text = text
    def add_choice(self, key, paragraph):
        self.choices[key] = paragraph
    def set_end(self, end):
        self.end = end
    def set_rpt(self, rpt, max_reps):
        self.rpt = rpt
        self.reps = 0
        self.max_reps = max_reps
    def run(self):
        print(self.text)
        exit_now = ((len(self.choices) == 0) or self.end) and not self.rpt
        bad_input = True
        next_paragraph = None
        while bad_input and not exit_now:
            if not self.rpt:
                choice = input()
                choice = choice.lower()
                if choice == "x":
                    exit_now = True
                    break
            else:
                self.reps += 1
                if self.reps >= self.max_reps:
                    import sys
                    sys.exit('The cat game has broken Python :-(')
                choice = None
            try:
                if choice != None:
                    next_paragraph = self.choices[choice]
                    bad_input = False
                else:
                    print(self.text)
            except:
                if not self.other is None:
                    next_paragraph = self.other
                    bad_input = False
                else:
                    print("Try again")
                    print(self.text)
        return [exit_now, self.restart, next_paragraph]

def run_cat():
    start = Story("This is the cat game. Press x to exit and enter t to try again")
    cashew = Paragraph("Say hello to Cashew.")
    nounou = Paragraph("Nice! Now say hi to Nounou")
    mitzi = Paragraph("Good job! Now say hello to Mitzi")
    greluche = Paragraph("Wow! Now say hi to Greluche")
    mimi = Paragraph("Incredible! Now say hey to Mimi")
    arthur = Paragraph("Awesome! Finally, say hello to Arthur")
    theend = Paragraph("Well done! You won the cat game!")
    theend.set_end(True)
    failc = Paragraph("You just had to say hi :( Try again")
    failn = Paragraph("The kitty is disappointed in you. Try again")
    failmit = Paragraph("You know you could have said hi. Try again")
    failg = Paragraph("You failed. Try again")
    failmim = Paragraph("You didn't say hello to the kitty :(:( Try again.")
    faila = Paragraph("Aww you were almost there. Try again.")
    wow1 = Paragraph("Haha very funny. Say hi to Nounou for real.")
    wow2 = Paragraph("You're hilarious just say hi to the Mitzi please")
    wow3 = Paragraph("Ok stop it it's not funny. Now say an actual hi to Greluche or it will end badly.")
    wow4 = Paragraph("I'M SERIOUS IF YOU DON'T STOP THERE WILL BE CONSEQUENCES!!! Now say: 'Hello Mimi' and everything will be fine")
    wow5 = Paragraph("Why won't you stop :(:(:( Just say hey to Arthur NORMALLY for once!")
    wow6 = Paragraph("Ok that's it i'm done with you. You broke the game. Good job.")
    wow6.set_rpt(True, 100)

    start.add_first_paragraph(cashew)
    cashew.add_choice("hello cashew", nounou)
    cashew.add_choice("hi cashew", nounou)
    cashew.add_choice("hey cashew", nounou)
    cashew.add_choice("hello", nounou)
    cashew.add_choice("hi", nounou)
    cashew.add_choice("hey", nounou)
    cashew.add_choice("hello to cashew", wow1)
    cashew.add_choice("t", cashew)
    cashew.add_other(failc)

    nounou.add_choice("hello nounou", mitzi)
    nounou.add_choice("hi nounou", mitzi)
    nounou.add_choice("hey nounou", mitzi)
    nounou.add_choice("hello", mitzi)
    nounou.add_choice("hi", mitzi)
    nounou.add_choice("hey", mitzi)
    nounou.add_choice("t", cashew)
    nounou.add_other(failn)

    mitzi.add_choice("hello mitzi", greluche)
    mitzi.add_choice("hi mitzi", greluche)
    mitzi.add_choice("hey mitzi", greluche)
    mitzi.add_choice("hello", greluche)
    mitzi.add_choice("hi", greluche)
    mitzi.add_choice("hey", greluche)
    mitzi.add_choice("t", cashew)
    mitzi.add_other(failmit)

    greluche.add_choice("hello greluche", mimi)
    greluche.add_choice("hi greluche", mimi)
    greluche.add_choice("hey greluche", mimi)
    greluche.add_choice("hello", mimi)
    greluche.add_choice("hi", mimi)
    greluche.add_choice("hey", mimi)
    greluche.add_choice("t", cashew)
    greluche.add_other(failg)

    mimi.add_choice("hello mimi", arthur)
    mimi.add_choice("hi mimi", arthur)
    mimi.add_choice("hey mimi", arthur)
    mimi.add_choice("hello", arthur)
    mimi.add_choice("hi", arthur)
    mimi.add_choice("hey", arthur)
    mimi.add_choice("t", cashew)
    mimi.add_other(failmim)

    arthur.add_choice("hello arthur", theend)
    arthur.add_choice("hi arthur", theend)
    arthur.add_choice("hey arthur", theend)
    arthur.add_choice("hello", theend)
    arthur.add_choice("hi", theend)
    arthur.add_choice("hey", theend)
    arthur.add_choice("t", cashew)
    arthur.add_other(faila)

    wow1.add_choice("hi to nounou for real", wow2)
    wow1.add_choice("hi to nounou for real.", wow2)
    wow1.add_choice("hi nounou", mitzi)
    wow1.add_choice("hello nounou", mitzi)
    wow1.add_choice("hey nounou", mitzi)
    wow1.add_choice("hi", mitzi)
    wow1.add_choice("hello", mitzi)
    wow1.add_choice("hey", mitzi)
    wow1.add_choice("t", cashew)
    wow1.add_other(failn)

    wow2.add_choice("hi to the mitzi please", wow3)
    wow2.add_choice("hi nounou", greluche)
    wow2.add_choice("hello nounou", greluche)
    wow2.add_choice("hey nounou", greluche)
    wow2.add_choice("hi", greluche)
    wow2.add_choice("hello", greluche)
    wow2.add_choice("hey", greluche)
    wow2.add_choice("t", cashew)
    wow2.add_other(failmit)

    wow3.add_choice("an actual hi to greluche or it will end badly", wow4)
    wow3.add_choice("hi greluche", mimi)
    wow3.add_choice("hello greluche", mimi)
    wow3.add_choice("hey greluche", mimi)
    wow3.add_choice("hi", mimi)
    wow3.add_choice("hello", mimi)
    wow3.add_choice("hey", mimi)
    wow3.add_choice("t", cashew)
    wow3.add_other(failg)

    wow4.add_choice("'hello mimi' and everything will be fine", wow5)
    wow4.add_choice("hello mimi and everything will be fine", wow5)
    wow4.add_choice("hi mimi", arthur)
    wow4.add_choice("hello mimi", arthur)
    wow4.add_choice("hey mimi", arthur)
    wow4.add_choice("hi", arthur)
    wow4.add_choice("hello", arthur)
    wow4.add_choice("hey", arthur)
    wow4.add_choice("t", cashew)
    wow4.add_other(failmim)

    wow5.add_choice("hey to arthur normally for once!", wow6)
    wow5.add_choice("hey to arthur normally for once", wow6)
    wow5.add_choice("hi arthur", theend)
    wow5.add_choice("hello arthur", theend)
    wow5.add_choice("hey arthur", theend)
    wow5.add_choice("hi", theend)
    wow5.add_choice("hello", theend)
    wow5.add_choice("hey", theend)
    wow5.add_choice("t", cashew)
    wow5.add_other(faila)

    failc.add_restart()
    failn.add_restart()
    failmit.add_restart()
    failg.add_restart()
    failmim.add_restart()
    faila.add_restart()

    start.run()

run_cat()
