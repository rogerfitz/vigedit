# coding: spec

from gi.repository import Gedit

from tests.helpers import GeditTestCase

describe GeditTestCase, "Helpers":
    describe "Text":
        it "can set and get text from the buffer":
            self.gedit.text = "hello there"
            self.gedit.text |should| equal_to("hello there")
    
    describe "Tabs":
        it "can create and count tabs":
            self.gedit.tabs |should| have(1).tab
            self.gedit.add_tab()
            self.gedit.tabs |should| have(2).tabs
