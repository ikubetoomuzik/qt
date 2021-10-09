#! /usr/bin/python

from qtrade import Questrade;
from functools import reduce;
from os import getenv;
import multiprocessing;
import time;

# Set your personal SPACING option.
SPACING = '{F2}    {/F}'

def get_cash_info(qt: Questrade, acct: int) -> str:
    bal_response = qt._send_message('get', 'accounts/' + str(acct) + '/balances')
    temp = qt._send_message('get', 'accounts/' + str(acct) + '/positions')
    print(temp);
    try:
        cash = round(bal_response['perCurrencyBalances'][0]['cash'], 2);
    except Exception:
        raise Exception;
    result = '{F2}Cash{F1}: $';
    result += '{:.2f}'.format(cash);
    result += '{/F}'
    return result;

def gen_position_display(acc: str,pos: dict) -> str:
    # Pull the basic values out of position dict.
    symbol = pos['symbol'];
    start_investment = round(pos['totalCost'], 2);
    current_val = round(pos['currentMarketValue'], 2);
    try:
        day_pnl = round(pos['dayPnl'], 2);
    except:
        day_pnl = 0.00;
    overall_pnl = round(pos['openPnl'], 2);
    # Calculate start val with pulled vals.
    start_val = round(current_val - day_pnl, 2);
    # Gen the percent values.
    day_pnl_perc = round(day_pnl / start_val * 100, 2);
    overall_pnl_perc = round(overall_pnl / start_investment * 100, 2);
    # Gen the daily percent font colour.
    if day_pnl_perc >= 0 and day_pnl_perc < 1:
        day_fnt = 5
    elif day_pnl_perc >= 0:
        day_fnt = 3;
    else:
        day_fnt = 4;
        day_pnl_perc *= -1;
    # Gen the overall percent font colour.
    if overall_pnl_perc >= 0 and overall_pnl_perc < 1:
        overall_fnt = 5
    elif overall_pnl_perc >= 0:
        overall_fnt = 3;
    else:
        overall_fnt = 4;
        overall_pnl_perc *= -1;
    result = '{F2}';
    result += symbol;
    result += '{F1}: $';
    result += '{:.2f}'.format(current_val);
    result += SPACING;
    result +='{F';
    result += str(day_fnt);
    result += '}';
    result += '{:.2f}'.format(day_pnl_perc);
    result += '%';
    result += SPACING;
    result += '{F';
    result += str(overall_fnt);
    result += '}';
    result += '{:.2f}'.format(overall_pnl_perc);
    result += '%';
    result += SPACING;
    return acc + result;


def get_position_info(qt: Questrade, acct: int) -> str:
    positions = qt.get_account_positions(account_id=acct);
    print(positions);
    return reduce(gen_position_display, positions, '  ');

def gen_string():
    # Defining the token location.
    access_info = getenv('HOME') + '/.config/questrade/access_token.yml';
    # Start the link using loaded conf.
    qt = Questrade(token_yaml=access_info);
    # we try up to three times to make requests.
    for _ in range(3):
        try:
            # Only have one account so we grab first entry.
            acct = qt.get_account_id()[0];
            # Get the info for all positions held.
            positions = get_position_info(qt, acct);
            # Get the specific cash balance info.
            cash = get_cash_info(qt, acct);
            break;
        except:
            # If the initial request fails then we refresh and try again.
            qt.refresh_access_token();
            # Save our newly generated token for next time.
            qt.save_token_to_yaml(yaml_path=access_info);
            continue;
    # then we print the result
    print(positions + cash, end = '');

# generate the output
# we are using multiprocessing to limit the request to 5 seconds.
process = multiprocessing.Process(target=gen_string);
# start running the process.
process.start();
# wait for 5 seconds or however long the process takes to finish.
process.join(5);
# check if the process is still running.
if process.is_alive():
    # now we kill it.
    process.kill();
    # and then just wait to finish.
    process.join();


# vim:ft=python
