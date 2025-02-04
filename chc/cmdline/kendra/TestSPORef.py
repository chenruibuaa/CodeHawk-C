# ------------------------------------------------------------------------------
# C Source Code Analyzer
# Author: Henny Sipma
# ------------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2017-2020 Kestrel Technology LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ------------------------------------------------------------------------------


class TestSPORef(object):
    def __init__(self, testcfunctionref, r):
        self.testcfunctionref = testcfunctionref
        self.r = r

    def get_line(self):
        return int(self.r["line"])

    def get_context(self):
        return self.r["cfgctxt"]

    def get_tgt_status(self):
        return self.r["tgtstatus"]

    def get_status(self):
        return self.r["status"]

    def get_predicate(self):
        return self.r["predicate"]

    def get_type(self):
        return self.r["type"]

    def get_argnr(self):
        return self.r["argnr"]

    def get_id(self):
        if self.get_type() == "callsite":
            return (self.get_predicate(), self.get_argnr())
