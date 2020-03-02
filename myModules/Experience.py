class Experience():
    def __init__(self, s_t, a_t, s_t1, r_t, done):
        self.s_t = s_t
        self.a_t = a_t
        self.s_t1 = s_t1
        self.r_t = r_t
        self.done = done

    def showExperience(self):
        print("s_t=%d a_t=%d s_t1=%d r_t=%d done=%d" % (self.s_t, self.a_t, self.s_t1, self.r_t, self.done))


