# BreachForums Analysis Report

## 1. Executive Summary

In 2022/2023, BreachForums, a major cybercrime forum, experienced a significant data breach resulting in the public leak of its database. This event is noteworthy due to the forum's role in facilitating cybercriminal activities and the sensitive nature of the data involved. Our analysis of the leaked data, sourced from Resecurity and the public leak (databoose.sql), was conducted with an ethics-first approach. We prioritized privacy and security by avoiding the publication of raw data and focusing solely on safe aggregate metrics. This report presents our findings, which offer insights into user behavior, security practices, and demographic distribution within the BreachForums community.

## 2. Methodology

To ensure the safe handling of the leaked data, we employed a rigorous methodology:

1. **Data Isolation**: The SQL dump was parsed into a Docker-based MySQL environment, ensuring complete isolation from other systems.
2. **Data Cleaning**: We cleaned the schema, focusing on TEXT columns, and deduplicated records to maintain data integrity.
3. **Aggregation**: Using SQL INT queries, we generated aggregate statistics (e.g., counts, GROUP BY) and exported these as CSV files.
4. **Visualization**: The aggregated data was visualized using Python to facilitate analysis without exposing any personally identifiable information (PII).

## 3. Data Analysis Findings

### User Growth (Registration Trends)

The registration data indicates significant growth in user numbers over time, with notable spikes in certain months. For instance, there was a substantial increase in new user registrations in April 2024 (24,758 users), followed by a decrease in subsequent months. This pattern suggests periodic surges in forum interest or activity, potentially linked to specific events or topics of interest within the cybercrime community.

### Security Posture (Password Algorithms)

The analysis of password algorithms reveals that all users in the dataset utilized the Argon2i algorithm, a modern and secure choice for password hashing. However, the dataset did not provide information on two-factor authentication (2FA) usage, an area that could further inform the community's security practices.

### Demographics (Timezones/Languages)

The timezone distribution shows a concentration of users in UTC+0, with significant representation across various timezones, indicating a global user base. The language data, though limited, suggests a diverse community with widespread participation.

### Anomaly Detection (Email Domains, Usernames)

- **Email Domains**: The prevalence of email domains such as gmail.com (240,278 users) and proton.me (29,883 users) highlights a preference for mainstream and privacy-focused email services. The presence of lesser-known domains like cock.li and onionmail.org suggests attempts to maintain anonymity.
  
- **Usernames**: The majority of usernames are alphanumeric (322,912), with a small subset being purely numeric (1,074). The distribution of username lengths, peaking at 8 characters, indicates a tendency towards relatively short usernames, possibly for ease of use or memorability.

## 4. Conclusion

The BreachForums community, as revealed by the data, is characterized by rapid user growth, a strong security posture with modern password hashing, and a global, diverse demographic. Users exhibit a preference for privacy-centric email services and demonstrate a range of behaviors in username selection. This analysis provides valuable insights into the structure and dynamics of the community, emphasizing the importance of ethical data handling and privacy protection in cyber threat intelligence research.