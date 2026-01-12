-- metrics.sql
-- Purpose: Generate SAFE aggregate statistics for BreachForums analysis.
-- SAFETY: NO SELECT * or PII columns (username, email, password) allowed.

SELECT "--- SCHEMA SUMMARY ---" as output_section;
DESCRIBE hcclmafd2jnkwmfufmybb_users;

SELECT "--- TOTAL USERS ---" as output_section;
SELECT COUNT(*) as total_users FROM hcclmafd2jnkwmfufmybb_users;

SELECT "--- PASSWORD ALGORITHM DISTRIBUTION ---" as output_section;
SELECT 
    password_algorithm, 
    COUNT(*) as count 
FROM hcclmafd2jnkwmfufmybb_users 
GROUP BY password_algorithm 
ORDER BY count DESC;

SELECT "--- 2FA ADOPTION ---" as output_section;
-- 'has_my2fa' is likely 0 or 1
SELECT 
    has_my2fa, 
    COUNT(*) as count 
FROM hcclmafd2jnkwmfufmybb_users 
GROUP BY has_my2fa;

SELECT "--- REGISTRATION YEAR/MONTH HISTOGRAM ---" as output_section;
-- regdate is likely a unix timestamp. Convert to YYYY-MM.
SELECT 
    FROM_UNIXTIME(regdate, '%Y-%m') as reg_month, 
    COUNT(*) as new_users 
FROM hcclmafd2jnkwmfufmybb_users 
GROUP BY reg_month 
ORDER BY reg_month ASC;

SELECT "--- USERGROUP DISTRIBUTION ---" as output_section;
SELECT 
    usergroup, 
    COUNT(*) as count 
FROM hcclmafd2jnkwmfufmybb_users 
GROUP BY usergroup 
ORDER BY count DESC 
LIMIT 20;

SELECT "--- LANGUAGE DISTRIBUTION ---" as output_section;
SELECT 
    language, 
    COUNT(*) as count 
FROM hcclmafd2jnkwmfufmybb_users 
GROUP BY language 
ORDER BY count DESC;

SELECT "--- TIMEZONE DISTRIBUTION ---" as output_section;
SELECT 
    timezone, 
    COUNT(*) as count 
FROM hcclmafd2jnkwmfufmybb_users 
GROUP BY timezone 
ORDER BY count DESC;



SELECT "--- EMAIL TOP DOMAINS ---" as output_section;
SELECT 
    SUBSTRING_INDEX(email, '@', -1) as domain, 
    COUNT(*) as count 
FROM hcclmafd2jnkwmfufmybb_users 
GROUP BY domain 
ORDER BY count DESC 
LIMIT 50;

SELECT "--- EMAIL TLD DISTRIBUTION ---" as output_section;
SELECT 
    SUBSTRING_INDEX(email, '.', -1) as tld, 
    COUNT(*) as count 
FROM hcclmafd2jnkwmfufmybb_users 
GROUP BY tld 
ORDER BY count DESC 
LIMIT 20;

SELECT "--- USERNAME LENGTH DISTRIBUTION ---" as output_section;
SELECT 
    LENGTH(username) as name_len, 
    COUNT(*) as count 
FROM hcclmafd2jnkwmfufmybb_users 
GROUP BY name_len 
ORDER BY name_len ASC;

SELECT "--- USERNAME COMPLETELY NUMERIC ---" as output_section;
SELECT 
    IF(username REGEXP '^[0-9]+$', 'Numeric', 'Alphanumeric') as type,
    COUNT(*) as count
FROM hcclmafd2jnkwmfufmybb_users
GROUP BY type;

