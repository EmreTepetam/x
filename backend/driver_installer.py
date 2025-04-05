import os
import subprocess
import concurrent.futures

class DriverInstaller:
    def __init__(self, driver_folder_path):
        self.driver_folder_path = driver_folder_path

    def scan_and_categorize_drivers(self):
        driver_files = self.findDriverFiles(self.driver_folder_path)
        return self.categorizeDrivers(driver_files)

    def findDriverFiles(self, path):
        driver_files = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(('.exe', '.inf', '.sys')):
                    driver_files.append(os.path.join(root, file))
        return driver_files

    def categorizeDrivers(self, driver_files):
        categories = {}
        for file in driver_files:
            category = self.identifyCategory(file)
            if category not in categories:
                categories[category] = []
            categories[category].append(file)
        return categories

    def identifyCategory(self, file_path):
        try:
            category = os.path.basename(os.path.dirname(file_path))
            print(f"Category: {category}")
            return category
        except Exception as e:
            print(f"Error identifying category: {e}")
            return 'Other Drivers'

    def getFullPath(self, category_item, file_name):
        for index in range(category_item.childCount()):
            item = category_item.child(index)
            if item.text(0) == file_name:
                return os.path.join(self.driver_folder_path, category_item.text(0), file_name)
        return None

    def installDrivers(self, driver_files):
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(self.installDriver, file) for file in driver_files]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error installing driver: {e}")

    def installDriver(self, file):
        try:
            if file.endswith('.exe'):
                print(f"Installing executable: {file}")
                subprocess.run([file], check=True)
            elif file.endswith('.inf'):
                print(f"Installing driver: {file}")
                subprocess.run(['pnputil', '/add-driver', file, '/install'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Installation failed for {file}: {e}")
