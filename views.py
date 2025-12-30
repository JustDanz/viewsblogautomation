import requests
import time
import random
from datetime import datetime
import sys


class BloggerTrafficSimulator:
    def __init__(self):
        self.user_agents = [
            # Desktop User-Agents
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            
            # Mobile User-Agents
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 14; SM-A146B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36"
        ]
        
        self.session = requests.Session()
        self.stats = {
            'total_visits': 0,
            'successful_visits': 0,
            'failed_visits': 0,
            'start_time': None,
            'end_time': None
        }
    
    def get_random_user_agent(self):
        """Mengembalikan User-Agent acak dari daftar"""
        return random.choice(self.user_agents)
    
    def get_random_delay(self, min_delay=5, max_delay=30):
        """Mengembalikan delay acak dalam detik"""
        return random.uniform(min_delay, max_delay)
    
    def make_request(self, url, user_agent):
        """Melakukan HTTP GET request ke target URL"""
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        try:
            response = self.session.get(url, headers=headers, timeout=10)
            return response
        except requests.exceptions.RequestException as e:
            print(f"    Error: {str(e)}")
            return None
    
    def log_visit(self, timestamp, user_agent, status_code, url):
        """Mencatat kunjungan ke log"""
        log_entry = f"[{timestamp}] User-Agent: {user_agent[:50]}... | Status: {status_code} | URL: {url}"
        print(log_entry)
        
        # Juga simpan ke file log
        with open('traffic_simulator.log', 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def simulate_visit(self, url, visit_number, total_visits):
        """Simulasi satu kunjungan"""
        user_agent = self.get_random_user_agent()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n[Visit {visit_number}/{total_visits}]")
        print(f"    Time: {timestamp}")
        print(f"    Using: {'Mobile' if 'Mobile' in user_agent else 'Desktop'} User-Agent")
        
        response = self.make_request(url, user_agent)
        
        if response is not None:
            status_code = response.status_code
            self.stats['successful_visits'] += 1
            
            if 200 <= status_code < 300:
                print(f"    Status: {status_code} (Success)")
            elif 400 <= status_code < 500:
                print(f"    Status: {status_code} (Client Error)")
            else:
                print(f"    Status: {status_code} (Other)")
        else:
            status_code = "ERROR"
            self.stats['failed_visits'] += 1
        
        self.log_visit(timestamp, user_agent, status_code, url)
        return status_code
    
    def run_simulation(self, url, num_visits, min_delay=5, max_delay=30):
        """Menjalankan simulasi kunjungan"""
        print("\n" + "="*60)
        print("BLOGGER TRAFFIC SIMULATOR")
        print("="*60)
        print(f"Target URL: {url}")
        print(f"Number of visits: {num_visits}")
        print(f"Delay range: {min_delay}-{max_delay} seconds")
        print("="*60 + "\n")
        
        self.stats['start_time'] = datetime.now()
        self.stats['total_visits'] = num_visits
        
        print("Starting simulation...\n")
        
        for i in range(1, num_visits + 1):
            status = self.simulate_visit(url, i, num_visits)
            
            # Jangan delay setelah kunjungan terakhir
            if i < num_visits:
                delay = self.get_random_delay(min_delay, max_delay)
                print(f"    Next visit in {delay:.1f} seconds...")
                time.sleep(delay)
        
        self.stats['end_time'] = datetime.now()
        self.display_summary()
    
    def display_summary(self):
        """Menampilkan ringkasan statistik simulasi"""
        duration = self.stats['end_time'] - self.stats['start_time']
        
        print("\n" + "="*60)
        print("SIMULATION SUMMARY")
        print("="*60)
        print(f"Total visits attempted: {self.stats['total_visits']}")
        print(f"Successful visits: {self.stats['successful_visits']}")
        print(f"Failed visits: {self.stats['failed_visits']}")
        print(f"Start time: {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"End time: {self.stats['end_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total duration: {duration}")
        print(f"Log file: traffic_simulator.log")
        print("="*60)


def get_configuration():
    """Mendapatkan konfigurasi dari pengguna"""
    print("\nBlogger Traffic Simulator Configuration")
    print("-" * 40)
    
    url = input("Enter Blogger URL (e.g., https://yourblog.blogspot.com): ").strip()
    
    while True:
        try:
            num_visits = int(input("Number of visits to simulate (1-1000): ").strip())
            if 1 <= num_visits <= 1000:
                break
            else:
                print("Please enter a number between 1 and 1000.")
        except ValueError:
            print("Please enter a valid number.")
    
    while True:
        try:
            delay_input = input("Delay range between visits (e.g., '5-30' seconds): ").strip()
            min_delay, max_delay = map(float, delay_input.split('-'))
            if 0 < min_delay <= max_delay:
                break
            else:
                print("Please enter a valid range (min-max, e.g., 5-30).")
        except (ValueError, IndexError):
            print("Please enter a valid range in format 'min-max'.")
    
    return url, num_visits, min_delay, max_delay


def display_disclaimer():
    """Menampilkan disclaimer penggunaan"""
    disclaimer = """
    ════════════════════════════════════════════════════════════════
    DISCLAIMER: ETIKA PENGGUNAAN
    ════════════════════════════════════════════════════════════════
    
    Alat ini HANYA diperuntukkan untuk:
    1. Blog pribadi milik sendiri
    2. Testing lingkungan lokal/server pribadi
    3. Analisis performa website sendiri
    
    PENGGUNAAN YANG DILARANG:
    • Memanipulasi sistem analitik pihak ketiga
    • Mengganggu website/orang lain
    • Menggunakan botnet, proxy ilegal, atau teknik eksploitasi
    • Pelanggaran Terms of Service platform manapun
    
    Gunakan alat ini dengan bertanggung jawab.
    ════════════════════════════════════════════════════════════════
    """
    print(disclaimer)
    
    response = input("Do you understand and agree to these terms? (yes/no): ").strip().lower()
    return response == 'yes'


def main():
    """Fungsi utama"""
    print("Blogger Traffic Simulator v1.0")
    print("Designed for performance testing and traffic analysis\n")
    
    if not display_disclaimer():
        print("\nYou must agree to the terms to use this tool.")
        sys.exit(0)
    
    # Konfigurasi otomatis untuk testing (bisa di-uncomment untuk penggunaan cepat)
    """
    # Contoh konfigurasi
    url = "https://example.blogspot.com"
    num_visits = 10
    min_delay = 5
    max_delay = 15
    """
    
    # Atau dapatkan konfigurasi dari user
    url, num_visits, min_delay, max_delay = get_configuration()
    
    # Jalankan simulasi
    simulator = BloggerTrafficSimulator()
    
    try:
        simulator.run_simulation(url, num_visits, min_delay, max_delay)
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
        simulator.display_summary()
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")


if __name__ == "__main__":
    main()