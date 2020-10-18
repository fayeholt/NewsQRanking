from newspaper import Article
import json
import requests

links = ["https://www.bbc.com/news/world-asia-54519628", 
"https://www.bbc.com/news/world-latin-america-54552921", 
"https://www.bbc.com/news/world-asia-54443119", 
"https://www.bbc.com/news/world-africa-54568055", 
"https://www.bbc.com/news/world-us-canada-54587863", 
"https://www.bbc.com/news/world-europe-54586437", 
"https://www.bbc.com/news/world-asia-54581830", 
"https://www.bbc.com/news/uk-54584583", 
"https://www.bbc.com/news/world-europe-54585828", 
"https://www.breitbart.com/europe/2020/10/17/report-anti-brexit-anti-trump-george-osborne-being-lined-up-as-next-bbc-chairman/", 
"https://www.breitbart.com/europe/2020/10/16/prison-staff-guarding-islamist-inmates-constant-threat-beheading/", 
"https://www.breitbart.com/europe/2020/10/15/blm-bandwagon-google-doodle-celebrates-black-nationalist-communist-activist-claudia-jones/", 
"https://www.breitbart.com/europe/2020/02/03/boris-admits-very-few-islamists-rehabilitated-favours-prison/", 
"https://www.breitbart.com/europe/2020/10/15/uk-spy-chief-confirms-tens-thousands-islamists-biggest-terror-threat-but-msm-hypes-far-right/", 
"https://www.breitbart.com/europe/2020/10/14/ethnic-pay-gap-data-shows-young-minorities-paid-more-than-young-whites/", 
"https://www.breitbart.com/europe/2020/10/14/stigma-of-white-privilege-toxic-masculinity-damaging-white-working-class-boys-report/", 
"https://www.breitbart.com/europe/2019/06/08/report-muslim-prison-gangs-forcing-inmates-convert-islam/", 
"https://www.breitbart.com/europe/2020/10/15/merkel-tells-eu-to-be-realistic-admits-uk-needs-good-deal-from-brussels/", 
"https://www.breitbart.com/europe/2020/10/11/post-brexit-britain-needs-president-trump-says-nigel-farage-as-bojos-government-courts-biden/", 
"https://www.breitbart.com/europe/2020/10/17/former-uk-deputy-prime-minister-nick-clegg-involved-in-facebooks-decision-to-censor-ny-post-hunter-biden-article-report/", 
"https://www.breitbart.com/europe/2020/10/16/farage-praises-boris-right-solution-preparing-uk-no-deal/", 
"https://www.breitbart.com/europe/2020/10/16/bbc-countryfile-presenter-countryside-is-racist/", 
"https://www.express.co.uk/news/royal/1349113/Prince-William-news-Meghan-Markle-Harry-Duchess-of-Sussex-Royal-latest", 
"https://www.express.co.uk/comment/expresscomment/1348851/brexit-news-nigel-farage-boris-johnson-eu-no-deal-latest", 
"https://www.express.co.uk/news/politics/1349035/brexit-news-trade-deal-EU-no-deal-withdrawal-agreement", 
"https://www.huffingtonpost.co.uk/entry/kevin-clarke-leslie-thomas-charges_uk_5f8478e4c5b6e6d033a5e54e", 
"https://www.huffpost.com/entry/a-second-national-lockdown-seems-inevitable-heres-what-stands-in-the-way_n_5f7dc203c5b6e5aba0d31ac2", 
"https://www.huffingtonpost.co.uk/entry/marcus-rashford-warns-boris-johnson-level-up-sticking-plaster-child-hunger_uk_5f8abb37c5b62dbe71c3172b", 
"https://www.huffingtonpost.co.uk/entry/boris-johnson-moonshot-tiers_uk_5f89fb4fc5b66ee9a5efcc47", 
"https://www.msn.com/en-gb/news/uknews/uk-eu-to-discuss-structure-of-brexit-talks-after-walkout-threat/ar-BB1a7X6k", 
"https://www.newstatesman.com/politics/2020/10/liberalism-will-remain-vulnerable-unless-it-can-speak-our-need-emotional", 
"https://www.newstatesman.com/world/africa/2020/10/end-sars-why-nigerians-are-protesting-hated-police-unit", 
"https://www.newstatesman.com/2020-10-16", 
"https://www.thecanary.co/feature/2020/10/12/the-government-is-legalising-and-extending-this-infamous-spycops-criminal-actions-and-you-could-be-a-victim/", 
"https://www.thecanary.co/uk/analysis/2020/10/09/we-face-a-quiet-threat-to-the-independence-of-our-elections-we-must-be-vigilant/", 
"https://www.thecanary.co/opinion/2020/10/13/we-need-to-smash-starmer-and-johnsons-disgusting-duopoly-thats-why-im-running-for-london-mayor/", 
"https://www.thecanary.co/uk/analysis/2020/10/15/police-admit-that-they-used-at-least-six-undercover-officers-to-spy-on-one-woman/", 
"https://www.economist.com/britain/2020/10/17/covid-19-is-limiting-access-to-maternity-services-for-british-fathers", 
"https://www.theguardian.com/us-news/2020/oct/17/new-trump-golf-course-provokes-fury-in-scotland", 
"https://www.msn.com/en-gb/news/uknews/coronavirus-poll-shows-lack-of-trust-in-boris-johnson-as-britons-feel-the-financial-pinch-from-pandemic/ar-BB1a8ezY", 
"https://www.msn.com/en-gb/news/uknews/jennifer-arcuri-admits-to-having-an-affair-with-boris-johnson-while-he-was-london-mayor/ar-BB1a7HCT", 
"https://www.independent.co.uk/news/world/europe/france-terror-attack-paris-samuel-paty-macron-charlie-hebdo-teacher-death-latest-b1098109.html", 
"https://www.independent.co.uk/news/uk/politics/bmg-poll-coronavirus-boris-johnson-matt-hancock-b1078965.html", 
"https://www.independent.co.uk/news/uk/home-news/salisbury-novichok-police-officer-quit-resign-b1105226.html", 
"https://www.independent.co.uk/news/health/coronavirus-police-test-and-trace-isolation-quarantine-law-b1110635.html", 
"https://www.independent.co.uk/independentpremium/news-analysis/uk-economy-health-coronavirus-pandemic-advice-b1037422.html", 
"https://www.independent.co.uk/news/world/europe/france-terror-attack-paris-samuel-paty-macron-charlie-hebdo-teacher-death-latest-b1098109.html", 
"https://www.independent.co.uk/independentpremium/business/ethnicity-pay-gap-gender-lloyds-cbi-tuc-chambers-of-commerce-b1046925.html", 
"https://metro.co.uk/2020/10/17/detective-who-nearly-died-from-salisbury-novichok-poisonings-quits-force-13439810/", 
"https://www.mirror.co.uk/news/politics/tony-blair-denies-breaking-coronavirus-22863982", 
"https://www.mirror.co.uk/news/us-news/trump-rally-chants-lock-up-22864048", 
"https://www.thesun.co.uk/news/12957484/uk-heading-tragedy-of-historic-proportions-church-decline/", 
"https://www.thesun.co.uk/news/12956877/government-bombard-migrants-facebook-ads-renounce/"
]

longString = ""

for i in links:

    try: 
        article = Article(i)

        article.download()

        article.parse()

        longString = longString + article.text

        print (article.title)
        printThingy = article.publish_date
        print (str(printThingy)[0:10])
    
    except: 
        pass

longString.replace("\"", "")

# with open('right.json', 'w') as f:
#     json.dump(longString, f)

