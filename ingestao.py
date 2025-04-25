from google_play_scraper import reviews, Sort

app_id = 'br.com.gabba.Caixa' # ID do aplicativo
result, continuation_token = reviews(
    app_id,
    lang='pt',
    country='br',
    sort=Sort.MOST_RELEVANT,
    count=5
)

for review in result:
    print(review)
    print()