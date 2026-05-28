import subprocess
import time
import cv2
import numpy as np
import random

class DBLCoopFarmer:
    def __init__(self):
        self.adb_path = r"C:\Users\theof\AppData\Local\Android\Sdk\platform-tools\adb.exe"
        self.cards = [(404, 1815), (625, 1803), (781, 1733), (942, 1700)]
        self.rising_rush_coords = (905, 1329)

    def take_screenshot(self):
        pipe = subprocess.Popen([self.adb_path, 'shell', 'screencap', '-p'], stdout=subprocess.PIPE)
        image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
        if not image_bytes: return None
        image_array = np.frombuffer(image_bytes, np.uint8)
        return cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    def is_image_on_screen(self, template_path, threshold=0.8):
        screen = self.take_screenshot()
        if screen is None: return False
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None: return False
        
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        return max_val >= threshold

    def find_and_tap(self, template_path, threshold=0.8):
        screen = self.take_screenshot()
        if screen is None: return False
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None: return False
        
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            h, w = template.shape[:-1]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            self.tap(center_x, center_y)
            return True
        return False

    def tap(self, x, y):
        subprocess.run([self.adb_path, 'shell', 'input', 'tap', str(x), str(y)])

    def spam_arts_cards(self):
        chosen_cards = random.sample(self.cards, 2)
        for x, y in chosen_cards:
            self.tap(x, y)

    def run_combat(self):
        print(">>> COMBAT INITIATED <<<")
        loop_counter = 0

        while True:
            loop_counter += 1
            self.spam_arts_cards()

            if loop_counter % 2 == 0:
                if self.is_image_on_screen('templates/rr_ready.png'):
                    print("[VISION] Rising Rush is glowing!")
                    # Keep shield at 0.92 so it doesn't accidentally fire from background colors
                    if not self.is_image_on_screen('templates/blue_shield.png', threshold=0.92):
                        print("[*** TRIGGER ***] Shield is DOWN! Firing Rising Rush!")
                        self.tap(self.rising_rush_coords[0], self.rising_rush_coords[1])
                        time.sleep(1) 
                        
                        random_card = random.choice(self.cards)
                        time.sleep(2) 
                        self.tap(random_card[0], random_card[1])
                        print("[COMBAT] RR Card selected.")

                        print("[COMBAT] Waiting for the clash animation...")
                        time.sleep(4) 
                        
                        print(">>> SPAMMING THE METER! <<<")
                        for _ in range(10):
                            self.tap(540, 1200)
                            
                        print("[COMBAT] Meter locked in. Resuming normal combat...")
                        time.sleep(10) 
                    else:
                        print("[VISION] Shield is still up. Holding RR.")

            if loop_counter % 5 == 0:
                print("[COMBAT] Checking if battle is over...")
                self.tap(540, 1000) 
                
                # FIXED: Raised to 0.65. Low enough to bypass transparency, high enough to ignore fireballs.
                if self.is_image_on_screen('templates/ok_button.png', threshold=0.65) or \
                   self.is_image_on_screen('templates/rematch_button.png', threshold=0.7):
                    print(">>> BATTLE WON! Exiting combat mode. <<<")
                    time.sleep(2) 
                    break 

    def auto_farm_loop(self):
        print(">>> MASTER AUTO-FARMER ONLINE <<<")
        print("Leave the bot running. It will navigate menus and fight automatically.")
        
        while True:
            # FIXED: Raised to 0.7 so it doesn't click random yellow UI elements
            if self.find_and_tap('templates/rematch_button.png', threshold=0.7):
                print("[MENU] Clicked Rematch! Searching for a partner...")
                time.sleep(5) 
                continue 

            # FIXED: Raised to 0.75 so it strictly waits for the actual Ready button
            if self.find_and_tap('templates/ready_button.png', threshold=0.75):
                print("[MENU] Partner found! Clicked Ready!")
                print("[MENU] Waiting 12 seconds for the match to load...")
                time.sleep(12) 
                self.run_combat() 
                continue 

            # FIXED: OK button set to 0.65
            if self.find_and_tap('templates/ok_button.png', threshold=0.65):
                print("[MENU] Clearing rewards...")
                time.sleep(2)
                continue
            
            print("[MENU] Scanning for menus...")
            self.tap(540, 1000) 
            time.sleep(2)

if __name__ == "__main__":
    bot = DBLCoopFarmer()
    bot.auto_farm_loop()