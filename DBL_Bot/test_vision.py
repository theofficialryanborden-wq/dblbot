import subprocess

print("Attempting to take a screenshot of your phone...")

# This points to the tool that talks to your phone. 
# Change the path if you didn't put it straight on your C: drive.
adb_path = r"C:\platform-tools-latest-windows\platform-tools\adb.exe" 

try:
    # This tells the phone to take a screenshot and send the data back to Python
    pipe = subprocess.Popen([adb_path, 'shell', 'screencap', '-p'], stdout=subprocess.PIPE)
    image_bytes = pipe.stdout.read()
    
    # This fixes a small formatting issue between Android and Windows
    image_bytes = image_bytes.replace(b'\r\n', b'\n') 

    # This creates a new image file in your folder and saves the picture data into it
    with open("test_screen.png", "wb") as f:
        f.write(image_bytes)
        
    print("Success! Check your DBL_Bot folder for test_screen.png")

except Exception as e:
    print(f"Uh oh, something went wrong: {e}")