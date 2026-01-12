import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

# Configuration
INPUT_DIR = "../outputs/aggregates/"
OUTPUT_DIR = "../outputs/figures/"

def setup_dirs():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def plot_password_algos(df):
    """Expects columns: password_algorithm, count"""
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df.head(10), x='count', y='password_algorithm', palette='viridis')
    plt.title('Top 10 Password Hashing Algorithms')
    plt.xlabel('User Count')
    plt.ylabel('Algorithm')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'password_algos.png'))
    plt.close()

def plot_registration_timeline(df):
    """Expects columns: reg_month, new_users"""
    plt.figure(figsize=(12, 6))
    df['reg_month'] = pd.to_datetime(df['reg_month'])
    sns.lineplot(data=df, x='reg_month', y='new_users')
    plt.title('New User Registrations Over Time')
    plt.xlabel('Month')
    plt.ylabel('New Users')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'registration_growth.png'))
    plt.close()

def plot_bar_chart(df, x_col, y_col, title, filename, top_n=20):
    """Generic bar chart plotter"""
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df.head(top_n), x=x_col, y=y_col, palette='viridis')
    plt.title(title)
    plt.xlabel('Count')
    plt.ylabel(y_col)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename))
    plt.close()

def main():
    setup_dirs()
    print(f"[*] Scanning {INPUT_DIR} for aggregate CSVs...")
    
    # This script assumes specific CSV filenames or structure.
    try:
        # Load Algo Stats
        algo_file = os.path.join(INPUT_DIR, "password_algos.csv")
        if os.path.exists(algo_file):
            print("[+] Generating password algo chart...")
            df_algo = pd.read_csv(algo_file)
            plot_password_algos(df_algo)
            
        # Load Reg Stats
        reg_file = os.path.join(INPUT_DIR, "registration_stats.csv")
        if os.path.exists(reg_file):
            print("[+] Generating registration timeline...")
            df_reg = pd.read_csv(reg_file)
            plot_registration_timeline(df_reg)

        # Load Language Stats
        lang_file = os.path.join(INPUT_DIR, "language_dist.csv")
        if os.path.exists(lang_file):
            print("[+] Generating language distribution...")
            df_lang = pd.read_csv(lang_file)
            plot_bar_chart(df_lang, 'count', 'language', 'User Language Distribution', 'language_dist.png')

        # Load Timezone Stats
        tz_file = os.path.join(INPUT_DIR, "timezone_dist.csv")
        if os.path.exists(tz_file):
            print("[+] Generating timezone distribution...")
            df_tz = pd.read_csv(tz_file)
            plot_bar_chart(df_tz, 'count', 'timezone', 'User Timezone Distribution', 'timezone_dist.png')

        # Load Email Domain Stats
        domain_file = os.path.join(INPUT_DIR, "email_domains.csv")
        if os.path.exists(domain_file):
            print("[+] Generating email domain chart...")
            df_domain = pd.read_csv(domain_file)
            plot_bar_chart(df_domain, 'count', 'domain', 'Top Email Domains', 'email_domains.png', top_n=20)

        # Load TLD Stats
        tld_file = os.path.join(INPUT_DIR, "email_tlds.csv")
        if os.path.exists(tld_file):
            print("[+] Generating TLD distribution...")
            df_tld = pd.read_csv(tld_file)
            plot_bar_chart(df_tld, 'count', 'tld', 'Top Top-Level Domains', 'email_tlds.png', top_n=15)

        # Load Username Lengths
        len_file = os.path.join(INPUT_DIR, "username_lengths.csv")
        if os.path.exists(len_file):
            print("[+] Generating username length histogram...")
            df_len = pd.read_csv(len_file)
            plt.figure(figsize=(12, 6))
            sns.barplot(data=df_len, x='name_len', y='count', color='skyblue')
            plt.title('Username Length Distribution')
            plt.xlabel('Length (Chars)')
            plt.ylabel('Count')
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, 'username_lengths.png'))
            plt.close()

        # Load Username Types (Numeric vs Alpha)
        type_file = os.path.join(INPUT_DIR, "username_types.csv")
        if os.path.exists(type_file):
            print("[+] Generating username type chart...")
            df_type = pd.read_csv(type_file)
            plt.figure(figsize=(6, 6))
            colors = sns.color_palette('pastel')[0:len(df_type)]
            plt.pie(df_type['count'], labels=df_type['type'], colors=colors, autopct='%.1f%%')
            plt.title('Username Format')
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, 'username_types.png'))
            plt.close()
            
    except Exception as e:
        print(f"[!] Error processing charts: {e}")

if __name__ == "__main__":
    main()
