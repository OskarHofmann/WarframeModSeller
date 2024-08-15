# WarframeModSeller
Script to check for the most profitbale augmentation mods of a syndicate in the game Warframe and automatically sell them via WarframeMarket

While I made this project mainly to sell syndicate mods and find the most profitable to sell at a given moment, this project can be used to evaluate and sell most Warframe items. For a more general library for the WarframeMarket API, check out the library from [AyajiLin](https://github.com/leonardodalinky/pywmapi).

## How to use
The example in main.py should give a good overview on how to use this project. To break it down:

https://github.com/OskarHofmann/WarframeModSeller/blob/f5c896600540c3d089214a1ac6937f91e0514f86/main.py#L12
uses the Warframe Wiki to read out all the augmentation mods from the given syndicate (here Red Veil). `mods` is just a list of mod names (as strings), so one can easily exchange this for other mods/items if needed.
<br/><br/>

https://github.com/OskarHofmann/WarframeModSeller/blob/f5c896600540c3d089214a1ac6937f91e0514f86/main.py#L13-L14
converts the mod/item names into `MarketItems` which allows to keep track of the WaframeMarket URL and ID of these mods/items.
<br/><br/>

https://github.com/OskarHofmann/WarframeModSeller/blob/f5c896600540c3d089214a1ac6937f91e0514f86/main.py#L18
uses the `SalesStrategy` `SellMostProfitable` to determine the current cheapest price of all given market items and determine the most profitable (i.e. most expensive) ones.
<br/><br/>

https://github.com/OskarHofmann/WarframeModSeller/blob/f5c896600540c3d089214a1ac6937f91e0514f86/main.py#L21
uses the `SalesAgent` `ManualSales`. This agent just prints the identified items to sell together with their price to the console. This line is not needed if the `AutomaticSales` agent is used.
<br/><br/>

https://github.com/OskarHofmann/WarframeModSeller/blob/f5c896600540c3d089214a1ac6937f91e0514f86/main.py#L24-L32
logs into an existing WarframeMarket account, which is needed for automatically listing the sales on WarframeMarket. The user must provide a .env file (the full filename should be ".env" without anything in front of the dot) in the same folder to provide the login credentials to Warframe Market. The file should look like this:
> WFM_MAIL=user@domain.com
> 
> WFM_PASSWORD=password123
<br/><br/>

Assuming a successfull login
https://github.com/OskarHofmann/WarframeModSeller/blob/f5c896600540c3d089214a1ac6937f91e0514f86/main.py#L34-L35
creates an `AutomaticSales` agent and lists the items on WarframeMarket
<br/><br/>

https://github.com/OskarHofmann/WarframeModSeller/blob/f5c896600540c3d089214a1ac6937f91e0514f86/main.py#L37
can then be used at the end to clean up the user's listings on WarframeMarket. Each of the user's listing of an item that is in `market_items` but was not listed by the agent in the previous step is deleted. This is especially usefull when selling syndicate mods to cleanup previous listings that are not the most profitable ones anymore.


