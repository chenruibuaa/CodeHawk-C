# ------------------------------------------------------------------------------
# CodeHawk C Analyzer
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
import xml.etree.ElementTree as ET

import chc.util.xmlutil as UX
import chc.proof.CFunctionPO as PO

from chc.app.CLocation import CLocation
from chc.proof.CFunctionReturnsiteSPO import CFunctionReturnsiteSPO

from chc.proof.CFunctionPO import CProofDependencies
from chc.proof.CFunctionPO import CProofDiagnostic


po_status = {"g": "safe", "o": "open", "r": "violation", "x": "dead-code"}


class CFunctionReturnsiteSPOs(object):
    """Represents the supporting proof obligations associated with a return site.

    All return site supporting proof obligations are generated by the analyzer.
    """

    def __init__(self, cspos, xnode):
        self.cspos = cspos
        self.cfile = self.cspos.cfile
        self.context = self.cfile.contexttable.read_xml_context(xnode)
        self.cfun = self.cspos.cfun
        self.location = self.cfile.declarations.read_xml_location(xnode)
        self.returnexp = self.cfile.declarations.dictionary.read_xml_exp_opt(xnode)
        self.spos = {}  # pcid -> CFunctionReturnsiteSPO list
        self._initialize(xnode)

    def get_line(self):
        return self.location.getline()

    def get_cfg_context_string(self):
        return str(self.context)

    def get_spo(self, id):
        for pcid in self.spos:
            for spo in self.spos[pcid]:
                if spo.id == id:
                    return spo

    def has_spo(self, id):
        for pcid in self.spos:
            for spo in self.spos[pcid]:
                if spo.id == id:
                    return True
        return False

    def iter(self, f):
        for id in self.spos:
            for spo in self.spos[id]:
                f(spo)

    def write_xml(self, cnode):
        self.cfile.declarations.write_xml_location(cnode, self.location)
        self.cfile.contexttable.write_xml_context(cnode, self.context)
        self.cfile.declarations.dictionary.write_xml_exp_opt(cnode, self.returnexp)
        oonode = ET.Element("post-guarantees")
        for pcid in self.spos:
            pcnode = ET.Element("pc")
            pcnode.set("iipc", str(pcid))
            for spo in self.spos[pcid]:
                onode = ET.Element("po")
                spo.write_xml(onode)
                pcnode.append(onode)
            oonode.append(pcnode)
        cnode.extend([oonode])

    def _initialize(self, xnode):
        for p in xnode.find("post-guarantees").findall("pc"):
            iipc = int(p.get("iipc"))
            self.spos[iipc] = []
            for po in p.findall("po"):
                spotype = self.cfun.podictionary.read_xml_spo_type(po)
                deps = PO.get_dependencies(self, po)
                status = po_status[po.get("s", "o")]
                expl = None if po.find("e") is None else po.find("e").get("txt")
                diag = PO.get_diagnostic(po.find("d"))
                self.spos[iipc].append(
                    CFunctionReturnsiteSPO(self, spotype, status, deps, expl, diag)
                )
