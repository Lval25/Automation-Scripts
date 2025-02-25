from booking.booking import Booking
import time

try:
    with Booking() as bot:
        bot.land_first_page()
        print("Exiting...")
        bot.change_currensy(currency='USD')
        bot.place_to_go(input("Where do you want to go?"))
        bot.choose_date(input("What is the check in date?"), input("What is the check out date?"))
        bot.occupancy(int(input("How many?")))
        bot.click_search()
        bot.booking_filtration()
        bot.refresh() # A workaround to get the data properly
        bot.report_results()
        time.sleep(10)

except Exception as e:
    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '    set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux: \n'
            '    PATH=$PATH:/path/toyour/folder/ \n'
        )
    else:
        raise