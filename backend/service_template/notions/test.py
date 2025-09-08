test_days = "15,10,5,0,neg"
day_tokens = test_days.split(",")
print(day_tokens)
for token in day_tokens:
    print(token)
    clean_token = token.strip()
    print(clean_token)