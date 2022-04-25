#! .\my_env\bin\ python
import CONST
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # both these options will be removed whe we launch officially
        page = browser.new_page()

        # this is the login logic, i'm removing it and going straight to the betting page to avoid signing in on every test run
        # page.goto(CONST.login_url)
        # page.fill('input#username', CONST[0])
        # page.fill('[id=password]', CONST[1]) #Decided to try both ways of selecting, both works
        # page.click('input[type=submit]') # i suspect just ['type=submit'] would work. but specifying input dosen't hurt

        page.goto(CONST.after_login)
        page.click('[data-sportid="2"]')
        page.wait_for_selector('[class="fob-featured-matches-container priority-events"]') # wait till this bets section loads before moving on
        # all_rows = page.query_selector_all('[class="fob-row col-container"]') # all rows of bets

        all_buttons_in_rows = page.query_selector_all('[class="clear-content fob-match-details fob-match-details-desktop"]')
        
        print(len(all_buttons_in_rows))

        for every_bet in all_buttons_in_rows:
            home_team_odds = 0
            home_team_name = 'default-team-name'
            home_team_selector = ''
            away_team_odds = 0
            away_team_selector = ''
            away_team_name = 'default-team-name'
            htsel = any
            atsel = any

            if every_bet.query_selector('button[data-label="H"]'):
                # print(every_bet.query_selector('button[data-label="H"]').inner_html())
                home_team_odds = float(every_bet.query_selector('[class="fob-bet-button"]').inner_text())
                home_team_name = every_bet.query_selector('[class="fob-hometeam"]').inner_text()
            print(f'{home_team_name} {home_team_odds}')

            if every_bet.query_selector('button[data-label="A"]'):

                away_team_odds = float(every_bet.query_selector('button[data-label="A"]').inner_text())
                away_team_name = every_bet.query_selector('[class="fob-awayteam"]').inner_text()
            print(f'{away_team_name} {away_team_odds}')

            ''' area below will actially click and buy the bets. 
                based on whats returned from chosefav()
                clicking based on the odds but... 
                there might be an issue if the same odd exist 
                for another team on the page
            ''' 
            if choose_fav(home_team_odds, away_team_odds, home_team_name, away_team_name) == 'home':
                page.click(f'button[data-value="{home_team_odds}"]')
            else:
                page.click(f'button[data-value="{away_team_odds}"]')
            print('#' * 20)

        page.wait_for_timeout(100000) # long timeout so the browser stays open (testing reasons)



def choose_fav(home, away, H, A): #this function calculates which team is the favourite. returns a string.
    if float(home) >= float(away):
        print(f'{A} is the favourites at {away}')

        return 'away' # basically if the team is playing at home and got same/equal ods then the home should be favourites
    else:
        print(f'{H} is the favourites at {home}')
        return 'home'


if __name__ == '__main__':
    main()