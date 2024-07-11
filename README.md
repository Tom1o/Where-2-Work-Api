<h1>Cafe API Website</h1>
<h2>About</h2>
<p>This is an API I created that can be used to find London cafes that you can bring a laptop to work in, using an SQL database to store all the cafe info.<br>It tells you, if it has wifi, plug sockets, if you can take calls there, if there are toilet facilites and the price of a coffee.</p>
<h2>How to use</h2>
<p>When you get to the homepage there are a few options:</p>
<img src='https://github.com/Tom1o/Where-2-Work-Api/assets/152978786/83092c14-50f6-49e0-8afe-aa6efd0b1bfa'>
<p>'Show all' and 'All Cafes' both bring you to a list of all the cafes currently stored, with the option to click straight on the Google Maps link to see it on the map.</p>
<img src='https://github.com/Tom1o/Where-2-Work-Api/assets/152978786/d3893353-f18c-46ce-9b41-3f585b0a7cd6'>
<p>Random cafe chooses one from the list at random and show the user the information about it</p>
<img src='https://github.com/Tom1o/Where-2-Work-Api/assets/152978786/9080edb5-687b-4771-a87e-ce396571ce25'>
<p>There are also a few API functions that can be used. The first being /add this brings up a form for you to add a new cafe to the list.</p>
<img src='https://github.com/user-attachments/assets/c24def13-f4e0-409f-b583-8efc3b2a270e'>
<p>There is also /search with the parameters being location for example: /search?loc=peckham would return all the cafes located in Peckham</p>
<img src='https://github.com/user-attachments/assets/313f4522-1e18-4e1d-b52e-4d252c81779b'>
<p>Finally there is the /update-price this also requires a cafe id. For example /update-price/1?new_price=2.50 would update the price of coffee in the first cafe on the list to be £2.50</p>
