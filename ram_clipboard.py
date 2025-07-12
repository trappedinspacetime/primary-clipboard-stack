#!/usr/bin/env python3
import os
import sys
import time
import locale
from collections import deque
from Xlib import X, display
import subprocess

# Türkçe locale ayarı
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

class RamClipboard:
    def __init__(self, max_size=5):
        self.stack = deque(maxlen=max_size)
        self.max_size = max_size
    
    def push(self, item):
        if item and (not self.stack or item != self.stack[0]):
            self.stack.appendleft(item)
            return True
        return False
    
    def get(self, index):
        try:
            return self.stack[index]
        except IndexError:
            return None
    
    def reset(self):
        self.stack.clear()
        print("\nClipboard Stack RESETLENDİ!")

def get_primary_clipboard():
    try:
        return subprocess.check_output(
            ['xclip', '-o', '-selection', 'primary'],
            stderr=subprocess.DEVNULL,
            timeout=0.1  # Timeout ekledik
        ).decode('utf-8').strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return ""

def paste_text(text):
    try:
        subprocess.run(
            ['xdotool', 'type', '--clearmodifiers', '--delay', '0', text],
            check=True,
            timeout=0.5  # Timeout ekledik
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        try:
            d = display.Display()
            for char in text:
                keysym = d.keysym_to_keycode(ord(char))
                d.xtest_fake_input(X.KeyPress, keysym)
                d.xtest_fake_input(X.KeyRelease, keysym)
            d.sync()
        except:
            pass

def monitor_clipboard(clipboard):
    last_content = ""
    while True:
        try:
            current_content = get_primary_clipboard()
            if current_content and current_content != last_content:
                if clipboard.push(current_content):
                    print(f"\nClipboard Stack: {list(clipboard.stack)}")
                last_content = current_content
            time.sleep(0.2)  # CPU kullanımını azaltmak için bekleme
        except KeyboardInterrupt:
            break

def main():
    clipboard = RamClipboard()
    
    # Clipboard izleme thread'i
    monitor_thread = threading.Thread(
        target=monitor_clipboard, 
        args=(clipboard,),
        daemon=True
    )
    monitor_thread.start()
    
    try:
        d = display.Display()
        root = d.screen().root
        
        # Tuş kodlarını ayarla (1-6)
        keycodes = {
            1: d.keysym_to_keycode(ord('1')),
            2: d.keysym_to_keycode(ord('2')),
            3: d.keysym_to_keycode(ord('3')),
            4: d.keysym_to_keycode(ord('4')),
            5: d.keysym_to_keycode(ord('5')),
            6: d.keysym_to_keycode(ord('0'))  # Reset için
        }
        
        # Kısayolları kaydet
        for num, keycode in keycodes.items():
            root.grab_key(keycode, X.ControlMask, True, X.GrabModeAsync, X.GrabModeAsync)
        
        print("Türkçe karakter destekli clipboard aktif! Kullanım:")
        print("Ctrl+1..5: Stack'ten yapıştır | Ctrl+0: Stack'i resetle")
        
        while True:
            event = d.next_event()
            if event.type == X.KeyPress:
                # Ctrl+1..5 için
                for num in range(1, 6):
                    if event.detail == keycodes[num] and (event.state & X.ControlMask):
                        content = clipboard.get(num-1)
                        if content:
                            paste_text(content)
                
                # Ctrl+0 için resetleme
                if event.detail == keycodes[6] and (event.state & X.ControlMask):
                    clipboard.reset()
            
            time.sleep(0.01)  # Ana döngüde küçük bir bekleme

    except KeyboardInterrupt:
        print("\nProgram sonlandırılıyor...")
    finally:
        try:
            d.close()
        except:
            pass

if __name__ == "__main__":
    import threading
    main()
