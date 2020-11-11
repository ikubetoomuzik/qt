#! /usr/bin/python

from qtrade import Questrade;
from functools import reduce;
import os;

# old script
# access_info = os.getenv('HOME') + '/.config/questrade/access_token.yml';
# qt = Questrade(token_yaml=access_info);
# Make sure our token is up to date and wont expire.
# qt.refresh_access_token();
# qt.save_token_to_yaml(yaml_path=access_info);
# temp.
qt = Questrade('tGUD1Hr6cD2KfaVnBwFvZGzifg-_BoN30');
# Only have one account so we grab first entry.
acct = qt.get_account_id()[0];
# My account balance code.
bal_response = qt._send_message('get', 'accounts/' + str(acct) + '/balances')
try:
    cash = round(bal_response['perCurrencyBalances'][0]['cash'], 2)
except Exception:
    print(resp);
    raise Exception
# Right now we are only investing in one index fund, so the positions work as a balance.
pos = qt.get_account_positions(account_id=acct)[0];
symbol = pos['symbol'];
start_investment = round(pos['totalCost'], 2);
current_val = round(pos['currentMarketValue'], 2);
day_pnl = round(pos['dayPnl'], 2);
overall_pnl = round(pos['openPnl'], 2);
start_val = round(current_val - day_pnl, 2);
day_pnl_perc = round(day_pnl / start_val * 100, 2);
overall_pnl_perc = round(overall_pnl / start_investment * 100, 2);
if day_pnl_perc >= 0 and day_pnl_perc < 1:
    day_fnt = 5
elif day_pnl_perc >= 0:
    day_fnt = 3;
else:
    day_fnt = 4;
    day_pnl_perc = day_pnl_perc[1:];
if overall_pnl_perc >= 0 and overall_pnl_perc < 1:
    overall_fnt = 5
elif overall_pnl_perc >= 0:
    overall_fnt = 3;
else:
    overall_fnt = 4;
    overall_pnl_perc = overall_pnl_perc[1:];
spacing = '{F2} |  {/F}'
display_str = '{F2} ';
display_str += symbol;
display_str += ':{F1} $';
display_str += '{:.2f}'.format(current_val);
display_str += spacing;
display_str +='{F';
display_str += str(day_fnt);
display_str += '}';
display_str += '{:.2f}'.format(day_pnl_perc);
display_str += '%';
display_str += spacing;
display_str += '{F';
display_str += str(overall_fnt);
display_str += '}';
display_str += '{:.2f}'.format(overall_pnl_perc);
display_str += '%';
display_str += spacing;
display_str += '{F2}Cash:{F1} $';
display_str += '{:.2f}'.format(cash);
display_str += '{/F}'
print(display_str, end = '');

# def get_cash_info(qt: Questrade, acct: int) -> str:
#     bal_response = qt._send_message('get', 'accounts/' + str(acct) + '/balances')
#     try:
#         cash = round(bal_response['perCurrencyBalances'][0]['cash'], 2);
#     except Exception:
#         print(resp);
#         raise Exception;
#     result = '{F2}Cash:{F1} $';
#     result += '{:.2f}'.format(cash);
#     result += '{/F}'
#     return result;
# def gen_position_display(acc,pos):
#     spacing = '{F2} |  {/F}'
#     # Pull the basic values out of position dict.
#     symbol = pos['symbol'];
#     start_investment = round(pos['totalCost'], 2);
#     current_val = round(pos['currentMarketValue'], 2);
#     day_pnl = round(pos['dayPnl'], 2);
#     overall_pnl = round(pos['openPnl'], 2);
#     # Calculate start val with pulled vals.
#     start_val = round(current_val - day_pnl, 2);
#     # Gen the percent values.
#     day_pnl_perc = round(day_pnl / start_val * 100, 2);
#     overall_pnl_perc = round(overall_pnl / start_investment * 100, 2);
#     # Gen the daily percent font colour.
#     if day_pnl_perc >= 0 and day_pnl_perc < 1:
#         day_fnt = 5
#     elif day_pnl_perc >= 0:
#         day_fnt = 3;
#     else:
#         day_fnt = 4;
#         day_pnl_perc = day_pnl_perc[1:];
#     # Gen the overall percent font colour.
#     if overall_pnl_perc >= 0 and overall_pnl_perc < 1:
#         overall_fnt = 5
#     elif overall_pnl_perc >= 0:
#         overall_fnt = 3;
#     else:
#         overall_fnt = 4;
#         overall_pnl_perc = overall_pnl_perc[1:];
#     result = '{F2}';
#     result += symbol;
#     result += ':{F1} $';
#     result += '{:.2f}'.format(current_val);
#     result += spacing;
#     result +='{F';
#     result += str(day_fnt);
#     result += '}';
#     result += '{:.2f}'.format(day_pnl_perc);
#     result += '%';
#     result += spacing;
#     result += '{F';
#     result += str(overall_fnt);
#     result += '}';
#     result += '{:.2f}'.format(overall_pnl_perc);
#     result += '%';
#     result += spacing;
#     return acc + result;
# def get_position_info(qt: Questrade, acct: int) -> str:
#     positions = qt.get_account_positions(account_id=acct);
#     result = reduce(gen_position_display, positions, '  ');
#     return result;
# def gen_string():
#     # Defining the token location.
#     access_info = os.getenv('HOME') + '/.config/questrade/access_token.yml';
#     # Start the link using loaded conf.
#     qt = Questrade(token_yaml=access_info);
#     # Make sure our token is up to date and wont expire.
#     qt.refresh_access_token();
#     qt.save_token_to_yaml(yaml_path=access_info);
#     # Only have one account so we grab first entry.
#     acct = qt.get_account_id()[0];
#     # Get the info for all positions held.
#     positions = get_position_info(qt, acct);
#     cash = get_cash_info(qt, acct);
#     print(positions + cash, end = '');
# gen_string();

# vim:ft=python
