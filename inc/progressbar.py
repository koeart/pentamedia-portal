import sys

class Progressbar:
    def __init__(self, minValue = 0, maxValue = 10, totalWidth=12, show_numbers=False):
        self._old_payload = ""
        self.show_numbers = show_numbers
        self.progBar = "[]"   # This holds the progress bar string
        self.min = minValue
        self.max = maxValue
        self.span = maxValue - minValue
        self.width = totalWidth
        self.amount = 0       # When amount == max, we are 100% done
        self.update(0)  # Build progress bar string
        self._old_pbar = self.pbar_str

    def update(self, newAmount = 0, payload = None):
        if newAmount < self.min: newAmount = self.min
        if newAmount > self.max: newAmount = self.max
        self.amount = newAmount

        # Figure out the new percent done, round to an integer
        diffFromMin = float(self.amount - self.min)
        if self.span == 0: percentDone = 0
        else: percentDone = (diffFromMin / float(self.span)) * 100.0
        percentDone = round(percentDone)
        percentDone = int(percentDone)

        # Figure out how many hash bars the percentage should be
        allFull = self.width - 2
        numHashes = (percentDone / 100.0) * allFull
        numHashes = int(round(numHashes))

        # build a progress bar with hashes and spaces
        self.progBar = "[" + '#'*numHashes + ' '*(allFull-numHashes) + "]"

        # figure out where to put the percentage, roughly centered
        percentPlace = (len(self.progBar) / 2) - len(str(percentDone))
        percentString = str(percentDone) + "%"

        # slice the percentage into the bar
        self.progBar = self.progBar[0:int(percentPlace)] + percentString + \
                       self.progBar[int(percentPlace+len(percentString)):]

        # add numbers at the end
        if self.show_numbers: self.progBar += " ({0}/{1})".\
                    format(self.amount-self.min, self.max-self.min)

        # add the payload
        if payload:
            self.progBar += " " + payload + \
                            " " * (len(self._old_payload) - len(payload))
            self._old_payload = payload
        else:
            if self._old_payload:
                self.progBar += " " * len(self._old_payload)
                self._old_payload = ""

        self.pbar_str = str(self)

    def __str__(self):
        return str(self.progBar)

    def draw(self):
        # draw progress bar - but only if it has changed
        if self.pbar_str != self._old_pbar:
            self._old_pbar = self.pbar_str
            sys.stdout.write(self.pbar_str + '\r')
            sys.stdout.flush()      # force updating of screen

    def clear(self):
        sys.stdout.write(" " * len(self.pbar_str) + '\r')
        sys.stdout.flush()      # force updating of screen
