""" Making a price retreiving tool for alternate quality gems in Path of Exile. """

import requests
import json
import tkinter as tk


server_endpoint = 'https://api.pathofexile.com'


response = requests.get('https://poe.ninja/api/data/itemoverview?league=Sanctum&type=SkillGem')

# From wiki retreive gems info with alt quality
#First item is like this 
# {'id': 96951, 
# 'name': 'Awakened Enlighten Support',
# 'icon': 'https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvR2Vtcy9TdXBwb3J0L1N1cHBvcnRQbHVzL0VubGlnaHRlbnBsdXMiLCJ3IjoxLCJoIjoxLCJzY2FsZSI6MX1d/7ec7d0544d/Enlightenplus.png',
# 'levelRequired': 80,
# 'variant': '5/23c',
# 'itemClass': 4,
# 'sparkline': {'data': [], 'totalChange': 0},
# 'lowConfidenceSparkline': {'data': [0, 7.29, 21.82, None, -1.19, -9.99, -1.52],
# 'totalChange': -1.52},
# 'implicitModifiers': [],
# 'explicitModifiers': [{'text': 'This Gem gains 115% increased Experience',
# 'optional': False}], 
# 'flavourText': '',
# 'corrupted': True, 
# 'gemLevel': 5, 'gemQuality': 23,
# 'chaosValue': 37800.84, 
# 'exaltedValue': 2196.45,
# 'divineValue': 154.0, 'count': 1,
# 'detailsId': 'awakened-enlighten-support-5-23c',
# 'listingCount': 1}



def get_gems_prices():
    """ Get gems from the server. """
    gem_prices = {}
    
    #threshold = input('Enter the threshold for gems in chaos: ')
    #if threshold == '':
    threshold = 0

    if response.status_code == 200:
    #print the field corrupted gems and not corrupted gems, sometimes the corrupted field is not present
        for item in response.json()['lines']:
            #Check name must contain Divergent, Anomalous or Phantasmal
            if 'Divergent' in item['name'] or 'Anomalous' in item['name'] or 'Phantasmal' in item['name']:
                if item.get('corrupted', False):
                    
                    #print(item['name'], item['chaosValue'],'chaos', item['exaltedValue'],'exalted', item['divineValue'],'divine')
                    #gem_prices[item['name']] = item['chaosValue']
                    pass
                else:
                    
                    #print(item['name'], item['chaosValue'],'chaos', item['exaltedValue'],'exalteds', item['divineValue'],'divines')

                    gem_prices[item['name']] = item['chaosValue']
    
    gem_price_sorted = sorted(gem_prices.items(), key=lambda x: x[1])
    
    #Divide in two list with support and active gems
    support_gems = [item for item in gem_price_sorted if 'Support' in item[0]]
    active_gems = [item for item in gem_price_sorted if 'Support' not in item[0]]
    
    support_gems_filtered = [item for item in support_gems if item[1] > threshold]
    active_gems_filtered = [item for item in active_gems if item[1] > threshold]
        

    return dict(support_gems_filtered), dict(active_gems_filtered)
 
def get_gems_weightings():
    """ Get gems weightings from the server. """
    
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'gemdata',
        'gdid': '-1'
    }
    
    response = requests.get('https://pathofexile.gamepedia.com/api.php', params=params)

     
    print('Showing weightings for each gem and type of gem')
    
    if response.status_code == 200:
        print(response.json())
    else:
        EOFError('Error getting gems weightings from the server')
    
    #Get the gem weightings from the server
    # Every gem has a weighting about how probable is to be changed with an item called lapidary lens
    # The higher the weighting the more probable is to be changed 
                
def show_all_gems():                
    gem_prices_support, gem_prices_actives = get_gems_prices()

    print('Showing support gems worth more than 100 chaos')

    for gem, price in gem_prices_support.items():
        print(gem, price)

    print('#'*50)

    print('Showing active gems worth more than 100 chaos')

    for gem, price in gem_prices_actives.items():
        print(gem, price)

    get_gems_weightings()

###################################################################################

# Create the root window
root = tk.Tk()
root.title("Gem Prices")

# Set the window size
root.geometry("1240x720")

# Create a button to show support gems
def show_support_gems():
    # Get the threshold from the slider
    threshold = slider.get()
    
    # Get the support gems
    support_gems, _ = get_gems_prices()
    
    # Filter the gems by the threshold
    support_gems = {k: v for k, v in support_gems.items() if v > threshold}
    
    # Clear the listbox
    listbox.delete(0, tk.END)
    
    # Add the gems to the listbox
    for gem, price in support_gems.items():
        listbox.insert(tk.END, f"{gem}: {price} chaos")
        
    #Make listbox bigger and show prices near each gem
    listbox.config(width=1000, height=1000)
    
    listbox.config(font=("Courier", 20))
    

support_button = tk.Button(root, text="Show Support Gems", command=show_support_gems)
support_button.pack()

# Create a button to show active gems
def show_active_gems():
    # Get the threshold from the slider
    threshold = slider.get()
    
    # Get the active gems
    _, active_gems = get_gems_prices()
    
    # Filter the gems by the threshold
    active_gems = {k: v for k, v in active_gems.items() if v > threshold}
    
    # Clear the listbox
    listbox.delete(0, tk.END)
    
    # Add the gems to the listbox
    for gem, price in active_gems.items():
        listbox.insert(tk.END, f"{gem}: {price} chaos")
        
    listbox.config(width=1000, height=1000)
    #Make text in listbox bigger and show prices near each gem
    listbox.config(font=("Courier", 20))

active_button = tk.Button(root, text="Show Active Gems", command=show_active_gems)
active_button.pack()


# add a search bar for gems that shows only searched gem after pressing search button and insert gem name
search_bar = tk.Entry(root)
search_bar.pack()

# Button to search 

button_search = tk.Button(root, text="Search")
#When pressed search button, show only searched gem
button_search.pack()
if button_search == True:
    #get text from search bar and look for it in the listbox showing only the searched gem
    search_bar.get()
    show_support_gems()
    show_active_gems()

    
# Create a slider to set the threshold
slider = tk.Scale(root, from_=0, to=1000, orient=tk.HORIZONTAL)
slider.pack()

# Create a listbox to display the gems
listbox = tk.Listbox(root)
listbox.pack()


# Start the main loop
root.mainloop()