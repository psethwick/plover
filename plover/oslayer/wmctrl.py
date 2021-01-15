
import sys


if sys.platform.startswith('win32'):

    from ctypes import windll

    GetForegroundWindow = windll.user32.GetForegroundWindow
    SetForegroundWindow = windll.user32.SetForegroundWindow


elif sys.platform.startswith('darwin'):

    from Cocoa import NSWorkspace, NSRunningApplication, NSApplicationActivateIgnoringOtherApps

    def GetForegroundWindow():
        return NSWorkspace.sharedWorkspace().frontmostApplication().processIdentifier()

    def SetForegroundWindow(pid):
        target_window = NSRunningApplication.runningApplicationWithProcessIdentifier_(pid)
        target_window.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)

elif sys.platform.startswith('linux'):

    from plover.oslayer.xwmctrl import WmCtrl

    wmctrl = WmCtrl()

    GetForegroundWindow = wmctrl.get_foreground_window
    SetForegroundWindow = wmctrl.set_foreground_window
